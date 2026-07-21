from __future__ import annotations

import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[2]


class SemanticMutationTests(unittest.TestCase):
    def test_semantic_mutation_reader_must_exist(self) -> None:
        reader = ROOT / "scripts/golden/retail_contract.py"
        self.assertTrue(reader.is_file(), "P1-RED-SEMANTIC-MUTATION-UNDETECTED")


if __name__ == "__main__":
    unittest.main()
