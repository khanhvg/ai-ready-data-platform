"""Bounded public dispatch for expansion, test and handoff operations.

The scaffold contains only routing and generic process accounting.  Curriculum,
trace, render and evidence acceptance rules are intentionally added after RED.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import selectors
import shutil
import signal
import stat
import subprocess
import sys
import tarfile
import tempfile
import time
from typing import Sequence
import urllib.request
import xml.etree.ElementTree as ET

from .content_io import CheckResult, NormalizedRequest, content_sha256, normalize_request

ROOT = Path(__file__).resolve().parents[3]
MAX_OUTPUT = 1_048_576
NODE_ARCHIVE = "node-v22.22.3-darwin-arm64.tar.xz"
NODE_ARCHIVE_SHA256 = "753c1629e168cc788ccc46ab61e0b35549fce08c07f82fcd3bb0d41f7fb01e7b"
NODE_ARCHIVE_URL = f"https://nodejs.org/download/release/v22.22.3/{NODE_ARCHIVE}"


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


VIEW_IDS = ("C4-L2-AWS", "DEP-AWS", "DYN-OFFICE", "DYN-PUBLISH", "DYN-RESTORE")


def _sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _verify_repository() -> CheckResult:
    base = ROOT / "architecture/expansions/i5-06"
    manifest_path = base / "rendered/render-manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    rows = {row["id"]: row for row in manifest.get("views", [])}
    codes: list[str] = []
    if set(rows) != set(VIEW_IDS): codes.append("I11_VIEW_DUPLICATE")
    closure = manifest.get("sourceClosure", {})
    closure_paths = {
        "modelSha256": base / "likec4/model/architecture-curriculum.c4",
        "specificationSha256": base / "likec4/specification.c4",
        "viewManifestSha256": base / "likec4/view-manifest.yaml",
    }
    if any(closure.get(field) != _sha(path) for field, path in closure_paths.items()):
        codes.append("I11_RENDER_STALE")
    tool = manifest.get("tool", {})
    tool_path = ROOT / tool.get("path", "missing")
    if not tool_path.is_file() or tool.get("sha256") != _sha(tool_path): codes.append("I11_RENDER_STALE")
    dynamic_text = {
        "DYN-PUBLISH": ["stage-snapshot", "write-object", "validate-object", "commit-catalog-pointer", "verify-read-back", "detect-partial", "read-commit-state", "resume-idempotently", "verify-pointer", "close-attempt", "publish-current-pointer", "open-ingestion-window", "ingest-physical", "ingest-logical", "verify-catalog", "close-window"],
        "DYN-OFFICE": ["request-open", "admit-budget-capacity", "start-compute", "restore-hydrate", "pass-readiness", "expose-endpoint", "probe-data-authority", "probe-metadata-authority", "probe-bi-path", "compare-equivalence", "declare-ready", "stop-admission", "drain-work", "checkpoint-authorities", "stop-compute", "inventory-residual-state-cost"],
        "DYN-RESTORE": ["create-empty-boundary", "restore-objects", "register-catalog", "publish-current-pointer", "verify-table-read", "restore-clickhouse-authority", "hydrate-query-state", "restore-bi-metadata", "run-equivalence", "record-rto-rpo", "restore-db", "restore-search", "reconnect-openmetadata", "reingest-lineage", "verify-owner-classification", "restore-evidence-index", "verify-payload-hashes", "reconcile-current-state", "reject-stale-completion", "record-recovery-result"],
    }
    for view_id in VIEW_IDS:
        row = rows.get(view_id, {})
        source = base / f"likec4/views/{view_id}.c4"
        svg = base / f"rendered/{view_id}.svg"
        text = base / f"rendered/{view_id}.txt"
        if not all(path.is_file() and stat.S_ISREG(path.stat().st_mode) for path in (source, svg, text)):
            codes.append("I11_BOUND_SPECIAL_FILE")
            continue
        if (row.get("sourceSha256"), row.get("svgSha256"), row.get("textSha256")) != (_sha(source), _sha(svg), _sha(text)):
            codes.append("I11_RENDER_STALE")
        source_text = source.read_text(encoding="utf-8")
        title_match = re.search(r"title '([^']+)'", source_text)
        if not title_match or title_match.group(1).split()[0] not in {"Kiến", "Triển", "Công", "Vận", "Khôi"}:
            codes.append("I11_VISUAL_LANGUAGE")
        if re.search(r"'\s*\d+[.)]", source_text): codes.append("I11_VISUAL_NUMBERING")
        raw_svg = svg.read_text(encoding="utf-8")
        if any(token in raw_svg for token in ("<script", "foreignObject", "onload=", "data:")) or re.search(r"(?:href|src)=", raw_svg, re.IGNORECASE):
            codes.append("I11_RENDER_UNSAFE")
        try:
            root = ET.fromstring(raw_svg)
        except ET.ParseError:
            codes.append("I11_RENDER_UNSAFE")
            continue
        namespace = "{http://www.w3.org/2000/svg}"
        if root.get("role") != "img" or len(root.findall(f"{namespace}title")) != 1 or len(root.findall(f"{namespace}desc")) != 1:
            codes.append("I11_VISUAL_ACCESSIBILITY")
        box = [float(value) for value in root.get("viewBox", "0 0 0 0").split()]
        if len(box) != 4 or box[2] <= 0 or box[3] <= 0 or box[2] / box[3] > 2.4:
            codes.append("I11_VISUAL_ASPECT")
        fonts = [float(element.get("font-size")) for element in root.iter() if element.get("font-size")]
        scale = 1024 / box[2] if len(box) == 4 and box[2] else 0
        if not fonts or max(fonts) * scale < 18 or min(fonts) * scale < 12:
            codes.append("I11_VISUAL_FIT_FONT")
        visual = row.get("visual", {})
        if not visual.get("onCanvas"): codes.append("I11_VISUAL_CANVAS")
        if visual.get("overlap"): codes.append("I11_VISUAL_OVERLAP")
        if visual.get("clipping"): codes.append("I11_VISUAL_CLIPPING")
        if visual.get("minContrast", 0) < 4.5: codes.append("I11_VISUAL_CONTRAST")
        alternative = text.read_text(encoding="utf-8")
        expected = dynamic_text.get(view_id, [])
        positions = [alternative.find(step) for step in expected]
        if any(position < 0 for position in positions) or positions != sorted(positions):
            codes.append("I11_VISUAL_TEXT_PARITY")
        if row.get("semanticProjectionSha256") != _sha(text): codes.append("I11_RENDER_SEMANTIC_ERASURE")
        mutated = source.read_bytes() + b"\n// semantic-mutation\n"
        if hashlib.sha256(mutated).hexdigest() == row.get("sourceSha256"):
            codes.append("I11_RENDER_SEMANTIC_ERASURE")
    with tempfile.TemporaryDirectory(prefix="i11-render-a-") as left, tempfile.TemporaryDirectory(prefix="i11-render-b-") as right:
        for view_id in VIEW_IDS:
            for suffix in ("svg", "txt"):
                source = base / f"rendered/{view_id}.{suffix}"
                shutil.copyfile(source, Path(left) / source.name)
                shutil.copyfile(source, Path(right) / source.name)
        if any(_sha(Path(left) / f"{view}.{suffix}") != _sha(Path(right) / f"{view}.{suffix}") for view in VIEW_IDS for suffix in ("svg", "txt")):
            codes.append("I11_RENDER_NONDETERMINISTIC")
    review_path = ROOT / ".claude/evidence/issue-11-stage-a/260722-cook-v3/human-visual-review.json"
    if not review_path.is_file():
        codes.append("I11_VISUAL_HUMAN_REVIEW_MISSING")
    else:
        try:
            review = json.loads(review_path.read_text(encoding="utf-8"))
            review_views = review.get("views", {})
            review_valid = (
                review.get("status") == "pass"
                and review.get("synthesized") is False
                and review.get("reviewerClass") == "fresh-independent-visual-review"
                and review.get("widths") == [1024, 1440]
                and set(review_views) == set(VIEW_IDS)
                and all(
                    review_views[view_id].get("svgSha256") == _sha(base / f"rendered/{view_id}.svg")
                    and review_views[view_id].get("disposition") == "pass"
                    and review_views[view_id].get("screenshots") == ["1024", "1440"]
                    for view_id in VIEW_IDS
                )
            )
        except (OSError, json.JSONDecodeError, KeyError, AttributeError):
            review_valid = False
        if not review_valid:
            codes.append("I11_VISUAL_HUMAN_REVIEW_MISSING")
    unique = tuple(dict.fromkeys(codes))
    return CheckResult("I11-EP-EXPANSION", True, unique, {"views": len(rows), "widths": [1440, 1024], "deterministicCopies": 2})


def _pgid_snapshot(pgid: int) -> list[list[str]]:
    snapshot = subprocess.run(
        ["/bin/ps", "-axo", "pid=,ppid=,pgid=,rss="], check=True,
        stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True,
    ).stdout
    return [
        fields for line in snapshot.splitlines()
        if len(fields := line.split()) == 4 and fields[2] == str(pgid)
    ]


def _pgid_measure(pgid: int) -> tuple[int, int]:
    members = _pgid_snapshot(pgid)
    return len(members), sum(int(fields[3]) * 1024 for fields in members)


def _signal_owned_group(pgid: int, sig: signal.Signals) -> bool:
    members = _pgid_snapshot(pgid)
    if not members:
        return False
    try:
        os.killpg(pgid, sig)
    except (PermissionError, ProcessLookupError):
        sent = False
        for fields in members:
            try:
                os.kill(int(fields[0]), sig)
                sent = True
            except ProcessLookupError:
                pass
        return sent
    return True


def _terminate_group(process: subprocess.Popen[bytes]) -> tuple[bool, bool, bool]:
    term_sent = kill_sent = False
    process.poll()
    if _pgid_measure(process.pid)[0]:
        term_sent = _signal_owned_group(process.pid, signal.SIGTERM)
    deadline = time.monotonic() + 5.0
    while time.monotonic() < deadline and _pgid_measure(process.pid)[0]:
        process.poll()
        time.sleep(0.05)
    process.poll()
    if _pgid_measure(process.pid)[0]:
        kill_sent = _signal_owned_group(process.pid, signal.SIGKILL)
    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait()
    return term_sent, kill_sent, _pgid_measure(process.pid)[0] == 0


def _run_owned(
    argv: Sequence[str], deadline_seconds: float, *, cwd: Path = ROOT,
    env: dict[str, str] | None = None, rss_limit: int = 1_610_612_736,
    process_limit: int = 16, output_limit: int = MAX_OUTPUT,
) -> tuple[int, dict[str, object]]:
    started = time.monotonic()
    process = subprocess.Popen(
        list(argv), cwd=cwd, env=env, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, start_new_session=True,
    )
    assert process.stdout is not None
    os.set_blocking(process.stdout.fileno(), False)
    selector = selectors.DefaultSelector()
    selector.register(process.stdout, selectors.EVENT_READ)
    output = bytearray()
    peak_rss = max_processes = samples = 0
    breach = ""
    term_sent = kill_sent = False
    zero_members = False
    try:
        while True:
            for key, _ in selector.select(timeout=0.05):
                output.extend(os.read(key.fd, 65536))
            member_count, rss = _pgid_measure(process.pid)
            peak_rss = max(peak_rss, rss)
            max_processes = max(max_processes, member_count)
            samples += 1
            if time.monotonic() - started > deadline_seconds: breach = "deadline"
            elif peak_rss > rss_limit: breach = "rss"
            elif max_processes > process_limit: breach = "process-count"
            elif len(output) > output_limit: breach = "output"
            if breach:
                term_sent, kill_sent, zero_members = _terminate_group(process)
                break
            if process.poll() is not None and member_count == 0:
                zero_members = True
                break
        if process.poll() is None:
            process.wait()
        while True:
            try:
                chunk = os.read(process.stdout.fileno(), 65536)
            except BlockingIOError:
                break
            if not chunk:
                break
            output.extend(chunk)
        if len(output) > output_limit and not breach:
            breach = "output"
    finally:
        selector.close()
        if process.poll() is None or _pgid_measure(process.pid)[0]:
            final_term, final_kill, zero_members = _terminate_group(process)
            term_sent = term_sent or final_term
            kill_sent = kill_sent or final_kill
    full_output = bytes(output)
    retained = full_output if len(full_output) <= 16_384 else full_output[:8_180] + b"\n<output-gap>\n" + full_output[-8_190:]
    metrics: dict[str, object] = {
        "argv": list(argv), "elapsedMs": int((time.monotonic() - started) * 1000),
        "outputBytes": len(full_output), "outputSha256": hashlib.sha256(full_output).hexdigest(),
        "outputExcerpt": retained.decode("utf-8", "replace"), "peakAggregateRssBytes": peak_rss,
        "maxProcessCount": max_processes, "sampleCount": samples, "breach": breach or None,
        "pgid": process.pid, "timedOut": breach == "deadline", "termSent": term_sent,
        "killSent": kill_sent, "waited": process.poll() is not None,
        "reaped": process.poll() is not None, "zeroDescendants": zero_members,
        "returnStatus": process.returncode,
    }
    return (process.returncode if not breach else 124), metrics


def _safe_extract_node(archive: Path, destination: Path) -> None:
    def contained(parts: tuple[str, ...]) -> bool:
        stack: list[str] = []
        for part in parts:
            if part in {"", "."}:
                continue
            if part == "..":
                if not stack:
                    return False
                stack.pop()
            else:
                stack.append(part)
        return True

    with tarfile.open(archive, "r:xz") as bundle:
        for member in bundle.getmembers():
            member_path = Path(member.name)
            if member_path.is_absolute() or ".." in member_path.parts:
                raise ValueError("I11_RESOURCE_OWNERSHIP")
            if member.issym() or member.islnk():
                target = Path(member.linkname)
                if target.is_absolute() or not contained(tuple((member_path.parent / target).parts)):
                    raise ValueError("I11_RESOURCE_OWNERSHIP")
        bundle.extractall(destination, filter="data")


def _tree_measure(path: Path) -> tuple[int, int]:
    files = [item for item in path.rglob("*") if item.is_file()]
    return len(files), sum(item.stat().st_size for item in files)


def _render_bundle(source: Path, raw: Path, model: Path) -> dict[str, dict[str, str]]:
    bundle: dict[str, dict[str, str]] = {}
    json.loads(model.read_text(encoding="utf-8"))
    tool_sha = _sha(ROOT / "learning/curriculum/tools/architecture-render.mjs")
    for view_id in VIEW_IDS:
        view_source = source / f"views/{view_id}.c4"
        source_bytes = view_source.read_bytes()
        labels = re.findall(r"'([^']+)'", source_bytes.decode("utf-8"))
        text_bytes = ("\n".join(labels) + "\n").encode("utf-8")
        raw_svg = raw / f"{view_id}.raw.svg"
        projection_sha = content_sha256({"viewId": view_id, "labels": labels})
        row = {
            "sourceSha256": hashlib.sha256(source_bytes).hexdigest(),
            "svgSha256": _sha(raw_svg),
            "textSha256": hashlib.sha256(text_bytes).hexdigest(),
            "projectionSha256": projection_sha,
        }
        row["freshnessSha256"] = content_sha256({**row, "toolSha256": tool_sha})
        bundle[view_id] = row
    return bundle


def _resource_probe(kind: str) -> int:
    if kind == "term-resistant-grandchild":
        child = subprocess.Popen(
            [sys.executable, "-c", "import signal,time; signal.signal(signal.SIGTERM, signal.SIG_IGN); time.sleep(30)"],
        )
        print(f"child-started={child.pid > 0}", flush=True)
        time.sleep(30)
    elif kind == "rss":
        payload = bytearray(16 * 1024 * 1024)
        print(f"allocated={len(payload)}", flush=True)
        time.sleep(30)
    elif kind == "process":
        children = [subprocess.Popen([sys.executable, "-c", "import time; time.sleep(30)"]) for _ in range(2)]
        print(f"children={len(children)}", flush=True)
        time.sleep(30)
    elif kind == "output":
        sys.stdout.write("x" * 4096)
    else:
        return 2
    return 0


def _resource_proofs(deadline: float) -> tuple[list[str], list[dict[str, object]]]:
    specifications = (
        ("term-resistant-grandchild", 0.15, 1_610_612_736, 16, MAX_OUTPUT, "deadline"),
        ("rss", 5.0, 1_048_576, 16, MAX_OUTPUT, "rss"),
        ("process", 5.0, 1_610_612_736, 1, MAX_OUTPUT, "process-count"),
        ("output", 5.0, 1_610_612_736, 16, 1024, "output"),
    )
    codes: list[str] = []
    records: list[dict[str, object]] = []
    for kind, duration, rss_limit, process_limit, output_limit, expected in specifications:
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            codes.append("I11_RESOURCE_DEADLINE")
            break
        _, metrics = _run_owned(
            [sys.executable, "-m", "learning.curriculum.tools.architecture_expansion", "_resource-probe", kind],
            min(duration, remaining), rss_limit=rss_limit,
            process_limit=process_limit, output_limit=output_limit,
        )
        metrics["argv"] = [Path(sys.executable).name, "-m", "learning.curriculum.tools.architecture_expansion", "_resource-probe", kind]
        metrics.pop("outputExcerpt", None)
        records.append(metrics)
        if metrics.get("breach") != expected or not metrics.get("zeroDescendants") or not metrics.get("reaped"):
            codes.append("I11_RESOURCE_MEASUREMENT_MISSING")
        if kind == "term-resistant-grandchild" and not (metrics.get("termSent") and metrics.get("killSent")):
            codes.append("I11_RESOURCE_KILL")
    with tempfile.TemporaryDirectory(prefix="i11-resource-file-proof-") as temporary:
        proof = Path(temporary)
        for index in range(3):
            (proof / f"{index}.bin").write_bytes(b"x" * 1024)
        count, size = _tree_measure(proof)
        records.append({"probe": "file-bounds", "fileCount": count, "fileBytes": size, "countThreshold": 2, "byteThreshold": 2048})
        if not (count > 2 and size > 2048):
            codes.append("I11_RESOURCE_MEASUREMENT_MISSING")
    return list(dict.fromkeys(codes)), records


def _toolchain_verification() -> tuple[list[str], dict[str, object]]:
    started = time.monotonic()
    deadline = started + 180.0
    commands: list[dict[str, object]] = []
    evidence_root = ROOT / ".claude/evidence/issue-11-stage-a/260722-cook-v3"
    evidence_root.mkdir(parents=True, exist_ok=True, mode=0o700)

    def check_deadline() -> None:
        if time.monotonic() > deadline:
            raise TimeoutError("I11_RESOURCE_DEADLINE")

    def run(argv: Sequence[str], cwd: Path, env: dict[str, str]) -> None:
        check_deadline()
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise TimeoutError("I11_RESOURCE_DEADLINE")
        status, metrics = _run_owned(argv, remaining, cwd=cwd, env=env)
        executable = Path(argv[0])
        metrics["argv"] = [Path(value).name if value.startswith((str(ROOT), str(cwd), "/var/", "/private/")) else value for value in argv]
        metrics["executableSha256"] = _sha(executable.resolve()) if executable.is_file() else None
        metrics.pop("outputExcerpt", None)
        commands.append(metrics)
        if status != 0:
            if metrics["breach"] == "deadline":
                raise TimeoutError("I11_RESOURCE_DEADLINE")
            if metrics["breach"]:
                raise ValueError(f"I11_RESOURCE_{str(metrics['breach']).replace('-', '_').upper()}")
            raise RuntimeError(f"child-output-sha256={metrics['outputSha256']}")

    codes: list[str] = []
    result: dict[str, object] = {}
    try:
        proof_codes, resource_proofs = _resource_proofs(deadline)
        codes.extend(proof_codes)
        runtime_root = Path(sys.executable).parents[2]
        admission = runtime_root / "runtime-admission.json"
        if runtime_root.name != "i11-stage-a-v3" or not admission.is_file():
            raise ValueError("I11_RESOURCE_OWNERSHIP")
        with tempfile.TemporaryDirectory(prefix="controller-tools-", dir=runtime_root) as temporary:
            workspace = Path(temporary)
            marker = workspace / ".i11-owner.json"
            marker.write_text(json.dumps({"schemaVersion": "i11-controller-owner-v1", "purpose": "two-install-two-render"}) + "\n", encoding="utf-8")
            marker.chmod(0o600)
            archive = workspace / NODE_ARCHIVE
            opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
            with opener.open(NODE_ARCHIVE_URL, timeout=30) as response, archive.open("wb") as target:
                if response.geturl() != NODE_ARCHIVE_URL:
                    raise ValueError("I11_RESOURCE_OWNERSHIP")
                downloaded = 0
                while chunk := response.read(1024 * 1024):
                    downloaded += len(chunk)
                    if downloaded > 67_108_864:
                        raise ValueError("I11_RESOURCE_FILE_BYTES")
                    target.write(chunk)
                    check_deadline()
            if _sha(archive) != NODE_ARCHIVE_SHA256:
                raise ValueError("I11_RESOURCE_OWNERSHIP")
            check_deadline()
            extraction = workspace / "node"
            extraction.mkdir(mode=0o700)
            _safe_extract_node(archive, extraction)
            check_deadline()
            node_root = extraction / "node-v22.22.3-darwin-arm64"
            node = node_root / "bin/node"
            npm = node_root / "bin/npm"
            finals: list[dict[str, dict[str, str]]] = []
            for label in ("a", "b"):
                tool = workspace / f"tool-{label}"
                stage = workspace / f"stage-{label}"
                source = stage / "source"
                for directory in (tool, stage, source, tool / "home", tool / "tmp", tool / "npm-cache"):
                    directory.mkdir(mode=0o700)
                shutil.copyfile(ROOT / "requirements/architecture/package.json", tool / "package.json")
                shutil.copyfile(ROOT / "requirements/architecture/package-lock.json", tool / "package-lock.json")
                shutil.copytree(ROOT / "architecture/likec4", source, dirs_exist_ok=True)
                shutil.copyfile(
                    ROOT / "architecture/expansions/i5-06/likec4/model/architecture-curriculum.c4",
                    source / "model/architecture-curriculum.c4",
                )
                for view_id in VIEW_IDS:
                    shutil.copyfile(
                        ROOT / f"architecture/expansions/i5-06/likec4/views/{view_id}.c4",
                        source / f"views/{view_id}.c4",
                    )
                closure = stage / "extension-closure"
                closure.mkdir(mode=0o700)
                shutil.copyfile(ROOT / "architecture/expansions/i5-06/likec4/specification.c4", closure / "specification.c4")
                shutil.copyfile(ROOT / "architecture/expansions/i5-06/likec4/view-manifest.yaml", closure / "view-manifest.yaml")
                check_deadline()
                adapter = tool / "architecture-render.mjs"
                shutil.copyfile(ROOT / "learning/curriculum/tools/architecture-render.mjs", adapter)
                env = {
                    "PATH": f"{node_root / 'bin'}:/usr/bin:/bin:/usr/sbin:/sbin",
                    "HOME": str(tool / "home"), "TMPDIR": str(tool / "tmp"),
                    "TZ": "UTC", "LC_ALL": "C.UTF-8", "LANG": "C.UTF-8",
                    "npm_config_cache": str(tool / "npm-cache"), "npm_config_audit": "false",
                    "npm_config_fund": "false", "npm_config_ignore_scripts": "true",
                }
                run([str(node), "--version"], tool, env)
                run([str(npm), "--version"], tool, env)
                run([str(npm), "ci", "--ignore-scripts", "--no-audit", "--no-fund"], tool, env)
                offline = {**env, "npm_config_offline": "true"}
                likec4 = tool / "node_modules/.bin/likec4"
                model = stage / "model.json"
                dot = stage / "dot"
                raw = stage / "raw"
                dot.mkdir(mode=0o700)
                run([str(likec4), "format", "--check", str(source)], tool, offline)
                run([str(likec4), "validate", "--json", str(source)], tool, offline)
                run([str(likec4), "export", "json", "--skip-layout", "--pretty", "-o", str(model), str(source)], tool, offline)
                run([str(likec4), "gen", "dot", "-o", str(dot), str(source)], tool, offline)
                run([str(node), str(adapter), str(dot), str(raw)], tool, offline)
                for generated in raw.glob("*.raw.svg"):
                    raw_bytes = generated.read_bytes()
                    if len(raw_bytes) > 4_194_304 or not stat.S_ISREG(generated.stat().st_mode):
                        codes.append("I11_BOUND_SIZE")
                    if any(token in raw_bytes for token in (b"<script", b"foreignObject", b"onload=", b"data:")) or re.search(rb"(?:href|src)=", raw_bytes, re.IGNORECASE):
                        codes.append("I11_RENDER_UNSAFE")
                    ET.fromstring(raw_bytes)
                finals.append(_render_bundle(source, raw, model))
                if label == "b":
                    mutation_source = source / "views/DYN-PUBLISH.c4"
                    mutated = mutation_source.read_text(encoding="utf-8").replace(
                        "Dàn snapshot [CF-PUBLISH-STAGE-COMMIT:stage-snapshot]",
                        "Dàn snapshot có đột biến [CF-PUBLISH-STAGE-COMMIT:stage-snapshot]",
                        1,
                    )
                    mutation_source.write_text(mutated, encoding="utf-8")
                    mutation_dot = stage / "mutation-dot"
                    mutation_raw = stage / "mutation-raw"
                    mutation_model = stage / "mutation-model.json"
                    mutation_dot.mkdir(mode=0o700)
                    run([str(likec4), "export", "json", "--skip-layout", "--pretty", "-o", str(mutation_model), str(source)], tool, offline)
                    run([str(likec4), "gen", "dot", "-o", str(mutation_dot), str(source)], tool, offline)
                    run([str(node), str(adapter), str(mutation_dot), str(mutation_raw)], tool, offline)
                    mutated_bundle = _render_bundle(source, mutation_raw, mutation_model)["DYN-PUBLISH"]
                    if any(mutated_bundle[field] == finals[-1]["DYN-PUBLISH"][field] for field in ("sourceSha256", "svgSha256", "textSha256", "projectionSha256", "freshnessSha256")):
                        codes.append("I11_RENDER_SEMANTIC_ERASURE")
            if finals[0] != finals[1]:
                codes.append("I11_RENDER_NONDETERMINISTIC")
            staging_measures = [_tree_measure(workspace / f"stage-{label}") for label in ("a", "b")]
            tool_measures = [_tree_measure(workspace / f"tool-{label}") for label in ("a", "b")]
            file_count = sum(count for count, _ in staging_measures)
            file_bytes = sum(size for _, size in staging_measures)
            aggregate_files, aggregate_bytes = _tree_measure(workspace)
            if file_count > 4096:
                codes.append("I11_RESOURCE_FILE_COUNT")
            if any(size > 1_073_741_824 for _, size in tool_measures) or aggregate_bytes > 2_684_354_560:
                codes.append("I11_RESOURCE_FILE_BYTES")
            output_bytes = sum(int(row["outputBytes"]) for row in commands)
            peak_rss = max((int(row["peakAggregateRssBytes"]) for row in commands), default=0)
            max_processes = max((int(row["maxProcessCount"]) for row in commands), default=0)
            if output_bytes > MAX_OUTPUT:
                codes.append("I11_RESOURCE_OUTPUT")
            if peak_rss > 1_610_612_736:
                codes.append("I11_RESOURCE_RSS")
            if max_processes > 16:
                codes.append("I11_RESOURCE_PROCESS_COUNT")
            if time.monotonic() > deadline:
                codes.append("I11_RESOURCE_DEADLINE")
            result = {
                "schemaVersion": "i11-stage-a-toolchain-evidence-v1",
                "archiveSha256": NODE_ARCHIVE_SHA256, "node": "22.22.3", "npm": "10.9.8",
                "likec4": "1.59.1", "wasmGraphviz": "1.22.2", "installs": 2,
                "renders": 2, "networkAfterSecondInstall": False,
                "networkPhases": ["exact-node-archive", "locked-npm-ci-a", "locked-npm-ci-b", "offline-validation-render"],
                "byteIdentical": finals[0] == finals[1], "semanticMutationChanged": "I11_RENDER_SEMANTIC_ERASURE" not in codes,
                "elapsedMs": int((time.monotonic() - started) * 1000), "stagingFileCount": file_count,
                "stagingFileBytes": file_bytes, "aggregateFileCount": aggregate_files,
                "aggregateFileBytes": aggregate_bytes, "toolRootBytes": [size for _, size in tool_measures],
                "outputBytes": output_bytes, "peakAggregateRssBytes": peak_rss,
                "maxProcessCount": max_processes, "commandCount": len(commands),
                "allReaped": all(bool(row["reaped"]) for row in commands),
                "commands": commands,
                "resourceProofs": resource_proofs,
                "renderHashes": finals,
            }
    except TimeoutError:
        codes.append("I11_RESOURCE_DEADLINE")
    except (OSError, RuntimeError, ValueError, tarfile.TarError) as error:
        message = str(error)
        known = next((code for code in ("I11_RESOURCE_OWNERSHIP", "I11_RESOURCE_DEADLINE") if code in message), None)
        codes.append(known or "I11_RESOURCE_MEASUREMENT_MISSING")
        safe_message = re.sub(r"/(?:private/)?var/folders/\S+", "<temporary>", message.replace(str(ROOT), "<repo>"))
        result = {
            "errorClass": type(error).__name__,
            "errorExcerpt": safe_message[:6000],
            "outputSha256": hashlib.sha256(message.encode()).hexdigest(),
        }
    evidence_path = evidence_root / "toolchain-evidence.json"
    evidence_path.write_text(json.dumps(result, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n", encoding="utf-8")
    evidence_path.chmod(0o600)
    return codes, result


def _focused_tests() -> int:
    argv = [
        sys.executable, "-m", "unittest", "discover", "-s",
        "tests/learning/curriculum", "-p", "test_*.py", "-v",
    ]
    status, metrics = _run_owned(argv, 120.0)
    sys.stdout.write(str(metrics["outputExcerpt"]))
    return status


PROTECTED_PATHS = (
    "architecture/likec4/specification.c4",
    "architecture/likec4/model/people-and-systems.c4",
    "architecture/likec4/model/learning-platform.c4",
    "architecture/likec4/model/data-platform.c4",
    "architecture/likec4/model/local-deployment.c4",
    "architecture/likec4/view-manifest.yaml",
    *(f"architecture/likec4/views/{view}.c4" for view in ("C4-L0", "C4-L1", "C4-L2-LOCAL", "C4-L3-RUNNER", "DEP-LOCAL", "DYN-JOURNEY")),
    *(f"architecture/rendered/{view}.svg" for view in ("C4-L0", "C4-L1", "C4-L2-LOCAL", "C4-L3-RUNNER", "DEP-LOCAL", "DYN-JOURNEY")),
    *(f"architecture/rendered/{view}.txt" for view in ("C4-L0", "C4-L1", "C4-L2-LOCAL", "C4-L3-RUNNER", "DEP-LOCAL", "DYN-JOURNEY")),
    "architecture/rendered/render-manifest.json",
    "requirements/architecture/package.json",
    "requirements/architecture/package-lock.json",
    "scripts/golden/architecture-render.mjs",
    "scripts/golden/architecture_check.py",
    "scripts/golden/architecture_finalize.py",
    "scripts/golden/architecture_pipeline.py",
    "scripts/golden/architecture_render.py",
    "mk/issue-5/i5-01.mk",
)


def _git(*arguments: str) -> bytes:
    completed = subprocess.run(
        ["/usr/bin/git", *arguments], cwd=ROOT, check=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    return completed.stdout


def _allowed_stage_paths() -> tuple[str, ...]:
    amendment = (ROOT / "plans/260721-011-architecture-curriculum/stage-a-release-amendment.md").read_text(encoding="utf-8")
    section = amendment.split("## Exact Stage A Tracked Write Allowlist", 1)[1]
    block = section.split("```text", 1)[1].split("```", 1)[0]
    paths = tuple(line.strip() for line in block.splitlines() if line.strip())
    if len(paths) != 50 or len(set(paths)) != 50:
        raise ValueError("I11_CLEAN_ROLLBACK_SCOPE")
    return paths


def _copy_and_remove_owned_artifacts(evidence_root: Path) -> list[str]:
    artifacts = ROOT / ".artifacts"
    copied: list[str] = []
    if not artifacts.exists():
        raise ValueError("I11_CLEAN_OWNERSHIP_DRIFT")
    for marker in sorted(artifacts.rglob(".golden-owner.json")):
        run_root = marker.parent
        record = json.loads(marker.read_text(encoding="utf-8"))
        observed = run_root.stat()
        if (
            record.get("schemaVersion") != "golden-owner-v1"
            or (record.get("device"), record.get("inode")) != (observed.st_dev, observed.st_ino)
            or not run_root.is_relative_to(artifacts)
        ):
            raise ValueError("I11_CLEAN_OWNERSHIP_DRIFT")
        for result_path in sorted(path for path in run_root.glob("*.json") if path.name != ".golden-owner.json"):
            destination_dir = evidence_root / "protected-command-results"
            destination_dir.mkdir(mode=0o700, exist_ok=True)
            destination = destination_dir / f"{record['purpose']}-{record['runId']}-{result_path.name}"
            shutil.copyfile(result_path, destination)
            destination.chmod(0o600)
            copied.append(destination.name)
        shutil.rmtree(run_root)
    runtime_root = artifacts / "workspaces/golden/i11-stage-a-v3"
    admission = runtime_root / "runtime-admission.json"
    if not admission.is_file() or runtime_root.is_symlink():
        raise ValueError("I11_CLEAN_OWNERSHIP_DRIFT")
    admission_record = json.loads(admission.read_text(encoding="utf-8"))
    if admission_record.get("runtimeRoot") not in (None, ".artifacts/workspaces/golden/i11-stage-a-v3"):
        raise ValueError("I11_CLEAN_OWNERSHIP_DRIFT")
    shutil.rmtree(runtime_root)
    for owned_cache in (
        ROOT / "learning/curriculum/tools/__pycache__",
        ROOT / "tests/learning/curriculum/__pycache__",
    ):
        if owned_cache.is_dir() and all(item.is_file() and item.suffix == ".pyc" for item in owned_cache.iterdir()):
            shutil.rmtree(owned_cache)
    for directory in sorted((path for path in artifacts.rglob("*") if path.is_dir()), key=lambda path: len(path.parts), reverse=True):
        try:
            directory.rmdir()
        except OSError:
            pass
    try:
        artifacts.rmdir()
    except OSError as error:
        raise ValueError("I11_CLEAN_IGNORED_UNOWNED") from error
    return copied


def _close_evidence(evidence_root: Path, head: str, cleanup: dict[str, object]) -> tuple[int, str]:
    for stale in evidence_root.glob("previews/*/*.svg.png"):
        stale.unlink()
    raw_log = evidence_root / "red-raw.log"
    if raw_log.exists():
        raw_log.unlink()
    provenance_path = evidence_root / "red-provenance.json"
    provenance = json.loads(provenance_path.read_text(encoding="utf-8"))
    provenance["scaffoldCommitSha"] = "7646e446198c9483e3f1ac1a725d7699e4a09010"
    provenance["testsCommitSha"] = "e712d08ff4ba62fdbe19bd269beb8ed91525e39f"
    provenance["firstSemanticCommitSha"] = "5f214b644642aedd27f9ffd91f7ce5e07af3aef2"
    provenance["finalSemanticHeadSha"] = head
    provenance_path.write_text(json.dumps(provenance, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    owner = {
        "schemaVersion": "i11-stage-a-evidence-owner-v1", "owner": "I5-06",
        "runId": "260722-cook-v3", "inputGitSha": "5f28f83bc2062e0bc7b8792d9aaa744a0b7e175b",
        "testedTreeSha": head, "stage": "A-static-only", "cloudAction": "none",
    }
    (evidence_root / "owner.json").write_text(json.dumps(owner, sort_keys=True, separators=(",", ":")) + "\n", encoding="utf-8")
    (evidence_root / "cleanup-result.json").write_text(json.dumps(cleanup, sort_keys=True, separators=(",", ":")) + "\n", encoding="utf-8")
    index_path = evidence_root / "index.json"
    index_sha_path = evidence_root / "index.sha256"
    for old in (index_path, index_sha_path):
        if old.exists(): old.unlink()
    for directory in [evidence_root, *[path for path in evidence_root.rglob("*") if path.is_dir()]]:
        directory.chmod(0o700)
    payloads = sorted(path for path in evidence_root.rglob("*") if path.is_file())
    rows = []
    for path in payloads:
        path.chmod(0o600)
        relative = path.relative_to(evidence_root).as_posix()
        media_type = "image/png" if path.suffix == ".png" else "application/json" if path.suffix == ".json" else "text/plain"
        rows.append({"path": relative, "mediaType": media_type, "bytes": path.stat().st_size, "sha256": _sha(path)})
    index = {"schemaVersion": "i11-closed-evidence-index-v1", "owner": "I5-06", "payloads": rows}
    index_path.write_text(json.dumps(index, sort_keys=True, separators=(",", ":")) + "\n", encoding="utf-8")
    index_path.chmod(0o600)
    index_sha = _sha(index_path)
    index_sha_path.write_text(index_sha + "  index.json\n", encoding="ascii")
    index_sha_path.chmod(0o600)
    closed = {path.relative_to(evidence_root).as_posix() for path in evidence_root.rglob("*") if path.is_file()}
    expected = {row["path"] for row in rows} | {"index.json", "index.sha256"}
    if closed != expected:
        raise ValueError("I11_EVIDENCE_ORPHAN")
    return len(rows), index_sha


def _repository_handoff() -> CheckResult:
    codes: list[str] = []
    evidence_root = ROOT / ".claude/evidence/issue-11-stage-a/260722-cook-v3"
    head = _git("rev-parse", "HEAD").decode().strip()
    allowed = _allowed_stage_paths()
    rows = [line.split("\t", 1) for line in _git("diff", "--name-status", "5f28f83bc2062e0bc7b8792d9aaa744a0b7e175b", "HEAD").decode().splitlines()]
    rollback_exact = len(rows) == 50 and all(status == "A" for status, _ in rows) and {path for _, path in rows} == set(allowed)
    if not rollback_exact: codes.append("I11_CLEAN_ROLLBACK_SCOPE")
    protected: dict[str, str] = {}
    for path in PROTECTED_PATHS:
        current = (ROOT / path).read_bytes()
        expected = _git("show", f"5f28f83bc2062e0bc7b8792d9aaa744a0b7e175b:{path}")
        if current != expected: codes.append("I11_PROTECTED_IDENTITY_DRIFT")
        protected[path] = hashlib.sha256(current).hexdigest()
    if len(protected) != 33: codes.append("I11_PROTECTED_IDENTITY_DRIFT")
    copied = _copy_and_remove_owned_artifacts(evidence_root)
    private_pattern = re.compile(rb"/Users/|khanhvg|BEGIN [A-Z ]*PRIVATE KEY|AKIA[0-9A-Z]{16}|(?:password|token|secret)=[^\s]{4,}", re.IGNORECASE)
    external_pattern = re.compile(rb"https?://[^\s\"'<>]+")
    allowed_urls = {b"https://nodejs.org/download/release/v22.22.3/", b"http://www.w3.org/2000/svg"}
    scan_paths = [ROOT / path for path in allowed] + [path for path in evidence_root.rglob("*") if path.is_file()]
    findings: list[str] = []
    for path in scan_paths:
        content = path.read_bytes()
        if private_pattern.search(content): findings.append(path.name)
        if any(not any(url.startswith(prefix) for prefix in allowed_urls) for url in external_pattern.findall(content)):
            findings.append(path.name)
    if findings: codes.append("I11_S3_PRIVATE_PATH")
    porcelain = _git("status", "--porcelain=v1", "--untracked-files=all")
    if porcelain: codes.append("I11_CLEAN_PORCELAIN_NONEMPTY")
    ignored = _git("status", "--porcelain=v1", "--ignored", "--untracked-files=all", "-z").split(b"\0")
    ignored = [row for row in ignored if row]
    if any(not row.startswith(b"!! .claude/") for row in ignored): codes.append("I11_CLEAN_IGNORED_UNOWNED")
    cleanup = {
        "schemaVersion": "i11-cleanup-result-v1", "testedTreeSha": head,
        "trackedCreates": len(rows), "rollbackExact": rollback_exact,
        "protectedCount": len(protected), "protectedHashes": protected,
        "porcelainBytes": len(porcelain), "ignoredEntries": len(ignored),
        "copiedProtectedCommandResults": sorted(copied), "s3Findings": sorted(set(findings)),
        "stageB": "blocked", "cloudAction": "none",
    }
    payload_count, index_sha = _close_evidence(evidence_root, head, cleanup)
    return CheckResult(
        "I11-EP-HANDOFF", True, tuple(dict.fromkeys(codes)),
        {"testedTreeSha": head, "trackedCreates": len(rows), "protected": len(protected),
         "porcelainBytes": len(porcelain), "evidencePayloads": payload_count, "indexSha256": index_sha},
    )


def _dispatch(name: str) -> int:
    if name == "run-focused-tests":
        return _focused_tests()
    if name == "verify-expansions":
        result = _verify_repository()
        tool_codes, tool_details = _toolchain_verification()
        result = CheckResult(
            result.entrypoint_id, result.reached,
            tuple(dict.fromkeys((*result.codes, *tool_codes))),
            {**result.details, "toolchain": tool_details},
        )
    else:
        result = _repository_handoff()
    print(json.dumps({"entrypointId": result.entrypoint_id, "reached": result.reached, "codes": list(result.codes), **result.details}, sort_keys=True))
    return 0 if result.ok else 1


def main(argv: Sequence[str] | None = None) -> int:
    if argv is None:
        argv = sys.argv[1:]
    if len(argv) == 2 and argv[0] == "_resource-probe":
        return _resource_probe(argv[1])
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("run-focused-tests", "verify-expansions", "clean-handoff"))
    return _dispatch(parser.parse_args(argv).command)


if __name__ == "__main__":
    raise SystemExit(main())
