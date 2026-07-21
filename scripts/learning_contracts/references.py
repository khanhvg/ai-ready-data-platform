"""Repository-contained reference and prerequisite graph checks."""
from __future__ import annotations

from pathlib import PurePosixPath

from .canonical import ContractError
from .schema import ROOT


def resolve(relative: str) -> object:
    if "://" in relative:
        raise ContractError("REF_REMOTE_FORBIDDEN")
    path = PurePosixPath(relative)
    if path.is_absolute() or any(part in {"", ".", ".."} for part in path.parts):
        raise ContractError("REF_TRAVERSAL_FORBIDDEN")
    target = ROOT.joinpath(*path.parts)
    if not target.is_file() or target.is_symlink():
        raise ContractError("REF_TARGET_MISSING")
    return target


def assert_acyclic(edges: dict[str, list[str]]) -> None:
    visiting: set[str] = set()
    visited: set[str] = set()
    def visit(node: str) -> None:
        if node in visiting:
            raise ContractError("REF_CYCLE")
        if node in visited:
            return
        visiting.add(node)
        for child in edges.get(node, []): visit(child)
        visiting.remove(node); visited.add(node)
    for node in edges: visit(node)
