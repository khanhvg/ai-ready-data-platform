"""Prerequisite and hint scaffold."""

from __future__ import annotations

from typing import Any

from .schema import LearningContractError


def evaluate_guidance(state: dict[str, Any], request: dict[str, Any]) -> dict[str, Any]:
    del state, request
    raise LearningContractError("LEARNING_GUIDANCE_NOT_IMPLEMENTED")
