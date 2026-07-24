from __future__ import annotations

import copy

import pytest

from assessment.domain.errors import ContentValidationError
from assessment.engine.evaluator import evaluate_assessment
from assessment.engine.gates import evaluate_gates
from assessment.engine.maturity import evaluate_maturity
from assessment.frameworks import load_framework
from assessment.storage.migrations import _prototype_to_v1
from prototype import run as prototype


@pytest.mark.parametrize(
    ("rule_id", "domain_index", "fact_id", "fact_value", "cap"),
    [
        ("G-QUALITY", 4, None, None, 1),
        ("G-SECURITY", 7, None, None, 1),
        ("G-PRIVACY", None, "privacy_control_level", 1, 1),
        ("G-GOVERNANCE", 6, None, None, 2),
        ("G-OWNERSHIP", None, "ownership_control_level", 1, 2),
        ("G-LINEAGE", None, "critical_lineage", False, 2),
        ("G-REPRODUCIBILITY", None, "reproducible_versioned", False, 2),
    ],
)
def test_each_rule_has_operand_provenance_and_independent_cap(
    rule_id: str,
    domain_index: int | None,
    fact_id: str | None,
    fact_value: int | bool | None,
    cap: int,
) -> None:
    prototype_framework = prototype.load_framework()
    fixture = copy.deepcopy(
        prototype.load_scenarios(prototype_framework)[
            "strong-engineering-no-ai-operating-model"
        ]["architect-a"]
    )
    fixture["ratings"] = [3] * 30
    fixture["evidence_statuses"] = ["Evidenced"] * 30
    fixture["diagnostic_facts"] = {
        "privacy_control_level": 3,
        "ownership_control_level": 3,
        "critical_lineage": True,
        "reproducible_versioned": True,
    }
    if domain_index is not None:
        fixture["ratings"][domain_index * 3 : domain_index * 3 + 3] = [1, 1, 1]
    if fact_id is not None:
        fixture["diagnostic_facts"][fact_id] = fact_value
    answers = _prototype_to_v1(fixture, "gate-test")["assessment/quick.json"]
    framework = load_framework("1.0.0")
    result = evaluate_gates(
        evaluate_maturity(answers, framework),
        answers["diagnostic_facts"],
        framework,
    )
    traces = {trace.rule_id: trace for trace in result.traces}
    assert len(traces) == 7
    assert traces[rule_id].triggered is True
    assert traces[rule_id].applied_cap == cap
    assert traces[rule_id].operand_provenance
    assert all(trace.final_level == result.final_level for trace in traces.values())


def test_combined_rules_select_minimum_cap_without_short_circuiting() -> None:
    prototype_framework = prototype.load_framework()
    fixture = copy.deepcopy(
        prototype.load_scenarios(prototype_framework)[
            "strong-engineering-no-ai-operating-model"
        ]["architect-a"]
    )
    fixture["ratings"] = [3] * 30
    fixture["evidence_statuses"] = ["Evidenced"] * 30
    fixture["ratings"][18:21] = [1, 1, 1]
    fixture["ratings"][21:24] = [1, 1, 1]
    fixture["diagnostic_facts"]["critical_lineage"] = False
    answers = _prototype_to_v1(fixture, "combined-gate-test")["assessment/quick.json"]
    framework = load_framework("1.0.0")
    result = evaluate_gates(
        evaluate_maturity(answers, framework), answers["diagnostic_facts"], framework
    )
    assert result.final_level == 1
    assert result.selected_cap == 1
    assert sum(trace.triggered for trace in result.traces) >= 3
    assert len(result.traces) == 7


@pytest.mark.parametrize(
    ("fact_id", "value"),
    [
        ("privacy_control_level", None),
        ("ownership_control_level", None),
        ("critical_lineage", None),
        ("reproducible_versioned", None),
    ],
)
def test_required_diagnostic_facts_cannot_bypass_gates(
    fact_id: str,
    value: None,
) -> None:
    fixture = copy.deepcopy(
        prototype.load_scenarios(prototype.load_framework())[
            "strong-engineering-no-ai-operating-model"
        ]["architect-a"]
    )
    fixture["ratings"] = [4] * 30
    fixture["evidence_statuses"] = ["Evidenced"] * 30
    fixture["diagnostic_facts"][fact_id] = value
    answers = _prototype_to_v1(fixture, "required-fact-test")[
        "assessment/quick.json"
    ]
    with pytest.raises(ContentValidationError, match="must be answered"):
        evaluate_assessment(answers, load_framework("1.0.0"))


def test_domain_operand_provenance_is_resolvable_json_pointer() -> None:
    fixture = copy.deepcopy(
        prototype.load_scenarios(prototype.load_framework())[
            "strong-engineering-no-ai-operating-model"
        ]["architect-a"]
    )
    answers = _prototype_to_v1(fixture, "provenance-test")[
        "assessment/quick.json"
    ]
    answers["answers"].reverse()
    result = evaluate_assessment(answers, load_framework("1.0.0"))
    domain_trace = next(
        trace for trace in result.gates.traces if trace.operand_id.startswith("domain.")
    )
    capability_id = domain_trace.operand_id.removeprefix("domain.")
    expected_question_ids = {
        question["id"]
        for question in load_framework("1.0.0").questions
        if question["domain_id"] == capability_id
    }
    actual_question_ids = set()
    for reference in domain_trace.operand_provenance:
        index = int(reference.rsplit("/", 1)[-1])
        actual_question_ids.add(answers["answers"][index]["question_id"])
    assert actual_question_ids == expected_question_ids
