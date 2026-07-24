from __future__ import annotations

import copy

import pytest

from assessment.engine.evaluator import evaluate_assessment
from assessment.frameworks import load_framework
from assessment.storage.migrations import _prototype_to_v1
from prototype import run as prototype


def test_demo_reference_mutation_cannot_change_engine_truth_or_priority() -> None:
    prototype_framework = prototype.load_framework()
    fixture = prototype.load_scenarios(prototype_framework)["startup-no-governance"][
        "architect-a"
    ]
    answers = _prototype_to_v1(fixture, "finding-test")["assessment/quick.json"]
    baseline_framework = load_framework("1.0.0")
    changed_framework = copy.deepcopy(baseline_framework)
    for recommendation in changed_framework.recommendations:
        recommendation["demo_reference"] = f"mutated-{recommendation['id']}"
    baseline = evaluate_assessment(answers, baseline_framework)
    changed = evaluate_assessment(answers, changed_framework)
    assert changed.maturity == baseline.maturity
    assert changed.gates == baseline.gates
    assert [(item.id, item.priority) for item in changed.findings] == [
        (item.id, item.priority) for item in baseline.findings
    ]


def test_architect_review_is_separate_from_generated_truth() -> None:
    prototype_framework = prototype.load_framework()
    fixture = prototype.load_scenarios(prototype_framework)["startup-no-governance"][
        "architect-a"
    ]
    answers = _prototype_to_v1(fixture, "review-test")["assessment/quick.json"]
    baseline = evaluate_assessment(answers, load_framework("1.0.0"))
    reviewed = evaluate_assessment(
        answers,
        load_framework("1.0.0"),
        reviews={
            baseline.findings[0].id: {
                "state": "defer",
                "edit_note": "Sequence after the control-owner workshop.",
            }
        },
    )
    assert reviewed.findings[0].generated_truth == baseline.findings[0].generated_truth
    assert reviewed.findings[0].review.state == "defer"
    assert reviewed.findings[0].review.edit_note


def test_accepted_level_four_target_makes_strategic_priority_reachable() -> None:
    fixture = copy.deepcopy(
        prototype.load_scenarios(prototype.load_framework())[
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
    answers = _prototype_to_v1(fixture, "target-four-test")[
        "assessment/quick.json"
    ]
    framework = load_framework("1.0.0")
    framework.finding_rules[0]["condition"] = {
        "operand": "domain.STR",
        "operator": "le",
        "threshold": 3,
    }
    framework.finding_rules[0]["priority_operand"] = "domain.STR"
    framework.finding_rules[0].pop("gate_id", None)
    result = evaluate_assessment(
        answers,
        framework,
        accepted_target_level=4,
    )
    assert result.findings[0].priority == "Strategic enhancement"


def test_stale_architect_review_cannot_be_silently_discarded() -> None:
    fixture = prototype.load_scenarios(prototype.load_framework())[
        "startup-no-governance"
    ]["architect-a"]
    answers = _prototype_to_v1(fixture, "stale-review-test")[
        "assessment/quick.json"
    ]
    with pytest.raises(ValueError, match="were not generated"):
        evaluate_assessment(
            answers,
            load_framework("1.0.0"),
            reviews={
                "F-NOT-GENERATED": {
                    "state": "defer",
                    "edit_note": "Preserve this decision.",
                }
            },
        )
