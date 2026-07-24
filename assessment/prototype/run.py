#!/usr/bin/env python3
"""Offline deterministic runner for the Issue #38 Phase 1 prototype."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import statistics
import tarfile
import zipfile
from collections import Counter
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path
from typing import Any

import yaml
from jinja2 import Environment, FileSystemLoader, StrictUndefined, select_autoescape

FRAMEWORK_VERSION = "0.1.0-prototype"
DOMAIN_ORDER = ("STR", "ING", "STO", "TRN", "QUA", "LIN", "GOV", "SEC", "OPS", "AID")
CONTENT_ROOT = Path(__file__).resolve().parent / "0.1.0"
ASSESSMENT_ROOT = (
    Path.cwd() / "assessment"
    if (Path.cwd() / "assessment" / "tests" / "fixtures").is_dir()
    else Path(__file__).resolve().parents[1]
)
FIXTURE_ROOT = ASSESSMENT_ROOT / "tests" / "fixtures" / "scenarios" / "0.1.0"
GENERATED_ROOT = ASSESSMENT_ROOT / ".generated" / "prototype"
CONTENT_FILES = (
    "capabilities.yaml",
    "quick-questions.yaml",
    "readiness-levels.yaml",
    "gates.yaml",
    "finding-rules.yaml",
    "recommendations.yaml",
)
RATER_FILES = ("architect-a.json", "architect-b.json")
REPORT_SECTION_IDS = (
    "executive-summary",
    "readiness",
    "capability-heatmap",
    "gates",
    "confidence",
    "blockers",
    "findings",
    "target-state",
    "reference-diagrams",
    "roadmap",
    "technology-options",
    "evidence-appendix",
)
ALLOWED_CONFIDENCE = (
    "Self-reported",
    "Partially evidenced",
    "Evidenced",
    "Conflicting evidence",
    "Not assessed",
)
CONFIDENCE_PRECEDENCE = (
    "Conflicting evidence",
    "Self-reported",
    "Partially evidenced",
    "Evidenced",
)
EXTERNAL_URL = re.compile(r"(?i)(?:(?:https?|file|ftp|data):|//[A-Za-z0-9])")
ABSOLUTE_PATH = re.compile(
    r"(?i)(?:^|[\s\"'])/(?!/)[A-Za-z0-9._~+-]+(?:/[A-Za-z0-9._~+-]+)*"
    r"|[A-Z]:[\\/]|\\\\[A-Za-z0-9_.-]+[\\/]"
)
SECRET = re.compile(
    r"(?:AKIA[0-9A-Z]{16}|ghp_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,}|"
    r"sk_(?:live|test)_[A-Za-z0-9]{16,}|xox[baprs]-[A-Za-z0-9-]{16,}|"
    r"-----BEGIN [A-Z ]*PRIVATE KEY-----|eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.|"
    r"(?i:(?:password|secret|token|credential)\s*[:=]\s*[\"']?[^,\s\"']{12,}))"
)
SAFE_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")


class ValidationError(ValueError):
    """Raised when prototype content or a fixture violates the contract."""


@dataclass(frozen=True)
class Framework:
    capabilities: Mapping[str, Any]
    questions: Mapping[str, Any]
    readiness: Mapping[str, Any]
    gates: Mapping[str, Any]
    finding_rules: Mapping[str, Any]
    recommendations: Mapping[str, Any]


def load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValidationError(f"{path.name}: document must be a mapping")
    return data


def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValidationError(f"{path.name}: document must be an object")
    return data


def canonical_json(data: Any) -> bytes:
    return (json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode()


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def iter_strings(value: Any) -> Iterable[str]:
    if isinstance(value, str):
        yield value
    elif isinstance(value, Mapping):
        for key, item in value.items():
            yield from iter_strings(key)
            yield from iter_strings(item)
    elif isinstance(value, Sequence) and not isinstance(value, str | bytes | bytearray):
        for item in value:
            yield from iter_strings(item)


def reject_sensitive_text(value: Any, *, authored: bool, context: str) -> None:
    for text in iter_strings(value):
        if EXTERNAL_URL.search(text):
            raise ValidationError(f"{context}: external URL is not allowed")
        if ABSOLUTE_PATH.search(text):
            raise ValidationError(f"{context}: absolute path is not allowed")
        if SECRET.search(text):
            raise ValidationError(f"{context}: secret-like text is not allowed")
        if authored and ("<" in text or ">" in text):
            raise ValidationError(f"{context}: raw HTML-like text is not allowed")


def require_exact_anchor_levels(anchors: Any, context: str) -> None:
    if not isinstance(anchors, dict):
        raise ValidationError(f"{context}: anchors must be a mapping")
    normalized: set[int] = set()
    for key, text in anchors.items():
        if type(key) is not int:
            raise ValidationError(f"{context}: anchor level must be an integer")
        level = key
        if level in normalized:
            raise ValidationError(f"{context}: duplicate anchor level {level}")
        if not isinstance(text, str) or len(text.strip()) < 12:
            raise ValidationError(f"{context}: anchor {level} must be observable text")
        normalized.add(level)
    if normalized != set(range(5)):
        raise ValidationError(f"{context}: anchors must contain exactly levels 0-4")


def require_unique_ids(items: Any, context: str) -> set[str]:
    if not isinstance(items, list):
        raise ValidationError(f"{context}: must be a list")
    ids: list[str] = []
    for item in items:
        if not isinstance(item, dict) or not isinstance(item.get("id"), str):
            raise ValidationError(f"{context}: every item must have an ID")
        item_id = item["id"]
        if not SAFE_ID.fullmatch(item_id):
            raise ValidationError(f"{context}: invalid ID {item_id!r}")
        ids.append(item_id)
    if len(ids) != len(set(ids)):
        raise ValidationError(f"{context}: duplicate IDs")
    return set(ids)


def load_framework(content_root: Path = CONTENT_ROOT) -> Framework:
    documents = {name: load_yaml(content_root / name) for name in CONTENT_FILES}
    for name, document in documents.items():
        if document.get("framework_version") != FRAMEWORK_VERSION:
            raise ValidationError(f"{name}: unsupported framework version")
        reject_sensitive_text(document, authored=False, context=name)
    framework = Framework(
        capabilities=documents["capabilities.yaml"],
        questions=documents["quick-questions.yaml"],
        readiness=documents["readiness-levels.yaml"],
        gates=documents["gates.yaml"],
        finding_rules=documents["finding-rules.yaml"],
        recommendations=documents["recommendations.yaml"],
    )
    validate_framework(framework)
    return framework


def validate_framework(framework: Framework) -> None:
    domains = framework.capabilities.get("domains")
    domain_ids = require_unique_ids(domains, "capabilities.domains")
    if not isinstance(domains, list) or len(domains) != 10:
        raise ValidationError("capabilities: exactly 10 domains are required")
    if tuple(domain["id"] for domain in domains) != DOMAIN_ORDER:
        raise ValidationError("capabilities: domain order or confirmed IDs changed")
    for domain in domains:
        require_exact_anchor_levels(domain.get("anchors"), f"domain {domain['id']}")
    if domain_ids != set(DOMAIN_ORDER):
        raise ValidationError("capabilities: domain coverage is invalid")

    questions = framework.questions.get("questions")
    require_unique_ids(questions, "questions")
    if not isinstance(questions, list) or len(questions) != 30:
        raise ValidationError("questions: exactly 30 questions are required")
    expected_question_ids = tuple(
        f"Q-{domain_id}-{question_number:02d}"
        for domain_id in DOMAIN_ORDER
        for question_number in range(1, 4)
    )
    if tuple(question["id"] for question in questions) != expected_question_ids:
        raise ValidationError("questions: confirmed IDs or domain order changed")
    expected_question_domains = tuple(domain_id for domain_id in DOMAIN_ORDER for _ in range(3))
    if tuple(question.get("domain_id") for question in questions) != expected_question_domains:
        raise ValidationError("questions: question-to-domain bindings changed")
    counts: Counter[str] = Counter()
    for question in questions:
        domain_id = question.get("domain_id")
        if domain_id not in domain_ids:
            raise ValidationError(f"question {question['id']}: unknown domain")
        counts[domain_id] += 1
        require_exact_anchor_levels(question.get("anchors"), f"question {question['id']}")
    if counts != Counter({domain_id: 3 for domain_id in DOMAIN_ORDER}):
        raise ValidationError("questions: exactly three questions per domain are required")

    levels = framework.readiness.get("levels")
    if levels != {
        0: "Not ready",
        1: "Foundation blocked",
        2: "Experiment-ready only",
        3: "Production-ready",
        4: "Optimized production-ready",
    }:
        raise ValidationError("readiness: exact versioned labels 0-4 are required")
    if framework.readiness.get("profile_id") != "quick-v1":
        raise ValidationError("readiness: unsupported profile")
    if framework.readiness.get("coverage") != {
        "minimum_answered_per_domain": 2,
        "minimum_answered_total": 27,
    }:
        raise ValidationError("readiness: unsupported coverage semantics")
    if framework.readiness.get("aggregation") != {
        "domain": "median_low",
        "pre_gate": "floor_mean_domain_scores",
        "presentation": "sum_domain_scores_times_2_5",
    }:
        raise ValidationError("readiness: unsupported aggregation semantics")
    sections = framework.readiness.get("report_sections")
    if not isinstance(sections, list):
        raise ValidationError("readiness: report sections must be a list")
    require_unique_ids(sections, "readiness.report_sections")
    if tuple(section["id"] for section in sections) != REPORT_SECTION_IDS:
        raise ValidationError("readiness: canonical 12-section order changed")
    confidence = framework.readiness.get("confidence")
    if not isinstance(confidence, dict):
        raise ValidationError("readiness: confidence contract missing")
    if tuple(confidence.get("statuses", ())) != ALLOWED_CONFIDENCE:
        raise ValidationError("readiness: confidence statuses changed")
    if tuple(confidence.get("least_assured_precedence", ())) != CONFIDENCE_PRECEDENCE:
        raise ValidationError("readiness: confidence precedence changed")

    gates = framework.gates.get("rules")
    require_unique_ids(gates, "gates.rules")
    if not isinstance(gates, list) or len(gates) != 7:
        raise ValidationError("gates: exactly seven rules are required")
    if (
        framework.gates.get("bundle_id") != "quick-readiness-gates"
        or framework.gates.get("bundle_version") != 1
        or framework.gates.get("profile_id") != "quick-v1"
    ):
        raise ValidationError("gates: unsupported bundle or profile")
    expected_rules = {
        "G-QUALITY": ("domain.QUA", "domain_score", "le", 1, 1),
        "G-SECURITY": ("domain.SEC", "domain_score", "le", 1, 1),
        "G-PRIVACY": ("fact.privacy_control_level", "diagnostic_fact", "le", 1, 1),
        "G-GOVERNANCE": ("domain.GOV", "domain_score", "le", 1, 2),
        "G-OWNERSHIP": ("fact.ownership_control_level", "diagnostic_fact", "le", 1, 2),
        "G-LINEAGE": ("fact.critical_lineage", "diagnostic_fact", "eq", False, 2),
        "G-REPRODUCIBILITY": (
            "fact.reproducible_versioned",
            "diagnostic_fact",
            "eq",
            False,
            2,
        ),
    }
    if {gate["id"] for gate in gates} != set(expected_rules):
        raise ValidationError("gates: required rule set changed")
    for gate in gates:
        required = {
            "version",
            "operand_id",
            "source",
            "operator",
            "threshold",
            "cap",
            "explanation",
        }
        if not required.issubset(gate) or gate["version"] != 1:
            raise ValidationError(f"gate {gate['id']}: malformed rule")
        actual = (
            gate["operand_id"],
            gate["source"],
            gate["operator"],
            gate["threshold"],
            gate["cap"],
        )
        if actual != expected_rules[gate["id"]]:
            raise ValidationError(f"gate {gate['id']}: unsupported semantics")
        if not isinstance(gate["explanation"], str) or not gate["explanation"].strip():
            raise ValidationError(f"gate {gate['id']}: explanation is required")
    diagnostic_facts = framework.gates.get("diagnostic_facts")
    diagnostic_fact_ids = require_unique_ids(diagnostic_facts, "gates.diagnostic_facts")
    if not isinstance(diagnostic_facts, list):
        raise ValidationError("gates: diagnostic facts must be a list")
    expected_facts = {
        "privacy_control_level": ("GOV", "integer", 0, 4),
        "ownership_control_level": ("STR", "integer", 0, 4),
        "critical_lineage": ("LIN", "boolean", None, None),
        "reproducible_versioned": ("AID", "boolean", None, None),
    }
    if diagnostic_fact_ids != set(expected_facts):
        raise ValidationError("gates: diagnostic fact set changed")
    for fact in diagnostic_facts:
        expected_domain, expected_type, minimum, maximum = expected_facts[fact["id"]]
        if fact.get("domain_id") != expected_domain or fact.get("type") != expected_type:
            raise ValidationError(f"diagnostic fact {fact['id']}: unsupported schema")
        if expected_type == "integer":
            if fact.get("minimum") != minimum or fact.get("maximum") != maximum:
                raise ValidationError(f"diagnostic fact {fact['id']}: invalid range")
        elif set(fact) != {"id", "domain_id", "type"}:
            raise ValidationError(f"diagnostic fact {fact['id']}: unexpected boolean metadata")

    recommendations = framework.recommendations.get("recommendations")
    recommendation_ids = require_unique_ids(recommendations, "recommendations")
    architectures = framework.recommendations.get("architectures")
    architecture_ids = require_unique_ids(architectures, "architectures")
    if not isinstance(recommendations, list):
        raise ValidationError("recommendations: list missing")
    for recommendation in recommendations:
        required = {
            "impact",
            "action",
            "architecture_reference",
            "technology_options",
            "demo_reference",
        }
        if not required.issubset(recommendation):
            raise ValidationError(f"recommendation {recommendation['id']}: incomplete")
        if recommendation["architecture_reference"] not in architecture_ids:
            raise ValidationError(f"recommendation {recommendation['id']}: unresolved architecture")
        for field in ("impact", "action", "demo_reference"):
            if not isinstance(recommendation[field], str) or not recommendation[field].strip():
                raise ValidationError(f"recommendation {recommendation['id']}: {field} is required")
        if not isinstance(recommendation["technology_options"], list) or not all(
            isinstance(option, str) and option.strip()
            for option in recommendation["technology_options"]
        ):
            raise ValidationError(
                f"recommendation {recommendation['id']}: technology options are malformed"
            )
    finding_rules = framework.finding_rules.get("rules")
    require_unique_ids(finding_rules, "finding_rules")
    if not isinstance(finding_rules, list):
        raise ValidationError("finding rules: list missing")
    priority_table = framework.finding_rules.get("priority_decision_table")
    expected_priority_table = {
        "triggered_gate": "Critical blocker",
        "ungated_level_0_or_1": "High-priority foundation",
        "cross_domain_blocker": "High-priority foundation",
        "domain_level_2": "Near-term improvement",
        "domain_level_3_target_4": "Strategic enhancement",
        "domain_level_4": None,
    }
    if priority_table != expected_priority_table:
        raise ValidationError("finding rules: unsupported priority decision table")
    if framework.finding_rules.get("priority_order") != [
        "Critical blocker",
        "High-priority foundation",
        "Near-term improvement",
        "Strategic enhancement",
    ]:
        raise ValidationError("finding rules: priority order changed")
    allowed_operands = {
        *(f"domain.{domain_id}" for domain_id in DOMAIN_ORDER),
        *(f"fact.{fact_id}" for fact_id in diagnostic_fact_ids),
    }
    for rule in finding_rules:
        if rule.get("recommendation_id") not in recommendation_ids:
            raise ValidationError(f"finding rule {rule['id']}: unresolved recommendation")
        if not isinstance(rule.get("title"), str) or not rule["title"].strip():
            raise ValidationError(f"finding rule {rule['id']}: title is required")
        validate_condition(rule.get("condition"), allowed_operands, f"finding rule {rule['id']}")
        gate_id = rule.get("gate_id")
        if gate_id is not None and gate_id not in expected_rules:
            raise ValidationError(f"finding rule {rule['id']}: unresolved gate")
        priority_operand = rule.get("priority_operand")
        if priority_operand is not None and priority_operand not in allowed_operands:
            raise ValidationError(f"finding rule {rule['id']}: invalid priority operand")
        if rule.get("priority_mode") not in {None, "cross_domain_blocker"}:
            raise ValidationError(f"finding rule {rule['id']}: invalid priority mode")


def validate_condition(condition: Any, allowed_operands: set[str], context: str) -> None:
    if not isinstance(condition, dict):
        raise ValidationError(f"{context}: condition must be a mapping")
    if set(condition) in ({"any"}, {"all"}):
        children = condition[next(iter(condition))]
        if not isinstance(children, list) or len(children) < 2:
            raise ValidationError(f"{context}: compound condition needs at least two children")
        for child in children:
            validate_condition(child, allowed_operands, context)
        return
    if set(condition) != {"operand", "operator", "threshold"}:
        raise ValidationError(f"{context}: malformed atomic condition")
    if condition["operand"] not in allowed_operands:
        raise ValidationError(f"{context}: unsupported operand")
    if condition["operator"] not in {"le", "eq"}:
        raise ValidationError(f"{context}: unsupported operator")
    operand_is_boolean = condition["operand"] in {
        "fact.critical_lineage",
        "fact.reproducible_versioned",
    }
    threshold = condition["threshold"]
    if operand_is_boolean:
        if condition["operator"] != "eq" or type(threshold) is not bool:
            raise ValidationError(f"{context}: malformed boolean comparison")
    elif type(threshold) is not int or not 0 <= threshold <= 4:
        raise ValidationError(f"{context}: malformed maturity threshold")


def question_ids(framework: Framework) -> tuple[str, ...]:
    return tuple(question["id"] for question in framework.questions["questions"])


def validate_fixture(fixture: Mapping[str, Any], framework: Framework) -> None:
    required = {
        "schema_version",
        "scenario_id",
        "rater_id",
        "organization_name",
        "duration_minutes",
        "ratings",
        "evidence_statuses",
        "notes",
        "diagnostic_facts",
        "actionability_review",
    }
    if set(fixture) != required:
        raise ValidationError("fixture: missing or unexpected fields")
    if fixture["schema_version"] != FRAMEWORK_VERSION:
        raise ValidationError("fixture: unsupported version")
    if fixture["rater_id"] not in {"architect-a", "architect-b"}:
        raise ValidationError("fixture: invalid rater")
    if (
        not isinstance(fixture["duration_minutes"], int)
        or not 0 < fixture["duration_minutes"] <= 60
    ):
        raise ValidationError("fixture: duration must be 1-60 minutes")
    ratings = fixture["ratings"]
    statuses = fixture["evidence_statuses"]
    notes = fixture["notes"]
    if not all(
        isinstance(items, list) and len(items) == 30 for items in (ratings, statuses, notes)
    ):
        raise ValidationError("fixture: ratings, statuses, and notes must each contain 30 values")
    for index, (rating, status, note) in enumerate(zip(ratings, statuses, notes, strict=True)):
        if rating is not None and (type(rating) is not int or not 0 <= rating <= 4):
            raise ValidationError(f"fixture: rating {index} must be 0-4 or null")
        if status not in ALLOWED_CONFIDENCE:
            raise ValidationError(f"fixture: invalid evidence status at {index}")
        if (rating is None) != (status == "Not assessed"):
            raise ValidationError(f"fixture: rating/status mismatch at {index}")
        if not isinstance(note, str) or not note.strip():
            raise ValidationError(f"fixture: missing architect note at {index}")
    facts = fixture["diagnostic_facts"]
    fact_schemas = {fact["id"]: fact for fact in framework.gates["diagnostic_facts"]}
    if not isinstance(facts, dict) or set(facts) != set(fact_schemas):
        raise ValidationError("fixture: malformed diagnostic facts")
    for fact_id, schema in fact_schemas.items():
        value = facts[fact_id]
        if schema["type"] == "integer" and (
            type(value) is not int or not schema["minimum"] <= value <= schema["maximum"]
        ):
            raise ValidationError(f"fixture: {fact_id} must be 0-4")
        if schema["type"] == "boolean" and type(value) is not bool:
            raise ValidationError(f"fixture: {fact_id} must be boolean")
    review = fixture["actionability_review"]
    if not isinstance(review, dict) or set(review) != {
        "recommendations_actionable",
        "gate_outcome_reasonable",
        "report_usable",
    }:
        raise ValidationError("fixture: malformed actionability review")
    if not all(value is True for value in review.values()):
        raise ValidationError("fixture: actionability review must pass")
    reject_sensitive_text(fixture, authored=True, context="fixture")

    result = evaluate_fixture(fixture, framework, validate=False)
    if result["coverage"]["answered_total"] < 27 or not result["coverage"]["complete"]:
        raise ValidationError("fixture: quick assessment coverage is below 90% or misses a domain")


def confidence_for(statuses: Sequence[str]) -> dict[str, Any]:
    distribution = {status: statuses.count(status) for status in ALLOWED_CONFIDENCE}
    assessed = [status for status in statuses if status != "Not assessed"]
    least_assured = next(
        (status for status in CONFIDENCE_PRECEDENCE if status in assessed),
        None,
    )
    return {
        "distribution": distribution,
        "least_assured_assessed_status": least_assured,
        "assessed_count": len(assessed),
        "not_assessed_count": distribution["Not assessed"],
    }


def priority_for(
    score: int | None,
    decision_table: Mapping[str, str | None],
    *,
    gate_cap: int | None = None,
    cross_domain_blocker: bool = False,
    target_level_four: bool = False,
) -> str | None:
    if gate_cap is not None:
        return decision_table["triggered_gate"]
    if score is None:
        return None
    if score <= 1 or cross_domain_blocker:
        return decision_table[
            "cross_domain_blocker" if cross_domain_blocker else "ungated_level_0_or_1"
        ]
    if score == 2:
        return decision_table["domain_level_2"]
    if score == 3 and target_level_four:
        return decision_table["domain_level_3_target_4"]
    return decision_table["domain_level_4"]


def resolve_operand(
    operand_id: str, domain_scores: Mapping[str, int], facts: Mapping[str, Any]
) -> Any:
    if operand_id.startswith("domain."):
        return domain_scores[operand_id.split(".", 1)[1]]
    if operand_id.startswith("fact."):
        return facts[operand_id.split(".", 1)[1]]
    raise ValidationError(f"unsupported operand {operand_id}")


def evaluate_condition(
    condition: Mapping[str, Any],
    domain_scores: Mapping[str, int],
    facts: Mapping[str, Any],
) -> bool:
    if "any" in condition:
        return any(evaluate_condition(child, domain_scores, facts) for child in condition["any"])
    if "all" in condition:
        return all(evaluate_condition(child, domain_scores, facts) for child in condition["all"])
    operand = resolve_operand(condition["operand"], domain_scores, facts)
    if condition["operator"] == "le":
        return operand <= condition["threshold"]
    if condition["operator"] == "eq":
        return operand == condition["threshold"]
    raise ValidationError("unsupported condition operator")


def evaluate_gate(
    rule: Mapping[str, Any], domain_scores: Mapping[str, int], facts: Mapping[str, Any]
) -> tuple[bool, Any]:
    operand_id = rule["operand_id"]
    operand = resolve_operand(operand_id, domain_scores, facts)
    if rule["operator"] == "le":
        triggered = operand <= rule["threshold"]
    elif rule["operator"] == "eq":
        triggered = operand == rule["threshold"]
    else:
        raise ValidationError(f"gate {rule['id']}: unsupported operator")
    return triggered, operand


def evaluate_fixture(
    fixture: Mapping[str, Any],
    framework: Framework,
    *,
    validate: bool = True,
) -> dict[str, Any]:
    if validate:
        validate_fixture(fixture, framework)
    ratings = fixture["ratings"]
    statuses = fixture["evidence_statuses"]
    questions = framework.questions["questions"]
    domain_scores: dict[str, int] = {}
    confidence: dict[str, Any] = {}
    answered_by_domain: dict[str, int] = {}
    for domain_id in DOMAIN_ORDER:
        indices = [
            index for index, question in enumerate(questions) if question["domain_id"] == domain_id
        ]
        assessed = [ratings[index] for index in indices if ratings[index] is not None]
        answered_by_domain[domain_id] = len(assessed)
        if len(assessed) >= 2:
            domain_scores[domain_id] = int(statistics.median_low(assessed))
        confidence[domain_id] = confidence_for([statuses[index] for index in indices])
    answered_total = sum(rating is not None for rating in ratings)
    complete = answered_total >= 27 and all(count >= 2 for count in answered_by_domain.values())
    coverage = {
        "answered_total": answered_total,
        "question_total": 30,
        "answered_percent": f"{Decimal(answered_total * 100) / Decimal(30):.1f}",
        "answered_by_domain": answered_by_domain,
        "complete": complete,
    }
    if not complete:
        return {
            "scenario_id": fixture["scenario_id"],
            "rater_id": fixture["rater_id"],
            "coverage": coverage,
            "domain_scores": domain_scores,
            "confidence": confidence,
            "pre_gate_readiness": None,
            "final_readiness": None,
            "presentation_score": None,
            "gate_traces": [],
            "findings": [],
        }
    pre_gate = math.floor(sum(domain_scores.values()) / 10)
    presentation = Decimal(sum(domain_scores.values())) * Decimal("2.5")
    gate_traces: list[dict[str, Any]] = []
    final = pre_gate
    for rule in framework.gates["rules"]:
        triggered, operand = evaluate_gate(rule, domain_scores, fixture["diagnostic_facts"])
        result = min(pre_gate, rule["cap"]) if triggered else pre_gate
        gate_traces.append(
            {
                "rule_id": rule["id"],
                "rule_version": rule["version"],
                "operand_id": rule["operand_id"],
                "operand_source": rule["source"],
                "operand_value": operand,
                "pre_gate_state": pre_gate,
                "triggered": triggered,
                "applied_cap": rule["cap"] if triggered else None,
                "rule_result": result,
                "final_state": None,
                "explanation": (
                    f"{rule['explanation']} Operand {rule['operand_id']} was {operand!r}; "
                    f"the rule {'applied' if triggered else 'did not apply'}."
                ),
            }
        )
        if triggered:
            final = min(final, rule["cap"])
    for trace in gate_traces:
        trace["final_state"] = final

    recommendations = {item["id"]: item for item in framework.recommendations["recommendations"]}
    facts = fixture["diagnostic_facts"]
    priority_table = framework.finding_rules["priority_decision_table"]
    overall_confidence = confidence_for(statuses)
    least_assured = overall_confidence["least_assured_assessed_status"]
    evidence_action = (
        "Maintain the evidence links and refresh them during the next assessment."
        if least_assured == "Evidenced"
        else (
            "Resolve conflicting evidence before relying on this finding."
            if least_assured == "Conflicting evidence"
            else "Validate self-reported or partial evidence before implementation."
        )
    )
    findings: list[dict[str, Any]] = []
    for rule in framework.finding_rules["rules"]:
        if not evaluate_condition(rule["condition"], domain_scores, facts):
            continue
        recommendation = recommendations[rule["recommendation_id"]]
        gate_id = rule.get("gate_id")
        gate_cap = (
            next(gate["cap"] for gate in framework.gates["rules"] if gate["id"] == gate_id)
            if gate_id is not None
            else None
        )
        priority_operand = rule.get("priority_operand")
        score = (
            resolve_operand(priority_operand, domain_scores, facts)
            if priority_operand is not None
            else None
        )
        findings.append(
            {
                "id": rule["id"],
                "title": rule["title"],
                "gap": (
                    f"Observed condition for {rule['id']} does not meet the target control state."
                ),
                "impact": recommendation["impact"],
                "priority": priority_for(
                    score,
                    priority_table,
                    gate_cap=gate_cap,
                    cross_domain_blocker=rule.get("priority_mode") == "cross_domain_blocker",
                ),
                "recommendation_id": recommendation["id"],
                "recommendation": recommendation["action"],
                "architecture_reference": recommendation["architecture_reference"],
                "technology_options": recommendation["technology_options"],
                "demo_reference": recommendation["demo_reference"],
                "action": recommendation["action"],
                "evidence_validation_action": evidence_action,
            }
        )
    return {
        "scenario_id": fixture["scenario_id"],
        "rater_id": fixture["rater_id"],
        "coverage": coverage,
        "domain_scores": domain_scores,
        "selected_capability_anchors": {
            domain["id"]: domain["anchors"][domain_scores[domain["id"]]]
            for domain in framework.capabilities["domains"]
        },
        "confidence": confidence,
        "pre_gate_readiness": pre_gate,
        "pre_gate_label": framework.readiness["levels"][pre_gate],
        "final_readiness": final,
        "final_label": framework.readiness["levels"][final],
        "presentation_score": f"{presentation:.1f}",
        "gate_traces": gate_traces,
        "findings": findings,
    }


def load_scenarios(
    framework: Framework,
    fixture_root: Path = FIXTURE_ROOT,
) -> dict[str, dict[str, Any]]:
    if not fixture_root.is_dir():
        raise ValidationError(
            "scenario fixture root was not found; pass --fixture-root with the tracked "
            "0.1.0 scenario directory"
        )
    scenarios: dict[str, dict[str, Any]] = {}
    for scenario_dir in sorted(path for path in fixture_root.iterdir() if path.is_dir()):
        raters: dict[str, Any] = {}
        for filename in RATER_FILES:
            fixture = load_json(scenario_dir / filename)
            validate_fixture(fixture, framework)
            if fixture["scenario_id"] != scenario_dir.name:
                raise ValidationError(f"{filename}: scenario ID/path mismatch")
            raters[fixture["rater_id"]] = fixture
        expected = load_json(scenario_dir / "expected.json")
        reject_sensitive_text(expected, authored=False, context=f"{scenario_dir.name}/expected")
        raters["expected"] = expected
        scenarios[scenario_dir.name] = raters
    if set(scenarios) != {
        "startup-no-governance",
        "enterprise-lake-weak-quality",
        "manual-governance-missing-lineage",
        "strong-engineering-no-ai-operating-model",
    }:
        raise ValidationError("scenarios: exact four-persona set is required")
    return scenarios


def assert_expected(
    scenarios: Mapping[str, Mapping[str, Any]], framework: Framework
) -> dict[str, Any]:
    checked = 0
    for scenario_id, scenario in scenarios.items():
        expected = scenario["expected"]
        for rater_id in ("architect-a", "architect-b"):
            result = evaluate_fixture(scenario[rater_id], framework)
            rater_expected = expected[rater_id]
            checks = {
                "domain_scores": [result["domain_scores"][domain_id] for domain_id in DOMAIN_ORDER],
                "pre_gate_readiness": result["pre_gate_readiness"],
                "final_readiness": result["final_readiness"],
                "triggered_gates": [
                    trace["rule_id"] for trace in result["gate_traces"] if trace["triggered"]
                ],
                "finding_ids": [finding["id"] for finding in result["findings"]],
                "confidence_distribution": confidence_for(scenario[rater_id]["evidence_statuses"])[
                    "distribution"
                ],
            }
            for field, actual in checks.items():
                if actual != rater_expected[field]:
                    raise AssertionError(
                        f"{scenario_id}/{rater_id}: {field} expected "
                        f"{rater_expected[field]!r}, got {actual!r}"
                    )
                checked += 1
    return {"scenario_raters": 8, "assertions": checked}


def calibration_summary(
    scenarios: Mapping[str, Mapping[str, Any]], framework: Framework
) -> dict[str, Any]:
    comparable = 0
    within_one = 0
    possible_slots = 0
    domain_pairs = 0
    final_pairs = 0
    largest_deltas: list[dict[str, Any]] = []
    for scenario_id, scenario in scenarios.items():
        result_a = evaluate_fixture(scenario["architect-a"], framework)
        result_b = evaluate_fixture(scenario["architect-b"], framework)
        for index, (a, b) in enumerate(
            zip(scenario["architect-a"]["ratings"], scenario["architect-b"]["ratings"], strict=True)
        ):
            possible_slots += 1
            if a is None or b is None:
                continue
            comparable += 1
            delta = abs(a - b)
            if delta <= 1:
                within_one += 1
            if delta > 1:
                largest_deltas.append(
                    {
                        "scenario_id": scenario_id,
                        "question_id": question_ids(framework)[index],
                        "delta": delta,
                    }
                )
        for domain_id in DOMAIN_ORDER:
            domain_pairs += 1
            if abs(result_a["domain_scores"][domain_id] - result_b["domain_scores"][domain_id]) > 1:
                raise AssertionError(f"{scenario_id}: paired domain result delta exceeds one")
        final_pairs += 1
        if abs(result_a["final_readiness"] - result_b["final_readiness"]) > 1:
            raise AssertionError(f"{scenario_id}: paired readiness result delta exceeds one")
    ratio = Decimal(within_one) / Decimal(comparable)
    if ratio < Decimal("0.85"):
        raise AssertionError("calibration is below 85%")
    summary = {
        "possible_question_slots": possible_slots,
        "comparable_pairs": comparable,
        "not_assessed_slots": possible_slots - comparable,
        "within_one_level_pairs": within_one,
        "within_one_level_percent": f"{ratio * 100:.1f}",
        "paired_domain_results_checked": domain_pairs,
        "paired_final_readiness_results_checked": final_pairs,
        "largest_rating_deltas": largest_deltas,
    }
    expected = {
        "possible_question_slots": 120,
        "comparable_pairs": 119,
        "not_assessed_slots": 1,
        "within_one_level_pairs": 117,
        "within_one_level_percent": "98.3",
        "paired_domain_results_checked": 40,
        "paired_final_readiness_results_checked": 4,
    }
    for field, expected_value in expected.items():
        if summary[field] != expected_value:
            raise AssertionError(
                f"calibration {field}: expected {expected_value}, got {summary[field]}"
            )
    return summary


def build_report(
    fixture: Mapping[str, Any],
    result: Mapping[str, Any],
    framework: Framework,
) -> dict[str, Any]:
    domains = {domain["id"]: domain for domain in framework.capabilities["domains"]}
    blockers = [
        finding for finding in result["findings"] if finding["priority"] == "Critical blocker"
    ]
    sections_by_id: dict[str, Any] = {
        "executive-summary": {
            "organization": fixture["organization_name"],
            "statement": (
                f"Final readiness is {result['final_readiness']} — {result['final_label']}. "
                "Capability maturity is authoritative; the normalized value is presentation-only."
            ),
        },
        "readiness": {
            "pre_gate_level": result["pre_gate_readiness"],
            "pre_gate_label": result["pre_gate_label"],
            "final_level": result["final_readiness"],
            "final_label": result["final_label"],
            "presentation_score": result["presentation_score"],
        },
        "capability-heatmap": [
            {
                "domain_id": domain_id,
                "name": domains[domain_id]["name"],
                "score": result["domain_scores"][domain_id],
                "anchor": result["selected_capability_anchors"][domain_id],
            }
            for domain_id in DOMAIN_ORDER
        ],
        "gates": result["gate_traces"],
        "confidence": result["confidence"],
        "blockers": blockers,
        "findings": result["findings"],
        "target-state": {
            "principle": "Raise critical foundations before claiming production AI readiness.",
            "target_level": min(4, result["final_readiness"] + 1),
        },
        "reference-diagrams": [
            {"architecture_id": finding["architecture_reference"], "status": "Phase 1 placeholder"}
            for finding in result["findings"]
        ],
        "roadmap": [
            {
                "sequence": index,
                "priority": finding["priority"],
                "action": finding["action"],
            }
            for index, finding in enumerate(result["findings"], start=1)
        ],
        "technology-options": [
            {
                "finding_id": finding["id"],
                "vendor_neutral_options": finding["technology_options"],
            }
            for finding in result["findings"]
        ],
        "evidence-appendix": {
            "question_ids": list(question_ids(framework)),
            "ratings": fixture["ratings"],
            "evidence_statuses": fixture["evidence_statuses"],
            "architect_notes": fixture["notes"],
            "diagnostic_facts": fixture["diagnostic_facts"],
            "demo_evidence_used_for_scoring": False,
        },
    }
    sections = [
        {"id": section["id"], "title": section["title"], "content": sections_by_id[section["id"]]}
        for section in framework.readiness["report_sections"]
    ]
    return {
        "schema_version": FRAMEWORK_VERSION,
        "framework_version": FRAMEWORK_VERSION,
        "title": f"AI-ready assessment prototype — {fixture['organization_name']}",
        "scenario_id": fixture["scenario_id"],
        "rater_id": fixture["rater_id"],
        "sections": sections,
    }


def render_report(report: Mapping[str, Any]) -> bytes:
    environment = Environment(
        loader=FileSystemLoader(Path(__file__).resolve().parent),
        undefined=StrictUndefined,
        autoescape=select_autoescape(("html", "xml"), default=True),
        keep_trailing_newline=True,
    )
    template = environment.get_template("report-template.html.j2")
    css = (Path(__file__).resolve().parent / "report.css").read_text(encoding="utf-8")
    rendered = template.render(report=report, css=css)
    return rendered.encode()


def validate_report_artifacts(json_bytes: bytes, html_bytes: bytes) -> None:
    report = json.loads(json_bytes)
    if tuple(section["id"] for section in report.get("sections", [])) != REPORT_SECTION_IDS:
        raise ValidationError("report: canonical 12-section order missing")
    for name, data in (("report.json", json_bytes), ("report.html", html_bytes)):
        text = data.decode("utf-8")
        if EXTERNAL_URL.search(text):
            raise ValidationError(f"{name}: external URL present")
        if ABSOLUTE_PATH.search(text):
            raise ValidationError(f"{name}: absolute path present")
        if SECRET.search(text):
            raise ValidationError(f"{name}: secret-like text present")
    html = html_bytes.decode("utf-8")
    if re.search(r"(?i)<(?:script|iframe|object|embed)\b", html):
        raise ValidationError("report.html: active or remote-capable element present")
    if re.search(r"(?i)\s(?:src|href)\s*=", html):
        raise ValidationError("report.html: linked assets are not allowed")
    if re.search(r"(?i)\son[a-z]+\s*=", html):
        raise ValidationError("report.html: event handler present")


def generate_report_artifacts(
    scenarios: Mapping[str, Mapping[str, Any]],
    framework: Framework,
    output_root: Path = GENERATED_ROOT,
) -> dict[str, str]:
    digests: dict[str, str] = {}
    for scenario_id, scenario in scenarios.items():
        for rater_id in ("architect-a", "architect-b"):
            fixture = scenario[rater_id]
            result = evaluate_fixture(fixture, framework)
            report = build_report(fixture, result, framework)
            json_bytes = canonical_json(report)
            html_bytes = render_report(report)
            validate_report_artifacts(json_bytes, html_bytes)
            report_dir = output_root / scenario_id / rater_id
            report_dir.mkdir(parents=True, exist_ok=True)
            summary_bytes = canonical_json(
                {
                    "scenario_id": scenario_id,
                    "rater_id": rater_id,
                    "answered": result["coverage"]["answered_total"],
                    "duration_minutes": fixture["duration_minutes"],
                    "pre_gate_readiness": result["pre_gate_readiness"],
                    "final_readiness": result["final_readiness"],
                    "report_json_sha256": sha256(json_bytes),
                    "report_html_sha256": sha256(html_bytes),
                }
            )
            files = {
                report_dir / "report.json": json_bytes,
                report_dir / "report.html": html_bytes,
                report_dir / "summary.json": summary_bytes,
            }
            for path, data in files.items():
                path.write_bytes(data)
                digests[path.relative_to(output_root).as_posix()] = sha256(data)
        primary_dir = output_root / scenario_id / "architect-a"
        for filename in ("report.json", "report.html", "summary.json"):
            data = (primary_dir / filename).read_bytes()
            path = output_root / scenario_id / filename
            path.write_bytes(data)
            digests[path.relative_to(output_root).as_posix()] = sha256(data)
    return dict(sorted(digests.items()))


def verify_report_stability(
    scenarios: Mapping[str, Mapping[str, Any]],
    framework: Framework,
    output_root: Path = GENERATED_ROOT,
) -> dict[str, Any]:
    first = generate_report_artifacts(scenarios, framework, output_root)
    first_bytes = {path: (output_root / path).read_bytes() for path in first}
    second = generate_report_artifacts(scenarios, framework, output_root)
    if first != second:
        raise AssertionError("report digests changed across consecutive generations")
    for path, data in first_bytes.items():
        if data != (output_root / path).read_bytes():
            raise AssertionError(f"{path}: report bytes changed across generations")
    return {"artifacts": len(first), "byte_stable": True, "digests": first}


def build_check(dist: Path) -> dict[str, Any]:
    wheels = sorted(dist.glob("*.whl"))
    sdists = sorted(dist.glob("*.tar.gz"))
    if len(wheels) != 1 or len(sdists) != 1:
        raise ValidationError("build: expected exactly one wheel and one sdist")
    public_schema_files = {
        "ai-ready-dataset-manifest-v1.schema.json",
        "answer-v1.schema.json",
        "demo-stage-manifest-v1.schema.json",
        "engagement-v1.schema.json",
        "framework-v1.schema.json",
        "recipe-v1.schema.json",
        "report-v1.schema.json",
    }
    wheel_schema_files = {
        f"assessment/public_schemas/{name}" for name in public_schema_files
    }
    wheel_expected = {
        *(f"prototype/0.1.0/{name}" for name in CONTENT_FILES),
        "prototype/report-template.html.j2",
        "prototype/report.css",
        "assessment/__init__.py",
        "assessment/__main__.py",
        "assessment/cli.py",
        "assessment/content/loader.py",
        "assessment/content/markdown.py",
        "assessment/content/schemas.py",
        "assessment/content/semantics.py",
        "assessment/domain/errors.py",
        "assessment/domain/models.py",
        "assessment/domain/versions.py",
        "assessment/public_schemas/__init__.py",
        *wheel_schema_files,
        "assessment/storage/archive.py",
        "assessment/storage/hygiene.py",
        "assessment/storage/limits.py",
        "assessment/storage/local.py",
        "assessment/storage/migrations.py",
        "assessment/storage/protocol.py",
    }
    with zipfile.ZipFile(wheels[0]) as archive:
        wheel_names = set(archive.namelist())
    if not wheel_expected.issubset(wheel_names):
        raise ValidationError("build: wheel is missing required package content")
    if {name for name in wheel_names if name.endswith(".schema.json")} != wheel_schema_files:
        raise ValidationError("build: wheel must contain exactly seven public JSON Schemas")
    sdist_expected = {
        f"src/{name}" if name.startswith("assessment/") else name for name in wheel_expected
    }
    with tarfile.open(sdists[0], "r:gz") as archive:
        sdist_names = {"/".join(name.split("/")[1:]) for name in archive.getnames()}
    if not sdist_expected.issubset(sdist_names):
        raise ValidationError("build: sdist is missing required package content")
    sdist_schema_files = {
        f"src/assessment/public_schemas/{name}" for name in public_schema_files
    }
    if {name for name in sdist_names if name.endswith(".schema.json")} != sdist_schema_files:
        raise ValidationError("build: sdist must contain exactly seven public JSON Schemas")
    return {
        "wheel": wheels[0].name,
        "sdist": sdists[0].name,
        "packaged_files_checked": len(wheel_expected),
    }


def emit_result(label: str, data: Mapping[str, Any]) -> None:
    print(f"{label}: {json.dumps(data, ensure_ascii=False, sort_keys=True)}")


def command_schema() -> None:
    framework = load_framework()
    emit_result(
        "assessment-schema PASS",
        {
            "domains": len(framework.capabilities["domains"]),
            "domain_anchors": sum(
                len(item["anchors"]) for item in framework.capabilities["domains"]
            ),
            "questions": len(framework.questions["questions"]),
            "question_anchors": sum(
                len(item["anchors"]) for item in framework.questions["questions"]
            ),
        },
    )


def command_contract(fixture_root: Path) -> None:
    framework = load_framework()
    scenarios = load_scenarios(framework, fixture_root)
    result = assert_expected(scenarios, framework)
    emit_result("assessment-contract PASS", result)


def command_scenarios(fixture_root: Path) -> None:
    framework = load_framework()
    scenarios = load_scenarios(framework, fixture_root)
    expected = assert_expected(scenarios, framework)
    completion = {
        scenario_id: {
            rater_id: {
                "answered": evaluate_fixture(scenario[rater_id], framework)["coverage"][
                    "answered_total"
                ],
                "duration_minutes": scenario[rater_id]["duration_minutes"],
            }
            for rater_id in ("architect-a", "architect-b")
        }
        for scenario_id, scenario in scenarios.items()
    }
    emit_result("assessment-scenarios PASS", {"expected": expected, "completion": completion})


def command_calibration(fixture_root: Path) -> None:
    framework = load_framework()
    scenarios = load_scenarios(framework, fixture_root)
    assert_expected(scenarios, framework)
    emit_result("assessment-calibration PASS", calibration_summary(scenarios, framework))


def command_report(verify_stability: bool, fixture_root: Path) -> None:
    framework = load_framework()
    scenarios = load_scenarios(framework, fixture_root)
    result = (
        verify_report_stability(scenarios, framework)
        if verify_stability
        else {"digests": generate_report_artifacts(scenarios, framework)}
    )
    emit_result("assessment-report PASS", result)


def command_build_check(dist: Path) -> None:
    emit_result("assessment-build PASS", build_check(dist))


def parser() -> argparse.ArgumentParser:
    cli = argparse.ArgumentParser(description=__doc__)
    subcommands = cli.add_subparsers(dest="command", required=True)
    subcommands.add_parser("schema")
    contract = subcommands.add_parser("contract")
    scenarios = subcommands.add_parser("scenarios")
    calibration = subcommands.add_parser("calibration")
    report = subcommands.add_parser("report")
    report.add_argument("--verify-stability", action="store_true")
    for command in (contract, scenarios, calibration, report):
        command.add_argument("--fixture-root", type=Path, default=FIXTURE_ROOT)
    build = subcommands.add_parser("build-check")
    build.add_argument("dist", type=Path)
    return cli


def main(argv: Sequence[str] | None = None) -> int:
    args = parser().parse_args(argv)
    if args.command == "schema":
        command_schema()
    elif args.command == "contract":
        command_contract(args.fixture_root)
    elif args.command == "scenarios":
        command_scenarios(args.fixture_root)
    elif args.command == "calibration":
        command_calibration(args.fixture_root)
    elif args.command == "report":
        command_report(args.verify_stability, args.fixture_root)
    elif args.command == "build-check":
        command_build_check(args.dist)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
