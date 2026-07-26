"""Strict models and cross-reference validation for advisory catalog content."""

from __future__ import annotations

import re
from collections import Counter
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator

from assessment.domain.errors import ContentValidationError, InvalidPathError
from assessment.domain.models import validate_identifier

CatalogVersion = Literal["1.0.0"]
ProvenanceType = Literal[
    "self-report",
    "customer-evidence",
    "architect-judgment",
    "demo-illustration",
]
ArchitectureTheme = Literal[
    "quality",
    "governance-ownership",
    "metadata-lineage",
    "security-privacy-policy",
    "platform-integration",
    "operations",
    "ai-ready-data-products",
]
SAFE_PATH_PART = re.compile(r"^[A-Za-z0-9._-]+$")
EXPECTED_CAPABILITY_IDS = (
    "STR",
    "ING",
    "STO",
    "TRN",
    "QUA",
    "LIN",
    "GOV",
    "SEC",
    "OPS",
    "AID",
)
EXPECTED_ARCHITECTURE_IDS = {
    "ARCH-QUALITY-GATE",
    "ARCH-OPERATING-MODEL",
    "ARCH-GOVERNANCE-CONTROL",
    "ARCH-METADATA-LINEAGE",
    "ARCH-PRIVACY-CONTROLS",
    "ARCH-POLICY-ACCESS",
    "ARCH-PLATFORM-INTEGRATION",
    "ARCH-AI-DATA-OPERATIONS",
    "ARCH-VERSIONED-PRODUCT",
}
EXPECTED_PROFILE_IDS = (
    "aws-first-profile",
    "local-demo-evidence",
    "deferred-alternatives",
)
EXPECTED_AWS_ROLE_SELECTIONS = {
    "object-storage": "Amazon S3",
    "data-catalog": "AWS Glue Data Catalog",
    "query": "Amazon Athena",
    "access-governance": "AWS Lake Formation",
    "transformation": "dbt Core with dbt-athena",
    "data-quality": "Soda Core",
    "metadata-lineage": "OpenMetadata",
    "analytics": "Apache Superset",
    "infrastructure-source": "Terraform",
    "synthetic-data": "Deterministic synthetic generator",
}
EXPECTED_DIAGRAM_IDS = (
    "executive-ai-readiness",
    "logical-platform-context",
    "engagement-lifecycle",
    "scoring-and-gates",
    "security-and-access",
    "metadata-and-lineage",
    "demo-evidence-mapping",
)
EXPECTED_FINDING_IDS = {
    "F-OWNERSHIP",
    "F-QUALITY",
    "F-PRIVACY",
    "F-SECURITY",
    "F-GOVERNANCE",
    "F-LINEAGE",
    "F-REPRODUCIBILITY",
    "F-AI-OPERATING",
}
EXPECTED_RECOMMENDATION_IDS = {
    item.replace("F-", "R-", 1) for item in EXPECTED_FINDING_IDS
}
EXPECTED_PROVENANCE_TYPES = {
    "self-report",
    "customer-evidence",
    "architect-judgment",
    "demo-illustration",
}
EXPECTED_DEMO_STAGE_IDS = (
    "DEMO-INGESTION",
    "DEMO-QUALITY-QUARANTINE",
    "DEMO-TRANSFORMATION",
    "DEMO-METADATA",
    "DEMO-LINEAGE",
    "DEMO-GOVERNANCE",
    "DEMO-POLICY-ACCESS",
    "DEMO-SERVING",
    "DEMO-AI-READY-PUBLICATION",
)
EXPECTED_DEMO_REFERENCE_IDS = {
    f"DEMO-PLACEHOLDER-{name}"
    for name in (
        "OWNERSHIP",
        "QUALITY",
        "PRIVACY",
        "SECURITY",
        "GOVERNANCE",
        "LINEAGE",
        "REPRODUCIBILITY",
        "AI-OPERATIONS",
    )
}


class CatalogModel(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)


def _identifier(value: str) -> str:
    return validate_identifier(value)


def _identifiers(value: list[str]) -> list[str]:
    validated = [_identifier(item) for item in value]
    if len(validated) != len(set(validated)):
        raise ValueError("identifier references must be unique")
    return validated


def validate_catalog_relative_path(value: str) -> str:
    if not value or value.startswith("/") or "\\" in value or "\x00" in value:
        raise InvalidPathError(f"unsafe catalog-relative path: {value!r}")
    parts = value.split("/")
    if any(
        part in {"", ".", ".."} or not SAFE_PATH_PART.fullmatch(part)
        for part in parts
    ):
        raise InvalidPathError(f"unsafe catalog-relative path: {value!r}")
    return value


class EvidenceExample(CatalogModel):
    provenance: ProvenanceType
    label: str = Field(min_length=1, max_length=128)
    example: str = Field(min_length=12, max_length=2048)
    scoring_effect: Literal["assessment-input", "confidence-only", "advisory-only", "none"]


class Capability(CatalogModel):
    id: str
    name: str = Field(min_length=1, max_length=256)
    customer_language: str = Field(min_length=12, max_length=2048)
    architect_language: str = Field(min_length=12, max_length=2048)
    evidence_examples: list[EvidenceExample] = Field(min_length=4, max_length=4)
    architecture_ids: list[str] = Field(min_length=1)
    recommendation_ids: list[str]

    _validate_id = field_validator("id")(_identifier)
    _validate_refs = field_validator("architecture_ids", "recommendation_ids")(_identifiers)


class Architecture(CatalogModel):
    id: str
    title: str = Field(min_length=1, max_length=256)
    theme: ArchitectureTheme
    problem: str = Field(min_length=12)
    forces: list[str] = Field(min_length=1)
    logical_components: list[str] = Field(min_length=1)
    controls: list[str] = Field(min_length=1)
    data_flows: list[str] = Field(min_length=1)
    trade_offs: list[str] = Field(min_length=1)
    evidence_expectations: list[str] = Field(min_length=1)
    capability_ids: list[str] = Field(min_length=1)
    finding_ids: list[str]
    recommendation_ids: list[str]
    diagram_ids: list[str]
    vendor_products: list[str] = Field(max_length=0)

    _validate_id = field_validator("id")(_identifier)
    _validate_refs = field_validator(
        "capability_ids",
        "finding_ids",
        "recommendation_ids",
        "diagram_ids",
    )(_identifiers)


class TechnologyRole(CatalogModel):
    id: str
    role: str = Field(min_length=1)
    selected_tool: str | None = Field(default=None, min_length=1)
    alternatives: list[str]
    capability_ids: list[str] = Field(min_length=1)
    architecture_ids: list[str] = Field(min_length=1)
    constraints: list[str] = Field(min_length=1)

    _validate_id = field_validator("id")(_identifier)
    _validate_refs = field_validator("capability_ids", "architecture_ids")(_identifiers)


class TechnologyProfile(CatalogModel):
    id: str
    title: str = Field(min_length=1)
    kind: Literal[
        "named-implementation",
        "local-demo-evidence",
        "deferred-alternatives",
    ]
    provider: str | None = None
    content_only: Literal[True]
    executable: Literal[False]
    read_only: bool
    published_date: str = Field(pattern=r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$")
    limitations: list[str] = Field(min_length=1)
    roles: list[TechnologyRole] = Field(min_length=1)

    _validate_id = field_validator("id")(_identifier)


class Diagram(CatalogModel):
    id: str
    audience: str = Field(min_length=1)
    purpose: str = Field(min_length=12)
    source_path: str
    svg_path: str
    accessible_title: str = Field(min_length=1)
    accessible_description: str = Field(min_length=12)
    text_alternative: str = Field(min_length=12)

    _validate_id = field_validator("id")(_identifier)
    _validate_paths = field_validator("source_path", "svg_path")(validate_catalog_relative_path)


class CatalogBundle(CatalogModel):
    version: CatalogVersion
    capabilities: list[Capability] = Field(min_length=10, max_length=10)
    architectures: list[Architecture] = Field(min_length=1)
    technology_profiles: list[TechnologyProfile] = Field(min_length=3, max_length=3)
    diagrams: list[Diagram] = Field(min_length=7, max_length=7)

    @staticmethod
    def _duplicates(items: list[Any], *, context: str) -> None:
        counts = Counter(str(item.id) for item in items)
        duplicates = sorted(item for item, count in counts.items() if count > 1)
        if duplicates:
            raise ContentValidationError(f"{context}: duplicate IDs: {', '.join(duplicates)}")

    @classmethod
    def validate_semantics(cls, document: dict[str, Any]) -> CatalogBundle:
        try:
            bundle = cls.model_validate(document)
        except ValidationError as error:
            raise ContentValidationError(f"catalog: {error}") from error
        cls._duplicates(bundle.capabilities, context="capabilities")
        cls._duplicates(bundle.architectures, context="architectures")
        cls._duplicates(bundle.technology_profiles, context="technology profiles")
        cls._duplicates(bundle.diagrams, context="diagrams")
        if tuple(item.id for item in bundle.capabilities) != EXPECTED_CAPABILITY_IDS:
            raise ContentValidationError("catalog: exact capability domains are required")
        if {item.id for item in bundle.architectures} != EXPECTED_ARCHITECTURE_IDS:
            raise ContentValidationError(
                "catalog: exact logical architecture patterns are required"
            )
        architecture_text = "\n".join(
            str(item.model_dump(mode="json")) for item in bundle.architectures
        ).lower()
        if any(
            term in architecture_text
            for term in (
                "amazon",
                "aws ",
                "azure",
                "google cloud",
                "snowflake",
                "databricks",
            )
        ):
            raise ContentValidationError(
                "catalog: logical architecture content must remain vendor-neutral"
            )
        if tuple(item.id for item in bundle.technology_profiles) != EXPECTED_PROFILE_IDS:
            raise ContentValidationError(
                "catalog: AWS, local demo, and deferred profiles are required in order"
            )
        if tuple(item.id for item in bundle.diagrams) != EXPECTED_DIAGRAM_IDS:
            raise ContentValidationError("catalog: exact audience diagram set is required")
        capability_ids = {item.id for item in bundle.capabilities}
        capability_architectures = {
            item.id: set(item.architecture_ids) for item in bundle.capabilities
        }
        architecture_ids = {item.id for item in bundle.architectures}
        diagram_ids = {item.id for item in bundle.diagrams}
        recommendation_ids = {
            recommendation_id
            for capability in bundle.capabilities
            for recommendation_id in capability.recommendation_ids
        }
        for capability in bundle.capabilities:
            if {
                example.provenance for example in capability.evidence_examples
            } != EXPECTED_PROVENANCE_TYPES:
                raise ContentValidationError(
                    f"capability {capability.id}: all evidence provenance types are required"
                )
            if not set(capability.architecture_ids) <= architecture_ids:
                raise ContentValidationError(
                    f"capability {capability.id}: unresolved architecture reference"
                )
        for architecture in bundle.architectures:
            if not set(architecture.capability_ids) <= capability_ids:
                raise ContentValidationError(
                    f"architecture {architecture.id}: unresolved capability reference"
                )
            if any(
                architecture.id not in capability_architectures[capability_id]
                for capability_id in architecture.capability_ids
            ):
                raise ContentValidationError(
                    f"architecture {architecture.id}: capability mapping is inconsistent"
                )
            if not set(architecture.recommendation_ids) <= recommendation_ids:
                raise ContentValidationError(
                    f"architecture {architecture.id}: unresolved recommendation reference"
                )
            if not set(architecture.diagram_ids) <= diagram_ids:
                raise ContentValidationError(
                    f"architecture {architecture.id}: unresolved diagram reference"
                )
        for profile in bundle.technology_profiles:
            role_ids = [role.id for role in profile.roles]
            if len(role_ids) != len(set(role_ids)):
                raise ContentValidationError(
                    f"technology profile {profile.id}: duplicate role IDs"
                )
            for role in profile.roles:
                if not set(role.capability_ids) <= capability_ids:
                    raise ContentValidationError(
                        f"technology role {role.id}: unresolved capability reference"
                    )
                if not set(role.architecture_ids) <= architecture_ids:
                    raise ContentValidationError(
                        f"technology role {role.id}: unresolved architecture reference"
                    )
                if profile.kind == "deferred-alternatives":
                    if role.selected_tool is not None or not role.alternatives:
                        raise ContentValidationError(
                            f"technology role {role.id}: deferred alternatives cannot select a tool"
                        )
                elif role.selected_tool is None or role.alternatives:
                    raise ContentValidationError(
                        f"technology role {role.id}: exactly one selected tool is required"
                    )
        aws_profile = bundle.technology_profiles[0]
        if (
            aws_profile.provider != "AWS"
            or {
                role.id: role.selected_tool for role in aws_profile.roles
            } != EXPECTED_AWS_ROLE_SELECTIONS
        ):
            raise ContentValidationError(
                "catalog: AWS profile must contain the planned role selections"
            )
        technology_text = "\n".join(
            str(profile.model_dump(mode="json"))
            for profile in bundle.technology_profiles
        ).lower()
        if any(
            marker in technology_text
            for marker in (
                "aws_access_key",
                "boto3",
                "s3://",
                "terraform apply",
                "terraform destroy",
            )
        ):
            raise ContentValidationError(
                "catalog: technology mappings contain an executable cloud marker"
            )
        finding_ids = {
            finding_id
            for architecture in bundle.architectures
            for finding_id in architecture.finding_ids
        }
        if finding_ids != EXPECTED_FINDING_IDS:
            raise ContentValidationError("catalog: complete finding coverage is required")
        architecture_recommendation_ids = {
            recommendation_id
            for architecture in bundle.architectures
            for recommendation_id in architecture.recommendation_ids
        }
        if architecture_recommendation_ids != EXPECTED_RECOMMENDATION_IDS:
            raise ContentValidationError("catalog: complete recommendation coverage is required")
        return bundle

    def technology_profile(self, profile_id: str) -> TechnologyProfile:
        _identifier(profile_id)
        for profile in self.technology_profiles:
            if profile.id == profile_id:
                return profile
        raise ContentValidationError(f"technology profile {profile_id!r}: not found")

    def architecture(self, architecture_id: str) -> Architecture:
        _identifier(architecture_id)
        for architecture in self.architectures:
            if architecture.id == architecture_id:
                return architecture
        raise ContentValidationError(f"architecture {architecture_id!r}: not found")


class ArtifactLocation(CatalogModel):
    label: str = Field(min_length=1)
    path: str
    expected: str = Field(min_length=12)
    status: Literal["available", "unavailable"]

    _validate_path = field_validator("path")(validate_catalog_relative_path)


class DemoStage(CatalogModel):
    id: str
    title: str = Field(min_length=1)
    presenter_goal: str = Field(min_length=12)
    prerequisites: list[str] = Field(min_length=1)
    artifacts: list[ArtifactLocation] = Field(min_length=1)
    expected_evidence: list[str] = Field(min_length=1)
    limitations: list[str] = Field(min_length=1)
    cleanup: list[str] = Field(min_length=1)
    read_only: Literal[True]
    non_scoring: Literal[True]

    _validate_id = field_validator("id")(_identifier)


class DemoEvidenceLink(CatalogModel):
    id: str
    stage_ids: list[str] = Field(min_length=1)
    explanation: str = Field(min_length=12)

    _validate_id = field_validator("id")(_identifier)
    _validate_stage_ids = field_validator("stage_ids")(_identifiers)


class DemoCatalog(CatalogModel):
    version: CatalogVersion
    title: str = Field(min_length=1)
    presenter_purpose: str = Field(min_length=12)
    non_scoring_disclaimer: str = Field(min_length=12)
    automation_eligible_steps: int = Field(gt=0)
    automation_automated_steps: int = Field(ge=0)
    operating_boundary: list[str] = Field(min_length=1)
    stage_order: list[str] = Field(min_length=1)
    stages: list[DemoStage] = Field(min_length=1)
    evidence_links: list[DemoEvidenceLink] = Field(min_length=1)

    _validate_stage_order = field_validator("stage_order")(_identifiers)

    @classmethod
    def validate_semantics(cls, document: dict[str, Any]) -> DemoCatalog:
        try:
            catalog = cls.model_validate(document)
        except ValidationError as error:
            raise ContentValidationError(f"demo catalog: {error}") from error
        CatalogBundle._duplicates(catalog.stages, context="demo stages")
        CatalogBundle._duplicates(catalog.evidence_links, context="demo evidence links")
        if tuple(stage.id for stage in catalog.stages) != EXPECTED_DEMO_STAGE_IDS:
            raise ContentValidationError("demo catalog: exact presenter stages are required")
        if tuple(catalog.stage_order) != EXPECTED_DEMO_STAGE_IDS:
            raise ContentValidationError(
                "demo catalog: guide stage order must match the presenter stages"
            )
        if (
            catalog.automation_automated_steps > catalog.automation_eligible_steps
            or catalog.automation_automated_steps * 100
            < catalog.automation_eligible_steps * 95
        ):
            raise ContentValidationError(
                "demo catalog: eligible automation must be an explicit ratio of at least 95%"
            )
        if {link.id for link in catalog.evidence_links} != EXPECTED_DEMO_REFERENCE_IDS:
            raise ContentValidationError(
                "demo catalog: exact finding evidence references are required"
            )
        stage_ids = {stage.id for stage in catalog.stages}
        for link in catalog.evidence_links:
            if not set(link.stage_ids) <= stage_ids:
                raise ContentValidationError(
                    f"demo evidence link {link.id}: unresolved stage reference"
                )
        return catalog

    def evidence_link(self, reference_id: str) -> DemoEvidenceLink:
        _identifier(reference_id)
        for link in self.evidence_links:
            if link.id == reference_id:
                return link
        raise ContentValidationError(f"demo evidence reference {reference_id!r}: not found")
