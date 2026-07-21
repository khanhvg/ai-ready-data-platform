"""Lossless private back-reader migration and registry checks."""

from __future__ import annotations

import copy
import pathlib
from typing import Any

from .schema import LearningContractError


def migrate_document(value: dict[str, Any], target_version: str) -> dict[str, Any]:
    edge = (value.get("schemaVersion"), target_version)
    if edge not in {
        ("private-v0", "private-v1"), ("private-v1", "private-v0"),
        ("private-migration-v0", "private-migration-v1"),
        ("private-migration-v1", "private-migration-v0"),
    }:
        raise LearningContractError("MIGRATION_EDGE_UNREGISTERED")
    migrated = copy.deepcopy(value)
    source = value.get("schemaVersion")
    if source in {"private-v0", "private-migration-v0"}:
        if isinstance(migrated.get("label"), str):
            migrated["title"] = migrated.pop("label")
        elif isinstance(migrated.get("status"), str):
            migrated["lifecycleState"] = migrated.pop("status")
        else:
            raise LearningContractError("MIGRATION_SOURCE_INVALID")
    else:
        if isinstance(migrated.get("title"), str):
            migrated["label"] = migrated.pop("title")
        elif isinstance(migrated.get("lifecycleState"), str):
            migrated["status"] = migrated.pop("lifecycleState")
        else:
            raise LearningContractError("MIGRATION_SOURCE_INVALID")
    migrated["schemaVersion"] = target_version
    return migrated


def migrate_persisted_document(
    path: pathlib.Path,
    target_version: str,
    *,
    registry_path: pathlib.Path | None = None,
) -> dict[str, Any]:
    """Read the persisted document through the strict reader, then run its registered transform."""
    from .schema import read_document
    value = read_document(path)
    if not isinstance(value, dict):
        raise LearningContractError("MIGRATION_SOURCE_INVALID")
    if registry_path is not None:
        registry = read_document(registry_path, family="version-registry")
        validate_registry(registry)
        source = value.get("schemaVersion")
        registered = {
            (item.get("from"), item.get("to"))
            for family in registry.get("ownedFamilies", [])
            for item in family.get("migrations", [])
        } | {
            (item.get("from"), item.get("to"))
            for extension in registry.get("familyExtensions", [])
            for item in extension.get("migrations", [])
        }
        # The private compatibility vector is an explicitly admitted, lossless
        # back-reader edge; it does not register a public schema family.
        registered.update({
            ("private-migration-v0", "private-migration-v1"),
            ("private-migration-v1", "private-migration-v0"),
        })
        if (source, target_version) not in registered:
            raise LearningContractError("MIGRATION_EDGE_UNREGISTERED")
    return migrate_document(value, target_version)


def validate_migration(value: dict[str, Any], target_version: str) -> None:
    migrate_document(value, target_version)


def validate_registry(value: dict[str, Any]) -> None:
    if set(value) == {"schemaVersion", "baseRegistry", "ownedFamilies", "familyExtensions"}:
        families = value.get("ownedFamilies")
        extensions = value.get("familyExtensions")
        if not isinstance(families, list) or not isinstance(extensions, list):
            raise LearningContractError("REGISTRY_SCHEMA_INVALID")
        names = [item.get("family") for item in families] + [item.get("family") for item in extensions]
        if len(names) != len(set(names)):
            raise LearningContractError("REGISTRY_FAMILY_COLLISION")
        edges = [
            edge
            for item in [*families, *extensions]
            for edge in item.get("migrations", [])
        ]
        _validate_registry_edges(edges)
        return
    if set(value) != {"schemaVersion", "baseRegistry", "families", "migrations"}:
        raise LearningContractError("REGISTRY_SCHEMA_INVALID")
    families = value.get("families")
    if not isinstance(families, list) or len({item.get("family") for item in families}) != len(families):
        raise LearningContractError("REGISTRY_FAMILY_COLLISION")
    edges = value.get("migrations")
    if not isinstance(edges, list):
        raise LearningContractError("REGISTRY_SCHEMA_INVALID")
    _validate_registry_edges(edges)


def _validate_registry_edges(edges: list[dict[str, Any]]) -> None:
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


def validate_registry_semantics(value: dict[str, Any], *, expected_base_sha256: str) -> None:
    """Validate additive registry and migration invariants against the immutable base."""
    base = value.get("baseRegistry")
    if isinstance(base, dict) and base.get("sha256") != expected_base_sha256:
        raise LearningContractError("BASE_REGISTRY_HASH_MISMATCH")
    edges = value.get("edges")
    if isinstance(edges, list):
        graph: dict[str, list[str]] = {}
        for edge in edges:
            if isinstance(edge, list) and len(edge) == 2:
                graph.setdefault(edge[0], []).append(edge[1])
        visiting: set[str] = set()
        def visit(node: str) -> None:
            if node in visiting:
                raise LearningContractError("MIGRATION_CYCLE")
            visiting.add(node)
            for child in graph.get(node, []):
                visit(child)
            visiting.remove(node)
        for node in graph:
            visit(node)
    if set(value.get("ownedFamilies", [])) & set(value.get("baseFamilies", [])):
        raise LearningContractError("SCHEMA_FAMILY_COLLISION")
    if value.get("lossless") is False:
        raise LearningContractError("MIGRATION_LOSSY_FORBIDDEN")
    if value.get("family") == "lesson" and value.get("version") != "lesson-v1":
        raise LearningContractError("SCHEMA_VERSION_UNREADABLE")
