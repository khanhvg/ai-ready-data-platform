from __future__ import annotations
import importlib.util
import pathlib
import os
import subprocess
import sys
import unittest

APP = pathlib.Path(__file__).resolve()
while APP.name != "lab-runner":
    APP = APP.parent
spec = importlib.util.spec_from_file_location("runner_gate", APP / "tools/run-gate.py")
assert spec and spec.loader
gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)
ROWS = {row["id"]: row for row in __import__("json").loads((APP / "tests/red-manifest.json").read_text())["rows"]}


class RedPublicPathTest(unittest.TestCase):
    def test_cli_rejects_state_and_image_path_overrides(self) -> None:
        environment={"PATH":"/usr/bin:/bin:/usr/local/bin","PYTHONPATH":str(APP/"src"),"PYTHONDONTWRITEBYTECODE":"1"}
        for option in ("--state-root","--image-lock"):
            result=subprocess.run([sys.executable,"-m","lab_runner",option,"/tmp/caller-controlled","run","workspace.prepare","--idempotency-key","entrypoint-override-test"],cwd=APP.parents[1],env=environment,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            self.assertEqual(2,result.returncode)
            self.assertIn("unrecognized arguments",result.stderr)

    def test_named_behavior_passes_public_gate(self) -> None:
        for case_id in ["RED-CMD-001","RED-OPS-001"]:
            with self.subTest(case_id=case_id):
                result = gate.evaluate_case(ROWS[case_id])
                self.assertIn("fixtureMarker", result)
                self.assertEqual(result["status"], "pass", result["failureCode"])


if __name__ == "__main__":
    unittest.main()
