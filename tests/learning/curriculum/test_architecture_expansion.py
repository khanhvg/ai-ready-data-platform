from __future__ import annotations

import base64
import hashlib
import json
import os
import shutil
import signal
import stat
import subprocess
import sys
import tempfile
import time
import unittest
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable

from learning.curriculum.tools.architecture_expansion import (
    _repository_handoff,
    _toolchain_verification,
)
from learning.curriculum.tools.check_curriculum import check_repository
from learning.curriculum.tools.check_traceability import _verify_repository
from learning.curriculum.tools.content_io import controller_environment


SOURCE_ROOT = Path(__file__).resolve().parents[3]
FIXTURE_PATH = SOURCE_ROOT / "tests/fixtures/learning/curriculum/invalid-cases-v1.json"
CASES = json.loads(FIXTURE_PATH.read_text())["cases"]

SCAFFOLD_PATHS = (
    "mk/issue-5/i5-06.mk",
    "learning/curriculum/tools/__init__.py",
    "learning/curriculum/tools/architecture_expansion.py",
    "learning/curriculum/tools/check_curriculum.py",
    "learning/curriculum/tools/check_traceability.py",
    "learning/curriculum/tools/content_io.py",
    "learning/curriculum/tools/architecture-render.mjs",
)

SEMANTIC_PATHS = (
    "architecture/expansions/i5-06/likec4/model/architecture-curriculum.c4",
    "architecture/expansions/i5-06/likec4/specification.c4",
    "architecture/expansions/i5-06/likec4/view-manifest.yaml",
    "architecture/expansions/i5-06/likec4/views/C4-L2-AWS.c4",
    "architecture/expansions/i5-06/likec4/views/DEP-AWS.c4",
    "architecture/expansions/i5-06/likec4/views/DYN-OFFICE.c4",
    "architecture/expansions/i5-06/likec4/views/DYN-PUBLISH.c4",
    "architecture/expansions/i5-06/likec4/views/DYN-RESTORE.c4",
    "architecture/expansions/i5-06/rendered/C4-L2-AWS.svg",
    "architecture/expansions/i5-06/rendered/C4-L2-AWS.txt",
    "architecture/expansions/i5-06/rendered/DEP-AWS.svg",
    "architecture/expansions/i5-06/rendered/DEP-AWS.txt",
    "architecture/expansions/i5-06/rendered/DYN-OFFICE.svg",
    "architecture/expansions/i5-06/rendered/DYN-OFFICE.txt",
    "architecture/expansions/i5-06/rendered/DYN-PUBLISH.svg",
    "architecture/expansions/i5-06/rendered/DYN-PUBLISH.txt",
    "architecture/expansions/i5-06/rendered/DYN-RESTORE.svg",
    "architecture/expansions/i5-06/rendered/DYN-RESTORE.txt",
    "architecture/expansions/i5-06/rendered/render-manifest.json",
    "learning/curriculum/architecture-curriculum-v1.json",
    "learning/curriculum/command-owner-activation-i5-06-stage-a-v1.json",
    "learning/curriculum/release-binding-i5-06-stage-a-v1.json",
    "learning/curriculum/assessments/architecture-assessment-v1.json",
    "learning/curriculum/contracts/architecture-curriculum-v1.schema.json",
    "learning/curriculum/contracts/architecture-module-collection-v1.schema.json",
    "learning/curriculum/contracts/architecture-release-binding-v1.schema.json",
    "learning/curriculum/contracts/architecture-template-registry-v1.schema.json",
    "learning/curriculum/contracts/architecture-trace-v1.schema.json",
    "learning/curriculum/contracts/architecture-view-extension-v1.schema.json",
    "learning/curriculum/examples/promotion-publication-architecture-v1.json",
    "learning/curriculum/mappings/local-aws-conceptual-v1.json",
    "learning/curriculum/modules/data-v1.json",
    "learning/curriculum/modules/foundation-v1.json",
    "learning/curriculum/modules/junior-v1.json",
    "learning/curriculum/modules/mid-v1.json",
    "learning/curriculum/patterns/system-design-patterns-v1.json",
    "learning/curriculum/templates/architecture-templates-v1.json",
    "learning/curriculum/traces/architecture-trace-v1.json",
)

PROTECTED_PATHS = (
    "architecture/likec4/specification.c4",
    "architecture/likec4/model/people-and-systems.c4",
    "architecture/likec4/model/learning-platform.c4",
    "architecture/likec4/model/data-platform.c4",
    "architecture/likec4/model/local-deployment.c4",
    "architecture/likec4/view-manifest.yaml",
    "architecture/likec4/views/C4-L0.c4",
    "architecture/likec4/views/C4-L1.c4",
    "architecture/likec4/views/C4-L2-LOCAL.c4",
    "architecture/likec4/views/C4-L3-RUNNER.c4",
    "architecture/likec4/views/DEP-LOCAL.c4",
    "architecture/likec4/views/DYN-JOURNEY.c4",
    "architecture/rendered/C4-L0.svg",
    "architecture/rendered/C4-L1.svg",
    "architecture/rendered/C4-L2-LOCAL.svg",
    "architecture/rendered/C4-L3-RUNNER.svg",
    "architecture/rendered/DEP-LOCAL.svg",
    "architecture/rendered/DYN-JOURNEY.svg",
    "architecture/rendered/C4-L0.txt",
    "architecture/rendered/C4-L1.txt",
    "architecture/rendered/C4-L2-LOCAL.txt",
    "architecture/rendered/C4-L3-RUNNER.txt",
    "architecture/rendered/DEP-LOCAL.txt",
    "architecture/rendered/DYN-JOURNEY.txt",
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

ARCHITECTURE_FAMILIES = frozenset({"I11-RED-RENDER-001", "I11-RED-VISUAL-001"})
TRACEABILITY_FAMILIES = frozenset(
    {
        "I11-RED-TRACE-001",
        "I11-RED-READONLY-001",
        "I11-RED-BRIDGE-001",
        "I11-RED-RELATION-ORDER-001",
        "I11-RED-TOPOLOGY-001",
    }
)
HANDOFF_FAMILIES = frozenset({"I11-RED-EVIDENCE-001", "I11-RED-CLEANUP-001"})


def _write_text(path: Path, value: str, mode: int = 0o644) -> None:
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    path.write_text(value)
    path.chmod(mode)


def _write_json(path: Path, value: object, mode: int = 0o644) -> None:
    _write_text(path, json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n", mode)


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text())


def _copy_file(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    shutil.copy2(source, destination)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _runtime_environment() -> dict[str, str]:
    runtime = Path(os.environ["I11_RUNTIME"])
    return controller_environment(runtime, os.environ["I11_RUNTIME_SHA256"])


def _git(root: Path, *arguments: str) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        ("/usr/bin/git", *arguments),
        cwd=root,
        env=_runtime_environment(),
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
        timeout=20,
    )


def _modules() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for index in range(1, 21):
        module_id = f"ARC-{index:02d}"
        rows.append(
            {
                "id": module_id,
                "level": (index - 1) // 5 + 1,
                "prerequisites": [] if index == 1 else [f"ARC-{index - 1:02d}"],
                "learningSignature": f"signature-{index:02d}",
                "artifact": f"artifact-{index:02d}",
                "controlledFailure": f"failure-{index:02d}",
                "verify": f"verify-{index:02d}",
                "evidence": f"evidence-{index:02d}",
                "reset": f"reset-{index:02d}",
                "hints": [f"hint-{index:02d}-1", f"hint-{index:02d}-2"],
                "solution": {"tradeoff": f"tradeoff-{index:02d}"},
                "traceIds": [f"TRACE-{index:02d}"],
            }
        )
    return rows


def _template_registry() -> dict[str, object]:
    template_ids = (
        "tpl-landscape",
        "tpl-context",
        "tpl-container",
        "tpl-component",
        "tpl-deployment",
        "tpl-dynamic",
        "tpl-data-flow",
        "tpl-threat-model",
        "tpl-adr",
        "tpl-pattern",
        "tpl-fitness-function",
        "tpl-runbook",
        "tpl-migration",
    )
    templates = []
    instances = []
    for template_id in template_ids:
        body = f"{template_id}: alternatives consequences evidence"
        instance_id = f"instance-{template_id}"
        templates.append(
            {
                "id": template_id,
                "version": "1.0.0",
                "compatibility": "same-major",
                "body": body,
                "contentSha256": hashlib.sha256(body.encode()).hexdigest(),
                "instances": [instance_id],
                "supersedes": None,
                "tombstone": None,
            }
        )
        instances.append(
            {
                "id": instance_id,
                "templateId": template_id,
                "templateVersion": "1.0.0",
                "migrationEvidence": [],
            }
        )
    return {"schemaVersion": "architecture-template-registry-v1", "templates": templates, "instances": instances}


def _curriculum() -> dict[str, object]:
    return {
        "schemaVersion": "architecture-curriculum-v1",
        "modules": _modules(),
        "views": [
            {"id": "C4-L2-AWS", "concern": "context", "abstraction": "container", "purpose": "decision"},
            {"id": "DEP-AWS", "concern": "deployment", "abstraction": "node", "purpose": "decision"},
            {"id": "DYN-OFFICE", "concern": "office", "abstraction": "interaction", "purpose": "decision"},
            {"id": "DYN-PUBLISH", "concern": "publish", "abstraction": "interaction", "purpose": "decision"},
            {"id": "DYN-RESTORE", "concern": "restore", "abstraction": "interaction", "purpose": "decision"},
        ],
        "criticalFlows": [
            {"id": "office", "steps": ["author decision", "verify relation", "retain evidence"]},
            {"id": "publish", "steps": ["bind source", "render view", "verify publication"]},
            {"id": "restore", "steps": ["select backup", "restore state", "verify rollback"]},
        ],
        "promotion": {"decision": "insufficient-evidence", "reason": "no-common-grain"},
    }


def _trace() -> dict[str, object]:
    return {
        "schemaVersion": "architecture-trace-v1",
        "rows": [
            {
                "id": f"TRACE-{index:02d}",
                "moduleId": f"ARC-{index:02d}",
                "reciprocalModuleRef": f"ARC-{index:02d}",
                "source": "local",
                "target": "aws",
            }
            for index in range(1, 21)
        ],
        "bridge": {
            "id": "BR-GOVERNANCE-01",
            "localRelation": "learning.adapters -> retail",
            "awsRelation": "learning.adapters -> retail",
            "divergence": "managed control plane differs from local process",
            "runtimeClaim": False,
        },
        "relationOrder": ["author", "verify", "publish", "restore"],
        "topology": {"deployment": "private-subnet", "view": "DEP-AWS"},
    }


def _schemas() -> dict[str, object]:
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "urn:architecture:contract",
        "type": "object",
        "additionalProperties": False,
        "properties": {"schemaVersion": {"type": "string"}},
        "required": ["schemaVersion"],
        "x-template-token": "closed",
    }


def _render_svg(view_id: str) -> str:
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" role="img" viewBox="0 0 1200 675" '
        'style="background:#ffffff"><title>'
        f"{view_id} architecture decision"
        f'</title><desc>Numbered accessible architecture view</desc><g id="node-a">'
        f'<rect x="80" y="80" width="360" height="160" fill="#ffffff" stroke="#111111"/>'
        f'<text x="100" y="130" fill="#111111" font-size="18">1. {view_id} source</text></g>'
        f'<g id="node-b"><text x="700" y="420" fill="#111111" font-size="18">2. {view_id} target</text></g></svg>\n'
    )


def _semantic_content(relative: str) -> str:
    path = Path(relative)
    if relative.endswith("architecture-curriculum-v1.json"):
        return json.dumps(_curriculum(), sort_keys=True, separators=(",", ":")) + "\n"
    if relative.endswith("architecture-templates-v1.json"):
        return json.dumps(_template_registry(), sort_keys=True, separators=(",", ":")) + "\n"
    if relative.endswith("architecture-trace-v1.json"):
        return json.dumps(_trace(), sort_keys=True, separators=(",", ":")) + "\n"
    if "/contracts/" in relative and path.suffix == ".json":
        return json.dumps(_schemas(), sort_keys=True, separators=(",", ":")) + "\n"
    if relative.endswith("system-design-patterns-v1.json"):
        return json.dumps(
            {
                "schemaVersion": "system-design-patterns-v1",
                "patterns": [{"id": "pat-01", "failure": "split-brain", "verifier": "compare relations"}],
                "adr": {"alternatives": ["local", "managed"], "consequences": ["cost", "control"], "evidence": ["trace"]},
            },
            sort_keys=True,
            separators=(",", ":"),
        ) + "\n"
    if relative.endswith("architecture-assessment-v1.json"):
        return '{"schemaVersion":"architecture-assessment-v1","stage":"design","runtimeResult":null}\n'
    if relative.endswith("promotion-publication-architecture-v1.json"):
        return '{"schemaVersion":"promotion-publication-architecture-v1","operation":"publish","channel":"repository"}\n'
    if relative.endswith("local-aws-conceptual-v1.json"):
        return '{"schemaVersion":"local-aws-conceptual-v1","relations":["learning.adapters -> retail"],"topology":"private-subnet"}\n'
    if path.suffix == ".json":
        return json.dumps(
            {"schemaVersion": path.stem, "modules": [row["id"] for row in _modules()]},
            sort_keys=True,
            separators=(",", ":"),
        ) + "\n"
    if path.suffix == ".svg":
        return _render_svg(path.stem)
    if path.suffix == ".txt":
        return f"1. {path.stem} source\n2. {path.stem} target\n"
    if path.name == "render-manifest.json":
        return '{"schemaVersion":"render-manifest-v1","views":[]}\n'
    if path.suffix == ".yaml":
        return "schemaVersion: architecture-view-manifest-v1\nviews: [C4-L2-AWS, DEP-AWS, DYN-OFFICE, DYN-PUBLISH, DYN-RESTORE]\n"
    return (
        "specification architecture-curriculum\n"
        "relation author -> verify label \"decision\" technology \"repository\"\n"
        "relation verify -> publish label \"evidence\" technology \"locked-tool\"\n"
        "relation publish -> restore label \"rollback\" technology \"repository\"\n"
        "deployment private-subnet binds DEP-AWS\n"
    )


def _refresh_render_manifest(root: Path) -> None:
    rendered = root / "architecture/expansions/i5-06/rendered"
    rows = []
    for item in sorted(rendered.iterdir()):
        if item.name == "render-manifest.json":
            continue
        rows.append({"path": item.name, "sha256": _sha256(item), "bytes": item.stat().st_size})
    _write_json(rendered / "render-manifest.json", {"schemaVersion": "render-manifest-v1", "artifacts": rows})


def _refresh_evidence_index(root: Path) -> None:
    evidence = root / ".claude/evidence/control"
    rows = []
    for item in sorted(evidence.iterdir()):
        if item.name in {"index.json", "index.sha256"}:
            continue
        rows.append(
            {
                "path": item.name,
                "bytes": item.stat().st_size,
                "mode": f"{stat.S_IMODE(item.stat().st_mode):04o}",
                "type": "regular",
                "sha256": _sha256(item),
            }
        )
    payload = json.dumps(rows, sort_keys=True, separators=(",", ":")) + "\n"
    _write_text(evidence / "index.json", payload, 0o600)
    _write_text(evidence / "index.sha256", hashlib.sha256(payload.encode()).hexdigest() + "\n", 0o600)


def build_repository(tmp_path: Path) -> Path:
    root = tmp_path / "repository"
    root.mkdir(mode=0o700)
    for relative in SCAFFOLD_PATHS:
        _copy_file(SOURCE_ROOT / relative, root / relative)
    for relative in PROTECTED_PATHS:
        _copy_file(SOURCE_ROOT / relative, root / relative)
    descriptor_path = SOURCE_ROOT / "learning/contracts/learning-contract-set-v1.json"
    descriptor = json.loads(descriptor_path.read_text())
    _copy_file(descriptor_path, root / "learning/contracts/learning-contract-set-v1.json")
    for row in descriptor["contracts"]:
        _copy_file(SOURCE_ROOT / row["path"], root / row["path"])
    for relative in SEMANTIC_PATHS:
        _write_text(root / relative, _semantic_content(relative))
    _refresh_render_manifest(root)
    _write_text(root / "Makefile", "include mk/issue-5/i5-06.mk\n")
    _write_text(root / ".gitignore", "/.claude/\n/.ignored/\n")
    evidence = root / ".claude/evidence/control"
    evidence.mkdir(parents=True, mode=0o700)
    _write_json(evidence / "owner.json", {"nonce": "control-owner", "sourceTree": "pending", "privacy": "private"}, 0o600)
    _write_text(evidence / "stdout.raw", "valid control stdout\n", 0o600)
    _write_text(evidence / "stderr.raw", "", 0o600)
    _write_text(evidence / "sanitized.log", "valid control\n", 0o600)
    _write_json(evidence / "process-measurement.json", {"rssBytes": 1024, "processes": 1, "complete": True}, 0o600)
    _write_json(
        evidence / "human-review.json",
        {"reviewClass": "cook-self-inspection", "independent": False, "synthesized": True},
        0o600,
    )
    _write_text(
        evidence / "inspection.html",
        '<!doctype html><html lang="en"><body><h1>1. Architecture view</h1><p>Visible decision evidence</p></body></html>\n',
        0o600,
    )
    _refresh_evidence_index(root)
    _git(root, "init", "-q")
    _git(root, "add", "--all")
    _git(root, "-c", "user.name=Checkpoint Test", "-c", "user.email=checkpoint@example.invalid", "commit", "-qm", "valid control")
    tree = _git(root, "rev-parse", "HEAD^{tree}").stdout.decode().strip()
    owner = _load_json(evidence / "owner.json")
    owner["sourceTree"] = tree
    _write_json(evidence / "owner.json", owner, 0o600)
    _refresh_evidence_index(root)
    return root


@dataclass
class MutationState:
    processes: list[subprocess.Popen[bytes]] = field(default_factory=list)
    streams: list[Any] = field(default_factory=list)

    def close(self) -> None:
        for process in self.processes:
            if process.poll() is None:
                try:
                    os.killpg(process.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
            try:
                process.wait(timeout=3)
            except subprocess.TimeoutExpired:
                pass
        for stream in self.streams:
            stream.close()


def _spawn(root: Path, code: str, state: MutationState, output: Path | None = None) -> subprocess.Popen[bytes]:
    stdout: Any = subprocess.DEVNULL
    if output is not None:
        output.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        stream = output.open("wb")
        state.streams.append(stream)
        stdout = stream
    process = subprocess.Popen(
        (sys.executable, "-c", code),
        cwd=root,
        env=_runtime_environment(),
        stdin=subprocess.DEVNULL,
        stdout=stdout,
        stderr=subprocess.DEVNULL,
        start_new_session=True,
    )
    state.processes.append(process)
    time.sleep(0.08)
    return process


def _mutate_json(path: Path, operation: Callable[[Any], None]) -> None:
    value = _load_json(path)
    operation(value)
    _write_json(path, value, stat.S_IMODE(path.stat().st_mode))


def apply_mutation(root: Path, mutation: dict[str, object]) -> MutationState:
    kind = str(mutation["kind"])
    state = MutationState()
    curriculum = root / "learning/curriculum/architecture-curriculum-v1.json"
    trace = root / "learning/curriculum/traces/architecture-trace-v1.json"
    templates = root / "learning/curriculum/templates/architecture-templates-v1.json"
    patterns = root / "learning/curriculum/patterns/system-design-patterns-v1.json"
    assessment = root / "learning/curriculum/assessments/architecture-assessment-v1.json"
    example = root / "learning/curriculum/examples/promotion-publication-architecture-v1.json"
    evidence = root / ".claude/evidence/control"
    svg = root / "architecture/expansions/i5-06/rendered/C4-L2-AWS.svg"
    text = root / "architecture/expansions/i5-06/rendered/C4-L2-AWS.txt"
    source = root / "architecture/expansions/i5-06/likec4/model/architecture-curriculum.c4"

    if kind == "remove-required-reference":
        _mutate_json(curriculum, lambda value: value["modules"][0].pop("artifact"))
    elif kind == "duplicate-learning-signature":
        _mutate_json(curriculum, lambda value: value["modules"][1].update(learningSignature=value["modules"][0]["learningSignature"]))
    elif kind == "break-lifecycle-reciprocity":
        _mutate_json(curriculum, lambda value: value["modules"][0].update(traceIds=[]))
    elif kind == "unknown-prerequisite":
        _mutate_json(curriculum, lambda value: value["modules"][1].update(prerequisites=["ARC-99"]))
    elif kind == "self-prerequisite":
        _mutate_json(curriculum, lambda value: value["modules"][1].update(prerequisites=["ARC-02"]))
    elif kind == "cyclic-prerequisite":
        _mutate_json(curriculum, lambda value: value["modules"][0].update(prerequisites=["ARC-02"]))
    elif kind == "unreachable-module":
        _mutate_json(curriculum, lambda value: value["modules"][10].update(prerequisites=[]))
    elif kind == "regress-progression-level":
        _mutate_json(curriculum, lambda value: value["modules"][10].update(level=1))
    elif kind == "duplicate-view-id":
        _mutate_json(curriculum, lambda value: value["views"].append(dict(value["views"][0])))
    elif kind == "make-view-decorative":
        _mutate_json(curriculum, lambda value: value["views"][0].update(purpose="decorative"))
    elif kind == "remove-view-concern":
        _mutate_json(curriculum, lambda value: value["views"][0].pop("concern"))
    elif kind == "mix-view-abstractions":
        _mutate_json(curriculum, lambda value: value["views"][0].update(abstraction=["context", "component"]))
    elif kind == "remove-adr-consequences":
        _mutate_json(patterns, lambda value: value["adr"].pop("consequences"))
    elif kind == "remove-pattern-failure":
        _mutate_json(patterns, lambda value: value["patterns"][0].pop("failure"))
    elif kind == "remove-pattern-verifier":
        _mutate_json(patterns, lambda value: value["patterns"][0].pop("verifier"))
    elif kind == "remove-trace-row":
        _mutate_json(trace, lambda value: value["rows"].pop())
    elif kind == "break-trace-reciprocity":
        _mutate_json(trace, lambda value: value["rows"][0].update(reciprocalModuleRef="ARC-02"))
    elif kind == "change-source-without-render":
        _write_text(source, source.read_text() + 'relation new -> node label "visible" technology "repository"\n')
    elif kind == "change-repeat-render-bytes":
        _write_text(svg.with_name("repeat-render.svg"), svg.read_text().replace("source", "repeat changed"))
    elif kind == "inject-active-svg-content":
        _write_text(svg, svg.read_text().replace("</svg>", '<script>alert("unsafe")</script></svg>'))
    elif kind == "erase-visible-render-label":
        _write_text(svg, svg.read_text().replace("1. C4-L2-AWS source", ""))
    elif kind == "modify-protected-source":
        protected = root / "architecture/likec4/model/data-platform.c4"
        _write_text(protected, protected.read_text() + "\n// drifted protected relation\n")
    elif kind == "add-unreleased-operation":
        _write_text(root / "contracts/openapi/learning-platform-v1.yaml", (root / "contracts/openapi/learning-platform-v1.yaml").read_text() + "\n  /unreleased-operation: {}\n")
    elif kind == "add-unreleased-channel":
        _mutate_json(example, lambda value: value.update(channel="unreleased-events"))
    elif kind == "write-secret-material":
        _write_json(root / "learning/curriculum/s3-policy.json", {"accessKey": "AKIAEXAMPLEPRIVATE", "secret": "not-for-network"})
    elif kind == "write-private-locator":
        _write_json(root / "learning/curriculum/s3-policy.json", {"path": str(Path.home() / "private/evidence")})
    elif kind == "write-external-url":
        _write_json(root / "learning/curriculum/s3-policy.json", {"url": "https://example.invalid/public-evidence"})
    elif kind == "record-cloud-action-attempt":
        _write_json(root / "learning/curriculum/s3-policy.json", {"action": "PutObject", "executed": False, "blocked": True})
    elif kind == "invalidate-template-schema-token":
        schema = root / "learning/curriculum/contracts/architecture-template-registry-v1.schema.json"
        _mutate_json(schema, lambda value: value.update({"x-template-token": "open"}))
    elif kind == "invalidate-template-compatibility":
        _mutate_json(templates, lambda value: value["templates"][0].update(compatibility="all-versions"))
    elif kind == "add-unregistered-template-instance":
        _mutate_json(templates, lambda value: value["instances"].append({"id": "instance-unknown", "templateId": "tpl-unknown", "templateVersion": "1.0.0"}))
    elif kind == "change-template-without-hash":
        _mutate_json(templates, lambda value: value["templates"][0].update(body="changed visible template body"))
    elif kind == "break-template-reciprocity":
        _mutate_json(templates, lambda value: value["templates"][0].update(instances=[]))
    elif kind == "forge-template-supersession":
        _mutate_json(templates, lambda value: value["templates"][0].update(supersedes="0.9.0", tombstone={"released": False}))
    elif kind == "remove-live-template-rows":
        _mutate_json(templates, lambda value: value["templates"].__delitem__(slice(0, 2)))
    elif kind == "remove-critical-flow":
        _mutate_json(curriculum, lambda value: value["criticalFlows"].pop())
    elif kind == "replace-flow-with-generic-steps":
        _mutate_json(curriculum, lambda value: value["criticalFlows"][0].update(steps=["do it", "check it"]))
    elif kind == "forge-assessment-runtime-result":
        _mutate_json(assessment, lambda value: value.update(runtimeResult={"status": "passed", "evidence": "forged"}))
    elif kind == "create-oversize-file":
        _write_text(root / "learning/curriculum/oversize.json", '{"payload":"' + ("x" * (2 * 1024 * 1024 + 1)) + '"}')
    elif kind == "create-deep-tree":
        deep = root / "learning/curriculum" / Path("/".join(f"d{index}" for index in range(20)))
        _write_text(deep / "record.json", '{"schemaVersion":"deep"}\n')
    elif kind == "write-duplicate-json-key":
        _write_text(curriculum, '{"schemaVersion":"one","schemaVersion":"two"}\n')
    elif kind == "create-special-file":
        os.mkfifo(root / "learning/curriculum/special.fifo", 0o600)
    elif kind == "remove-raw-evidence":
        (evidence / "stdout.raw").unlink()
    elif kind == "duplicate-evidence-index-row":
        _mutate_json(evidence / "index.json", lambda value: value.append(dict(value[0])))
    elif kind == "add-orphan-evidence-file":
        _write_text(evidence / "orphan.raw", "unindexed\n", 0o600)
    elif kind == "stale-evidence-source-tree":
        _mutate_json(evidence / "owner.json", lambda value: value.update(sourceTree="0" * 40))
    elif kind == "tamper-indexed-evidence":
        _write_text(evidence / "stdout.raw", "tampered raw bytes\n", 0o600)
    elif kind == "relax-evidence-mode":
        (evidence / "stdout.raw").chmod(0o644)
    elif kind == "change-promotion-decision":
        _mutate_json(curriculum, lambda value: value["promotion"].update(decision="approved"))
    elif kind == "change-promotion-reason":
        _mutate_json(curriculum, lambda value: value["promotion"].update(reason="runtime-passed"))
    elif kind == "remove-governance-bridge":
        _mutate_json(trace, lambda value: value.pop("bridge"))
    elif kind == "remove-bridge-divergence":
        _mutate_json(trace, lambda value: value["bridge"].pop("divergence"))
    elif kind == "add-bridge-runtime-claim":
        _mutate_json(trace, lambda value: value["bridge"].update(runtimeClaim=True))
    elif kind == "spawn-deadline-process":
        process = _spawn(root, "import time; time.sleep(30)", state)
        _write_json(root / "learning/curriculum/process-state.json", {"pid": process.pid, "deadlineMs": 10})
    elif kind == "spawn-memory-process":
        process = _spawn(root, "import time; payload=bytearray(64*1024*1024); time.sleep(30)", state)
        _write_json(root / "learning/curriculum/process-state.json", {"pid": process.pid, "rssLimitBytes": 1024 * 1024})
    elif kind == "spawn-process-tree":
        process = _spawn(root, "import subprocess,sys,time; subprocess.Popen([sys.executable,'-c','import time; time.sleep(30)']); time.sleep(30)", state)
        _write_json(root / "learning/curriculum/process-state.json", {"pid": process.pid, "processLimit": 1})
    elif kind == "produce-excess-output":
        output = root / ".claude/evidence/control/process.stdout.raw"
        process = _spawn(root, "import sys; sys.stdout.write('x'*(3*1024*1024))", state, output)
        process.wait(timeout=5)
        _write_json(root / "learning/curriculum/process-state.json", {"output": str(output.relative_to(root)), "outputLimitBytes": 1024})
    elif kind == "create-many-files":
        for index in range(130):
            _write_text(root / f".claude/evidence/control/files/{index:03d}.txt", "x", 0o600)
    elif kind == "create-large-output-file":
        _write_text(root / ".claude/evidence/control/large-output.bin", "x" * (3 * 1024 * 1024), 0o600)
    elif kind == "drift-process-owner":
        process = _spawn(root, "import time; time.sleep(30)", state)
        _write_json(root / "learning/curriculum/process-state.json", {"pid": process.pid, "ownerNonce": "wrong-owner"})
    elif kind == "spawn-term-resistant-process":
        process = _spawn(root, "import signal,time; signal.signal(signal.SIGTERM,signal.SIG_IGN); time.sleep(30)", state)
        os.killpg(process.pid, signal.SIGTERM)
        _write_json(root / "learning/curriculum/process-state.json", {"pid": process.pid, "termSent": True})
    elif kind == "spawn-kill-required-process":
        process = _spawn(root, "import signal,time; signal.signal(signal.SIGTERM,signal.SIG_IGN); time.sleep(30)", state)
        _write_json(root / "learning/curriculum/process-state.json", {"pid": process.pid, "killRequired": True, "killRecorded": False})
    elif kind == "leave-unreaped-process":
        process = _spawn(root, "import subprocess,sys,time; subprocess.Popen([sys.executable,'-c','pass']); time.sleep(30)", state)
        _write_json(root / "learning/curriculum/process-state.json", {"pid": process.pid, "reaped": False})
    elif kind == "remove-resource-measurement":
        (evidence / "process-measurement.json").unlink()
    elif kind == "change-visible-language":
        _write_text(text, text.read_text().replace("source", "fuente"))
    elif kind == "change-visible-numbering":
        _write_text(svg, svg.read_text().replace("1. C4", "9. C4"))
    elif kind == "change-visible-font-size":
        _write_text(svg, svg.read_text().replace('font-size="18"', 'font-size="4"', 1))
    elif kind == "change-visible-aspect-ratio":
        _write_text(svg, svg.read_text().replace('viewBox="0 0 1200 675"', 'viewBox="0 0 3000 200"'))
    elif kind == "change-visible-canvas":
        _write_text(svg, svg.read_text().replace("background:#ffffff", "background:#000000"))
    elif kind == "overlap-visible-nodes":
        _write_text(svg, svg.read_text().replace('x="700" y="420"', 'x="100" y="130"'))
    elif kind == "clip-visible-text":
        _write_text(svg, svg.read_text().replace('width="360"', 'width="12"'))
    elif kind == "reduce-visible-contrast":
        _write_text(svg, svg.read_text().replace('fill="#111111"', 'fill="#ffffff"'))
    elif kind == "remove-accessible-title":
        _write_text(svg, svg.read_text().replace("<title>C4-L2-AWS architecture decision</title>", ""))
    elif kind == "change-visible-text-only":
        _write_text(text, text.read_text().replace("target", "different visible target"))
    elif kind == "remove-human-review-record":
        (evidence / "human-review.json").unlink()
    elif kind == "dirty-tracked-file":
        _write_text(root / "learning/curriculum/modules/data-v1.json", (root / "learning/curriculum/modules/data-v1.json").read_text() + " ")
    elif kind == "add-unowned-ignored-file":
        _write_text(root / ".ignored/unowned.bin", "unowned ignored bytes\n", 0o600)
    elif kind == "add-untracked-file":
        _write_text(root / "unexpected.txt", "untracked\n")
    elif kind == "drift-cleanup-owner":
        _mutate_json(evidence / "owner.json", lambda value: value.update(nonce="drifted-owner"))
    elif kind == "expand-rollback-scope":
        _write_json(root / ".claude/evidence/control/rollback.json", {"delete": ["README.md", "contracts"]}, 0o600)
    elif kind == "reorder-source-relations":
        lines = source.read_text().splitlines()
        _write_text(source, "\n".join([lines[0], lines[2], lines[1], *lines[3:]]) + "\n")
    elif kind == "change-deployment-topology":
        deployment = root / "architecture/expansions/i5-06/likec4/views/DEP-AWS.c4"
        _write_text(deployment, deployment.read_text().replace("private-subnet", "public-subnet"))
    else:
        raise AssertionError(f"unhandled mutation kind: {kind}")
    return state


def _callable_for_family(family: str) -> Callable[[Path], object]:
    if family in HANDOFF_FAMILIES:
        return _repository_handoff
    if family in ARCHITECTURE_FAMILIES:
        return _toolchain_verification
    if family in TRACEABILITY_FAMILIES:
        return _verify_repository
    return check_repository


def _run_public(root: Path, family: str) -> tuple[subprocess.CompletedProcess[bytes], subprocess.CompletedProcess[bytes]]:
    runtime = Path(os.environ["I11_RUNTIME"])
    interpreter = runtime / "venv/bin/python"
    if family in HANDOFF_FAMILIES:
        cli_argv = (str(interpreter), "-m", "learning.curriculum.tools.architecture_expansion", "clean-handoff")
        make_target = "traceability-check"
    elif family in ARCHITECTURE_FAMILIES:
        cli_argv = (str(interpreter), "-m", "learning.curriculum.tools.architecture_expansion", "verify-expansions")
        make_target = "curriculum-check"
    elif family in TRACEABILITY_FAMILIES:
        cli_argv = (str(interpreter), "-m", "learning.curriculum.tools.check_traceability")
        make_target = "traceability-check"
    else:
        cli_argv = (str(interpreter), "-m", "learning.curriculum.tools.check_curriculum")
        make_target = "curriculum-check"
    environment = _runtime_environment()
    cli = subprocess.run(
        cli_argv,
        cwd=root,
        env=environment,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=40,
    )
    make = subprocess.run(
        (
            "/usr/bin/make",
            make_target,
            f"LEARNING_RUNTIME_ROOT={runtime}/..",
            f"LEARNING_RUNTIME_CANDIDATE={runtime}",
            f"LEARNING_RUNTIME_INTERPRETER_SHA256={os.environ['I11_RUNTIME_SHA256']}",
        ),
        cwd=root,
        env=environment,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=40,
    )
    return cli, make


def _call(root: Path, family: str) -> str:
    try:
        value = _callable_for_family(family)(root)
    except Exception as exc:
        return f"{type(exc).__name__}:{exc}"
    if hasattr(value, "as_dict"):
        value = value.as_dict()
    return json.dumps(value, sort_keys=True, separators=(",", ":"), default=str)


def _receipt(process: subprocess.CompletedProcess[bytes]) -> dict[str, object]:
    return {
        "returncode": process.returncode,
        "stdoutBase64": base64.b64encode(process.stdout).decode(),
        "stderrBase64": base64.b64encode(process.stderr).decode(),
    }


def _tree_digest(root: Path) -> str:
    digest = hashlib.sha256()
    for item in sorted(root.rglob("*")):
        if ".git" in item.parts or item.is_symlink() or not item.is_file():
            continue
        digest.update(item.relative_to(root).as_posix().encode() + b"\0")
        digest.update(item.read_bytes())
    return digest.hexdigest()


def execute_case(case: dict[str, object], tmp_path: Path) -> None:
    root = build_repository(tmp_path)
    family = str(case["family"])
    expected = str(case["expectedCode"])
    mutation_only = {"family": family, "mutation": dict(case["mutation"])}
    valid_direct = _call(root, family)
    valid_cli, valid_make = _run_public(root, family)
    assert valid_cli.returncode == 0, valid_cli.stderr.decode(errors="replace")
    assert valid_make.returncode == 0, valid_make.stderr.decode(errors="replace")
    assert expected not in valid_direct
    state = apply_mutation(root, mutation_only["mutation"])
    try:
        mutated_direct = _call(root, family)
        mutated_cli, mutated_make = _run_public(root, family)
        receipt = {
            "caseId": case["id"],
            "family": family,
            "expectedCode": expected,
            "fixtureSha256": _sha256(FIXTURE_PATH),
            "validTree": _git(root, "rev-parse", "HEAD^{tree}").stdout.decode().strip(),
            "mutatedTreeSha256": _tree_digest(root),
            "toolSha256": {relative: _sha256(SOURCE_ROOT / relative) for relative in SCAFFOLD_PATHS},
            "valid": {"callable": valid_direct, "cli": _receipt(valid_cli), "make": _receipt(valid_make)},
            "mutation": {
                "descriptor": mutation_only,
                "callable": mutated_direct,
                "cli": _receipt(mutated_cli),
                "make": _receipt(mutated_make),
            },
        }
        print(json.dumps(receipt, sort_keys=True, separators=(",", ":")))
        assert expected in mutated_direct
        assert expected in (mutated_cli.stdout + mutated_cli.stderr).decode(errors="replace")
        assert expected in (mutated_make.stdout + mutated_make.stderr).decode(errors="replace")
        assert mutated_cli.returncode != 0
        assert mutated_make.returncode != 0
    finally:
        state.close()


def install_case_tests(
    test_class: type[unittest.TestCase],
    cases: list[dict[str, object]],
) -> None:
    for case in cases:
        def run_case(self: unittest.TestCase, selected: dict[str, object] = case) -> None:
            with tempfile.TemporaryDirectory(
                prefix="repository-red-",
                dir=os.environ["TMPDIR"],
            ) as temporary:
                execute_case(selected, Path(temporary))

        name = "test_" + str(case["id"]).replace("-", "_")
        setattr(test_class, name, run_case)


class ArchitectureAndVisibleRenderMutations(unittest.TestCase):
    pass


install_case_tests(
    ArchitectureAndVisibleRenderMutations,
    [case for case in CASES if case["family"] in ARCHITECTURE_FAMILIES],
)
