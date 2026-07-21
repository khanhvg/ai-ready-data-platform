from __future__ import annotations

import unittest

from tests.contracts.learning import assert_invalid, fixture


class GuidanceBehaviorTest(unittest.TestCase):
    def test_probe_mutation(self) -> None:
        assert_invalid(self, "I8-PROBE-MUTATION-167", "guidance", fixture("invalid/guidance/mutating-probe.json"), "PROBE_MUTATION_FORBIDDEN")

    def test_hint_order(self) -> None:
        assert_invalid(self, "I8-HINT-ORDER-168", "guidance", fixture("invalid/guidance/out-of-order-hint.json"), "HINT_ORDER_INVALID")

    def test_hint_never_completes(self) -> None:
        assert_invalid(self, "I8-HINT-COMPLETION-169", "guidance", fixture("invalid/guidance/hint-completes.json"), "HINT_COMPLETION_FORBIDDEN")

    def test_required_unavailable(self) -> None:
        assert_invalid(self, "I8-PROBE-REQUIRED-176", "guidance", fixture("invalid/guidance/required-unavailable-passes.json"), "PROBE_REQUIRED_UNAVAILABLE")

    def test_optional_false_pass(self) -> None:
        assert_invalid(self, "I8-PROBE-OPTIONAL-177", "guidance", fixture("invalid/guidance/optional-unavailable-passes.json"), "PROBE_OPTIONAL_FALSE_PASS")

    def test_unauthorized_reveal(self) -> None:
        assert_invalid(self, "I8-HINT-REVEAL-178", "guidance", fixture("invalid/guidance/unauthorized-reveal.json"), "HINT_REVEAL_FORBIDDEN")
