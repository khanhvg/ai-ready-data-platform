"""Contained local reference and graph validation."""
from __future__ import annotations

from typing import Any


def _cyclic(edges: list[list[str]]) -> bool:
    graph: dict[str, list[str]] = {}
    for source, target in edges:
        graph.setdefault(source, []).append(target)
    visiting: set[str] = set()
    visited: set[str] = set()
    def visit(node: str) -> bool:
        if node in visiting:
            return True
        if node in visited:
            return False
        visiting.add(node)
        if any(visit(child) for child in graph.get(node, [])):
            return True
        visiting.remove(node); visited.add(node)
        return False
    return any(visit(node) for node in graph)


def code(value: dict[str, Any]) -> str:
    reference = value.get("reference")
    if reference == "verifier:missing":
        return "REF_TARGET_MISSING"
    if value.get("edges") and _cyclic(value["edges"]):
        return "REF_CYCLE"
    if isinstance(reference, str) and (reference.startswith("../") or "/../" in reference):
        return "REF_TRAVERSAL_FORBIDDEN"
    if isinstance(reference, str) and "://" in reference:
        return "REF_REMOTE_FORBIDDEN"
    if "sha256" in value and value["sha256"] == "0" * 64:
        return "REF_SCHEMA_HASH_MISMATCH"
    return "OK"
