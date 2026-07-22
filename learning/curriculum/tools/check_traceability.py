"""Public trace checker entrypoint; semantic rules are added after RED."""

from __future__ import annotations

from typing import Any

from .content_io import CheckResult, NormalizedRequest, content_sha256

ENTRYPOINT_ID = "I11-EP-TRACE"


def _codes(payload: dict[str, Any]) -> list[str]:
    codes: list[str] = []
    if trace := payload.get("trace"):
        stages = trace.get("stages", [])
        expected = [f"{left}>{right}" for left, right in zip(stages, stages[1:])]
        if trace.get("edges") != expected: codes.append("I11_TRACE_GAP")
        if not trace.get("reciprocal"): codes.append("I11_TRACE_NONRECIPROCAL")
    if bridge := payload.get("bridge"):
        if not bridge.get("present"): codes.append("I11_BRIDGE_MISSING")
        if not bridge.get("divergences"): codes.append("I11_BRIDGE_DIVERGENCE_MISSING")
        if bridge.get("claimClass") != "conceptual-only" or bridge.get("usedForRuntime"):
            codes.append("I11_BRIDGE_RUNTIME_CLAIM")
    if relation := payload.get("relationOrder"):
        if relation.get("steps") != relation.get("dynamicRelations"):
            codes.append("I11_RELATION_ORDER_MISMATCH")
    if topology := payload.get("topology"):
        admitted = set(topology.get("deploymentNodes", [])) | set(topology.get("bridgeNodes", []))
        if not set(topology.get("relationEndpoints", [])).issubset(admitted):
            codes.append("I11_TOPOLOGY_BINDING_MISMATCH")
    return codes


def run(request: NormalizedRequest) -> CheckResult:
    projection: dict[str, Any] = {"trace": request.payload, "sourceClass": request.source.split(":", 1)[0]}
    return CheckResult(ENTRYPOINT_ID, True, tuple(_codes(dict(request.payload))), {"projectionSha256": content_sha256(projection)})
