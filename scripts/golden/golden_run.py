#!/usr/bin/env python3
"""Allocate and enforce one formal, state-independent golden run."""
from __future__ import annotations
import argparse, json, os, pathlib, platform, secrets, shutil, subprocess, sys, tempfile, time
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent))
import release_contract, run_bundle, runtime, source_state, workspace as workspace_core

ROOT=pathlib.Path(__file__).resolve().parents[2]
RUN_DEADLINE_SECONDS=300; PAIR_DEADLINE_SECONDS=600
class GoldenError(RuntimeError): pass
def plan_run_for_test(seed:str)->dict[str,str]: return {name:f"{seed}-{name}" for name in ("home","venv","cache","raw","warehouse","target","logs","export","workspace","evidence")}
def compare_projections(first:bytes,second:bytes)->None:
    if first!=second: raise GoldenError("GOLDEN_PROJECTION_MISMATCH")
def rehearse_rollback_for_test()->bool:
    files=("Makefile","mk/issue-5/i5-01.mk","contracts/data/curated-release-manifest.schema.json","requirements/golden-py312-macos-arm64.in","requirements/golden-py312-macos-arm64.lock","requirements/golden-py312-macos-arm64.metadata.json","requirements/golden-lock-tools.in","requirements/golden-lock-tools.lock")
    directories=("learning/contracts","architecture/likec4","architecture/rendered","scripts/golden")
    required=tuple(ROOT/path for path in files)+tuple(ROOT/path for path in directories)
    if not all(path.exists() for path in required): return False
    def tree_hash(root:pathlib.Path)->str:
        import hashlib
        digest=hashlib.sha256()
        for path in sorted(item for item in root.rglob("*") if item.is_file()):
            digest.update(path.relative_to(root).as_posix().encode()+b"\0"+path.read_bytes())
        return digest.hexdigest()
    with tempfile.TemporaryDirectory() as temp:
        private=pathlib.Path(temp); previous=private/"previous"; active=private/"active"; previous.mkdir(mode=0o700)
        for relative in files:
            target=previous/relative; target.parent.mkdir(mode=0o700,parents=True,exist_ok=True); shutil.copy2(ROOT/relative,target)
        for relative in directories: shutil.copytree(ROOT/relative,previous/relative)
        import hashlib, rfc8785
        manifest=release_contract.example_manifest(); manifests={manifest["releaseId"]:manifest}
        pointer={"schemaVersion":"curated-release-current-pointer-v1","currentReleaseId":manifest["releaseId"],"manifestSha256":hashlib.sha256(rfc8785.dumps(manifest)).hexdigest()}
        model=previous/"private-pointer-model.json"; model.write_text(json.dumps({"pointer":pointer,"manifests":manifests},sort_keys=True,separators=(",",":"))+"\n")
        expected=tree_hash(previous); shutil.copytree(previous,active)
        for relative in ("Makefile","requirements/golden-py312-macos-arm64.lock","requirements/golden-py312-macos-arm64.metadata.json","learning/contracts/schema-version-registry.json","learning/contracts/fitness-result-v1.schema.json","scripts/golden/schema_reader.py","contracts/data/curated-release-manifest.schema.json","private-pointer-model.json","architecture/likec4/specification.c4","architecture/rendered/render-manifest.json","architecture/rendered/C4-L0.svg"):
            (active/relative).write_bytes(b"unsafe candidate\n")
        shutil.rmtree(active); shutil.copytree(previous,active)
        if tree_hash(active)!=expected: return False
        restored=json.loads((active/"private-pointer-model.json").read_text()); release_contract.validate_pointer(restored["pointer"],restored["manifests"])
        runtime_base=active/"runtime-base"; runtime_base.mkdir(mode=0o700)
        owner=workspace_core.allocate_at_for_test(runtime_base,"a"*32,"golden-run")
        try:
            if owner.marker["runId"]!="a"*32 or owner.marker["purpose"]!="golden-run": return False
        finally: owner.close()
    return True
def compare_run_evidence(current:pathlib.Path,tested_tree_sha:str)->dict[str,str]:
    current_bundle=run_bundle.verify(current,tested_tree_sha)
    parent=current.parent
    peers=[]
    for candidate in parent.iterdir():
        if candidate==current or candidate.is_symlink(): continue
        try:
            peer_bundle=run_bundle.verify(candidate,tested_tree_sha); peers.append(peer_bundle)
        except (OSError,ValueError): continue
    if not peers: return {"status":"awaiting-independent-peer"}
    peer=max(peers,key=lambda bundle:bundle.metadata["finishedMonotonicNs"])
    compare_projections(peer.projection_bytes,current_bundle.projection_bytes)
    if peer.normalized_raw_bytes!=current_bundle.normalized_raw_bytes: raise GoldenError("GOLDEN_RAW_NORMALIZED_MISMATCH")
    if peer.run_id==current_bundle.run_id: raise GoldenError("GOLDEN_SHARED_STATE")
    if peer.metadata["finishedMonotonicNs"]>current_bundle.metadata["startedMonotonicNs"]: raise GoldenError("GOLDEN_RUNS_NOT_SEQUENTIAL")
    pair_duration=(current_bundle.metadata["finishedMonotonicNs"]-peer.metadata["startedMonotonicNs"])//1_000_000
    if pair_duration<0 or pair_duration>PAIR_DEADLINE_SECONDS*1000: raise GoldenError("GOLDEN_PAIR_TIMEOUT")
    return {"status":"equal","peerRunId":peer.run_id,"pairDurationMs":pair_duration}
def main()->int:
    parser=argparse.ArgumentParser(); parser.add_argument("--profile",required=True); parser.add_argument("--seed",required=True); args=parser.parse_args()
    if (args.profile,args.seed)!=("small","42"): raise GoldenError("GOLDEN_INPUT_UNSUPPORTED")
    if platform.system()!="Darwin" or platform.machine()!="arm64": raise GoldenError("PYTHON_BASELINE_UNSUPPORTED")
    free=os.statvfs(ROOT); available=free.f_bavail*free.f_frsize
    if available<6*1024**3: raise GoldenError("WORKSPACE_DISK_LIMIT")
    source=source_state.identity(); started=time.monotonic(); started_monotonic_ns=time.monotonic_ns(); deadline=started+RUN_DEADLINE_SECONDS; run_id=secrets.token_hex(16)
    old=os.umask(0o077)
    workspace_owner=evidence_owner=None
    try:
        workspace_owner=workspace_core.allocate_family(("workspaces","golden"),"golden-run",run_id)
        evidence_owner=workspace_core.allocate_family(("evidence","golden"),"golden-run",run_id)
        workspace=workspace_owner.path; evidence=evidence_owner.path
        venv,env=runtime.bootstrap(workspace,deadline)
        tested=source[0]
        worker_env={**env,"VIRTUAL_ENV":str(venv)}
        result=runtime.run([str(venv/"bin/python"),str(ROOT/"scripts/golden/golden_worker.py"),"--run-root",str(workspace),"--evidence-root",str(evidence),"--tested-tree-sha",tested,"--budget",str(max(1,deadline-time.monotonic()))],cwd=ROOT,env=worker_env,deadline=deadline,limit=16*1024*1024)
        finished_monotonic_ns=time.monotonic_ns()
        metadata={"schemaVersion":"golden-run-metadata-v1","runId":run_id,"testedTreeSha":tested,"startedMonotonicNs":started_monotonic_ns,"finishedMonotonicNs":finished_monotonic_ns,"durationMs":(finished_monotonic_ns-started_monotonic_ns)//1_000_000}
        (evidence/"run-metadata.json").write_text(json.dumps(metadata,sort_keys=True,separators=(",",":"))+"\n"); os.chmod(evidence/"run-metadata.json",0o600)
        import hashlib
        core=("raw.json","projection.json","envelope.json","result.json","run-metadata.json")
        completion={"schemaVersion":"golden-run-completion-v1","runId":run_id,"artifacts":[{"locator":name,"sha256":hashlib.sha256((evidence/name).read_bytes()).hexdigest()} for name in core]}
        (evidence/"completion.json").write_text(json.dumps(completion,sort_keys=True,separators=(",",":"))+"\n"); os.chmod(evidence/"completion.json",0o600)
        comparison=compare_run_evidence(evidence,tested)
        (evidence/"comparison.json").write_text(json.dumps(comparison,sort_keys=True,separators=(",",":"))+"\n"); os.chmod(evidence/"comparison.json",0o600)
        if not rehearse_rollback_for_test(): raise GoldenError("ROLLBACK_REHEARSAL_FAILED")
        source_state.assert_unchanged(source)
        sys.stdout.buffer.write(result.stdout); print(f"golden-run-root=golden/{run_id} comparison={comparison['status']}")
        workspace_owner.close(); evidence_owner.close(); workspace_owner=evidence_owner=None
        return 0
    except subprocess.TimeoutExpired as exc: raise GoldenError("PROCESS_TIMEOUT") from exc
    finally:
        if workspace_owner is not None: workspace_owner.close()
        if evidence_owner is not None: evidence_owner.close()
        os.umask(old)
if __name__=="__main__": raise SystemExit(main())
