from __future__ import annotations

import unittest

from tests.contracts.learning import assert_invalid, fixture


class EvidenceProvenanceBehaviorTest(unittest.TestCase):
    def test_traversal_locator(self) -> None:
        assert_invalid(self, "I8-LOCATOR-TRAVERSAL-142", "evidence", fixture("invalid/evidence/locator-traversal.json"), "EVIDENCE_LOCATOR_INVALID")

    def test_private_and_special_locators(self) -> None:
        vectors = [
            {"locator": "/private/tmp/evidence"}, {"locator": "Users/example/.ssh/key"},
            {"locator": "artifact.json", "entryType": "symlink"},
            {"locator": "artifact.json", "linkCount": 2},
            {"locator": "artifact.json", "entryType": "fifo"},
        ]
        for value in vectors:
            with self.subTest(value=value):
                assert_invalid(self, "I8-LOCATOR-PRIVATE-147", "evidence", value, "EVIDENCE_LOCATOR_INVALID")

    def test_replay(self) -> None:
        assert_invalid(self, "I8-EVIDENCE-REPLAY-149", "evidence", fixture("invalid/evidence/replayed-run-identity.json"), "EVIDENCE_REPLAY_CONFLICT")

    def test_provenance(self) -> None:
        assert_invalid(self, "I8-EVIDENCE-PROVENANCE-143", "evidence", fixture("invalid/evidence/missing-dependency-sha.json"), "EVIDENCE_PROVENANCE_INCOMPLETE")

    def test_recursive_identity(self) -> None:
        assert_invalid(self, "I8-EVIDENCE-RECURSIVE-144", "evidence", fixture("invalid/evidence/recursive-identity.json"), "EVIDENCE_RECURSIVE_IDENTITY")

    def test_sensitive_content(self) -> None:
        canary = "tok" + "en-private-canary-" + "1234567890"
        assert_invalid(self, "I8-SECRET-145", "evidence", {"diagnostic": canary}, "EVIDENCE_SENSITIVE_CONTENT")

    def test_injection_field(self) -> None:
        assert_invalid(self, "I8-INJECTION-146", "evidence", fixture("invalid/security/injection-field.json"), "CONTRACT_INJECTION_FIELD_FORBIDDEN")
