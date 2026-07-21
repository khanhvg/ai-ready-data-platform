from __future__ import annotations

import unittest

from scripts.learning_contracts import engine_ready
from tests.contracts.learning import assert_invalid


class ScaffoldTest(unittest.TestCase):
    def test_scaffold_entrypoint_is_executable(self) -> None:
        self.assertIs(engine_ready(), True, "I8-SCAFFOLD-READY expected=True actual=False")


class AuthorityBehaviorTest(unittest.TestCase):
    def test_authority_identity(self) -> None:
        assert_invalid(self, "I8-AUTH-BASE-001", "authority", {"local": "a", "tracking": "b", "live": "b"}, "AUTHORITY_HEAD_MISMATCH")

    def test_authority_lease(self) -> None:
        assert_invalid(self, "I8-AUTH-LEASE-002", "authority", {"leaseOwners": []}, "AUTHORITY_LEASE_REQUIRED")

    def test_protected_bytes(self) -> None:
        assert_invalid(self, "I8-AUTH-PROTECTED-003", "authority", {"protectedExpected": "a", "protectedActual": "b"}, "PROTECTED_PATH_CHANGED")

    def test_issue6_fixture_pin(self) -> None:
        assert_invalid(self, "I8-I6-FIXTURE-PIN-004", "authority", {"fixtureManifestHash": "a", "artifactHash": "b"}, "FIXTURE_MANIFEST_ARTIFACT_MISMATCH")

    def test_stage_a_framework_boundary(self) -> None:
        assert_invalid(self, "I8-STAGEA-NO-I7-010", "authority", {"reads": ["spikes/web/package.json"]}, "STAGE_A_FRAMEWORK_DEPENDENCY")


if __name__ == "__main__":
    unittest.main()
