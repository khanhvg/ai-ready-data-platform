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
    payload = request.payload
    codes: list[str] = []
    if render := payload.get("render"):
        if render.get("sourceHash") != render.get("freshnessSourceHash"): codes.append("I11_RENDER_STALE")
        if len(set(render.get("runHashes", []))) != 1: codes.append("I11_RENDER_NONDETERMINISTIC")
        if not render.get("safe"): codes.append("I11_RENDER_UNSAFE")
        if render.get("semanticHash") == render.get("mutatedSemanticHash"): codes.append("I11_RENDER_SEMANTIC_ERASURE")
    if protected := payload.get("protected"):
        if protected.get("expectedCount") != protected.get("actualCount") or protected.get("drift"):
            codes.append("I11_PROTECTED_IDENTITY_DRIFT")
    if resources := payload.get("resources"):
        rules = (
            ("deadline", "I11_RESOURCE_DEADLINE"), ("rssExceeded", "I11_RESOURCE_RSS"),
            ("processExceeded", "I11_RESOURCE_PROCESS_COUNT"), ("outputExceeded", "I11_RESOURCE_OUTPUT"),
            ("fileCountExceeded", "I11_RESOURCE_FILE_COUNT"), ("fileBytesExceeded", "I11_RESOURCE_FILE_BYTES"),
        )
        codes.extend(code for field, code in rules if resources.get(field))
        inverse = (("owned", "I11_RESOURCE_OWNERSHIP"), ("termOk", "I11_RESOURCE_TERM"),
                   ("killOk", "I11_RESOURCE_KILL"), ("reaped", "I11_RESOURCE_REAP"),
                   ("measurementsComplete", "I11_RESOURCE_MEASUREMENT_MISSING"))
        codes.extend(code for field, code in inverse if not resources.get(field))
    if visual := payload.get("visual"):
        rules = (
            (not visual.get("vietnameseFirst"), "I11_VISUAL_LANGUAGE"),
            (visual.get("numberingCount") != 1, "I11_VISUAL_NUMBERING"),
            (visual.get("minFont", 0) < 14, "I11_VISUAL_FIT_FONT"),
            (visual.get("aspect", 99) > 2.4, "I11_VISUAL_ASPECT"),
            (not visual.get("onCanvas"), "I11_VISUAL_CANVAS"),
            (visual.get("overlap"), "I11_VISUAL_OVERLAP"),
            (visual.get("clipping"), "I11_VISUAL_CLIPPING"),
            (visual.get("contrast", 0) < 4.5, "I11_VISUAL_CONTRAST"),
            (not visual.get("accessible"), "I11_VISUAL_ACCESSIBILITY"),
            (not visual.get("textParity"), "I11_VISUAL_TEXT_PARITY"),
            (not visual.get("humanReview"), "I11_VISUAL_HUMAN_REVIEW_MISSING"),
        )
        codes.extend(code for failed, code in rules if failed)
    return CheckResult(
        "I11-EP-EXPANSION", True, tuple(codes),
        details={"projectionSha256": content_sha256({"expansion": request.payload})},
    )


def clean_handoff(request: NormalizedRequest) -> CheckResult:
    payload = request.payload
    codes: list[str] = []
    if security := payload.get("security"):
        rules = (("secretFindings", "I11_S3_SECRET"), ("privatePaths", "I11_S3_PRIVATE_PATH"),
                 ("externalUrls", "I11_S3_EXTERNAL_URL"), ("cloudActions", "I11_S3_CLOUD_ACTION"))
        codes.extend(code for field, code in rules if security.get(field))
    if bounds := payload.get("bounds"):
        if bounds.get("bytes", 0) > bounds.get("maxBytes", 0): codes.append("I11_BOUND_SIZE")
        if bounds.get("depth", 0) > bounds.get("maxDepth", 0): codes.append("I11_BOUND_DEPTH")
        if bounds.get("duplicateKeys"): codes.append("I11_BOUND_DUPLICATE_KEY")
        if not bounds.get("regularFile"): codes.append("I11_BOUND_SPECIAL_FILE")
    if evidence := payload.get("evidence"):
        rules = (("missing", "I11_EVIDENCE_MISSING"), ("duplicates", "I11_EVIDENCE_DUPLICATE"),
                 ("orphans", "I11_EVIDENCE_ORPHAN"), ("stale", "I11_EVIDENCE_STALE"),
                 ("tampered", "I11_EVIDENCE_TAMPERED"), ("privacyFindings", "I11_EVIDENCE_PRIVACY"))
        codes.extend(code for field, code in rules if evidence.get(field))
    if cleanup := payload.get("cleanup"):
        rules = (("nonignoredDirty", "I11_CLEAN_NONIGNORED_DIRTY"),
                 ("ignoredUnowned", "I11_CLEAN_IGNORED_UNOWNED"),
                 ("ownershipDrift", "I11_CLEAN_OWNERSHIP_DRIFT"))
        codes.extend(code for field, code in rules if cleanup.get(field))
        if cleanup.get("porcelainBytes") != 0: codes.append("I11_CLEAN_PORCELAIN_NONEMPTY")
        if not cleanup.get("rollbackExact"): codes.append("I11_CLEAN_ROLLBACK_SCOPE")
    return CheckResult(
        "I11-EP-HANDOFF", True, tuple(codes),
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
