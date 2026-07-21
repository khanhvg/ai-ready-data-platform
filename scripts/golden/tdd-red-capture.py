#!/usr/bin/env python3
"""Run one audited RED command and retain a bounded, sanitized result."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import pathlib
import re
import subprocess
import sys
import time
from datetime import datetime, timezone

ROOT = pathlib.Path(__file__).resolve().parents[2]
ARTIFACT_ROOT = ROOT / ".artifacts" / "evidence" / "tdd-red"
MAX_OUTPUT = 2 * 1024 * 1024
SAFE_ID = re.compile(r"^[A-Z0-9-]+$")


def _relative_text(data: bytes) -> str:
    text = data[:MAX_OUTPUT].decode("utf-8", "replace")
    root = str(ROOT)
    text = text.replace(root, "<repo>")
    text = re.sub(r"/" r"Users/[^/\s]+", "<private-home>", text)
    return text


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", required=True, choices=[str(i) for i in range(1, 9)])
    parser.add_argument("--expected-id", action="append", required=True)
    parser.add_argument("--implementation-input", required=True)
    parser.add_argument("--expected-missing", required=True)
    parser.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    command = args.command[1:] if args.command[:1] == ["--"] else args.command
    if not command or any(not SAFE_ID.fullmatch(item) for item in args.expected_id):
        parser.error("a command and safe expected IDs are required")
    if not re.fullmatch(r"[0-9a-f]{40}", args.implementation_input):
        parser.error("implementation input must be a full lowercase commit SHA")

    status = subprocess.check_output(
        ["git", "status", "--porcelain=v1", "--untracked-files=all"], cwd=ROOT
    )
    clean_digest = hashlib.sha256(status).hexdigest()
    started_wall = datetime.now(timezone.utc)
    started = time.monotonic()
    completed = subprocess.run(
        command,
        cwd=ROOT,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=120,
        env={key: value for key, value in os.environ.items() if key != "PYTHONPATH"},
        check=False,
    )
    duration_ms = round((time.monotonic() - started) * 1000)
    output = _relative_text(completed.stdout)
    found = [item for item in args.expected_id if item in output]
    valid_red = completed.returncode != 0 and found == args.expected_id
    run_id = started_wall.strftime("%Y%m%dT%H%M%S%fZ")
    out_dir = ARTIFACT_ROOT / f"P{args.phase}" / run_id
    out_dir.mkdir(mode=0o700, parents=True, exist_ok=False)
    os.chmod(ARTIFACT_ROOT.parents[1], 0o700)
    output_bytes = output.encode("utf-8")
    (out_dir / "bounded-output.txt").write_bytes(output_bytes)
    result = {
        "schemaVersion": "tdd-red-result-v1",
        "phase": int(args.phase),
        "redIds": args.expected_id,
        "observedRedIds": found,
        "implementationInputSha": args.implementation_input,
        "cleanTreeDigest": clean_digest,
        "command": command,
        "startedAt": started_wall.isoformat().replace("+00:00", "Z"),
        "finishedAt": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "durationMs": duration_ms,
        "expectedMissingBehavior": args.expected_missing,
        "actualFailure": "required behavior absent" if valid_red else "unexpected RED result",
        "exitCode": completed.returncode,
        "output": {
            "locator": "bounded-output.txt",
            "sha256": hashlib.sha256(output_bytes).hexdigest(),
            "truncated": len(completed.stdout) > MAX_OUTPUT,
        },
        "validRed": valid_red,
    }
    (out_dir / "red-result.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(out_dir.relative_to(ROOT))
    return 0 if valid_red else 2


if __name__ == "__main__":
    sys.exit(main())
