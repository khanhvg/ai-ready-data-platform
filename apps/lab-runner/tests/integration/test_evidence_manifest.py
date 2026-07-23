from __future__ import annotations
import importlib.util
import pathlib
import json
import shutil
import tempfile
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
    def test_cached_gate_rows_and_result_are_exactly_bound(self) -> None:
        latest=APP/".local-state/evidence/gates/latest.json"
        value=json.loads(latest.read_text())
        source=APP/value["evidenceRole"]
        with tempfile.TemporaryDirectory() as temporary:
            target=pathlib.Path(temporary);shutil.copytree(source,target,dirs_exist_ok=True)
            gate.verify_gate_evidence(value,target)
            row=target/"rows"/f"{value['results'][0]['id']}.json"
            row.write_text('{"status":"fail"}\n')
            with self.assertRaisesRegex(RuntimeError,"RUNNER_GATE_EVIDENCE_TAMPERED"):
                gate.verify_gate_evidence(value,target)

    def test_named_behavior_passes_public_gate(self) -> None:
        for case_id in ["S3-SYN-001","S3-CODE-001","S3-DEP-001","S3-LIC-001","S3-PROV-001","S3-POL-001","S3-CNT-001","S3-SRC-001","S3-SEC-001","S3-EVD-001","S3-OPS-001","S3-RES-001","S3-RAC-001","S3-CLOUD-001"]:
            with self.subTest(case_id=case_id):
                result = gate.evaluate_case(ROWS[case_id])
                self.assertIn("fixtureMarker", result)
                self.assertEqual(result["status"], "pass", result["failureCode"])


if __name__ == "__main__":
    unittest.main()
