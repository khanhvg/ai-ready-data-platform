"""Closed bounded supervisor result protocol."""
from __future__ import annotations
import json, pathlib
LIMIT=65_536


def write(path:pathlib.Path,value:dict[str,object])->None:
    raw=json.dumps(value,sort_keys=True,separators=(",",":"),allow_nan=False).encode()+b"\n"
    if len(raw)>LIMIT: raise RuntimeError("RUNNER_PROTOCOL_LIMIT")
    path.write_bytes(raw)


def read(path:pathlib.Path)->dict[str,object]:
    raw=path.read_bytes()
    if len(raw)>LIMIT: raise RuntimeError("RUNNER_PROTOCOL_LIMIT")
    value=json.loads(raw)
    if type(value) is not dict or set(value)-{"schemaVersion","operationId","status","result","failureCode","stdoutBytes","stderrBytes","descendantPeak","resourceTrackerObserved","cgroup"}:
        raise RuntimeError("RUNNER_PROTOCOL_INVALID")
    if value.get("schemaVersion")!="runner-container-result-v1" or value.get("status") not in ("pass","fail"):
        raise RuntimeError("RUNNER_PROTOCOL_INVALID")
    return value
