"""Completion-authority scaffold."""

from __future__ import annotations

from typing import Any

from .schema import LearningContractError


def complete(state: dict[str, Any], request: dict[str, Any]) -> dict[str, Any]:
    del state, request
    raise LearningContractError("LEARNING_COMPLETION_NOT_IMPLEMENTED")
