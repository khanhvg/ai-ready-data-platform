#!/usr/bin/env python3
"""Independent third reader for the authorized aggregate fixture and manifest."""
from __future__ import annotations
import hashlib, json, pathlib, re, subprocess, sys
import jsonschema, rfc8785
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent)); import issue7_fixture, run_bundle, source_state

ROOT=pathlib.Path(__file__).resolve().parents[2]
EXPECTED=(("mart_promotion_effectiveness",7),("mart_fulfillment_performance",25),("mart_returns_analysis",47),("mart_data_quality",10))
def main()->int:
    source=source_state.identity()
    root=ROOT/"tests/fixtures/learning/promotion-trust"; evidence_path=root/"evidence-v1.json"; manifest_path=root/"manifest.json"
    evidence=json.loads(evidence_path.read_text()); manifest=json.loads(manifest_path.read_text())
    for value,schema_name in ((evidence,"promotion-trust-evidence-v1.schema.json"),(manifest,"promotion-trust-fixture-manifest-v1.schema.json")):
        schema=json.loads((ROOT/"learning/contracts"/schema_name).read_text()); jsonschema.Draft202012Validator(schema).validate(value); issue7_fixture.validate_nonrecursive(value)
    issue7_fixture.verify_fixture(evidence)
    if tuple((row["sourceId"],len(row["records"])) for row in evidence["sources"])!=EXPECTED or sum(len(row["records"]) for row in evidence["sources"])!=89: raise SystemExit("FIXTURE_ROW_SET_MISMATCH")
    for source_entry in evidence["sources"]:
        if hashlib.sha256(rfc8785.dumps(source_entry["records"])).hexdigest()!=source_entry["normalizedRecordsSha256"]: raise SystemExit("FIXTURE_RECORD_HASH_MISMATCH")
    payload=evidence_path.read_bytes()
    if manifest["evidence"]!={"byteLength":len(payload),"sha256":hashlib.sha256(payload).hexdigest()}: raise SystemExit("FIXTURE_MANIFEST_EVIDENCE_MISMATCH")
    for artifact in manifest["artifacts"]:
        path=ROOT/artifact["locator"]
        if path.stat().st_size!=artifact["byteLength"] or hashlib.sha256(path.read_bytes()).hexdigest()!=artifact["sha256"]: raise SystemExit("FIXTURE_MANIFEST_ARTIFACT_MISMATCH")
    tested=manifest["testedTreeSha"]
    subprocess.run(["git","cat-file","-e",f'{tested}^{{commit}}'],cwd=ROOT,check=True)
    subprocess.run(["git","merge-base","--is-ancestor",tested,source[0]],cwd=ROOT,check=True)
    locators=manifest["cleanRunEvidenceLocators"]
    if len(set(locators))!=2 or any(re.fullmatch(r"golden/[0-9a-f]{32}",locator) is None for locator in locators): raise SystemExit("FIXTURE_RUN_LOCATOR_INVALID")
    bundles=[run_bundle.verify(ROOT/".artifacts/evidence"/locator,tested) for locator in locators]
    if bundles[0].projection_bytes!=bundles[1].projection_bytes or bundles[0].normalized_raw_bytes!=bundles[1].normalized_raw_bytes: raise SystemExit("FIXTURE_RETAINED_RUN_MISMATCH")
    if bundles[0].metadata["finishedMonotonicNs"]>bundles[1].metadata["startedMonotonicNs"]: raise SystemExit("FIXTURE_RETAINED_RUN_NOT_SEQUENTIAL")
    pair_duration=(bundles[1].metadata["finishedMonotonicNs"]-bundles[0].metadata["startedMonotonicNs"])//1_000_000
    if not 0<=pair_duration<=600_000: raise SystemExit("FIXTURE_RETAINED_RUN_TIMEOUT")
    expected_fixture,expected_manifest=issue7_fixture.fixture_documents(bundles[1].projection,tested,(bundles[0].run_id,bundles[1].run_id))
    if evidence!=expected_fixture or manifest!=expected_manifest: raise SystemExit("FIXTURE_RECOMPUTATION_MISMATCH")
    text=payload.decode()+manifest_path.read_text()
    if re.search(r"/(?:Users|home)/|https?://[^/@\s]+:[^/@\s]+@|attestationCommitSha|mergeOrTagSha|frameworkScore|\bADR\b",text,re.I): raise SystemExit("FIXTURE_SENSITIVE_OR_RECURSIVE")
    source_state.assert_unchanged(source)
    print(f"issue7-third-reader: pass rows=89 testedTreeSha={manifest['testedTreeSha']}"); return 0
if __name__=="__main__": raise SystemExit(main())
