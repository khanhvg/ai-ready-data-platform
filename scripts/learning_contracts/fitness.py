"""Activation-bound fitness-result-v2 construction and validation."""
from __future__ import annotations

from typing import Any

COMMANDS = {"learning-contracts-check", "lesson-check", "api-contracts-check", "evidence-verify"}


def code(value: dict[str, Any]) -> str:
    if value.get("schemaVersion") != "fitness-result-v2":
        return "FITNESS_RESULT_OWNER_VERSION_MISMATCH"
    if value.get("owner") != "I5-03" or value.get("commandId") not in COMMANDS:
        return "FITNESS_RESULT_OWNER_VERSION_MISMATCH"
    if value.get("activeEvidenceVersion", "fitness-result-v2") != "fitness-result-v2":
        return "FITNESS_RESULT_OWNER_VERSION_MISMATCH"
    return "OK"
