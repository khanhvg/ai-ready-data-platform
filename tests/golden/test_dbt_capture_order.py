from __future__ import annotations

import importlib.util
import pathlib
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[2]


class DbtCaptureOrderTests(unittest.TestCase):
    def test_build_capture_is_exclusive_and_docs_disjoint(self) -> None:
        module = ROOT / "scripts/golden/dbt_capture.py"
        if not module.is_file(): self.fail("P4-RED-DBT-CAPTURE-ORDER")
        spec = importlib.util.spec_from_file_location("golden_dbt_capture", module)
        assert spec and spec.loader
        capture = importlib.util.module_from_spec(spec); spec.loader.exec_module(capture)
        with tempfile.TemporaryDirectory() as temp:
            root = pathlib.Path(temp); source = root / "target"; source.mkdir()
            (source / "manifest.json").write_text("build", encoding="utf-8")
            destination = root / "raw" / "build"
            first = capture.capture_build(source, destination)
            (source / "manifest.json").write_text("docs", encoding="utf-8")
            self.assertEqual("build", (destination / "manifest.json").read_text())
            with self.assertRaisesRegex(capture.CaptureError, "DBT_RAW_CAPTURE_EXISTS"):
                capture.capture_build(source, destination)
            self.assertEqual(first["manifest.json"], capture.hash_file(destination / "manifest.json"))


if __name__ == "__main__": unittest.main()
