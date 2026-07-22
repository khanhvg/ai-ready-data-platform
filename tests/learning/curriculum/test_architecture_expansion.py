from __future__ import annotations

import hashlib
import json
import pathlib
import tempfile
import unittest

from test_curriculum_contract import ROOT, apply_mutation, candidate_root, cases, require_stage_a_behavior, run_public


def tree_hash(root: pathlib.Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        digest.update(path.relative_to(root).as_posix().encode())
        digest.update(b"\0")
        digest.update(path.read_bytes())
    return digest.hexdigest()


class ArchitectureExpansionTests(unittest.TestCase):
    def test_public_renderer_is_two_run_deterministic(self) -> None:
        require_stage_a_behavior()
        with tempfile.TemporaryDirectory(prefix="i11-render-a-") as first, tempfile.TemporaryDirectory(prefix="i11-render-b-") as second:
            a = run_public("learning.curriculum.tools.architecture_expansion", ROOT, "render", "--output", first)
            b = run_public("learning.curriculum.tools.architecture_expansion", ROOT, "render", "--output", second)
            self.assertEqual(a.returncode, 0, a.stdout)
            self.assertEqual(b.returncode, 0, b.stdout)
            self.assertEqual(tree_hash(pathlib.Path(first)), tree_hash(pathlib.Path(second)))

    def test_architecture_invalid_cases_reach_real_checker_and_renderer(self) -> None:
        require_stage_a_behavior()
        for case in cases("architecture"):
            with self.subTest(case=case["id"]), candidate_root() as temporary:
                root = pathlib.Path(temporary)
                if case["mutation"]["kind"] == "render-source-set":
                    with tempfile.TemporaryDirectory(prefix="i11-stale-render-") as output:
                        rendered = run_public("learning.curriculum.tools.architecture_expansion", root, "render", "--output", output)
                        self.assertEqual(rendered.returncode, 0, rendered.stdout)
                        apply_mutation(root, case["mutation"])
                        result = run_public("learning.curriculum.tools.architecture_expansion", root, "check", "--rendered", output)
                else:
                    apply_mutation(root, case["mutation"])
                    result = run_public("learning.curriculum.tools.architecture_expansion", root, "check")
                self.assertNotEqual(result.returncode, 0, result.stdout)
                self.assertIn(str(case["expectedCode"]), result.stdout)

    def test_tracked_expansion_is_accessible_and_fresh(self) -> None:
        require_stage_a_behavior()
        result = run_public("learning.curriculum.tools.architecture_expansion", ROOT, "check", "--json")
        self.assertEqual(result.returncode, 0, result.stdout)
        summary = json.loads(result.stdout)
        self.assertEqual(summary["viewCount"], 5)
        self.assertTrue(summary["accessible"])
        self.assertTrue(summary["fresh"])
        self.assertEqual(summary["protectedCount"], 33)


if __name__ == "__main__":
    unittest.main()
