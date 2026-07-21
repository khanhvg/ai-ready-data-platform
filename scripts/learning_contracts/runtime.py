"""Read-only discovery of the manifest-admitted Issue #6 runtime."""
from __future__ import annotations

import os
from pathlib import Path
import subprocess
import sys

from .canonical import ContractError
from .schema import ROOT, sha256

LOCK_SHA = "f41c727b39f99106f95b7937b2811e8d27db89d1d5106e9f1d9effd4403143d2"
FREEZE_SHA = "cdb87ed71e0996f90041371cc25138afa02d78b134cbdc4afe9c25baa6649bba"
CLOUD_KEYS = {"AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY", "AWS_SESSION_TOKEN", "AWS_PROFILE", "AWS_DEFAULT_PROFILE", "GOOGLE_APPLICATION_CREDENTIALS", "AZURE_CLIENT_ID", "AZURE_CLIENT_SECRET"}


def _clean_environment() -> dict[str, str]:
    return {key: value for key, value in os.environ.items() if key not in CLOUD_KEYS and key != "PYTHONPATH"}


def candidates() -> list[Path]:
    return sorted(ROOT.glob(".artifacts/workspaces/golden/*/venv/bin/python"), reverse=True)


def verify(python: Path) -> None:
    if sha256(ROOT / "requirements/golden-py312-macos-arm64.lock") != LOCK_SHA:
        raise ContractError("DEPENDENCY_MANIFEST_DRIFT")
    script = "import importlib.metadata as m,platform; print(platform.python_version()); print('|'.join(m.version(x) for x in ('jsonschema','rfc8785','PyYAML')))"
    result = subprocess.run([str(python), "-c", script], env=_clean_environment(), stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=30, check=False)
    if result.returncode or result.stdout.splitlines() != ["3.12.3", "4.26.0|0.1.4|6.0.3"]:
        raise ContractError("DEPENDENCY_MANIFEST_DRIFT")
    check = subprocess.run([str(python), "-m", "pip", "check"], env=_clean_environment(), stdin=subprocess.DEVNULL, capture_output=True, timeout=30, check=False)
    if check.returncode: raise ContractError("DEPENDENCY_MANIFEST_DRIFT")
    freeze = subprocess.run([str(python), "-m", "pip", "freeze", "--all"], env=_clean_environment(), stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=30, check=True).stdout.splitlines()
    import hashlib
    digest = hashlib.sha256(("\n".join(sorted(freeze)) + "\n").encode()).hexdigest()
    if digest != FREEZE_SHA: raise ContractError("DEPENDENCY_MANIFEST_DRIFT")


def admitted_python() -> Path:
    for python in candidates():
        try: verify(python); return python
        except (ContractError, OSError, subprocess.SubprocessError): continue
    raise ContractError("GOLDEN_RUNTIME_REQUIRED")


def reexec_if_needed() -> None:
    python = admitted_python()
    if Path(sys.prefix).resolve() == python.parents[1].resolve(): return
    os.execve(str(python), [str(python), "-m", "scripts.learning_contracts.check", *sys.argv[1:]], _clean_environment())
