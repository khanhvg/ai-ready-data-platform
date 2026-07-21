from __future__ import annotations

import copy
import unittest

from scripts.learning_contracts import completion, guidance, openapi, schema, state
from scripts.learning_contracts.schema import LearningContractError


OPERATIONS = [
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
]


def matrix() -> dict[str, object]:
    return {
        "schemaVersion": "operation-matrix-v1",
        "channels": [],
        "operations": [
            {
                "operationId": operation_id,
                "method": method,
                "path": path,
                "successStatus": status,
                "authorization": "bearer" if not path.startswith("/health/") else "public",
                "idempotency": method == "POST",
                "taxonomy": "Process" if method == "POST" else "Experience",
                "processRole": "learning-contract-service",
                "evidenceRule": "required" if operation_id == "verifyWorkspace" else "none",
            }
            for operation_id, method, path, status in OPERATIONS
        ],
    }


class StateCompletionApiTests(unittest.TestCase):
    def assert_code(self, expected: str, call, *args, **kwargs) -> None:
        with self.assertRaises(LearningContractError) as caught:
            call(*args, **kwargs)
        self.assertEqual(expected, caught.exception.code)

    def test_i8_v3_operation_matrix_16_007(self) -> None:
        """I8-V3-OPERATION-MATRIX-16-007."""
        self.assertIsNone(openapi.validate_operation_matrix(matrix()))

    def test_i8_v3_api_auth_version_008(self) -> None:
        """I8-V3-API-AUTH-VERSION-008."""
        self.assert_code(
            "AUTH_REQUIRED",
            openapi.dispatch,
            {"method": "GET", "path": "/v1/progress", "headers": {}},
        )
        self.assert_code(
            "VERSION_UNSUPPORTED",
            openapi.dispatch,
            {"method": "GET", "path": "/v2/progress", "headers": {"Authorization": "Bearer learner"}},
        )

    def test_i8_v3_completion_cas_idempotency_009(self) -> None:
        """I8-V3-COMPLETION-CAS-IDEMPOTENCY-009."""
        progress = {"revision": 0, "state": "verified", "effects": [], "idempotency": {}}
        request = {"expectedRevision": 0, "idempotencyKey": "complete-1", "evidenceId": "evidence-1"}
        first = completion.complete(progress, copy.deepcopy(request))
        second = completion.complete(progress, copy.deepcopy(request))
        self.assertEqual(first, second)
        self.assertEqual("completed", progress["state"])
        self.assertEqual(1, len(progress["effects"]))

    def test_i8_v3_conflict_reconciliation_010(self) -> None:
        """I8-V3-CONFLICT-RECONCILIATION-010."""
        progress = {"revision": 2, "state": "verified", "effects": [], "idempotency": {}}
        self.assert_code(
            "PROGRESS_VERSION_CONFLICT",
            completion.complete,
            progress,
            {"expectedRevision": 1, "idempotencyKey": "complete-2", "evidenceId": "evidence-2"},
        )
        completion.complete(
            progress,
            {"expectedRevision": 2, "idempotencyKey": "complete-3", "evidenceId": "evidence-3"},
        )
        self.assert_code(
            "IDEMPOTENCY_KEY_REUSE",
            completion.complete,
            progress,
            {"expectedRevision": 2, "idempotencyKey": "complete-3", "evidenceId": "changed"},
        )
        pristine = {"revision": 2, "state": "verified", "effects": []}
        before = copy.deepcopy(pristine)
        self.assert_code(
            "PROGRESS_VERSION_CONFLICT",
            completion.complete,
            pristine,
            {"expectedRevision": 1, "idempotencyKey": "complete-4", "evidenceId": "evidence-4"},
        )
        self.assertEqual(before, pristine)

    def test_i8_v3_prerequisite_hint_reset_011(self) -> None:
        """I8-V3-PREREQUISITE-HINT-RESET-011."""
        progress = {"revision": 0, "state": "not-started", "effects": [], "idempotency": {}}
        before = copy.deepcopy(progress)
        hint = guidance.evaluate_guidance(progress, {"action": "hint", "prerequisites": ["golden-small-42"]})
        self.assertEqual(before, progress)
        self.assertFalse(hint["completes"])
        self.assert_code(
            "PREREQUISITE_REQUIRED",
            state.execute_operation,
            progress,
            {"action": "start", "expectedRevision": 0, "prerequisitesSatisfied": False},
        )
        reset = state.execute_operation(
            progress,
            {"action": "reset", "expectedRevision": 0, "prerequisitesSatisfied": True},
        )
        self.assertEqual("not-started", reset["state"])

    def test_i8_v3_openapi_wiring_012(self) -> None:
        """I8-V3-OPENAPI-WIRING-012."""
        shipped = schema.read_document(schema.ROOT / "contracts/openapi/learning-platform-v1.yaml")
        self.assertIsNone(openapi.validate_openapi_document(shipped, matrix()))
        for operation_id, method, path, status in OPERATIONS:
            operation = shipped["paths"][path][method.lower()]
            self.assertIn("500", operation["responses"])
            if method == "POST":
                reference = operation["requestBody"]["content"]["application/json"]["schema"]["$ref"]
                self.assertNotEqual("#/components/schemas/VersionedRequest", reference)
        self.assertEqual(202, next(row[3] for row in OPERATIONS if row[0] == "resetWorkspace"))
        self.assertEqual(202, next(row[3] for row in OPERATIONS if row[0] == "verifyWorkspace"))
        self.assertEqual(202, next(row[3] for row in OPERATIONS if row[0] == "queryDataProduct"))

    def test_six_high_h4_dispatch_executes_authoritative_state(self) -> None:
        platform = openapi.LearningPlatform()
        common = {
            "Authorization": "Bearer learner-1",
            "X-Correlation-ID": "correlation-1",
            "Origin": "http://localhost",
            "Host": "localhost",
            "X-CSRF-Token": "csrf-1",
            "Idempotency-Key": "workspace-1",
            "Content-Type": "application/json",
        }
        created = platform.dispatch({
            "method": "POST",
            "path": "/v1/labs/promotion-trust-v1/workspaces",
            "headers": common,
            "body": {
                "schemaVersion": "create-workspace-request-v1",
                "labVersion": "1.0.0",
                "contractSetSha256": "0" * 64,
                "parameters": {},
                "expectedProgressRevision": 0,
            },
        })
        self.assertEqual(201, created["status"])
        workspace_id = created["body"]["workspaceId"]
        fetched = platform.dispatch({
            "method": "GET",
            "path": f"/v1/workspaces/{workspace_id}",
            "headers": {"Authorization": "Bearer learner-1", "X-Correlation-ID": "correlation-2"},
        })
        self.assertEqual(created["body"], fetched["body"])

    def test_review_h3_invalid_body_returns_validated_problem(self) -> None:
        platform = openapi.LearningPlatform()
        response = platform.dispatch({
            "method": "POST",
            "path": "/v1/labs/promotion-trust-v1/workspaces",
            "headers": {
                "Authorization": "Bearer learner-1", "X-Correlation-ID": "correlation-invalid",
                "Origin": "http://localhost", "Host": "localhost", "X-CSRF-Token": "csrf",
                "Idempotency-Key": "invalid-body", "Content-Type": "application/json",
            },
            "body": {
                "schemaVersion": "create-workspace-request-v1", "labVersion": "1.0.0",
                "contractSetSha256": "not-a-sha", "parameters": {}, "expectedProgressRevision": 0,
            },
        })
        self.assertEqual(422, response["status"])
        self.assertEqual("LAB_PARAMETER_INVALID", response["body"]["code"])
        schema.validate_document(response["body"], family="problem-details")

    def test_review_h4_stale_verify_is_atomic(self) -> None:
        platform = openapi.LearningPlatform()
        headers = {
            "Authorization": "Bearer learner-1", "X-Correlation-ID": "create",
            "Origin": "http://localhost", "Host": "localhost", "X-CSRF-Token": "csrf",
            "Idempotency-Key": "create", "Content-Type": "application/json",
        }
        created = platform.dispatch({"method": "POST", "path": "/v1/labs/promotion-trust-v1/workspaces", "headers": headers, "body": {
            "schemaVersion": "create-workspace-request-v1", "labVersion": "1.0.0",
            "contractSetSha256": "0" * 64, "parameters": {}, "expectedProgressRevision": 0,
        }})
        workspace_id = created["body"]["workspaceId"]
        before = copy.deepcopy((platform.workspaces, platform.operations, platform.evidence, platform.progress))
        verify_headers = dict(headers, **{"X-Correlation-ID": "verify", "Idempotency-Key": "verify"})
        response = platform.dispatch({"method": "POST", "path": f"/v1/workspaces/{workspace_id}/verify", "headers": verify_headers, "body": {
            "schemaVersion": "verify-workspace-request-v1", "verifierId": "promotion.verify",
            "expectedWorkspaceRevision": 0, "expectedProgressRevision": 99,
        }})
        self.assertEqual(412, response["status"])
        self.assertEqual("PROGRESS_VERSION_CONFLICT", response["body"]["code"])
        self.assertEqual(before, (platform.workspaces, platform.operations, platform.evidence, platform.progress))

    def test_final_repair_query_replay_precedes_cas_and_stale_new_key_is_mapped(self) -> None:
        platform = openapi.LearningPlatform()
        headers = {
            "Authorization": "Bearer learner-1", "X-Correlation-ID": "create-query-workspace",
            "Origin": "http://localhost", "Host": "localhost", "X-CSRF-Token": "csrf",
            "Idempotency-Key": "create-query-workspace", "Content-Type": "application/json",
        }
        created = platform.dispatch({
            "method": "POST", "path": "/v1/labs/promotion-trust-v1/workspaces", "headers": headers,
            "body": {
                "schemaVersion": "create-workspace-request-v1", "labVersion": "1.0.0",
                "contractSetSha256": "0" * 64, "parameters": {}, "expectedProgressRevision": 0,
            },
        })
        self.assertEqual(201, created["status"])
        workspace_id = created["body"]["workspaceId"]
        query = {
            "schemaVersion": "registered-query-request-v1", "workspaceId": workspace_id,
            "queryId": "promotion-grains", "parameters": {},
            "expectedWorkspaceRevision": created["body"]["revision"],
        }
        query_headers = dict(
            headers,
            **{"X-Correlation-ID": "query-replay", "Idempotency-Key": "query-replay"},
        )
        request = {
            "method": "POST", "path": "/v1/data-products/promotion-trust/queries",
            "headers": query_headers, "body": query,
        }
        accepted = platform.dispatch(copy.deepcopy(request))
        self.assertEqual(202, accepted["status"])
        platform.workspaces[workspace_id]["revision"] += 1

        replayed = platform.dispatch(copy.deepcopy(request))
        self.assertEqual(accepted, replayed)
        platform._validate_success("queryDataProduct", replayed["body"])

        changed = copy.deepcopy(request)
        changed["body"]["queryId"] = "promotion-limitations"
        reuse = platform.dispatch(changed)
        self.assertEqual(409, reuse["status"])
        self.assertEqual("IDEMPOTENCY_KEY_REUSE", reuse["body"]["code"])
        schema.validate_document(reuse["body"], family="problem-details")

        stale = copy.deepcopy(request)
        stale["headers"]["Idempotency-Key"] = "query-stale-new-key"
        conflict = platform.dispatch(stale)
        self.assertEqual(409, conflict["status"])
        self.assertEqual("WORKSPACE_REVISION_CONFLICT", conflict["body"]["code"])
        schema.validate_document(conflict["body"], family="problem-details")

        row = next(
            item for item in platform.matrix["operations"]
            if item["operationId"] == "queryDataProduct"
        )
        self.assertIn(
            {"status": 409, "code": "WORKSPACE_REVISION_CONFLICT"}, row["problems"],
        )
        operation = platform.openapi["paths"]["/v1/data-products/{productId}/queries"]["post"]
        self.assertEqual(row["problems"], operation["x-problems"])
        self.assertEqual({"$ref": "#/components/responses/Problem"}, operation["responses"]["409"])


if __name__ == "__main__":
    unittest.main()
