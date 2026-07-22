from __future__ import annotations

import pathlib
import subprocess
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[2]
I5_02 = ROOT / "mk/issue-5/i5-02.mk"
INTERPRETER_SHA256 = "a" * 64


class MakeFragmentCompositionTests(unittest.TestCase):
    def _make(self, *arguments: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["make", *arguments],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )

    def assert_parses(self, result: subprocess.CompletedProcess[str]) -> None:
        self.assertEqual(0, result.returncode, result.stdout)
        self.assertNotIn("unauthorized target(s):", result.stdout)

    def test_root_golden_clean_parses(self) -> None:
        result = self._make("-n", "golden-clean", "PROFILE=small", "SEED=42")
        self.assert_parses(result)

    def test_root_learning_contracts_check_parses(self) -> None:
        result = self._make(
            "-n",
            "learning-contracts-check",
            f"LEARNING_RUNTIME_INTERPRETER_SHA256={INTERPRETER_SHA256}",
        )
        self.assert_parses(result)

    def test_preexisting_root_target_parses(self) -> None:
        self.assert_parses(self._make("-n", "health"))

    def test_direct_recognized_issue7_target_parses_for_relative_and_absolute_paths(self) -> None:
        for makefile in ("mk/issue-5/i5-02.mk", str(I5_02)):
            with self.subTest(makefile=makefile):
                self.assert_parses(
                    self._make("-f", makefile, "-n", "i5-02-toolchain-check")
                )

    def test_direct_unknown_target_remains_fail_closed(self) -> None:
        result = self._make("-f", "mk/issue-5/i5-02.mk", "-n", "golden-clean")
        self.assertNotEqual(0, result.returncode, result.stdout)
        self.assertIn("unauthorized target(s): golden-clean", result.stdout)

    def test_root_and_direct_default_goals_remain_distinct(self) -> None:
        root = self._make("-n")
        self.assert_parses(root)
        self.assertNotIn("continuation-check.mjs", root.stdout)

        for makefile in ("mk/issue-5/i5-02.mk", str(I5_02)):
            with self.subTest(makefile=makefile):
                direct = self._make("-f", makefile, "-n")
                self.assertEqual(0, direct.returncode, direct.stdout)
                self.assertIn("continuation-check.mjs", direct.stdout)
                self.assertIn("--check authority", direct.stdout)


if __name__ == "__main__":
    unittest.main()
