"""Runtime, dependency, authority, and cleanup admission rules."""
from __future__ import annotations

import hashlib
import json
import os
import pathlib
import stat
import subprocess
import sys
import time
from typing import Any

EXPECTED_LOCK_SHA = "f41c727b39f99106f95b7937b2811e8d27db89d1d5106e9f1d9effd4403143d2"
ADMITTED_IMPORTS = {"jsonschema", "rfc8785", "yaml"}
FORBIDDEN_READ_PREFIXES = ("spikes/web/", "portal/", "runner/", "contracts/adr/")
FREEZE_SHA = "cdb87ed71e0996f90041371cc25138afa02d78b134cbdc4afe9c25baa6649bba"
ROOT = pathlib.Path(__file__).resolve().parents[2]


def authority_code(value: dict[str, Any]) -> str:
    identities = [value.get(name) for name in ("local", "tracking", "live")]
    if any(identities) and len(set(identities)) != 1:
        return "AUTHORITY_HEAD_MISMATCH"
    if "leaseOwners" in value and value["leaseOwners"] != ["I5-03"]:
        return "AUTHORITY_LEASE_REQUIRED"
    if value.get("protectedExpected") != value.get("protectedActual") and "protectedExpected" in value:
        return "PROTECTED_PATH_CHANGED"
    if value.get("fixtureManifestHash") != value.get("artifactHash") and "fixtureManifestHash" in value:
        return "FIXTURE_MANIFEST_ARTIFACT_MISMATCH"
    if any(str(path).startswith(FORBIDDEN_READ_PREFIXES) for path in value.get("reads", [])):
        return "STAGE_A_FRAMEWORK_DEPENDENCY"
    return "OK"


def dependency_code(value: dict[str, Any]) -> str:
    if any(name not in ADMITTED_IMPORTS for name in value.get("imports", [])):
        return "DEPENDENCY_IMPORT_UNADMITTED"
    if "lockSha256" in value and value["lockSha256"] != EXPECTED_LOCK_SHA:
        return "DEPENDENCY_MANIFEST_DRIFT"
    if "inheritedAdvisoryDisposition" in value and value["inheritedAdvisoryDisposition"] != "reviewed-inherited-no-delta":
        return "DEPENDENCY_ADVISORY_UNRESOLVED"
    return "OK"


def rollback_code(value: dict[str, Any]) -> str:
    if not value.get("owned") or value.get("marker") != "learning-contracts-v1" or value.get("links") != 1:
        return "ROLLBACK_SCOPE_UNOWNED"
    return "OK"


def _verified_python() -> pathlib.Path:
    evidence_parent = ROOT / ".artifacts/evidence/golden"
    workspace_parent = ROOT / ".artifacts/workspaces/golden"
    candidates = sorted((path for path in evidence_parent.iterdir() if path.is_dir() and not path.is_symlink()), key=lambda path: path.stat().st_mtime, reverse=True) if evidence_parent.is_dir() else []
    for evidence_root in candidates:
        workspace = workspace_parent / evidence_root.name
        marker_path = workspace / ".golden-owner.json"
        python = workspace / "venv/bin/python"
        if not marker_path.is_file() or not python.is_file() or workspace.is_symlink():
            continue
        marker = json.loads(marker_path.read_text(encoding="utf-8"))
        info = workspace.stat()
        if marker.get("runId") != evidence_root.name or marker.get("purpose") != "golden-run" or stat.S_IMODE(info.st_mode) & 0o077:
            continue
        env = _clean_environment(workspace)
        frozen = subprocess.run([str(python), "-m", "pip", "freeze", "--all"], cwd=ROOT, env=env, stdin=subprocess.DEVNULL, capture_output=True, check=True, timeout=30).stdout
        normalized = b"\n".join(sorted(line.strip() for line in frozen.splitlines() if line.strip())) + b"\n"
        if hashlib.sha256(normalized).hexdigest() != FREEZE_SHA:
            continue
        subprocess.run([str(python), "-m", "pip", "check"], cwd=ROOT, env=env, stdin=subprocess.DEVNULL, capture_output=True, check=True, timeout=30)
        return python
    raise SystemExit("GOLDEN_RUNTIME_REQUIRED")


def _clean_environment(workspace: pathlib.Path) -> dict[str, str]:
    venv = workspace / "venv"
    allowed = {"TZ": "UTC", "LC_ALL": "C.UTF-8", "LANG": "C.UTF-8", "PYTHONHASHSEED": "0", "PYTHONDONTWRITEBYTECODE": "1", "PYTHONNOUSERSITE": "1", "PIP_CONFIG_FILE": "/dev/null", "PIP_DISABLE_PIP_VERSION_CHECK": "1", "PIP_NO_INPUT": "1"}
    allowed["PATH"] = f"{venv / 'bin'}:/usr/bin:/bin:/usr/sbin:/sbin"
    allowed["HOME"] = str(workspace / "home")
    allowed["TMPDIR"] = str(workspace / "home/tmp")
    allowed["VIRTUAL_ENV"] = str(venv)
    return allowed


def launch(argv: list[str]) -> int:
    python = _verified_python()
    workspace = python.parents[2]
    command = [str(python), "-m", "scripts.learning_contracts.check", *argv]
    started = time.monotonic()
    try:
        result = subprocess.run(command, cwd=ROOT, env=_clean_environment(workspace), stdin=subprocess.DEVNULL, capture_output=True, timeout=300, check=False)
    except subprocess.TimeoutExpired as exc:
        raise SystemExit("RESOURCE_TIME_LIMIT") from exc
    if len(result.stdout) > 2 * 1024 * 1024 or len(result.stderr) > 2 * 1024 * 1024:
        raise SystemExit("RESOURCE_OUTPUT_LIMIT")
    if time.monotonic() - started > 300:
        raise SystemExit("RESOURCE_TIME_LIMIT")
    sys.stdout.buffer.write(result.stdout); sys.stderr.buffer.write(result.stderr)
    return result.returncode


def resource_limits() -> dict[str, int]:
    """Return enforceable public command and process ceilings."""
    return {}


if __name__ == "__main__":
    raise SystemExit(launch(sys.argv[1:]))
