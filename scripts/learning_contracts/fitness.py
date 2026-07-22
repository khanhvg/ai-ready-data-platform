"""Fitness-result-v2 verification and promotion decision."""

from __future__ import annotations

import pathlib
import hashlib
from typing import Any

from .canonical import canonical_bytes, parse_json
from .references import resolve_reference
from .schema import LearningContractError, validate_document


def verify_fitness(
    value: dict[str, Any],
    *,
    root: pathlib.Path,
    activation: dict[str, Any] | None = None,
    expected_provenance: dict[str, Any] | None = None,
) -> None:
    try:
        validate_document(value, family="fitness-result")
    except LearningContractError as exc:
        if exc.code == "SCHEMA_INVALID":
            raise LearningContractError("FITNESS_SCHEMA_INVALID") from exc
        raise
    parameters = value["requested"]["parameters"]
    if parameters != sorted(parameters, key=lambda item: item["name"]) or len({item["name"] for item in parameters}) != len(parameters):
        raise LearningContractError("FITNESS_PARAMETER_ORDER_INVALID")
    for field in ("contractHashes", "fixtureHashes", "schemaHashes"):
        rows = value[field]
        if rows != sorted(rows, key=lambda item: (item["name"], item["sha256"])) or len({item["name"] for item in rows}) != len(rows):
            raise LearningContractError("FITNESS_PROVENANCE_ORDER_INVALID")
    if activation is not None:
        if activation.get("schemaVersion") != "command-owner-activation-v1" or value["owner"] != activation.get("owner"):
            raise LearningContractError("FITNESS_ACTIVATION_MISMATCH")
        matching = [
            row for row in activation.get("commands", [])
            if isinstance(row, dict) and row.get("commandId") == value["commandId"]
        ]
        if len(matching) != 1 or matching[0].get("availability") != "implemented" or matching[0].get("evidenceVersion") != "fitness-result-v2":
            raise LearningContractError("FITNESS_ACTIVATION_MISMATCH")
    if expected_provenance is not None:
        for key in (
            "inputSha", "testedTreeSha", "dependencyMergeShas", "contractHashes",
            "fixtureHashes", "schemaHashes", "lockSha256",
        ):
            expected = expected_provenance.get(key)
            actual = value.get(key)
            if key.endswith("Hashes") and isinstance(expected, list) and isinstance(actual, list):
                expected = sorted(expected, key=lambda item: (item["name"], item["sha256"]))
                actual = sorted(actual, key=lambda item: (item["name"], item["sha256"]))
            if actual != expected:
                raise LearningContractError("FITNESS_PROVENANCE_MISMATCH")
    payload = {key: child for key, child in value.items() if key != "payloadSha256"}
    if hashlib.sha256(canonical_bytes(payload)).hexdigest() != value["payloadSha256"]:
        raise LearningContractError("FITNESS_PAYLOAD_TAMPER")
    for item in value["artifacts"]:
        try:
            raw = resolve_reference(root, item["locator"], item["sha256"])
        except LearningContractError as exc:
            raise LearningContractError("FITNESS_ARTIFACT_TAMPER") from exc
        if len(raw) != item["size"]:
            raise LearningContractError("FITNESS_ARTIFACT_TAMPER")


def evaluate_promotion(grains: list[dict[str, Any]]) -> dict[str, Any]:
    if len(grains) != 4 or len({item.get("grain") for item in grains}) != 4:
        raise LearningContractError("PROMOTION_GRAIN_SET_INVALID")
    key_sets = [set(item.get("keys", [])) for item in grains]
    common = set.intersection(*key_sets) if key_sets else set()
    return {
        "decision": "sufficient-evidence/common-grain" if common else "insufficient-evidence/no-common-grain",
        "independentGrainCount": len(grains),
        "commonKeys": sorted(common),
    }


def evaluate_promotion_document(
    value: dict[str, Any] | pathlib.Path,
    *,
    root: pathlib.Path | None = None,
) -> dict[str, Any]:
    """Evaluate the released promotion fixture/manifest document, never a caller-supplied grain verdict."""
    from .schema import read_document
    document = read_document(value, family="promotion-manifest") if isinstance(value, pathlib.Path) else value
    if not isinstance(document, dict):
        raise LearningContractError("PROMOTION_DOCUMENT_INVALID")
    if root is not None:
        for name in ("lesson", "lab", "evidenceSchema", "dataContract", "fixture"):
            reference = document.get(name)
            if not isinstance(reference, dict) or set(reference) != {"path", "sha256"}:
                raise LearningContractError("PROMOTION_DOCUMENT_INVALID")
            raw = resolve_reference(root, reference["path"], reference["sha256"])
            if name == "lesson":
                read_document(root / reference["path"], family="lesson")
            elif name == "lab":
                read_document(root / reference["path"], family="lab")
            elif reference["path"].endswith(".json") and not isinstance(parse_json(raw), dict):
                raise LearningContractError("PROMOTION_DOCUMENT_INVALID")
    grains = document.get("grains")
    if grains is None and isinstance(document.get("sources"), list):
        grains = []
        for source in document["sources"]:
            if not isinstance(source, dict) or set(source) != {"grain", "keys", "document"}:
                raise LearningContractError("PROMOTION_DOCUMENT_INVALID")
            reference = source["document"]
            if root is not None:
                source_document = parse_json(resolve_reference(root, reference["path"], reference["sha256"]))
                required_mart = {
                    "promotion": "mart_promotion_effectiveness",
                    "fulfillment": "mart_fulfillment_performance",
                    "returns": "mart_returns_analysis",
                    "dq": "mart_data_quality",
                }.get(source["grain"])
                marts = source_document.get("marts", []) if isinstance(source_document, dict) else []
                if required_mart is None or required_mart not in {item.get("martId") for item in marts if isinstance(item, dict)}:
                    raise LearningContractError("PROMOTION_DOCUMENT_INVALID")
            grains.append({"grain": source["grain"], "keys": source["keys"]})
    result = evaluate_promotion(grains)
    declared = document.get("decision")
    if declared is not None and declared != result["decision"]:
        raise LearningContractError("PROMOTION_DECISION_MISMATCH")
    return result


def validate_promotion_semantics(value: dict[str, Any], *, expected_fixture_sha256: str) -> None:
    """Validate the released fixture identity and four-independent-grain conclusion."""
    if value.get("fixtureSha256") != expected_fixture_sha256 and "fixtureSha256" in value:
        raise LearningContractError("PROMOTION_FIXTURE_HASH_MISMATCH")
    if value.get("commonGrain") is not None:
        raise LearningContractError("PROMOTION_COMMON_GRAIN_FORBIDDEN")
    if value.get("limitations") == []:
        raise LearningContractError("PROMOTION_LIMITATION_REQUIRED")
