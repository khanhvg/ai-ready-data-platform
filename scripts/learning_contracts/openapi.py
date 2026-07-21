"""Framework-neutral 16-operation API and OpenAPI profile."""

from __future__ import annotations

from typing import Any

import jsonschema

from .schema import ROOT, LearningContractError, read_document, read_regular_bytes
from .canonical import parse_json


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
        if not isinstance(row, dict) or set(row) != {
            "operationId", "method", "path", "successStatus", "authorization",
            "idempotency", "taxonomy", "processRole", "evidenceRule",
        }:
            raise LearningContractError("OPERATION_ROW_INVALID")
        key = (row["operationId"], row["method"], row["path"], row["successStatus"])
        if key in observed or row["taxonomy"] not in {"Experience", "Process", "System", "Backend", "Technical"}:
            raise LearningContractError("OPERATION_ROW_INVALID")
        if row["processRole"] != "learning-contract-service":
            raise LearningContractError("OPERATION_ROLE_NOT_NEUTRAL")
        if row["idempotency"] != (row["method"] == "POST"):
            raise LearningContractError("OPERATION_IDEMPOTENCY_INVALID")
        observed.add(key)
    if observed != EXPECTED_OPERATIONS:
        raise LearningContractError("OPERATION_MATRIX_DRIFT")


def validate_openapi_document(value: dict[str, Any], matrix: dict[str, Any]) -> None:
    validate_operation_matrix(matrix)
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
        if set(responses) != REQUIRED_RESPONSES[operation_id]:
            raise LearningContractError("OPENAPI_RESPONSE_DRIFT")
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
                or reference == "./learning-platform-problem-details-v1.schema.json"
            ):
                raise LearningContractError("OPENAPI_REF_FORBIDDEN")
            for nested in child.values():
                walk(nested)
        elif isinstance(child, list):
            for nested in child:
                walk(nested)
    walk(value)


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
