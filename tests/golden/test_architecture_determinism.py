from __future__ import annotations
import importlib.util, pathlib, tempfile, unittest
ROOT=pathlib.Path(__file__).resolve().parents[2]

class ArchitectureDeterminismTests(unittest.TestCase):
    def _load(self):
        path=ROOT/"scripts/golden/architecture_render.py"
        if not path.is_file(): raise AssertionError("P6-RED-SVG-SEMANTICS\nP6-RED-STALE-OR-NONDETERMINISTIC")
        spec=importlib.util.spec_from_file_location("architecture_render",path); assert spec and spec.loader
        module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module); return module
    def test_svg_normalizer_preserves_semantics_and_rejects_active_content(self) -> None:
        module=self._load(); first=module.normalize_svg('<svg viewBox="0 0 1 1"><path id="a" d="M0 0L1 1"/></svg>',"A","B")
        second=module.normalize_svg('<svg viewBox="0 0 1 1"><path id="a" d="M0 0L1 0"/></svg>',"A","B")
        self.assertNotEqual(first,second)
        with self.assertRaisesRegex(module.ArchitectureError,"ARCH_RENDER_FAILED"): module.normalize_svg('<svg><script/></svg>',"A","B")
    def test_committed_render_is_fresh_and_deterministic(self) -> None:
        module=self._load()
        with tempfile.TemporaryDirectory() as a, tempfile.TemporaryDirectory() as b:
            module.render(pathlib.Path(a)); module.render(pathlib.Path(b)); self.assertEqual(module.tree_hash(pathlib.Path(a)),module.tree_hash(pathlib.Path(b)))
            module.compare_committed(pathlib.Path(a))

if __name__ == "__main__": unittest.main()
