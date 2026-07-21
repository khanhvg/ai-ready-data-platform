"""Bounded command and owned-cleanup scaffold."""

from __future__ import annotations

import pathlib
from collections.abc import Sequence

from .schema import LearningContractError


def run_bounded(
    command: Sequence[str],
    *,
    cwd: pathlib.Path,
    timeout: float = 120,
    output_limit: int = 2 * 1024 * 1024,
    max_rss_bytes: int = 512 * 1024 * 1024,
) -> bytes:
    del command, cwd, timeout, output_limit, max_rss_bytes
    raise LearningContractError("LEARNING_RUNTIME_NOT_IMPLEMENTED")


def validate_evidence_locator(root: pathlib.Path, locator: str, sha256: str) -> bytes:
    del root, locator, sha256
    raise LearningContractError("LEARNING_LOCATOR_NOT_IMPLEMENTED")


def cleanup_owned(path: pathlib.Path, marker: dict[str, object]) -> None:
    del path, marker
    raise LearningContractError("LEARNING_CLEANUP_NOT_IMPLEMENTED")
