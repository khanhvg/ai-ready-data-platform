#!/usr/bin/env python3
"""Verify the portable tracked handoff; replay private bundles only on request."""
from __future__ import annotations
import argparse, hashlib, json, pathlib, re, subprocess, sys
import jsonschema, rfc8785
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent)); import issue7_fixture, run_bundle, schema_reader, source_state

ROOT=pathlib.Path(__file__).resolve().parents[2]
EXPECTED=(("mart_promotion_effectiveness",7),("mart_fulfillment_performance",25),("mart_returns_analysis",47),("mart_data_quality",10))

def verify_tracked_handoff()->tuple[dict,dict,tuple[str,str]]:
    source=source_state.identity(); root=ROOT/"tests/fixtures/learning/promotion-trust"; evidence_path=root/"evidence-v1.json"; manifest_path=root/"manifest.json"
    evidence=json.loads(evidence_path.read_text()); manifest=json.loads(manifest_path.read_text())
    evidence_schema=json.loads((ROOT/"learning/contracts/promotion-trust-evidence-v1.schema.json").read_text()); jsonschema.Draft202012Validator(evidence_schema).validate(evidence)
    schema_reader.validate("promotion-trust-fixture-manifest",manifest); schema_reader.validate("promotion-trust-portable-run-attestation",manifest["portableRunAttestation"])
    issue7_fixture.validate_nonrecursive(evidence); issue7_fixture.validate_nonrecursive(manifest); issue7_fixture.verify_fixture(evidence)
    if tuple((row["sourceId"],len(row["records"])) for row in evidence["sources"])!=EXPECTED or sum(len(row["records"]) for row in evidence["sources"])!=89: raise SystemExit("FIXTURE_ROW_SET_MISMATCH")
    for source_entry in evidence["sources"]:
        if hashlib.sha256(rfc8785.dumps(source_entry["records"])).hexdigest()!=source_entry["normalizedRecordsSha256"]: raise SystemExit("FIXTURE_RECORD_HASH_MISMATCH")
    payload=evidence_path.read_bytes()
    if manifest["evidence"]!={"byteLength":len(payload),"sha256":hashlib.sha256(payload).hexdigest()}: raise SystemExit("FIXTURE_MANIFEST_EVIDENCE_MISMATCH")
    for artifact in manifest["artifacts"]:
        path=ROOT/artifact["locator"]
        if path.stat().st_size!=artifact["byteLength"] or hashlib.sha256(path.read_bytes()).hexdigest()!=artifact["sha256"]: raise SystemExit("FIXTURE_MANIFEST_ARTIFACT_MISMATCH")
    tested=manifest["testedTreeSha"]
    subprocess.run(["git","cat-file","-e",f"{tested}^{{commit}}"],cwd=ROOT,check=True); subprocess.run(["git","merge-base","--is-ancestor",tested,source[0]],cwd=ROOT,check=True)
    issue7_fixture.verify_portable_attestation(manifest["portableRunAttestation"],tested)
    if manifest!=issue7_fixture.manifest_document(evidence,tested,manifest["portableRunAttestation"]): raise SystemExit("FIXTURE_RECOMPUTATION_MISMATCH")
    text=payload.decode()+manifest_path.read_text()
    if re.search(r"/(?:Users|home)/|https?://[^/@\s]+:[^/@\s]+@|attestationCommitSha|mergeOrTagSha|frameworkScore|\bADR\b",text,re.I): raise SystemExit("FIXTURE_SENSITIVE_OR_RECURSIVE")
    source_state.assert_unchanged(source); return evidence,manifest,source

def verify_owner_bound_replay(evidence:dict,manifest:dict)->None:
    tested=manifest["testedTreeSha"]; attestation=manifest["portableRunAttestation"]
    bundles=[run_bundle.verify(ROOT/".artifacts/evidence/golden"/run["runId"],tested) for run in attestation["runs"]]
    derived=issue7_fixture.portable_attestation_document(bundles[0],bundles[1],tested)
    if derived!=attestation: raise SystemExit("FIXTURE_OWNER_BOUND_ATTESTATION_MISMATCH")
    expected_fixture,_=issue7_fixture.fixture_documents(bundles[1].projection,tested,derived)
    if evidence!=expected_fixture: raise SystemExit("FIXTURE_OWNER_BOUND_RECOMPUTATION_MISMATCH")

def main(argv:list[str]|None=None)->int:
    parser=argparse.ArgumentParser(); parser.add_argument("--strict-owner-bound-replay",action="store_true"); args=parser.parse_args(argv)
    evidence,manifest,_=verify_tracked_handoff()
    if args.strict_owner_bound_replay: verify_owner_bound_replay(evidence,manifest)
    mode="strict-owner-bound-replay" if args.strict_owner_bound_replay else "portable-clean"
    print(f"issue7-third-reader: pass mode={mode} rows=89 testedTreeSha={manifest['testedTreeSha']}"); return 0
if __name__=="__main__": raise SystemExit(main())
