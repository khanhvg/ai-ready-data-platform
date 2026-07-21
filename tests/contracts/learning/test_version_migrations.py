from __future__ import annotations

import pathlib
import unittest

from scripts.learning_contracts.registry import migrate_document
from scripts.learning_contracts.schema import read_document


ROOT = pathlib.Path(__file__).resolve().parents[3]


class VersionMigrationTests(unittest.TestCase):
    def test_private_vector_round_trips_losslessly(self) -> None:
        old = read_document(ROOT / "tests/fixtures/learning/contracts/valid/private-migration-v0.json")
        current = migrate_document(old, "private-migration-v1")
        self.assertEqual(old, migrate_document(current, "private-migration-v0"))


if __name__ == "__main__":
    unittest.main()
