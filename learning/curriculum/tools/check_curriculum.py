"""Public curriculum checker entrypoint; semantic rules are added after RED."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Sequence
from jsonschema import Draft202012Validator

from .content_io import CheckResult, NormalizedRequest, admitted_runtime_ok, content_sha256, load_json

ENTRYPOINT_ID = "I11-EP-CURRICULUM"


def _prerequisite_codes(value: dict[str, Any]) -> list[str]:
    nodes = value.get("nodes", [])
    edges = value.get("edges", {})
    codes: list[str] = []
    if any(parent not in nodes for parents in edges.values() for parent in parents):
        codes.append("I11_PREQ_UNKNOWN")
    if any(node in edges.get(node, []) for node in nodes):
        codes.append("I11_PREQ_SELF")
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node: str) -> bool:
        if node in visiting:
            return True
        if node in visited:
            return False
        visiting.add(node)
        cyclic = any(parent in nodes and visit(parent) for parent in edges.get(node, []))
        visiting.remove(node)
        visited.add(node)
        return cyclic

    if any(visit(node) for node in nodes):
        codes.append("I11_PREQ_CYCLE")
    if any(node not in nodes for node in value.get("required", [])):
        codes.append("I11_PREQ_UNREACHABLE")
    if value.get("skipPreservesVerification") is False:
        codes.append("I11_PREQ_FORGED_SKIP")
    return codes


def _codes(payload: dict[str, Any]) -> list[str]:
    codes: list[str] = []
    if refs := payload.get("references"):
        if not refs.get("targetExists"): codes.append("I11_REF_MISSING")
        if refs.get("expectedHash") != refs.get("actualHash"): codes.append("I11_REF_STALE")
        if not refs.get("reciprocal"): codes.append("I11_REF_NONRECIPROCAL")
    if prerequisites := payload.get("prerequisites"):
        codes.extend(_prerequisite_codes(prerequisites))
    if views := payload.get("views"):
        ids = [item.get("id") for item in views]
        keys = [item.get("key") for item in views]
        if len(ids) != len(set(ids)) or len(keys) != len(set(keys)): codes.append("I11_VIEW_DUPLICATE")
        if any(not item.get("relations") for item in views): codes.append("I11_VIEW_DECORATIVE")
        if any(not item.get("concern") or not item.get("audience") for item in views): codes.append("I11_VIEW_CONCERN_MISSING")
        if any("+" in item.get("abstraction", "") for item in views): codes.append("I11_VIEW_ABSTRACTION_MIXED")
    if adr := payload.get("adr"):
        required = ("alternatives", "forces", "consequences", "verifier", "evidence")
        if any(not adr.get(field) for field in required) or adr.get("blockerTbc"):
            codes.append("I11_ADR_INCOMPLETE")
    if pattern := payload.get("pattern"):
        if not pattern.get("failure"): codes.append("I11_PATTERN_FAILURE_MISSING")
        if not pattern.get("verifier") or not pattern.get("removalRule"): codes.append("I11_PATTERN_VERIFIER_MISSING")
    if api := payload.get("apiTeaching"):
        if not set(api.get("referencedOperations", [])).issubset(api.get("releasedOperations", [])):
            codes.append("I11_API_OPERATION_UNRELEASED")
        if api.get("channels"): codes.append("I11_ASYNC_CHANNEL_UNRELEASED")
    if registry := payload.get("templateRegistry"):
        if registry.get("schemaToken") != "i5-06-architecture-template-registry-v1": codes.append("I11_TEMPLATE_SCHEMA_TOKEN_INVALID")
        compatibility = registry.get("compatibility", {})
        if not all(compatibility.get(k) for k in ("readerRange", "instanceBindingVersion", "supersessionPolicy", "removalPolicy")): codes.append("I11_TEMPLATE_COMPATIBILITY_INVALID")
        if not registry.get("registered"): codes.append("I11_TEMPLATE_UNREGISTERED")
        if registry.get("expectedHash") != registry.get("actualHash"): codes.append("I11_TEMPLATE_HASH_DRIFT")
        if not registry.get("reciprocal"): codes.append("I11_TEMPLATE_NONRECIPROCAL")
        if not registry.get("supersessionValid"): codes.append("I11_TEMPLATE_SUPERSESSION_INVALID")
        if not registry.get("removalValid"): codes.append("I11_TEMPLATE_REMOVAL_INVALID")
    if flow := payload.get("criticalFlow"):
        if not flow.get("dynamicView") or not flow.get("deploymentView"): codes.append("I11_CRITICAL_FLOW_COVERAGE_MISSING")
        if flow.get("reusedGenericVector"): codes.append("I11_CRITICAL_FLOW_GENERIC_STEPS")
    if assessment := payload.get("assessment"):
        if assessment.get("runtimeStatus") != "not-executed-static-only" or any(assessment.get(k) for k in ("writesProgress", "writesCompletion", "learnerEvidence")):
            codes.append("I11_STAGE_BOUNDARY_RUNTIME_FORGERY")
    if promotion := payload.get("promotion"):
        if promotion.get("decision") != "insufficient-evidence": codes.append("I11_PROMOTION_DECISION_DRIFT")
        if promotion.get("reason") != "no-common-grain": codes.append("I11_PROMOTION_REASON_DRIFT")
    return codes


def run(request: NormalizedRequest) -> CheckResult:
    projection: dict[str, Any] = {"document": request.payload, "sourceClass": request.source.split(":", 1)[0]}
    return CheckResult(ENTRYPOINT_ID, True, tuple(_codes(dict(request.payload))), {"projectionSha256": content_sha256(projection)})


ROOT = Path(__file__).resolve().parents[3]
EXPECTED_PREREQUISITES = {
    "F01": [], "F02": ["F01"], "F03": ["F02"], "F04": ["F03"],
    "J01": ["F03", "F04"], "J02": ["F04"], "J03": ["J02"], "J04": ["J03"],
    "J05": ["J03", "J04"], "J06": ["J03"], "D01": ["F03"], "D02": ["D01"],
    "D03": ["D02", "J04"], "D04": ["D02"], "D05": ["D02", "D03", "D04"],
    "D06": ["D05"], "M01": ["J02", "J03", "J04", "J05", "J06", "D05"],
    "M02": ["M01", "J04"], "M03": ["D04", "D05", "M01"], "M04": ["J05", "M01"],
}


def _read(relative: str) -> dict[str, Any]:
    return dict(load_json(ROOT / relative).payload)


def _schema_valid(document: dict[str, Any], schema_name: str) -> bool:
    schema = _read(f"learning/curriculum/contracts/{schema_name}")
    return not list(Draft202012Validator(schema).iter_errors(document))


def check_repository() -> CheckResult:
    codes: list[str] = []
    if not admitted_runtime_ok(): codes.append("I11_RESOURCE_OWNERSHIP")
    manifest = _read("learning/curriculum/architecture-curriculum-v1.json")
    if not _schema_valid(manifest, "architecture-curriculum-v1.schema.json"):
        codes.append("I11_REF_STALE")
    modules = [
        module for path in manifest.get("moduleCollections", [])
        for module in _read(path).get("modules", [])
    ]
    by_id = {module.get("moduleId"): module for module in modules}
    if len(modules) != 20 or len(by_id) != 20 or set(by_id) != set(EXPECTED_PREREQUISITES):
        codes.append("I11_PREQ_UNREACHABLE")
    for module_id, prerequisites in EXPECTED_PREREQUISITES.items():
        module = by_id.get(module_id, {})
        if module.get("prerequisites") != prerequisites:
            codes.append("I11_PREQ_UNKNOWN")
        title = module.get("titleVi", "")
        if not title or not any(character in title for character in "ăâđêôơưDữệềờứấậốộíìáàảãạ"): codes.append("I11_VIEW_CONCERN_MISSING")
        assessment = module.get("assessment", {})
        if assessment.get("runtimeStatus") != "not-executed-static-only" or any(assessment.get(k) for k in ("writesProgress", "writesCompletion", "learnerEvidence")):
            codes.append("I11_STAGE_BOUNDARY_RUNTIME_FORGERY")
        if set(module.get("consequences", {})) != {"operations", "resilience", "security", "cost", "governance"}:
            codes.append("I11_TRACE_GAP")
        exercise = module.get("exercise", {})
        if len(exercise.get("options", [])) < 2 or not exercise.get("implementationIntent"):
            codes.append("I11_ADR_INCOMPLETE")
    registry = _read(manifest["templateRegistry"])
    if not _schema_valid(registry, "architecture-template-registry-v1.schema.json"):
        codes.append("I11_TEMPLATE_SCHEMA_TOKEN_INVALID")
    templates = registry.get("templates", [])
    if len(templates) != 12 or len({item.get("templateId") for item in templates}) != 12:
        codes.append("I11_TEMPLATE_UNREGISTERED")
    instances: dict[str, list[dict[str, Any]]] = {}
    for module in modules:
        for binding in module.get("templateBindings", []):
            instances.setdefault(binding.get("templateId", ""), []).append({"moduleId": module["moduleId"], **binding})
    for template in templates:
        digest = content_sha256(template.get("content"))
        if template.get("contentSha256") != digest: codes.append("I11_TEMPLATE_HASH_DRIFT")
        bound = instances.get(template.get("templateId"), [])
        if sorted(item["moduleId"] for item in bound) != template.get("instanceIds"): codes.append("I11_TEMPLATE_NONRECIPROCAL")
        for item in bound:
            if (item.get("registryId"), item.get("version"), item.get("contentSha256")) != (registry.get("registryId"), template.get("version"), digest):
                codes.append("I11_TEMPLATE_NONRECIPROCAL")
    catalogue = _read("learning/curriculum/patterns/system-design-patterns-v1.json")
    patterns = {item.get("patternId"): item for item in catalogue.get("patterns", [])}
    adrs = {item.get("adrId"): item for item in catalogue.get("adrs", [])}
    trace = _read(manifest["trace"])
    if len(patterns) != 20 or len(adrs) != 20 or set(adrs) != set(trace.get("adrIds", [])):
        codes.append("I11_ADR_INCOMPLETE")
    for module in modules:
        exercise = module.get("exercise", {})
        pattern = patterns.get(exercise.get("pattern"), {})
        adr = adrs.get(exercise.get("decision"), {})
        expected_adr = {
            "adrId": exercise.get("decision"), "moduleId": module.get("moduleId"),
            "status": "accepted-static-teaching-decision", "alternatives": exercise.get("options"),
            "selectedAlternative": exercise.get("selectedAlternative"),
            "forces": {"stakeholderConcern": module.get("stakeholderConcern"),
                       "nonFunctional": module.get("requirements", {}).get("nonFunctional"),
                       "asr": module.get("requirements", {}).get("asr")},
            "failure": pattern.get("failure"), "verifier": module.get("evidence", {}).get("verifier"),
            "evidenceExpectation": module.get("evidence", {}).get("expected"),
            "consequences": module.get("consequences"), "removalRule": pattern.get("removalRule"),
            "patternId": exercise.get("pattern"), "reciprocalModuleId": module.get("moduleId"),
        }
        option_ids = {option.get("id") for option in exercise.get("options", [])}
        if adr != expected_adr or exercise.get("selectedAlternative") not in option_ids:
            codes.append("I11_ADR_INCOMPLETE")
        if not pattern.get("forces") or not pattern.get("failure") or not pattern.get("verifier") or not pattern.get("consequences") or not pattern.get("removalRule"):
            codes.append("I11_PATTERN_VERIFIER_MISSING")
    promotion = _read(manifest["promotionExample"])
    codes.extend(_codes({"promotion": promotion}))
    if promotion.get("pinnedSchema", {}).get("sha256") != "43fc68833237ef5b522f82fbbd18caba0f11e16bf66e0ff26cf44f0238c39871":
        codes.append("I11_REF_STALE")
    operation_matrix = _read("learning/contracts/operation-matrix-v1.json")
    if len(operation_matrix.get("operations", [])) != 16 or operation_matrix.get("channels") != []:
        codes.append("I11_API_OPERATION_UNRELEASED")
    for path in manifest.get("moduleCollections", []):
        if not _schema_valid(_read(path), "architecture-module-collection-v1.schema.json"):
            codes.append("I11_REF_STALE")
    release = _read("learning/curriculum/release-binding-i5-06-stage-a-v1.json")
    if not _schema_valid(release, "architecture-release-binding-v1.schema.json"):
        codes.append("I11_REF_STALE")
    unique = tuple(dict.fromkeys(codes))
    return CheckResult(ENTRYPOINT_ID, True, unique, {"modules": len(modules), "templates": len(templates), "projectionSha256": content_sha256(manifest)})


def main(argv: Sequence[str] | None = None) -> int:
    result = check_repository()
    print(json.dumps({"entrypointId": result.entrypoint_id, "codes": result.codes, **result.details}, ensure_ascii=False, sort_keys=True))
    return 0 if result.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
