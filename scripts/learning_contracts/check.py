"""Deterministic entrypoint shared by direct tests and public commands."""
from __future__ import annotations
from dataclasses import dataclass
import json
import pathlib
from typing import Any

from . import canonical, completion, evidence, fitness, guidance, openapi, references, registry, runtime, schema, state

@dataclass(frozen=True)
class Outcome:
    code: str
    pointer: str | None = None
    detail: str = ""

def evaluate(domain: str, value: Any) -> Outcome:
    """Evaluate one contract input through its domain validator."""
    if domain == "authority":
        return Outcome(runtime.authority_code(value))
    if domain == "dependency":
        return Outcome(runtime.dependency_code(value))
    if domain == "activation":
        return Outcome(registry.activation_code(value))
    if domain == "rollback":
        return Outcome(runtime.rollback_code(value))
    if domain == "schema":
        return Outcome(schema.code(value))
    if domain == "canonical":
        return Outcome(canonical.code(value))
    if domain == "reference":
        return Outcome(references.code(value))
    if domain == "migration":
        return Outcome(registry.migration_code(value))
    if domain == "state":
        return Outcome(state.code(value))
    if domain == "completion":
        return Outcome(completion.code(value))
    if domain == "evidence":
        return Outcome(evidence.code(value))
    if domain == "operation":
        return Outcome(schema.operation_code(value))
    if domain == "openapi":
        return Outcome(openapi.code(value))
    if domain == "guidance":
        return Outcome(guidance.code(value))
    if domain == "promotion":
        return Outcome(guidance.promotion_code(value))
    if domain == "fitness":
        return Outcome(fitness.code(value))
    return Outcome("BEHAVIOR_NOT_IMPLEMENTED")


def release_documents() -> dict[str, Any]:
    """Return the complete immutable Stage A document model."""
    root = pathlib.Path(__file__).resolve().parents[2]
    paths = [
        "learning/contracts/lesson-v1.schema.json", "learning/contracts/lab-v1.schema.json",
        "learning/contracts/progress-v1.schema.json", "learning/contracts/learning-evidence-v1.schema.json",
        "learning/contracts/completion-reconciliation-v1.schema.json", "learning/contracts/operation-matrix-v1.schema.json",
        "learning/contracts/promotion-trust-learning-manifest-v1.schema.json",
        "learning/contracts/learning-contract-version-registry-v1.schema.json",
        "learning/contracts/learning-contract-version-registry-v1.json", "learning/contracts/fitness-result-v2.schema.json",
        "learning/contracts/command-owner-activation-v1.schema.json", "learning/contracts/command-owner-activation-i5-03-v1.json",
        "learning/contracts/learning-contract-set-v1.schema.json", "learning/contracts/learning-contract-set-v1.json",
        "learning/contracts/operation-matrix-v1.json", "learning/contracts/completion-reconciliation-v1.json",
        "learning/lessons/promotion-trust/lesson-v1.json", "learning/labs/promotion-trust/lab-v1.json",
        "learning/manifests/promotion-trust-v1.json", "contracts/openapi/learning-platform-v1.yaml",
        "contracts/openapi/learning-platform-openapi-profile-v1.schema.json",
        "contracts/openapi/learning-platform-problem-details-v1.schema.json",
    ]
    result: dict[str, Any] = {}
    for relative in paths:
        raw = (root / relative).read_bytes()
        if relative.endswith(".yaml"):
            result[relative] = raw
        else:
            result[relative] = json.loads(raw)
    return result


def public_surface() -> tuple[tuple[str, ...], tuple[str, ...]]:
    """Return the registered Make targets and independent valid vectors."""
    return (), ()
