from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path

import pytest

from prototype import run as prototype


@pytest.fixture(scope="module")
def framework() -> prototype.Framework:
    return prototype.load_framework()


@pytest.fixture(scope="module")
def scenarios(framework: prototype.Framework) -> dict[str, dict[str, object]]:
    return prototype.load_scenarios(framework)


def changed_framework(
    framework: prototype.Framework,
    field: str,
    value: dict[str, object],
) -> prototype.Framework:
    values = {
        "capabilities": framework.capabilities,
        "questions": framework.questions,
        "readiness": framework.readiness,
        "gates": framework.gates,
        "finding_rules": framework.finding_rules,
        "recommendations": framework.recommendations,
    }
    values[field] = value
    return prototype.Framework(**values)


def test_exact_content_counts_and_order(framework: prototype.Framework) -> None:
    domains = framework.capabilities["domains"]
    questions = framework.questions["questions"]
    assert tuple(domain["id"] for domain in domains) == prototype.DOMAIN_ORDER
    assert len(domains) == 10
    assert sum(len(domain["anchors"]) for domain in domains) == 50
    assert len(questions) == 30
    assert sum(len(question["anchors"]) for question in questions) == 150
    assert tuple(question["id"] for question in questions) == tuple(
        f"Q-{domain_id}-{question_number:02d}"
        for domain_id in prototype.DOMAIN_ORDER
        for question_number in range(1, 4)
    )


def test_all_synthetic_expected_results_are_recomputed(
    scenarios: dict[str, dict[str, object]],
    framework: prototype.Framework,
) -> None:
    assert prototype.assert_expected(scenarios, framework) == {
        "scenario_raters": 8,
        "assertions": 48,
    }
    for scenario in scenarios.values():
        for rater_id in ("architect-a", "architect-b"):
            fixture = scenario[rater_id]
            result = prototype.evaluate_fixture(fixture, framework)
            assert result["coverage"]["complete"] is True
            assert fixture["duration_minutes"] <= 60
            assert len(result["gate_traces"]) == 7
            assert all(trace["explanation"] for trace in result["gate_traces"])
            assert all(
                trace["final_state"] == result["final_readiness"] for trace in result["gate_traces"]
            )
            for finding in result["findings"]:
                assert finding["impact"]
                assert finding["priority"]
                assert finding["recommendation"]
                assert finding["architecture_reference"]
                assert finding["action"]
                assert finding["evidence_validation_action"]


def test_coverage_failure_suppresses_overall_readiness(
    scenarios: dict[str, dict[str, object]],
    framework: prototype.Framework,
) -> None:
    fixture = copy.deepcopy(scenarios["startup-no-governance"]["architect-a"])
    fixture["ratings"][0:2] = [None, None]
    fixture["evidence_statuses"][0:2] = ["Not assessed", "Not assessed"]
    result = prototype.evaluate_fixture(fixture, framework, validate=False)
    assert result["coverage"]["complete"] is False
    assert result["pre_gate_readiness"] is None
    assert result["final_readiness"] is None
    assert result["presentation_score"] is None


@pytest.mark.parametrize(
    ("rule_id", "mutation"),
    [
        ("G-QUALITY", ("ratings", slice(12, 15), [1, 1, 1])),
        ("G-SECURITY", ("ratings", slice(21, 24), [1, 1, 1])),
        ("G-PRIVACY", ("fact", "privacy_control_level", 1)),
        ("G-GOVERNANCE", ("ratings", slice(18, 21), [1, 1, 1])),
        ("G-OWNERSHIP", ("fact", "ownership_control_level", 1)),
        ("G-LINEAGE", ("fact", "critical_lineage", False)),
        ("G-REPRODUCIBILITY", ("fact", "reproducible_versioned", False)),
    ],
)
def test_each_gate_is_independently_traced(
    scenarios: dict[str, dict[str, object]],
    framework: prototype.Framework,
    rule_id: str,
    mutation: tuple[str, object, object],
) -> None:
    fixture = copy.deepcopy(scenarios["strong-engineering-no-ai-operating-model"]["architect-a"])
    fixture["diagnostic_facts"]["reproducible_versioned"] = True
    kind, key, value = mutation
    if kind == "ratings":
        fixture["ratings"][key] = value
    else:
        fixture["diagnostic_facts"][key] = value
    result = prototype.evaluate_fixture(fixture, framework, validate=False)
    traces = {trace["rule_id"]: trace for trace in result["gate_traces"]}
    assert traces[rule_id]["triggered"] is True
    assert traces[rule_id]["operand_source"] in {"domain_score", "diagnostic_fact"}
    assert traces[rule_id]["explanation"]
    assert all(trace["final_state"] == result["final_readiness"] for trace in traces.values())


def test_most_restrictive_gate_wins_without_raising_pre_gate(
    scenarios: dict[str, dict[str, object]],
    framework: prototype.Framework,
) -> None:
    fixture = copy.deepcopy(scenarios["enterprise-lake-weak-quality"]["architect-a"])
    fixture["ratings"][12:15] = [2, 2, 2]
    fixture["diagnostic_facts"]["critical_lineage"] = False
    result = prototype.evaluate_fixture(fixture, framework, validate=False)
    assert result["pre_gate_readiness"] == 2
    assert result["final_readiness"] == 2
    fixture["diagnostic_facts"]["privacy_control_level"] = 1
    result = prototype.evaluate_fixture(fixture, framework, validate=False)
    assert result["final_readiness"] == 1


@pytest.mark.parametrize(
    ("rule_id", "mutation"),
    [
        ("G-GOVERNANCE", ("ratings", slice(18, 21), [1, 1, 1])),
        ("G-OWNERSHIP", ("fact", "ownership_control_level", 1)),
        ("G-LINEAGE", ("fact", "critical_lineage", False)),
        ("G-REPRODUCIBILITY", ("fact", "reproducible_versioned", False)),
    ],
)
def test_cap_two_gates_reduce_pre_gate_three(
    scenarios: dict[str, dict[str, object]],
    framework: prototype.Framework,
    rule_id: str,
    mutation: tuple[str, object, object],
) -> None:
    fixture = copy.deepcopy(scenarios["strong-engineering-no-ai-operating-model"]["architect-a"])
    fixture["diagnostic_facts"] = {
        "privacy_control_level": 3,
        "ownership_control_level": 3,
        "critical_lineage": True,
        "reproducible_versioned": True,
    }
    kind, key, value = mutation
    if kind == "ratings":
        fixture["ratings"] = [4] * 30
        fixture["ratings"][key] = value
    else:
        fixture["ratings"] = [3] * 30
        fixture["diagnostic_facts"][key] = value
    result = prototype.evaluate_fixture(fixture, framework, validate=False)
    traces = {trace["rule_id"]: trace for trace in result["gate_traces"]}
    assert result["pre_gate_readiness"] == 3
    assert traces[rule_id]["triggered"] is True
    assert traces[rule_id]["applied_cap"] == 2
    assert result["final_readiness"] == 2


def test_confidence_is_independent_from_maturity(
    scenarios: dict[str, dict[str, object]],
    framework: prototype.Framework,
) -> None:
    fixture = copy.deepcopy(scenarios["enterprise-lake-weak-quality"]["architect-a"])
    baseline = prototype.evaluate_fixture(fixture, framework)
    fixture["evidence_statuses"] = ["Self-reported"] * 30
    changed = prototype.evaluate_fixture(fixture, framework)
    assert changed["domain_scores"] == baseline["domain_scores"]
    assert changed["final_readiness"] == baseline["final_readiness"]
    assert changed["confidence"] != baseline["confidence"]


def test_priority_decision_table(framework: prototype.Framework) -> None:
    table = framework.finding_rules["priority_decision_table"]
    assert prototype.priority_for(0, table) == "High-priority foundation"
    assert (
        prototype.priority_for(1, table, cross_domain_blocker=True)
        == "High-priority foundation"
    )
    assert prototype.priority_for(2, table) == "Near-term improvement"
    assert prototype.priority_for(3, table, target_level_four=True) == "Strategic enhancement"
    assert prototype.priority_for(4, table) is None
    assert prototype.priority_for(3, table, gate_cap=2) == "Critical blocker"


@pytest.mark.parametrize(
    "mutator",
    [
        lambda fixture: fixture.update({"scenario_id": "<img src=x>"}),
        lambda fixture: fixture.update({"organization_name": "https://invalid.example"}),
        lambda fixture: fixture.update({"organization_name": "/var/tmp/private"}),
        lambda fixture: fixture.update({"organization_name": "AKIAABCDEFGHIJKLMNOP"}),
        lambda fixture: fixture.update({"organization_name": "token=not-a-real-secret-value"}),
        lambda fixture: fixture.update({"duration_minutes": 61}),
        lambda fixture: fixture.update({"diagnostic_facts": {"critical_lineage": True}}),
        lambda fixture: fixture["ratings"].__setitem__(0, 5),
        lambda fixture: fixture["evidence_statuses"].__setitem__(0, "Not assessed"),
    ],
)
def test_fixture_validation_rejects_unsafe_or_malformed_data(
    scenarios: dict[str, dict[str, object]],
    framework: prototype.Framework,
    mutator: object,
) -> None:
    fixture = copy.deepcopy(scenarios["startup-no-governance"]["architect-a"])
    mutator(fixture)
    with pytest.raises(prototype.ValidationError):
        prototype.validate_fixture(fixture, framework)


def test_semantic_validation_rejects_duplicate_and_missing_content(
    framework: prototype.Framework,
) -> None:
    capabilities = copy.deepcopy(framework.capabilities)
    capabilities["domains"][1]["id"] = capabilities["domains"][0]["id"]
    with pytest.raises(prototype.ValidationError):
        prototype.validate_framework(changed_framework(framework, "capabilities", capabilities))

    capabilities = copy.deepcopy(framework.capabilities)
    del capabilities["domains"][0]["anchors"][4]
    with pytest.raises(prototype.ValidationError):
        prototype.validate_framework(changed_framework(framework, "capabilities", capabilities))

    questions = copy.deepcopy(framework.questions)
    questions["questions"].pop()
    with pytest.raises(prototype.ValidationError):
        prototype.validate_framework(changed_framework(framework, "questions", questions))

    questions = copy.deepcopy(framework.questions)
    questions["questions"][3], questions["questions"][4] = (
        questions["questions"][4],
        questions["questions"][3],
    )
    with pytest.raises(prototype.ValidationError):
        prototype.validate_framework(changed_framework(framework, "questions", questions))

    questions = copy.deepcopy(framework.questions)
    questions["questions"][0]["domain_id"], questions["questions"][9]["domain_id"] = (
        questions["questions"][9]["domain_id"],
        questions["questions"][0]["domain_id"],
    )
    with pytest.raises(prototype.ValidationError):
        prototype.validate_framework(changed_framework(framework, "questions", questions))

    questions = copy.deepcopy(framework.questions)
    questions["questions"][0]["anchors"]["0"] = questions["questions"][0]["anchors"].pop(0)
    with pytest.raises(prototype.ValidationError):
        prototype.validate_framework(changed_framework(framework, "questions", questions))

    gates = copy.deepcopy(framework.gates)
    gates["rules"][0].pop("explanation")
    with pytest.raises(prototype.ValidationError):
        prototype.validate_framework(changed_framework(framework, "gates", gates))

    gates = copy.deepcopy(framework.gates)
    gates["rules"][0]["operand_id"] = "domain.AID"
    with pytest.raises(prototype.ValidationError):
        prototype.validate_framework(changed_framework(framework, "gates", gates))

    readiness = copy.deepcopy(framework.readiness)
    readiness["coverage"]["minimum_answered_total"] = 1
    with pytest.raises(prototype.ValidationError):
        prototype.validate_framework(changed_framework(framework, "readiness", readiness))

    readiness = copy.deepcopy(framework.readiness)
    readiness["levels"][3] = "Almost ready"
    with pytest.raises(prototype.ValidationError):
        prototype.validate_framework(changed_framework(framework, "readiness", readiness))

    gates = copy.deepcopy(framework.gates)
    gates["diagnostic_facts"][0]["maximum"] = 5
    with pytest.raises(prototype.ValidationError):
        prototype.validate_framework(changed_framework(framework, "gates", gates))

    finding_rules = copy.deepcopy(framework.finding_rules)
    finding_rules["rules"][0]["condition"]["operator"] = "contains"
    with pytest.raises(prototype.ValidationError):
        prototype.validate_framework(
            changed_framework(framework, "finding_rules", finding_rules)
        )

    finding_rules = copy.deepcopy(framework.finding_rules)
    finding_rules["priority_decision_table"]["triggered_gate"] = "Optional"
    with pytest.raises(prototype.ValidationError):
        prototype.validate_framework(
            changed_framework(framework, "finding_rules", finding_rules)
        )

    readiness = copy.deepcopy(framework.readiness)
    readiness["confidence"]["least_assured_precedence"].reverse()
    with pytest.raises(prototype.ValidationError):
        prototype.validate_framework(changed_framework(framework, "readiness", readiness))

    recommendations = copy.deepcopy(framework.recommendations)
    recommendations["recommendations"][0]["architecture_reference"] = "ARCH-MISSING"
    with pytest.raises(prototype.ValidationError):
        prototype.validate_framework(
            changed_framework(framework, "recommendations", recommendations)
        )


def test_report_generation_is_byte_stable_and_safe(
    tmp_path: Path,
    scenarios: dict[str, dict[str, object]],
    framework: prototype.Framework,
) -> None:
    stability = prototype.verify_report_stability(scenarios, framework, tmp_path)
    assert stability["byte_stable"] is True
    assert stability["artifacts"] == 36
    for scenario_id in scenarios:
        report = json.loads((tmp_path / scenario_id / "report.json").read_text())
        assert (
            tuple(section["id"] for section in report["sections"]) == prototype.REPORT_SECTION_IDS
        )
        html = (tmp_path / scenario_id / "report.html").read_text()
        assert "http://" not in html
        assert "https://" not in html
        assert "<script" not in html.lower()
        assert "<strong>Operand:</strong>" in html
        assert "<strong>Readiness trace:</strong>" in html
        assert "<strong>Gap:</strong>" in html
        assert "<strong>Demo reference:</strong>" in html


def test_template_escapes_report_content(framework: prototype.Framework) -> None:
    report = {
        "title": "<Unsafe title>",
        "framework_version": prototype.FRAMEWORK_VERSION,
        "rater_id": "architect-a",
        "sections": [
            {"id": section_id, "title": section_id, "content": {}}
            for section_id in prototype.REPORT_SECTION_IDS
        ],
    }
    html = prototype.render_report(report).decode()
    assert "<Unsafe title>" not in html
    assert "&lt;Unsafe title&gt;" in html


def test_prototype_migration_fixture_freeze() -> None:
    manifest_path = (
        prototype.ASSESSMENT_ROOT
        / "tests"
        / "fixtures"
        / "migration"
        / "0.1.0-prototype"
        / "manifest.json"
    )
    manifest = json.loads(manifest_path.read_text())
    records = []
    for record in manifest["records"]:
        path = prototype.ASSESSMENT_ROOT / record["path"]
        assert hashlib.sha256(path.read_bytes()).hexdigest() == record["sha256"]
        records.append(record)
    aggregate = hashlib.sha256(json.dumps(records, separators=(",", ":")).encode()).hexdigest()
    assert len(records) == manifest["frozen_files"] == 18
    assert aggregate == manifest["aggregate_sha256"]


def test_missing_fixture_root_fails_with_actionable_error(
    tmp_path: Path, framework: prototype.Framework
) -> None:
    with pytest.raises(prototype.ValidationError, match="--fixture-root"):
        prototype.load_scenarios(framework, tmp_path / "missing")
