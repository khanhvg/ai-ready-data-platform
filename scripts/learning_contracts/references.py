"""Local hash-bound reference resolution scaffold."""

from __future__ import annotations

import pathlib

from .schema import LearningContractError


def resolve_reference(root: pathlib.Path, locator: str, sha256: str) -> bytes:
    del root, locator, sha256
    raise LearningContractError("LEARNING_REFERENCE_NOT_IMPLEMENTED")
