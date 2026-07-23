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
    def test_removed_run_is_recovered_without_external_identity(self) -> None:
        from lab_runner.container_backend import Backend
        from lab_runner.state import Store

        class EngineMustNotBeCalled:
            def __getattr__(self,name: str) -> object:
                raise AssertionError(f"engine called during durable recovery: {name}")

        with tempfile.TemporaryDirectory() as temporary:
            root=pathlib.Path(temporary);store=Store(root/"state")
            request={"operationId":"workspace.prepare","idempotencyKey":"removed-recovery-key","workspaceRevision":0}
            admitted=store.admit(request,1);store.transition(admitted.run_id,1,"creating");store.transition(admitted.run_id,1,"created");store.transition(admitted.run_id,1,"removed")
            backend=Backend(EngineMustNotBeCalled(),"sha256:"+"a"*64,root/"seccomp.json",root/"staging",store)
            backend.reconcile(admitted.run_id,"removed",None,None,1,None)
            self.assertEqual([],store.incomplete())

    def test_committed_run_is_terminal(self) -> None:
        from lab_runner.state import StateError, Store

        with tempfile.TemporaryDirectory() as temporary:
            store = Store(pathlib.Path(temporary))
            request = {"operationId": "workspace.prepare", "idempotencyKey": "terminal-state-key", "workspaceRevision": 0}
            admitted = store.admit(request, 1)
            store.transition(admitted.run_id, 1, "creating")
            store.transition(admitted.run_id, 1, "created")
            store.transition(admitted.run_id, 1, "removed")
            result = {"status": "pass"}
            store.commit(admitted.run_id, 1, result, 1)
            with self.assertRaisesRegex(StateError, "RUNNER_ILLEGAL_TRANSITION"):
                store.transition(admitted.run_id, 1, "failed")

    def test_committed_result_tamper_is_rejected_before_replay(self) -> None:
        from lab_runner.state import StateError, Store

        with tempfile.TemporaryDirectory() as temporary:
            store=Store(pathlib.Path(temporary));request={"operationId":"workspace.prepare","idempotencyKey":"tamper-replay-key","workspaceRevision":0};admitted=store.admit(request,1);store.transition(admitted.run_id,1,"creating");store.transition(admitted.run_id,1,"created");store.transition(admitted.run_id,1,"removed");store.commit(admitted.run_id,1,{"status":"pass"},1);store.db.execute("UPDATE runs SET result_json=? WHERE run_id=?",('{"status":"hostile"}',admitted.run_id))
            with self.assertRaisesRegex(StateError,"RUNNER_AUDIT_TAMPERED"):store.admit(request,2)

    def test_ambiguous_external_identity_remains_reconcilable(self) -> None:
        from lab_runner.state import Store

        with tempfile.TemporaryDirectory() as temporary:
            store=Store(pathlib.Path(temporary));request={"operationId":"workspace.prepare","idempotencyKey":"ambiguous-cleanup-key","workspaceRevision":0}
            admitted=store.admit(request,1);store.transition(admitted.run_id,1,"creating",image_digest="sha256:"+"a"*64,daemon_identity="d"*64);store.transition(admitted.run_id,1,"created",container_id="c"*64)
            self.assertFalse(store.fail_if_safe(admitted.run_id,1))
            self.assertEqual(admitted.run_id,store.incomplete()[0][0])

    def test_named_behavior_passes_public_gate(self) -> None:
        for case_id in ["RED-CRS-001"]:
            with self.subTest(case_id=case_id):
                result = gate.evaluate_case(ROWS[case_id])
                self.assertIn("fixtureMarker", result)
                self.assertEqual(result["status"], "pass", result["failureCode"])


if __name__ == "__main__":
    unittest.main()
