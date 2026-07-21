"""Deterministic entrypoint shared by direct tests and public commands."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any

@dataclass(frozen=True)
class Outcome:
    code: str
    pointer: str | None = None
    detail: str = ""

def evaluate(domain: str, value: Any) -> Outcome:
    """Evaluate one contract input through its domain validator."""
    del domain, value
    return Outcome("BEHAVIOR_NOT_IMPLEMENTED")
