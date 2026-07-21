"""Framework-neutral 16-operation API and OpenAPI profile."""

from __future__ import annotations

from typing import Any

from .schema import LearningContractError


EXPECTED_OPERATIONS = {
    ("listLessons", "GET", "/v1/lessons", 200),
    ("getLesson", "GET", "/v1/lessons/{lessonId}", 200),
    ("getProgress", "GET", "/v1/progress", 200),
    ("getLessonProgress", "GET", "/v1/progress/{lessonId}", 200),
    ("createWorkspace", "POST", "/v1/labs/{labId}/workspaces", 201),
    ("getWorkspace", "GET", "/v1/workspaces/{workspaceId}", 200),
    ("startWorkspaceOperation", "POST", "/v1/workspaces/{workspaceId}/operations", 202),
    ("getOperation", "GET", "/v1/operations/{operationId}", 200),
    ("resetWorkspace", "POST", "/v1/workspaces/{workspaceId}/reset", 200),
    ("verifyWorkspace", "POST", "/v1/workspaces/{workspaceId}/verify", 200),
    ("getEvidence", "GET", "/v1/evidence/{evidenceId}", 200),
    ("listTools", "GET", "/v1/tools", 200),
    ("getTool", "GET", "/v1/tools/{toolId}", 200),
    ("queryDataProduct", "POST", "/v1/data-products/{productId}/queries", 200),
    ("getLiveness", "GET", "/health/live", 200),
    ("getReadiness", "GET", "/health/ready", 200),
}


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
        if method == "POST" and not isinstance(operation.get("requestBody"), dict):
            raise LearningContractError("OPENAPI_REQUEST_BODY_MISSING")
        responses = operation.get("responses", {})
        if str(status) not in responses or not {"400", "401"}.issubset(responses):
            raise LearningContractError("OPENAPI_RESPONSE_DRIFT")
        observed.add((operation_id, method, path, status))
    if observed != EXPECTED_OPERATIONS:
        raise LearningContractError("OPENAPI_OPERATION_DRIFT")
