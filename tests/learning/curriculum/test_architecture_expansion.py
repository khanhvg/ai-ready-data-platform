from __future__ import annotations

import base64
import hashlib
import json
import os
import re
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
from learning.curriculum.tools.content_io import (
    RepositoryInputError,
    RepositoryLimits,
    _run_owned_process,
)


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


def _canonical_sha256(value: object) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()


def _evidence_receipt(
    source_head: str,
    source_tree: str,
    argv: list[str],
    returncode: int,
    stdout: bytes,
    stderr: bytes = b"",
) -> dict[str, object]:
    return {
        "argv": argv,
        "returncode": returncode,
        "sourceHead": source_head,
        "sourceTree": source_tree,
        "startedNs": 1,
        "finishedNs": 2,
        "stdoutBase64": base64.b64encode(stdout).decode(),
        "stdoutBytes": len(stdout),
        "stdoutSha256": hashlib.sha256(stdout).hexdigest(),
        "stderrBase64": base64.b64encode(stderr).decode(),
        "stderrBytes": len(stderr),
        "stderrSha256": hashlib.sha256(stderr).hexdigest(),
    }


def _refresh_control_closure(root: Path) -> None:
    evidence = root / ".claude/evidence/control"
    tree = _git(root, "rev-parse", "HEAD^{tree}").stdout.decode().strip() if (root / ".git").exists() else "pending"
    head = _git(root, "rev-parse", "HEAD").stdout.decode().strip() if (root / ".git").exists() else "pending"
    command_argv = (
        ["python", "-m", "learning.curriculum.tools.check_curriculum"],
        ["python", "-m", "learning.curriculum.tools.check_traceability"],
        ["python", "-m", "learning.curriculum.tools.architecture_expansion", "verify-expansions"],
        ["make", "curriculum-check"],
        ["make", "traceability-check"],
        ["python", "-m", "unittest", "discover"],
        ["node", "architecture-render.mjs", "render", "run-1"],
        ["node", "architecture-render.mjs", "render", "run-2"],
        ["python", "protected-identities"],
        ["python", "released-byproducts"],
        ["python", "public-cli"],
        ["make", "public-make"],
        ["python", "resource-processes"],
        ["python", "visible-mutation"],
        ["python", "artifact-smoke", "1440"],
        ["python", "artifact-smoke", "1024"],
    )
    commands = []
    for index, argv in enumerate(command_argv, 1):
        row = _evidence_receipt(head, tree, argv, 0, f"command-{index:02d}:pass\n".encode())
        row["commandId"] = f"command-{index:02d}"
        commands.append(row)
    _write_json(evidence / "commands.raw.json", commands, 0o600)
    _write_json(
        evidence / "commands.sanitized.json",
        [
            {
                "commandId": row["commandId"],
                "rawSha256": _canonical_sha256(row),
                "redacted": True,
                "returncode": 0,
            }
            for row in commands
        ],
        0o600,
    )
    mutations = []
    for case in CASES:
        expected = str(case["expectedCode"])
        receipts = {
            route: _evidence_receipt(
                head,
                tree,
                [route, str(case["id"])],
                1,
                f"{expected}\n".encode(),
            )
            for route in (
                "check_repository",
                "verify_repository",
                "toolchain_verification",
                "repository_handoff",
                "cli",
                "make",
            )
        }
        mutations.append(
            {
                "caseId": case["id"],
                "expectedCode": expected,
                "routeReceipts": receipts,
            }
        )
    _write_json(evidence / "mutations.raw.json", mutations, 0o600)
    _write_json(
        evidence / "mutations.sanitized.json",
        [
            {
                "caseId": row["caseId"],
                "expectedCode": row["expectedCode"],
                "rawSha256": _canonical_sha256(row),
                "redacted": True,
            }
            for row in mutations
        ],
        0o600,
    )
    manifest = _load_json(root / "architecture/expansions/i5-06/rendered/render-manifest.json")
    render_rows = [
        {
            **{
                key: row[key]
                for key in (
                    "viewId",
                    "projectionSha256",
                    "dotSha256",
                    "rawSvgSha256",
                    "svgSha256",
                    "textSha256",
                    "fittedHtmlSha256",
                )
            },
            "renderer": manifest["renderer"],
            "likec4": manifest["toolIdentity"]["likec4"],
            "graphvizPackage": manifest["toolIdentity"]["graphvizPackage"],
            "returncode": 0,
        }
        for row in manifest["views"]
    ]
    _write_json(evidence / "render.raw.json", render_rows, 0o600)
    _write_json(
        evidence / "render.sanitized.json",
        [
            {
                "viewId": row["viewId"],
                "lineageClosed": True,
                "rawSha256": _canonical_sha256(row),
                "redacted": True,
                "renderer": row["renderer"],
                "likec4": row["likec4"],
                "graphvizPackage": row["graphvizPackage"],
                "returncode": 0,
            }
            for row in render_rows
        ],
        0o600,
    )
    descriptor = _load_json(root / "learning/contracts/learning-contract-set-v1.json")
    released = [
        {
            "path": row["path"],
            "sha256": _sha256(root / row["path"]),
            "releasedByproductClosed": True,
        }
        for row in descriptor["contracts"]
    ]
    _write_json(evidence / "released-byproducts.json", released, 0o600)
    payload_paths = sorted(
        item
        for item in evidence.rglob("*")
        if item.is_file() and item.name not in {"closure.json", "index.json", "index.sha256"}
    )
    aggregate = hashlib.sha256()
    for item in payload_paths:
        aggregate.update(item.relative_to(evidence).as_posix().encode() + b"\0")
        aggregate.update(item.read_bytes())
        aggregate.update(b"\0")
    _write_json(
        evidence / "closure.json",
        {
            "schemaVersion": "i11-stage-a-control-closure-v1",
            "sourceHead": head,
            "sourceTree": tree,
            "commands": 16,
            "mutations": 82,
            "renderViews": 5,
            "protectedIdentities": 33,
            "releasedContracts": 21,
            "rawSanitizedPairs": 3,
            "payloadFiles": len(payload_paths),
            "payloadBytes": sum(item.stat().st_size for item in payload_paths),
            "payloadSha256": aggregate.hexdigest(),
            "selectorPublication": "last",
        },
        0o600,
    )


def _refresh_closure_payload_binding(root: Path) -> None:
    evidence = root / ".claude/evidence/control"
    payload_paths = sorted(
        item
        for item in evidence.rglob("*")
        if item.is_file() and item.name not in {"closure.json", "index.json", "index.sha256"}
    )
    aggregate = hashlib.sha256()
    for item in payload_paths:
        aggregate.update(item.relative_to(evidence).as_posix().encode() + b"\0")
        aggregate.update(item.read_bytes())
        aggregate.update(b"\0")
    closure = _load_json(evidence / "closure.json")
    closure.update(
        payloadFiles=len(payload_paths),
        payloadBytes=sum(item.stat().st_size for item in payload_paths),
        payloadSha256=aggregate.hexdigest(),
    )
    _write_json(evidence / "closure.json", closure, 0o600)


def _refresh_selector(root: Path) -> None:
    evidence = root / ".claude/evidence/control"
    tree = _git(root, "rev-parse", "HEAD^{tree}").stdout.decode().strip()
    _write_json(
        root / ".claude/evidence/selected.json",
        {
            "generation": "control",
            "indexSha256": _sha256(evidence / "index.json"),
            "publicationOrder": "selector-last",
            "sourceTree": tree,
        },
        0o600,
    )


def _record_resource_violation(root: Path, measurement: Path, code: str) -> None:
    _mutate_json(measurement, lambda value: value.update(violation=code))
    _refresh_control_closure(root)
    _refresh_evidence_index(root)
    _refresh_selector(root)


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
        _copy_file(SOURCE_ROOT / relative, root / relative)
    _write_text(root / "Makefile", "include mk/issue-5/i5-06.mk\n")
    _write_text(root / ".gitignore", "/.claude/\n/.ignored/\n")
    evidence = root / ".claude/evidence/control"
    evidence.mkdir(parents=True, mode=0o700)
    _write_json(evidence / "owner.json", {"nonce": "control-owner", "sourceTree": "pending", "privacy": "private"}, 0o600)
    _write_text(evidence / "stdout.raw", "valid control stdout\n", 0o600)
    _write_text(evidence / "stderr.raw", "", 0o600)
    _write_text(evidence / "sanitized.log", "valid control\n", 0o600)
    _write_json(
        evidence / "process-measurement.json",
        {
            "aggregateRssSampled": True,
            "processGroupSampled": True,
            "createdFilesSampled": True,
            "outputSampled": True,
            "deadlineEnforced": True,
            "termGraceSeconds": 5,
            "waited": True,
            "descendantsAfterReap": 0,
        },
        0o600,
    )
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
    _refresh_control_closure(root)
    _refresh_evidence_index(root)
    _git(root, "init", "-q")
    _git(root, "add", "--all")
    _git(root, "-c", "user.name=Checkpoint Test", "-c", "user.email=checkpoint@example.invalid", "commit", "-qm", "valid control")
    tree = _git(root, "rev-parse", "HEAD^{tree}").stdout.decode().strip()
    owner = _load_json(evidence / "owner.json")
    owner["sourceTree"] = tree
    owner["sourceHead"] = _git(root, "rev-parse", "HEAD").stdout.decode().strip()
    _write_json(evidence / "owner.json", owner, 0o600)
    _refresh_control_closure(root)
    _refresh_evidence_index(root)
    _refresh_selector(root)
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
    measurement = evidence / "process-measurement.json"
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
        _mutate_json(curriculum, lambda value: value["modules"][1].update(prerequisites=["F02"]))
    elif kind == "cyclic-prerequisite":
        _mutate_json(curriculum, lambda value: value["modules"][0].update(prerequisites=["F02"]))
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
        _mutate_json(trace, lambda value: value["rows"][0].update(reciprocalModuleRef="F02"))
    elif kind == "change-source-without-render":
        _write_text(source, source.read_text() + 'relation new -> node label "visible" technology "repository"\n')
    elif kind == "change-repeat-render-bytes":
        _write_text(svg.with_name("repeat-render.svg"), svg.read_text().replace("source", "repeat changed"))
    elif kind == "inject-active-svg-content":
        _write_text(svg, svg.read_text().replace("</svg>", '<script>alert("unsafe")</script></svg>'))
    elif kind == "erase-visible-render-label":
        _write_text(svg, svg.read_text().replace("</svg>", "<!-- semantic drift --></svg>"))
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
        _mutate_json(templates, lambda value: value["templates"][0].update(consumingInstanceIds=[]))
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
        _record_resource_violation(root, measurement, "I11_RESOURCE_DEADLINE")
    elif kind == "spawn-memory-process":
        _record_resource_violation(root, measurement, "I11_RESOURCE_RSS")
    elif kind == "spawn-process-tree":
        _record_resource_violation(root, measurement, "I11_RESOURCE_PROCESS_COUNT")
    elif kind == "produce-excess-output":
        _record_resource_violation(root, measurement, "I11_RESOURCE_OUTPUT")
    elif kind == "create-many-files":
        _record_resource_violation(root, measurement, "I11_RESOURCE_FILE_COUNT")
    elif kind == "create-large-output-file":
        _record_resource_violation(root, measurement, "I11_RESOURCE_FILE_BYTES")
    elif kind == "drift-process-owner":
        _record_resource_violation(root, measurement, "I11_RESOURCE_OWNERSHIP")
    elif kind == "spawn-term-resistant-process":
        _record_resource_violation(root, measurement, "I11_RESOURCE_TERM")
    elif kind == "spawn-kill-required-process":
        _record_resource_violation(root, measurement, "I11_RESOURCE_KILL")
    elif kind == "leave-unreaped-process":
        _record_resource_violation(root, measurement, "I11_RESOURCE_REAP")
    elif kind == "remove-resource-measurement":
        (evidence / "process-measurement.json").unlink()
    elif kind == "change-visible-language":
        _write_text(text, "fuente\n" + text.read_text())
    elif kind == "change-visible-numbering":
        _write_text(svg, svg.read_text().replace("</svg>", "<!-- 9. C4 --></svg>"))
    elif kind == "change-visible-font-size":
        _write_text(svg, re.sub(r'font-size="[0-9.]+"', 'font-size="4"', svg.read_text(), count=1))
    elif kind == "change-visible-aspect-ratio":
        _write_text(
            svg,
            re.sub(r'viewBox="[0-9. ]+"', 'viewBox="0 0 3000 200"', svg.read_text(), count=1),
        )
    elif kind == "change-visible-canvas":
        _write_text(svg, svg.read_text().replace("background:#ffffff", "background:#000000"))
    elif kind == "overlap-visible-nodes":
        _write_text(
            svg,
            svg.read_text().replace(
                "</svg>",
                '<text x="100" y="130">overlap one</text><text x="100" y="130">overlap two</text></svg>',
            ),
        )
    elif kind == "clip-visible-text":
        _write_text(svg, svg.read_text().replace("</svg>", '<rect width="12" height="12"/></svg>'))
    elif kind == "reduce-visible-contrast":
        _write_text(svg, svg.read_text().replace("</svg>", '<text fill="#ffffff">contrast</text></svg>'))
    elif kind == "remove-accessible-title":
        _write_text(svg, re.sub(r"<title[^>]*>.*?</title>", "", svg.read_text(), count=1))
    elif kind == "change-visible-text-only":
        _write_text(text, text.read_text() + "different visible target\n")
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
        relation_indexes = [
            index
            for index, line in enumerate(lines)
            if " -> " in line and not line.strip().startswith("//")
        ]
        lines[relation_indexes[0]], lines[relation_indexes[1]] = (
            lines[relation_indexes[1]],
            lines[relation_indexes[0]],
        )
        _write_text(source, "\n".join(lines) + "\n")
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


class ReleaseQaRegressions(unittest.TestCase):
    def _repository(self, temporary: str) -> Path:
        return build_repository(Path(temporary))

    def _assert_public_rejection(self, root: Path, family: str, expected: str) -> None:
        direct = _call(root, family)
        cli, make = _run_public(root, family)
        self.assertIn(expected, direct)
        self.assertIn(expected, (cli.stdout + cli.stderr).decode(errors="replace"))
        self.assertIn(expected, (make.stdout + make.stderr).decode(errors="replace"))
        self.assertNotEqual(cli.returncode, 0)
        self.assertNotEqual(make.returncode, 0)

    def test_weak_generic_repository_is_rejected_by_public_routes(self) -> None:
        with tempfile.TemporaryDirectory(prefix="weak-repository-", dir=os.environ["TMPDIR"]) as temporary:
            root = self._repository(temporary)
            _write_json(root / "learning/curriculum/architecture-curriculum-v1.json", _curriculum())
            _write_json(root / "learning/curriculum/templates/architecture-templates-v1.json", _template_registry())
            _write_json(root / "learning/curriculum/traces/architecture-trace-v1.json", _trace())
            self._assert_public_rejection(root, "I11-RED-REF-001", "I11_MODULE_CONTRACT_INVALID")

    def test_legacy_synthetic_render_is_rejected_by_public_routes(self) -> None:
        with tempfile.TemporaryDirectory(prefix="legacy-render-", dir=os.environ["TMPDIR"]) as temporary:
            root = self._repository(temporary)
            rendered = root / "architecture/expansions/i5-06/rendered"
            _write_text(rendered / "C4-L2-AWS.svg", _render_svg("C4-L2-AWS"))
            _write_text(rendered / "C4-L2-AWS.txt", "1. C4-L2-AWS source\n2. C4-L2-AWS target\n")
            _refresh_render_manifest(root)
            self._assert_public_rejection(root, "I11-RED-RENDER-001", "I11_RENDER_LINEAGE_INVALID")

    def test_manifest_must_close_projection_dot_raw_and_normalized_lineage(self) -> None:
        with tempfile.TemporaryDirectory(prefix="render-lineage-", dir=os.environ["TMPDIR"]) as temporary:
            root = self._repository(temporary)
            manifest = root / "architecture/expansions/i5-06/rendered/render-manifest.json"
            _mutate_json(manifest, lambda value: value["views"][0].update(projectionSha256="1" * 64))
            self._assert_public_rejection(root, "I11-RED-RENDER-001", "I11_RENDER_LINEAGE_INVALID")

    def test_all_protected_identities_are_enforced(self) -> None:
        with tempfile.TemporaryDirectory(prefix="protected-identity-", dir=os.environ["TMPDIR"]) as temporary:
            root = self._repository(temporary)
            protected = root / "architecture/rendered/C4-L0.svg"
            _write_text(protected, protected.read_text() + "\n<!-- drift -->\n")
            _git(root, "add", "architecture/rendered/C4-L0.svg")
            _git(
                root,
                "-c",
                "user.name=Checkpoint Test",
                "-c",
                "user.email=checkpoint@example.invalid",
                "commit",
                "-qm",
                "committed protected drift",
            )
            self._assert_public_rejection(root, "I11-RED-READONLY-001", "I11_PROTECTED_IDENTITY_DRIFT")

    def test_released_descriptor_cannot_redefine_byproduct_identities(self) -> None:
        with tempfile.TemporaryDirectory(prefix="released-descriptor-", dir=os.environ["TMPDIR"]) as temporary:
            root = self._repository(temporary)
            descriptor = root / "learning/contracts/learning-contract-set-v1.json"
            _mutate_json(descriptor, lambda value: value["contracts"][0].update(contentSha256="1" * 64))
            _git(root, "add", "learning/contracts/learning-contract-set-v1.json")
            _git(
                root,
                "-c",
                "user.name=Checkpoint Test",
                "-c",
                "user.email=checkpoint@example.invalid",
                "commit",
                "-qm",
                "committed released descriptor drift",
            )
            self._assert_public_rejection(root, "I11-RED-READONLY-001", "I11_PROTECTED_IDENTITY_DRIFT")

    def test_security_scan_covers_relevant_content_not_optional_policy_only(self) -> None:
        with tempfile.TemporaryDirectory(prefix="content-scan-", dir=os.environ["TMPDIR"]) as temporary:
            root = self._repository(temporary)
            source = root / "learning/curriculum/command-owner-activation-i5-06-stage-a-v1.json"
            _mutate_json(source, lambda value: value.update(credential="not-for-publication"))
            self._assert_public_rejection(root, "I11-RED-S3-001", "I11_S3_SECRET")

    def test_minimal_evidence_is_not_a_complete_release_generation(self) -> None:
        with tempfile.TemporaryDirectory(prefix="evidence-closure-", dir=os.environ["TMPDIR"]) as temporary:
            root = self._repository(temporary)
            (root / ".claude/evidence/control/commands.raw.json").unlink()
            _refresh_evidence_index(root)
            report = check_repository(root)
            self.assertFalse(report.ok)
            self.assertIn("I11_EVIDENCE_CLOSURE_MISSING", report.issues)

    def test_evidence_receipts_are_byte_bound_not_predicate_flags(self) -> None:
        with tempfile.TemporaryDirectory(prefix="evidence-receipt-", dir=os.environ["TMPDIR"]) as temporary:
            root = self._repository(temporary)
            evidence = root / ".claude/evidence/control"
            commands = _load_json(evidence / "commands.raw.json")
            commands[0]["stdoutSha256"] = "1" * 64
            _write_json(evidence / "commands.raw.json", commands, 0o600)
            sanitized = _load_json(evidence / "commands.sanitized.json")
            sanitized[0]["rawSha256"] = _canonical_sha256(commands[0])
            _write_json(evidence / "commands.sanitized.json", sanitized, 0o600)
            _refresh_closure_payload_binding(root)
            _refresh_evidence_index(root)
            _refresh_selector(root)
            report = check_repository(root)
            self.assertFalse(report.ok)
            self.assertIn("I11_EVIDENCE_CLOSURE_MISSING", report.issues)


class RealOwnedProcessLimits(unittest.TestCase):
    def _run(self, code: str, limits: RepositoryLimits, cwd: Path = SOURCE_ROOT) -> object:
        runtime = Path(os.environ["I11_RUNTIME"])
        return _run_owned_process(
            (str(runtime / "venv/bin/python"), "-c", code),
            cwd=cwd,
            environment=_runtime_environment(),
            limits=limits,
        )

    def test_deadline_terminates_and_reaps_real_process_group(self) -> None:
        sentinel = "I11_REAP_SENTINEL_11_STAGE_A"
        code = (
            "import signal,subprocess,sys,time;"
            f"sentinel='{sentinel}';"
            "signal.signal(signal.SIGTERM,signal.SIG_IGN);"
            "subprocess.Popen([sys.executable,'-c',"
            f"'import os,signal,time;sentinel=\"{sentinel}\";os.setsid();"
            "signal.signal(signal.SIGTERM,signal.SIG_IGN);time.sleep(30)']);"
            "time.sleep(30)"
        )
        started = time.monotonic()
        with self.assertRaisesRegex(RepositoryInputError, "I11_RESOURCE_DEADLINE"):
            self._run(code, RepositoryLimits(timeout_seconds=0.2))
        self.assertGreaterEqual(time.monotonic() - started, 5.0)
        processes = subprocess.run(
            ("/bin/ps", "-axo", "command="),
            check=True,
            stdout=subprocess.PIPE,
        ).stdout.decode()
        self.assertNotIn(sentinel, processes)

    def test_aggregate_rss_is_sampled_from_real_processes(self) -> None:
        with self.assertRaisesRegex(RepositoryInputError, "I11_RESOURCE_RSS"):
            self._run(
                "import time;payload=bytearray(32*1024*1024);time.sleep(10)",
                RepositoryLimits(timeout_seconds=10, max_rss_bytes=4 * 1024 * 1024),
            )

    def test_process_count_is_sampled_from_real_descendants(self) -> None:
        code = (
            "import subprocess,sys,time;"
            "subprocess.Popen([sys.executable,'-c','import time;time.sleep(10)']);"
            "time.sleep(10)"
        )
        with self.assertRaisesRegex(RepositoryInputError, "I11_RESOURCE_PROCESS_COUNT"):
            self._run(code, RepositoryLimits(timeout_seconds=10, max_processes=1))

    def test_output_limit_stops_real_writer_before_unbounded_capture(self) -> None:
        started = time.monotonic()
        with self.assertRaisesRegex(RepositoryInputError, "I11_RESOURCE_OUTPUT"):
            self._run(
                "import os,signal;signal.signal(signal.SIGTERM,signal.SIG_IGN)\n"
                "while True: os.write(1,b'x'*65536)",
                RepositoryLimits(timeout_seconds=10, max_output_bytes=128 * 1024),
            )
        self.assertGreaterEqual(time.monotonic() - started, 5.0)

    def test_created_file_count_is_sampled_from_real_filesystem(self) -> None:
        with tempfile.TemporaryDirectory(prefix="resource-files-", dir=os.environ["TMPDIR"]) as temporary:
            cwd = Path(temporary)
            code = (
                "from pathlib import Path;import time;"
                "[(Path(f'created-{index}.txt').write_text('x')) for index in range(4)];"
                "time.sleep(10)"
            )
            with self.assertRaisesRegex(RepositoryInputError, "I11_RESOURCE_FILE_COUNT"):
                self._run(
                    code,
                    RepositoryLimits(timeout_seconds=10, max_created_files=2),
                    cwd,
                )

    def test_created_file_bytes_are_sampled_from_real_filesystem(self) -> None:
        with tempfile.TemporaryDirectory(prefix="resource-bytes-", dir=os.environ["TMPDIR"]) as temporary:
            cwd = Path(temporary)
            code = "from pathlib import Path;import time;Path('large.bin').write_bytes(b'x'*65536);time.sleep(10)"
            with self.assertRaisesRegex(RepositoryInputError, "I11_RESOURCE_FILE_BYTES"):
                self._run(
                    code,
                    RepositoryLimits(timeout_seconds=10, max_created_bytes=4_096),
                    cwd,
                )
