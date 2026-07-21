"""Lossless private back-reader migration and registry checks."""

from __future__ import annotations

import copy
from typing import Any

from .schema import LearningContractError


def migrate_document(value: dict[str, Any], target_version: str) -> dict[str, Any]:
    edge = (value.get("schemaVersion"), target_version)
    if edge not in {("private-v0", "private-v1"), ("private-v1", "private-v0")}:
        raise LearningContractError("MIGRATION_EDGE_UNREGISTERED")
    migrated = copy.deepcopy(value)
    migrated["schemaVersion"] = target_version
    return migrated


def validate_registry(value: dict[str, Any]) -> None:
    if set(value) != {"schemaVersion", "baseRegistry", "families", "migrations"}:
        raise LearningContractError("REGISTRY_SCHEMA_INVALID")
    families = value.get("families")
    if not isinstance(families, list) or len({item.get("family") for item in families}) != len(families):
        raise LearningContractError("REGISTRY_FAMILY_COLLISION")
    edges = value.get("migrations")
    if not isinstance(edges, list):
        raise LearningContractError("REGISTRY_SCHEMA_INVALID")
    graph: dict[str, list[str]] = {}
    for item in edges:
        if item.get("kind") not in {"identity", "lossless"}:
            raise LearningContractError("MIGRATION_LOSSY")
        if item.get("from") != item.get("to"):
            graph.setdefault(item["from"], []).append(item["to"])
    visiting: set[str] = set()
    visited: set[str] = set()
    def visit(node: str) -> None:
        if node in visiting:
            raise LearningContractError("MIGRATION_CYCLE")
        if node in visited:
            return
        visiting.add(node)
        for child in graph.get(node, []):
            visit(child)
        visiting.remove(node)
        visited.add(node)
    for node in graph:
        visit(node)
