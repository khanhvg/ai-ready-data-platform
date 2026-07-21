#!/usr/bin/env python3
"""Run one registered contract suite in a fresh exact locked interpreter."""
from __future__ import annotations
import datetime, hashlib, json, os, pathlib, secrets, stat, subprocess, sys, time
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent)); import fitness, runtime, source_state, workspace as workspace_core

ROOT=pathlib.Path(__file__).resolve().parents[2]
SUITES={
"data-contracts":["tests.golden.test_generator_characterization","tests.golden.test_dbt_characterization","tests.golden.test_mart_rill_characterization","tests.golden.test_airflow_curated_characterization","tests.contracts.test_retail_golden_contract","tests.contracts.test_curated_release_manifest","tests.contracts.test_promotion_trust"],
"evidence-contracts":["tests.golden.test_workspace_security","tests.golden.test_process_security","tests.contracts.test_fitness_result_envelope","tests.contracts.test_canonicalization","tests.contracts.test_schema_mutations","tests.contracts.test_semantic_mutations","tests.golden.test_historical_evidence_reader","tests.golden.test_dbt_capture_order"],
"migration-contracts":["tests.contracts.test_version_migration"]}
FREEZE_SHA="cdb87ed71e0996f90041371cc25138afa02d78b134cbdc4afe9c25baa6649bba"
def verified_runtime(deadline:float)->tuple[pathlib.Path,dict[str,str]]:
    evidence_parent=ROOT/".artifacts/evidence/golden"; workspace_parent=ROOT/".artifacts/workspaces/golden"
    candidates=sorted((path for path in evidence_parent.iterdir() if path.is_dir() and not path.is_symlink() and (path/"projection.json").is_file()),key=lambda path:path.stat().st_mtime,reverse=True) if evidence_parent.is_dir() else []
    for evidence in candidates:
        workspace=workspace_parent/evidence.name; marker_path=workspace/".golden-owner.json"
        if not workspace.is_dir() or workspace.is_symlink() or not marker_path.is_file(): continue
        marker=json.loads(marker_path.read_text()); info=workspace.stat()
        if marker.get("runId")!=evidence.name or marker.get("purpose")!="golden-run" or stat.S_IMODE(info.st_mode)&0o077: continue
        venv=workspace/"venv"; env=runtime.clean_env(workspace/"home",workspace/"pip-cache",venv)
        freeze=runtime.run([str(venv/"bin/python"),"-m","pip","freeze","--all"],cwd=ROOT,env=env,deadline=deadline).stdout
        normalized=b"\n".join(sorted(line.strip() for line in freeze.splitlines() if line.strip()))+b"\n"
        if hashlib.sha256(normalized).hexdigest()!=FREEZE_SHA: continue
        return venv,env
    raise SystemExit("GOLDEN_RUNTIME_REQUIRED")
def main()->int:
    if len(sys.argv)!=2 or sys.argv[1] not in SUITES: raise SystemExit("CONTRACT_SUITE_UNKNOWN")
    suite=sys.argv[1]; source=source_state.identity(); run_id=secrets.token_hex(16); started_wall=datetime.datetime.now(datetime.timezone.utc); started=time.monotonic(); deadline=started+60
    old=os.umask(0o077)
    workspace_owner=evidence_owner=None
    try:
        workspace_owner=workspace_core.allocate_family(("workspaces","golden"),suite,run_id)
        evidence_owner=workspace_core.allocate_family(("evidence",suite),suite,run_id)
        workspace=workspace_owner.path; evidence=evidence_owner.path
        venv,env=verified_runtime(deadline)
        result=runtime.run([str(venv/"bin/python"),"-m","unittest",*SUITES[suite],"-v"],cwd=ROOT,env={**env,"VIRTUAL_ENV":str(venv)},deadline=deadline,limit=16*1024*1024)
        source_state.assert_unchanged(source); tested=source[0]; digest=hashlib.sha256(result.stderr+result.stdout).hexdigest()
        payload=fitness.passed(command_id=f"{suite}-check",tested_tree_sha=tested,projection_sha256=digest,started_at=started_wall,duration_ms=round((time.monotonic()-started)*1000))
        (evidence/"result.json").write_text(json.dumps(payload,sort_keys=True,separators=(",",":"))+"\n"); os.chmod(evidence/"result.json",0o600)
        sys.stdout.buffer.write(result.stderr); print(f"{suite}: pass evidence={suite}/{run_id}/result.json"); workspace_owner.close(); evidence_owner.close(); workspace_owner=evidence_owner=None
        return 0
    finally:
        if workspace_owner is not None: workspace_owner.close()
        if evidence_owner is not None: evidence_owner.close()
        os.umask(old)
if __name__=="__main__": raise SystemExit(main())
