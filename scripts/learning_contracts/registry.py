"""Version-registry and migration scaffold."""

from __future__ import annotations

from typing import Any

from .schema import LearningContractError


def migrate_document(value: dict[str, Any], target_version: str) -> dict[str, Any]:
    del value, target_version
    raise LearningContractError("LEARNING_MIGRATION_NOT_IMPLEMENTED")
