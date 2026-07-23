from __future__ import annotations
import importlib.util
import json
import pathlib
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
    def test_staged_evidence_is_not_published_until_commit(self) -> None:
        from lab_runner.evidence import publish, stage

        with tempfile.TemporaryDirectory() as temporary:
            root=pathlib.Path(temporary)/"evidence";run_id="a"*32
            staged=stage(root,run_id,{"status":"pass"})
            self.assertFalse((root/run_id).exists())
            index=publish(root,run_id,staged)
            self.assertEqual(run_id,json.loads(index.read_text())["runId"])

    def test_committed_staged_evidence_is_reconciled(self) -> None:
        from lab_runner.evidence import reconcile, stage

        with tempfile.TemporaryDirectory() as temporary:
            root=pathlib.Path(temporary)/"evidence";run_id="b"*32
            stage(root,run_id,{"status":"pass"})
            index=reconcile(root,run_id,{"status":"pass"})
            self.assertEqual(run_id,json.loads(index.read_text())["runId"])

    def test_published_evidence_tamper_is_rejected(self) -> None:
        from lab_runner.evidence import reconcile, write

        with tempfile.TemporaryDirectory() as temporary:
            root=pathlib.Path(temporary)/"evidence";run_id="c"*32;value={"status":"pass"}
            write(root,run_id,value);(root/run_id/"result.json").write_text("{}\n")
            with self.assertRaisesRegex(RuntimeError,"RUNNER_EVIDENCE_RECOVERY_INVALID"):reconcile(root,run_id,value)

    def test_named_behavior_is_not_yet_implemented(self) -> None:
        for case_id in ["S3-EVD-001"]:
            with self.subTest(case_id=case_id):
                result = gate.evaluate_case(ROWS[case_id])
                self.assertIn("fixtureMarker", result)
                self.assertEqual(result["status"], "pass", result["failureCode"])


if __name__ == "__main__":
    unittest.main()
