from __future__ import annotations
import importlib.util
import pathlib
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
    def test_named_behavior_is_not_yet_implemented(self) -> None:
        for case_id in ["S3-SYN-001","S3-CODE-001","S3-DEP-001","S3-LIC-001","S3-PROV-001","S3-POL-001","S3-CNT-001","S3-SRC-001","S3-SEC-001","S3-EVD-001","S3-OPS-001","S3-RES-001","S3-RAC-001","S3-CLOUD-001"]:
            with self.subTest(case_id=case_id):
                result = gate.evaluate_case(ROWS[case_id])
                self.assertIn("fixtureMarker", result)
                self.assertEqual(result["status"], "pass", result["failureCode"])


if __name__ == "__main__":
    unittest.main()
