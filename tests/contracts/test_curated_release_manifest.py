from __future__ import annotations
import copy, hashlib, importlib.util, pathlib, unittest
import rfc8785
ROOT = pathlib.Path(__file__).resolve().parents[2]

class CuratedReleaseManifestTests(unittest.TestCase):
    def _load(self):
        path = ROOT / "scripts/golden/release_contract.py"
        if not path.is_file(): raise AssertionError("P5-RED-EXACT-11-ASSETS\nP5-RED-MIXED-GENERATION")
        spec = importlib.util.spec_from_file_location("golden_release", path); assert spec and spec.loader
        module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module); return module
    def test_exact_asset_set(self) -> None:
        release = self._load(); document = release.example_manifest()
        contract = __import__("json").loads((ROOT / "contracts/data/curated-release-manifest.schema.json").read_text())
        self.assertEqual(release.ASSET_IDS, tuple(contract["x-assetIds"]))
        self.assertEqual("not-implemented-by-i5-01", contract["x-publicationBehavior"])
        release.validate_manifest(document)
        for mutation in (document["assets"][:-1], document["assets"] + [document["assets"][0]]):
            changed = copy.deepcopy(document); changed["assets"] = mutation
            with self.assertRaisesRegex(release.ReleaseError, "CURATED_ASSET_SET_MISMATCH"): release.validate_manifest(changed)
    def test_mixed_generation_is_rejected(self) -> None:
        release = self._load(); changed = release.example_manifest(); changed["assets"][0]["dataRunId"] = "other-run"
        with self.assertRaisesRegex(release.ReleaseError, "CURATED_MIXED_GENERATION"): release.validate_manifest(changed)
    def test_pointer_digest_and_rollback_target_are_validated(self) -> None:
        release=self._load(); current=release.example_manifest(); manifests={current["releaseId"]:current}
        pointer={"schemaVersion":"curated-release-current-pointer-v1","currentReleaseId":current["releaseId"],"manifestSha256":hashlib.sha256(rfc8785.dumps(current)).hexdigest()}
        release.validate_pointer(pointer,manifests)
        changed=copy.deepcopy(pointer); changed["manifestSha256"]="0"*64
        with self.assertRaisesRegex(release.ReleaseError,"CURATED_POINTER_DIGEST_INVALID"): release.validate_pointer(changed,manifests)
        changed=copy.deepcopy(pointer); changed["previousReleaseId"]="missing"
        with self.assertRaisesRegex(release.ReleaseError,"CURATED_ROLLBACK_TARGET_INVALID"): release.validate_pointer(changed,manifests)
        changed=copy.deepcopy(pointer); changed.pop("schemaVersion")
        with self.assertRaisesRegex(release.ReleaseError,"CURATED_POINTER_INVALID"): release.validate_pointer(changed,manifests)
        changed=copy.deepcopy(current); changed["unexpected"]=True
        with self.assertRaisesRegex(release.ReleaseError,"CURATED_MANIFEST_SCHEMA_INVALID"): release.validate_manifest(changed)
        previous=copy.deepcopy(current); previous["releaseId"]="different-release"
        for asset in previous["assets"]:
            asset["releaseId"]="different-release"; asset["stagedLocator"]=f"curated/releases/different-release/{asset['assetId']}"
        changed=copy.deepcopy(pointer); changed["previousReleaseId"]="previous-key"
        with self.assertRaisesRegex(release.ReleaseError,"CURATED_ROLLBACK_TARGET_INVALID"): release.validate_pointer(changed,{**manifests,"previous-key":previous})

if __name__ == "__main__": unittest.main()
