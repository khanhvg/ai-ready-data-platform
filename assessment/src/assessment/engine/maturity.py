"""Deterministic maturity and coverage aggregation."""

from __future__ import annotations

import math
import statistics
from dataclasses import dataclass
from decimal import Decimal
from typing import Any

from assessment.engine.input import question_ids_by_capability, validate_answer_snapshot
from assessment.frameworks import FrameworkBundle


@dataclass(frozen=True)
class Coverage:
    answered_total: int
    question_total: int
    answered_percent: str
    answered_by_capability: dict[str, int]
    complete: bool


@dataclass(frozen=True)
class CapabilityMaturity:
    capability_id: str
    name: str
    score: int | None
    label: str
    anchor: str | None
    presentation_score: str | None
    answered_count: int
    question_count: int
    source_question_ids: tuple[str, ...]
    source_question_refs: tuple[str, ...]


@dataclass(frozen=True)
class MaturityResult:
    capabilities: tuple[CapabilityMaturity, ...]
    coverage: Coverage
    pre_gate_level: int | None
    pre_gate_label: str
    presentation_score: str | None


def evaluate_maturity(
    answer_document: dict[str, Any], framework: FrameworkBundle
) -> MaturityResult:
    validated = validate_answer_snapshot(answer_document, framework)
    answer_by_id = {answer.question_id: answer for answer in validated.answers}
    answer_index = {
        answer.question_id: index for index, answer in enumerate(validated.answers)
    }
    capabilities: list[CapabilityMaturity] = []
    scores: list[int] = []
    answered_by_capability: dict[str, int] = {}
    minimum_per_domain = int(
        framework.readiness["coverage"]["minimum_answered_per_domain"]
    )
    minimum_total = int(framework.readiness["coverage"]["minimum_answered_total"])
    labels = framework.readiness["levels"]
    question_ids_by_domain = question_ids_by_capability(framework)

    for domain in framework.domains:
        question_ids = question_ids_by_domain[domain["id"]]
        ratings = [
            answer.rating
            for question_id in question_ids
            if (answer := answer_by_id.get(question_id)) is not None
            and answer.rating is not None
        ]
        answered_count = len(ratings)
        answered_by_capability[domain["id"]] = answered_count
        score = (
            int(statistics.median_low(ratings))
            if answered_count >= minimum_per_domain
            else None
        )
        if score is not None:
            scores.append(score)
        capabilities.append(
            CapabilityMaturity(
                capability_id=domain["id"],
                name=domain["name"],
                score=score,
                label=labels[score] if score is not None else "Not assessed",
                anchor=domain["anchors"][score] if score is not None else None,
                presentation_score=(
                    f"{Decimal(score) * Decimal('25'):.1f}"
                    if score is not None
                    else None
                ),
                answered_count=answered_count,
                question_count=len(question_ids),
                source_question_ids=question_ids,
                source_question_refs=tuple(
                    f"assessment/quick.json#/answers/{answer_index[question_id]}"
                    for question_id in question_ids
                    if question_id in answer_index
                ),
            )
        )

    answered_total = sum(answered_by_capability.values())
    complete = answered_total >= minimum_total and all(
        count >= minimum_per_domain for count in answered_by_capability.values()
    )
    coverage = Coverage(
        answered_total=answered_total,
        question_total=len(framework.questions),
        answered_percent=(
            f"{Decimal(answered_total * 100) / Decimal(len(framework.questions)):.1f}"
        ),
        answered_by_capability=answered_by_capability,
        complete=complete,
    )
    if not complete:
        return MaturityResult(
            capabilities=tuple(capabilities),
            coverage=coverage,
            pre_gate_level=None,
            pre_gate_label="Not assessed",
            presentation_score=None,
        )

    pre_gate = math.floor(sum(scores) / len(framework.domains))
    presentation = Decimal(sum(scores)) * Decimal("2.5")
    return MaturityResult(
        capabilities=tuple(capabilities),
        coverage=coverage,
        pre_gate_level=pre_gate,
        pre_gate_label=labels[pre_gate],
        presentation_score=f"{presentation:.1f}",
    )
