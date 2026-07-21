"""One-authority learning state scaffold."""

from __future__ import annotations

from typing import Any

from .schema import LearningContractError


def execute_operation(state: dict[str, Any], request: dict[str, Any]) -> dict[str, Any]:
    del state, request
    raise LearningContractError("LEARNING_STATE_NOT_IMPLEMENTED")
