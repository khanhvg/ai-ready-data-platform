"""Bounded command and owned-cleanup scaffold."""

from __future__ import annotations

import pathlib
from collections.abc import Sequence

from .schema import LearningContractError


def run_bounded(command: Sequence[str], *, cwd: pathlib.Path, timeout: float = 120) -> bytes:
    del command, cwd, timeout
    raise LearningContractError("LEARNING_RUNTIME_NOT_IMPLEMENTED")


def cleanup_owned(path: pathlib.Path, marker: dict[str, object]) -> None:
    del path, marker
    raise LearningContractError("LEARNING_CLEANUP_NOT_IMPLEMENTED")
