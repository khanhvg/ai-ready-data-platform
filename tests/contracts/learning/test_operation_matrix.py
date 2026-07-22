from __future__ import annotations

import pathlib
import copy
import unittest

from scripts.learning_contracts.openapi import validate_openapi_document, validate_operation_matrix
from scripts.learning_contracts.schema import LearningContractError
from scripts.learning_contracts.schema import read_document


ROOT = pathlib.Path(__file__).resolve().parents[3]


class OperationMatrixTests(unittest.TestCase):
    def test_shipped_matrix_has_exact_operations(self) -> None:
        matrix = read_document(ROOT / "learning/contracts/operation-matrix-v1.json")
        self.assertIsNone(validate_operation_matrix(matrix))

    def test_six_high_h3_matrix_carries_complete_wire_contract(self) -> None:
        matrix = read_document(ROOT / "learning/contracts/operation-matrix-v1.json")
        required = {
            "operationId", "method", "path", "apiVersion", "taxonomy", "processRole",
            "authn", "authz", "csrf", "request", "response", "problems",
            "idempotency", "cas", "evidence",
        }
        self.assertEqual(16, len(matrix["operations"]))
        for row in matrix["operations"]:
            self.assertEqual(required, set(row), row["operationId"])

    def test_review_h3_matrix_response_schema_is_bound_to_openapi(self) -> None:
        matrix = read_document(ROOT / "learning/contracts/operation-matrix-v1.json")
        document = read_document(ROOT / "contracts/openapi/learning-platform-v1.yaml")
        drifted = copy.deepcopy(matrix)
        next(row for row in drifted["operations"] if row["operationId"] == "listLessons")["response"]["schema"] = "Workspace"
        with self.assertRaises(LearningContractError) as caught:
            validate_openapi_document(document, drifted)
        self.assertEqual("OPENAPI_RESPONSE_CONTRACT_DRIFT", caught.exception.code)


if __name__ == "__main__":
    unittest.main()
