from __future__ import annotations

import copy
import unittest

from scripts.learning_contracts import completion, guidance, openapi, state
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
    ("resetWorkspace", "POST", "/v1/workspaces/{workspaceId}/reset", 200),
    ("verifyWorkspace", "POST", "/v1/workspaces/{workspaceId}/verify", 200),
    ("getEvidence", "GET", "/v1/evidence/{evidenceId}", 200),
    ("listTools", "GET", "/v1/tools", 200),
    ("getTool", "GET", "/v1/tools/{toolId}", 200),
    ("queryDataProduct", "POST", "/v1/data-products/{productId}/queries", 200),
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
        document = {
            "openapi": "3.2.0",
            "security": [{"bearerAuth": []}],
            "paths": {
                path: {
                    method.lower(): {
                        "operationId": operation_id,
                        **({"requestBody": {"required": True}} if method == "POST" else {}),
                        "responses": {
                            str(status): {"description": "success"},
                            "400": {"$ref": "#/components/responses/Problem"},
                            "401": {"$ref": "#/components/responses/Problem"},
                        },
                    }
                }
                for operation_id, method, path, status in OPERATIONS
            },
            "components": {
                "securitySchemes": {"bearerAuth": {"type": "http", "scheme": "bearer"}},
                "responses": {"Problem": {"description": "problem"}},
            },
        }
        self.assertIsNone(openapi.validate_openapi_document(document, matrix()))
        shipped = schema.read_document(schema.ROOT / "contracts/openapi/learning-platform-v1.yaml")
        for operation_id, method, path, status in OPERATIONS:
            operation = shipped["paths"][path][method.lower()]
            self.assertIn("500", operation["responses"])
            if method == "POST":
                reference = operation["requestBody"]["content"]["application/json"]["schema"]["$ref"]
                self.assertNotEqual("#/components/schemas/VersionedRequest", reference)
        self.assertEqual(202, next(row[3] for row in OPERATIONS if row[0] == "resetWorkspace"))
        self.assertEqual(202, next(row[3] for row in OPERATIONS if row[0] == "verifyWorkspace"))
        self.assertEqual(202, next(row[3] for row in OPERATIONS if row[0] == "queryDataProduct"))


if __name__ == "__main__":
    unittest.main()
