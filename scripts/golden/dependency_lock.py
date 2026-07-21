#!/usr/bin/env python3
"""Read-only verifier and hash-only installer for the golden Python lane."""

from __future__ import annotations

import argparse
import hashlib
import os
import pathlib
import platform
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
LOCK = ROOT / "requirements/golden-py312-macos-arm64.lock"
METADATA = ROOT / "requirements/golden-py312-macos-arm64.metadata.json"
EXPECTED_LOCK_SHA = "f41c727b39f99106f95b7937b2811e8d27db89d1d5106e9f1d9effd4403143d2"
EXPECTED_DISTRIBUTIONS = 56


class LockError(RuntimeError):
    pass


def platform_preflight(system: str | None = None, machine: str | None = None) -> None:
    actual_system = system or platform.system()
    actual_machine = machine or platform.machine()
    if sys.implementation.name != "cpython" or sys.version_info[:2] != (3, 12):
        raise LockError("PYTHON_BASELINE_UNSUPPORTED")
    if (actual_system, actual_machine) != ("Darwin", "arm64"):
        raise LockError("PYTHON_BASELINE_UNSUPPORTED")


def verify_lock(path: pathlib.Path = LOCK) -> dict[str, str]:
    data = path.read_bytes()
    if hashlib.sha256(data).hexdigest() != EXPECTED_LOCK_SHA:
        raise LockError("DEPENDENCY_LOCK_DRIFT")
    text = data.decode("utf-8")
    active = "\n".join(line for line in text.splitlines() if not line.lstrip().startswith("#"))
    forbidden = ("--index-url", "--extra-index-url", "--trusted-host", "git+", "file:", "-e ")
    if any(token in active for token in forbidden) or "--only-binary :all:" not in active:
        raise LockError("LOCK_POLICY_INVALID")
    packages = {}
    for line in text.splitlines():
        match = re.match(r"^([A-Za-z0-9_.-]+)==([^ \\]+) \\$", line)
        if match:
            key = re.sub(r"[-_.]+", "-", match.group(1)).lower()
            if key in packages:
                raise LockError("LOCK_DUPLICATE_DISTRIBUTION")
            packages[key] = match.group(2)
    if len(packages) != EXPECTED_DISTRIBUTIONS or packages.get("rfc8785") != "0.1.4":
        raise LockError("DEPENDENCY_LOCK_DRIFT")
    if any("--hash=sha256:" not in block for block in text.split("\n# via")[:0]):
        raise LockError("LOCK_HASH_MISSING")
    return packages


def install(venv_python: pathlib.Path, cache: pathlib.Path) -> None:
    platform_preflight()
    verify_lock()
    env = {
        "PATH": os.environ.get("PATH", ""),
        "PIP_CONFIG_FILE": "/dev/null",
        "PIP_CACHE_DIR": str(cache),
        "PIP_NO_INPUT": "1",
        "PIP_DISABLE_PIP_VERSION_CHECK": "1",
        "PYTHONNOUSERSITE": "1",
    }
    subprocess.run(
        [str(venv_python), "-m", "pip", "install", "--isolated", "--no-cache-dir",
         "--require-hashes", "--only-binary=:all:", "--no-deps", "-r", str(LOCK)],
        env=env, stdin=subprocess.DEVNULL, check=True, timeout=120,
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    try:
        platform_preflight()
        packages = verify_lock()
    except (LockError, OSError) as exc:
        print(str(exc), file=sys.stderr)
        return 2
    if args.verify:
        print(f"lock verified: {len(packages)} distributions")
    return 0


if __name__ == "__main__":
    sys.exit(main())
