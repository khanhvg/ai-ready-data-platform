from __future__ import annotations

import copy
import json
import re
from html.parser import HTMLParser

import pytest

from assessment.reporting.generator import generate_report
from assessment.reporting.renderer import render_report
from assessment.storage.migrations import _prototype_to_v1
from prototype import run as prototype


class StructuralParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.main_count = 0
        self.section_ids: list[str] = []
        self.table_captions: list[str] = []
        self._in_caption = False

    def handle_starttag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        values = dict(attrs)
        if tag == "main":
            self.main_count += 1
        if tag == "section" and values.get("id"):
            self.section_ids.append(str(values["id"]))
        if tag == "caption":
            self._in_caption = True

    def handle_endtag(self, tag: str) -> None:
        if tag == "caption":
            self._in_caption = False

    def handle_data(self, data: str) -> None:
        if self._in_caption and data.strip():
            self.table_captions.append(data.strip())


def _source() -> tuple[dict[str, object], dict[str, object]]:
    framework = prototype.load_framework()
    fixture = copy.deepcopy(
        prototype.load_scenarios(framework)["startup-no-governance"]["architect-a"]
    )
    documents = _prototype_to_v1(fixture, "report-test")
    return documents["engagement.json"], documents["assessment/quick.json"]


def test_report_has_exact_sections_provenance_digest_and_safe_stable_html() -> None:
    engagement, answers = _source()
    first = generate_report(engagement, answers)
    second = generate_report(engagement, answers)
    assert first.json_bytes == second.json_bytes
    assert first.source_state_digest == second.source_state_digest
    report = json.loads(first.json_bytes)
    assert [section["id"] for section in report["sections"]] == list(
        prototype.REPORT_SECTION_IDS
    )
    appendix = report["sections"][-1]["content"]
    assert appendix["source_state_digest"] == first.source_state_digest
    assert set(appendix["provenance_classes"]) == {
        "customer answer",
        "customer evidence",
        "architect judgment",
        "demo illustration",
    }
    sections = {section["id"]: section["content"] for section in report["sections"]}
    assert all(
        item["provenance_class"] == "architect judgment"
        for item in sections["reference-diagrams"]["items"]
    )
    assert all(
        item["provenance_class"] == "architect judgment"
        for item in sections["technology-options"]["items"]
    )
    assert all(
        item["demo_provenance_class"] == "demo illustration"
        for item in sections["findings"]["items"]
    )
    html_a = render_report(report)
    html_b = render_report(report)
    assert html_a == html_b
    text = html_a.decode()
    assert "report-test" in text
    assert "Q-STR-01" in text
    assert "DEMO-PLACEHOLDER-QUALITY" in text
    assert "Self-reported:" in text
    assert "critical_lineage" in text
    assert "<svg" in text and "Diagram data table" in text
    assert "@media print" in text
    assert not re.search(r"(?i)<(?:script|form|iframe|object|embed)\b", text)
    assert not re.search(r"(?i)(?:https?:|//|@font-face|telemetry)", text)
    assert not re.search(r"(?i)\s(?:src|href|on[a-z]+)\s*=", text)
    parser = StructuralParser()
    parser.feed(text)
    assert parser.main_count == 1
    assert parser.section_ids == list(prototype.REPORT_SECTION_IDS)
    assert "Diagram data table" in parser.table_captions


def test_source_digest_tracks_evidence_but_excludes_generated_reports() -> None:
    engagement, answers = _source()
    baseline = generate_report(
        engagement,
        answers,
        source_snapshot={
            "assessment/quick.json": "answers-digest",
            "evidence/files/proof.txt": "proof-a",
            "reports/report.json": "generated-a",
        },
    )
    report_only_change = generate_report(
        engagement,
        answers,
        source_snapshot={
            "assessment/quick.json": "answers-digest",
            "evidence/files/proof.txt": "proof-a",
            "reports/report.json": "generated-b",
        },
    )
    evidence_change = generate_report(
        engagement,
        answers,
        source_snapshot={
            "assessment/quick.json": "answers-digest",
            "evidence/files/proof.txt": "proof-b",
            "reports/report.json": "generated-a",
        },
    )
    assert report_only_change.source_state_digest == baseline.source_state_digest
    assert evidence_change.source_state_digest != baseline.source_state_digest


def test_authored_markdown_and_credential_uri_are_rejected() -> None:
    engagement, answers = _source()
    answers["answers"][0]["note"] = "<script>unsafe</script>"
    try:
        generate_report(engagement, answers)
    except ValueError as error:
        assert "raw HTML" in str(error)
    else:
        raise AssertionError("raw HTML must be rejected")

    engagement, answers = _source()
    answers["answers"][0]["note"] = "See https://user:password@example.invalid/proof"
    try:
        generate_report(engagement, answers)
    except ValueError as error:
        assert "credential" in str(error).lower() or "secret" in str(error).lower()
    else:
        raise AssertionError("credential URI must be rejected")


def test_plain_text_url_is_rendered_without_becoming_a_remote_resource() -> None:
    engagement, answers = _source()
    answers["answers"][0]["note"] = (
        "Public reference: https://example.invalid/control-evidence"
    )
    html = render_report(json.loads(generate_report(engagement, answers).json_bytes))
    assert b"https://example.invalid/control-evidence" in html
    assert b"href=" not in html


def test_literal_attribute_policy_text_remains_inert() -> None:
    engagement, answers = _source()
    answers["answers"][0]["note"] = (
        "Record the literal href= and onclick= attribute policy in the evidence."
    )
    html = render_report(json.loads(generate_report(engagement, answers).json_bytes))
    assert b"literal href= and onclick= attribute policy" in html


def test_incomplete_coverage_renders_not_assessed_without_python_none() -> None:
    engagement, answers = _source()
    answers["answers"] = answers["answers"][:1]
    html = render_report(json.loads(generate_report(engagement, answers).json_bytes))
    assert b"None \xe2\x80\x94 Not assessed" not in html
    assert html.count(b"<dd>Not assessed</dd>") >= 2


def test_report_rejects_contract_extras_and_cross_engagement_answers() -> None:
    engagement, answers = _source()
    engagement["organization_name"] = "forbidden"
    with pytest.raises(ValueError, match="Extra inputs"):
        generate_report(engagement, answers)

    engagement, answers = _source()
    answers["engagement_id"] = "another-engagement"
    with pytest.raises(ValueError, match="IDs differ"):
        generate_report(engagement, answers)
