"""Public trace checker entrypoint; semantic rules are added after RED."""

from __future__ import annotations

import json
from pathlib import Path
import re
from typing import Any, Sequence

from .content_io import CheckResult, NormalizedRequest, content_sha256, load_json

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


ROOT = Path(__file__).resolve().parents[3]
EXPECTED_FLOW_STEPS = {
    "CF-LEARNER-FIRST-JOURNEY": ["load", "start", "run", "record-controlled-failure", "diagnose", "reset", "verify", "retain-evidence", "complete"],
    "CF-PUBLISH-STAGE-COMMIT": ["stage-snapshot", "write-object", "validate-object", "commit-catalog-pointer", "verify-read-back"],
    "CF-PUBLISH-RETRY-RESUME": ["detect-partial", "read-commit-state", "resume-idempotently", "verify-pointer", "close-attempt"],
    "CF-CATALOG-INGEST-HANDOFF": ["publish-current-pointer", "open-ingestion-window", "ingest-physical", "ingest-logical", "verify-catalog", "close-window"],
    "CF-OFFICE-OPEN": ["request-open", "admit-budget-capacity", "start-compute", "restore-hydrate", "pass-readiness", "expose-endpoint"],
    "CF-OFFICE-READINESS": ["probe-data-authority", "probe-metadata-authority", "probe-bi-path", "compare-equivalence", "declare-ready"],
    "CF-OFFICE-CLOSE": ["stop-admission", "drain-work", "checkpoint-authorities", "stop-compute", "inventory-residual-state-cost"],
    "CF-RESTORE-OBJECT-CATALOG": ["create-empty-boundary", "restore-objects", "register-catalog", "publish-current-pointer", "verify-table-read"],
    "CF-RESTORE-ANALYTICS": ["restore-clickhouse-authority", "hydrate-query-state", "restore-bi-metadata", "run-equivalence", "record-rto-rpo"],
    "CF-RESTORE-GOVERNANCE": ["restore-db", "restore-search", "reconnect-openmetadata", "reingest-lineage", "verify-owner-classification"],
    "CF-RESTORE-EVIDENCE": ["restore-evidence-index", "verify-payload-hashes", "reconcile-current-state", "reject-stale-completion", "record-recovery-result"],
}


def check_repository() -> CheckResult:
    trace = dict(load_json(ROOT / "learning/curriculum/traces/architecture-trace-v1.json").payload)
    mapping = dict(load_json(ROOT / "learning/curriculum/mappings/local-aws-conceptual-v1.json").payload)
    codes: list[str] = []
    flows = {flow.get("flowId"): flow for flow in trace.get("criticalFlows", [])}
    if set(flows) != set(EXPECTED_FLOW_STEPS): codes.append("I11_CRITICAL_FLOW_COVERAGE_MISSING")
    sources: dict[str, str] = {}
    for view in ("DYN-PUBLISH", "DYN-OFFICE", "DYN-RESTORE"):
        sources[view] = (ROOT / f"architecture/expansions/i5-06/likec4/views/{view}.c4").read_text(encoding="utf-8")
    for flow_id, expected in EXPECTED_FLOW_STEPS.items():
        flow = flows.get(flow_id, {})
        if flow.get("stepIds") != expected or flow.get("dynamicRelations") != expected:
            codes.append("I11_RELATION_ORDER_MISMATCH")
        if not flow.get("deploymentView") or not flow.get("topologyNodes"):
            codes.append("I11_TOPOLOGY_BINDING_MISMATCH")
        if flow.get("dynamicView") in sources:
            tokens = re.findall(rf"\[{re.escape(flow_id)}:([^\]]+)\]", sources[flow["dynamicView"]])
            if tokens != expected: codes.append("I11_RELATION_ORDER_MISMATCH")
    bridges = mapping.get("bridges", [])
    if len(bridges) != 8 or len({item.get("bridgeId") for item in bridges}) != 8:
        codes.append("I11_BRIDGE_MISSING")
    for bridge in bridges:
        if bridge.get("claimClass") != "conceptual-only": codes.append("I11_BRIDGE_RUNTIME_CLAIM")
        if not bridge.get("divergences") or not bridge.get("preservedInvariant"): codes.append("I11_BRIDGE_DIVERGENCE_MISSING")
    spine = trace.get("spine", {})
    if len(spine.get("stages", [])) != 10 or not spine.get("reciprocal") or spine.get("orphanPolicy") != "reject":
        codes.append("I11_TRACE_NONRECIPROCAL")
    unique = tuple(dict.fromkeys(codes))
    return CheckResult(ENTRYPOINT_ID, True, unique, {"flows": len(flows), "bridges": len(bridges), "projectionSha256": content_sha256(trace)})


def main(argv: Sequence[str] | None = None) -> int:
    result = check_repository()
    print(json.dumps({"entrypointId": result.entrypoint_id, "codes": result.codes, **result.details}, ensure_ascii=False, sort_keys=True))
    return 0 if result.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
