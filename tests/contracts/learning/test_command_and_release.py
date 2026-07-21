from __future__ import annotations

import unittest

from tests.contracts.learning import assert_invalid, fixture


class CommandReleaseBehaviorTest(unittest.TestCase):
    def test_activation_base_hash(self) -> None:
        assert_invalid(self, "I8-COMMAND-ACTIVATION-184", "activation", fixture("invalid/command/base-command-registry-hash-mismatch.json"), "COMMAND_ACTIVATION_BASE_MISMATCH")

    def test_rollback_scope(self) -> None:
        assert_invalid(self, "I8-ROLLBACK-SCOPE-190", "rollback", {"owned": False, "marker": "foreign", "links": 1}, "ROLLBACK_SCOPE_UNOWNED")

    def test_fitness_owner_version_activation(self) -> None:
        vectors = [
            {"schemaVersion": "fitness-result-v1", "owner": "I5-03", "commandId": "learning-contracts-check"},
            {"schemaVersion": "fitness-result-v2", "owner": "I5-04", "commandId": "learning-contracts-check"},
            {"schemaVersion": "fitness-result-v2", "owner": "I5-03", "commandId": "unknown-check"},
            {"schemaVersion": "fitness-result-v2", "owner": "I5-03", "commandId": "learning-contracts-check", "activeEvidenceVersion": "fitness-result-v1"},
        ]
        for value in vectors:
            with self.subTest(value=value):
                assert_invalid(self, "I8-FITNESS-OWNER-180", "fitness", value, "FITNESS_RESULT_OWNER_VERSION_MISMATCH")
