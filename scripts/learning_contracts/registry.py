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
    if "version" in value and value["version"] not in {"v1", "v2"}:
        return "SCHEMA_VERSION_UNREADABLE"
    if value.get("lossless") is False:
        return "MIGRATION_LOSSY_FORBIDDEN"
    edges = value.get("edges", [])
    if edges:
        graph = {source: target for source, target in edges}
        for origin in graph:
            seen: set[str] = set()
            node = origin
            while node in graph:
                if node in seen:
                    return "MIGRATION_CYCLE"
                seen.add(node); node = graph[node]
    if set(value.get("ownedFamilies", [])).intersection(value.get("baseFamilies", [])):
        return "SCHEMA_FAMILY_COLLISION"
    if "readableVersions" in value and not set(value["readableVersions"]).issubset(value.get("readers", [])):
        return "SCHEMA_VERSION_UNREADABLE"
    return "OK"
