"""Evidence verification scaffold."""

from __future__ import annotations

import pathlib
from typing import Any

from .schema import LearningContractError


def verify_evidence(value: dict[str, Any], *, root: pathlib.Path) -> None:
    del value, root
    raise LearningContractError("LEARNING_EVIDENCE_NOT_IMPLEMENTED")


def verify_manifest(value: dict[str, Any], *, root: pathlib.Path) -> None:
    del value, root
    raise LearningContractError("LEARNING_MANIFEST_NOT_IMPLEMENTED")
