from __future__ import annotations

from prototype import run as prototype


def test_calibration_exact_comparable_denominator_and_ratio() -> None:
    framework = prototype.load_framework()
    scenarios = prototype.load_scenarios(framework)
    summary = prototype.calibration_summary(scenarios, framework)
    assert summary["possible_question_slots"] == 120
    assert summary["comparable_pairs"] == 119
    assert summary["not_assessed_slots"] == 1
    assert summary["within_one_level_pairs"] == 117
    assert summary["within_one_level_percent"] == "98.3"
    assert summary["paired_domain_results_checked"] == 40
    assert summary["paired_final_readiness_results_checked"] == 4
    assert summary["largest_rating_deltas"] == [
        {
            "scenario_id": "strong-engineering-no-ai-operating-model",
            "question_id": "Q-STR-02",
            "delta": 2,
        },
        {
            "scenario_id": "strong-engineering-no-ai-operating-model",
            "question_id": "Q-AID-01",
            "delta": 2,
        },
    ]
