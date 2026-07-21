"""Descriptor-bound local hash reference resolution."""

from __future__ import annotations

import pathlib
import hashlib
import stat

from .schema import LearningContractError, read_regular_bytes


def resolve_reference(root: pathlib.Path, locator: str, sha256: str) -> bytes:
    if not isinstance(locator, str) or "\\" in locator or "\x00" in locator or "://" in locator:
        raise LearningContractError("REFERENCE_PATH_INVALID")
    relative = pathlib.PurePosixPath(locator)
    if relative.is_absolute() or not relative.parts or any(part in {"", ".", ".."} for part in relative.parts):
        raise LearningContractError("REFERENCE_PATH_INVALID")
    if not isinstance(sha256, str) or len(sha256) != 64:
        raise LearningContractError("REFERENCE_HASH_INVALID")
    path = root.joinpath(*relative.parts)
    try:
        root_info = root.lstat()
        if not stat.S_ISDIR(root_info.st_mode) or stat.S_ISLNK(root_info.st_mode):
            raise LearningContractError("REFERENCE_SPECIAL_FILE")
        cursor = root
        for part in relative.parts[:-1]:
            cursor = cursor / part
            info = cursor.lstat()
            if not stat.S_ISDIR(info.st_mode) or stat.S_ISLNK(info.st_mode):
                raise LearningContractError("REFERENCE_SPECIAL_FILE")
    except OSError as exc:
        raise LearningContractError("REFERENCE_UNREADABLE") from exc
    try:
        raw = read_regular_bytes(path)
    except LearningContractError as exc:
        if exc.code == "DOCUMENT_SPECIAL_FILE":
            raise LearningContractError("REFERENCE_SPECIAL_FILE") from exc
        raise LearningContractError("REFERENCE_UNREADABLE") from exc
    if hashlib.sha256(raw).hexdigest() != sha256:
        raise LearningContractError("REFERENCE_HASH_MISMATCH")
    return raw
