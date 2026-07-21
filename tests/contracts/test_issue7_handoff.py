from __future__ import annotations
import copy, hashlib, importlib.util, pathlib, subprocess, sys, unittest
from unittest import mock
import rfc8785
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
    def test_tracked_fixture_passes_clean_third_reader_when_present(self) -> None:
        fixture=ROOT/"tests/fixtures/learning/promotion-trust/evidence-v1.json"
        if fixture.is_file(): subprocess.run([sys.executable,str(ROOT/"scripts/golden/verify_issue7_fixture.py")],cwd=ROOT,check=True)

    def _portable_attestation(self):
        module=self._load(); tested="a"*40
        core={name:hashlib.sha256(name.encode()).hexdigest() for name in ("raw.json","projection.json","envelope.json","result.json","run-metadata.json")}
        runs=[]
        for run_id,start,finish in (("1"*32,1_000_000_000,2_000_000_000),("2"*32,2_100_000_000,3_000_000_000)):
            completion={"schemaVersion":"golden-run-completion-v1","runId":run_id,"artifacts":[{"locator":name,"sha256":core[name]} for name in core]}
            completion_bytes=(__import__("json").dumps(completion,sort_keys=True,separators=(",",":"))+"\n").encode()
            runs.append({"runId":run_id,"testedTreeSha":tested,"startedMonotonicNs":start,"finishedMonotonicNs":finish,"durationMs":(finish-start)//1_000_000,"completionSha256":hashlib.sha256(completion_bytes).hexdigest(),"coreSha256":dict(core),"projectionSha256":core["projection.json"],"normalizedRawSha256":"c"*64})
        payload={"schemaVersion":"promotion-trust-portable-run-attestation-v1","testedTreeSha":tested,"sourceBundleVerification":"strict-owner-bound-at-publication","runs":runs,"timing":{"runsSequential":True,"pairDurationMs":2000,"maxRunDurationMs":300000,"maxPairDurationMs":600000},"equality":{"projection":"exact","normalizedRaw":"exact"},"integrityScope":"local-artifact-integrity-only","publisherAuthenticity":"externally-attested-not-claimed"}
        payload["integrity"]={"canonicalization":"rfc8785-jcs-v1","algorithm":"sha-256","payloadSha256":hashlib.sha256(rfc8785.dumps(payload)).hexdigest()}
        return module,payload,tested

    def test_portable_attestation_schema_and_integrity(self) -> None:
        module,value,tested=self._portable_attestation(); module.verify_portable_attestation(value,tested)
        tampered=copy.deepcopy(value); tampered["runs"][0]["durationMs"]+=1
        with self.assertRaisesRegex(module.FixtureError,"PORTABLE_ATTESTATION_INTEGRITY_MISMATCH"): module.verify_portable_attestation(tampered,tested)
        missing=copy.deepcopy(value); del missing["runs"]
        with self.assertRaisesRegex(module.FixtureError,"PORTABLE_ATTESTATION_SCHEMA_INVALID"): module.verify_portable_attestation(missing,tested)

    def test_portable_attestation_rejects_run_order_hash_and_timing_drift(self) -> None:
        module,value,tested=self._portable_attestation()
        cases=[]
        wrong_id=copy.deepcopy(value); wrong_id["runs"][1]["runId"]=wrong_id["runs"][0]["runId"]; cases.append((wrong_id,"PORTABLE_ATTESTATION_RUN_IDS_INVALID"))
        wrong_order=copy.deepcopy(value); wrong_order["runs"][1]["startedMonotonicNs"]=wrong_order["runs"][0]["finishedMonotonicNs"]-1; cases.append((wrong_order,"PORTABLE_ATTESTATION_RUN_ORDER_INVALID"))
        wrong_hash=copy.deepcopy(value); wrong_hash["runs"][1]["normalizedRawSha256"]="d"*64; cases.append((wrong_hash,"PORTABLE_ATTESTATION_EQUALITY_MISMATCH"))
        wrong_timing=copy.deepcopy(value); wrong_timing["runs"][0]["durationMs"]-=1; cases.append((wrong_timing,"PORTABLE_ATTESTATION_TIMING_INVALID"))
        for changed,error in cases:
            changed["integrity"]["payloadSha256"]=module.portable_attestation_payload_sha256(changed)
            with self.subTest(error=error),self.assertRaisesRegex(module.FixtureError,error): module.verify_portable_attestation(changed,tested)

    def test_portable_attestation_rejects_wrong_tested_tree_and_core_identity(self) -> None:
        module,value,tested=self._portable_attestation()
        with self.assertRaisesRegex(module.FixtureError,"PORTABLE_ATTESTATION_TESTED_TREE_MISMATCH"): module.verify_portable_attestation(value,"f"*40)
        changed=copy.deepcopy(value); del changed["runs"][0]["coreSha256"]["raw.json"]; changed["integrity"]["payloadSha256"]=module.portable_attestation_payload_sha256(changed)
        with self.assertRaisesRegex(module.FixtureError,"PORTABLE_ATTESTATION_SCHEMA_INVALID"): module.verify_portable_attestation(changed,tested)
        changed=copy.deepcopy(value); changed["runs"][0]["coreSha256"]["raw.json"]="e"*64; changed["integrity"]["payloadSha256"]=module.portable_attestation_payload_sha256(changed)
        with self.assertRaisesRegex(module.FixtureError,"PORTABLE_ATTESTATION_CORE_IDENTITY_MISMATCH"): module.verify_portable_attestation(changed,tested)

    def test_clean_mode_is_separate_from_explicit_owner_bound_replay(self) -> None:
        path=ROOT/"scripts/golden/verify_issue7_fixture.py"; spec=importlib.util.spec_from_file_location("verify_issue7_fixture",path); assert spec and spec.loader
        verifier=importlib.util.module_from_spec(spec); spec.loader.exec_module(verifier)
        tracked=({}, {"testedTreeSha":"a"*40}, ("a"*40,"b"*40))
        with mock.patch.object(verifier,"verify_tracked_handoff",return_value=tracked),mock.patch.object(verifier,"verify_owner_bound_replay") as strict:
            self.assertEqual(0,verifier.main([])); strict.assert_not_called()
            self.assertEqual(0,verifier.main(["--strict-owner-bound-replay"])); strict.assert_called_once_with(*tracked[:2])
if __name__=="__main__": unittest.main()
