from __future__ import annotations

import copy

import pytest

from assessment.domain.errors import ContentValidationError
from assessment.engine.recommendations import resolve_recommendation
from assessment.frameworks import load_framework


def test_recommendation_requires_resolved_architecture() -> None:
    framework = load_framework("1.0.0")
    recommendation = resolve_recommendation("R-QUALITY", framework)
    assert recommendation["architecture_reference"] == "ARCH-QUALITY-GATE"

    changed = copy.deepcopy(framework)
    changed.architectures.clear()
    with pytest.raises(ContentValidationError, match="unresolved architecture"):
        resolve_recommendation("R-QUALITY", changed)


def test_unknown_recommendation_is_a_contract_error() -> None:
    with pytest.raises(ContentValidationError, match="unresolved recommendation"):
        resolve_recommendation("R-MISSING", load_framework("1.0.0"))
