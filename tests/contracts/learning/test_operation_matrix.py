from __future__ import annotations

import pathlib
import unittest

from scripts.learning_contracts.openapi import validate_operation_matrix
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


if __name__ == "__main__":
    unittest.main()
