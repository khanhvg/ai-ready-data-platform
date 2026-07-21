from __future__ import annotations
import hashlib, importlib.util, pathlib, unittest, yaml
ROOT=pathlib.Path(__file__).resolve().parents[2]
IDS=("C4-L0","C4-L1","C4-L2-LOCAL","C4-L3-RUNNER","DEP-LOCAL","DYN-JOURNEY")

class ArchitectureContractTests(unittest.TestCase):
    def test_exact_tool_lock(self) -> None:
        package=ROOT/"requirements/architecture/package.json"; lock=ROOT/"requirements/architecture/package-lock.json"
        if not package.is_file() or not lock.is_file(): self.fail("P6-RED-TOOL-LOCK")
        self.assertEqual("5cebd6d09ecef1334a492b871e388049392b6c0f6c9738873438b88958bd475d",hashlib.sha256(package.read_bytes()).hexdigest())
        self.assertEqual("7a56d803a47454023f40a04bcdb3b037f4ab2c2a05321292ad3b7f7225c2118c",hashlib.sha256(lock.read_bytes()).hexdigest())
    def test_six_view_set_and_fitness(self) -> None:
        manifest=ROOT/"architecture/likec4/view-manifest.yaml"; checker=ROOT/"scripts/golden/architecture_check.py"
        if not manifest.is_file(): self.fail("P6-RED-SIX-VIEW-SET")
        if not checker.is_file(): self.fail("P6-RED-C4-FITNESS")
        value=yaml.safe_load(manifest.read_text()); self.assertEqual(IDS,tuple(item["id"] for item in value["views"]))
        self.assertIn("deployment view dep_local",(ROOT/"architecture/likec4/views/DEP-LOCAL.c4").read_text())
        spec=importlib.util.spec_from_file_location("architecture_check",checker); assert spec and spec.loader
        module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module); module.check_sources()
    def test_semantic_text_is_source_derived(self) -> None:
        text=ROOT/"architecture/rendered/DYN-JOURNEY.txt"
        if not text.is_file(): self.fail("P6-RED-TEXT-FROM-MODEL")
        value=text.read_text(); self.assertIn("1. Load",value); self.assertIn("9. Complete",value); self.assertNotIn("<svg",value)

if __name__ == "__main__": unittest.main()
