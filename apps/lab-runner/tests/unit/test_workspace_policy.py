from __future__ import annotations
import importlib.util
import pathlib
import tarfile
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
    def test_input_archive_selects_admitted_revision_not_mutable_pointer(self) -> None:
        from lab_runner.workspace import Workspace

        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary)
            workspace = Workspace(root / "workspace")
            archives = []
            for revision, payload in ((1, b"one"), (2, b"two")):
                source = root / f"source-{revision}.tar"
                data = root / f"value-{revision}"
                data.write_bytes(payload)
                with tarfile.open(source, "w") as archive:
                    info = archive.gettarinfo(str(data), "value")
                    info.uid = info.gid = 65532
                    with data.open("rb") as stream:
                        archive.addfile(info, stream)
                archives.append(workspace.commit(source, revision))
            selected = root / "selected.tar"
            workspace.input_archive(1, selected)
            self.assertEqual(archives[0].read_bytes(), selected.read_bytes())
            self.assertNotEqual(archives[1].read_bytes(), selected.read_bytes())

    def test_named_behavior_is_not_yet_implemented(self) -> None:
        for case_id in ["RED-FS-001","RED-FS-005"]:
            with self.subTest(case_id=case_id):
                result = gate.evaluate_case(ROWS[case_id])
                self.assertIn("fixtureMarker", result)
                self.assertEqual(result["status"], "pass", result["failureCode"])


if __name__ == "__main__":
    unittest.main()
