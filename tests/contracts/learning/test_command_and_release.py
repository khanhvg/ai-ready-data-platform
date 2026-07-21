from __future__ import annotations

import unittest

from tests.contracts.learning import assert_invalid, fixture


class CommandReleaseBehaviorTest(unittest.TestCase):
    def test_activation_base_hash(self) -> None:
        assert_invalid(self, "I8-COMMAND-ACTIVATION-184", "activation", fixture("invalid/command/base-command-registry-hash-mismatch.json"), "COMMAND_ACTIVATION_BASE_MISMATCH")

    def test_rollback_scope(self) -> None:
        assert_invalid(self, "I8-ROLLBACK-SCOPE-190", "rollback", {"owned": False, "marker": "foreign", "links": 1}, "ROLLBACK_SCOPE_UNOWNED")
