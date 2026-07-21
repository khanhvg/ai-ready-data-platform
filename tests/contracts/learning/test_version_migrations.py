from __future__ import annotations

import unittest

from tests.contracts.learning import assert_invalid, fixture


class VersionMigrationBehaviorTest(unittest.TestCase):
    def test_unknown_version(self) -> None:
        assert_invalid(self, "I8-MIGRATION-UNKNOWN-150", "migration", fixture("invalid/migration/unknown-version.json"), "SCHEMA_VERSION_UNREADABLE")

    def test_lossy_edge(self) -> None:
        assert_invalid(self, "I8-MIGRATION-LOSS-151", "migration", fixture("invalid/migration/lossy-edge.json"), "MIGRATION_LOSSY_FORBIDDEN")

    def test_cycle(self) -> None:
        assert_invalid(self, "I8-MIGRATION-CYCLE-152", "migration", fixture("invalid/migration/cycle.json"), "MIGRATION_CYCLE")

    def test_family_collision(self) -> None:
        assert_invalid(self, "I8-MIGRATION-COLLISION-153", "migration", fixture("invalid/migration/family-collision.json"), "SCHEMA_FAMILY_COLLISION")

    def test_old_reader_retained(self) -> None:
        assert_invalid(self, "I8-MIGRATION-BACKWARD-159", "migration", {"readableVersions": ["v1", "v2"], "readers": ["v2"]}, "SCHEMA_VERSION_UNREADABLE")
