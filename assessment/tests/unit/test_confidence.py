from __future__ import annotations

import copy

from assessment.engine.confidence import summarize_confidence
from assessment.engine.evaluator import evaluate_assessment
from assessment.frameworks import load_framework
from assessment.storage.migrations import _prototype_to_v1
from prototype import run as prototype


def test_conflicting_evidence_is_conservative_and_distinct_from_maturity() -> None:
    framework = prototype.load_framework()
    fixture = prototype.load_scenarios(framework)["enterprise-lake-weak-quality"]["architect-a"]
    document = _prototype_to_v1(fixture, "confidence-test")["assessment/quick.json"]
    document["answers"][0]["evidence_status"] = "Conflicting evidence"
    result = summarize_confidence(document, load_framework("1.0.0"))
    assert result.capabilities[0].least_assured_assessed_status == "Conflicting evidence"
    assert result.capabilities[0].distribution["Conflicting evidence"] == 1
    assert "Resolve conflicting evidence" in result.capabilities[0].next_action


def test_confidence_mutations_do_not_change_maturity_gates_or_priority() -> None:
    prototype_framework = prototype.load_framework()
    fixture = prototype.load_scenarios(prototype_framework)["startup-no-governance"][
        "architect-a"
    ]
    baseline_document = _prototype_to_v1(fixture, "confidence-invariance")[
        "assessment/quick.json"
    ]
    changed_document = copy.deepcopy(baseline_document)
    changed_document["answers"][0]["evidence_status"] = "Conflicting evidence"
    framework = load_framework("1.0.0")
    baseline = evaluate_assessment(baseline_document, framework)
    changed = evaluate_assessment(changed_document, framework)
    assert changed.maturity == baseline.maturity
    assert changed.gates == baseline.gates
    assert [(item.id, item.priority) for item in changed.findings] == [
        (item.id, item.priority) for item in baseline.findings
    ]
    assert changed.confidence != baseline.confidence


def test_missing_answers_are_reported_as_not_assessed_coverage() -> None:
    prototype_framework = prototype.load_framework()
    fixture = prototype.load_scenarios(prototype_framework)["enterprise-lake-weak-quality"][
        "architect-a"
    ]
    document = _prototype_to_v1(fixture, "confidence-missing")["assessment/quick.json"]
    document["answers"] = document["answers"][3:]
    result = summarize_confidence(document, load_framework("1.0.0"))
    assert result.capabilities[0].assessed_count == 0
    assert result.capabilities[0].not_assessed_count == 3
    assert result.capabilities[0].least_assured_assessed_status is None
