from __future__ import annotations

import unittest

from tests.contracts.learning import assert_invalid, fixture


class ReferenceIntegrityBehaviorTest(unittest.TestCase):
    def test_missing_target(self) -> None:
        assert_invalid(self, "I8-REF-MISSING-110", "reference", fixture("invalid/ref/missing-verifier.json"), "REF_TARGET_MISSING")

    def test_cycle(self) -> None:
        assert_invalid(self, "I8-REF-CYCLE-111", "reference", fixture("invalid/ref/prerequisite-cycle.json"), "REF_CYCLE")

    def test_traversal(self) -> None:
        assert_invalid(self, "I8-REF-TRAVERSAL-112", "reference", fixture("invalid/ref/path-traversal.json"), "REF_TRAVERSAL_FORBIDDEN")

    def test_remote(self) -> None:
        assert_invalid(self, "I8-REF-REMOTE-113", "reference", fixture("invalid/ref/remote-ref.json"), "REF_REMOTE_FORBIDDEN")

    def test_hash_binding(self) -> None:
        assert_invalid(self, "I8-REF-HASH-114", "reference", fixture("invalid/ref/schema-hash-mismatch.json"), "REF_SCHEMA_HASH_MISMATCH")

    def test_base_registry_binding(self) -> None:
        assert_invalid(self, "I8-REGISTRY-BASE-115", "migration", fixture("invalid/migration/base-registry-hash-mismatch.json"), "BASE_REGISTRY_HASH_MISMATCH")
