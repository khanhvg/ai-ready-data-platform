from __future__ import annotations

import re
from pathlib import Path

from fastapi.testclient import TestClient

from assessment.domain.deep_dives import DeepDiveAnswer
from assessment.web.app import create_app
from assessment.web.config import WebConfig
from assessment.web.dependencies import WebServices
from assessment.web.forms import AnswerForm

CSRF = re.compile(r'name="csrf_token" value="([^"]+)"')
SOURCE = re.compile(r"source=([0-9a-f]{64})")


def _token(text: str) -> str:
    match = CSRF.search(text)
    assert match
    return match.group(1)


def _populated_services(tmp_path: Path) -> WebServices:
    services = WebServices(
        WebConfig.for_roots(
            tmp_path / "engagements",
            tmp_path / "runtime",
            repository_root=Path(__file__).resolve().parents[3],
        )
    )
    services.create_engagement("phase7-web")
    revision = 0
    for question in services.framework.questions:
        revision = services.save_answer(
            "phase7-web",
            expected_revision=revision,
            answer=AnswerForm(
                question_id=str(question["id"]),
                rating=1,
                evidence_status="Self-reported",
                note="Synthetic quick assessment evidence.",
            ),
        )
    services.save_diagnostic_facts(
        "phase7-web",
        expected_revision=revision,
        facts={
            str(fact["id"]): 1 if fact["type"] == "integer" else False
            for fact in services.framework.diagnostic_facts
        },
    )
    return services


def test_deep_dive_complete_review_promote_and_revision_views(tmp_path: Path) -> None:
    services = _populated_services(tmp_path)
    app = create_app(config=services.config, services=services)
    origin = {"origin": "http://127.0.0.1"}
    with TestClient(app, base_url="http://127.0.0.1") as client:
        select_page = client.get("/engagements/phase7-web/deep-dives")
        assert select_page.status_code == 200
        assert "20 questions" in select_page.text
        assert "24 questions" in select_page.text
        selected = client.post(
            "/engagements/phase7-web/deep-dives",
            data={
                "csrf_token": _token(select_page.text),
                "revision": str(services.state("phase7-web")["revision"]),
                "capability_id": "QUA",
                "planning_note": "Review synthetic quality controls.",
            },
            headers=origin,
            follow_redirects=False,
        )
        assert selected.status_code == 303
        reopened = client.get(selected.headers["location"])
        assert "Open data-quality" in reopened.text

        workshop = client.get("/engagements/phase7-web/deep-dives/data-quality")
        assert workshop.status_code == 200
        assert workshop.text.count("Maturity rating") == 20
        payload = {
            "csrf_token": _token(workshop.text),
            "revision": str(services.state("phase7-web")["revision"]),
        }
        for question in services.deep_dive_service.registry.by_id(
            "data-quality"
        ).questions:
            payload[f"rating-{question.id}"] = "4"
            payload[f"evidence-status-{question.id}"] = "Evidenced"
            payload[f"note-{question.id}"] = (
                "Synthetic redacted evidence A & B remains local."
            )
        completed = client.post(
            "/engagements/phase7-web/deep-dives/data-quality",
            data=payload,
            headers=origin,
            follow_redirects=False,
        )
        assert completed.status_code == 303
        source_match = SOURCE.search(completed.headers["location"])
        assert source_match
        source_digest = source_match.group(1)
        advisory_page = client.get(completed.headers["location"])
        assert "Advisory result · no readiness effect" in advisory_page.text

        promoted = client.post(
            "/engagements/phase7-web/deep-dives/data-quality/promote",
            data={
                "csrf_token": _token(advisory_page.text),
                "source_digest": source_digest,
                "target_digest": (
                    services.deep_dive_service.promotion_target_digest(
                        "phase7-web"
                    )
                ),
                "promote-QUA": "yes",
                "choice-QUA": "use-deep-dive",
                "reviewed_by": "solution-architect",
                "rationale": "Reviewed complete synthetic quality evidence.",
            },
            headers=origin,
            follow_redirects=False,
        )
        assert promoted.status_code == 303
        promoted_page = client.get(promoted.headers["location"])
        assert "2 · reviewed-promotion" in promoted_page.text
        assert "1 · retained" in promoted_page.text

        review = client.get("/engagements/phase7-web/review")
        assert review.status_code == 200
        assert "Accountable roadmap action" in review.text
        assert "Vendor-neutral technology options" in review.text
        assert "optional and not used for scoring" in review.text

        report = services.generate_report("phase7-web")
        assert b'"active_revision": 2' in report.json_bytes
        assert b'"promotion_reviewed": true' in report.json_bytes
        assert b'"mapping_chain"' in report.json_bytes
        assert b"active 2; prior 1" in report.html_bytes
        assert b"A &amp; B remains local" in report.html_bytes

        prior_report = services.generate_report("phase7-web", revision_number=1)
        assert b'"selected_revision": 1' in prior_report.json_bytes
        assert b'"active_revision": 2' in prior_report.json_bytes
        assert b'"is_active": false' in prior_report.json_bytes
        assert b"selected 1 (prior); active 2" in prior_report.html_bytes

        report_page = client.get("/engagements/phase7-web/report")
        selected_prior = client.post(
            "/engagements/phase7-web/report",
            data={
                "csrf_token": _token(report_page.text),
                "revision": "1",
            },
            headers=origin,
            follow_redirects=False,
        )
        assert selected_prior.status_code == 303
        prior_page = client.get(selected_prior.headers["location"])
        assert "Selected revision 1 (prior)" in prior_page.text
        assert "Report is stale" not in prior_page.text
        downloaded = client.get("/engagements/phase7-web/report/report.json")
        assert downloaded.status_code == 200
        assert downloaded.json()["sections"][-1]["content"][
            "assessment_revision"
        ]["selected_revision"] == 1


def test_quick_document_cannot_be_mutated_after_reviewed_promotion(tmp_path: Path) -> None:
    services = _populated_services(tmp_path)
    definition = services.deep_dive_service.registry.by_id("data-quality")
    advisory = services.save_deep_dive_advisory(
        "phase7-web",
        deep_dive_id="data-quality",
        answers=[
            DeepDiveAnswer(
                question_id=question.id,
                rating=4,
                evidence_status="Evidenced",
                note="Synthetic reviewed evidence.",
                evidence_refs=[],
            )
            for question in definition.questions
        ],
    )
    services.promote_deep_dive(
        "phase7-web",
        source_digest=advisory.document_digest,
        target_digest=services.deep_dive_service.promotion_target_digest(
            "phase7-web"
        ),
        capability_ids=["QUA"],
        rationale="Reviewed complete synthetic quality evidence.",
        reviewed_by="solution-architect",
        choices={"QUA": "use-deep-dive"},
    )
    quick_before = services.quick_document("phase7-web")
    try:
        services.save_answer(
            "phase7-web",
            expected_revision=int(services.state("phase7-web")["revision"]),
            answer=AnswerForm(
                question_id="Q-QUA-01",
                rating=0,
                evidence_status="Self-reported",
                note="Attempted mutation.",
            ),
        )
    except ValueError as error:
        assert "immutable after reviewed promotion" in str(error)
    else:
        raise AssertionError("promoted quick assessment must be immutable")
    assert services.quick_document("phase7-web") == quick_before


def test_corrupt_demo_fails_closed_without_hiding_or_mutating_assessment(
    tmp_path: Path,
) -> None:
    corrupt_manifest = (
        tmp_path
        / "corrupt-repository"
        / "demo"
        / "manifests"
        / "stages"
        / "ingestion.yaml"
    )
    corrupt_manifest.parent.mkdir(parents=True)
    corrupt_manifest.write_text(
        "schema_version: 1.0.0\nstage_id: wrong\n",
        encoding="utf-8",
    )
    services = WebServices(
        WebConfig.for_roots(
            tmp_path / "corrupt-engagements",
            tmp_path / "corrupt-runtime",
            repository_root=tmp_path / "corrupt-repository",
        )
    )
    services.create_engagement("recoverable-assessment")
    before = services.store.snapshot("recoverable-assessment")
    with TestClient(
        create_app(config=services.config, services=services),
        base_url="http://127.0.0.1",
    ) as client:
        demo = client.get("/demo")
        quick = client.get("/engagements/recoverable-assessment/quick")
    assert demo.status_code == 422
    assert "corrupt stage manifest" in demo.text
    assert quick.status_code == 200
    assert "Quick assessment" in quick.text
    assert services.store.snapshot("recoverable-assessment") == before
