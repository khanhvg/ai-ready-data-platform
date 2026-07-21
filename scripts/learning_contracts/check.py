"""Deterministic entrypoint shared by direct tests and public commands."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any

from . import registry, runtime

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
    return Outcome("BEHAVIOR_NOT_IMPLEMENTED")
