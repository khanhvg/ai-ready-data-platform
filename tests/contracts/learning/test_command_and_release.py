from __future__ import annotations

import unittest

from scripts.learning_contracts.check import public_surface, release_documents
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

    def test_release_model_is_complete_and_framework_neutral(self) -> None:
        documents = release_documents()
        self.assertEqual(len(documents), 22, f"I8-RELEASE-MODEL expected=22 actual={len(documents)}")
        matrix = documents.get("learning/contracts/operation-matrix-v1.json", {})
        self.assertEqual(len(matrix.get("operations", [])), 16)
        self.assertEqual(matrix.get("channels"), [])
        self.assertFalse(any("vite" in path.lower() or "asyncapi" in path.lower() for path in documents))

    def test_public_surface_and_independent_vectors(self) -> None:
        targets, vectors = public_surface()
        self.assertEqual(targets, ("learning-contracts-check", "lesson-check", "api-contracts-check", "evidence-verify"), f"I8-PUBLIC-SURFACE expected=4 actual={len(targets)}")
        self.assertEqual(len(vectors), 4, f"I8-VALID-VECTORS expected=4 actual={len(vectors)}")
