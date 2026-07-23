"""Bounded evidence artifacts with a closed SHA-256 index."""
from __future__ import annotations
import hashlib, json, os, pathlib, stat


def stage(root: pathlib.Path, run_id: str, value: dict[str,object]) -> pathlib.Path:
    root.mkdir(mode=0o700,parents=True,exist_ok=True); os.chmod(root,0o700)
    temporary=root/f".{run_id}.{os.getpid()}.tmp"; temporary.mkdir(mode=0o700)
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
    return temporary


def verify(root:pathlib.Path,run_id:str,expected:dict[str,object])->pathlib.Path:
    run=root/run_id
    if run.is_symlink() or not run.is_dir() or stat.S_IMODE(run.stat(follow_symlinks=False).st_mode)!=0o700 or {p.name for p in run.iterdir()}!={"result.json","index.json"}:raise RuntimeError("RUNNER_EVIDENCE_RECOVERY_INVALID")
    raw=json.dumps(expected,sort_keys=True,separators=(",",":"),allow_nan=False).encode()+b"\n"
    for name in ("result.json","index.json"):
        path=run/name;observed=path.stat(follow_symlinks=False)
        if not stat.S_ISREG(observed.st_mode) or observed.st_nlink!=1 or stat.S_IMODE(observed.st_mode)!=0o600:raise RuntimeError("RUNNER_EVIDENCE_RECOVERY_INVALID")
    index=json.loads((run/"index.json").read_text());wanted={"schemaVersion":"runner-evidence-index-v1","runId":run_id,"artifacts":[{"locator":"result.json","size":len(raw),"sha256":hashlib.sha256(raw).hexdigest()}]}
    if index!=wanted or (run/"result.json").read_bytes()!=raw:raise RuntimeError("RUNNER_EVIDENCE_RECOVERY_INVALID")
    return run/"index.json"


def publish(root:pathlib.Path,run_id:str,temporary:pathlib.Path,expected:dict[str,object]|None=None)->pathlib.Path:
    run=root/run_id
    if run.exists():raise RuntimeError("RUNNER_EVIDENCE_CONFLICT")
    os.replace(temporary,run);root_fd=os.open(root,os.O_RDONLY);os.fsync(root_fd);os.close(root_fd)
    return verify(root,run_id,expected) if expected is not None else run/"index.json"


def reconcile(root:pathlib.Path,run_id:str,expected:dict[str,object])->pathlib.Path:
    published=root/run_id
    if published.is_dir():return verify(root,run_id,expected)
    candidates=list(root.glob(f".{run_id}.*.tmp"))
    if len(candidates)!=1:raise RuntimeError("RUNNER_EVIDENCE_RECOVERY_INVALID")
    return publish(root,run_id,candidates[0],expected)


def discard(temporary:pathlib.Path)->None:
    if temporary.parent.name!="evidence" or not temporary.name.startswith(".") or not temporary.name.endswith(".tmp"):raise RuntimeError("RUNNER_EVIDENCE_IDENTITY_INVALID")
    for name in ("result.json","index.json"):(temporary/name).unlink(missing_ok=True)
    temporary.rmdir()


def write(root: pathlib.Path, run_id: str, value: dict[str,object]) -> pathlib.Path:
    return publish(root,run_id,stage(root,run_id,value))
