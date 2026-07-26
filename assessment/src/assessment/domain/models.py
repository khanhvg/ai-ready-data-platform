"""Pydantic consumers of the authoritative v1 JSON Schemas."""

from __future__ import annotations

import re
from typing import Annotated, Any, Literal

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    StringConstraints,
    field_validator,
    model_validator,
)

from assessment.domain.errors import InvalidPathError

Identifier = Annotated[
    str,
    StringConstraints(pattern=r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$"),
]
SchemaVersion = Literal["1.0.0"]
FrameworkVersion = Literal["1.0.0"]
EvidenceStatus = Literal[
    "Self-reported",
    "Partially evidenced",
    "Evidenced",
    "Conflicting evidence",
    "Not assessed",
]

ID_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")
PATH_PART_PATTERN = ID_PATTERN
MANIFEST_PATH_PART_PATTERN = re.compile(r"^[A-Za-z0-9_][A-Za-z0-9._-]{0,127}$")
WINDOWS_DRIVE = re.compile(r"^[A-Za-z]:")


def validate_identifier(value: str) -> str:
    if not ID_PATTERN.fullmatch(value):
        raise ValueError(f"invalid stable ID: {value!r}")
    return value


def validate_relative_posix_path(value: str) -> str:
    if (
        not value
        or value.startswith("/")
        or WINDOWS_DRIVE.match(value)
        or "\\" in value
        or "\x00" in value
    ):
        raise InvalidPathError(f"unsafe relative POSIX path: {value!r}")
    parts = value.split("/")
    if any(
        part in {"", ".", ".."} or not PATH_PART_PATTERN.fullmatch(part)
        for part in parts
    ):
        raise InvalidPathError(f"unsafe relative POSIX path: {value!r}")
    return value


def validate_manifest_relative_posix_path(value: str) -> str:
    if (
        not value
        or value.startswith("/")
        or WINDOWS_DRIVE.match(value)
        or "\\" in value
        or "\x00" in value
    ):
        raise InvalidPathError(f"unsafe manifest-relative POSIX path: {value!r}")
    parts = value.split("/")
    if any(
        part in {"", ".", ".."} or not MANIFEST_PATH_PART_PATTERN.fullmatch(part)
        for part in parts
    ):
        raise InvalidPathError(f"unsafe manifest-relative POSIX path: {value!r}")
    return value


class ContractModel(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)


class Engagement(ContractModel):
    schema_version: SchemaVersion
    engagement_id: Identifier
    framework_version: FrameworkVersion
    catalog_version: Literal["1.0.0"]
    demo_content_version: Literal["1.0.0"]
    assessment_profile_id: Literal["quick-v1"]
    gate_bundle_version: Literal[1]

    _validate_id = field_validator("engagement_id")(validate_identifier)


class Answer(ContractModel):
    question_id: Identifier
    rating: int | None = Field(ge=0, le=4)
    evidence_status: EvidenceStatus
    note: str = Field(max_length=4096)
    evidence_refs: list[str] = Field(max_length=32)

    _validate_question_id = field_validator("question_id")(validate_identifier)

    @field_validator("evidence_refs")
    @classmethod
    def validate_evidence_refs(cls, value: list[str]) -> list[str]:
        if len(value) != len(set(value)):
            raise ValueError("evidence references must be unique")
        return [validate_relative_posix_path(item) for item in value]

    @model_validator(mode="after")
    def rating_matches_assessment_status(self) -> Answer:
        if (self.evidence_status == "Not assessed") != (self.rating is None):
            raise ValueError(
                "Not assessed requires a null rating and assessed answers require a rating"
            )
        return self


class AnswerEvidenceDocument(ContractModel):
    schema_version: SchemaVersion
    engagement_id: Identifier
    framework_version: FrameworkVersion
    answers: list[Answer] = Field(max_length=30)
    diagnostic_facts: dict[str, int | bool | str | None] = Field(max_length=32)

    _validate_engagement_id = field_validator("engagement_id")(validate_identifier)


class ReportSection(ContractModel):
    id: Identifier
    content: dict[str, Any]

    _validate_id = field_validator("id")(validate_identifier)


REPORT_SECTION_IDS = (
    "executive-summary",
    "readiness",
    "capability-heatmap",
    "gates",
    "confidence",
    "blockers",
    "findings",
    "target-state",
    "reference-diagrams",
    "roadmap",
    "technology-options",
    "evidence-appendix",
)


class Report(ContractModel):
    schema_version: SchemaVersion
    engagement_id: Identifier
    framework_version: FrameworkVersion
    sections: list[ReportSection] = Field(min_length=12, max_length=12)

    _validate_engagement_id = field_validator("engagement_id")(validate_identifier)

    @model_validator(mode="after")
    def sections_are_canonical(self) -> Report:
        if tuple(section.id for section in self.sections) != REPORT_SECTION_IDS:
            raise ValueError("report sections must use the canonical v1 order")
        return self


class Recipe(ContractModel):
    schema_version: SchemaVersion
    recipe_id: Identifier
    framework_version: FrameworkVersion
    title: str = Field(min_length=1, max_length=256)
    capability_ids: list[Identifier]
    question_ids: list[Identifier]

    _validate_recipe_id = field_validator("recipe_id")(validate_identifier)

    @field_validator("capability_ids", "question_ids")
    @classmethod
    def validate_reference_ids(cls, value: list[str]) -> list[str]:
        if len(value) != len(set(value)):
            raise ValueError("recipe references must be unique")
        return [validate_identifier(item) for item in value]


def validate_anchor_map(value: dict[str, str]) -> dict[str, str]:
    if set(value) != {str(level) for level in range(5)}:
        raise ValueError("anchors/labels must contain exactly levels 0-4")
    if any(len(anchor) < 12 for anchor in value.values()):
        raise ValueError("anchors must contain at least 12 characters")
    return value


def validate_label_map(value: dict[str, str]) -> dict[str, str]:
    if set(value) != {str(level) for level in range(5)}:
        raise ValueError("labels must contain exactly levels 0-4")
    if any(not label for label in value.values()):
        raise ValueError("labels must not be empty")
    return value


def validate_unique_identifiers(value: list[str]) -> list[str]:
    if len(value) != len(set(value)):
        raise ValueError("identifier references must be unique")
    return value


class Domain(ContractModel):
    id: Identifier
    name: str = Field(min_length=1)
    anchors: dict[str, str]

    _validate_id = field_validator("id")(validate_identifier)
    _validate_anchors = field_validator("anchors")(validate_anchor_map)


class Question(ContractModel):
    id: Identifier
    domain_id: Identifier
    text: str = Field(min_length=1)
    anchors: dict[str, str]

    _validate_ids = field_validator("id", "domain_id")(validate_identifier)
    _validate_anchors = field_validator("anchors")(validate_anchor_map)


class ReadinessContract(ContractModel):
    profile_id: Literal["quick-v1"]
    domain_aggregation: Literal["median_low"]
    minimum_answered_per_domain: Literal[2]
    minimum_answered_total: Literal[27]
    labels: dict[str, str]

    _validate_labels = field_validator("labels")(validate_label_map)


class GateRule(ContractModel):
    id: Identifier
    operand_id: str = Field(min_length=1)
    source: Literal["domain_score", "diagnostic_fact"]
    operator: Literal["le", "eq"]
    threshold: int | bool
    cap: int = Field(ge=0, le=4)

    _validate_id = field_validator("id")(validate_identifier)


class GateBundle(ContractModel):
    id: Identifier
    version: Literal[1]
    rules: list[GateRule] = Field(min_length=7, max_length=7)

    _validate_id = field_validator("id")(validate_identifier)


class DiagnosticFact(ContractModel):
    id: Identifier
    domain_id: Identifier
    type: Literal["integer", "boolean"]

    _validate_id = field_validator("id", "domain_id")(validate_identifier)


class ArchitectureReference(ContractModel):
    id: Identifier
    title: str = Field(min_length=1)

    _validate_id = field_validator("id")(validate_identifier)


class RecommendationReference(ContractModel):
    id: Identifier
    architecture_id: Identifier
    demo_stage_ids: list[Identifier]

    _validate_id = field_validator("id", "architecture_id")(validate_identifier)
    _validate_demo_stage_ids = field_validator("demo_stage_ids")(validate_unique_identifiers)


class FindingRuleReference(ContractModel):
    id: Identifier
    recommendation_id: Identifier
    gate_id: Identifier | None = None

    _validate_id = field_validator("id", "recommendation_id")(validate_identifier)


class TechnologyMappingReference(ContractModel):
    id: Identifier
    architecture_id: Identifier
    recommendation_ids: list[Identifier]

    _validate_id = field_validator("id", "architecture_id")(validate_identifier)
    _validate_recommendation_ids = field_validator("recommendation_ids")(
        validate_unique_identifiers
    )


class Framework(ContractModel):
    schema_version: SchemaVersion
    framework_version: FrameworkVersion
    domains: list[Domain] = Field(min_length=10, max_length=10)
    questions: list[Question] = Field(min_length=30, max_length=30)
    readiness: ReadinessContract
    gate_bundle: GateBundle
    diagnostic_facts: list[DiagnosticFact]
    architectures: list[ArchitectureReference]
    recommendations: list[RecommendationReference]
    finding_rules: list[FindingRuleReference]
    technology_mappings: list[TechnologyMappingReference]
    demo_stage_ids: list[Identifier]
    report_sections: list[Identifier] = Field(min_length=12, max_length=12)

    _validate_unique_lists = field_validator("demo_stage_ids", "report_sections")(
        validate_unique_identifiers
    )


class ManifestArtifact(ContractModel):
    path: str
    sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    origin: Literal["tracked", "generated", "historical"] | None = None
    availability: Literal["available", "current", "historical", "unavailable"] | None = None
    description: str | None = Field(default=None, min_length=1, max_length=2048)

    _validate_path = field_validator("path")(validate_manifest_relative_posix_path)


class ManifestCommand(ContractModel):
    command: str = Field(min_length=1, max_length=512)
    purpose: str = Field(min_length=1, max_length=1024)
    eligible_for_automation: bool
    automated: bool
    automation_rationale: str = Field(min_length=1, max_length=1024)

    @model_validator(mode="after")
    def validate_automation_eligibility(self) -> ManifestCommand:
        if self.automated and not self.eligible_for_automation:
            raise ValueError("an ineligible command cannot be declared automated")
        return self


class ManifestProvenance(ContractModel):
    input_sha: str = Field(pattern=r"^[0-9a-f]{40}$")
    evidence_kind: Literal["current", "historical", "configured", "unavailable"]
    current_execution: Literal["executed", "unexecuted", "not-applicable"]
    references: list[str]

    @field_validator("references")
    @classmethod
    def validate_references(cls, value: list[str]) -> list[str]:
        if len(value) != len(set(value)):
            raise ValueError("provenance references must be unique")
        return [validate_manifest_relative_posix_path(item) for item in value]


class DemoStageManifest(ContractModel):
    schema_version: SchemaVersion
    demo_content_version: Literal["1.0.0"]
    stage_id: Identifier
    status: Literal["planned", "executed", "historical", "unavailable"]
    artifacts: list[ManifestArtifact]
    commands: list[ManifestCommand] | None = Field(default=None, min_length=1)
    expected_contracts: list[str] | None = Field(default=None, min_length=1)
    cleanup: list[ManifestCommand] | None = Field(default=None, min_length=1)
    limitations: list[str] | None = Field(default=None, min_length=1)
    provenance: ManifestProvenance | None = None
    non_scoring: Literal[True] | None = None

    _validate_stage_id = field_validator("stage_id")(validate_identifier)


class DatasetOwner(ContractModel):
    name: str = Field(min_length=1, max_length=256)
    accountable_role: str = Field(min_length=1, max_length=256)


class DatasetColumn(ContractModel):
    name: Identifier
    type: str = Field(min_length=1, max_length=128)
    nullable: bool
    description: str = Field(min_length=1, max_length=1024)

    _validate_name = field_validator("name")(validate_identifier)


class DatasetContract(ContractModel):
    schema_path: str = Field(alias="schema", serialization_alias="schema")
    grain: str = Field(min_length=1, max_length=1024)
    columns: list[DatasetColumn] = Field(min_length=1)

    _validate_schema = field_validator("schema_path")(validate_manifest_relative_posix_path)


class DatasetServiceLevel(ContractModel):
    objective: str = Field(min_length=1, max_length=1024)
    verification: str = Field(min_length=1, max_length=512)


class DatasetServiceLevels(ContractModel):
    quality: DatasetServiceLevel
    freshness: DatasetServiceLevel


class DatasetAccess(ContractModel):
    classification: Literal["synthetic-pii-derived"]
    approved_role_ids: list[Identifier] = Field(min_length=1)
    policy_path: str
    prohibited_fields: list[Identifier] = Field(min_length=1)

    _validate_policy_path = field_validator("policy_path")(
        validate_manifest_relative_posix_path
    )
    _validate_roles = field_validator("approved_role_ids")(validate_unique_identifiers)
    _validate_fields = field_validator("prohibited_fields")(validate_unique_identifiers)


class DatasetLineage(ContractModel):
    sources: list[Identifier] = Field(min_length=1)
    model_path: str
    metadata_references: list[str] = Field(min_length=1)

    _validate_sources = field_validator("sources")(validate_unique_identifiers)
    _validate_model_path = field_validator("model_path")(
        validate_manifest_relative_posix_path
    )

    @field_validator("metadata_references")
    @classmethod
    def validate_metadata_references(cls, value: list[str]) -> list[str]:
        if len(value) != len(set(value)):
            raise ValueError("metadata references must be unique")
        return [validate_manifest_relative_posix_path(item) for item in value]


class AIReadyDatasetManifest(ContractModel):
    schema_version: SchemaVersion
    dataset_id: Identifier
    dataset_version: str = Field(pattern=r"^[0-9]+\.[0-9]+\.[0-9]+$")
    source_stage_ids: list[Identifier] = Field(min_length=1)
    artifact_path: str
    sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    row_count: int = Field(ge=0)
    owner: DatasetOwner | None = None
    contract: DatasetContract | None = None
    service_levels: DatasetServiceLevels | None = None
    access: DatasetAccess | None = None
    lineage: DatasetLineage | None = None
    reproduction: list[ManifestCommand] | None = Field(default=None, min_length=1)
    source_checksums: list[ManifestArtifact] | None = Field(default=None, min_length=1)
    limitations: list[str] | None = Field(default=None, min_length=1)
    synthetic_data: Literal[True] | None = None
    non_scoring: Literal[True] | None = None

    _validate_dataset_id = field_validator("dataset_id")(validate_identifier)
    _validate_artifact_path = field_validator("artifact_path")(
        validate_manifest_relative_posix_path
    )

    @field_validator("source_stage_ids")
    @classmethod
    def validate_stage_ids(cls, value: list[str]) -> list[str]:
        if len(value) != len(set(value)):
            raise ValueError("source stage IDs must be unique")
        return [validate_identifier(item) for item in value]
