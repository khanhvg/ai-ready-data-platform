"""Fitness-result-v2 verification and promotion decision."""

from __future__ import annotations

import pathlib
import hashlib
from typing import Any

from .canonical import canonical_bytes
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
