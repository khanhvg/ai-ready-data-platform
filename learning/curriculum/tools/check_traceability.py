"""Public trace checker entrypoint; semantic rules are added after RED."""

from __future__ import annotations

import json
from pathlib import Path
import re
from typing import Any, Sequence
from jsonschema import Draft202012Validator
import yaml

from .content_io import CheckResult, NormalizedRequest, admitted_runtime_ok, content_sha256, load_json

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


def _relations(path: Path, flow_id: str, expected: list[str]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source, target, label in re.findall(r"^\s*([A-Za-z0-9_.]+) -> ([A-Za-z0-9_.]+) '([^']+)'", path.read_text(encoding="utf-8"), re.MULTILINE):
        token = re.search(r"\[([^:]+):([^\]]+)\]", label)
        if flow_id == "CF-LEARNER-FIRST-JOURNEY":
            step_id = expected[len(rows)] if len(rows) < len(expected) else "unexpected"
        elif token and token.group(1) == flow_id:
            step_id = token.group(2)
        else:
            continue
        rows.append({"ordinal": len(rows) + 1, "stepId": step_id, "sourceId": source, "targetId": target,
                     "labelVi": re.sub(r"\s*\[[^\]]+\]$", "", label), "technology": None})
    return rows


def _deployment_nodes(path: Path) -> set[str]:
    text = path.read_text(encoding="utf-8")
    declarations = re.findall(r"\b(?:environment|host|privateStorage)\s+([A-Za-z0-9_]+)", text)
    instances = re.findall(r"^\s*([A-Za-z0-9_]+)\s*=\s*instanceOf\b", text, re.MULTILINE)
    return set(declarations + instances)


def check_repository() -> CheckResult:
    trace = dict(load_json(ROOT / "learning/curriculum/traces/architecture-trace-v1.json").payload)
    mapping = dict(load_json(ROOT / "learning/curriculum/mappings/local-aws-conceptual-v1.json").payload)
    codes: list[str] = []
    if not admitted_runtime_ok(): codes.append("I11_RESOURCE_OWNERSHIP")
    trace_schema = dict(load_json(ROOT / "learning/curriculum/contracts/architecture-trace-v1.schema.json").payload)
    if list(Draft202012Validator(trace_schema).iter_errors(trace)): codes.append("I11_REF_STALE")
    view_schema = dict(load_json(ROOT / "learning/curriculum/contracts/architecture-view-extension-v1.schema.json").payload)
    view_manifest = yaml.safe_load((ROOT / "architecture/expansions/i5-06/likec4/view-manifest.yaml").read_text(encoding="utf-8"))
    if list(Draft202012Validator(view_schema).iter_errors(view_manifest)): codes.append("I11_REF_STALE")
    flows = {flow.get("flowId"): flow for flow in trace.get("criticalFlows", [])}
    if set(flows) != set(EXPECTED_FLOW_STEPS): codes.append("I11_CRITICAL_FLOW_COVERAGE_MISSING")
    view_paths = {
        "DYN-JOURNEY": ROOT / "architecture/likec4/views/DYN-JOURNEY.c4",
        **{view: ROOT / f"architecture/expansions/i5-06/likec4/views/{view}.c4" for view in ("DYN-PUBLISH", "DYN-OFFICE", "DYN-RESTORE")},
    }
    deployment_nodes = {
        "DEP-LOCAL": _deployment_nodes(ROOT / "architecture/likec4/model/local-deployment.c4"),
        "DEP-AWS": _deployment_nodes(ROOT / "architecture/expansions/i5-06/likec4/model/architecture-curriculum.c4"),
    }
    for flow_id, expected in EXPECTED_FLOW_STEPS.items():
        flow = flows.get(flow_id, {})
        actual_relations = _relations(view_paths.get(flow.get("dynamicView"), Path("missing")), flow_id, expected) if flow.get("dynamicView") in view_paths else []
        if flow.get("stepIds") != expected or flow.get("dynamicRelations") != actual_relations:
            codes.append("I11_RELATION_ORDER_MISMATCH")
        topology = flow.get("topology", {})
        admitted_nodes = deployment_nodes.get(flow.get("deploymentView"), set())
        placements = topology.get("endpointPlacements", {})
        expected_edges = [
            {"ordinal": row["ordinal"], "stepId": row["stepId"],
             "sourceNode": placements.get(row["sourceId"]), "targetNode": placements.get(row["targetId"])}
            for row in actual_relations
        ]
        endpoints = {value for row in actual_relations for value in (row["sourceId"], row["targetId"])}
        if (
            set(topology.get("nodes", [])) != admitted_nodes
            or set(placements) != endpoints or not set(placements.values()).issubset(admitted_nodes)
            or topology.get("edges") != expected_edges
            or not set(topology.get("trustBoundaryNodes", [])).issubset(admitted_nodes)
            or not set(topology.get("failureNodes", [])).issubset(admitted_nodes)
        ):
            codes.append("I11_TOPOLOGY_BINDING_MISMATCH")
    bridges = mapping.get("bridges", [])
    if len(bridges) != 8 or len({item.get("bridgeId") for item in bridges}) != 8:
        codes.append("I11_BRIDGE_MISSING")
    trace_relation_bindings = {
        f"{flow['flowId']}:{relation['stepId']}"
        for flow in flows.values() for relation in flow.get("dynamicRelations", [])
    }
    source_relation_bindings = {
        token for path in view_paths.values() if path.is_file()
        for token in re.findall(r"\[([A-Z0-9-]+:[a-z0-9-]+)\]", path.read_text(encoding="utf-8"))
    }
    for bridge in bridges:
        if bridge.get("claimClass") != "conceptual-only": codes.append("I11_BRIDGE_RUNTIME_CLAIM")
        if not bridge.get("divergences") or not bridge.get("preservedInvariant"): codes.append("I11_BRIDGE_DIVERGENCE_MISSING")
        topology = bridge.get("topologyBindings", {})
        if topology.get("sourceNode") not in deployment_nodes["DEP-LOCAL"] or topology.get("targetNode") not in deployment_nodes["DEP-AWS"]:
            codes.append("I11_TOPOLOGY_BINDING_MISMATCH")
        relation_bindings = bridge.get("relationBindings", [])
        if not relation_bindings or len(relation_bindings) != len(set(relation_bindings)) or not set(relation_bindings).issubset(trace_relation_bindings & source_relation_bindings):
            codes.append("I11_BRIDGE_MISSING")
    module_documents = [
        module for path in sorted((ROOT / "learning/curriculum/modules").glob("*.json"))
        for module in dict(load_json(path).payload).get("modules", [])
    ]
    trace_bindings = {row.get("moduleId"): row for row in trace.get("moduleTraceBindings", [])}
    for module in module_documents:
        expected_binding = {
            "moduleId": module["moduleId"], "moduleSha256": content_sha256(module),
            "businessOutcomeSha256": content_sha256(module["businessOutcome"]), "capabilitySha256": content_sha256(module["capability"]),
            "stakeholderConcernSha256": content_sha256(module["stakeholderConcern"]), "requirementsSha256": content_sha256(module["requirements"]),
            "optionsSha256": content_sha256(module["exercise"]["options"]), "viewIds": module["exercise"]["requiredViews"],
            "adrId": module["exercise"]["decision"], "patternId": module["exercise"]["pattern"],
            "implementationIntentSha256": content_sha256(module["exercise"]["implementationIntent"]),
            "verifier": module["evidence"]["verifier"], "consequencesSha256": content_sha256(module["consequences"]),
            "reciprocalModuleId": module["moduleId"],
        }
        if trace_bindings.get(module["moduleId"]) != expected_binding: codes.append("I11_TRACE_NONRECIPROCAL")
    if set(trace_bindings) != {module["moduleId"] for module in module_documents}: codes.append("I11_TRACE_NONRECIPROCAL")
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
