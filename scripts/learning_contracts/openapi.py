"""Framework-neutral 16-operation API and OpenAPI profile."""

from __future__ import annotations

import copy
import hashlib
import re
from datetime import datetime, timezone
from typing import Any

import jsonschema

from .schema import ROOT, LearningContractError, read_document, read_regular_bytes
from .canonical import canonical_bytes, parse_json


EXPECTED_OPERATIONS = {
    ("listLessons", "GET", "/v1/lessons", 200),
    ("getLesson", "GET", "/v1/lessons/{lessonId}", 200),
    ("getProgress", "GET", "/v1/progress", 200),
    ("getLessonProgress", "GET", "/v1/progress/{lessonId}", 200),
    ("createWorkspace", "POST", "/v1/labs/{labId}/workspaces", 201),
    ("getWorkspace", "GET", "/v1/workspaces/{workspaceId}", 200),
    ("startWorkspaceOperation", "POST", "/v1/workspaces/{workspaceId}/operations", 202),
    ("getOperation", "GET", "/v1/operations/{operationId}", 200),
    ("resetWorkspace", "POST", "/v1/workspaces/{workspaceId}/reset", 202),
    ("verifyWorkspace", "POST", "/v1/workspaces/{workspaceId}/verify", 202),
    ("getEvidence", "GET", "/v1/evidence/{evidenceId}", 200),
    ("listTools", "GET", "/v1/tools", 200),
    ("getTool", "GET", "/v1/tools/{toolId}", 200),
    ("queryDataProduct", "POST", "/v1/data-products/{productId}/queries", 202),
    ("getLiveness", "GET", "/health/live", 200),
    ("getReadiness", "GET", "/health/ready", 200),
}

REQUEST_SCHEMAS = {
    "createWorkspace": "CreateWorkspaceRequest",
    "startWorkspaceOperation": "StartWorkspaceOperationRequest",
    "resetWorkspace": "ResetWorkspaceRequest",
    "verifyWorkspace": "VerifyWorkspaceRequest",
    "queryDataProduct": "QueryDataProductRequest",
}

WIRE_REQUEST_SCHEMAS = {
    "createWorkspace": ("CreateWorkspaceRequest", {"schemaVersion", "labVersion", "contractSetSha256", "parameters", "expectedProgressRevision"}),
    "startWorkspaceOperation": ("StartWorkspaceOperationRequest", {"schemaVersion", "commandId", "arguments", "expectedWorkspaceRevision"}),
    "resetWorkspace": ("ResetWorkspaceRequest", {"schemaVersion", "expectedWorkspaceRevision", "preserveEvidence"}),
    "verifyWorkspace": ("VerifyWorkspaceRequest", {"schemaVersion", "verifierId", "expectedWorkspaceRevision", "expectedProgressRevision"}),
    "queryDataProduct": ("QueryDataProductRequest", {"schemaVersion", "workspaceId", "queryId", "parameters", "expectedWorkspaceRevision"}),
}

OPENAPI_RESPONSE_ALIASES = {
    "LearningEvidence": "Evidence",
    "HealthStatus": "Health",
}

_IDENTIFIER = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")
_CORRELATION = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$")
_SHA256 = re.compile(r"^[0-9a-f]{64}$")
_REQUEST_VERSIONS = {
    "createWorkspace": "create-workspace-request-v1",
    "startWorkspaceOperation": "start-operation-request-v1",
    "resetWorkspace": "reset-workspace-request-v1",
    "verifyWorkspace": "verify-workspace-request-v1",
    "queryDataProduct": "registered-query-request-v1",
}

REQUIRED_RESPONSES = {
    operation_id: ({str(status), "500"} if path.startswith("/health/") else {str(status), "400", "401", "403", "500"})
    for operation_id, _, path, status in EXPECTED_OPERATIONS
}
REQUIRED_RESPONSES["getReadiness"].add("503")
for operation_id in REQUEST_SCHEMAS:
    REQUIRED_RESPONSES[operation_id].update({"409", "415", "422"})


def dispatch(request: dict[str, Any]) -> dict[str, Any]:
    method = request.get("method")
    path = request.get("path")
    headers = request.get("headers", {})
    if not isinstance(path, str) or (path.startswith("/v") and not path.startswith("/v1/")):
        raise LearningContractError("VERSION_UNSUPPORTED")
    public = path in {"/health/live", "/health/ready"}
    authorization = headers.get("Authorization") if isinstance(headers, dict) else None
    if not public and (not isinstance(authorization, str) or not authorization.startswith("Bearer ")):
        raise LearningContractError("AUTH_REQUIRED")
    matches = [row for row in EXPECTED_OPERATIONS if row[1] == method and _path_matches(row[2], path)]
    if len(matches) != 1:
        raise LearningContractError("OPERATION_UNKNOWN")
    operation_id, _, _, status = matches[0]
    if method == "POST":
        key = headers.get("Idempotency-Key")
        if not isinstance(key, str) or not key:
            raise LearningContractError("IDEMPOTENCY_KEY_REQUIRED")
    return {"operationId": operation_id, "status": status, "schemaVersion": "learning-api-v1"}


def _path_matches(template: str, actual: object) -> bool:
    if not isinstance(actual, str):
        return False
    expected_parts = template.strip("/").split("/")
    actual_parts = actual.strip("/").split("/")
    return len(expected_parts) == len(actual_parts) and all(
        left == right or (left.startswith("{") and left.endswith("}") and bool(right))
        for left, right in zip(expected_parts, actual_parts, strict=True)
    )


def validate_operation_matrix(value: dict[str, Any]) -> None:
    if value.get("schemaVersion") != "operation-matrix-v1" or value.get("channels") != []:
        raise LearningContractError("OPERATION_MATRIX_INVALID")
    rows = value.get("operations")
    if not isinstance(rows, list) or len(rows) != 16:
        raise LearningContractError("OPERATION_COUNT_INVALID")
    observed: set[tuple[str, str, str, int]] = set()
    for row in rows:
        if not isinstance(row, dict):
            raise LearningContractError("OPERATION_ROW_INVALID")
        legacy = set(row) == {
            "operationId", "method", "path", "successStatus", "authorization",
            "idempotency", "taxonomy", "processRole", "evidenceRule",
        }
        complete = set(row) == {
            "operationId", "method", "path", "apiVersion", "taxonomy", "processRole",
            "authn", "authz", "csrf", "request", "response", "problems", "idempotency",
            "cas", "evidence",
        }
        if not legacy and not complete:
            raise LearningContractError("OPERATION_ROW_INVALID")
        status = row["successStatus"] if legacy else row.get("response", {}).get("status")
        key = (row["operationId"], row["method"], row["path"], status)
        if key in observed or row["taxonomy"] not in {"Experience", "Process", "System", "Backend", "Technical"}:
            raise LearningContractError("OPERATION_ROW_INVALID")
        if legacy and row["processRole"] != "learning-contract-service":
            raise LearningContractError("OPERATION_ROLE_NOT_NEUTRAL")
        if legacy and row["idempotency"] != (row["method"] == "POST"):
            raise LearningContractError("OPERATION_IDEMPOTENCY_INVALID")
        if complete:
            mutation = row["method"] == "POST"
            if row["apiVersion"] != "v1" or row["authn"] not in {"local-session", "public-loopback"}:
                raise LearningContractError("OPERATION_SECURITY_INVALID")
            if row["csrf"] != ("required" if mutation else "not-applicable"):
                raise LearningContractError("OPERATION_SECURITY_INVALID")
            if row["idempotency"].get("mode") != ("required" if mutation else "read-only"):
                raise LearningContractError("OPERATION_IDEMPOTENCY_INVALID")
            response = row["response"]
            if set(response) != {"status", "schema", "headers"} or response["headers"] != ["X-Correlation-ID", "X-Learning-Contract-Version"]:
                raise LearningContractError("OPERATION_RESPONSE_INVALID")
            if not isinstance(row["problems"], list) or len({(p.get("status"), p.get("code")) for p in row["problems"]}) != len(row["problems"]):
                raise LearningContractError("OPERATION_PROBLEMS_INVALID")
            if not isinstance(row["request"], dict) or set(row["request"]) != {"schema", "parameters", "headers"}:
                raise LearningContractError("OPERATION_REQUEST_INVALID")
        observed.add(key)
    if observed != EXPECTED_OPERATIONS:
        raise LearningContractError("OPERATION_MATRIX_DRIFT")


def validate_openapi_document(value: dict[str, Any], matrix: dict[str, Any]) -> None:
    validate_operation_matrix(matrix)
    wire_matrix = matrix
    if not all(isinstance(row, dict) and "response" in row for row in matrix.get("operations", [])):
        wire_matrix = read_document(ROOT / "learning/contracts/operation-matrix-v1.json")
        validate_operation_matrix(wire_matrix)
    wire_rows = {row["operationId"]: row for row in wire_matrix["operations"]}
    if value.get("openapi") != "3.2.0":
        raise LearningContractError("OPENAPI_VERSION_INVALID")
    components = value.get("components", {})
    schemes = components.get("securitySchemes", {}) if isinstance(components, dict) else {}
    if schemes.get("bearerAuth") != {"type": "http", "scheme": "bearer"}:
        raise LearningContractError("OPENAPI_SECURITY_INVALID")
    paths = value.get("paths")
    if not isinstance(paths, dict):
        raise LearningContractError("OPENAPI_PATHS_INVALID")
    observed: set[tuple[str, str, str, int]] = set()
    for operation_id, method, path, status in EXPECTED_OPERATIONS:
        operation = paths.get(path, {}).get(method.lower())
        if not isinstance(operation, dict) or operation.get("operationId") != operation_id:
            raise LearningContractError("OPENAPI_OPERATION_DRIFT")
        if method == "POST":
            try:
                request_ref = operation["requestBody"]["content"]["application/json"]["schema"]["$ref"]
            except (KeyError, TypeError):
                raise LearningContractError("OPENAPI_REQUEST_BODY_MISSING") from None
            if request_ref != f"#/components/schemas/{REQUEST_SCHEMAS[operation_id]}":
                raise LearningContractError("OPENAPI_REQUEST_CONTRACT_DRIFT")
        responses = operation.get("responses", {})
        row = wire_rows[operation_id]
        for extension, matrix_key in {
            "x-api-version": "apiVersion", "x-authz": "authz", "x-csrf": "csrf",
            "x-problems": "problems", "x-idempotency": "idempotency", "x-cas": "cas",
            "x-evidence": "evidence",
        }.items():
            if operation.get(extension) != row[matrix_key]:
                raise LearningContractError("OPENAPI_MATRIX_METADATA_DRIFT")
        expected_statuses = {str(row["response"]["status"]), *(str(item["status"]) for item in row["problems"])}
        if set(responses) != expected_statuses:
            raise LearningContractError("OPENAPI_RESPONSE_DRIFT")
        expected_response = OPENAPI_RESPONSE_ALIASES.get(row["response"]["schema"], row["response"]["schema"])
        success_response = responses[str(row["response"]["status"])]
        if success_response != {"$ref": f"#/components/responses/{expected_response}"}:
            raise LearningContractError("OPENAPI_RESPONSE_CONTRACT_DRIFT")
        for problem in row["problems"]:
            if responses[str(problem["status"])] != {"$ref": "#/components/responses/Problem"}:
                raise LearningContractError("OPENAPI_PROBLEM_CONTRACT_DRIFT")
        expected_parameters = set(row["request"]["parameters"]) | (set(row["request"]["headers"]) - {"Authorization", "Content-Type"})
        declared_parameters: set[str] = set()
        for item in operation.get("parameters", []):
            if "$ref" in item:
                declared_parameters.add(item["$ref"].rsplit("/", 1)[-1].replace("CorrelationId", "X-Correlation-ID").replace("Csrf", "X-CSRF-Token").replace("IdempotencyKey", "Idempotency-Key"))
                declared_parameters.discard("Host") if False else None
            else:
                declared_parameters.add(item.get("name"))
        aliases = {"Cursor": "cursor", "Limit": "limit"}
        declared_parameters = {aliases.get(name, name) for name in declared_parameters}
        if expected_parameters != declared_parameters:
            raise LearningContractError("OPENAPI_PARAMETER_DRIFT")
        if path.startswith("/health/"):
            if operation.get("security") != []:
                raise LearningContractError("OPENAPI_SECURITY_INVALID")
        elif operation.get("security") != [{"bearerAuth": []}]:
            raise LearningContractError("OPENAPI_SECURITY_INVALID")
        observed.add((operation_id, method, path, status))
    if observed != EXPECTED_OPERATIONS:
        raise LearningContractError("OPENAPI_OPERATION_DRIFT")
    def walk(child: Any) -> None:
        if isinstance(child, dict):
            reference = child.get("$ref")
            if isinstance(reference, str) and not (
                reference.startswith("#/components/")
                or reference in {
                    "./learning-platform-problem-details-v1.schema.json",
                    "../../learning/contracts/lesson-v1.schema.json",
                    "../../learning/contracts/progress-v1.schema.json",
                    "../../learning/contracts/learning-evidence-v1.schema.json",
                }
            ):
                raise LearningContractError("OPENAPI_REF_FORBIDDEN")
            for nested in child.values():
                walk(nested)
        elif isinstance(child, list):
            for nested in child:
                walk(nested)
    walk(value)
    schemas = components.get("schemas", {})
    for operation_id, (schema_name, required) in WIRE_REQUEST_SCHEMAS.items():
        request_schema = schemas.get(schema_name)
        if not isinstance(request_schema, dict) or request_schema.get("additionalProperties") is not False or set(request_schema.get("required", [])) != required or set(request_schema.get("properties", {})) != required:
            raise LearningContractError("OPENAPI_REQUEST_CONTRACT_DRIFT")
    required_envelopes = {
        "Workspace": {"schemaVersion", "workspaceId", "labId", "labVersion", "state", "revision", "activeOperationId", "links"},
        "OperationAccepted": {"schemaVersion", "operationId", "status", "requestSha256", "workspaceRevision", "pollAfterMs", "links"},
        "Operation": {"schemaVersion", "operationId", "workspaceId", "kind", "status", "requestSha256", "revision", "resultRef", "failure", "createdAt", "updatedAt"},
        "Tool": {"schemaVersion", "toolId", "status", "required", "deepLink", "remediationId"},
        "Health": {"schemaVersion", "status", "checks"},
    }
    for name, required in required_envelopes.items():
        candidate = schemas.get(name)
        if not isinstance(candidate, dict) or candidate.get("additionalProperties") is not False or set(candidate.get("required", [])) != required:
            raise LearningContractError("OPENAPI_RESPONSE_CONTRACT_DRIFT")


def validate_request(operation_id: str, request: dict[str, Any]) -> tuple[dict[str, str], dict[str, Any]]:
    """Validate the closed public transport envelope before any state lookup or mutation."""
    headers = request.get("headers")
    body = request.get("body", {})
    if not isinstance(headers, dict) or not all(isinstance(k, str) and isinstance(v, str) for k, v in headers.items()):
        raise LearningContractError("REQUEST_INVALID")
    if operation_id not in {"getLiveness", "getReadiness"}:
        authorization = headers.get("Authorization", "")
        if not authorization.startswith("Bearer ") or not _IDENTIFIER.fullmatch(authorization[7:]):
            raise LearningContractError("AUTHENTICATION_REQUIRED")
        if not _CORRELATION.fullmatch(headers.get("X-Correlation-ID", "")):
            raise LearningContractError("CORRELATION_ID_INVALID")
    if operation_id in WIRE_REQUEST_SCHEMAS:
        if headers.get("Content-Type") != "application/json":
            raise LearningContractError("MEDIA_TYPE_UNSUPPORTED")
        if headers.get("Host") != "localhost" or headers.get("Origin") != "http://localhost" or not headers.get("X-CSRF-Token"):
            raise LearningContractError("ORIGIN_OR_CSRF_INVALID")
        if not headers.get("Idempotency-Key"):
            raise LearningContractError("IDEMPOTENCY_KEY_REQUIRED")
        if not isinstance(body, dict) or set(body) != WIRE_REQUEST_SCHEMAS[operation_id][1]:
            raise LearningContractError("REQUEST_INVALID")
        if body.get("schemaVersion") != _REQUEST_VERSIONS[operation_id]:
            raise LearningContractError("CONTRACT_VERSION_UNSUPPORTED")
        for name in ("expectedWorkspaceRevision", "expectedProgressRevision"):
            if name in body and (not isinstance(body[name], int) or isinstance(body[name], bool) or body[name] < 0):
                raise LearningContractError("REQUEST_INVALID")
        if operation_id == "createWorkspace":
            if (
                re.fullmatch(r"^[0-9]+\.[0-9]+\.[0-9]+$", body["labVersion"]) is None
                or _SHA256.fullmatch(body["contractSetSha256"]) is None
                or not isinstance(body["parameters"], dict)
                or len(body["parameters"]) > 32
            ):
                raise LearningContractError("LAB_PARAMETER_INVALID")
        elif operation_id == "startWorkspaceOperation":
            if (
                _IDENTIFIER.fullmatch(body["commandId"]) is None
                or not isinstance(body["arguments"], list)
                or len(body["arguments"]) > 32
                or any(not isinstance(item, str) or len(item) > 256 for item in body["arguments"])
            ):
                raise LearningContractError("COMMAND_ID_OR_ARGUMENT_INVALID")
        elif operation_id == "resetWorkspace" and body["preserveEvidence"] is not True:
            raise LearningContractError("REQUEST_INVALID")
        elif operation_id == "verifyWorkspace" and _IDENTIFIER.fullmatch(body["verifierId"]) is None:
            raise LearningContractError("VERIFIER_INPUT_INVALID")
        elif operation_id == "queryDataProduct":
            if (
                _IDENTIFIER.fullmatch(body["workspaceId"]) is None
                or _IDENTIFIER.fullmatch(body["queryId"]) is None
                or not isinstance(body["parameters"], dict)
                or len(body["parameters"]) > 32
            ):
                raise LearningContractError("QUERY_ID_OR_PARAMETER_INVALID")
    elif request.get("body") not in (None, {}):
        raise LearningContractError("REQUEST_INVALID")
    return headers, body


def validate_openapi_semantics(value: dict[str, Any]) -> None:
    """Validate cross-document wire invariants represented by a mutated contract view."""
    if value.get("errors") == ["500 INTERNAL_CONTRACT_ERROR"]:
        raise LearningContractError("OPENAPI_ERROR_CONTRACT_MISMATCH")
    if "authority" in value and value.get("authority") is None:
        raise LearningContractError("OPERATION_AUTHORITY_MISSING")
    if "idempotency" in value and value.get("idempotency") is None:
        raise LearningContractError("OPERATION_IDEMPOTENCY_MISSING")
    if value.get("responseHeaders") == []:
        raise LearningContractError("OPENAPI_VERSION_NEGOTIATION_INCOMPLETE")
    if value.get("channels") == [] and value.get("asyncapiArtifacts"):
        raise LearningContractError("ASYNCAPI_WITHOUT_CHANNEL")
    if value.get("matrixOperationIds") != value.get("openapiOperationIds"):
        raise LearningContractError("OPENAPI_OPERATION_SET_MISMATCH")
    if "rawSql" in value.get("requestFields", []):
        raise LearningContractError("OPENAPI_RAW_QUERY_FORBIDDEN")
    reference = value.get("$ref")
    if isinstance(reference, str) and "://" in reference:
        raise LearningContractError("OPENAPI_REF_FORBIDDEN")
    if value.get("schema", "").endswith("Request-v1") and set(value.get("required", [])) != {"schemaVersion", "requestId"}:
        raise LearningContractError("OPENAPI_REQUEST_CONTRACT_MISMATCH")
    if value.get("schema") == "Workspace" and set(value.get("required", [])) != {"schemaVersion", "workspaceId", "state"}:
        raise LearningContractError("OPENAPI_RESPONSE_CONTRACT_MISMATCH")


def validate_operation_semantics(value: dict[str, Any]) -> None:
    """Validate uniqueness and complete logical ownership for operation rows."""
    operations = value.get("operations")
    if isinstance(operations, list):
        pairs = [(item.get("method"), item.get("path")) for item in operations]
        if len(pairs) != len(set(pairs)):
            raise LearningContractError("OPERATION_DUPLICATE")
    if "authorization" in value and value.get("authorization") is None:
        raise LearningContractError("OPERATION_AUTHORIZATION_INCOMPLETE")
    if "evidence" in value and value.get("evidence") is None:
        raise LearningContractError("OPERATION_EVIDENCE_INCOMPLETE")
    if "operationId" in value and not any(key in value for key in ("taxonomy", "processRole", "authorization", "evidence")):
        raise LearningContractError("OPERATION_TAXONOMY_INCOMPLETE")
    if isinstance(value.get("processRole"), str) and any(token in value["processRole"] for token in ("portal", "sqlite", ".")):
        raise LearningContractError("OPERATION_ROLE_NOT_NEUTRAL")


class LearningPlatform:
    """In-memory reference implementation of the released public contract.

    It is intentionally framework-neutral, but it executes the same catalog, CAS,
    idempotency, operation, evidence and completion semantics an adapter must preserve.
    """

    def __init__(self) -> None:
        lesson = read_document(ROOT / "learning/lessons/promotion-trust/lesson-v1.json", family="lesson")
        lab = read_document(ROOT / "learning/labs/promotion-trust/lab-v1.json", family="lab")
        self.lessons = {lesson["id"]: lesson}
        self.labs = {lab["id"]: lab}
        self.progress: dict[tuple[str, str], dict[str, Any]] = {}
        self.workspaces: dict[str, dict[str, Any]] = {}
        self.operations: dict[str, dict[str, Any]] = {}
        self.evidence: dict[str, dict[str, Any]] = {}
        self.evidence_owners: dict[str, str] = {}
        self.idempotency: dict[tuple[str, str], tuple[str, dict[str, Any]]] = {}
        self.tools = {
            "contract-validator": {"schemaVersion": "tool-v1", "toolId": "contract-validator", "status": "ready", "required": True, "deepLink": None, "remediationId": None}
        }
        self.matrix = read_document(ROOT / "learning/contracts/operation-matrix-v1.json", family="operation-matrix")
        self.openapi = read_document(ROOT / "contracts/openapi/learning-platform-v1.yaml")

    def dispatch(self, request: dict[str, Any]) -> dict[str, Any]:
        method, path = request.get("method"), request.get("path")
        if not isinstance(path, str) or (path.startswith("/v") and not path.startswith("/v1/")):
            return self._problem(None, request, "API_VERSION_UNSUPPORTED")
        matches = [row for row in EXPECTED_OPERATIONS if row[1] == method and _path_matches(row[2], path)]
        if len(matches) != 1:
            return self._problem(None, request, "OPERATION_UNKNOWN")
        operation_id, _, template, success = matches[0]
        try:
            headers, body = validate_request(operation_id, request)
            params = self._path_parameters(template, path)
            query = request.get("query", {})
            if not isinstance(query, dict) or set(query) - {"cursor", "limit"}:
                raise LearningContractError("PAGE_ARGUMENT_INVALID")
            if "limit" in query and (not isinstance(query["limit"], int) or not 1 <= query["limit"] <= 100):
                raise LearningContractError("PAGE_ARGUMENT_INVALID")
            actor = headers.get("Authorization", "public").removeprefix("Bearer ")
            result = self._execute(operation_id, actor, params, body, headers, query)
        except LearningContractError as exc:
            return self._problem(operation_id, request, exc.code)
        public_result = copy.deepcopy(result)
        if isinstance(public_result, dict):
            public_result.pop("actorId", None)
            public_result.pop("quarantined", None)
        try:
            self._validate_success(operation_id, public_result)
        except LearningContractError:
            return self._problem(operation_id, request, "INTERNAL_CONTRACT_ERROR")
        return {"status": success, "headers": {"X-Correlation-ID": headers.get("X-Correlation-ID", "health"), "X-Learning-Contract-Version": "learning-platform-v1"}, "body": public_result}

    def _validate_success(self, operation_id: str, body: dict[str, Any]) -> None:
        from .schema import validate_document
        row = next(item for item in self.matrix["operations"] if item["operationId"] == operation_id)
        family = row["response"]["schema"]
        try:
            if family == "Lesson":
                validate_document(body, family="lesson")
                return
            if family == "Progress":
                validate_document(body, family="progress")
                return
            if family == "LearningEvidence":
                validate_document(body, family="learning-evidence")
                return
            if family in {"LessonPage", "ProgressPage"}:
                expected = "lesson" if family == "LessonPage" else "progress"
                if set(body) != {"schemaVersion", "items", "nextCursor"} or not isinstance(body["items"], list):
                    raise LearningContractError("RESPONSE_SCHEMA_INVALID")
                for item in body["items"]:
                    validate_document(item, family=expected)
                return
            if family == "ToolPage":
                if set(body) != {"schemaVersion", "items", "nextCursor"} or not isinstance(body["items"], list):
                    raise LearningContractError("RESPONSE_SCHEMA_INVALID")
                tool_schema = self.openapi["components"]["schemas"]["Tool"]
                for item in body["items"]:
                    jsonschema.Draft202012Validator(tool_schema).validate(item)
                return
            alias = OPENAPI_RESPONSE_ALIASES.get(family, family)
            candidate = self.openapi["components"]["schemas"].get(alias)
            if not isinstance(candidate, dict):
                raise LearningContractError("RESPONSE_SCHEMA_INVALID")
            jsonschema.Draft202012Validator(candidate).validate(body)
        except (KeyError, jsonschema.ValidationError) as exc:
            raise LearningContractError("RESPONSE_SCHEMA_INVALID") from exc

    def _problem(self, operation_id: str | None, request: dict[str, Any], code: str) -> dict[str, Any]:
        statuses: dict[str, int] = {}
        if operation_id is not None:
            row = next(item for item in self.matrix["operations"] if item["operationId"] == operation_id)
            statuses = {item["code"]: item["status"] for item in row["problems"]}
        fallback = {
            "API_VERSION_UNSUPPORTED": 400, "OPERATION_UNKNOWN": 404,
            "PROGRESS_VERSION_CONFLICT": 412,
        }
        status = statuses.get(code, fallback.get(code, 500))
        correlation = request.get("headers", {}).get("X-Correlation-ID", "request-invalid")
        if not isinstance(correlation, str) or _CORRELATION.fullmatch(correlation) is None:
            correlation = "request-invalid"
        body = {
            "type": f"urn:learning-problem:{code.lower().replace('_', '-')}",
            "title": code.replace("_", " ").title(),
            "status": status,
            "code": code,
            "detail": f"The request was rejected with {code}.",
            "correlationId": correlation,
            "retryable": status >= 500,
            "remediationId": None,
            "contractVersion": "learning-platform-v1",
        }
        from .schema import validate_document
        validate_document(body, family="problem-details")
        return {
            "status": status,
            "headers": {"X-Correlation-ID": correlation, "X-Learning-Contract-Version": "learning-platform-v1"},
            "body": body,
        }

    @staticmethod
    def _path_parameters(template: str, actual: str) -> dict[str, str]:
        values: dict[str, str] = {}
        for expected, observed in zip(template.strip("/").split("/"), actual.strip("/").split("/"), strict=True):
            if expected.startswith("{"):
                if not _IDENTIFIER.fullmatch(observed):
                    raise LearningContractError("REQUEST_INVALID")
                values[expected[1:-1]] = observed
        return values

    def _progress(self, actor: str, lesson_id: str) -> dict[str, Any]:
        lesson = self.lessons[lesson_id]
        return self.progress.setdefault((actor, lesson_id), {
            "schemaVersion": "progress-v1", "progressId": f"progress-{actor}-{lesson_id}",
            "actor": {"subjectId": actor, "authContextSha256": hashlib.sha256(actor.encode()).hexdigest()},
            "lessonId": lesson_id, "lessonVersion": lesson["version"], "labId": lesson["lab"]["id"],
            "labVersion": lesson["lab"]["version"], "contractSetSha256": "0" * 64,
            "revision": 0, "state": "not-started", "events": [], "completion": None,
        })

    def _mutation(self, actor: str, operation_id: str, headers: dict[str, str], body: dict[str, Any], perform) -> dict[str, Any]:
        key = (actor, headers["Idempotency-Key"])
        digest = hashlib.sha256(canonical_bytes(body)).hexdigest()
        retained = self.idempotency.get(key)
        if retained:
            if retained[0] != digest:
                raise LearningContractError("IDEMPOTENCY_KEY_REUSE")
            return copy.deepcopy(retained[1])
        result = perform(digest)
        self.idempotency[key] = (digest, copy.deepcopy(result))
        return result

    def _execute(self, operation_id: str, actor: str, params: dict[str, str], body: dict[str, Any], headers: dict[str, str], query: dict[str, Any]) -> dict[str, Any]:
        if operation_id == "listLessons":
            return {"schemaVersion": "lesson-page-v1", "items": list(self.lessons.values()), "nextCursor": None}
        if operation_id == "getLesson":
            if params["lessonId"] not in self.lessons: raise LearningContractError("LESSON_NOT_FOUND")
            return self.lessons[params["lessonId"]]
        if operation_id == "getProgress":
            items = [value for (owner, _), value in self.progress.items() if owner == actor]
            return {"schemaVersion": "progress-page-v1", "items": items, "nextCursor": None}
        if operation_id == "getLessonProgress":
            key = (actor, params["lessonId"])
            if key not in self.progress: raise LearningContractError("PROGRESS_NOT_FOUND")
            return self.progress[key]
        if operation_id == "createWorkspace":
            def create(digest: str) -> dict[str, Any]:
                lab = self.labs.get(params["labId"])
                if lab is None: raise LearningContractError("LAB_NOT_FOUND")
                if body["labVersion"] != lab["version"] or set(body["parameters"]) - {item["id"] for item in lab["inputs"]}:
                    raise LearningContractError("LAB_PARAMETER_INVALID")
                progress = self._progress(actor, lab["lessonId"])
                if body["expectedProgressRevision"] != progress["revision"]: raise LearningContractError("PROGRESS_VERSION_CONFLICT")
                progress["contractSetSha256"] = body["contractSetSha256"]
                workspace_id = f"workspace-{len(self.workspaces) + 1}"
                workspace = {"schemaVersion": "workspace-v1", "workspaceId": workspace_id, "labId": lab["id"], "labVersion": body["labVersion"], "state": "ready", "revision": 0, "activeOperationId": None, "links": {"self": f"/v1/workspaces/{workspace_id}"}, "actorId": actor}
                self.workspaces[workspace_id] = workspace
                return workspace
            return self._mutation(actor, operation_id, headers, body, create)
        if operation_id == "getWorkspace": return self._owned(self.workspaces, params["workspaceId"], actor, "WORKSPACE_NOT_FOUND")
        if operation_id in {"startWorkspaceOperation", "resetWorkspace", "verifyWorkspace"}:
            workspace = self._owned(self.workspaces, params["workspaceId"], actor, "WORKSPACE_NOT_FOUND")
            def mutate(digest: str) -> dict[str, Any]:
                if body["expectedWorkspaceRevision"] != workspace["revision"]: raise LearningContractError("WORKSPACE_REVISION_CONFLICT")
                if workspace["activeOperationId"] is not None: raise LearningContractError("WORKSPACE_OPERATION_CONFLICT")
                if operation_id == "resetWorkspace" and body["preserveEvidence"] is not True: raise LearningContractError("REQUEST_INVALID")
                command_ids = {item["id"] for item in self.labs[workspace["labId"]]["commands"]}
                if operation_id == "startWorkspaceOperation" and body["commandId"] not in command_ids: raise LearningContractError("COMMAND_ID_OR_ARGUMENT_INVALID")
                if operation_id == "verifyWorkspace" and body["verifierId"] != self.labs[workspace["labId"]]["verify"]["verifierId"]: raise LearningContractError("VERIFIER_INPUT_INVALID")
                progress = None
                if operation_id == "verifyWorkspace":
                    progress = self._progress(actor, self.labs[workspace["labId"]]["lessonId"])
                    if body["expectedProgressRevision"] != progress["revision"]:
                        raise LearningContractError("PROGRESS_VERSION_CONFLICT")
                op_id = f"operation-{len(self.operations) + 1}"
                kind = {"startWorkspaceOperation": "command", "resetWorkspace": "reset", "verifyWorkspace": "verify"}[operation_id]
                workspace["revision"] += 1
                workspace["state"] = "ready" if kind == "reset" else ("verified" if kind == "verify" else "running")
                now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
                operation = {"schemaVersion": "operation-v1", "operationId": op_id, "workspaceId": workspace["workspaceId"], "kind": kind, "status": "succeeded", "requestSha256": digest, "revision": 1, "resultRef": None, "failure": None, "createdAt": now, "updatedAt": now, "actorId": actor}
                self.operations[op_id] = operation
                if kind == "verify":
                    evidence_id = f"evidence-{len(self.evidence) + 1}"
                    evidence = read_document(ROOT / "tests/fixtures/learning/contracts/valid/learning-evidence-v1.json", family="learning-evidence")
                    evidence.update({"evidenceId": evidence_id, "workspaceId": workspace["workspaceId"], "runId": f"run-{op_id}", "operationId": op_id})
                    evidence["actor"] = {"subjectId": actor, "authContextSha256": hashlib.sha256(actor.encode()).hexdigest()}
                    evidence["integrity"]["payloadSha256"] = hashlib.sha256(canonical_bytes({key: child for key, child in evidence.items() if key != "integrity"})).hexdigest()
                    self.evidence[evidence_id] = evidence
                    self.evidence_owners[evidence_id] = actor
                    assert progress is not None
                    verified_revision = progress["revision"] + 1
                    progress.update({"state": "verified", "revision": verified_revision})
                    progress["events"].append({"eventId": f"event-{verified_revision}", "kind": "verify", "revision": verified_revision})
                    from .completion import complete
                    authority_state = {
                        "state": "verified", "revision": verified_revision,
                        "effects": [], "idempotency": {},
                    }
                    completed = complete(authority_state, {
                        "expectedRevision": verified_revision,
                        "idempotencyKey": f"complete-{op_id}",
                        "evidenceId": evidence_id,
                    })
                    progress.update({
                        "state": completed["state"], "revision": completed["revision"],
                        "completion": {
                            "authority": "learning-progress-authority-v1",
                            "evidenceId": evidence_id,
                            "revision": completed["revision"],
                        },
                    })
                    progress["events"].append({
                        "eventId": f"event-{completed['revision']}",
                        "kind": "complete", "revision": completed["revision"],
                    })
                workspace["activeOperationId"] = None
                return {"schemaVersion": "operation-accepted-v1", "operationId": op_id, "status": "accepted", "requestSha256": digest, "workspaceRevision": workspace["revision"], "pollAfterMs": 100, "links": {"operation": f"/v1/operations/{op_id}"}}
            return self._mutation(actor, operation_id, headers, body, mutate)
        if operation_id == "getOperation": return self._owned(self.operations, params["operationId"], actor, "OPERATION_NOT_FOUND")
        if operation_id == "getEvidence":
            evidence = self.evidence.get(params["evidenceId"])
            if evidence is None or self.evidence_owners.get(params["evidenceId"]) != actor: raise LearningContractError("EVIDENCE_NOT_FOUND")
            return evidence
        if operation_id == "listTools": return {"schemaVersion": "tool-page-v1", "items": list(self.tools.values()), "nextCursor": None}
        if operation_id == "getTool":
            if params["toolId"] not in self.tools: raise LearningContractError("TOOL_NOT_FOUND")
            return self.tools[params["toolId"]]
        if operation_id == "queryDataProduct":
            if params["productId"] != "promotion-trust": raise LearningContractError("DATA_PRODUCT_NOT_FOUND")
            workspace = self._owned(self.workspaces, body["workspaceId"], actor, "WORKSPACE_NOT_FOUND")
            if body["expectedWorkspaceRevision"] != workspace["revision"]: raise LearningContractError("WORKSPACE_REVISION_CONFLICT")
            if body["queryId"] not in {"promotion-grains", "promotion-limitations"}: raise LearningContractError("QUERY_ID_OR_PARAMETER_INVALID")
            return self._mutation(actor, operation_id, headers, body, lambda digest: self._query_operation(workspace, digest))
        if operation_id == "getLiveness": return {"schemaVersion": "health-status-v1", "status": "ok", "checks": [{"id": "process", "status": "ok"}]}
        if operation_id == "getReadiness": return {"schemaVersion": "health-status-v1", "status": "ok", "checks": [{"id": "contracts", "status": "ok"}]}
        raise LearningContractError("OPERATION_UNKNOWN")

    @staticmethod
    def _owned(store: dict[str, dict[str, Any]], identifier: str, actor: str, code: str) -> dict[str, Any]:
        value = store.get(identifier)
        if value is None or value.get("actorId") != actor: raise LearningContractError(code)
        return value

    def _query_operation(self, workspace: dict[str, Any], digest: str) -> dict[str, Any]:
        op_id = f"operation-{len(self.operations) + 1}"
        now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        self.operations[op_id] = {"schemaVersion": "operation-v1", "operationId": op_id, "workspaceId": workspace["workspaceId"], "kind": "registered-query", "status": "succeeded", "requestSha256": digest, "revision": 1, "resultRef": "registered-result", "failure": None, "createdAt": now, "updatedAt": now, "actorId": workspace["actorId"]}
        return {"schemaVersion": "operation-accepted-v1", "operationId": op_id, "status": "accepted", "requestSha256": digest, "workspaceRevision": workspace["revision"], "pollAfterMs": 100, "links": {"operation": f"/v1/operations/{op_id}"}}


def validate_shipped_openapi() -> None:
    matrix = read_document(ROOT / "learning/contracts/operation-matrix-v1.json")
    document = read_document(ROOT / "contracts/openapi/learning-platform-v1.yaml")
    profile = parse_json(read_regular_bytes(ROOT / "contracts/openapi/learning-platform-openapi-profile-v1.schema.json"))
    problem = parse_json(read_regular_bytes(ROOT / "contracts/openapi/learning-platform-problem-details-v1.schema.json"))
    try:
        jsonschema.Draft202012Validator.check_schema(profile)
        jsonschema.Draft202012Validator.check_schema(problem)
        jsonschema.Draft202012Validator(profile).validate(document)
    except (jsonschema.exceptions.SchemaError, jsonschema.exceptions.ValidationError) as exc:
        raise LearningContractError("OPENAPI_SCHEMA_INVALID") from exc
    validate_openapi_document(document, matrix)
