"""Hash-bound Issue #8 registry and command activation rules."""
from __future__ import annotations

from typing import Any

BASE_COMMAND_REGISTRY_SHA = "a94ac86bda0b70643edef9f144a59d8753d91f963b83d22cd510adbc31970e80"
BASE_SCHEMA_REGISTRY_SHA = "8e18588f63b5d99c0b60a229758575e8badf0f055bfcb4f89908f9fa2684a57e"


def activation_code(value: dict[str, Any]) -> str:
    if value.get("baseRegistrySha256") != BASE_COMMAND_REGISTRY_SHA:
        return "COMMAND_ACTIVATION_BASE_MISMATCH"
    return "OK"


def migration_code(value: dict[str, Any]) -> str:
    base = value.get("baseRegistry")
    if isinstance(base, dict) and base.get("sha256") != BASE_SCHEMA_REGISTRY_SHA:
        return "BASE_REGISTRY_HASH_MISMATCH"
    return "BEHAVIOR_NOT_IMPLEMENTED"
