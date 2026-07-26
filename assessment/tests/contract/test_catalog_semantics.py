from __future__ import annotations

import copy
from pathlib import Path

import pytest

from assessment.catalog.loader import load_catalog, load_demo_catalog
from assessment.catalog.models import CatalogBundle, DemoCatalog
from assessment.domain.errors import ContentValidationError
from assessment.engine.evaluator import evaluate_assessment
from assessment.frameworks import load_framework

DOMAIN_IDS = ("STR", "ING", "STO", "TRN", "QUA", "LIN", "GOV", "SEC", "OPS", "AID")
FINDING_IDS = {
    "F-OWNERSHIP",
    "F-QUALITY",
    "F-PRIVACY",
    "F-SECURITY",
    "F-GOVERNANCE",
    "F-LINEAGE",
    "F-REPRODUCIBILITY",
    "F-AI-OPERATING",
}
RECOMMENDATION_IDS = {
    "R-OWNERSHIP",
    "R-QUALITY",
    "R-PRIVACY",
    "R-SECURITY",
    "R-GOVERNANCE",
    "R-LINEAGE",
    "R-REPRODUCIBILITY",
    "R-AI-OPERATING",
}
AWS_ROLE_SELECTIONS = {
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
PROVENANCE_TYPES = {
    "self-report",
    "customer-evidence",
    "architect-judgment",
    "demo-illustration",
}


def test_catalog_has_exact_domains_and_distinct_evidence_provenance() -> None:
    catalog = load_catalog()
    assert tuple(capability.id for capability in catalog.capabilities) == DOMAIN_IDS
    assert catalog.version == "1.0.0"
    for capability in catalog.capabilities:
        assert capability.customer_language
        assert capability.architect_language
        assert {example.provenance for example in capability.evidence_examples} == (
            PROVENANCE_TYPES
        )
        assert capability.architecture_ids
        assert capability.recommendation_ids


def test_all_framework_findings_recommendations_and_demo_references_resolve() -> None:
    framework = load_framework("1.0.0")
    catalog = load_catalog()
    demo = load_demo_catalog()

    assert {rule["id"] for rule in framework.finding_rules} == FINDING_IDS
    assert {item["id"] for item in framework.recommendations} == RECOMMENDATION_IDS
    assert {reference.id for reference in demo.evidence_links} == {
        item["demo_reference"] for item in framework.recommendations
    }

    architecture_ids = {architecture.id for architecture in catalog.architectures}
    recommendation_ids = {item["id"] for item in framework.recommendations}
    finding_ids = {item["id"] for item in framework.finding_rules}
    stage_ids = {stage.id for stage in demo.stages}
    for architecture in catalog.architectures:
        assert set(architecture.finding_ids) <= finding_ids
        assert set(architecture.recommendation_ids) <= recommendation_ids
    for recommendation in framework.recommendations:
        assert recommendation["architecture_reference"] in architecture_ids
        resolved = demo.evidence_link(str(recommendation["demo_reference"]))
        assert set(resolved.stage_ids) <= stage_ids


def test_vendor_neutral_patterns_cover_every_required_theme_and_reference() -> None:
    catalog = load_catalog()
    assert {architecture.theme for architecture in catalog.architectures} == {
        "quality",
        "governance-ownership",
        "metadata-lineage",
        "security-privacy-policy",
        "platform-integration",
        "operations",
        "ai-ready-data-products",
    }
    for architecture in catalog.architectures:
        assert architecture.problem
        assert architecture.forces
        assert architecture.logical_components
        assert architecture.controls
        assert architecture.data_flows
        assert architecture.trade_offs
        assert architecture.evidence_expectations
        assert not architecture.vendor_products
    referenced_findings = {
        finding_id
        for architecture in catalog.architectures
        for finding_id in architecture.finding_ids
    }
    assert referenced_findings == FINDING_IDS
    referenced_recommendations = {
        recommendation_id
        for architecture in catalog.architectures
        for recommendation_id in architecture.recommendation_ids
    }
    assert referenced_recommendations == RECOMMENDATION_IDS
    architecture_text = "\n".join(
        str(architecture.model_dump(mode="json"))
        for architecture in catalog.architectures
    ).lower()
    for vendor_term in (
        "amazon",
        "aws ",
        "azure",
        "google cloud",
        "snowflake",
        "databricks",
    ):
        assert vendor_term not in architecture_text


def test_aws_profile_is_content_only_with_exactly_one_selected_tool_per_role() -> None:
    catalog = load_catalog()
    profile = catalog.technology_profile("aws-first-profile")
    assert profile.kind == "named-implementation"
    assert profile.content_only is True
    assert profile.executable is False
    assert {role.id: role.selected_tool for role in profile.roles} == AWS_ROLE_SELECTIONS
    assert all(role.selected_tool and role.alternatives == [] for role in profile.roles)

    local = catalog.technology_profile("local-demo-evidence")
    assert local.kind == "local-demo-evidence"
    assert local.content_only is True
    assert local.executable is False
    assert local.read_only is True
    assert local is not profile

    deferred = catalog.technology_profile("deferred-alternatives")
    assert deferred.kind == "deferred-alternatives"
    assert all(role.selected_tool is None and role.alternatives for role in deferred.roles)
    all_content = "\n".join(
        str(item.model_dump(mode="json"))
        for item in catalog.technology_profiles
    ).lower()
    for executable_marker in (
        "boto3",
        "aws_access_key",
        "s3://",
        "terraform apply",
        "terraform destroy",
    ):
        assert executable_marker not in all_content


def test_demo_guide_paths_are_safe_read_only_and_non_scoring(tmp_path: Path) -> None:
    demo = load_demo_catalog(repository_root=tmp_path)
    assert demo.version == "1.0.0"
    assert demo.title == "Read-only AI-ready data platform Demo Guide"
    assert demo.presenter_purpose
    assert demo.non_scoring_disclaimer
    assert demo.operating_boundary
    assert tuple(demo.stage_order) == tuple(stage.id for stage in demo.stages)
    for stage in demo.stages:
        assert stage.presenter_goal
        assert stage.prerequisites
        assert stage.expected_evidence
        assert stage.limitations
        assert stage.cleanup
        assert stage.read_only is True
        assert stage.non_scoring is True
        for artifact in stage.artifacts:
            assert not artifact.path.startswith("/")
            assert "\\" not in artifact.path
            assert ".." not in artifact.path.split("/")
            assert artifact.status == "unavailable"


def test_demo_catalog_mutation_cannot_change_engine_result() -> None:
    framework = load_framework("1.0.0")
    answers = {
        "schema_version": "1.0.0",
        "engagement_id": "catalog-isolation",
        "framework_version": "1.0.0",
        "answers": [
            {
                "question_id": question["id"],
                "rating": 2,
                "evidence_status": "Self-reported",
                "note": "",
                "evidence_refs": [],
            }
            for question in framework.questions
        ],
        "diagnostic_facts": {
            "privacy_control_level": 2,
            "ownership_control_level": 2,
            "critical_lineage": True,
            "reproducible_versioned": True,
        },
    }
    before = evaluate_assessment(answers, framework)
    mutated_demo = copy.deepcopy(load_demo_catalog().model_dump(mode="json"))
    mutated_demo["non_scoring_disclaimer"] = "Changed demo illustration."
    DemoCatalog.model_validate(mutated_demo)
    after = evaluate_assessment(answers, framework)
    assert before == after


def test_catalog_models_fail_closed_on_duplicate_and_unresolved_references() -> None:
    document = copy.deepcopy(load_catalog().model_dump(mode="json"))
    document["capabilities"][1]["id"] = document["capabilities"][0]["id"]
    with pytest.raises(ContentValidationError, match="duplicate"):
        CatalogBundle.validate_semantics(document)

    document = copy.deepcopy(load_catalog().model_dump(mode="json"))
    document["architectures"][0]["recommendation_ids"].append("R-MISSING")
    with pytest.raises(ContentValidationError, match="unresolved"):
        CatalogBundle.validate_semantics(document)

    document = copy.deepcopy(load_catalog().model_dump(mode="json"))
    document["capabilities"][0]["id"] = "ALT"
    with pytest.raises(ContentValidationError, match="exact capability domains"):
        CatalogBundle.validate_semantics(document)

    document = copy.deepcopy(load_catalog().model_dump(mode="json"))
    document["architectures"][0]["finding_ids"] = []
    with pytest.raises(ContentValidationError, match="finding coverage"):
        CatalogBundle.validate_semantics(document)

    document = copy.deepcopy(load_catalog().model_dump(mode="json"))
    document["technology_profiles"][0]["roles"][0]["selected_tool"] = None
    with pytest.raises(ContentValidationError, match="selected tool"):
        CatalogBundle.validate_semantics(document)

    document = copy.deepcopy(load_catalog().model_dump(mode="json"))
    document["architectures"][0]["problem"] = (
        "Amazon S3 is named inside a logical architecture pattern."
    )
    with pytest.raises(ContentValidationError, match="vendor-neutral"):
        CatalogBundle.validate_semantics(document)

    document = copy.deepcopy(load_catalog().model_dump(mode="json"))
    document["capabilities"][0]["architecture_ids"].remove("ARCH-OPERATING-MODEL")
    with pytest.raises(ContentValidationError, match="inconsistent"):
        CatalogBundle.validate_semantics(document)
