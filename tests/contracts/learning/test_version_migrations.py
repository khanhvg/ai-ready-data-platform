from __future__ import annotations

import pathlib
import tempfile
import unittest

from scripts.learning_contracts.registry import migrate_document, migrate_persisted_document
from scripts.learning_contracts.schema import read_document


ROOT = pathlib.Path(__file__).resolve().parents[3]


class VersionMigrationTests(unittest.TestCase):
    def test_private_vector_round_trips_losslessly(self) -> None:
        old = read_document(ROOT / "tests/fixtures/learning/contracts/valid/private-migration-v0.json")
        current = migrate_document(old, "private-migration-v1")
        self.assertEqual(old, migrate_document(current, "private-migration-v0"))

    def test_review_h4_persisted_migration_requires_registered_real_document(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            persisted = pathlib.Path(temporary) / "persisted.json"
            persisted.write_bytes(
                (ROOT / "tests/fixtures/learning/contracts/valid/private-migration-v0.json").read_bytes()
            )
            migrated = migrate_persisted_document(
                persisted,
                "private-migration-v1",
                registry_path=ROOT / "learning/contracts/learning-contract-version-registry-v1.json",
            )
        self.assertEqual("private-migration-v1", migrated["schemaVersion"])
        self.assertEqual("private reversible vector", migrated["title"])


if __name__ == "__main__":
    unittest.main()
