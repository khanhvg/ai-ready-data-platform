from __future__ import annotations

import json
import pathlib
import unittest

from test_curriculum_contract import apply_mutation, candidate_root, cases, require_stage_a_behavior, run_public


class TraceabilityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        require_stage_a_behavior()

    def test_public_trace_checker_closes_every_node_and_edge(self) -> None:
        from test_curriculum_contract import ROOT

        result = run_public("learning.curriculum.tools.check_traceability", ROOT, "--no-evidence", "--json")
        self.assertEqual(result.returncode, 0, result.stdout)
        summary = json.loads(result.stdout)
        self.assertEqual(summary["moduleCount"], 20)
        self.assertEqual(summary["orphanCount"], 0)
        self.assertEqual(summary["danglingCount"], 0)
        self.assertEqual(summary["nonReciprocalCount"], 0)
        self.assertGreater(summary["nodeCount"], 200)
        self.assertGreater(summary["edgeCount"], 400)

    def test_trace_invalid_cases_reach_public_checker(self) -> None:
        for case in cases("trace"):
            with self.subTest(case=case["id"]), candidate_root() as temporary:
                root = pathlib.Path(temporary)
                apply_mutation(root, case["mutation"])
                result = run_public("learning.curriculum.tools.check_traceability", root, "--no-evidence")
                self.assertNotEqual(result.returncode, 0, result.stdout)
                self.assertIn(str(case["expectedCode"]), result.stdout)


if __name__ == "__main__":
    unittest.main()
