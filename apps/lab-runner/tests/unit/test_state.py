from __future__ import annotations
import importlib.util
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
    def test_committed_run_is_terminal(self) -> None:
        from lab_runner.state import StateError, Store

        with tempfile.TemporaryDirectory() as temporary:
            store = Store(pathlib.Path(temporary))
            request = {"operationId": "workspace.prepare", "idempotencyKey": "terminal-state-key", "workspaceRevision": 0}
            admitted = store.admit(request, 1)
            store.transition(admitted.run_id, 1, "removed")
            result = {"status": "pass"}
            store.commit(admitted.run_id, 1, result, 1)
            with self.assertRaisesRegex(StateError, "RUNNER_ILLEGAL_TRANSITION"):
                store.transition(admitted.run_id, 1, "failed")

    def test_named_behavior_is_not_yet_implemented(self) -> None:
        for case_id in ["RED-CRS-001"]:
            with self.subTest(case_id=case_id):
                result = gate.evaluate_case(ROWS[case_id])
                self.assertIn("fixtureMarker", result)
                self.assertEqual(result["status"], "pass", result["failureCode"])


if __name__ == "__main__":
    unittest.main()
