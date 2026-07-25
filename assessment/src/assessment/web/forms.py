"""Small strict form parsers; domain rules remain in framework and engine services."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from assessment.domain.models import EvidenceStatus, validate_identifier

EVIDENCE_STATUSES: tuple[EvidenceStatus, ...] = (
    "Self-reported",
    "Partially evidenced",
    "Evidenced",
    "Conflicting evidence",
    "Not assessed",
)
REVIEW_STATES = ("accept", "defer", "edit-note")


@dataclass(frozen=True)
class AnswerForm:
    question_id: str
    rating: int | None
    evidence_status: EvidenceStatus
    note: str


def parse_revision(value: Any) -> int:
    try:
        revision = int(str(value))
    except (TypeError, ValueError) as error:
        raise ValueError("revision must be an integer") from error
    if revision < 0:
        raise ValueError("revision must not be negative")
    return revision


def parse_answer(
    question_id: Any,
    rating: Any,
    evidence_status: Any,
    note: Any,
    *,
    allowed_question_ids: set[str],
) -> AnswerForm:
    question = validate_identifier(str(question_id))
    if question not in allowed_question_ids:
        raise ValueError("question is not part of the pinned framework")
    status = str(evidence_status)
    if status not in EVIDENCE_STATUSES:
        raise ValueError("evidence status is invalid")
    if status == "Not assessed":
        parsed_rating = None
    else:
        try:
            parsed_rating = int(str(rating))
        except (TypeError, ValueError) as error:
            raise ValueError("rating must be from 0 to 4") from error
        if parsed_rating not in range(5):
            raise ValueError("rating must be from 0 to 4")
    parsed_note = str(note)
    if len(parsed_note) > 4096:
        raise ValueError("answer note exceeds 4096 characters")
    return AnswerForm(
        question_id=question,
        rating=parsed_rating,
        evidence_status=status,  # type: ignore[arg-type]
        note=parsed_note,
    )
