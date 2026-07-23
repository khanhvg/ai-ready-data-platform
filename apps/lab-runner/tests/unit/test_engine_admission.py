from __future__ import annotations
import importlib.util
import pathlib
import tempfile
import unittest
from unittest import mock

APP = pathlib.Path(__file__).resolve()
while APP.name != "lab-runner":
    APP = APP.parent
spec = importlib.util.spec_from_file_location("runner_gate", APP / "tools/run-gate.py")
assert spec and spec.loader
gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)
ROWS = {row["id"]: row for row in __import__("json").loads((APP / "tests/red-manifest.json").read_text())["rows"]}


class RedPublicPathTest(unittest.TestCase):
    def test_group_or_other_writable_engine_socket_is_rejected(self) -> None:
        from lab_runner.engine import Engine, EngineError
        observed=__import__("os").stat_result((__import__("stat").S_IFSOCK|0o666,0,0,1,__import__("os").geteuid(),0,0,0,0,0))
        with mock.patch("lab_runner.engine.os.lstat",return_value=observed),mock.patch("lab_runner.engine.pathlib.Path.is_symlink",return_value=False):
            with self.assertRaisesRegex(EngineError,"RUNNER_ENGINE_UNAVAILABLE"):Engine().admit()
    def test_ambiguous_inspect_failure_never_authorizes_removal(self) -> None:
        from lab_runner.container_backend import Backend
        from lab_runner.engine import EngineError

        class AmbiguousEngine:
            def admit(self, *, timeout=30):
                return {"ID":"d"*32}

            def inspect_optional(self, _container_id, *, timeout=30):
                raise EngineError("RUNNER_ENGINE_OPERATION_FAILED")

        class RecordingStore:
            def __init__(self):
                self.transitions = []

            def transition(self, *args):
                self.transitions.append(args)

        with tempfile.TemporaryDirectory() as temporary:
            store = RecordingStore()
            backend = Backend(AmbiguousEngine(), "sha256:" + "a" * 64, pathlib.Path(temporary) / "seccomp.json", pathlib.Path(temporary) / "stage", store)
            with self.assertRaisesRegex(EngineError, "RUNNER_ENGINE_OPERATION_FAILED"):
                backend._teardown("container-id", "r" * 32, 7, __import__("hashlib").sha256(("d"*32).encode()).hexdigest())
            self.assertEqual([], store.transitions)

    def test_named_behavior_passes_public_gate(self) -> None:
        for case_id in ["RED-ENG-001","RED-ENG-002","RED-ENG-003"]:
            with self.subTest(case_id=case_id):
                result = gate.evaluate_case(ROWS[case_id])
                self.assertIn("fixtureMarker", result)
                self.assertEqual(result["status"], "pass", result["failureCode"])


if __name__ == "__main__":
    unittest.main()
