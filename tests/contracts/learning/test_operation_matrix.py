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


if __name__ == "__main__":
    unittest.main()
