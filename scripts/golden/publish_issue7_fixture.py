#!/usr/bin/env python3
"""Publish only the authorized C1-derived issue #7 aggregate fixture set."""
from __future__ import annotations
import json, os, pathlib, sys
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent)); import issue7_fixture, run_bundle, source_state

ROOT=pathlib.Path(__file__).resolve().parents[2]
RAW_INVALID={"duplicate-name.json":b'{"a":1,"a":2}\n',"nan.json":b'{"n":NaN}\n',"positive-infinity.json":b'{"n":Infinity}\n',"negative-infinity.json":b'{"n":-Infinity}\n',"lone-surrogate.json":b'{"s":"\\uDEAD"}\n',"negative-zero-decimal.json":b'{"value":"-0.00"}\n'}
def main()->int:
    source=source_state.identity(); evidence_parent=ROOT/".artifacts/evidence/golden"
    candidates=[]
    for path in evidence_parent.iterdir():
        if path.is_symlink() or not (path/"comparison.json").is_file(): continue
        try:
            current=run_bundle.verify(path,source[0]); comparison=json.loads((path/"comparison.json").read_text())
            peer_id=comparison.get("peerRunId"); peer=run_bundle.verify(evidence_parent/str(peer_id),source[0])
            if peer.metadata["finishedMonotonicNs"]>current.metadata["startedMonotonicNs"]: continue
            pair_duration=(current.metadata["finishedMonotonicNs"]-peer.metadata["startedMonotonicNs"])//1_000_000
            if comparison!={"status":"equal","peerRunId":peer.run_id,"pairDurationMs":pair_duration}: continue
            if not (0<=pair_duration<=600_000) or current.projection_bytes!=peer.projection_bytes or current.normalized_raw_bytes!=peer.normalized_raw_bytes: continue
            candidates.append((path,current,peer))
        except (OSError,ValueError,json.JSONDecodeError): continue
    if not candidates: raise SystemExit("FIXTURE_TWO_EQUAL_C1_RUNS_REQUIRED")
    run,current,peer=max(candidates,key=lambda item:item[1].metadata["finishedMonotonicNs"]); projection=current.projection
    fixture,manifest=issue7_fixture.fixture_documents(projection,source[0],(peer.run_id,current.run_id))
    target=ROOT/"tests/fixtures/learning/promotion-trust"
    if target.exists(): raise SystemExit("FIXTURE_DESTINATION_PREEXISTS")
    invalid=target/"invalid/canonicalization"; invalid.mkdir(mode=0o700,parents=True)
    evidence_bytes=(json.dumps(fixture,ensure_ascii=False,sort_keys=True,separators=(",",":"))+"\n").encode(); manifest_bytes=(json.dumps(manifest,ensure_ascii=False,sort_keys=True,separators=(",",":"))+"\n").encode()
    (target/"evidence-v1.json").write_bytes(evidence_bytes); (target/"manifest.json").write_bytes(manifest_bytes)
    for name,payload in RAW_INVALID.items(): (invalid/name).write_bytes(payload)
    for path in target.rglob("*"):
        if path.is_file(): os.chmod(path,0o600)
    staged=tuple(path.relative_to(ROOT).as_posix() for path in target.rglob("*") if path.is_file()); issue7_fixture.validate_staged_paths(staged)
    source_state.assert_unchanged(source,tuple(sorted(staged)))
    print(f"fixture-published paths={len(staged)} sourceRun={run.name} testedTreeSha={source[0]}"); return 0
if __name__=="__main__": raise SystemExit(main())
