from __future__ import annotations
import importlib.util
import pathlib
import unittest
from lab_runner.container_backend import Backend
from lab_runner.engine import EngineError

APP = pathlib.Path(__file__).resolve()
while APP.name != "lab-runner":
    APP = APP.parent
spec = importlib.util.spec_from_file_location("runner_gate", APP / "tools/run-gate.py")
assert spec and spec.loader
gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)
ROWS = {row["id"]: row for row in __import__("json").loads((APP / "tests/red-manifest.json").read_text())["rows"]}


class RedPublicPathTest(unittest.TestCase):
    def test_effective_protocol_rejects_wrong_operation_and_cgroup(self) -> None:
        value={"schemaVersion":"runner-container-result-v1","operationId":"workspace.prepare","status":"pass","result":{},"failureCode":None,"stdoutBytes":0,"stderrBytes":0,"descendantPeak":0,"resourceTrackerObserved":False,"cgroup":{"memoryMax":"536870912","memorySwapMax":"0","memoryPeak":1,"memoryEvents":{}}}
        Backend.effective_protocol(value,"workspace.prepare")
        for mutation in (
            {**value,"operationId":"retail.generate"},
            {**value,"cgroup":{**value["cgroup"],"memoryMax":"max"}},
            {**value,"cgroup":{**value["cgroup"],"memorySwapMax":"536870912"}},
        ):
            with self.assertRaisesRegex(EngineError,"RUNNER_CONTAINMENT_UNAVAILABLE"):
                Backend.effective_protocol(mutation,"workspace.prepare")

    def test_named_behavior_passes_public_gate(self) -> None:
        for case_id in ["RED-OUT-002"]:
            with self.subTest(case_id=case_id):
                result = gate.evaluate_case(ROWS[case_id])
                self.assertIn("fixtureMarker", result)
                self.assertEqual(result["status"], "pass", result["failureCode"])


if __name__ == "__main__":
    unittest.main()
