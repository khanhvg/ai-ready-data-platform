"""Framework-neutral API contract scaffold."""

from __future__ import annotations

from typing import Any

from .schema import LearningContractError


def dispatch(request: dict[str, Any]) -> dict[str, Any]:
    del request
    raise LearningContractError("LEARNING_API_NOT_IMPLEMENTED")
