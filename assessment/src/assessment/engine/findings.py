"""Deterministic linked findings and separate architect review records."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal

from assessment.content.markdown import validate_markdown
from assessment.engine.confidence import ConfidenceResult
from assessment.engine.gates import GateResult
from assessment.engine.maturity import MaturityResult
from assessment.engine.priority import PRIORITY_ORDER, select_priority
from assessment.engine.recommendations import resolve_recommendation
from assessment.frameworks import FrameworkBundle

ReviewState = Literal["unreviewed", "accept", "defer", "edit-note"]


@dataclass(frozen=True)
class FindingReview:
    state: ReviewState = "unreviewed"
    edit_note: str = ""


@dataclass(frozen=True)
class Finding:
    id: str
    title: str
    gap: str
    impact: str
    priority: str
    recommendation_id: str
    recommendation: str
    architecture_reference: str
    technology_options: tuple[str, ...]
    demo_reference: str
    evidence_validation_action: str
    source_operand_ids: tuple[str, ...]
    review: FindingReview

    @property
    def generated_truth(self) -> tuple[object, ...]:
        return (
            self.id,
            self.title,
            self.gap,
            self.impact,
            self.priority,
            self.recommendation_id,
            self.recommendation,
            self.architecture_reference,
            self.technology_options,
            self.source_operand_ids,
        )


def _resolve_operand(
    operand_id: str, maturity: MaturityResult, facts: dict[str, Any]
) -> int | bool | None:
    if operand_id.startswith("domain."):
        capability_id = operand_id.removeprefix("domain.")
        return next(
            item.score
            for item in maturity.capabilities
            if item.capability_id == capability_id
        )
    return facts.get(operand_id.removeprefix("fact."))


def _condition(
    condition: dict[str, Any], maturity: MaturityResult, facts: dict[str, Any]
) -> tuple[bool, tuple[str, ...]]:
    if "any" in condition:
        children = [_condition(item, maturity, facts) for item in condition["any"]]
        return any(result for result, _ in children), tuple(
            operand for _, operands in children for operand in operands
        )
    if "all" in condition:
        children = [_condition(item, maturity, facts) for item in condition["all"]]
        return all(result for result, _ in children), tuple(
            operand for _, operands in children for operand in operands
        )
    value = _resolve_operand(condition["operand"], maturity, facts)
    if value is None:
        return False, (condition["operand"],)
    result = (
        value <= condition["threshold"]
        if condition["operator"] == "le"
        else value == condition["threshold"]
    )
    return bool(result), (condition["operand"],)


def _review(
    finding_id: str, reviews: dict[str, dict[str, str]] | None
) -> FindingReview:
    record = (reviews or {}).get(finding_id, {})
    if set(record) - {"state", "edit_note"}:
        raise ValueError(f"finding review {finding_id}: unknown fields")
    state = record.get("state", "unreviewed")
    note = record.get("edit_note", "")
    if not isinstance(state, str) or not isinstance(note, str):
        raise ValueError(
            f"finding review {finding_id}: state and edit_note must be strings"
        )
    if state not in {"unreviewed", "accept", "defer", "edit-note"}:
        raise ValueError(f"finding review {finding_id}: unsupported state {state!r}")
    validate_markdown(note, context=f"finding review {finding_id}")
    return FindingReview(state=state, edit_note=note)  # type: ignore[arg-type]


def generate_findings(
    maturity: MaturityResult,
    confidence: ConfidenceResult,
    gates: GateResult,
    diagnostic_facts: dict[str, Any],
    framework: FrameworkBundle,
    *,
    reviews: dict[str, dict[str, str]] | None = None,
    accepted_target_level: int | None = None,
) -> tuple[Finding, ...]:
    if accepted_target_level not in {None, 4}:
        raise ValueError("accepted target level must be 4 or omitted")
    for finding_id in sorted(reviews or {}):
        _review(finding_id, reviews)
    if maturity.pre_gate_level is None:
        if reviews:
            raise ValueError(
                "finding reviews cannot be linked while maturity is not assessed"
            )
        return ()
    gate_by_id = {trace.rule_id: trace for trace in gates.traces}
    capability_order = {
        capability.capability_id: index
        for index, capability in enumerate(maturity.capabilities)
    }
    fact_capability = {
        fact["id"]: fact["domain_id"] for fact in framework.diagnostic_facts
    }
    findings: list[Finding] = []
    least_assured = confidence.least_assured_assessed_status
    evidence_action = {
        "Conflicting evidence": "Resolve conflicting evidence before relying on this finding.",
        "Self-reported": "Validate self-reported evidence before implementation.",
        "Partially evidenced": "Close partial evidence gaps before implementation.",
        "Evidenced": "Maintain evidence links and refresh them at the next review.",
        None: "Complete the unanswered evidence review.",
    }[least_assured]
    for rule in framework.finding_rules:
        matched, operand_ids = _condition(
            rule["condition"], maturity, diagnostic_facts
        )
        if not matched:
            continue
        recommendation = resolve_recommendation(rule["recommendation_id"], framework)
        gate_id = rule.get("gate_id")
        triggered_gate = bool(
            gate_id is not None
            and gate_id in gate_by_id
            and gate_by_id[gate_id].triggered
        )
        priority_operand = rule.get("priority_operand")
        score_value = (
            _resolve_operand(priority_operand, maturity, diagnostic_facts)
            if priority_operand is not None
            else None
        )
        score = score_value if type(score_value) is int else None
        priority = select_priority(
            score,
            triggered_gate=triggered_gate,
            cross_domain_blocker=rule.get("priority_mode")
            == "cross_domain_blocker",
            target_level_four=accepted_target_level == 4,
        )
        if priority is None:
            continue
        findings.append(
            Finding(
                id=rule["id"],
                title=rule["title"],
                gap=(
                    f"Observed condition for {rule['id']} does not meet the "
                    "target control state."
                ),
                impact=recommendation["impact"],
                priority=priority,
                recommendation_id=recommendation["id"],
                recommendation=recommendation["action"],
                architecture_reference=recommendation["architecture_reference"],
                technology_options=tuple(recommendation["technology_options"]),
                demo_reference=recommendation["demo_reference"],
                evidence_validation_action=evidence_action,
                source_operand_ids=tuple(dict.fromkeys(operand_ids)),
                review=_review(rule["id"], reviews),
            )
        )

    def sort_key(finding: Finding) -> tuple[int, int, str]:
        domain_orders = [
            capability_order[operand.removeprefix("domain.")]
            for operand in finding.source_operand_ids
            if operand.startswith("domain.")
            and operand.removeprefix("domain.") in capability_order
        ]
        domain_orders.extend(
            capability_order[fact_capability[operand.removeprefix("fact.")]]
            for operand in finding.source_operand_ids
            if operand.startswith("fact.")
            and operand.removeprefix("fact.") in fact_capability
        )
        return (
            PRIORITY_ORDER.index(finding.priority),
            min(domain_orders, default=len(capability_order)),
            finding.id,
        )

    generated_ids = {finding.id for finding in findings}
    stale_review_ids = sorted(set(reviews or {}) - generated_ids)
    if stale_review_ids:
        raise ValueError(
            "finding reviews reference findings that were not generated: "
            f"{', '.join(stale_review_ids)}"
        )
    return tuple(sorted(findings, key=sort_key))
