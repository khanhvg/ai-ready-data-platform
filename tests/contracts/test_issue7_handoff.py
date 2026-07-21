from __future__ import annotations
import importlib.util, pathlib, unittest
ROOT=pathlib.Path(__file__).resolve().parents[2]
class Issue7HandoffTests(unittest.TestCase):
    def _load(self):
        path=ROOT/"scripts/golden/issue7_fixture.py"
        if not path.is_file(): raise AssertionError("P8-RED-C1-C2-M-RECURSION\nP8-RED-FOUR-DIGEST-INVALIDATION\nP8-RED-ARTIFACT-STAGING")
        spec=importlib.util.spec_from_file_location("issue7_fixture",path); assert spec and spec.loader
        module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module); return module
    def test_non_recursive_handoff_and_invalidation(self) -> None:
        module=self._load()
        with self.assertRaisesRegex(module.FixtureError,"FIXTURE_RECURSIVE_IDENTITY"): module.validate_nonrecursive({"attestationCommitSha":"0"*40})
        baseline={path:"0"*64 for path in module.FOUR_HANDOFF_PATHS}; changed=dict(baseline); changed[module.FOUR_HANDOFF_PATHS[0]]="1"*64
        self.assertTrue(module.invalidates_issue7(baseline,changed))
    def test_only_authorized_artifact_paths(self) -> None:
        module=self._load(); module.validate_staged_paths(module.AUTHORIZED_FIXTURE_PATHS)
        with self.assertRaisesRegex(module.FixtureError,"FIXTURE_PATH_UNAUTHORIZED"): module.validate_staged_paths(("tests/fixtures/other.json",))
if __name__=="__main__": unittest.main()
