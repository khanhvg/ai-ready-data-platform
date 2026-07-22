"""Bounded public dispatch for expansion, test and handoff operations.

The scaffold contains only routing and generic process accounting.  Curriculum,
trace, render and evidence acceptance rules are intentionally added after RED.
"""

from __future__ import annotations

import argparse
import hashlib
import os
from pathlib import Path
import signal
import subprocess
import sys
import time
from typing import Sequence

from .content_io import CheckResult, NormalizedRequest, content_sha256, normalize_request

ROOT = Path(__file__).resolve().parents[3]
MAX_OUTPUT = 1_048_576


def verify_expansions(request: NormalizedRequest) -> CheckResult:
    return CheckResult(
        "I11-EP-EXPANSION", True,
        details={"projectionSha256": content_sha256({"expansion": request.payload})},
    )


def clean_handoff(request: NormalizedRequest) -> CheckResult:
    return CheckResult(
        "I11-EP-HANDOFF", True,
        details={"projectionSha256": content_sha256({"handoff": request.payload})},
    )


def _terminate_group(process: subprocess.Popen[bytes]) -> tuple[bool, bool]:
    term_sent = kill_sent = False
    if process.poll() is None:
        os.killpg(process.pid, signal.SIGTERM)
        term_sent = True
        deadline = time.monotonic() + 5.0
        while process.poll() is None and time.monotonic() < deadline:
            time.sleep(0.05)
        if process.poll() is None:
            os.killpg(process.pid, signal.SIGKILL)
            kill_sent = True
    process.wait()
    return term_sent, kill_sent


def _run_owned(argv: Sequence[str], deadline_seconds: float) -> tuple[int, dict[str, object]]:
    started = time.monotonic()
    process = subprocess.Popen(
        list(argv), cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        start_new_session=True,
    )
    timed_out = False
    try:
        output, _ = process.communicate(timeout=deadline_seconds)
    except subprocess.TimeoutExpired:
        timed_out = True
        term_sent, kill_sent = _terminate_group(process)
        output, _ = process.communicate()
    else:
        term_sent = kill_sent = False
    if len(output) > MAX_OUTPUT:
        output = output[:MAX_OUTPUT]
    metrics: dict[str, object] = {
        "argv": list(argv), "elapsedMs": int((time.monotonic() - started) * 1000),
        "outputBytes": len(output), "outputSha256": hashlib.sha256(output).hexdigest(),
        "outputExcerpt": output[-16_384:].decode("utf-8", "replace"),
        "pgid": process.pid, "timedOut": timed_out, "termSent": term_sent,
        "killSent": kill_sent, "waited": process.poll() is not None,
    }
    return process.returncode, metrics


def _focused_tests() -> int:
    argv = [
        sys.executable, "-m", "unittest", "discover", "-s",
        "tests/learning/curriculum", "-p", "test_*.py", "-v",
    ]
    status, metrics = _run_owned(argv, 120.0)
    sys.stdout.write(str(metrics["outputExcerpt"]))
    return status


def _dispatch(name: str) -> int:
    if name == "run-focused-tests":
        return _focused_tests()
    request = normalize_request({}, source="public-cli")
    result = verify_expansions(request) if name == "verify-expansions" else clean_handoff(request)
    print({"entrypointId": result.entrypoint_id, "reached": result.reached, "codes": list(result.codes)})
    return 0 if result.ok else 1


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("run-focused-tests", "verify-expansions", "clean-handoff"))
    return _dispatch(parser.parse_args(argv).command)


if __name__ == "__main__":
    raise SystemExit(main())
