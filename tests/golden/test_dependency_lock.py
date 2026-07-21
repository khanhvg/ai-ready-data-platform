from __future__ import annotations

import importlib.util
import hashlib
import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[2]


class DependencyLockTests(unittest.TestCase):
    def test_tool_lock_is_published_exactly(self) -> None:
        path = ROOT / "requirements/golden-lock-tools.lock"
        self.assertTrue(path.is_file(), "P2-RED-TOOL-LOCK-MISSING")
        self.assertEqual(40, len(path.read_text(encoding="utf-8").splitlines()))
        self.assertEqual("ece1d20658685e8673a98a12135e1680321f0c04e0f1ec35b5c30e15135a7bc4", hashlib.sha256(path.read_bytes()).hexdigest())

    def test_application_lock_is_published_exactly(self) -> None:
        path = ROOT / "requirements/golden-py312-macos-arm64.lock"
        self.assertTrue(path.is_file(), "P2-RED-APP-LOCK-MISSING")
        self.assertEqual(840, len(path.read_text(encoding="utf-8").splitlines()))
        self.assertEqual("f41c727b39f99106f95b7937b2811e8d27db89d1d5106e9f1d9effd4403143d2", hashlib.sha256(path.read_bytes()).hexdigest())

    def test_rfc8785_is_a_direct_root(self) -> None:
        path = ROOT / "requirements/golden-py312-macos-arm64.in"
        text = path.read_text(encoding="utf-8") if path.exists() else ""
        self.assertIn("rfc8785==0.1.4", text.splitlines(), "P2-RED-RFC8785-ROOT-MISSING")

    def test_unsupported_tuple_has_typed_preflight(self) -> None:
        module = ROOT / "scripts/golden/dependency_lock.py"
        self.assertTrue(module.is_file(), "P2-RED-UNSUPPORTED-TUPLE")
        spec = importlib.util.spec_from_file_location("golden_dependency_lock_platform", module)
        loaded = importlib.util.module_from_spec(spec)
        assert spec and spec.loader
        spec.loader.exec_module(loaded)
        with self.assertRaisesRegex(loaded.LockError, "PYTHON_BASELINE_UNSUPPORTED"):
            loaded.platform_preflight("Linux", "x86_64")

    def test_runtime_installer_denies_sdist_and_resolution(self) -> None:
        module = ROOT / "scripts/golden/dependency_lock.py"
        if not module.exists():
            self.fail("P2-RED-SDIST-OR-RESOLVER")
        spec = importlib.util.spec_from_file_location("golden_dependency_lock", module)
        self.assertIsNotNone(spec)
        text = module.read_text(encoding="utf-8")
        self.assertIn('"--require-hashes"', text)
        self.assertIn('"--only-binary=:all:"', text)
        self.assertIn('"--no-deps"', text)


if __name__ == "__main__":
    unittest.main()
