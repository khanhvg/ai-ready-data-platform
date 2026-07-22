from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import unittest

from test_curriculum_contract import ROOT, apply_mutation, candidate_root, cases, require_stage_a_behavior, run_public


class SecurityAndEvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        require_stage_a_behavior()

    def test_security_and_bounds_cases_use_public_curriculum_validator(self) -> None:
        for case in cases("security"):
            with self.subTest(case=case["id"]), candidate_root() as temporary:
                root = pathlib.Path(temporary)
                apply_mutation(root, case["mutation"])
                result = run_public("learning.curriculum.tools.check_curriculum", root, "--no-evidence")
                self.assertNotEqual(result.returncode, 0, result.stdout)
                self.assertIn(str(case["expectedCode"]), result.stdout)

    def test_public_command_emits_and_verifies_closed_evidence(self) -> None:
        case = cases("evidence")[0]
        emitted = subprocess.run(
            ["make", "curriculum-check"],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=60,
        )
        self.assertEqual(emitted.returncode, 0, emitted.stdout)
        locator_line = next(line for line in emitted.stdout.splitlines() if line.startswith("EVIDENCE_LOCATOR="))
        locator = locator_line.split("=", 1)[1]
        evidence_root = ROOT / locator
        verified = subprocess.run(
            [sys.executable, "-m", "learning.curriculum.tools.check_curriculum", "--verify-evidence", str(evidence_root)],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=60,
        )
        self.assertEqual(verified.returncode, 0, verified.stdout)
        orphan = evidence_root / str(case["mutation"]["target"])
        orphan.write_text(json.dumps(case["mutation"]["value"], sort_keys=True) + "\n")
        rejected = subprocess.run(
            [sys.executable, "-m", "learning.curriculum.tools.check_curriculum", "--verify-evidence", str(evidence_root)],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=60,
        )
        self.assertNotEqual(rejected.returncode, 0, rejected.stdout)
        self.assertIn(str(case["expectedCode"]), rejected.stdout)


if __name__ == "__main__":
    unittest.main()
