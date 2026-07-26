from __future__ import annotations

import copy
import hashlib
import json
from dataclasses import asdict
from pathlib import Path

import pytest

from assessment.cli import main
from assessment.domain.deep_dives import (
    ConflictChoice,
    DeepDiveAnswer,
    DeepDiveService,
    PromotionRequest,
)
from assessment.domain.errors import ArchiveValidationError
from assessment.engine.evaluator import evaluate_assessment
from assessment.storage.archive import export_engagement, import_engagement
from assessment.storage.local import LocalEngagementStore, canonical_json
from assessment.storage.migrations import _prototype_to_v1
from assessment.web.config import WebConfig
from assessment.web.dependencies import WebServices
from prototype import run as prototype


def _services(tmp_path: Path) -> WebServices:
    engagement_root = tmp_path / "engagements"
    runtime_root = tmp_path / "runtime"
    engagement_root.mkdir()
    runtime_root.mkdir()
    config = WebConfig(
        engagement_root=engagement_root,
        runtime_root=runtime_root,
        repository_root=Path(__file__).resolve().parents[3],
        host="127.0.0.1",
        port=8765,
    )
    return WebServices(config, store=LocalEngagementStore(engagement_root))


def _create_complete_engagement(web: WebServices) -> None:
    web.create_engagement("promotion-test")
    framework = prototype.load_framework()
    fixture = prototype.load_scenarios(framework)["startup-no-governance"][
        "architect-a"
    ]
    quick = _prototype_to_v1(fixture, "promotion-test")["assessment/quick.json"]
    web.store.write_document("promotion-test", "assessment/quick.json", quick)


def _digest(document: dict[str, object]) -> str:
    return hashlib.sha256(canonical_json(document)).hexdigest()


def _promote_quality(web: WebServices) -> tuple[DeepDiveService, str]:
    _create_complete_engagement(web)
    service = DeepDiveService(web.store, web.framework)
    definition = service.registry.by_id("data-quality")
    advisory = service.save_advisory(
        "promotion-test",
        deep_dive_id=definition.id,
        answers=[
            DeepDiveAnswer(
                question_id=question.id,
                rating=4,
                evidence_status="Evidenced",
                note="Synthetic evidence only.",
                evidence_refs=[],
            )
            for question in definition.questions
        ],
    )
    service.promote(
        "promotion-test",
        PromotionRequest(
            source_digest=advisory.document_digest,
            target_digest=service.promotion_target_digest("promotion-test"),
            capability_ids=["QUA"],
            rationale="Architect reviewed the complete synthetic evidence.",
            reviewed_by="solution-architect",
            review_timestamp=service.engagement_timestamp("promotion-test"),
            conflict_choices=[
                ConflictChoice(
                    capability_id="QUA",
                    choice="use-deep-dive",
                    rationale="Complete evidenced deep dive is selected.",
                )
            ],
        ),
    )
    return service, advisory.document_digest


@pytest.mark.parametrize(
    ("deep_dive_id", "capability_ids"),
    (
        ("data-quality", ("QUA",)),
        ("governance-metadata-lineage", ("GOV", "LIN")),
        ("security-privacy-policy", ("SEC", "GOV")),
    ),
)
def test_each_deep_dive_advisory_is_separate_and_cannot_change_quick_readiness(
    tmp_path: Path,
    deep_dive_id: str,
    capability_ids: tuple[str, ...],
) -> None:
    web = _services(tmp_path)
    _create_complete_engagement(web)
    quick_before = web.quick_document("promotion-test")
    quick_bytes = canonical_json(quick_before)
    result_before = web.evaluate("promotion-test")
    service = DeepDiveService(web.store, web.framework)
    questions = service.registry.by_id(deep_dive_id).questions
    advisory = service.save_advisory(
        "promotion-test",
        deep_dive_id=deep_dive_id,
        answers=[
            DeepDiveAnswer(
                question_id=question.id,
                rating=4,
                evidence_status="Evidenced",
                note="Synthetic reviewed evidence retained in the engagement.",
                evidence_refs=[],
            )
            for question in questions
        ],
    )

    assert advisory.scope == "deep-dive"
    assert advisory.advisory_only is True
    assert advisory.capability_scores == {
        capability_id: 4 for capability_id in capability_ids
    }
    assert canonical_json(web.quick_document("promotion-test")) == quick_bytes
    assert web.evaluate("promotion-test") == result_before


@pytest.mark.parametrize(
    ("deep_dive_id", "capability_ids"),
    (
        ("data-quality", ("QUA",)),
        ("governance-metadata-lineage", ("GOV", "LIN")),
        ("security-privacy-policy", ("SEC", "GOV")),
    ),
)
def test_each_reviewed_digest_bound_promotion_creates_revision_and_retains_prior(
    tmp_path: Path,
    deep_dive_id: str,
    capability_ids: tuple[str, ...],
) -> None:
    web = _services(tmp_path)
    _create_complete_engagement(web)
    service = DeepDiveService(web.store, web.framework)
    quick_before = web.quick_document("promotion-test")
    source = service.save_advisory(
        "promotion-test",
        deep_dive_id=deep_dive_id,
        answers=[
            DeepDiveAnswer(
                question_id=question.id,
                rating=4,
                evidence_status="Evidenced",
                note="Synthetic evidence only.",
                evidence_refs=[],
            )
            for question in service.registry.by_id(deep_dive_id).questions
        ],
    )
    request = PromotionRequest(
        source_digest=source.document_digest,
        target_digest=service.promotion_target_digest("promotion-test"),
        capability_ids=list(capability_ids),
        rationale="Architect reviewed the complete deep dive and its evidence.",
        reviewed_by="solution-architect",
        review_timestamp=service.engagement_timestamp("promotion-test"),
        conflict_choices=[
            ConflictChoice(
                capability_id=capability_id,
                choice="use-deep-dive",
                rationale="Complete evidenced deep dive supersedes self-report for this revision.",
            )
            for capability_id in capability_ids
        ],
    )
    promoted = service.promote("promotion-test", request)

    assert promoted.revision == 2
    assert promoted.active is True
    assert promoted.prior_revision == 1
    assert promoted.before_result_digest != promoted.after_result_digest
    assert len(promoted.gate_trace) == 7
    assert web.store.read_document(
        "promotion-test", "assessment/quick.json"
    ) == quick_before
    assert web.store.read_document(
        "promotion-test", "results/revisions/1.json"
    )["revision"] == 1
    assert web.store.read_document(
        "promotion-test", "results/revisions/2.json"
    )["revision"] == 2
    assert web.store.read_document(
        "promotion-test", "results/active.json"
    )["active_revision"] == 2
    assert web.store.read_document(
        "promotion-test", "promotions/revision-2.json"
    )["reviewed_by"] == "solution-architect"
    with pytest.raises(ValueError, match="stale target"):
        service.promote("promotion-test", request)


def test_promotion_rejects_stale_duplicates_unknowns_and_unresolved_conflicts(
    tmp_path: Path,
) -> None:
    web = _services(tmp_path)
    _create_complete_engagement(web)
    service = DeepDiveService(web.store, web.framework)
    source = service.save_advisory(
        "promotion-test",
        deep_dive_id="data-quality",
        answers=[
            DeepDiveAnswer(
                question_id=question.id,
                rating=3,
                evidence_status="Partially evidenced",
                note="Synthetic evidence only.",
                evidence_refs=[],
            )
            for question in service.registry.by_id("data-quality").questions
        ],
    )
    base = {
        "source_digest": source.document_digest,
        "target_digest": service.promotion_target_digest("promotion-test"),
        "capability_ids": ["QUA"],
        "rationale": "Architect review completed.",
        "reviewed_by": "enterprise-architect",
        "review_timestamp": service.engagement_timestamp("promotion-test"),
        "conflict_choices": [
            {
                "capability_id": "QUA",
                "choice": "use-deep-dive",
                "rationale": "Reviewed deep-dive evidence is selected.",
            }
        ],
    }
    for changed, match in (
        ({"source_digest": "0" * 64}, "stale source"),
        ({"target_digest": "0" * 64}, "stale target"),
        ({"capability_ids": ["QUA", "QUA"]}, "duplicate"),
        ({"capability_ids": ["UNKNOWN"]}, "capability"),
        ({"conflict_choices": []}, "conflict"),
    ):
        document = copy.deepcopy(base)
        document.update(changed)
        with pytest.raises(ValueError, match=match):
            service.promote("promotion-test", PromotionRequest.model_validate(document))


def test_reviewed_promotion_ignores_not_assessed_when_deriving_evidence_status(
    tmp_path: Path,
) -> None:
    web = _services(tmp_path)
    _create_complete_engagement(web)
    service = DeepDiveService(web.store, web.framework)
    definition = service.registry.by_id("data-quality")
    source = service.save_advisory(
        "promotion-test",
        deep_dive_id=definition.id,
        answers=[
            DeepDiveAnswer(
                question_id=question.id,
                rating=None if index == 0 else 4,
                evidence_status="Not assessed" if index == 0 else "Evidenced",
                note="Coverage is explicit and assessed answers use synthetic evidence.",
                evidence_refs=[],
            )
            for index, question in enumerate(definition.questions)
        ],
    )

    promoted = service.promote(
        "promotion-test",
        PromotionRequest(
            source_digest=source.document_digest,
            target_digest=service.promotion_target_digest("promotion-test"),
            capability_ids=["QUA"],
            rationale="Architect reviewed partial coverage and assessed evidence.",
            reviewed_by="solution-architect",
            review_timestamp=service.engagement_timestamp("promotion-test"),
            conflict_choices=[
                ConflictChoice(
                    capability_id="QUA",
                    choice="use-deep-dive",
                    rationale="Use the assessed deep-dive answers for this revision.",
                )
            ],
        ),
    )

    answers = web.store.read_document(
        "promotion-test", promoted.answer_document_key
    )["answers"]
    quality = [
        answer
        for answer in answers
        if answer["question_id"].startswith("Q-QUA-")
    ]
    assert {answer["rating"] for answer in quality} == {4}
    assert {answer["evidence_status"] for answer in quality} == {"Evidenced"}


def test_use_quick_conflict_choice_replays_without_changing_answers(
    tmp_path: Path,
) -> None:
    web = _services(tmp_path)
    _create_complete_engagement(web)
    service = DeepDiveService(web.store, web.framework)
    quick_before = web.quick_document("promotion-test")
    definition = service.registry.by_id("data-quality")
    source = service.save_advisory(
        "promotion-test",
        deep_dive_id=definition.id,
        answers=[
            DeepDiveAnswer(
                question_id=question.id,
                rating=4,
                evidence_status="Evidenced",
                note="Synthetic evidence only.",
                evidence_refs=[],
            )
            for question in definition.questions
        ],
    )
    promoted = service.promote(
        "promotion-test",
        PromotionRequest(
            source_digest=source.document_digest,
            target_digest=service.promotion_target_digest("promotion-test"),
            capability_ids=["QUA"],
            rationale="Architect retained the quick result after review.",
            reviewed_by="solution-architect",
            review_timestamp=service.engagement_timestamp("promotion-test"),
            conflict_choices=[
                ConflictChoice(
                    capability_id="QUA",
                    choice="use-quick",
                    rationale="Quick evidence remains authoritative.",
                )
            ],
        ),
    )

    assert web.store.read_document(
        "promotion-test", promoted.answer_document_key
    ) == quick_before
    export_engagement(
        web.store.open("promotion-test"),
        tmp_path / "use-quick.zip",
    )


@pytest.mark.parametrize(
    "corruption",
    (
        "unresolved-active-pointer",
        "revision-number-mismatch",
        "missing-answer-revision",
        "result-digest-mismatch",
        "advisory-digest-mismatch",
        "promotion-source-mismatch",
        "replayed-answer-mismatch",
        "duplicate-conflict-choice",
    ),
)
def test_export_rejects_internally_broken_phase7_revision_graph(
    tmp_path: Path,
    corruption: str,
) -> None:
    web = _services(tmp_path)
    _, advisory_digest = _promote_quality(web)
    if corruption == "unresolved-active-pointer":
        web.store.write_document(
            "promotion-test",
            "results/active.json",
            {"schema_version": "1.0.0", "active_revision": 999},
        )
    elif corruption == "revision-number-mismatch":
        revision = web.store.read_document(
            "promotion-test", "results/revisions/2.json"
        )
        revision["revision"] = 99
        web.store.write_document(
            "promotion-test", "results/revisions/2.json", revision
        )
    elif corruption == "missing-answer-revision":
        (
            web.store.open("promotion-test")
            / "assessment/revisions/2.json"
        ).unlink()
    elif corruption == "result-digest-mismatch":
        revision = web.store.read_document(
            "promotion-test", "results/revisions/2.json"
        )
        revision["result_digest"] = "0" * 64
        web.store.write_document(
            "promotion-test", "results/revisions/2.json", revision
        )
    elif corruption == "advisory-digest-mismatch":
        advisory_key = (
            f"assessment/deep-dives/data-quality/{advisory_digest}.json"
        )
        advisory = web.store.read_document("promotion-test", advisory_key)
        advisory["answers"][0]["note"] = "Changed after the digest was recorded."
        web.store.write_document("promotion-test", advisory_key, advisory)
    elif corruption == "promotion-source-mismatch":
        promotion = web.store.read_document(
            "promotion-test", "promotions/revision-2.json"
        )
        promotion["source_digest"] = "f" * 64
        web.store.write_document(
            "promotion-test", "promotions/revision-2.json", promotion
        )
    elif corruption == "replayed-answer-mismatch":
        answers = web.store.read_document(
            "promotion-test", "assessment/revisions/2.json"
        )
        for answer in answers["answers"]:
            if answer["question_id"].startswith("Q-QUA-"):
                answer["rating"] = 0
        web.store.write_document(
            "promotion-test", "assessment/revisions/2.json", answers
        )
        result = evaluate_assessment(
            answers,
            web.framework,
            expected_engagement_id="promotion-test",
        )
        result_digest = _digest(asdict(result))
        revision = web.store.read_document(
            "promotion-test", "results/revisions/2.json"
        )
        revision["result_digest"] = result_digest
        revision["after_result_digest"] = result_digest
        revision["gate_trace"] = [asdict(trace) for trace in result.gates.traces]
        web.store.write_document(
            "promotion-test", "results/revisions/2.json", revision
        )
        promotion = web.store.read_document(
            "promotion-test", "promotions/revision-2.json"
        )
        promotion["after_result_digest"] = result_digest
        web.store.write_document(
            "promotion-test", "promotions/revision-2.json", promotion
        )
    elif corruption == "duplicate-conflict-choice":
        promotion = web.store.read_document(
            "promotion-test", "promotions/revision-2.json"
        )
        promotion["conflict_choices"].insert(
            0,
            {
                "capability_id": "QUA",
                "choice": "use-quick",
                "rationale": "Contradictory duplicate must be rejected.",
            },
        )
        web.store.write_document(
            "promotion-test", "promotions/revision-2.json", promotion
        )
    else:  # pragma: no cover - exhaustive parametrization guard
        raise AssertionError(corruption)

    with pytest.raises(ArchiveValidationError, match="revision graph"):
        export_engagement(
            web.store.open("promotion-test"),
            tmp_path / f"{corruption}.zip",
        )


def test_quick_synchronization_revision_graph_remains_portable(
    tmp_path: Path,
) -> None:
    web = _services(tmp_path)
    _create_complete_engagement(web)
    service = DeepDiveService(web.store, web.framework)
    service.ensure_quick_revision("promotion-test")
    quick = web.quick_document("promotion-test")
    quick["answers"][0]["note"] = "Updated before the reviewed promotion."
    web.store.write_document("promotion-test", "assessment/quick.json", quick)
    definition = service.registry.by_id("data-quality")
    advisory = service.save_advisory(
        "promotion-test",
        deep_dive_id=definition.id,
        answers=[
            DeepDiveAnswer(
                question_id=question.id,
                rating=4,
                evidence_status="Evidenced",
                note="Synthetic evidence only.",
                evidence_refs=[],
            )
            for question in definition.questions
        ],
    )
    promoted = service.promote(
        "promotion-test",
        PromotionRequest(
            source_digest=advisory.document_digest,
            target_digest=service.promotion_target_digest("promotion-test"),
            capability_ids=["QUA"],
            rationale="Architect reviewed the synchronized quick revision.",
            reviewed_by="solution-architect",
            review_timestamp=service.engagement_timestamp("promotion-test"),
            conflict_choices=[
                ConflictChoice(
                    capability_id="QUA",
                    choice="use-deep-dive",
                    rationale="Use the complete reviewed deep dive.",
                )
            ],
        ),
    )
    assert promoted.revision == 3

    archive = tmp_path / "synchronized.zip"
    export_engagement(web.store.open("promotion-test"), archive)
    import_root = tmp_path / "imported"
    import_root.mkdir()
    destination = import_root / "promotion-test"
    import_engagement(archive, destination)
    imported = LocalEngagementStore(import_root)
    assert imported.read_document(
        "promotion-test", "results/active.json"
    )["active_revision"] == 3


def test_revision_selection_is_explicit_and_never_latest_wins(tmp_path: Path) -> None:
    web = _services(tmp_path)
    _create_complete_engagement(web)
    service = DeepDiveService(web.store, web.framework)
    service.ensure_quick_revision("promotion-test")
    forged = web.store.read_document("promotion-test", "results/revisions/1.json")
    forged["revision"] = 99
    forged["active"] = False
    web.store.write_document("promotion-test", "results/revisions/99.json", forged)

    assert service.active_revision("promotion-test").revision == 1
    with pytest.raises(ValueError, match="explicit"):
        service.revision("promotion-test", None)
    assert service.revision("promotion-test", 99).revision == 99


def test_cli_evaluate_and_report_can_select_retained_revision(tmp_path: Path) -> None:
    web = _services(tmp_path)
    _create_complete_engagement(web)
    service = DeepDiveService(web.store, web.framework)
    definition = service.registry.by_id("data-quality")
    advisory = service.save_advisory(
        "promotion-test",
        deep_dive_id=definition.id,
        answers=[
            DeepDiveAnswer(
                question_id=question.id,
                rating=4,
                evidence_status="Evidenced",
                note="Synthetic evidence only.",
                evidence_refs=[],
            )
            for question in definition.questions
        ],
    )
    service.promote(
        "promotion-test",
        PromotionRequest(
            source_digest=advisory.document_digest,
            target_digest=service.promotion_target_digest("promotion-test"),
            capability_ids=["QUA"],
            rationale="Architect reviewed retained-revision reporting.",
            reviewed_by="solution-architect",
            review_timestamp=service.engagement_timestamp("promotion-test"),
            conflict_choices=[
                ConflictChoice(
                    capability_id="QUA",
                    choice="use-deep-dive",
                    rationale="Reviewed deep-dive evidence is selected.",
                )
            ],
        ),
    )
    engagement_root = web.store.root / "promotion-test"
    evaluate_output = tmp_path / "evaluate-prior"
    report_output = tmp_path / "report-prior"
    for command, output in (
        ("evaluate", evaluate_output),
        ("report", report_output),
    ):
        assert (
            main(
                [
                    command,
                    "--engagement-root",
                    str(engagement_root),
                    "--output-root",
                    str(output),
                    "--revision",
                    "1",
                ]
            )
            == 0
        )
    evaluation = json.loads(
        (evaluate_output / "assessment-result.json").read_bytes()
    )
    report = json.loads((report_output / "report.json").read_bytes())
    assert evaluation["assessment_revision"]["selected_revision"] == 1
    assert evaluation["assessment_revision"]["active_revision"] == 2
    appendix = report["sections"][-1]["content"]["assessment_revision"]
    assert appendix["selected_revision"] == 1
    assert appendix["active_revision"] == 2
    assert appendix["is_active"] is False
