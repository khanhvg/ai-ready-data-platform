"""Stable recommendation and architecture resolution."""

from __future__ import annotations

from typing import Any

from assessment.domain.errors import ContentValidationError
from assessment.frameworks import FrameworkBundle


def resolve_recommendation(
    recommendation_id: str, framework: FrameworkBundle
) -> dict[str, Any]:
    recommendation = next(
        (item for item in framework.recommendations if item["id"] == recommendation_id),
        None,
    )
    if recommendation is None:
        raise ContentValidationError(
            f"finding: unresolved recommendation {recommendation_id!r}"
        )
    architecture_id = recommendation["architecture_reference"]
    if not any(item["id"] == architecture_id for item in framework.architectures):
        raise ContentValidationError(
            f"recommendation {recommendation_id}: unresolved architecture {architecture_id!r}"
        )
    return recommendation
