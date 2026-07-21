"""Framework-neutral API contract scaffold."""

from __future__ import annotations

from typing import Any

from .schema import LearningContractError


def dispatch(request: dict[str, Any]) -> dict[str, Any]:
    del request
    raise LearningContractError("LEARNING_API_NOT_IMPLEMENTED")


def validate_operation_matrix(value: dict[str, Any]) -> None:
    del value
    raise LearningContractError("LEARNING_OPERATION_MATRIX_NOT_IMPLEMENTED")


def validate_openapi_document(value: dict[str, Any], matrix: dict[str, Any]) -> None:
    del value, matrix
    raise LearningContractError("LEARNING_OPENAPI_NOT_IMPLEMENTED")
