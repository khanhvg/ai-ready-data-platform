"""Confidence distribution and conservative summary independent of maturity."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from assessment.domain.models import EvidenceStatus
from assessment.engine.input import question_ids_by_capability, validate_answer_snapshot
from assessment.frameworks import FrameworkBundle

STATUSES: tuple[EvidenceStatus, ...] = (
    "Self-reported",
    "Partially evidenced",
    "Evidenced",
    "Conflicting evidence",
    "Not assessed",
)
CONSERVATIVE_PRECEDENCE: tuple[EvidenceStatus, ...] = (
    "Conflicting evidence",
    "Self-reported",
    "Partially evidenced",
    "Evidenced",
)


@dataclass(frozen=True)
class CapabilityConfidence:
    capability_id: str
    distribution: dict[str, int]
    least_assured_assessed_status: EvidenceStatus | None
    assessed_count: int
    not_assessed_count: int
    next_action: str
    source_question_ids: tuple[str, ...]


@dataclass(frozen=True)
class ConfidenceResult:
    capabilities: tuple[CapabilityConfidence, ...]
    overall_distribution: dict[str, int]
    least_assured_assessed_status: EvidenceStatus | None


def _distribution(statuses: list[EvidenceStatus]) -> dict[str, int]:
    return {status: statuses.count(status) for status in STATUSES}


def _least_assured(statuses: list[EvidenceStatus]) -> EvidenceStatus | None:
    assessed = [status for status in statuses if status != "Not assessed"]
    return next(
        (status for status in CONSERVATIVE_PRECEDENCE if status in assessed),
        None,
    )


def _next_action(status: EvidenceStatus | None) -> str:
    if status == "Conflicting evidence":
        return "Resolve conflicting evidence before relying on the assessment claim."
    if status == "Self-reported":
        return "Validate the self-reported claim with independent customer evidence."
    if status == "Partially evidenced":
        return "Close the remaining evidence gaps and confirm control operation."
    if status == "Evidenced":
        return "Maintain the evidence links and refresh them at the next review."
    return "Complete the unanswered assessment items before drawing a conclusion."


def summarize_confidence(
    answer_document: dict[str, Any], framework: FrameworkBundle
) -> ConfidenceResult:
    validated = validate_answer_snapshot(answer_document, framework)
    answer_by_id = {answer.question_id: answer for answer in validated.answers}
    capabilities: list[CapabilityConfidence] = []
    all_statuses: list[EvidenceStatus] = []
    question_ids_by_domain = question_ids_by_capability(framework)
    for domain in framework.domains:
        question_ids = question_ids_by_domain[domain["id"]]
        statuses: list[EvidenceStatus] = [
            (
                answer_by_id[question_id].evidence_status
                if question_id in answer_by_id
                else "Not assessed"
            )
            for question_id in question_ids
        ]
        all_statuses.extend(statuses)
        distribution = _distribution(statuses)
        least_assured = _least_assured(statuses)
        capabilities.append(
            CapabilityConfidence(
                capability_id=domain["id"],
                distribution=distribution,
                least_assured_assessed_status=least_assured,
                assessed_count=len(statuses) - distribution["Not assessed"],
                not_assessed_count=distribution["Not assessed"],
                next_action=_next_action(least_assured),
                source_question_ids=question_ids,
            )
        )
    return ConfidenceResult(
        capabilities=tuple(capabilities),
        overall_distribution=_distribution(all_statuses),
        least_assured_assessed_status=_least_assured(all_statuses),
    )
