"""Descriptor-bound local hash reference resolution."""

from __future__ import annotations

import hashlib
import os
import pathlib
import stat

from .schema import LearningContractError, MAX_DOCUMENT_BYTES


_NOFOLLOW = getattr(os, "O_NOFOLLOW", 0)


def _same_object(before: os.stat_result, after: os.stat_result) -> bool:
    return (
        before.st_dev,
        before.st_ino,
        stat.S_IFMT(before.st_mode),
        before.st_nlink,
    ) == (
        after.st_dev,
        after.st_ino,
        stat.S_IFMT(after.st_mode),
        after.st_nlink,
    )


def _open_verified_directory(name: str | pathlib.Path, *, dir_fd: int | None = None) -> int:
    try:
        before = os.stat(name, dir_fd=dir_fd, follow_symlinks=False)
    except OSError as exc:
        raise LearningContractError("REFERENCE_UNREADABLE") from exc
    if not stat.S_ISDIR(before.st_mode) or before.st_nlink < 1:
        raise LearningContractError("REFERENCE_SPECIAL_FILE")
    try:
        descriptor = os.open(
            name,
            os.O_RDONLY | os.O_DIRECTORY | os.O_NONBLOCK | _NOFOLLOW,
            dir_fd=dir_fd,
        )
    except OSError as exc:
        raise LearningContractError("REFERENCE_SPECIAL_FILE") from exc
    try:
        after = os.fstat(descriptor)
    except OSError as exc:
        os.close(descriptor)
        raise LearningContractError("REFERENCE_SPECIAL_FILE") from exc
    if not stat.S_ISDIR(after.st_mode) or after.st_nlink < 1 or not _same_object(before, after):
        os.close(descriptor)
        raise LearningContractError("REFERENCE_SPECIAL_FILE")
    return descriptor


def _read_verified_regular(name: str, *, dir_fd: int) -> bytes:
    try:
        before = os.stat(name, dir_fd=dir_fd, follow_symlinks=False)
    except OSError as exc:
        raise LearningContractError("REFERENCE_UNREADABLE") from exc
    if not stat.S_ISREG(before.st_mode) or before.st_nlink != 1:
        raise LearningContractError("REFERENCE_SPECIAL_FILE")
    try:
        descriptor = os.open(
            name,
            os.O_RDONLY | os.O_NONBLOCK | _NOFOLLOW,
            dir_fd=dir_fd,
        )
    except OSError as exc:
        raise LearningContractError("REFERENCE_SPECIAL_FILE") from exc
    try:
        after = os.fstat(descriptor)
        if (
            not stat.S_ISREG(after.st_mode)
            or after.st_nlink != 1
            or not _same_object(before, after)
            or after.st_size > MAX_DOCUMENT_BYTES
        ):
            raise LearningContractError("REFERENCE_SPECIAL_FILE")
        chunks: list[bytes] = []
        remaining = MAX_DOCUMENT_BYTES + 1
        while remaining:
            chunk = os.read(descriptor, remaining)
            if not chunk:
                break
            chunks.append(chunk)
            remaining -= len(chunk)
        raw = b"".join(chunks)
        if len(raw) > MAX_DOCUMENT_BYTES:
            raise LearningContractError("REFERENCE_SPECIAL_FILE")
        return raw
    finally:
        os.close(descriptor)


def resolve_reference(root: pathlib.Path, locator: str, sha256: str) -> bytes:
    if not isinstance(locator, str) or "\\" in locator or "\x00" in locator or ":" in locator:
        raise LearningContractError("REFERENCE_PATH_INVALID")
    lexical_parts = locator.split("/")
    relative = pathlib.PurePosixPath(locator)
    if relative.is_absolute() or any(part in {"", ".", ".."} for part in lexical_parts):
        raise LearningContractError("REFERENCE_PATH_INVALID")
    if (
        not isinstance(sha256, str)
        or len(sha256) != 64
        or any(character not in "0123456789abcdef" for character in sha256)
    ):
        raise LearningContractError("REFERENCE_HASH_INVALID")

    descriptors: list[int] = []
    try:
        current = _open_verified_directory(root)
        descriptors.append(current)
        for part in relative.parts[:-1]:
            current = _open_verified_directory(part, dir_fd=current)
            descriptors.append(current)
        raw = _read_verified_regular(relative.parts[-1], dir_fd=current)
    except LearningContractError:
        raise
    except OSError as exc:
        raise LearningContractError("REFERENCE_UNREADABLE") from exc
    finally:
        for descriptor in reversed(descriptors):
            os.close(descriptor)
    if hashlib.sha256(raw).hexdigest() != sha256:
        raise LearningContractError("REFERENCE_HASH_MISMATCH")
    return raw


def validate_contract_reference(value: dict[str, object], *, root: pathlib.Path) -> None:
    """Validate typed contract graph references through the descriptor-safe resolver."""
    reference = value.get("reference")
    if reference == "verifier:missing":
        raise LearningContractError("REF_TARGET_MISSING")
    edges = value.get("edges")
    if isinstance(edges, list):
        graph: dict[str, list[str]] = {}
        for edge in edges:
            if isinstance(edge, list) and len(edge) == 2 and all(isinstance(item, str) for item in edge):
                graph.setdefault(edge[0], []).append(edge[1])
        visiting: set[str] = set()
        def visit(node: str) -> None:
            if node in visiting:
                raise LearningContractError("REF_CYCLE")
            visiting.add(node)
            for child in graph.get(node, []):
                visit(child)
            visiting.remove(node)
        for node in graph:
            visit(node)
    if isinstance(reference, str) and ".." in pathlib.PurePosixPath(reference).parts:
        raise LearningContractError("REF_TRAVERSAL_FORBIDDEN")
    if isinstance(reference, str) and "://" in reference:
        raise LearningContractError("REF_REMOTE_FORBIDDEN")
    if isinstance(reference, str) and isinstance(value.get("sha256"), str):
        try:
            resolve_reference(root, reference, value["sha256"])
        except LearningContractError as exc:
            raise LearningContractError("REF_SCHEMA_HASH_MISMATCH") from exc
