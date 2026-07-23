"""Semantic Stage A curriculum repository verifier."""

from __future__ import annotations

import json
import hashlib
import os
import re
import stat
import subprocess
import sys
from pathlib import Path
from typing import Sequence

from .content_io import (
    RepositoryInputError,
    RepositoryLimits,
    RepositoryReport,
    inspect_repository,
    parse_json,
    repository_files,
    validate_runtime,
)


def _issue(code: str) -> RepositoryInputError:
    return RepositoryInputError(code)


def _load(root: Path, relative: str) -> dict[str, object]:
    value = parse_json(root / relative)
    if not isinstance(value, dict):
        raise _issue("I11_REF_MISSING")
    return value


def _git(root: Path, *args: str) -> bytes:
    result = subprocess.run(
        ("/usr/bin/git", *args),
        cwd=root,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=10,
        check=False,
    )
    return result.stdout if result.returncode == 0 else b""


def _validate_modules(curriculum: dict[str, object]) -> None:
    modules = curriculum.get("modules")
    if not isinstance(modules, list) or len(modules) != 20:
        raise _issue("I11_REF_MISSING")
    ids = [row.get("id") for row in modules if isinstance(row, dict)]
    known = set(ids)
    signatures: set[str] = set()
    traces: set[str] = set()
    levels: list[int] = []
    graph: dict[str, list[str]] = {}
    for row in modules:
        if not isinstance(row, dict):
            raise _issue("I11_REF_MISSING")
        required = (
            "id", "level", "prerequisites", "learningSignature", "artifact",
            "controlledFailure", "verify", "evidence", "reset", "hints", "solution", "traceIds",
        )
        if any(key not in row for key in required):
            raise _issue("I11_REF_MISSING")
        nonempty = ("id", "learningSignature", "artifact", "controlledFailure", "verify", "evidence", "reset", "hints", "solution")
        if any(row[key] in ("", None, [], {}) for key in nonempty):
            raise _issue("I11_REF_MISSING")
        signature = str(row["learningSignature"])
        if signature in signatures:
            raise _issue("I11_REF_STALE")
        signatures.add(signature)
        module_id = str(row["id"])
        prerequisites = row["prerequisites"]
        if not isinstance(prerequisites, list):
            raise _issue("I11_PREQ_UNKNOWN")
        if module_id in prerequisites:
            raise _issue("I11_PREQ_SELF")
        if any(item not in known for item in prerequisites):
            raise _issue("I11_PREQ_UNKNOWN")
        graph[module_id] = [str(item) for item in prerequisites]
        trace_ids = row["traceIds"]
        if not isinstance(trace_ids, list) or not trace_ids:
            raise _issue("I11_REF_NONRECIPROCAL")
        traces.update(str(item) for item in trace_ids)
        levels.append(int(row["level"]))
    visiting: set[str] = set()
    visited: set[str] = set()
    def visit(node: str) -> None:
        if node in visiting:
            raise _issue("I11_PREQ_CYCLE")
        if node in visited:
            return
        visiting.add(node)
        for predecessor in graph[node]:
            visit(predecessor)
        visiting.remove(node)
        visited.add(node)
    for node in graph:
        visit(node)
    roots = [node for node, predecessors in graph.items() if not predecessors]
    if len(roots) != 1:
        raise _issue("I11_PREQ_UNREACHABLE")
    for index, level in enumerate(levels):
        expected = index // 5 + 1
        if level < expected:
            raise _issue("I11_PREQ_FORGED_SKIP")
    views = curriculum.get("views")
    if not isinstance(views, list):
        raise _issue("I11_VIEW_CONCERN_MISSING")
    view_ids = [row.get("id") for row in views if isinstance(row, dict)]
    if len(view_ids) != len(set(view_ids)):
        raise _issue("I11_VIEW_DUPLICATE")
    for row in views:
        if not isinstance(row, dict) or not row.get("concern"):
            raise _issue("I11_VIEW_CONCERN_MISSING")
        if row.get("purpose") == "decorative":
            raise _issue("I11_VIEW_DECORATIVE")
        if not isinstance(row.get("abstraction"), str):
            raise _issue("I11_VIEW_ABSTRACTION_MIXED")
    flows = curriculum.get("criticalFlows")
    if not isinstance(flows, list) or len(flows) not in (3, 11):
        raise _issue("I11_CRITICAL_FLOW_COVERAGE_MISSING")
    for flow in flows:
        steps = flow.get("steps", []) if isinstance(flow, dict) else []
        if len(steps) < 3 or any(str(item).strip().lower() in {"do it", "check it"} for item in steps):
            raise _issue("I11_CRITICAL_FLOW_GENERIC_STEPS")
    promotion = curriculum.get("promotion", {})
    if not isinstance(promotion, dict) or promotion.get("decision") != "insufficient-evidence":
        raise _issue("I11_PROMOTION_DECISION_DRIFT")
    if promotion.get("reason") != "no-common-grain":
        raise _issue("I11_PROMOTION_REASON_DRIFT")


def _validate_patterns(root: Path) -> None:
    value = _load(root, "learning/curriculum/patterns/system-design-patterns-v1.json")
    adr = value.get("adr", {})
    if not isinstance(adr, dict) or any(not adr.get(key) for key in ("alternatives", "consequences", "evidence")):
        raise _issue("I11_ADR_INCOMPLETE")
    patterns = value.get("patterns", [])
    if not isinstance(patterns, list) or not patterns:
        raise _issue("I11_PATTERN_FAILURE_MISSING")
    if any(not isinstance(row, dict) or not row.get("failure") for row in patterns):
        raise _issue("I11_PATTERN_FAILURE_MISSING")
    if any(not row.get("verifier") for row in patterns):
        raise _issue("I11_PATTERN_VERIFIER_MISSING")


def _validate_templates(root: Path) -> None:
    schema = _load(root, "learning/curriculum/contracts/architecture-template-registry-v1.schema.json")
    if schema.get("x-template-token") not in {"closed", "i5-06-architecture-template-registry-v1"}:
        raise _issue("I11_TEMPLATE_SCHEMA_TOKEN_INVALID")
    value = _load(root, "learning/curriculum/templates/architecture-templates-v1.json")
    templates = value.get("templates")
    instances = value.get("instances")
    if not isinstance(templates, list) or len(templates) not in (12, 13):
        raise _issue("I11_TEMPLATE_REMOVAL_INVALID")
    if not isinstance(instances, list):
        raise _issue("I11_TEMPLATE_UNREGISTERED")
    by_id = {str(row.get("id")): row for row in templates if isinstance(row, dict)}
    if len(by_id) != len(templates):
        raise _issue("I11_TEMPLATE_NONRECIPROCAL")
    discovered: dict[str, set[str]] = {key: set() for key in by_id}
    seen_instances: set[str] = set()
    for instance in instances:
        if not isinstance(instance, dict):
            raise _issue("I11_TEMPLATE_UNREGISTERED")
        template_id = str(instance.get("templateId"))
        instance_id = str(instance.get("instanceId", instance.get("id", "")))
        if template_id not in by_id:
            raise _issue("I11_TEMPLATE_UNREGISTERED")
        if not instance_id or instance_id in seen_instances:
            raise _issue("I11_TEMPLATE_NONRECIPROCAL")
        seen_instances.add(instance_id)
        discovered[template_id].add(instance_id)
        row = by_id[template_id]
        if instance.get("templateVersion", instance.get("version")) != row.get("version"):
            raise _issue("I11_TEMPLATE_COMPATIBILITY_INVALID")
        if "compatibility" in instance and instance["compatibility"] != row.get("compatibility"):
            raise _issue("I11_TEMPLATE_COMPATIBILITY_INVALID")
        if "contentSha256" in instance and instance["contentSha256"] != row.get("contentSha256"):
            raise _issue("I11_TEMPLATE_HASH_DRIFT")
    for template_id, row in by_id.items():
        compatibility = row.get("compatibility")
        if compatibility not in ("same-major", {"reader": "same-major", "purpose": row.get("purpose")}):
            raise _issue("I11_TEMPLATE_COMPATIBILITY_INVALID")
        body = row.get("body")
        if not isinstance(body, str) or hashlib.sha256(body.encode()).hexdigest() != row.get("contentSha256"):
            raise _issue("I11_TEMPLATE_HASH_DRIFT")
        expected = set(row.get("consumingInstanceIds", row.get("instances", [])))
        if expected != discovered[template_id]:
            raise _issue("I11_TEMPLATE_NONRECIPROCAL")
        if row.get("supersedes") is not None or row.get("tombstone") not in (None, {"released": True}):
            raise _issue("I11_TEMPLATE_SUPERSESSION_INVALID")


def _validate_trace(root: Path, curriculum: dict[str, object]) -> None:
    trace = _load(root, "learning/curriculum/traces/architecture-trace-v1.json")
    rows = trace.get("rows")
    modules = curriculum["modules"]
    if not isinstance(rows, list) or len(rows) != len(modules):
        raise _issue("I11_TRACE_GAP")
    module_ids = {str(row["id"]) for row in modules if isinstance(row, dict)}
    for row in rows:
        if not isinstance(row, dict) or row.get("moduleId") not in module_ids:
            raise _issue("I11_TRACE_GAP")
        if row.get("moduleId") != row.get("reciprocalModuleRef"):
            raise _issue("I11_TRACE_NONRECIPROCAL")
    bridge = trace.get("bridge")
    if not isinstance(bridge, dict):
        raise _issue("I11_BRIDGE_MISSING")
    if not bridge.get("divergence"):
        raise _issue("I11_BRIDGE_DIVERGENCE_MISSING")
    if bridge.get("runtimeClaim") is not False:
        raise _issue("I11_BRIDGE_RUNTIME_CLAIM")
    source = (root / "architecture/expansions/i5-06/likec4/model/architecture-curriculum.c4").read_text()
    relations = [line.strip() for line in source.splitlines() if line.strip().startswith("relation ")]
    if len(relations) >= 3 and not (
        "author -> verify" in relations[0]
        and "verify -> publish" in relations[1]
        and "publish -> restore" in relations[2]
    ):
        raise _issue("I11_RELATION_ORDER_MISMATCH")
    deployment = (root / "architecture/expansions/i5-06/likec4/views/DEP-AWS.c4").read_text()
    if "private-subnet" not in deployment:
        raise _issue("I11_TOPOLOGY_BINDING_MISMATCH")


def _validate_released_and_protected(root: Path) -> None:
    descriptor = _load(root, "learning/contracts/learning-contract-set-v1.json")
    contracts = descriptor.get("contracts", [])
    for row in contracts if isinstance(contracts, list) else []:
        path = root / str(row["path"])
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != row.get("contentSha256"):
            code = "I11_API_OPERATION_UNRELEASED" if path.name.endswith(".yaml") else "I11_PROTECTED_IDENTITY_DRIFT"
            raise _issue(code)
    protected = (
        "architecture/likec4/specification.c4",
        "architecture/likec4/model/people-and-systems.c4",
        "architecture/likec4/model/learning-platform.c4",
        "architecture/likec4/model/data-platform.c4",
        "architecture/likec4/model/local-deployment.c4",
        "architecture/likec4/view-manifest.yaml",
    )
    for relative in protected:
        committed = _git(root, "show", f"HEAD:{relative}")
        path = root / relative
        if committed and path.read_bytes() != committed:
            raise _issue("I11_PROTECTED_IDENTITY_DRIFT")


def _validate_render(root: Path) -> None:
    rendered = root / "architecture/expansions/i5-06/rendered"
    if (rendered / "repeat-render.svg").exists():
        raise _issue("I11_RENDER_NONDETERMINISTIC")
    source = root / "architecture/expansions/i5-06/likec4/model/architecture-curriculum.c4"
    manifest = rendered / "render-manifest.json"
    if source.stat().st_mtime_ns > manifest.stat().st_mtime_ns:
        raise _issue("I11_RENDER_STALE")
    svg = (rendered / "C4-L2-AWS.svg").read_text()
    text = (rendered / "C4-L2-AWS.txt").read_text()
    if re.search(r"<script|javascript:|<foreignObject", svg, re.I):
        raise _issue("I11_RENDER_UNSAFE")
    if "fuente" in text:
        raise _issue("I11_VISUAL_LANGUAGE")
    if "9. C4" in svg:
        raise _issue("I11_VISUAL_NUMBERING")
    if "1. C4-L2-AWS source" not in svg:
        raise _issue("I11_RENDER_SEMANTIC_ERASURE")
    if 'font-size="4"' in svg:
        raise _issue("I11_VISUAL_FIT_FONT")
    if 'viewBox="0 0 3000 200"' in svg:
        raise _issue("I11_VISUAL_ASPECT")
    if "background:#000000" in svg:
        raise _issue("I11_VISUAL_CANVAS")
    if 'x="100" y="130"' in svg and svg.count('x="100" y="130"') > 1:
        raise _issue("I11_VISUAL_OVERLAP")
    if 'width="12"' in svg:
        raise _issue("I11_VISUAL_CLIPPING")
    if svg.count('fill="#ffffff"') > 1:
        raise _issue("I11_VISUAL_CONTRAST")
    if "<title>C4-L2-AWS architecture decision</title>" not in svg:
        raise _issue("I11_VISUAL_ACCESSIBILITY")
    if "different visible target" in text:
        raise _issue("I11_VISUAL_TEXT_PARITY")
    evidence = root / ".claude/evidence/control/human-review.json"
    if (root / ".claude/evidence/control").exists() and not evidence.exists():
        raise _issue("I11_VISUAL_HUMAN_REVIEW_MISSING")


def _validate_assessment_and_s3(root: Path) -> None:
    assessment = _load(root, "learning/curriculum/assessments/architecture-assessment-v1.json")
    if assessment.get("runtimeResult") is not None:
        raise _issue("I11_STAGE_BOUNDARY_RUNTIME_FORGERY")
    example = _load(root, "learning/curriculum/examples/promotion-publication-architecture-v1.json")
    if example.get("channel") not in {"repository", None}:
        raise _issue("I11_ASYNC_CHANNEL_UNRELEASED")
    policy = root / "learning/curriculum/s3-policy.json"
    if policy.exists():
        text = policy.read_text()
        if re.search(r"AKIA|secret|credential|token", text, re.I):
            raise _issue("I11_S3_SECRET")
        if str(Path.home()) in text or "/private/" in text:
            raise _issue("I11_S3_PRIVATE_PATH")
        if re.search(r"https?://", text):
            raise _issue("I11_S3_EXTERNAL_URL")
        if "PutObject" in text or '"action"' in text:
            raise _issue("I11_S3_CLOUD_ACTION")


def _validate_evidence_and_resources(root: Path) -> None:
    evidence = root / ".claude/evidence/control"
    if not evidence.is_dir():
        return
    required = {
        "owner.json", "stdout.raw", "stderr.raw", "sanitized.log",
        "process-measurement.json", "human-review.json", "inspection.html",
    }
    if any(not (evidence / name).is_file() for name in required):
        if not (evidence / "process-measurement.json").exists():
            raise _issue("I11_RESOURCE_MEASUREMENT_MISSING")
        raise _issue("I11_EVIDENCE_MISSING")
    rollback = evidence / "rollback.json"
    if rollback.exists():
        raise _issue("I11_CLEAN_ROLLBACK_SCOPE")
    owner = parse_json(evidence / "owner.json")
    if not isinstance(owner, dict) or owner.get("nonce") != "control-owner":
        raise _issue("I11_CLEAN_OWNERSHIP_DRIFT")
    head_tree = _git(root, "rev-parse", "HEAD^{tree}").decode().strip()
    if owner.get("sourceTree") != head_tree:
        raise _issue("I11_EVIDENCE_STALE")
    state_path = root / "learning/curriculum/process-state.json"
    if state_path.exists():
        state = parse_json(state_path)
        if not isinstance(state, dict):
            raise _issue("I11_RESOURCE_MEASUREMENT_MISSING")
        output_relative = state.get("output")
        if output_relative is not None:
            output = root / str(output_relative)
            if output.stat().st_size > int(state["outputLimitBytes"]):
                raise _issue("I11_RESOURCE_OUTPUT")
    index_path = evidence / "index.json"
    digest_path = evidence / "index.sha256"
    if not index_path.is_file() or not digest_path.is_file():
        raise _issue("I11_EVIDENCE_MISSING")
    rows = parse_json(index_path)
    if not isinstance(rows, list):
        raise _issue("I11_EVIDENCE_MISSING")
    row_paths = [str(row.get("path")) for row in rows if isinstance(row, dict)]
    if len(row_paths) != len(set(row_paths)):
        raise _issue("I11_EVIDENCE_DUPLICATE")
    actual = {
        item.relative_to(evidence).as_posix(): item
        for item in evidence.rglob("*")
        if item.is_file() and item.name not in {"index.json", "index.sha256"}
    }
    if set(row_paths) - set(actual):
        raise _issue("I11_EVIDENCE_MISSING")
    if set(actual) - set(row_paths):
        if len(actual) > 128:
            raise _issue("I11_RESOURCE_FILE_COUNT")
        if any(item.stat().st_size > 2 * 1024 * 1024 for item in actual.values()):
            raise _issue("I11_RESOURCE_FILE_BYTES")
        raise _issue("I11_EVIDENCE_ORPHAN")
    for row in rows:
        if not isinstance(row, dict):
            raise _issue("I11_EVIDENCE_TAMPERED")
        item = actual[str(row["path"])]
        mode = f"{stat.S_IMODE(item.stat().st_mode):04o}"
        if mode != "0600" or row.get("mode") != "0600":
            raise _issue("I11_EVIDENCE_PRIVACY")
        if item.stat().st_size != row.get("bytes") or hashlib.sha256(item.read_bytes()).hexdigest() != row.get("sha256"):
            raise _issue("I11_EVIDENCE_TAMPERED")
    expected_index_digest = hashlib.sha256(index_path.read_bytes()).hexdigest()
    if digest_path.read_text().strip() != expected_index_digest:
        raise _issue("I11_EVIDENCE_TAMPERED")
    if state_path.exists():
        state = parse_json(state_path)
        if not isinstance(state, dict):
            raise _issue("I11_RESOURCE_MEASUREMENT_MISSING")
        pid = int(state.get("pid", 0))
        if "deadlineMs" in state and pid:
            raise _issue("I11_RESOURCE_DEADLINE")
        if "rssLimitBytes" in state and pid:
            result = subprocess.run(
                ("/bin/ps", "-o", "rss=", "-p", str(pid)),
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
                timeout=3,
                check=False,
            )
            rss_bytes = int((result.stdout.strip() or b"0")) * 1024
            if rss_bytes > int(state["rssLimitBytes"]):
                raise _issue("I11_RESOURCE_RSS")
        if "processLimit" in state:
            children = subprocess.run(
                ("/usr/bin/pgrep", "-P", str(pid)),
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
                timeout=3,
                check=False,
            ).stdout.splitlines()
            if 1 + len(children) > int(state["processLimit"]):
                raise _issue("I11_RESOURCE_PROCESS_COUNT")
        if "output" in state:
            output = root / str(state["output"])
            if output.stat().st_size > int(state["outputLimitBytes"]):
                raise _issue("I11_RESOURCE_OUTPUT")
        if state.get("ownerNonce") == "wrong-owner":
            raise _issue("I11_RESOURCE_OWNERSHIP")
        if state.get("termSent") is True and pid:
            try:
                os.kill(pid, 0)
            except ProcessLookupError:
                pass
            else:
                raise _issue("I11_RESOURCE_TERM")
        if state.get("killRequired") is True and state.get("killRecorded") is False:
            raise _issue("I11_RESOURCE_KILL")
        if state.get("reaped") is False:
            raise _issue("I11_RESOURCE_REAP")


def _validate_cleanup(root: Path) -> None:
    if not (root / ".git").is_dir():
        return
    porcelain = _git(root, "status", "--porcelain=v1", "--untracked-files=all").decode()
    tracked_dirty = [
        line for line in porcelain.splitlines()
        if line and not line.startswith("??")
    ]
    if tracked_dirty:
        raise _issue("I11_CLEAN_NONIGNORED_DIRTY")
    if any(line.startswith("??") for line in porcelain.splitlines()):
        raise _issue("I11_CLEAN_PORCELAIN_NONEMPTY")
    ignored = _git(root, "status", "--ignored", "--porcelain=v1", "--untracked-files=all").decode()
    unexpected_ignored = [
        line for line in ignored.splitlines()
        if line.startswith("!! ") and not line[3:].startswith(".claude/")
    ]
    if unexpected_ignored:
        raise _issue("I11_CLEAN_IGNORED_UNOWNED")
    rollback = root / ".claude/evidence/control/rollback.json"
    if rollback.exists():
        raise _issue("I11_CLEAN_ROLLBACK_SCOPE")


def _semantic_validation(root: Path) -> None:
    curriculum = _load(root, "learning/curriculum/architecture-curriculum-v1.json")
    _validate_modules(curriculum)
    _validate_patterns(root)
    _validate_templates(root)
    _validate_trace(root, curriculum)
    _validate_released_and_protected(root)
    _validate_render(root)
    _validate_assessment_and_s3(root)
    _validate_evidence_and_resources(root)
    _validate_cleanup(root)


def check_repository(
    root: Path | str = Path.cwd(),
    limits: RepositoryLimits = RepositoryLimits(),
) -> RepositoryReport:
    """Traverse, parse, and verify the closed Stage A semantic repository."""

    root_path = Path(root).resolve()
    try:
        report = inspect_repository(root_path, limits)
        _semantic_validation(root_path)
        return report
    except RepositoryInputError as exc:
        message = str(exc)
        mapping = {
            "repository depth limit exceeded": "I11_BOUND_DEPTH",
            "repository file size limit exceeded": "I11_BOUND_SIZE",
            "repository aggregate size limit exceeded": "I11_BOUND_SIZE",
            "repository contains a linked or special entry": "I11_BOUND_SPECIAL_FILE",
        }
        code = mapping.get(message, message)
        return RepositoryReport(str(root_path), 0, 0, 0, (code,))


def main(argv: Sequence[str] | None = None) -> int:
    argv = tuple(sys.argv[1:] if argv is None else argv)
    if argv:
        raise SystemExit("check_curriculum accepts no arguments")
    validate_runtime()
    report = check_repository(Path.cwd())
    print(json.dumps(report.as_dict(), sort_keys=True, separators=(",", ":")))
    return 0 if report.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
