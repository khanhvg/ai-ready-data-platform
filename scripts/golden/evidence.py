#!/usr/bin/env python3
"""Safe evidence selection and atomic publication primitives."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import pathlib
import re
import datetime
from typing import Any


ROOT = pathlib.Path(__file__).resolve().parents[2]
WORKSPACE_PATH = ROOT / "scripts/golden/workspace.py"
_spec = importlib.util.spec_from_file_location("golden_workspace_for_evidence", WORKSPACE_PATH)
assert _spec and _spec.loader
workspace = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(workspace)


class EvidenceError(RuntimeError):
    pass


SENSITIVE = (
    re.compile(r"(?i)(token|password|secret|credential|private[_ -]?key)\s*[:=]"),
    re.compile(r"(?i)https?://[^/@\s:]+:[^/@\s]+@"),
    re.compile(r"/(Users|home)/[^/\s]+"),
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
)


def assert_safe_text(value: str) -> None:
    if any(pattern.search(value) for pattern in SENSITIVE):
        raise EvidenceError("EVIDENCE_SENSITIVE_CONTENT")


def canonical_json(value: Any) -> bytes:
    data = (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode()
    assert_safe_text(data.decode("utf-8"))
    return data


def fitness_envelope(*, fitness_id: str, result: str, tested_tree_sha: str, projection_sha256: str) -> dict[str, Any]:
    if result not in {"pass", "fail"}:
        raise EvidenceError("EVIDENCE_RESULT_INVALID")
    if not re.fullmatch(r"[0-9a-f]{40}", tested_tree_sha) or not re.fullmatch(r"[0-9a-f]{64}", projection_sha256):
        raise EvidenceError("EVIDENCE_DIGEST_INVALID")
    if result != "pass": raise EvidenceError("EVIDENCE_FAILURE_REQUIRES_TYPED_BUILDER")
    spec=importlib.util.spec_from_file_location("golden_fitness",ROOT/"scripts/golden/fitness.py"); assert spec and spec.loader
    module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    return module.passed(command_id=fitness_id,tested_tree_sha=tested_tree_sha,projection_sha256=projection_sha256,started_at=datetime.datetime.now(datetime.timezone.utc),duration_ms=0)


def publish_json(parent_fd: int, name: str, value: Any) -> str:
    payload = canonical_json(value)
    workspace.atomic_write(parent_fd, name, payload)
    return hashlib.sha256(payload).hexdigest()
