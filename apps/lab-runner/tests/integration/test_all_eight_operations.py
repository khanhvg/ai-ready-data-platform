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
    def test_output_archive_uses_bounded_workspace_tmpfs(self) -> None:
        from lab_runner.container_supervisor import OUTPUT, WORKSPACE

        self.assertEqual(OUTPUT.parent, WORKSPACE)
        self.assertNotEqual(OUTPUT.parent, pathlib.Path("/run/runner"))

    def test_dbt_profile_matches_released_project_profile(self) -> None:
        from lab_runner.operation_adapters import _dbt_profile

        profile = _dbt_profile(pathlib.Path("/workspace/state/warehouse/retail.duckdb"))
        self.assertTrue(profile.startswith("retail_pipeline:\n"))
        self.assertIn("threads: 2\n", profile)

    def test_workspace_output_archive_has_no_recursive_state_prefix(self) -> None:
        from lab_runner.container_supervisor import _archive_output

        with tempfile.TemporaryDirectory() as temporary_directory:
            root = pathlib.Path(temporary_directory)
            state = root / "state"
            (state / "data/raw").mkdir(parents=True)
            (state / "data/raw/manifest.json").write_text("{}\n")
            archive = root / "output.tar"
            _archive_output(archive, state)
            with tarfile.open(archive) as opened:
                names = opened.getnames()

        self.assertIn("data/raw/manifest.json", names)
        self.assertFalse(any(name == "state" or name.startswith("state/") for name in names))

    def test_operation_module_loader_supports_dataclasses(self) -> None:
        from lab_runner.operation_adapters import _load

        with tempfile.TemporaryDirectory() as temporary_directory:
            module_path = pathlib.Path(temporary_directory) / "released-operation.py"
            module_path.write_text(
                "from __future__ import annotations\n"
                "from dataclasses import dataclass\n"
                "@dataclass(frozen=True)\n"
                "class ReleasedRecord:\n"
                "    value: int\n"
            )
            loaded = _load("runner_released_operation", module_path)

        self.assertEqual(loaded.ReleasedRecord(9).value, 9)

    def test_named_behavior_is_not_yet_implemented(self) -> None:
        for case_id in ["RED-OPS-001"]:
            with self.subTest(case_id=case_id):
                result = gate.evaluate_case(ROWS[case_id])
                self.assertIn("fixtureMarker", result)
                self.assertEqual(result["status"], "pass", result["failureCode"])


if __name__ == "__main__":
    unittest.main()
