from __future__ import annotations

import argparse
import datetime
import json
import pathlib
import sys
import time
from typing import Any

import jsonschema

from .check_curriculum import CurriculumError, EXPECTED_IDS, ROOT, validate_all
from .content_io import ContentError, emit_evidence, load_json


CATEGORIES = (
    "outcomes", "capabilities", "concerns", "requirements", "options", "views",
    "decisions", "patterns", "implementations", "evidence", "operations", "consequences",
)


class TraceError(ValueError):
    """Stable reciprocal-trace failure."""


def _early_semantic_guards(value: dict[str, Any]) -> None:
    edges = value.get("edges")
    if not isinstance(edges, list) or any(not isinstance(edge, dict) or not edge.get("reciprocalEdgeId") for edge in edges):
        raise TraceError("TRACE_RECIPROCITY_INVALID")
    decisions = value.get("nodes", {}).get("decisions", [])
    if not decisions or any(not node.get("consequenceIds") for node in decisions):
        raise TraceError("TRACE_DECISION_INVALID")
    critical = value.get("criticalFlows")
    if not isinstance(critical, list) or any(not row.get("sequenceViewIds") or not row.get("deploymentViewIds") or not row.get("orderedSteps") for row in critical):
        raise TraceError("TRACE_CRITICAL_FLOW_INVALID")


def validate_trace(root: pathlib.Path = ROOT) -> dict[str, Any]:
    value = load_json(root / "learning/curriculum/traces/architecture-trace-v1.json")
    _early_semantic_guards(value)
    curriculum = validate_all(root)
    schema = load_json(root / "learning/curriculum/contracts/architecture-trace-v1.schema.json")
    errors = sorted(jsonschema.Draft202012Validator(schema).iter_errors(value), key=lambda error: tuple(str(part) for part in error.absolute_path))
    if errors:
        raise TraceError(f"TRACEABILITY_INVALID:{errors[0].json_path}:{errors[0].message}")

    if tuple(value["nodes"]) != CATEGORIES or len(value["traces"]) != 20:
        raise TraceError("TRACEABILITY_INVALID")
    all_nodes: dict[str, dict[str, Any]] = {}
    category_ids: dict[str, set[str]] = {}
    for category in CATEGORIES:
        rows = value["nodes"][category]
        if len(rows) != 20 or tuple(row["moduleId"] for row in rows) != EXPECTED_IDS:
            raise TraceError("TRACEABILITY_INVALID")
        identifiers = {row["id"] for row in rows}
        if len(identifiers) != 20 or identifiers & set(all_nodes):
            raise TraceError("TRACEABILITY_INVALID")
        category_ids[category] = identifiers
        all_nodes.update({row["id"]: row for row in rows})

    traces = {trace["moduleId"]: trace for trace in value["traces"]}
    if tuple(traces) != EXPECTED_IDS or any(trace["id"] != f"trace-{module_id}" for module_id, trace in traces.items()):
        raise TraceError("TRACEABILITY_INVALID")
    edges = {edge["id"]: edge for edge in value["edges"]}
    if len(edges) != 40 or len(edges) != len(value["edges"]):
        raise TraceError("TRACE_RECIPROCITY_INVALID")

    for module_id, trace in traces.items():
        expected_nodes = [value["nodes"][category][EXPECTED_IDS.index(module_id)]["id"] for category in CATEGORIES]
        if trace["nodeIds"] != expected_nodes:
            raise TraceError("TRACEABILITY_INVALID")
        forward = edges.get(trace["forwardPathId"])
        reverse = edges.get(trace["reversePathId"])
        if not forward or not reverse or forward["reciprocalEdgeId"] != reverse["id"] or reverse["reciprocalEdgeId"] != forward["id"]:
            raise TraceError("TRACE_RECIPROCITY_INVALID")
        if forward["direction"] != "forward" or reverse["direction"] != "reverse" or forward["nodeIds"] != expected_nodes or reverse["nodeIds"] != list(reversed(expected_nodes)):
            raise TraceError("TRACE_RECIPROCITY_INVALID")
        path_ids = {forward["id"], reverse["id"]}
        for index, node_id in enumerate(expected_nodes):
            node = all_nodes[node_id]
            if set(node["pathIds"]) != path_ids:
                raise TraceError("TRACE_RECIPROCITY_INVALID")
            neighbours = set()
            if index:
                neighbours.add(expected_nodes[index - 1])
            if index + 1 < len(expected_nodes):
                neighbours.add(expected_nodes[index + 1])
            if set(node["referenceIds"]) != neighbours:
                raise TraceError("TRACE_RECIPROCITY_INVALID")
            if any(node_id not in all_nodes[neighbour]["referenceIds"] for neighbour in neighbours):
                raise TraceError("TRACE_RECIPROCITY_INVALID")

    module_files = ["foundation-v1.json", "junior-v1.json", "data-v1.json", "mid-v1.json"]
    modules = {
        module["id"]: module
        for filename in module_files
        for module in load_json(root / "learning/curriculum/modules" / filename)["modules"]
    }
    pattern_ids = {row["id"] for row in load_json(root / "learning/curriculum/patterns/system-design-patterns-v1.json")["patterns"]}
    view_ids = {
        *(row["id"] for row in load_json(root / "architecture/expansions/i5-06/likec4/view-manifest.yaml")["views"]),
        "C4-L0", "C4-L1", "C4-L2-LOCAL", "C4-L3-RUNNER", "DEP-LOCAL", "DYN-JOURNEY",
    }
    operation_ids = {row["operationId"] for row in load_json(root / "learning/contracts/operation-matrix-v1.json")["operations"]}
    for module_id in EXPECTED_IDS:
        index = EXPECTED_IDS.index(module_id)
        module = modules[module_id]
        content = {category: value["nodes"][category][index]["contentIds"] for category in CATEGORIES}
        unique = lambda values: list(dict.fromkeys(values))
        expected = {
            "outcomes": [module["business"]["outcomeId"]],
            "capabilities": [module["business"]["capabilityId"], module["business"]["valueStreamId"]],
            "concerns": [module["business"]["stakeholderId"], module["business"]["concernId"]],
            "requirements": [*([row["id"] for row in module["requirements"]["fr"]]), *([row["id"] for row in module["requirements"]["nfr"]]), *([row["id"] for row in module["requirements"]["asr"]])],
            "options": [row["id"] for row in module["options"]],
            "views": unique([*module["views"]["c4Ids"], *module["views"]["dataIds"], *module["views"]["integrationIds"], *module["views"]["securityIds"], *module["views"]["deploymentIds"], *module["views"]["dynamicIds"]]),
            "decisions": [module["decision"]["adrId"]],
            "patterns": module["decision"]["patternIds"],
            "implementations": [module["implementation"]["intentId"]],
            "evidence": module["evidence"]["expectationIds"],
            "operations": [module["consequences"]["operationId"]],
            "consequences": [module["consequences"][key] for key in ("resilienceId", "securityId", "costId", "governanceId")],
        }
        if any(content[category] != expected[category] for category in CATEGORIES):
            raise TraceError("TRACEABILITY_INVALID")
        if not set(content["views"]) <= view_ids or not set(content["patterns"]) <= pattern_ids:
            raise TraceError("TRACEABILITY_INVALID")
        openapi = value["nodes"]["operations"][index]["openApiOperationIds"]
        if not openapi or not set(openapi) <= operation_ids:
            raise TraceError("TRACE_OPERATION_INVALID")
        decision = value["nodes"]["decisions"][index]
        if decision["consequenceIds"] != expected["consequences"]:
            raise TraceError("TRACE_DECISION_INVALID")

    critical_by_module = {row["moduleId"]: row for row in value["criticalFlows"]}
    expected_critical = {module_id for module_id, module in modules.items() if module["views"]["criticalFlow"]}
    if set(critical_by_module) != expected_critical:
        raise TraceError("TRACE_CRITICAL_FLOW_INVALID")
    for module_id, row in critical_by_module.items():
        module = modules[module_id]
        if row["sequenceViewIds"] != module["views"]["dynamicIds"] or row["deploymentViewIds"] != module["views"]["deploymentIds"]:
            raise TraceError("TRACE_CRITICAL_FLOW_INVALID")
        if not all(view.startswith("DYN-") for view in row["sequenceViewIds"]) or not all(view.startswith("DEP-") for view in row["deploymentViewIds"]):
            raise TraceError("TRACE_CRITICAL_FLOW_INVALID")

    node_count = len(all_nodes)
    logical_edge_count = sum(len(edge["nodeIds"]) - 1 for edge in edges.values())
    if node_count != 240 or logical_edge_count != 440:
        raise TraceError("TRACEABILITY_INVALID")
    return {
        "schemaVersion": "architecture-trace-validation-v1",
        "moduleCount": curriculum["moduleCount"],
        "nodeCount": node_count,
        "edgeCount": logical_edge_count,
        "pathRecordCount": len(edges),
        "orphanCount": 0,
        "danglingCount": 0,
        "nonReciprocalCount": 0,
        "criticalFlowCount": len(critical_by_module),
        "reciprocal": True,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=pathlib.Path, default=ROOT)
    parser.add_argument("--no-evidence", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    try:
        started_wall = datetime.datetime.now(datetime.timezone.utc)
        started = time.monotonic()
        summary = validate_trace(args.root.resolve())
        if args.json:
            print(json.dumps(summary, sort_keys=True))
        elif args.no_evidence or args.root.resolve() != ROOT:
            print(f"traceability-check: pass nodes={summary['nodeCount']} edges={summary['edgeCount']}")
        else:
            locator = emit_evidence("traceability-check", summary, started_wall, started)
            print(f"EVIDENCE_LOCATOR={locator.as_posix()}")
            print(f"traceability-check: pass nodes={summary['nodeCount']} edges={summary['edgeCount']}")
        return 0
    except (ContentError, CurriculumError, TraceError, jsonschema.ValidationError, OSError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
