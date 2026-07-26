"""Validated deep-dive content and explicit reviewed promotion service."""

from __future__ import annotations

import hashlib
from dataclasses import asdict
from importlib import resources
from statistics import median_low
from typing import Any, Literal

import yaml
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    ValidationError,
    field_validator,
    model_validator,
)
from yaml.tokens import AliasToken, AnchorToken

from assessment.content.markdown import validate_markdown
from assessment.domain.errors import ContentValidationError
from assessment.domain.models import (
    AnswerEvidenceDocument,
    EvidenceStatus,
    validate_identifier,
    validate_relative_posix_path,
)
from assessment.engine.evaluator import evaluate_assessment
from assessment.frameworks import FrameworkBundle
from assessment.storage.local import LocalEngagementStore, canonical_json

DEEP_DIVE_ORDER = (
    "data-quality",
    "governance-metadata-lineage",
    "security-privacy-policy",
)
CONFIDENCE_SEMANTICS = (
    "Use the existing evidence status independently from the maturity rating."
)
STATUS_ORDER = {
    "Evidenced": 0,
    "Partially evidenced": 1,
    "Self-reported": 2,
    "Conflicting evidence": 3,
    "Not assessed": 4,
}


class DeepDiveModel(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)


class DeepDiveQuestion(DeepDiveModel):
    id: str
    text: str = Field(min_length=12)
    anchors: dict[str, str]
    evidence_guidance: str = Field(min_length=12)
    duration_minutes: int = Field(ge=2, le=15)
    linked_recommendation_ids: list[str] = Field(min_length=1)
    confidence_semantics: Literal[
        "Use the existing evidence status independently from the maturity rating."
    ]

    _validate_id = field_validator("id")(validate_identifier)

    @field_validator("anchors")
    @classmethod
    def complete_anchors(cls, value: dict[str, str]) -> dict[str, str]:
        if set(value) != {str(level) for level in range(5)}:
            raise ValueError("deep-dive anchors must contain exactly levels 0-4")
        if any(len(anchor) < 12 for anchor in value.values()):
            raise ValueError("deep-dive anchors must be observable statements")
        return value


class DeepDiveDefinition(DeepDiveModel):
    schema_version: Literal["1.0.0"]
    id: str
    title: str = Field(min_length=1)
    capability_ids: list[str] = Field(min_length=1)
    duration_minutes: int = Field(ge=30, le=180)
    evidence_guidance: str = Field(min_length=12)
    linked_recommendation_ids: list[str] = Field(min_length=1)
    questions: list[DeepDiveQuestion] = Field(min_length=15, max_length=30)

    _validate_id = field_validator("id")(validate_identifier)


class DeepDiveRegistry(DeepDiveModel):
    deep_dives: list[DeepDiveDefinition]

    def by_id(self, deep_dive_id: str) -> DeepDiveDefinition:
        for item in self.deep_dives:
            if item.id == deep_dive_id:
                return item
        raise ValueError("deep-dive ID is not installed")


class DeepDiveAnswer(DeepDiveModel):
    question_id: str
    rating: int | None = Field(ge=0, le=4)
    evidence_status: EvidenceStatus
    note: str = Field(max_length=4096)
    evidence_refs: list[str] = Field(max_length=32)

    _validate_question_id = field_validator("question_id")(validate_identifier)

    @field_validator("evidence_refs")
    @classmethod
    def validate_evidence_refs(cls, value: list[str]) -> list[str]:
        if len(value) != len(set(value)):
            raise ValueError("deep-dive evidence references must be unique")
        return [validate_relative_posix_path(item) for item in value]

    @model_validator(mode="after")
    def rating_matches_status(self) -> DeepDiveAnswer:
        if (self.evidence_status == "Not assessed") != (self.rating is None):
            raise ValueError(
                "Not assessed requires a null rating and assessed answers require a rating"
            )
        validate_markdown(self.note, context=f"deep-dive answer {self.question_id}")
        return self


class DeepDiveAdvisory(DeepDiveModel):
    schema_version: Literal["1.0.0"]
    engagement_id: str
    framework_version: Literal["1.0.0"]
    scope: Literal["deep-dive"]
    deep_dive_id: str
    capability_ids: list[str]
    answers: list[DeepDiveAnswer]
    capability_scores: dict[str, int | None]
    advisory_only: Literal[True]
    document_digest: str = Field(pattern=r"^[0-9a-f]{64}$")


class ConflictChoice(DeepDiveModel):
    capability_id: str
    choice: Literal["use-quick", "use-deep-dive"]
    rationale: str = Field(min_length=12, max_length=4096)

    _validate_id = field_validator("capability_id")(validate_identifier)


class PromotionRequest(DeepDiveModel):
    source_digest: str = Field(pattern=r"^[0-9a-f]{64}$")
    target_digest: str = Field(pattern=r"^[0-9a-f]{64}$")
    capability_ids: list[str] = Field(min_length=1)
    rationale: str = Field(min_length=12, max_length=4096)
    reviewed_by: str = Field(min_length=1, max_length=128)
    review_timestamp: str = Field(
        pattern=r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$"
    )
    conflict_choices: list[ConflictChoice]


class AssessmentRevision(DeepDiveModel):
    schema_version: Literal["1.0.0"]
    engagement_id: str
    revision: int = Field(ge=1)
    prior_revision: int | None
    source_kind: Literal["quick", "reviewed-promotion"]
    source_digest: str = Field(pattern=r"^[0-9a-f]{64}$")
    result_digest: str = Field(pattern=r"^[0-9a-f]{64}$")
    before_result_digest: str = Field(pattern=r"^[0-9a-f]{64}$")
    after_result_digest: str = Field(pattern=r"^[0-9a-f]{64}$")
    answer_document_key: str
    gate_trace: list[dict[str, Any]] = Field(min_length=7, max_length=7)
    active: bool = False


def _load_authored_yaml(name: str) -> dict[str, Any]:
    raw = (
        resources.files("assessment")
        .joinpath("content", "frameworks", "1.0.0", "deep-dives", name)
        .read_text(encoding="utf-8")
    )
    try:
        if any(isinstance(token, AliasToken | AnchorToken) for token in yaml.scan(raw)):
            raise ContentValidationError(
                f"deep dive {name}: YAML anchors and aliases are not allowed"
            )
        document = yaml.safe_load(raw)
    except yaml.YAMLError as error:
        raise ContentValidationError(f"deep dive {name}: malformed YAML") from error
    if not isinstance(document, dict):
        raise ContentValidationError(f"deep dive {name}: mapping required")
    return document


def load_deep_dive_registry() -> DeepDiveRegistry:
    definitions: list[DeepDiveDefinition] = []
    expected_counts = (20, 24, 20)
    for deep_dive_id, expected_count in zip(
        DEEP_DIVE_ORDER, expected_counts, strict=True
    ):
        document = _load_authored_yaml(f"{deep_dive_id}.yaml")
        document["questions"] = [
            {**question, "confidence_semantics": CONFIDENCE_SEMANTICS}
            for question in document.get("questions", [])
            if isinstance(question, dict)
        ]
        try:
            definition = DeepDiveDefinition.model_validate(document)
        except ValidationError as error:
            raise ContentValidationError(f"deep dive {deep_dive_id}: {error}") from error
        if definition.id != deep_dive_id or len(definition.questions) != expected_count:
            raise ContentValidationError(
                f"deep dive {deep_dive_id}: exact planned identity/count required"
            )
        definitions.append(definition)
    question_ids = [
        question.id for definition in definitions for question in definition.questions
    ]
    if len(question_ids) != len(set(question_ids)):
        raise ContentValidationError("deep dives: question IDs must be globally unique")
    return DeepDiveRegistry(deep_dives=definitions)


def _sha(document: Any) -> str:
    return hashlib.sha256(canonical_json(document)).hexdigest()


def _result_document(result: Any) -> dict[str, Any]:
    return asdict(result)


def build_promoted_answer_document(
    framework: FrameworkBundle,
    active_answers: dict[str, Any],
    advisory: DeepDiveAdvisory,
    request: PromotionRequest,
) -> dict[str, Any]:
    """Replay one reviewed promotion without store or engine side effects."""
    promoted_answers = {
        str(item["question_id"]): dict(item)
        for item in active_answers.get("answers", [])
    }
    assessed_statuses = [
        answer.evidence_status
        for answer in advisory.answers
        if answer.rating is not None
    ]
    source_status = (
        max(assessed_statuses, key=STATUS_ORDER.__getitem__)
        if assessed_statuses
        else "Not assessed"
    )
    source_refs = sorted(
        {
            reference
            for answer in advisory.answers
            for reference in answer.evidence_refs
        }
    )
    choices_by_id = {
        choice.capability_id: choice for choice in request.conflict_choices
    }
    for capability_id in request.capability_ids:
        choice = choices_by_id.get(capability_id)
        if choice is None:
            raise ValueError("every promoted capability requires a conflict choice")
        if choice.choice == "use-quick":
            continue
        score = advisory.capability_scores[capability_id]
        for question in framework.questions:
            if question["domain_id"] == capability_id:
                promoted_answers[str(question["id"])] = {
                    "question_id": str(question["id"]),
                    "rating": score,
                    "evidence_status": (
                        "Not assessed" if score is None else source_status
                    ),
                    "note": (
                        "Reviewed deep-dive promotion "
                        f"{advisory.document_digest}; {request.rationale}"
                    ),
                    "evidence_refs": source_refs,
                }
    promoted_document = {
        **active_answers,
        "answers": [
            promoted_answers[str(question["id"])]
            for question in framework.questions
            if str(question["id"]) in promoted_answers
        ],
    }
    return AnswerEvidenceDocument.model_validate(promoted_document).model_dump(
        mode="json"
    )


class DeepDiveService:
    """Persist advisory documents and produce explicit immutable result revisions."""

    def __init__(
        self,
        store: LocalEngagementStore,
        framework: FrameworkBundle,
    ) -> None:
        self.store = store
        self.framework = framework
        self.registry = load_deep_dive_registry()

    def engagement_timestamp(self, engagement_id: str) -> str:
        metadata = self.store.read_document(engagement_id, "engagement/metadata.json")
        value = metadata.get("assessment_timestamp")
        if not isinstance(value, str):
            raise ValueError("engagement metadata timestamp is required")
        return value

    def save_advisory(
        self,
        engagement_id: str,
        *,
        deep_dive_id: str,
        answers: list[DeepDiveAnswer],
    ) -> DeepDiveAdvisory:
        definition = self.registry.by_id(deep_dive_id)
        expected = [question.id for question in definition.questions]
        actual = [answer.question_id for answer in answers]
        if actual != expected:
            raise ValueError("deep-dive answers must be complete and in question order")
        scores = [
            answer.rating for answer in answers if answer.rating is not None
        ]
        score = int(median_low(scores)) if scores else None
        payload: dict[str, Any] = {
            "schema_version": "1.0.0",
            "engagement_id": engagement_id,
            "framework_version": self.framework.version,
            "scope": "deep-dive",
            "deep_dive_id": deep_dive_id,
            "capability_ids": definition.capability_ids,
            "answers": [answer.model_dump(mode="json") for answer in answers],
            "capability_scores": {
                capability_id: score for capability_id in definition.capability_ids
            },
            "advisory_only": True,
        }
        payload["document_digest"] = _sha(payload)
        advisory = DeepDiveAdvisory.model_validate(payload)
        self.store.write_document(
            engagement_id,
            f"assessment/deep-dives/{deep_dive_id}/{advisory.document_digest}.json",
            advisory.model_dump(mode="json"),
        )
        return advisory

    def _advisory_by_digest(
        self, engagement_id: str, source_digest: str
    ) -> DeepDiveAdvisory:
        for definition in self.registry.deep_dives:
            try:
                document = self.store.read_document(
                    engagement_id,
                    f"assessment/deep-dives/{definition.id}/{source_digest}.json",
                )
            except FileNotFoundError:
                continue
            advisory = DeepDiveAdvisory.model_validate(document)
            unsigned = advisory.model_dump(mode="json", exclude={"document_digest"})
            if advisory.document_digest != source_digest or _sha(unsigned) != source_digest:
                raise ValueError("stale source digest")
            return advisory
        raise ValueError("stale source digest")

    def advisory(
        self, engagement_id: str, source_digest: str
    ) -> DeepDiveAdvisory:
        return self._advisory_by_digest(engagement_id, source_digest)

    def _quick(self, engagement_id: str) -> dict[str, Any]:
        return self.store.read_document(engagement_id, "assessment/quick.json")

    def _make_revision(
        self,
        engagement_id: str,
        *,
        revision: int,
        prior_revision: int | None,
        source_kind: Literal["quick", "reviewed-promotion"],
        source_digest: str,
        answers: dict[str, Any],
        before_result_digest: str | None = None,
    ) -> AssessmentRevision:
        result = evaluate_assessment(
            answers,
            self.framework,
            expected_engagement_id=engagement_id,
        )
        result_document = _result_document(result)
        result_digest = _sha(result_document)
        answer_key = f"assessment/revisions/{revision}.json"
        self.store.write_document(engagement_id, answer_key, answers)
        revision_document = AssessmentRevision(
            schema_version="1.0.0",
            engagement_id=engagement_id,
            revision=revision,
            prior_revision=prior_revision,
            source_kind=source_kind,
            source_digest=source_digest,
            result_digest=result_digest,
            before_result_digest=before_result_digest or result_digest,
            after_result_digest=result_digest,
            answer_document_key=answer_key,
            gate_trace=[asdict(trace) for trace in result.gates.traces],
            active=False,
        )
        self.store.write_document(
            engagement_id,
            f"results/revisions/{revision}.json",
            revision_document.model_dump(mode="json"),
        )
        return revision_document

    def ensure_quick_revision(self, engagement_id: str) -> AssessmentRevision:
        try:
            return self.revision(engagement_id, 1)
        except FileNotFoundError:
            quick = self._quick(engagement_id)
            revision = self._make_revision(
                engagement_id,
                revision=1,
                prior_revision=None,
                source_kind="quick",
                source_digest=_sha(quick),
                answers=quick,
            )
            self.store.write_document(
                engagement_id,
                "results/active.json",
                {"schema_version": "1.0.0", "active_revision": 1},
            )
            return revision.model_copy(update={"active": True})

    def active_revision(self, engagement_id: str) -> AssessmentRevision:
        try:
            pointer = self.store.read_document(engagement_id, "results/active.json")
        except FileNotFoundError:
            return self.ensure_quick_revision(engagement_id)
        revision_number = pointer.get("active_revision")
        if not isinstance(revision_number, int):
            raise ValueError("active result revision pointer is invalid")
        return self.revision(engagement_id, revision_number).model_copy(
            update={"active": True}
        )

    def revision(
        self, engagement_id: str, revision: int | None
    ) -> AssessmentRevision:
        if revision is None:
            raise ValueError("revision selection must be explicit")
        document = self.store.read_document(
            engagement_id, f"results/revisions/{revision}.json"
        )
        return AssessmentRevision.model_validate(document)

    def active_answer_document(self, engagement_id: str) -> dict[str, Any]:
        revision = self.active_revision(engagement_id)
        quick = self._quick(engagement_id)
        if revision.source_kind == "quick" and _sha(quick) != revision.source_digest:
            return quick
        return self.store.read_document(engagement_id, revision.answer_document_key)

    def promotion_target_digest(self, engagement_id: str) -> str:
        """Bind a review to the explicit active result and its current answers."""
        active = self.active_revision(engagement_id)
        return _sha(
            {
                "active_revision": active.revision,
                "active_result_digest": active.result_digest,
                "answer_digest": _sha(self.active_answer_document(engagement_id)),
            }
        )

    def promote(
        self,
        engagement_id: str,
        request: PromotionRequest,
    ) -> AssessmentRevision:
        if len(request.capability_ids) != len(set(request.capability_ids)):
            raise ValueError("duplicate capability IDs are not allowed")
        allowed = {str(domain["id"]) for domain in self.framework.domains}
        if not set(request.capability_ids) <= allowed:
            raise ValueError("promotion contains an unknown capability")
        choices = [choice.capability_id for choice in request.conflict_choices]
        if len(choices) != len(set(choices)):
            raise ValueError("duplicate conflict choices are not allowed")
        if set(choices) != set(request.capability_ids):
            raise ValueError("every promoted capability requires a conflict choice")
        if request.review_timestamp != self.engagement_timestamp(engagement_id):
            raise ValueError("review timestamp must come from engagement metadata")
        advisory = self._advisory_by_digest(engagement_id, request.source_digest)
        if not set(request.capability_ids) <= set(advisory.capability_ids):
            raise ValueError("promotion capability is outside the source deep dive")
        active = self.active_revision(engagement_id)
        if self.promotion_target_digest(engagement_id) != request.target_digest:
            raise ValueError("stale target digest")
        quick = self._quick(engagement_id)
        quick_digest = _sha(quick)
        if active.source_kind == "quick" and active.source_digest != quick_digest:
            active = self._make_revision(
                engagement_id,
                revision=active.revision + 1,
                prior_revision=active.revision,
                source_kind="quick",
                source_digest=quick_digest,
                answers=quick,
                before_result_digest=active.result_digest,
            )
            self.store.write_document(
                engagement_id,
                "results/active.json",
                {
                    "schema_version": "1.0.0",
                    "active_revision": active.revision,
                },
            )
            active = active.model_copy(update={"active": True})
        active_answers = self.active_answer_document(engagement_id)
        promoted_document = build_promoted_answer_document(
            self.framework,
            active_answers,
            advisory,
            request,
        )
        revision_number = active.revision + 1
        promoted = self._make_revision(
            engagement_id,
            revision=revision_number,
            prior_revision=active.revision,
            source_kind="reviewed-promotion",
            source_digest=advisory.document_digest,
            answers=promoted_document,
            before_result_digest=active.result_digest,
        )
        promotion_record = {
            "schema_version": "1.0.0",
            "revision": revision_number,
            **request.model_dump(mode="json"),
            "before_result_digest": active.result_digest,
            "after_result_digest": promoted.result_digest,
        }
        self.store.write_document(
            engagement_id,
            f"promotions/revision-{revision_number}.json",
            promotion_record,
        )
        self.store.write_document(
            engagement_id,
            "results/active.json",
            {
                "schema_version": "1.0.0",
                "active_revision": revision_number,
            },
        )
        return promoted.model_copy(update={"active": True})
