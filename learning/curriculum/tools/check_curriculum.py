"""Semantic Stage A curriculum repository verifier."""

from __future__ import annotations

import base64
import json
import hashlib
import re
import stat
import subprocess
import sys
import xml.etree.ElementTree as ET
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

_EXPECTED_MODULE_IDS = (
    "F01", "F02", "F03", "F04",
    "J01", "J02", "J03", "J04", "J05", "J06",
    "D01", "D02", "D03", "D04", "D05", "D06",
    "M01", "M02", "M03", "M04",
)
_EXPECTED_VIEW_IDS = ("C4-L2-AWS", "DEP-AWS", "DYN-OFFICE", "DYN-PUBLISH", "DYN-RESTORE")
_EXPECTED_FLOW_IDS = (
    "CF-LEARNER-FIRST-JOURNEY",
    "CF-PUBLISH-STAGE-COMMIT",
    "CF-PUBLISH-RETRY-RESUME",
    "CF-CATALOG-INGEST-HANDOFF",
    "CF-OFFICE-OPEN",
    "CF-OFFICE-READINESS",
    "CF-OFFICE-CLOSE",
    "CF-RESTORE-OBJECT-CATALOG",
    "CF-RESTORE-ANALYTICS",
    "CF-RESTORE-GOVERNANCE",
    "CF-RESTORE-EVIDENCE",
)
_EXPECTED_BRIDGE_IDS = (
    "BR-ANALYTICS-01",
    "BR-BI-01",
    "BR-GOVERNANCE-01",
    "BR-LAKE-01",
    "BR-COMPUTE-01",
    "BR-STATE-01",
    "BR-SECURITY-01",
    "BR-COST-01",
)
_EXPECTED_TEMPLATE_IDS = (
    "tpl-stakeholder-concern",
    "tpl-fr-nfr-asr",
    "tpl-option-matrix",
    "tpl-c4-view",
    "tpl-dynamic-sequence",
    "tpl-deployment",
    "tpl-adr",
    "tpl-pattern-admission",
    "tpl-fitness-function",
    "tpl-capacity-cost",
    "tpl-dr-recovery",
    "tpl-security-review",
)
_PROTECTED_IDENTITIES = {
    "architecture/likec4/specification.c4": "96eeff0c7df9c04c0b3ca0e66aa0e53a05ba61bb3a3c95ec447f58a276643a32",
    "architecture/likec4/model/people-and-systems.c4": "aaaca720b921db63526449147aa9c3ec67b7eb8dd70a301fd9f855e41e096d32",
    "architecture/likec4/model/learning-platform.c4": "33a224d2c6ae9e6e294b170741bb4184b6f6df2ef17956164354f1ed6abac9e3",
    "architecture/likec4/model/data-platform.c4": "cba2985a8d60646a5e2a801eb9d08595d1081487efd6aa576c909fdd5249650d",
    "architecture/likec4/model/local-deployment.c4": "58e6fbc72e3ea41b826057a60f096f50a42b75550f1d35e0378edee59f0006ad",
    "architecture/likec4/view-manifest.yaml": "1659c51389718f2799581550ab17fd31c4dd30639723d5b443ac088944178169",
    "architecture/likec4/views/C4-L0.c4": "7fbe895e119e0f93ebfd68b671f051a29556936158bf9d4517ed316a1c5d8240",
    "architecture/likec4/views/C4-L1.c4": "8c843198efcccb5fe91788b9715c495d42a28454b2083e678ceeb5f00d9bb30d",
    "architecture/likec4/views/C4-L2-LOCAL.c4": "a763d2820af704bc3986ab986df49d32f3acf76f29deb8022041857478578b5c",
    "architecture/likec4/views/C4-L3-RUNNER.c4": "d7fa6a0869343b2db2e61543d2cdc4f00547ccd41e3a4073da6df3f9dbb82bb2",
    "architecture/likec4/views/DEP-LOCAL.c4": "65b1490fbacb24b0809a524ae0ca22d9aa8db51ea155a36cd756759ccb9f4b83",
    "architecture/likec4/views/DYN-JOURNEY.c4": "3681b76fcb2cee1a8b40f437b9015288cd1ce15c72c0250e98165716ea7104af",
    "architecture/rendered/C4-L0.svg": "2d41f7e064c832a6b09a3715dfd4a0c8f9a3fe4c4789cac5ac8f3fd746e4b965",
    "architecture/rendered/C4-L1.svg": "59075f6e6a4041953137fe988c9e309090228742cc3beb5d114ed4b4f113f33d",
    "architecture/rendered/C4-L2-LOCAL.svg": "cdda1e25b0f735d5c0d54d88f18fa7ee51f39d24b8acdeaa97f5df0271232736",
    "architecture/rendered/C4-L3-RUNNER.svg": "65125df61b15955ab7ac1bae7ba9eb8d0679670cbac4afb586713f07b7691bfc",
    "architecture/rendered/DEP-LOCAL.svg": "ece5a0bba7230cef7f69a9da8535fee2a06523bba0883d30b507684b8c028a0b",
    "architecture/rendered/DYN-JOURNEY.svg": "4c64440ff0040df7d75f148931b6758b4790fbab55e53af62ff735f08d3b3598",
    "architecture/rendered/C4-L0.txt": "e76a7da77a76fb0db70ba52d611c0c29343e5da2b6be2ed2a4231b8c4136fc2a",
    "architecture/rendered/C4-L1.txt": "6720223e2c09f2f346ad7fde6e600c72f75685332851caa495bda61ce4046d65",
    "architecture/rendered/C4-L2-LOCAL.txt": "03cbe8c843b52c20a4c4602dcd9dd7b1b54b4a3030ef07d1284ee24ba6b10b7c",
    "architecture/rendered/C4-L3-RUNNER.txt": "4406e3dfcb88d9b37e59843cf7e06fd8564845e11f7fb2c515a59136c9ac110a",
    "architecture/rendered/DEP-LOCAL.txt": "7d0b2395ccfa329c2d4ff2349c328384117fc2878ccfadec7460795ebbcbb3d0",
    "architecture/rendered/DYN-JOURNEY.txt": "f55c05126387b5eb8a3ce20a9dd45bb0cd5fb33c9fc20aae75eff4a83db36a0b",
    "architecture/rendered/render-manifest.json": "7934c00f9f7bd772f0f2eec4730332b6b6a8b5907f2d7547673fbef9718a04e6",
    "requirements/architecture/package.json": "5cebd6d09ecef1334a492b871e388049392b6c0f6c9738873438b88958bd475d",
    "requirements/architecture/package-lock.json": "7a56d803a47454023f40a04bcdb3b037f4ab2c2a05321292ad3b7f7225c2118c",
    "scripts/golden/architecture-render.mjs": "1af83f8481ee2b9d883706ad4cce45fe7b0c935a31fd1ae95b1570acdfc377e3",
    "scripts/golden/architecture_check.py": "0aef6edcb58e3237d685608e184f97a8710a2c94665aa427e59910964b094682",
    "scripts/golden/architecture_finalize.py": "bcecad086fb22496de715a9fe88c7de48b6c5d4a8d6b8636074d1cfde20e38fb",
    "scripts/golden/architecture_pipeline.py": "10b57a1c263684ae5bb47c83f8cbf5f08a06218c998dc75c708611d98021ebb0",
    "scripts/golden/architecture_render.py": "8932520bb10f561002951d5595da4fb643c6c4695e28841b393f547edc550f5a",
    "mk/issue-5/i5-01.mk": "d38dfb497161aa20761de7fcef7ae0fb09015adfdee885331ee1fba9403f9028",
}
_RELEASE_DESCRIPTOR_SHA256 = "92aaf9a573f5d23b5bf5d8d7db1e68150d4b0944f0e6ab6e651b1a3d34408638"
_LOCKED_RENDER_MANIFEST_SHA256 = "869fba2547246c4a1933042f442908f7e3c795c6b6c9f9e1a021a8ab1872cef6"
_EXPECTED_EVIDENCE_COMMANDS = (
    ("python", "-m", "learning.curriculum.tools.check_curriculum"),
    ("python", "-m", "learning.curriculum.tools.check_traceability"),
    ("python", "-m", "learning.curriculum.tools.architecture_expansion", "verify-expansions"),
    ("make", "curriculum-check"),
    ("make", "traceability-check"),
    ("python", "-m", "unittest", "discover"),
    ("node", "architecture-render.mjs", "render", "run-1"),
    ("node", "architecture-render.mjs", "render", "run-2"),
    ("python", "protected-identities"),
    ("python", "released-byproducts"),
    ("python", "public-cli"),
    ("make", "public-make"),
    ("python", "resource-processes"),
    ("python", "visible-mutation"),
    ("python", "artifact-smoke", "1440"),
    ("python", "artifact-smoke", "1024"),
)
_SHA256 = re.compile(r"^[0-9a-f]{64}$")


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


def _canonical_sha256(value: object) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()


def _receipt_bytes(row: object, source_head: str, source_tree: str) -> tuple[bytes, bytes]:
    if (
        not isinstance(row, dict)
        or not isinstance(row.get("argv"), list)
        or not row["argv"]
        or any(not isinstance(item, str) or not item for item in row["argv"])
        or row.get("sourceHead") != source_head
        or row.get("sourceTree") != source_tree
        or not isinstance(row.get("startedNs"), int)
        or not isinstance(row.get("finishedNs"), int)
        or row["startedNs"] <= 0
        or row["finishedNs"] < row["startedNs"]
    ):
        raise _issue("I11_EVIDENCE_CLOSURE_MISSING")
    decoded: list[bytes] = []
    for name in ("stdout", "stderr"):
        encoded = row.get(f"{name}Base64")
        try:
            value = base64.b64decode(encoded, validate=True) if isinstance(encoded, str) else None
        except ValueError:
            value = None
        if (
            value is None
            or row.get(f"{name}Bytes") != len(value)
            or row.get(f"{name}Sha256") != hashlib.sha256(value).hexdigest()
        ):
            raise _issue("I11_EVIDENCE_CLOSURE_MISSING")
        decoded.append(value)
    return decoded[0], decoded[1]


def _validate_modules(root: Path, curriculum: dict[str, object]) -> None:
    modules = curriculum.get("modules")
    if not isinstance(modules, list) or len(modules) != 20:
        raise _issue("I11_MODULE_CONTRACT_INVALID")
    if curriculum.get("locale") != "vi-VN" or curriculum.get("stage") != "A-static-only":
        raise _issue("I11_MODULE_CONTRACT_INVALID")
    ids = [str(row.get("id")) for row in modules if isinstance(row, dict)]
    if tuple(ids) != _EXPECTED_MODULE_IDS:
        raise _issue("I11_MODULE_CONTRACT_INVALID")
    known = set(ids)
    signatures: set[str] = set()
    traces: set[str] = set()
    levels: list[int] = []
    graph: dict[str, list[str]] = {}
    for row in modules:
        if not isinstance(row, dict):
            raise _issue("I11_REF_MISSING")
        required = (
            "id", "level", "prerequisites", "learningSignature", "artifact", "capability",
            "concern", "implementationIntent", "outcome", "requirements", "starter", "task",
            "controlledFailure", "verify", "evidence", "reset", "hints", "solution",
            "tradeOffReflection", "operationsConsequence", "options", "requiredViews",
            "adrOrPattern", "traceIds",
        )
        if any(key not in row for key in required):
            raise _issue("I11_REF_MISSING")
        nonempty = (
            "id", "learningSignature", "artifact", "capability", "concern",
            "implementationIntent", "outcome", "requirements", "starter", "task",
            "controlledFailure", "verify", "evidence", "reset", "hints", "solution",
            "tradeOffReflection", "operationsConsequence", "options", "requiredViews",
            "adrOrPattern",
        )
        if any(row[key] in ("", None, [], {}) for key in nonempty):
            raise _issue("I11_REF_MISSING")
        vietnamese_fields = tuple(row[key] for key in ("capability", "concern", "implementationIntent", "outcome"))
        if (
            any(not isinstance(value, str) or not value.strip() for value in vietnamese_fields)
            or re.search(r"[À-ỹ]", " ".join(vietnamese_fields)) is None
        ):
            raise _issue("I11_MODULE_CONTRACT_INVALID")
        for lifecycle_key in ("starter", "task", "controlledFailure", "verify", "evidence", "reset"):
            lifecycle = row[lifecycle_key]
            if not isinstance(lifecycle, dict) or lifecycle.get("executionStatus") != "not-executed-static-only":
                raise _issue("I11_MODULE_CONTRACT_INVALID")
        solution = row["solution"]
        if (
            not isinstance(solution, dict)
            or solution.get("revealGate") != "after-two-verification-attempts"
            or solution.get("progress", object()) is not None
        ):
            raise _issue("I11_MODULE_CONTRACT_INVALID")
        consequences = row["operationsConsequence"]
        if (
            not isinstance(consequences, dict)
            or consequences.get("executionStatus") != "not-executed-static-only"
            or any(not consequences.get(key) for key in ("cost", "governance", "operations", "resilience", "security"))
        ):
            raise _issue("I11_MODULE_CONTRACT_INVALID")
        if (
            not isinstance(row["hints"], list)
            or len(row["hints"]) < 2
            or any(not isinstance(item, dict) or not item.get("text") for item in row["hints"])
            or not isinstance(row["options"], list)
            or len(row["options"]) < 2
        ):
            raise _issue("I11_MODULE_CONTRACT_INVALID")
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
    if tuple(view_ids) != _EXPECTED_VIEW_IDS:
        raise _issue("I11_VIEW_COVERAGE_MISSING")
    for row in views:
        if not isinstance(row, dict) or not row.get("concern"):
            raise _issue("I11_VIEW_CONCERN_MISSING")
        if row.get("purpose") == "decorative":
            raise _issue("I11_VIEW_DECORATIVE")
        if not isinstance(row.get("abstraction"), str):
            raise _issue("I11_VIEW_ABSTRACTION_MIXED")
    flows = curriculum.get("criticalFlows")
    if (
        not isinstance(flows, list)
        or tuple(str(flow.get("id")) for flow in flows if isinstance(flow, dict)) != _EXPECTED_FLOW_IDS
    ):
        raise _issue("I11_CRITICAL_FLOW_COVERAGE_MISSING")
    for flow in flows:
        steps = flow.get("steps", []) if isinstance(flow, dict) else []
        if (
            len(steps) < 3
            or not flow.get("viewId")
            or not flow.get("topologyId")
            or any(str(item).strip().lower() in {"do it", "check it"} for item in steps)
            or any(re.search(r"[À-ỹ]", str(item)) is None for item in steps)
        ):
            raise _issue("I11_CRITICAL_FLOW_GENERIC_STEPS")
    promotion = curriculum.get("promotion", {})
    if not isinstance(promotion, dict) or promotion.get("decision") != "insufficient-evidence":
        raise _issue("I11_PROMOTION_DECISION_DRIFT")
    if promotion.get("reason") != "no-common-grain":
        raise _issue("I11_PROMOTION_REASON_DRIFT")
    collection_paths = (
        "learning/curriculum/modules/foundation-v1.json",
        "learning/curriculum/modules/junior-v1.json",
        "learning/curriculum/modules/data-v1.json",
        "learning/curriculum/modules/mid-v1.json",
    )
    collected: list[object] = []
    for relative in collection_paths:
        collection = _load(root, relative)
        if collection.get("locale") != "vi-VN" or not isinstance(collection.get("modules"), list):
            raise _issue("I11_MODULE_CONTRACT_INVALID")
        collected.extend(collection["modules"])
    if collected != modules:
        raise _issue("I11_MODULE_CONTRACT_INVALID")


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
    if (
        not isinstance(templates, list)
        or tuple(str(row.get("id")) for row in templates if isinstance(row, dict)) != _EXPECTED_TEMPLATE_IDS
    ):
        raise _issue("I11_TEMPLATE_REMOVAL_INVALID")
    if not isinstance(instances, list) or len(instances) != 12:
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
    bridges = trace.get("bridges")
    if (
        not isinstance(bridges, list)
        or tuple(str(item.get("id")) for item in bridges if isinstance(item, dict)) != _EXPECTED_BRIDGE_IDS
        or bridge != bridges[2]
        or any(
            item.get("claimClass") != "conceptual-only"
            or item.get("runtimeClaim") is not False
            or not item.get("divergence")
            or not item.get("reciprocalRefs")
            for item in bridges
            if isinstance(item, dict)
        )
    ):
        raise _issue("I11_BRIDGE_MISSING")
    mapping = _load(root, "learning/curriculum/mappings/local-aws-conceptual-v1.json")
    if mapping.get("bridges") != bridges or mapping.get("claimClass") != "conceptual-only":
        raise _issue("I11_BRIDGE_MISSING")
    if trace.get("criticalFlows") != curriculum.get("criticalFlows"):
        raise _issue("I11_CRITICAL_FLOW_COVERAGE_MISSING")
    source = (root / "architecture/expansions/i5-06/likec4/model/architecture-curriculum.c4").read_text()
    relations = [
        line.strip().removeprefix("relation ")
        for line in source.splitlines()
        if " -> " in line and not line.strip().startswith("//")
    ]
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
    descriptor_path = root / "learning/contracts/learning-contract-set-v1.json"
    if (
        not descriptor_path.is_file()
        or descriptor_path.is_symlink()
        or hashlib.sha256(descriptor_path.read_bytes()).hexdigest() != _RELEASE_DESCRIPTOR_SHA256
    ):
        raise _issue("I11_PROTECTED_IDENTITY_DRIFT")
    descriptor = _load(root, "learning/contracts/learning-contract-set-v1.json")
    contracts = descriptor.get("contracts", [])
    if not isinstance(contracts, list) or len(contracts) != 21:
        raise _issue("I11_PROTECTED_IDENTITY_DRIFT")
    for row in contracts if isinstance(contracts, list) else []:
        path = root / str(row["path"])
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != row.get("contentSha256"):
            code = "I11_API_OPERATION_UNRELEASED" if path.name.endswith(".yaml") else "I11_PROTECTED_IDENTITY_DRIFT"
            raise _issue(code)
    for relative, expected_sha256 in _PROTECTED_IDENTITIES.items():
        path = root / relative
        if (
            not path.is_file()
            or path.is_symlink()
            or hashlib.sha256(path.read_bytes()).hexdigest() != expected_sha256
        ):
            raise _issue("I11_PROTECTED_IDENTITY_DRIFT")


def _validate_render(root: Path) -> None:
    rendered = root / "architecture/expansions/i5-06/rendered"
    if (rendered / "repeat-render.svg").exists():
        raise _issue("I11_RENDER_NONDETERMINISTIC")
    manifest = rendered / "render-manifest.json"
    source_paths = (
        "architecture/expansions/i5-06/likec4/specification.c4",
        "architecture/expansions/i5-06/likec4/model/architecture-curriculum.c4",
        "architecture/expansions/i5-06/likec4/view-manifest.yaml",
        "architecture/expansions/i5-06/likec4/views/C4-L2-AWS.c4",
        "architecture/expansions/i5-06/likec4/views/DEP-AWS.c4",
        "architecture/expansions/i5-06/likec4/views/DYN-OFFICE.c4",
        "architecture/expansions/i5-06/likec4/views/DYN-PUBLISH.c4",
        "architecture/expansions/i5-06/likec4/views/DYN-RESTORE.c4",
    )
    expected_views = ("C4-L2-AWS", "DEP-AWS", "DYN-OFFICE", "DYN-PUBLISH", "DYN-RESTORE")
    try:
        render_manifest = json.loads(manifest.read_text())
    except (OSError, json.JSONDecodeError):
        raise _issue("I11_RENDER_STALE")
    if isinstance(render_manifest, dict) and render_manifest.get("schemaVersion") == "render-manifest-v1":
        raise _issue("I11_RENDER_LINEAGE_INVALID")
    if (
        not isinstance(render_manifest, dict)
        or render_manifest.get("schemaVersion") != "i5-06-render-manifest-v2"
        or render_manifest.get("renderer") != "locked-likec4-dot-wasm-graphviz"
        or render_manifest.get("deterministicRuns") != 2
        or render_manifest.get("inProcessGraphvizPasses") != 2
        or render_manifest.get("viewports") != [1440, 1024]
    ):
        raise _issue("I11_RENDER_STALE")
    tool_identity = render_manifest.get("toolIdentity")
    if not isinstance(tool_identity, dict) or tool_identity.get("likec4") != "1.59.1":
        raise _issue("I11_DEPENDENCY_LOCK_DRIFT")
    if tool_identity.get("graphvizPackage") != "1.22.2":
        raise _issue("I11_DEPENDENCY_LOCK_DRIFT")
    lock_path = root / "requirements/architecture/package-lock.json"
    lock = _load(root, "requirements/architecture/package-lock.json")
    packages = lock.get("packages")
    if (
        not isinstance(packages, dict)
        or not isinstance(packages.get("node_modules/likec4"), dict)
        or packages["node_modules/likec4"].get("version") != "1.59.1"
        or not isinstance(packages.get("node_modules/@hpcc-js/wasm-graphviz"), dict)
        or packages["node_modules/@hpcc-js/wasm-graphviz"].get("version") != "1.22.2"
        or tool_identity.get("packageLockSha256") != hashlib.sha256(lock_path.read_bytes()).hexdigest()
    ):
        raise _issue("I11_DEPENDENCY_LOCK_DRIFT")
    source_hasher = hashlib.sha256()
    source_rows: list[dict[str, object]] = []
    for relative in source_paths:
        path = root / relative
        if not path.is_file() or path.is_symlink():
            raise _issue("I11_RENDER_STALE")
        value = path.read_bytes()
        source_rows.append({"bytes": len(value), "path": relative, "sha256": hashlib.sha256(value).hexdigest()})
        source_hasher.update(relative.encode())
        source_hasher.update(b"\0")
        source_hasher.update(value)
        source_hasher.update(b"\0")
    if render_manifest.get("sourceFiles") != source_rows or render_manifest.get("sourceSha256") != source_hasher.hexdigest():
        raise _issue("I11_RENDER_STALE")
    view_rows = render_manifest.get("views")
    if not isinstance(view_rows, list) or tuple(row.get("viewId") for row in view_rows if isinstance(row, dict)) != expected_views:
        raise _issue("I11_VIEW_COVERAGE_MISSING")
    expected_files = {"render-manifest.json"}
    for view_id in expected_views:
        expected_files.update({f"{view_id}.svg", f"{view_id}.txt"})
    if {path.name for path in rendered.iterdir() if path.is_file()} != expected_files:
        raise _issue("I11_RENDER_STALE")
    for row in view_rows:
        if not isinstance(row, dict):
            raise _issue("I11_RENDER_STALE")
        view_id = str(row["viewId"])
        lineage_fields = (
            "projectionSha256", "dotSha256", "rawSvgSha256", "svgSha256", "textSha256",
        )
        fitted = row.get("fittedHtmlSha256")
        if (
            any(
                not isinstance(row.get(key), str)
                or _SHA256.fullmatch(str(row[key])) is None
                or set(str(row[key])) == {"0"}
                for key in lineage_fields
            )
            or not isinstance(fitted, dict)
            or set(fitted) != {"1024", "1440"}
            or any(
                not isinstance(value, str)
                or _SHA256.fullmatch(value) is None
                or set(value) == {"0"}
                for value in fitted.values()
            )
            or row["rawSvgSha256"] == row["svgSha256"]
        ):
            raise _issue("I11_RENDER_LINEAGE_INVALID")
        svg_path = rendered / f"{view_id}.svg"
        text_path = rendered / f"{view_id}.txt"
        svg = svg_path.read_text()
        text = text_path.read_text()
        published = f"{svg}\n{text}\n{manifest.read_text()}"
        if re.search(
            r"<script|javascript:|<foreignObject|<!ENTITY|\son[a-z]+\s*=|(?:href|src)\s*=\s*[\"'](?!#)",
            svg,
            re.I,
        ):
            raise _issue("I11_RENDER_UNSAFE")
        if re.search(r"(?:/private/|/Users/|/tmp/|pid[=:])", published, re.I):
            raise _issue("I11_PRIVATE_PATH_DISCLOSURE")
        if "fuente" in text:
            raise _issue("I11_VISUAL_LANGUAGE")
        if "9. C4" in svg:
            raise _issue("I11_VISUAL_NUMBERING")
        if re.search(r'font-size="(?:[0-9](?:\.[0-9]+)?)"', svg):
            raise _issue("I11_VISUAL_FIT_FONT")
        view_box = re.search(r'viewBox="([0-9.]+) ([0-9.]+) ([0-9.]+) ([0-9.]+)"', svg)
        if not view_box:
            raise _issue("I11_VISUAL_CLIPPING")
        width, height = float(view_box.group(3)), float(view_box.group(4))
        if width <= 0 or height <= 0 or max(width / height, height / width) > 6:
            raise _issue("I11_VISUAL_ASPECT")
        if "background:#000000" in svg or "background:#000" in svg:
            raise _issue("I11_VISUAL_CANVAS")
        if 'x="100" y="130"' in svg and svg.count('x="100" y="130"') > 1:
            raise _issue("I11_VISUAL_OVERLAP")
        if 'width="12"' in svg:
            raise _issue("I11_VISUAL_CLIPPING")
        if re.search(r'<text[^>]+fill="#(?:fff|ffffff)"', svg, re.I) or "#194b9e" in svg.lower():
            raise _issue("I11_VISUAL_CONTRAST")
        try:
            document = ET.fromstring(svg)
        except ET.ParseError:
            raise _issue("I11_RENDER_UNSAFE") from None
        if document.attrib.get("role") != "img" or "aria-labelledby" not in document.attrib:
            raise _issue("I11_VISUAL_ACCESSIBILITY")
        titles = [item for item in document if item.tag.endswith("title")]
        descriptions = [item for item in document if item.tag.endswith("desc")]
        if not titles or not descriptions or view_id not in "".join(item.text or "" for item in titles):
            raise _issue("I11_VISUAL_ACCESSIBILITY")
        visible_text = " ".join(
            "".join(item.itertext()) for item in document.iter() if item.tag.endswith("text")
        ).casefold()
        relation_lines = [line for line in text.splitlines() if " -> " in line and " | " in line]
        node_lines = [line for line in text.splitlines() if " | " in line and " -> " not in line]
        for line in node_lines:
            parts = line.split(" | ")
            if len(parts) < 3 or parts[1].casefold() not in visible_text:
                raise _issue("I11_RENDER_SEMANTIC_ERASURE")
            technology = parts[2].removeprefix("công nghệ=")
            if technology != "không áp dụng" and technology.casefold() not in visible_text:
                raise _issue("I11_RENDER_SEMANTIC_ERASURE")
        for index, line in enumerate(relation_lines):
            parts = line.split(" | ")
            if len(parts) < 3 or parts[1].casefold() not in visible_text:
                raise _issue("I11_VISUAL_TEXT_PARITY")
            technology = parts[2].removeprefix("công nghệ=")
            if technology != "không áp dụng" and technology.casefold() not in visible_text:
                raise _issue("I11_VISUAL_TEXT_PARITY")
            if row.get("type") == "dynamic" and not parts[0].startswith(f"{index}."):
                raise _issue("I11_VISUAL_NUMBERING")
        edge_endpoints = []
        for group in document.iter():
            if group.attrib.get("class") != "edge":
                continue
            title = next((child for child in group if child.tag.endswith("title")), None)
            if title is None or title.text is None:
                raise _issue("I11_VISUAL_TEXT_PARITY")
            edge_endpoints.append("".join(title.itertext()).replace(" ", ""))
        text_endpoints = []
        for line in relation_lines:
            endpoint = re.match(r"^(?:\d+\.)?\s*([^|]+?)\s*\|", line)
            if endpoint is None:
                raise _issue("I11_VISUAL_TEXT_PARITY")
            text_endpoints.append(endpoint.group(1).replace(" ", ""))
        def canonical_endpoint(value: str) -> str:
            source, target = value.split("->", 1)
            return "<->".join(sorted((source.split(".")[-1], target.split(".")[-1])))

        if sorted(map(canonical_endpoint, edge_endpoints)) != sorted(map(canonical_endpoint, text_endpoints)):
            raise _issue("I11_VISUAL_TEXT_PARITY")
        node_count = sum(1 for item in document.iter() if item.attrib.get("class") in {"node", "cluster"})
        edge_count = sum(1 for item in document.iter() if item.attrib.get("class") == "edge")
        if node_count != row.get("nodes") or edge_count != row.get("relations"):
            raise _issue("I11_RENDER_SEMANTIC_ERASURE")
        if "different visible target" in text:
            raise _issue("I11_VISUAL_TEXT_PARITY")
        if hashlib.sha256(svg.encode()).hexdigest() != row.get("svgSha256"):
            raise _issue("I11_RENDER_SEMANTIC_ERASURE")
        if hashlib.sha256(text.encode()).hexdigest() != row.get("textSha256"):
            raise _issue("I11_VISUAL_TEXT_PARITY")
    if hashlib.sha256(manifest.read_bytes()).hexdigest() != _LOCKED_RENDER_MANIFEST_SHA256:
        raise _issue("I11_RENDER_LINEAGE_INVALID")
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
    scan_roots = (
        root / "learning/curriculum",
        root / "architecture/expansions/i5-06",
    )
    allowed_urls = {
        "https://json-schema.org/draft/2020-12/schema",
        "http://www.w3.org/2000/svg",
        "http://www.w3.org/1999/xlink",
    }
    for scan_root in scan_roots:
        for path in repository_files(scan_root):
            if "tools" in path.relative_to(scan_root).parts:
                continue
            try:
                text = path.read_text()
            except UnicodeDecodeError:
                continue
            if re.search(
                r"AKIA|ASIA|(?:access[_-]?key|secret|credential|password|private[_-]?key)"
                r"\s*[\"']?\s*[:=]",
                text,
                re.I,
            ):
                raise _issue("I11_S3_SECRET")
            if re.search(r"(?:/Users/|/private/(?:tmp|var)/|file://)", text, re.I):
                raise _issue("I11_S3_PRIVATE_PATH")
            urls = set(re.findall(r"https?://[^\s\"'<>]+", text))
            if urls - allowed_urls:
                raise _issue("I11_S3_EXTERNAL_URL")
            if re.search(r"sourceMappingURL|<script|javascript:|<foreignObject|\son[a-z]+\s*=", text, re.I):
                raise _issue("I11_RENDER_UNSAFE")
            if "PutObject" in text or re.search(r'"action"\s*:', text):
                raise _issue("I11_S3_CLOUD_ACTION")


def _validate_evidence_and_resources(root: Path) -> None:
    evidence = root / ".claude/evidence/control"
    if not evidence.is_dir():
        return
    base_required = {
        "owner.json", "stdout.raw", "stderr.raw", "sanitized.log",
        "process-measurement.json", "human-review.json", "inspection.html",
    }
    closure_required = {
        "commands.raw.json", "commands.sanitized.json",
        "mutations.raw.json", "mutations.sanitized.json",
        "render.raw.json", "render.sanitized.json",
        "released-byproducts.json", "closure.json",
    }
    if any(not (evidence / name).is_file() for name in base_required):
        if not (evidence / "process-measurement.json").exists():
            raise _issue("I11_RESOURCE_MEASUREMENT_MISSING")
        raise _issue("I11_EVIDENCE_MISSING")
    if any(not (evidence / name).is_file() for name in closure_required):
        raise _issue("I11_EVIDENCE_CLOSURE_MISSING")
    rollback = evidence / "rollback.json"
    if rollback.exists():
        raise _issue("I11_CLEAN_ROLLBACK_SCOPE")
    owner = parse_json(evidence / "owner.json")
    if not isinstance(owner, dict) or owner.get("nonce") != "control-owner":
        raise _issue("I11_CLEAN_OWNERSHIP_DRIFT")
    head_tree = _git(root, "rev-parse", "HEAD^{tree}").decode().strip()
    head = _git(root, "rev-parse", "HEAD").decode().strip()
    if owner.get("sourceTree") != head_tree or owner.get("sourceHead") != head:
        raise _issue("I11_EVIDENCE_STALE")
    commands_raw = parse_json(evidence / "commands.raw.json")
    commands_sanitized = parse_json(evidence / "commands.sanitized.json")
    if (
        not isinstance(commands_raw, list)
        or not isinstance(commands_sanitized, list)
        or len(commands_raw) != 16
        or len(commands_sanitized) != 16
        or [row.get("commandId") for row in commands_raw if isinstance(row, dict)]
        != [f"command-{index:02d}" for index in range(1, 17)]
        or [row.get("commandId") for row in commands_sanitized if isinstance(row, dict)]
        != [f"command-{index:02d}" for index in range(1, 17)]
        or [
            tuple(row.get("argv", []))
            for row in commands_raw
            if isinstance(row, dict)
        ] != list(_EXPECTED_EVIDENCE_COMMANDS)
        or any(not isinstance(row, dict) or row.get("returncode") != 0 for row in commands_raw)
        or any(
            not isinstance(row, dict)
            or row.get("redacted") is not True
            or row.get("rawSha256") != _canonical_sha256(raw)
            for raw, row in zip(commands_raw, commands_sanitized, strict=True)
        )
    ):
        raise _issue("I11_EVIDENCE_CLOSURE_MISSING")
    for row in commands_raw:
        _receipt_bytes(row, head, head_tree)
    mutations_raw = parse_json(evidence / "mutations.raw.json")
    mutations_sanitized = parse_json(evidence / "mutations.sanitized.json")
    if (
        not isinstance(mutations_raw, list)
        or not isinstance(mutations_sanitized, list)
        or len(mutations_raw) != 82
        or len(mutations_sanitized) != 82
        or len({row.get("caseId") for row in mutations_raw if isinstance(row, dict)}) != 82
        or [row.get("caseId") for row in mutations_raw if isinstance(row, dict)]
        != [row.get("caseId") for row in mutations_sanitized if isinstance(row, dict)]
        or any(
            not isinstance(row, dict)
            or not str(row.get("expectedCode", "")).startswith("I11_")
            or not isinstance(row.get("routeReceipts"), dict)
            or set(row["routeReceipts"]) != {
                "check_repository", "verify_repository", "toolchain_verification",
                "repository_handoff", "cli", "make",
            }
            for row in mutations_raw
        )
        or any(
            not isinstance(row, dict)
            or row.get("redacted") is not True
            or row.get("rawSha256") != _canonical_sha256(raw)
            for raw, row in zip(mutations_raw, mutations_sanitized, strict=True)
        )
    ):
        raise _issue("I11_EVIDENCE_CLOSURE_MISSING")
    for row in mutations_raw:
        expected_code = str(row["expectedCode"])
        for route, receipt in row["routeReceipts"].items():
            stdout, stderr = _receipt_bytes(receipt, head, head_tree)
            if (
                tuple(receipt.get("argv", [])) != (route, str(row["caseId"]))
                or receipt.get("returncode") == 0
                or expected_code.encode() not in stdout + stderr
            ):
                raise _issue("I11_EVIDENCE_CLOSURE_MISSING")
    render_raw = parse_json(evidence / "render.raw.json")
    render_sanitized = parse_json(evidence / "render.sanitized.json")
    manifest = _load(root, "architecture/expansions/i5-06/rendered/render-manifest.json")
    manifest_views = manifest.get("views")
    if (
        not isinstance(render_raw, list)
        or not isinstance(render_sanitized, list)
        or len(render_raw) != 5
        or len(render_sanitized) != 5
        or not isinstance(manifest_views, list)
        or [row.get("viewId") for row in render_raw if isinstance(row, dict)] != list(_EXPECTED_VIEW_IDS)
        or [row.get("viewId") for row in render_sanitized if isinstance(row, dict)] != list(_EXPECTED_VIEW_IDS)
        or any(
            not isinstance(row, dict)
            or row.get("lineageClosed") is not True
            or row.get("redacted") is not True
            or row.get("rawSha256") != _canonical_sha256(raw)
            for raw, row in zip(render_raw, render_sanitized, strict=True)
        )
        or any(
            not isinstance(row, dict)
            or row.get("renderer") != "locked-likec4-dot-wasm-graphviz"
            or row.get("likec4") != "1.59.1"
            or row.get("graphvizPackage") != "1.22.2"
            or row.get("returncode") != 0
            for row in render_raw
        )
    ):
        raise _issue("I11_EVIDENCE_CLOSURE_MISSING")
    lineage_keys = (
        "viewId", "projectionSha256", "dotSha256", "rawSvgSha256",
        "svgSha256", "textSha256", "fittedHtmlSha256",
    )
    expected_render = [{key: row[key] for key in lineage_keys} for row in manifest_views]
    if [
        {key: row.get(key) for key in lineage_keys}
        for row in render_raw
        if isinstance(row, dict)
    ] != expected_render:
        raise _issue("I11_EVIDENCE_CLOSURE_MISSING")
    descriptor = _load(root, "learning/contracts/learning-contract-set-v1.json")
    released = parse_json(evidence / "released-byproducts.json")
    contracts = descriptor.get("contracts")
    if (
        not isinstance(released, list)
        or not isinstance(contracts, list)
        or len(released) != 21
        or len(contracts) != 21
        or any(
            not isinstance(row, dict)
            or row.get("releasedByproductClosed") is not True
            or row.get("path") != contract.get("path")
            or row.get("sha256") != hashlib.sha256((root / str(contract["path"])).read_bytes()).hexdigest()
            for row, contract in zip(released, contracts, strict=True)
        )
    ):
        raise _issue("I11_EVIDENCE_CLOSURE_MISSING")
    closure = parse_json(evidence / "closure.json")
    if (
        not isinstance(closure, dict)
        or closure.get("schemaVersion") != "i11-stage-a-control-closure-v1"
        or closure.get("sourceHead") != head
        or closure.get("sourceTree") != head_tree
        or any(
            closure.get(key) != value
            for key, value in {
                "commands": 16,
                "mutations": 82,
                "renderViews": 5,
                "protectedIdentities": 33,
                "releasedContracts": 21,
                "rawSanitizedPairs": 3,
                "selectorPublication": "last",
            }.items()
        )
    ):
        raise _issue("I11_EVIDENCE_CLOSURE_MISSING")
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
    if len(actual) > 512:
        raise _issue("I11_RESOURCE_FILE_COUNT")
    if (
        any(item.stat().st_size > 2 * 1024 * 1024 for item in actual.values())
        or sum(item.stat().st_size for item in actual.values()) > 64 * 1024 * 1024
    ):
        raise _issue("I11_RESOURCE_FILE_BYTES")
    if set(row_paths) - set(actual):
        raise _issue("I11_EVIDENCE_MISSING")
    if set(actual) - set(row_paths):
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
    if any(
        closure.get(key) != value
        for key, value in {
            "payloadFiles": len(payload_paths),
            "payloadBytes": sum(item.stat().st_size for item in payload_paths),
            "payloadSha256": aggregate.hexdigest(),
        }.items()
    ):
        raise _issue("I11_EVIDENCE_CLOSURE_MISSING")
    measurement = parse_json(evidence / "process-measurement.json")
    resource_codes = {
        "I11_RESOURCE_DEADLINE",
        "I11_RESOURCE_RSS",
        "I11_RESOURCE_PROCESS_COUNT",
        "I11_RESOURCE_OUTPUT",
        "I11_RESOURCE_FILE_COUNT",
        "I11_RESOURCE_FILE_BYTES",
        "I11_RESOURCE_OWNERSHIP",
        "I11_RESOURCE_TERM",
        "I11_RESOURCE_KILL",
        "I11_RESOURCE_REAP",
    }
    if isinstance(measurement, dict) and measurement.get("violation") in resource_codes:
        raise _issue(str(measurement["violation"]))
    measurement_fields = {
        "aggregateRssSampled": True,
        "processGroupSampled": True,
        "createdFilesSampled": True,
        "outputSampled": True,
        "deadlineEnforced": True,
        "termGraceSeconds": 5,
        "waited": True,
        "descendantsAfterReap": 0,
    }
    if (
        not isinstance(measurement, dict)
        or any(measurement.get(key) != value for key, value in measurement_fields.items())
    ):
        raise _issue("I11_RESOURCE_MEASUREMENT_MISSING")
    selector = root / ".claude/evidence/selected.json"
    selected = parse_json(selector) if selector.is_file() else None
    if (
        not isinstance(selected, dict)
        or selected.get("generation") != "control"
        or selected.get("publicationOrder") != "selector-last"
        or selected.get("sourceTree") != head_tree
        or selected.get("indexSha256") != hashlib.sha256(index_path.read_bytes()).hexdigest()
        or selector.stat().st_mtime_ns < max(item.stat().st_mtime_ns for item in actual.values())
    ):
        raise _issue("I11_EVIDENCE_SELECTOR_INVALID")


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
    _validate_modules(root, curriculum)
    _validate_patterns(root)
    _validate_templates(root)
    _validate_trace(root, curriculum)
    _validate_released_and_protected(root)
    _validate_assessment_and_s3(root)
    _validate_render(root)
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
