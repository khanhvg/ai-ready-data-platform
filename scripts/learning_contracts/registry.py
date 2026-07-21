"""Hash-bound Issue #8 registry and command activation rules."""
from __future__ import annotations

from typing import Any

BASE_COMMAND_REGISTRY_SHA = "a94ac86bda0b70643edef9f144a59d8753d91f963b83d22cd510adbc31970e80"


def activation_code(value: dict[str, Any]) -> str:
    if value.get("baseRegistrySha256") != BASE_COMMAND_REGISTRY_SHA:
        return "COMMAND_ACTIVATION_BASE_MISMATCH"
    return "OK"
