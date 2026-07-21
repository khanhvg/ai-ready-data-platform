"""Deterministic entrypoint shared by direct tests and public commands."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any

from . import canonical, completion, references, registry, runtime, schema, state

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
    return Outcome("BEHAVIOR_NOT_IMPLEMENTED")
