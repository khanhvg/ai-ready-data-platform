from __future__ import annotations
import importlib.util, pathlib, unittest
import datetime, hashlib, json, os, tempfile
ROOT=pathlib.Path(__file__).resolve().parents[2]
class TwoRunReleaseTests(unittest.TestCase):
    def _load(self):
        path=ROOT/"scripts/golden/golden_run.py"
        if not path.is_file(): raise AssertionError("P8-RED-SHARED-STATE\nP8-RED-300-600-TIMEOUT\nP8-RED-PROJECTION-DRIFT\nP8-RED-ROLLBACK")
        spec=importlib.util.spec_from_file_location("golden_run",path); assert spec and spec.loader
        module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module); return module
    def test_run_identity_and_deadline_contract(self) -> None:
        module=self._load(); a=module.plan_run_for_test("a"); b=module.plan_run_for_test("b")
        self.assertTrue(set(a.values()).isdisjoint(set(b.values()))); self.assertEqual(300,module.RUN_DEADLINE_SECONDS); self.assertEqual(600,module.PAIR_DEADLINE_SECONDS)
        self.assertNotIn("release_contract",module.__dict__); self.assertNotIn("run_bundle",module.__dict__)
    def test_projection_and_rollback_contract(self) -> None:
        module=self._load()
        with self.assertRaisesRegex(module.GoldenError,"GOLDEN_PROJECTION_MISMATCH"): module.compare_projections(b"a",b"b")
        self.assertTrue(module.rehearse_rollback_for_test())
        with tempfile.TemporaryDirectory() as temp:
            artifacts=pathlib.Path(temp).resolve()/".artifacts"; parent=artifacts/"evidence/golden"; workspaces=artifacts/"workspaces/golden"
            parent.mkdir(mode=0o700,parents=True); workspaces.mkdir(mode=0o700,parents=True)
            first=self._bundle(module,parent,workspaces,"1"*32,1000,2000); second=self._bundle(module,parent,workspaces,"2"*32,2100,3000)
            self.assertEqual("equal",module.compare_run_evidence(second,"0"*40)["status"])
            (first/"result.json").write_text("{}\n")
            run_bundle=importlib.import_module("run_bundle")
            with self.assertRaisesRegex(ValueError,"RUN_BUNDLE_COMPLETION_MISMATCH"): run_bundle.verify(first,"0"*40)
    def test_overlapping_or_symlinked_runs_cannot_establish_equality(self) -> None:
        module=self._load()
        with tempfile.TemporaryDirectory() as temp:
            artifacts=pathlib.Path(temp).resolve()/".artifacts"; parent=artifacts/"evidence/golden"; workspaces=artifacts/"workspaces/golden"
            parent.mkdir(mode=0o700,parents=True); workspaces.mkdir(mode=0o700,parents=True)
            peer=self._bundle(module,parent,workspaces,"3"*32,1000,2500); current=self._bundle(module,parent,workspaces,"4"*32,2000,3000)
            with self.assertRaisesRegex(module.GoldenError,"GOLDEN_RUNS_NOT_SEQUENTIAL"): module.compare_run_evidence(current,"0"*40)
            link=parent/("5"*32); link.symlink_to(peer)
            run_bundle=importlib.import_module("run_bundle")
            with self.assertRaisesRegex(ValueError,"RUN_BUNDLE_DIRECTORY_UNSAFE"): run_bundle.verify(link,"0"*40)

    def _bundle(self,module,parent:pathlib.Path,workspaces:pathlib.Path,run_id:str,start:int,finish:int)->pathlib.Path:
        evidence=parent/run_id; workspace=workspaces/run_id
        evidence.mkdir(mode=0o700); workspace.mkdir(mode=0o700)
        for directory in (evidence,workspace):
            info=directory.stat(); marker={"schemaVersion":"golden-owner-v1","nonce":"a"*64,"runId":run_id,"purpose":"golden-run","device":info.st_dev,"inode":info.st_ino}
            (directory/".golden-owner.json").write_text(json.dumps(marker)+"\n"); os.chmod(directory/".golden-owner.json",0o600)
        tested="0"*40; projection={"testedTreeSha":tested,"value":1}; projection_bytes=json.dumps(projection,sort_keys=True,separators=(",",":")).encode(); projection_sha=hashlib.sha256(projection_bytes).hexdigest()
        raw={"run":{"runId":run_id,"startedAt":"a","finishedAt":"b","durationMs":finish-start,"workspaceLocator":f"golden/{run_id}"},"semanticProjectionSha256":projection_sha,"testedTreeSha":tested,"value":1}
        raw_bytes=json.dumps(raw,sort_keys=True,separators=(",",":")).encode(); raw_sha=hashlib.sha256(raw_bytes).hexdigest()
        payload={"testedTreeSha":tested,"artifacts":[{"locator":"raw.json","sha256":raw_sha},{"locator":"projection.json","sha256":projection_sha}]}
        import rfc8785
        envelope={"schemaVersion":"golden-evidence-envelope-v1","payload":payload,"integrity":{"canonicalization":"rfc8785-jcs-v1","algorithm":"sha-256","payloadSha256":hashlib.sha256(rfc8785.dumps(payload)).hexdigest()}}
        envelope_bytes=rfc8785.dumps(envelope)
        now=datetime.datetime(2026,1,1,tzinfo=datetime.timezone.utc)
        result={"schemaVersion":"fitness-result-v1","commandId":"golden-clean","owner":"I5-01","requested":{"profile":"small","seed":42},"status":"pass","failureCode":None,"remediation":None,"testedTreeSha":tested,"toolchain":{"python":"3.12"},"lockSha256":"f41c727b39f99106f95b7937b2811e8d27db89d1d5106e9f1d9effd4403143d2","startedAt":now.isoformat(),"finishedAt":now.isoformat(),"durationMs":finish-start,"rawLocator":"raw.json","projectionLocator":"projection.json","envelopeLocator":"envelope.json","projectionSha256":projection_sha,"artifacts":[{"locator":"raw.json","sha256":raw_sha},{"locator":"projection.json","sha256":projection_sha},{"locator":"envelope.json","sha256":hashlib.sha256(envelope_bytes).hexdigest()}]}
        metadata={"schemaVersion":"golden-run-metadata-v1","runId":run_id,"testedTreeSha":tested,"startedMonotonicNs":start*1_000_000,"finishedMonotonicNs":finish*1_000_000,"durationMs":finish-start}
        values={"raw.json":raw_bytes,"projection.json":projection_bytes,"envelope.json":envelope_bytes,"result.json":json.dumps(result,sort_keys=True,separators=(",",":")).encode()+b"\n","run-metadata.json":json.dumps(metadata,sort_keys=True,separators=(",",":")).encode()+b"\n"}
        for name,payload_bytes in values.items(): (evidence/name).write_bytes(payload_bytes); os.chmod(evidence/name,0o600)
        core_files=importlib.import_module("run_bundle").CORE_FILES
        completion={"schemaVersion":"golden-run-completion-v1","runId":run_id,"artifacts":[{"locator":name,"sha256":hashlib.sha256(values[name]).hexdigest()} for name in core_files]}
        (evidence/"completion.json").write_text(json.dumps(completion,sort_keys=True,separators=(",",":"))+"\n"); os.chmod(evidence/"completion.json",0o600)
        return evidence
if __name__=="__main__": unittest.main()
