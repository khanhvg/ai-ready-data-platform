"""Bounded evidence artifacts with a closed SHA-256 index."""
from __future__ import annotations
import hashlib, json, os, pathlib, time


def write(root: pathlib.Path, run_id: str, value: dict[str,object]) -> pathlib.Path:
    root.mkdir(mode=0o700,parents=True,exist_ok=True); os.chmod(root,0o700)
    run=root/run_id; run.mkdir(mode=0o700)
    raw=json.dumps(value,sort_keys=True,separators=(",",":"),allow_nan=False).encode()+b"\n"
    if len(raw)>65536: raise RuntimeError("RUNNER_EVIDENCE_TOO_LARGE")
    result=run/"result.json"; result.write_bytes(raw); os.chmod(result,0o600)
    index={"schemaVersion":"runner-evidence-index-v1","runId":run_id,"artifacts":[{"locator":"result.json","size":len(raw),"sha256":hashlib.sha256(raw).hexdigest()}]}
    index_raw=json.dumps(index,sort_keys=True,separators=(",",":")).encode()+b"\n"
    (run/"index.json").write_bytes(index_raw); os.chmod(run/"index.json",0o600)
    dfd=os.open(run,os.O_RDONLY); os.fsync(dfd); os.close(dfd)
    return run/"index.json"
