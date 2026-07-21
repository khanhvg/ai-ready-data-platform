from __future__ import annotations

import importlib.util
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[2]


class SchemaMutationTests(unittest.TestCase):
    def test_drift_policy_is_exactly_five_pointers(self) -> None:
        path = ROOT / "scripts/golden/projection.py"
        if not path.is_file(): self.fail("P4-RED-FIVE-POINTER-DRIFT")
        spec = importlib.util.spec_from_file_location("golden_projection", path)
        assert spec and spec.loader
        projection = importlib.util.module_from_spec(spec); spec.loader.exec_module(projection)
        self.assertEqual(("/run/runId", "/run/startedAt", "/run/finishedAt", "/run/durationMs", "/run/workspaceLocator"), projection.ALLOWED_RAW_DRIFT)
        with self.assertRaisesRegex(projection.ProjectionError, "DRIFT_POLICY_VIOLATION"):
            projection.normalize_raw({"semantic": 1}, ("/semantic",))


if __name__ == "__main__": unittest.main()
