from __future__ import annotations

import unittest

from tests.contracts.learning import assert_invalid, fixture


class EvidenceTamperBehaviorTest(unittest.TestCase):
    def test_payload_hash(self) -> None:
        assert_invalid(self, "I8-TAMPER-PAYLOAD-140", "evidence", fixture("invalid/evidence/evidence-payload.json"), "EVIDENCE_PAYLOAD_HASH_MISMATCH")

    def test_artifact_hash(self) -> None:
        assert_invalid(self, "I8-TAMPER-ARTIFACT-141", "evidence", fixture("invalid/evidence/artifact-hash.json"), "EVIDENCE_ARTIFACT_HASH_MISMATCH")

    def test_verifier_hash(self) -> None:
        assert_invalid(self, "I8-TAMPER-VERIFIER-148", "evidence", fixture("invalid/evidence/stale-verifier-hash.json"), "EVIDENCE_VERIFIER_HASH_MISMATCH")
