from __future__ import annotations

import unittest

from tests.contracts.learning import assert_invalid, fixture


class StateCompletionBehaviorTest(unittest.TestCase):
    def test_illegal_transition(self) -> None:
        assert_invalid(self, "I8-STATE-ILLEGAL-120", "state", fixture("invalid/state/illegal-transition.json"), "STATE_TRANSITION_FORBIDDEN")

    def test_stale_revision(self) -> None:
        assert_invalid(self, "I8-STATE-STALE-121", "state", fixture("invalid/state/stale-version.json"), "PROGRESS_VERSION_CONFLICT")

    def test_idempotency_reuse(self) -> None:
        assert_invalid(self, "I8-IDEMPOTENCY-CONFLICT-122", "state", fixture("invalid/state/idempotency-payload-conflict.json"), "IDEMPOTENCY_KEY_REUSE")

    def test_duplicate_effect(self) -> None:
        assert_invalid(self, "I8-IDEMPOTENCY-DUPLICATE-123", "state", fixture("invalid/state/duplicate-effect.json"), "IDEMPOTENCY_DUPLICATE_EFFECT")

    def test_forged_browser_completion(self) -> None:
        assert_invalid(self, "I8-COMPLETION-FORGE-130", "completion", fixture("invalid/completion/forged-browser-completion.json"), "COMPLETION_AUTHORITY_REQUIRED")

    def test_operation_dual_truth(self) -> None:
        assert_invalid(self, "I8-COMPLETION-DUAL-131", "completion", fixture("invalid/completion/operation-result-direct-write.json"), "COMPLETION_DUAL_TRUTH")

    def test_evidence_presence_dual_truth(self) -> None:
        assert_invalid(self, "I8-COMPLETION-PRESENCE-134", "completion", fixture("invalid/completion/evidence-presence-completes.json"), "COMPLETION_DUAL_TRUTH")

    def test_orphan_cannot_complete(self) -> None:
        assert_invalid(self, "I8-RECONCILE-ORPHAN-132", "completion", fixture("invalid/completion/orphan-self-completion.json"), "RECONCILIATION_ORPHAN_CANNOT_COMPLETE")

    def test_orphan_hash_mismatch(self) -> None:
        assert_invalid(self, "I8-RECONCILE-TAMPER-133", "completion", fixture("invalid/completion/orphan-hash-mismatch.json"), "RECONCILIATION_HASH_MISMATCH")
