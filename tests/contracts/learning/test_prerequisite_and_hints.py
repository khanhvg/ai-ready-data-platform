from __future__ import annotations

import copy
import unittest

from scripts.learning_contracts.guidance import evaluate_guidance


class PrerequisiteAndHintTests(unittest.TestCase):
    def test_hint_is_read_only_and_never_completes(self) -> None:
        state = {"state": "in-progress", "satisfiedPrerequisites": ["golden-small-42"]}
        before = copy.deepcopy(state)
        result = evaluate_guidance(state, {"action": "hint", "prerequisites": ["golden-small-42"]})
        self.assertEqual(before, state)
        self.assertFalse(result["completes"])


if __name__ == "__main__":
    unittest.main()
