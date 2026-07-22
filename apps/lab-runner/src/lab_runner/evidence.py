"""Bounded evidence artifacts with a closed SHA-256 index."""
from __future__ import annotations
import hashlib, json, os, pathlib, stat


def write(root: pathlib.Path, run_id: str, value: dict[str,object]) -> pathlib.Path:
    root.mkdir(mode=0o700,parents=True,exist_ok=True); os.chmod(root,0o700)
    run=root/run_id; temporary=root/f".{run_id}.{os.getpid()}.tmp"; temporary.mkdir(mode=0o700)
    raw=json.dumps(value,sort_keys=True,separators=(",",":"),allow_nan=False).encode()+b"\n"
    if len(raw)>65536: raise RuntimeError("RUNNER_EVIDENCE_TOO_LARGE")
    result=temporary/"result.json"; result.write_bytes(raw); os.chmod(result,0o600)
    index={"schemaVersion":"runner-evidence-index-v1","runId":run_id,"artifacts":[{"locator":"result.json","size":len(raw),"sha256":hashlib.sha256(raw).hexdigest()}]}
    index_raw=json.dumps(index,sort_keys=True,separators=(",",":")).encode()+b"\n"
    (temporary/"index.json").write_bytes(index_raw); os.chmod(temporary/"index.json",0o600)
    for path in temporary.iterdir():
        observed=path.stat(follow_symlinks=False)
        if not stat.S_ISREG(observed.st_mode) or observed.st_nlink!=1: raise RuntimeError("RUNNER_EVIDENCE_TYPE_INVALID")
        fd=os.open(path,os.O_RDONLY|getattr(os,"O_NOFOLLOW",0)); os.fsync(fd); os.close(fd)
    dfd=os.open(temporary,os.O_RDONLY); os.fsync(dfd); os.close(dfd)
    os.replace(temporary,run)
    root_fd=os.open(root,os.O_RDONLY); os.fsync(root_fd); os.close(root_fd)
    return run/"index.json"
