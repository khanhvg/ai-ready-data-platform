"""Build canonical report JSON from immutable source snapshots."""

from __future__ import annotations

import hashlib
from dataclasses import asdict
from typing import Any

from assessment.content.markdown import validate_markdown
from assessment.domain.models import (
    REPORT_SECTION_IDS,
    Engagement,
    Report,
)
from assessment.engine.evaluator import AssessmentResult, evaluate_assessment
from assessment.frameworks import load_framework
from assessment.reporting.models import GeneratedReport
from assessment.storage.hygiene import scan_bytes, scan_json_keys
from assessment.storage.local import canonical_json

PROVENANCE_CLASSES = (
    "customer answer",
    "customer evidence",
    "architect judgment",
    "demo illustration",
)
SOURCE_STATE_KEYS = {
    "engagement.json",
    "findings/review.json",
    "selections/deep-dives.json",
}
SOURCE_STATE_PREFIXES = ("assessment/", "evidence/")


def canonical_source_state(
    engagement_document: dict[str, Any],
    answer_document: dict[str, Any],
    reviews: dict[str, dict[str, str]],
    source_snapshot: dict[str, str] | None = None,
) -> dict[str, Any]:
    """Return only inputs that may legitimately influence a generated report."""
    source_files = {
        key: digest
        for key, digest in sorted((source_snapshot or {}).items())
        if key in SOURCE_STATE_KEYS or key.startswith(SOURCE_STATE_PREFIXES)
    }
    return {
        "engagement": engagement_document,
        "answers": answer_document,
        "reviews": reviews,
        "source_files": source_files,
    }


def source_state_digest(
    engagement_document: dict[str, Any],
    answer_document: dict[str, Any],
    reviews: dict[str, dict[str, str]],
    source_snapshot: dict[str, str] | None = None,
) -> str:
    return hashlib.sha256(
        canonical_json(
            canonical_source_state(
                engagement_document,
                answer_document,
                reviews,
                source_snapshot,
            )
        )
    ).hexdigest()


def _validate_source(
    engagement_document: dict[str, Any],
    answer_document: dict[str, Any],
    reviews: dict[str, dict[str, str]],
    source_snapshot: dict[str, str] | None,
) -> tuple[Engagement, str]:
    engagement = Engagement.model_validate(engagement_document)
    if answer_document.get("engagement_id") != engagement.engagement_id:
        raise ValueError("engagement and answer snapshot IDs differ")
    for answer in answer_document.get("answers", []):
        note = answer.get("note")
        if isinstance(note, str):
            validate_markdown(note, context=f"answer {answer.get('question_id')} note")
    for finding_id, review in reviews.items():
        if set(review) - {"state", "edit_note"}:
            raise ValueError(f"finding review {finding_id}: unknown fields")
        state = review.get("state", "unreviewed")
        note = review.get("edit_note", "")
        if not isinstance(state, str) or not isinstance(note, str):
            raise ValueError(
                f"finding review {finding_id}: state and edit_note must be strings"
            )
        validate_markdown(note, context=f"finding review {finding_id}")
    source = canonical_source_state(
        engagement_document,
        answer_document,
        reviews,
        source_snapshot,
    )
    source_bytes = canonical_json(source)
    scan_bytes(source_bytes, context="report source state")
    scan_json_keys(source, context="report source state")
    return engagement, hashlib.sha256(source_bytes).hexdigest()


def _capability_items(result: AssessmentResult) -> list[dict[str, Any]]:
    confidence = {
        item.capability_id: item for item in result.confidence.capabilities
    }
    return [
        {
            "capability_id": item.capability_id,
            "name": item.name,
            "score": item.score,
            "label": item.label,
            "anchor": item.anchor,
            "presentation_score": item.presentation_score,
            "answered_count": item.answered_count,
            "question_count": item.question_count,
            "source_question_ids": list(item.source_question_ids),
            "source_question_refs": list(item.source_question_refs),
            "confidence": asdict(confidence[item.capability_id]),
            "provenance_class": "customer answer",
        }
        for item in result.maturity.capabilities
    ]


def _finding_items(result: AssessmentResult) -> list[dict[str, Any]]:
    return [
        {
            "id": finding.id,
            "title": finding.title,
            "gap": finding.gap,
            "impact": finding.impact,
            "priority": finding.priority,
            "recommendation_id": finding.recommendation_id,
            "recommendation": finding.recommendation,
            "architecture_reference": finding.architecture_reference,
            "technology_options": list(finding.technology_options),
            "demo_reference": finding.demo_reference,
            "evidence_validation_action": finding.evidence_validation_action,
            "source_operand_ids": list(finding.source_operand_ids),
            "generated_truth_preserved": True,
            "architect_review": asdict(finding.review),
            "provenance_class": "architect judgment",
            "demo_provenance_class": "demo illustration",
        }
        for finding in result.findings
    ]


def generate_report(
    engagement_document: dict[str, Any],
    answer_document: dict[str, Any],
    *,
    reviews: dict[str, dict[str, str]] | None = None,
    source_snapshot: dict[str, str] | None = None,
) -> GeneratedReport:
    review_records = reviews or {}
    engagement, source_digest = _validate_source(
        engagement_document,
        answer_document,
        review_records,
        source_snapshot,
    )
    framework = load_framework(engagement.framework_version)
    result = evaluate_assessment(
        answer_document,
        framework,
        reviews=review_records,
    )
    capabilities = _capability_items(result)
    findings = _finding_items(result)
    blockers = [
        finding for finding in findings if finding["priority"] == "Critical blocker"
    ]
    organization = str(
        engagement_document.get("organization_name", engagement.engagement_id)
    )
    sections_by_id: dict[str, dict[str, Any]] = {
        "executive-summary": {
            "organization": organization,
            "statement": (
                f"Final readiness is {result.gates.final_level} — "
                f"{result.gates.final_label}. Capability maturity is authoritative; "
                "the normalized value is presentation-only."
                if result.gates.final_level is not None
                else (
                    "Overall readiness is Not assessed because configured coverage "
                    "requirements are not met."
                )
            ),
            "provenance_class": "architect judgment",
        },
        "readiness": {
            "pre_gate_level": result.maturity.pre_gate_level,
            "pre_gate_label": result.maturity.pre_gate_label,
            "final_level": result.gates.final_level,
            "final_label": result.gates.final_label,
            "presentation_score": result.maturity.presentation_score,
            "selected_cap": result.gates.selected_cap,
            "selected_rule_ids": list(result.gates.selected_rule_ids),
            "provenance_class": "customer answer",
        },
        "capability-heatmap": {"items": capabilities},
        "gates": {"items": [asdict(trace) for trace in result.gates.traces]},
        "confidence": {
            "items": [asdict(item) for item in result.confidence.capabilities],
            "overall_distribution": result.confidence.overall_distribution,
            "least_assured_assessed_status": (
                result.confidence.least_assured_assessed_status
            ),
            "provenance_class": "customer evidence",
        },
        "blockers": {"items": blockers},
        "findings": {"items": findings},
        "target-state": {
            "principle": (
                "Raise critical foundations before claiming production AI readiness."
            ),
            "target_level": (
                min(4, result.gates.final_level + 1)
                if result.gates.final_level is not None
                else None
            ),
            "provenance_class": "architect judgment",
        },
        "reference-diagrams": {
            "items": [
                {
                    "architecture_id": finding["architecture_reference"],
                    "title": finding["title"],
                    "score": next(
                        (
                            item["score"]
                            for item in capabilities
                            if any(
                                operand == f"domain.{item['capability_id']}"
                                for operand in finding["source_operand_ids"]
                            )
                        ),
                        None,
                    ),
                    "provenance_class": "architect judgment",
                }
                for finding in findings
            ]
        },
        "roadmap": {
            "items": [
                {
                    "sequence": index,
                    "priority": finding["priority"],
                    "action": finding["recommendation"],
                    "review_state": finding["architect_review"]["state"],
                    "provenance_class": "architect judgment",
                }
                for index, finding in enumerate(findings, start=1)
            ]
        },
        "technology-options": {
            "items": [
                {
                    "finding_id": finding["id"],
                    "vendor_neutral_options": finding["technology_options"],
                    "provenance_class": "architect judgment",
                }
                for finding in findings
            ]
        },
        "evidence-appendix": {
            "source_state_digest": source_digest,
            "provenance_classes": list(PROVENANCE_CLASSES),
            "answers": answer_document["answers"],
            "diagnostic_facts": answer_document["diagnostic_facts"],
            "demo_evidence_used_for_scoring": False,
        },
    }
    report_document = {
        "schema_version": "1.0.0",
        "engagement_id": engagement.engagement_id,
        "framework_version": framework.version,
        "sections": [
            {"id": section_id, "content": sections_by_id[section_id]}
            for section_id in REPORT_SECTION_IDS
        ],
    }
    validated = Report.model_validate(report_document)
    return GeneratedReport(
        json_bytes=canonical_json(validated.model_dump(mode="json")),
        source_state_digest=source_digest,
    )
