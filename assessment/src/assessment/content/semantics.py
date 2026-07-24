"""Cross-document semantic validation for framework v1."""

from __future__ import annotations

from collections import Counter
from collections.abc import Iterable, Mapping
from typing import Any

from assessment.domain.errors import ContentValidationError
from assessment.domain.models import REPORT_SECTION_IDS
from assessment.domain.versions import FRAMEWORK_VERSION, SCHEMA_VERSION

DOMAIN_ORDER = ("STR", "ING", "STO", "TRN", "QUA", "LIN", "GOV", "SEC", "OPS", "AID")
EXPECTED_GATES = {
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
EXPECTED_FACTS = {
    "privacy_control_level": ("GOV", "integer"),
    "ownership_control_level": ("STR", "integer"),
    "critical_lineage": ("LIN", "boolean"),
    "reproducible_versioned": ("AID", "boolean"),
}


def _unique_ids(items: object, *, context: str) -> set[str]:
    if not isinstance(items, list):
        raise ContentValidationError(f"{context}: expected a list")
    ids: list[str] = []
    for item in items:
        if not isinstance(item, Mapping) or not isinstance(item.get("id"), str):
            raise ContentValidationError(f"{context}: every item requires an ID")
        ids.append(item["id"])
    if len(ids) != len(set(ids)):
        raise ContentValidationError(f"{context}: duplicate IDs")
    return set(ids)


def _require_refs(values: Iterable[object], allowed: set[str], *, context: str) -> None:
    for value in values:
        if not isinstance(value, str) or value not in allowed:
            raise ContentValidationError(f"{context}: unresolved reference {value!r}")


def _anchors(value: object, *, context: str) -> None:
    if not isinstance(value, Mapping) or set(value) != {str(level) for level in range(5)}:
        raise ContentValidationError(f"{context}: anchors must contain exactly levels 0-4")


def validate_framework_semantics(document: Mapping[str, Any]) -> None:
    if (
        document.get("schema_version") != SCHEMA_VERSION
        or document.get("framework_version") != FRAMEWORK_VERSION
    ):
        raise ContentValidationError("framework: unsupported schema/framework version isolation")

    domains = document.get("domains")
    domain_ids = _unique_ids(domains, context="domains")
    if not isinstance(domains, list) or tuple(item["id"] for item in domains) != DOMAIN_ORDER:
        raise ContentValidationError("domains: exact v1 order and coverage are required")
    for domain in domains:
        _anchors(domain.get("anchors"), context=f"domain {domain['id']}")

    questions = document.get("questions")
    _unique_ids(questions, context="questions")
    if not isinstance(questions, list) or len(questions) != 30:
        raise ContentValidationError("questions: exactly 30 are required")
    counts: Counter[str] = Counter()
    for question in questions:
        domain_id = question.get("domain_id")
        if domain_id not in domain_ids:
            raise ContentValidationError(f"question {question.get('id')}: unknown domain")
        counts[domain_id] += 1
        _anchors(question.get("anchors"), context=f"question {question.get('id')}")
    if counts != Counter({domain_id: 3 for domain_id in DOMAIN_ORDER}):
        raise ContentValidationError("questions: exactly three per domain are required")

    gate_bundle = document.get("gate_bundle")
    if not isinstance(gate_bundle, Mapping):
        raise ContentValidationError("gate_bundle: missing")
    gate_ids = _unique_ids(gate_bundle.get("rules"), context="gate rules")
    fact_ids = _unique_ids(document.get("diagnostic_facts"), context="diagnostic facts")
    if gate_ids != set(EXPECTED_GATES):
        raise ContentValidationError("gate rules: exact v1 rule set is required")
    if fact_ids != set(EXPECTED_FACTS):
        raise ContentValidationError("diagnostic facts: exact v1 fact set is required")
    architectures = _unique_ids(document.get("architectures"), context="architectures")
    recommendations = _unique_ids(document.get("recommendations"), context="recommendations")
    _unique_ids(document.get("finding_rules"), context="finding rules")
    _unique_ids(document.get("technology_mappings"), context="technology mappings")
    demo_stage_ids = set(document.get("demo_stage_ids", []))

    for gate in gate_bundle["rules"]:
        actual = (
            gate.get("operand_id"),
            gate.get("source"),
            gate.get("operator"),
            gate.get("threshold"),
            gate.get("cap"),
        )
        if actual != EXPECTED_GATES[gate["id"]]:
            raise ContentValidationError(f"gate {gate['id']}: v1 semantics changed")
        operand = gate.get("operand_id")
        if gate.get("source") == "domain_score":
            _require_refs([str(operand).removeprefix("domain.")], domain_ids, context="gate")
        elif gate.get("source") == "diagnostic_fact":
            _require_refs([str(operand).removeprefix("fact.")], fact_ids, context="gate")
        else:
            raise ContentValidationError("gate: unsupported operand source")
    for fact in document["diagnostic_facts"]:
        if (fact.get("domain_id"), fact.get("type")) != EXPECTED_FACTS[fact["id"]]:
            raise ContentValidationError(f"diagnostic fact {fact['id']}: v1 semantics changed")

    for recommendation in document["recommendations"]:
        _require_refs(
            [recommendation.get("architecture_id")],
            architectures,
            context="recommendation",
        )
        _require_refs(
            recommendation.get("demo_stage_ids", []),
            demo_stage_ids,
            context="recommendation",
        )
    for rule in document["finding_rules"]:
        _require_refs([rule.get("recommendation_id")], recommendations, context="finding rule")
        if rule.get("gate_id") is not None:
            _require_refs([rule["gate_id"]], gate_ids, context="finding rule")
    for mapping in document["technology_mappings"]:
        _require_refs([mapping.get("architecture_id")], architectures, context="technology mapping")
        _require_refs(
            mapping.get("recommendation_ids", []),
            recommendations,
            context="technology mapping",
        )
    if tuple(document.get("report_sections", [])) != REPORT_SECTION_IDS:
        raise ContentValidationError("report sections: canonical v1 order is required")
