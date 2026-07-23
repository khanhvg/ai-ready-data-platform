from __future__ import annotations
import importlib.util
import pathlib
import sqlite3
import unittest
import tempfile
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
    def test_pending_anchor_is_discarded_after_database_rollback(self) -> None:
        from lab_runner.state import Store

        with tempfile.TemporaryDirectory() as temporary:
            root=pathlib.Path(temporary);store=Store(root)
            store.db.execute("BEGIN IMMEDIATE");store._append({"kind":"fault-before-commit"});store._prepare_anchor();store.db.execute("ROLLBACK");store.db.close()
            recovered=Store(root)
            self.assertFalse(recovered.pending_anchor_path.exists())
            recovered.verify_audit()

    def test_pending_anchor_completes_after_database_commit(self) -> None:
        from lab_runner.state import Store

        with tempfile.TemporaryDirectory() as temporary:
            root=pathlib.Path(temporary);store=Store(root)
            store.db.execute("BEGIN IMMEDIATE");store._append({"kind":"fault-after-commit"});store._prepare_anchor();store.db.execute("COMMIT");store.db.close()
            recovered=Store(root)
            self.assertFalse(recovered.pending_anchor_path.exists())
            recovered.verify_audit()

    def test_completed_anchor_discards_pending_unlink_after_crash(self) -> None:
        from lab_runner.state import Store

        with tempfile.TemporaryDirectory() as temporary:
            root=pathlib.Path(temporary);store=Store(root)
            store.db.execute("BEGIN IMMEDIATE");store._append({"kind":"fault-after-anchor"});store._prepare_anchor();store.db.execute("COMMIT")
            pending=store._read_pending();store._write_document(store.anchor_path,pending["next"]);store.db.close()
            recovered=Store(root)
            self.assertFalse(recovered.pending_anchor_path.exists())
            recovered.verify_audit()

    def test_genesis_commit_recovers_before_anchor_publication(self) -> None:
        from lab_runner.state import Store

        with tempfile.TemporaryDirectory() as temporary:
            root=pathlib.Path(temporary)
            with mock.patch.object(Store,"_finalize_anchor",side_effect=RuntimeError("simulated crash")):
                with self.assertRaisesRegex(RuntimeError,"simulated crash"):Store(root)
            recovered=Store(root)
            self.assertFalse(recovered.pending_anchor_path.exists())
            recovered.verify_audit()

    def test_external_anchor_rejects_whole_audit_truncation(self) -> None:
        from lab_runner.state import StateError, Store

        with tempfile.TemporaryDirectory() as temporary:
            root=pathlib.Path(temporary);store=Store(root);store.db.close()
            db=sqlite3.connect(root/"runner.sqlite3");db.execute("DROP TRIGGER audit_no_delete");db.execute("DELETE FROM audit");db.commit();db.close()
            with self.assertRaisesRegex(StateError,"RUNNER_AUDIT_TAMPERED"):
                Store(root)

    def test_named_behavior_passes_public_gate(self) -> None:
        for case_id in ["RED-AUD-001"]:
            with self.subTest(case_id=case_id):
                result = gate.evaluate_case(ROWS[case_id])
                self.assertIn("fixtureMarker", result)
                self.assertEqual(result["status"], "pass", result["failureCode"])


if __name__ == "__main__":
    unittest.main()
