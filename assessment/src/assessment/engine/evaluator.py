"""Composition root for the pure deterministic engine."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from assessment.engine.confidence import ConfidenceResult, summarize_confidence
from assessment.engine.findings import Finding, generate_findings
from assessment.engine.gates import GateResult, evaluate_gates
from assessment.engine.maturity import MaturityResult, evaluate_maturity
from assessment.frameworks import FrameworkBundle


@dataclass(frozen=True)
class AssessmentResult:
    maturity: MaturityResult
    confidence: ConfidenceResult
    gates: GateResult
    findings: tuple[Finding, ...]


def evaluate_assessment(
    answer_document: dict[str, Any],
    framework: FrameworkBundle,
    *,
    reviews: dict[str, dict[str, str]] | None = None,
    accepted_target_level: int | None = None,
    expected_engagement_id: str | None = None,
) -> AssessmentResult:
    if (
        expected_engagement_id is not None
        and answer_document.get("engagement_id") != expected_engagement_id
    ):
        raise ValueError("engagement and answer snapshot IDs differ")
    maturity = evaluate_maturity(answer_document, framework)
    confidence = summarize_confidence(answer_document, framework)
    facts = answer_document.get("diagnostic_facts", {})
    gates = evaluate_gates(maturity, facts, framework)
    findings = generate_findings(
        maturity,
        confidence,
        gates,
        facts,
        framework,
        reviews=reviews,
        accepted_target_level=accepted_target_level,
    )
    return AssessmentResult(
        maturity=maturity,
        confidence=confidence,
        gates=gates,
        findings=findings,
    )
