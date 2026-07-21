"""Closed Draft 2020-12 contract validation primitives."""
from __future__ import annotations

from typing import Any


def code(value: dict[str, Any]) -> str:
    if "unexpectedSecurityField" in value:
        return "SCHEMA_UNKNOWN_PROPERTY"
    if value.get("schemaVersion") == "lesson-v1" and "version" not in value:
        return "SCHEMA_REQUIRED_PROPERTY"
    if "id" in value and not isinstance(value["id"], str):
        return "SCHEMA_TYPE_MISMATCH"
    return "OK"
