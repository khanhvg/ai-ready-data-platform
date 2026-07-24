from __future__ import annotations

import json
from pathlib import Path

import assessment.cli as assessment_cli
from assessment.cli import main
from assessment.engine.evaluator import evaluate_assessment
from assessment.frameworks import load_framework
from assessment.storage.migrations import migrate_prototype_fixture
from prototype import run as prototype


def test_migrated_v1_scenarios_preserve_intended_phase_one_results(tmp_path: Path) -> None:
    framework = load_framework("1.0.0")
    prototype_framework = prototype.load_framework()
    scenarios = prototype.load_scenarios(prototype_framework)
    golden_root = prototype.ASSESSMENT_ROOT / "tests" / "fixtures" / "scenarios" / "1.0.0"
    v1_expected = json.loads((golden_root / "expected.json").read_text())
    deltas = json.loads((golden_root / "phase-1-to-v1-deltas.json").read_text())
    assert deltas["unchanged_truth"] == [
        "domain_scores",
        "pre_gate_readiness",
        "final_readiness",
        "triggered_gates",
        "finding_membership",
    ]
    for scenario_id, scenario in scenarios.items():
        for rater_id in ("architect-a", "architect-b"):
            engagement = tmp_path / f"{scenario_id}-{rater_id}"
            source = prototype.FIXTURE_ROOT / scenario_id / f"{rater_id}.json"
            migrate_prototype_fixture(source, engagement)
            answers = json.loads((engagement / "assessment/quick.json").read_text())
            result = evaluate_assessment(answers, framework)
            expected = scenario["expected"][rater_id]
            assert [item.score for item in result.maturity.capabilities] == expected[
                "domain_scores"
            ]
            assert result.maturity.pre_gate_level == expected["pre_gate_readiness"]
            assert result.gates.final_level == expected["final_readiness"]
            assert {item.id for item in result.findings} == set(expected["finding_ids"])
            actual_v1 = {
                "domain_scores": [item.score for item in result.maturity.capabilities],
                "pre_gate_readiness": result.maturity.pre_gate_level,
                "final_readiness": result.gates.final_level,
                "triggered_gates": [
                    item.rule_id for item in result.gates.traces if item.triggered
                ],
                "finding_ids": [item.id for item in result.findings],
                "presentation_score": result.maturity.presentation_score,
            }
            assert actual_v1 == v1_expected[scenario_id][rater_id]


def test_cli_evaluate_and_report_write_only_below_explicit_output_root(
    tmp_path: Path,
) -> None:
    source = prototype.FIXTURE_ROOT / "startup-no-governance" / "architect-a.json"
    engagement = tmp_path / "engagement"
    migrate_prototype_fixture(source, engagement)
    output = tmp_path / "output"
    assert (
        main(
            [
                "evaluate",
                "--engagement-root",
                str(engagement),
                "--output-root",
                str(output),
            ]
        )
        == 0
    )
    assert (output / "assessment-result.json").is_file()
    assert (
        main(
            [
                "report",
                "--engagement-root",
                str(engagement),
                "--output-root",
                str(output),
            ]
        )
        == 0
    )
    assert (output / "report.json").is_file()
    assert (output / "report.html").is_file()
    assert not (engagement / "reports").exists()
    second_output = tmp_path / "second-output"
    assert (
        main(
            [
                "report",
                "--engagement-root",
                str(engagement),
                "--output-root",
                str(second_output),
            ]
        )
        == 0
    )
    assert (second_output / "report.json").read_bytes() == (
        output / "report.json"
    ).read_bytes()
    assert (second_output / "report.html").read_bytes() == (
        output / "report.html"
    ).read_bytes()


def test_cli_rejects_output_aliasing_source_state(
    tmp_path: Path, capsys: object
) -> None:
    source = prototype.FIXTURE_ROOT / "startup-no-governance" / "architect-a.json"
    engagement = tmp_path / "engagement"
    migrate_prototype_fixture(source, engagement)
    assert (
        main(
            [
                "report",
                "--engagement-root",
                str(engagement),
                "--output-root",
                str(engagement / "assessment"),
            ]
        )
        != 0
    )
    captured = capsys.readouterr()
    error = json.loads(captured.err)
    assert error["error"]["code"] == "unsafe_output_root"


def test_cli_rejects_symlink_output_root(
    tmp_path: Path, capsys: object
) -> None:
    source = prototype.FIXTURE_ROOT / "startup-no-governance" / "architect-a.json"
    engagement = tmp_path / "engagement"
    migrate_prototype_fixture(source, engagement)
    real_output = tmp_path / "real-output"
    real_output.mkdir()
    linked_output = tmp_path / "linked-output"
    linked_output.symlink_to(real_output, target_is_directory=True)
    assert (
        main(
            [
                "evaluate",
                "--engagement-root",
                str(engagement),
                "--output-root",
                str(linked_output),
            ]
        )
        != 0
    )
    error = json.loads(capsys.readouterr().err)
    assert error["error"]["code"] == "unsafe_output_root"
    assert not (real_output / "assessment-result.json").exists()


def test_cli_usage_and_malformed_reviews_are_machine_readable(
    tmp_path: Path,
    capsys: object,
) -> None:
    assert main(["evaluate", "--engagement-root", str(tmp_path)]) != 0
    usage_error = json.loads(capsys.readouterr().err)
    assert usage_error["error"]["code"] == "assessment_error"
    assert "invalid_arguments" in usage_error["error"]["message"]

    source = prototype.FIXTURE_ROOT / "startup-no-governance" / "architect-a.json"
    engagement = tmp_path / "engagement"
    migrate_prototype_fixture(source, engagement)
    review_path = engagement / "findings" / "review.json"
    review_path.parent.mkdir()
    review_path.write_text(
        json.dumps(
            {
                "reviews": {
                    "F-QUALITY": {
                        "state": "edit-note",
                        "edit_note": 7,
                    }
                }
            }
        )
    )
    assert (
        main(
            [
                "evaluate",
                "--engagement-root",
                str(engagement),
                "--output-root",
                str(tmp_path / "output"),
            ]
        )
        != 0
    )
    review_error = json.loads(capsys.readouterr().err)
    assert review_error["error"]["code"] == "assessment_error"


def test_report_publication_failure_restores_coherent_artifact_set(
    tmp_path: Path,
    monkeypatch: object,
) -> None:
    source = prototype.FIXTURE_ROOT / "startup-no-governance" / "architect-a.json"
    engagement = tmp_path / "engagement"
    migrate_prototype_fixture(source, engagement)
    output = tmp_path / "output"
    arguments = [
        "report",
        "--engagement-root",
        str(engagement),
        "--output-root",
        str(output),
    ]
    assert main(arguments) == 0
    names = ("report.json", "report.html", "report-manifest.json")
    baseline = {name: (output / name).read_bytes() for name in names}
    real_write = assessment_cli.atomic_write_at
    writes = 0

    def fail_second_write(
        output_descriptor: int,
        name: str,
        content: bytes,
    ) -> None:
        nonlocal writes
        writes += 1
        if writes == 2:
            raise OSError("injected second-artifact failure")
        real_write(output_descriptor, name, content)

    monkeypatch.setattr(assessment_cli, "atomic_write_at", fail_second_write)
    assert main(arguments) != 0
    assert {name: (output / name).read_bytes() for name in names} == baseline
