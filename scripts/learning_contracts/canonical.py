"""I-JSON and RFC 8785 canonicalization scaffold."""

from __future__ import annotations

from typing import Any

from .schema import LearningContractError


def parse_json(raw: bytes) -> Any:
    del raw
    raise LearningContractError("LEARNING_CANONICAL_NOT_IMPLEMENTED")


def canonical_bytes(value: Any) -> bytes:
    del value
    raise LearningContractError("LEARNING_CANONICAL_NOT_IMPLEMENTED")
