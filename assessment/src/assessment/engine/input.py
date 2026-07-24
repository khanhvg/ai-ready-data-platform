"""Validation shared by pure engine services."""

from __future__ import annotations

from typing import Any

from assessment.domain.errors import ContentValidationError
from assessment.domain.models import AnswerEvidenceDocument
from assessment.frameworks import FrameworkBundle

FACT_TYPES: dict[str, type[int] | type[bool]] = {
    "privacy_control_level": int,
    "ownership_control_level": int,
    "critical_lineage": bool,
    "reproducible_versioned": bool,
}


def question_ids_by_capability(
    framework: FrameworkBundle,
) -> dict[str, tuple[str, ...]]:
    """Group question IDs once while preserving framework order."""
    grouped: dict[str, list[str]] = {
        domain["id"]: [] for domain in framework.domains
    }
    for question in framework.questions:
        grouped[question["domain_id"]].append(question["id"])
    return {
        capability_id: tuple(question_ids)
        for capability_id, question_ids in grouped.items()
    }


def validate_answer_snapshot(
    answer_document: dict[str, Any], framework: FrameworkBundle
) -> AnswerEvidenceDocument:
    validated = AnswerEvidenceDocument.model_validate(answer_document)
    if validated.framework_version != framework.version:
        raise ContentValidationError("answer snapshot and framework versions differ")
    question_ids = [answer.question_id for answer in validated.answers]
    if len(question_ids) != len(set(question_ids)):
        raise ContentValidationError("answer snapshot contains duplicate question IDs")
    allowed = {question["id"] for question in framework.questions}
    unknown = sorted(set(question_ids) - allowed)
    if unknown:
        raise ContentValidationError(
            f"answer snapshot contains unknown question IDs: {', '.join(unknown)}"
        )
    facts = validated.diagnostic_facts
    unknown_facts = sorted(set(facts) - set(FACT_TYPES))
    if unknown_facts:
        raise ContentValidationError(
            f"answer snapshot contains unknown diagnostic facts: {', '.join(unknown_facts)}"
        )
    missing_facts = sorted(set(FACT_TYPES) - set(facts))
    if missing_facts:
        raise ContentValidationError(
            "answer snapshot is missing required diagnostic facts: "
            f"{', '.join(missing_facts)}"
        )
    for fact_id in FACT_TYPES:
        value = facts[fact_id]
        if value is None:
            raise ContentValidationError(
                f"required diagnostic fact {fact_id} must be answered"
            )
        expected = FACT_TYPES[fact_id]
        if type(value) is not expected:
            raise ContentValidationError(
                f"diagnostic fact {fact_id} must be {expected.__name__} or null"
            )
        if fact_id in {"privacy_control_level", "ownership_control_level"} and (
            type(value) is not int or not 0 <= value <= 4
        ):
            raise ContentValidationError(
                f"diagnostic fact {fact_id} must be from 0 to 4"
            )
    return validated
