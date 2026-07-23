from __future__ import annotations
import importlib.util
import hashlib
import json
import os
import pathlib
import stat
import tempfile
import unittest

import jsonschema

from lab_runner.release import ASSETS, contract_schema_sha256, publish, validate_manifest

APP = pathlib.Path(__file__).resolve()
while APP.name != "lab-runner":
    APP = APP.parent
spec = importlib.util.spec_from_file_location("runner_gate", APP / "tools/run-gate.py")
assert spec and spec.loader
gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)
ROWS = {row["id"]: row for row in __import__("json").loads((APP / "tests/red-manifest.json").read_text())["rows"]}


class RedPublicPathTest(unittest.TestCase):
    @staticmethod
    def _publish_result(revision: int) -> dict[str, object]:
        release_id = str(revision) * 64
        common = {"releaseId": release_id, "dataRunId": f"data-{revision}", "testedTreeSha": "0" * 40, "lockSha256": "1" * 64, "contractSetId": "golden-contract-set-v1", "engineSnapshotId": "duckdb-1.5.4"}
        assets = [{**common, "assetId": asset_id, "logicalFqn": f"retail_duckdb.retail.main_marts.{asset_id}", "physicalFqn": f"retail_iceberg.default.retail.{asset_id}", "schemaSha256": "2" * 64, "contentSha256": "3" * 64, "rowCount": 0, "stagedLocator": f"curated/releases/{release_id}/{asset_id}"} for asset_id in ASSETS]
        document = {"schemaVersion": "curated-release-manifest-v1", **common, "profile": "small", "seed": 42, "assets": assets}
        manifest_sha = hashlib.sha256(json.dumps(document, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
        return {"runId": str(revision) * 32, "fence": revision, "workspaceRevision": revision, "releaseManifest": {"releaseId": release_id, "manifestSha256": manifest_sha, "contractSchemaSha256": contract_schema_sha256(), "assets": assets}}

    def test_manifest_is_accepted_by_the_released_reader(self) -> None:
        root = APP.parents[1]
        schema = json.loads((root / "contracts/data/curated-release-manifest.schema.json").read_text())
        golden = json.loads((root / "contracts/data/retail-golden-v1.json").read_text())
        golden_by_id = {row["martId"]: row for row in golden["marts"]}
        release_id = "a" * 64
        probe = b"PAR1x" + (1).to_bytes(4, "little") + b"PAR1"
        schema_sha = hashlib.sha256(b"x").hexdigest()
        common = {
            "releaseId": release_id,
            "dataRunId": "data-small-42-v1",
            "testedTreeSha": "5644f01b4c0443a81f3af0bcce80f44c847cd986",
            "lockSha256": hashlib.sha256((root / "contracts/data/retail-golden-v1.json").read_bytes()).hexdigest(),
            "contractSetId": "retail-golden-v1",
            "engineSnapshotId": "duckdb-test",
        }
        assets = []
        for asset_id in ASSETS:
            expected = golden_by_id[asset_id]
            assets.append({
                **common,
                "assetId": asset_id,
                "logicalFqn": f"retail_duckdb.retail.main_marts.{asset_id}",
                "physicalFqn": f"retail_iceberg.default.retail.{asset_id}",
                "schemaSha256": schema_sha,
                "contentSha256": expected["contentSha256"],
                "rowCount": expected["rowCount"],
                "stagedLocator": f"curated/releases/{release_id}/{asset_id}",
            })
        document = {"schemaVersion": "curated-release-manifest-v1", **common, "profile": "small", "seed": 42, "assets": assets}
        with tempfile.TemporaryDirectory() as temporary:
            workspace = pathlib.Path(temporary)
            serving = workspace / "serving/export"
            release = workspace / "curated/releases" / release_id
            serving.mkdir(parents=True)
            release.mkdir(parents=True)
            for asset_id in ASSETS:
                for path in (serving / f"{asset_id}.parquet", release / asset_id):
                    path.write_bytes(probe)
                    os.chmod(path, 0o600)
            (release / "manifest.json").write_bytes(json.dumps(document, sort_keys=True, separators=(",", ":")).encode())
            os.chmod(release / "manifest.json", 0o600)
            self.assertEqual(document, validate_manifest(workspace))
            validator = jsonschema.Draft202012Validator(schema)
            validator.validate(document)

    def test_stale_replay_cannot_rewind_current_pointer(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary)
            publish(root, self._publish_result(1))
            publish(root, self._publish_result(2))
            publish(root, self._publish_result(1))
            pointer = json.loads((root / "current.json").read_text())
            self.assertEqual("curated-release-current-pointer-v1", pointer["schemaVersion"])
            self.assertEqual("2" * 64, pointer["currentReleaseId"])
            self.assertEqual("1" * 64, pointer["previousReleaseId"])

    def test_generation_directory_is_fsynced_before_pointer(self) -> None:
        original_fsync = os.fsync
        synced: list[tuple[int, int]] = []

        def observe(fd: int) -> None:
            value = os.fstat(fd)
            synced.append((value.st_ino, stat.S_IFMT(value.st_mode)))
            original_fsync(fd)

        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary)
            try:
                os.fsync = observe
                publish(root, self._publish_result(1))
            finally:
                os.fsync = original_fsync
            generations = root / "generations"
            self.assertIn((generations.stat().st_ino, stat.S_IFDIR), synced)

    def test_named_behavior_is_not_yet_implemented(self) -> None:
        for case_id in ["RED-REL-001","RED-REL-002"]:
            with self.subTest(case_id=case_id):
                result = gate.evaluate_case(ROWS[case_id])
                self.assertIn("fixtureMarker", result)
                self.assertEqual(result["status"], "pass", result["failureCode"])


if __name__ == "__main__":
    unittest.main()
