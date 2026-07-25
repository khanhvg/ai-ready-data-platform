"""Presentation-only projections over validated catalog models."""

from __future__ import annotations

from typing import Any

from assessment.catalog.models import CatalogBundle, DemoCatalog


def catalog_view(catalog: CatalogBundle) -> dict[str, Any]:
    return {
        "version": catalog.version,
        "capabilities": [item.model_dump(mode="json") for item in catalog.capabilities],
        "architectures": [item.model_dump(mode="json") for item in catalog.architectures],
        "technology_profiles": [
            item.model_dump(mode="json") for item in catalog.technology_profiles
        ],
        "diagrams": [item.model_dump(mode="json") for item in catalog.diagrams],
    }


def demo_view(demo: DemoCatalog) -> dict[str, Any]:
    return {
        "version": demo.version,
        "title": demo.title,
        "presenter_purpose": demo.presenter_purpose,
        "non_scoring_disclaimer": demo.non_scoring_disclaimer,
        "operating_boundary": list(demo.operating_boundary),
        "stage_order": list(demo.stage_order),
        "stages": [item.model_dump(mode="json") for item in demo.stages],
        "evidence_links": [item.model_dump(mode="json") for item in demo.evidence_links],
    }
