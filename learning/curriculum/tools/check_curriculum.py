"""Public curriculum checker entrypoint; semantic rules are added after RED."""

from __future__ import annotations

from typing import Any

from .content_io import CheckResult, NormalizedRequest, content_sha256

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
