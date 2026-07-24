from __future__ import annotations

import copy

from assessment.engine.maturity import evaluate_maturity
from assessment.frameworks import load_framework
from assessment.storage.migrations import _prototype_to_v1
from prototype import run as prototype


def _answers() -> dict[str, object]:
    framework = prototype.load_framework()
    scenario = prototype.load_scenarios(framework)["strong-engineering-no-ai-operating-model"]
    return _prototype_to_v1(scenario["architect-a"], "maturity-test")["assessment/quick.json"]


def test_lower_median_coverage_labels_and_presentation_are_exact() -> None:
    result = evaluate_maturity(_answers(), load_framework("1.0.0"))
    assert [item.capability_id for item in result.capabilities] == list(prototype.DOMAIN_ORDER)
    assert result.coverage.complete is True
    assert result.pre_gate_level == 2
    assert result.pre_gate_label == "Experiment-ready only"
    assert result.presentation_score == "67.5"
    assert result.capabilities[0].source_question_ids == (
        "Q-STR-01",
        "Q-STR-02",
        "Q-STR-03",
    )
    assert result.capabilities[0].anchor


def test_missing_domain_is_not_assessed_and_suppresses_overall_values() -> None:
    document = copy.deepcopy(_answers())
    for answer in document["answers"][:2]:
        answer["rating"] = None
        answer["evidence_status"] = "Not assessed"
    result = evaluate_maturity(document, load_framework("1.0.0"))
    assert result.coverage.complete is False
    assert result.capabilities[0].score is None
    assert result.capabilities[0].label == "Not assessed"
    assert result.pre_gate_level is None
    assert result.presentation_score is None


def test_lower_median_ties_are_exact_for_every_rating_pair() -> None:
    framework = load_framework("1.0.0")
    for low in range(5):
        for high in range(low, 5):
            document = copy.deepcopy(_answers())
            document["answers"][0]["rating"] = high
            document["answers"][1]["rating"] = low
            document["answers"][2]["rating"] = None
            document["answers"][2]["evidence_status"] = "Not assessed"
            result = evaluate_maturity(document, framework)
            assert result.capabilities[0].score == low


def test_overall_coverage_threshold_is_separate_from_domain_coverage() -> None:
    document = copy.deepcopy(_answers())
    for domain_index in range(3):
        answer = document["answers"][domain_index * 3 + 2]
        answer["rating"] = None
        answer["evidence_status"] = "Not assessed"
    result = evaluate_maturity(document, load_framework("1.0.0"))
    assert all(count >= 2 for count in result.coverage.answered_by_capability.values())
    assert result.coverage.answered_total == 26
    assert result.coverage.complete is False


def test_duplicate_and_unknown_question_ids_fail_closed() -> None:
    duplicate = copy.deepcopy(_answers())
    duplicate["answers"][1]["question_id"] = duplicate["answers"][0]["question_id"]
    try:
        evaluate_maturity(duplicate, load_framework("1.0.0"))
    except ValueError as error:
        assert "duplicate question" in str(error)
    else:
        raise AssertionError("duplicate question IDs must fail")

    unknown = copy.deepcopy(_answers())
    unknown["answers"][0]["question_id"] = "Q-UNKNOWN-01"
    try:
        evaluate_maturity(unknown, load_framework("1.0.0"))
    except ValueError as error:
        assert "unknown question" in str(error)
    else:
        raise AssertionError("unknown question IDs must fail")
