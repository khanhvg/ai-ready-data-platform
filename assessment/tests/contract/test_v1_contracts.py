from __future__ import annotations

import copy
import os
from collections.abc import Callable
from importlib import resources
from pathlib import Path
from typing import Any

import pytest

from assessment.cli import main as assessment_main
from assessment.content.loader import load_markdown, load_yaml
from assessment.content.schemas import load_schema, validate_document
from assessment.content.semantics import validate_framework_semantics
from assessment.domain.errors import ContentValidationError
from assessment.domain.models import (
    AIReadyDatasetManifest,
    AnswerEvidenceDocument,
    DemoStageManifest,
    Engagement,
    Framework,
    Recipe,
    Report,
)

ROOT = Path(__file__).resolve().parents[3]
SCHEMA_NAMES = ("framework", "engagement", "answer", "report", "recipe")
DEMO_SCHEMA_NAMES = ("demo-stage-manifest", "ai-ready-dataset-manifest")
PUBLIC_SCHEMA_FILENAMES = {
    *(f"{name}-v1.schema.json" for name in SCHEMA_NAMES),
    *(f"{name}-v1.schema.json" for name in DEMO_SCHEMA_NAMES),
}


@pytest.fixture()
def framework_document() -> dict[str, object]:
    return {
        "schema_version": "1.0.0",
        "framework_version": "1.0.0",
        "domains": [
            {
                "id": domain,
                "name": f"{domain} domain",
                "anchors": {
                    str(level): f"Observable {domain} state at level {level}" for level in range(5)
                },
            }
            for domain in ("STR", "ING", "STO", "TRN", "QUA", "LIN", "GOV", "SEC", "OPS", "AID")
        ],
        "questions": [
            {
                "id": f"Q-{domain}-{number:02d}",
                "domain_id": domain,
                "text": f"How is {domain} control {number} operated?",
                "anchors": {
                    str(level): f"Observable {domain} question {number} level {level}"
                    for level in range(5)
                },
            }
            for domain in ("STR", "ING", "STO", "TRN", "QUA", "LIN", "GOV", "SEC", "OPS", "AID")
            for number in range(1, 4)
        ],
        "readiness": {
            "profile_id": "quick-v1",
            "domain_aggregation": "median_low",
            "minimum_answered_per_domain": 2,
            "minimum_answered_total": 27,
            "labels": {
                "0": "Not ready",
                "1": "Foundation blocked",
                "2": "Experiment-ready only",
                "3": "Production-ready",
                "4": "Optimized production-ready",
            },
        },
        "gate_bundle": {
            "id": "quick-readiness-gates",
            "version": 1,
            "rules": [
                {
                    "id": "G-QUALITY",
                    "operand_id": "domain.QUA",
                    "source": "domain_score",
                    "operator": "le",
                    "threshold": 1,
                    "cap": 1,
                },
                {
                    "id": "G-SECURITY",
                    "operand_id": "domain.SEC",
                    "source": "domain_score",
                    "operator": "le",
                    "threshold": 1,
                    "cap": 1,
                },
                {
                    "id": "G-PRIVACY",
                    "operand_id": "fact.privacy_control_level",
                    "source": "diagnostic_fact",
                    "operator": "le",
                    "threshold": 1,
                    "cap": 1,
                },
                {
                    "id": "G-GOVERNANCE",
                    "operand_id": "domain.GOV",
                    "source": "domain_score",
                    "operator": "le",
                    "threshold": 1,
                    "cap": 2,
                },
                {
                    "id": "G-OWNERSHIP",
                    "operand_id": "fact.ownership_control_level",
                    "source": "diagnostic_fact",
                    "operator": "le",
                    "threshold": 1,
                    "cap": 2,
                },
                {
                    "id": "G-LINEAGE",
                    "operand_id": "fact.critical_lineage",
                    "source": "diagnostic_fact",
                    "operator": "eq",
                    "threshold": False,
                    "cap": 2,
                },
                {
                    "id": "G-REPRODUCIBILITY",
                    "operand_id": "fact.reproducible_versioned",
                    "source": "diagnostic_fact",
                    "operator": "eq",
                    "threshold": False,
                    "cap": 2,
                },
            ],
        },
        "diagnostic_facts": [
            {"id": "privacy_control_level", "domain_id": "GOV", "type": "integer"},
            {"id": "ownership_control_level", "domain_id": "STR", "type": "integer"},
            {"id": "critical_lineage", "domain_id": "LIN", "type": "boolean"},
            {"id": "reproducible_versioned", "domain_id": "AID", "type": "boolean"},
        ],
        "architectures": [{"id": "ARCH-FOUNDATION", "title": "Foundation"}],
        "recommendations": [
            {
                "id": "REC-FOUNDATION",
                "architecture_id": "ARCH-FOUNDATION",
                "demo_stage_ids": ["DEMO-INGEST"],
            }
        ],
        "finding_rules": [
            {
                "id": "F-QUALITY",
                "recommendation_id": "REC-FOUNDATION",
                "gate_id": "G-QUALITY",
            }
        ],
        "technology_mappings": [
            {
                "id": "MAP-LOCAL",
                "architecture_id": "ARCH-FOUNDATION",
                "recommendation_ids": ["REC-FOUNDATION"],
            }
        ],
        "demo_stage_ids": ["DEMO-INGEST"],
        "report_sections": [
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
        ],
    }


def test_all_seven_public_schemas_are_valid_and_versioned() -> None:
    for name in SCHEMA_NAMES:
        schema = load_schema(ROOT / "assessment" / "contracts" / f"{name}-v1.schema.json")
        assert schema["$id"].endswith(f"/{name}/1.0.0")
        assert schema["additionalProperties"] is False
    for name in DEMO_SCHEMA_NAMES:
        schema = load_schema(ROOT / "demo" / "contracts" / f"{name}-v1.schema.json")
        assert schema["$id"].endswith(f"/{name}/1.0.0")
        assert schema["additionalProperties"] is False


def test_all_seven_public_schemas_are_packaged_as_authoritative_resources() -> None:
    packaged_root = resources.files("assessment").joinpath("public_schemas")
    try:
        packaged_names = {
            resource.name
            for resource in packaged_root.iterdir()
            if resource.name.endswith(".schema.json")
        }
    except FileNotFoundError:
        packaged_names = set()
    assert packaged_names == PUBLIC_SCHEMA_FILENAMES

    repository_schemas = {
        **{
            f"{name}-v1.schema.json": ROOT
            / "assessment"
            / "contracts"
            / f"{name}-v1.schema.json"
            for name in SCHEMA_NAMES
        },
        **{
            f"{name}-v1.schema.json": ROOT
            / "demo"
            / "contracts"
            / f"{name}-v1.schema.json"
            for name in DEMO_SCHEMA_NAMES
        },
    }
    for filename, repository_path in repository_schemas.items():
        assert packaged_root.joinpath(filename).read_bytes() == repository_path.read_bytes()


def test_schema_cli_rejects_an_explicit_root_without_public_authority(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    assert assessment_main(["schema", "--repo-root", str(tmp_path)]) == 2
    assert "no public JSON Schema authority" in capsys.readouterr().err


def test_schema_and_typed_models_accept_and_reject_the_same_documents(
    framework_document: dict[str, object],
) -> None:
    documents = {
        "framework": (framework_document, Framework),
        "engagement": (
            {
                "schema_version": "1.0.0",
                "engagement_id": "engagement-001",
                "framework_version": "1.0.0",
                "catalog_version": "1.0.0",
                "demo_content_version": "1.0.0",
                "assessment_profile_id": "quick-v1",
                "gate_bundle_version": 1,
            },
            Engagement,
        ),
        "answer": (
            {
                "schema_version": "1.0.0",
                "engagement_id": "engagement-001",
                "framework_version": "1.0.0",
                "answers": [
                    {
                        "question_id": "Q-STR-01",
                        "rating": 2,
                        "evidence_status": "Self-reported",
                        "note": "Named ownership forum is used.",
                        "evidence_refs": ["evidence/files/ownership.txt"],
                    }
                ],
                "diagnostic_facts": {"privacy_control_level": 2},
            },
            AnswerEvidenceDocument,
        ),
        "report": (
            {
                "schema_version": "1.0.0",
                "engagement_id": "engagement-001",
                "framework_version": "1.0.0",
                "sections": [
                    {"id": section_id, "content": {}}
                    for section_id in framework_document["report_sections"]
                ],
            },
            Report,
        ),
        "recipe": (
            {
                "schema_version": "1.0.0",
                "recipe_id": "recipe-retail",
                "framework_version": "1.0.0",
                "title": "Retail recipe",
                "capability_ids": ["STR"],
                "question_ids": ["Q-STR-01"],
            },
            Recipe,
        ),
        "demo-stage-manifest": (
            {
                "schema_version": "1.0.0",
                "demo_content_version": "1.0.0",
                "stage_id": "DEMO-INGEST",
                "status": "planned",
                "artifacts": [
                    {
                        "path": "demo/artifacts/ingest.json",
                        "sha256": "0" * 64,
                    }
                ],
            },
            DemoStageManifest,
        ),
        "ai-ready-dataset-manifest": (
            {
                "schema_version": "1.0.0",
                "dataset_id": "retail-ai-ready",
                "dataset_version": "1.0.0",
                "source_stage_ids": ["DEMO-INGEST"],
                "artifact_path": "demo/artifacts/retail.parquet",
                "sha256": "0" * 64,
                "row_count": 0,
            },
            AIReadyDatasetManifest,
        ),
    }
    for name, (document, model) in documents.items():
        schema_root = "demo" if name in DEMO_SCHEMA_NAMES else "assessment"
        schema_path = ROOT / schema_root / "contracts" / f"{name}-v1.schema.json"
        schema = load_schema(schema_path)
        assert set(schema["properties"]) == set(model.model_fields)
        assert set(schema["required"]) == set(model.model_fields)
        validate_document(document, schema_path)
        assert model.model_validate(document).model_dump(mode="json", exclude_none=True) == document

        invalid = copy.deepcopy(document)
        invalid["unexpected"] = True
        with pytest.raises(ContentValidationError):
            validate_document(invalid, schema_path)
        with pytest.raises(ValueError):
            model.model_validate(invalid)

        wrong_version = copy.deepcopy(document)
        wrong_version["schema_version"] = "2.0.0"
        with pytest.raises(ContentValidationError):
            validate_document(wrong_version, schema_path)
        with pytest.raises(ValueError):
            model.model_validate(wrong_version)

        dot_component = copy.deepcopy(document)
        if name == "answer":
            dot_component["answers"][0]["evidence_refs"] = ["evidence/./proof.txt"]
        elif name == "demo-stage-manifest":
            dot_component["artifacts"][0]["path"] = "demo/./artifact.json"
        elif name == "ai-ready-dataset-manifest":
            dot_component["artifact_path"] = "demo/./dataset.parquet"
        else:
            continue
        with pytest.raises(ContentValidationError):
            validate_document(dot_component, schema_path)
        with pytest.raises(ValueError):
            model.model_validate(dot_component)


@pytest.mark.parametrize(
    "mutate",
    [
        lambda value: value["domains"][0].update({"id": "invalid/id"}),
        lambda value: value["domains"][0].update({"name": ""}),
        lambda value: value["domains"][0]["anchors"].update({"0": "too short"}),
        lambda value: value["questions"][0].update({"text": ""}),
        lambda value: value["readiness"]["labels"].update({"0": ""}),
        lambda value: value["gate_bundle"]["rules"][0].update({"operand_id": ""}),
        lambda value: value["architectures"][0].update({"title": ""}),
        lambda value: value["recommendations"][0].update(
            {"demo_stage_ids": ["DEMO-INGEST", "DEMO-INGEST"]}
        ),
        lambda value: value["finding_rules"][0].update({"gate_id": "invalid/id"}),
        lambda value: value["technology_mappings"][0].update(
            {"recommendation_ids": ["REC-FOUNDATION", "REC-FOUNDATION"]}
        ),
        lambda value: value.update({"demo_stage_ids": ["DEMO-INGEST", "DEMO-INGEST"]}),
    ],
)
def test_nested_schema_and_model_constraints_remain_in_parity(
    framework_document: dict[str, object],
    mutate: Callable[[dict[str, Any]], None],
) -> None:
    changed = copy.deepcopy(framework_document)
    mutate(changed)
    schema_path = ROOT / "assessment" / "contracts" / "framework-v1.schema.json"
    with pytest.raises(ContentValidationError):
        validate_document(changed, schema_path)
    with pytest.raises(ValueError):
        Framework.model_validate(changed)


def test_semantics_validate_coverage_references_sections_and_version_isolation(
    framework_document: dict[str, object],
) -> None:
    validate_framework_semantics(framework_document)
    mutations = [
        lambda value: value["domains"][0]["anchors"].pop("4"),
        lambda value: value["questions"].__setitem__(1, copy.deepcopy(value["questions"][0])),
        lambda value: value["questions"][0].update({"domain_id": "MISSING"}),
        lambda value: value["finding_rules"][0].update({"recommendation_id": "MISSING"}),
        lambda value: value["recommendations"][0].update({"architecture_id": "MISSING"}),
        lambda value: value["recommendations"][0].update({"demo_stage_ids": ["MISSING"]}),
        lambda value: value["report_sections"].reverse(),
        lambda value: value.update({"framework_version": "1.1.0"}),
    ]
    for mutate in mutations:
        changed = copy.deepcopy(framework_document)
        mutate(changed)
        with pytest.raises(ContentValidationError):
            validate_framework_semantics(changed)


def test_safe_bounded_yaml_and_markdown_loading(tmp_path: Path) -> None:
    yaml_path = tmp_path / "safe.yaml"
    yaml_path.write_text("schema_version: 1.0.0\nname: safe\n", encoding="utf-8")
    assert load_yaml(yaml_path)["name"] == "safe"

    yaml_path.write_text("value: !!python/object/apply:os.system ['false']\n", encoding="utf-8")
    with pytest.raises(ContentValidationError):
        load_yaml(yaml_path)
    yaml_path.write_text("defaults: &defaults {name: safe}\ncopy: *defaults\n", encoding="utf-8")
    with pytest.raises(ContentValidationError):
        load_yaml(yaml_path)

    markdown_path = tmp_path / "safe.md"
    markdown_path.write_text("# Safe\n\nPlain **authored** text.\n", encoding="utf-8")
    assert load_markdown(markdown_path).startswith("# Safe")
    markdown_path.write_text("# Unsafe\n\n<script>alert(1)</script>\n", encoding="utf-8")
    with pytest.raises(ContentValidationError):
        load_markdown(markdown_path)
    markdown_path.write_text("# Unsafe\n\n<!-- hidden raw HTML -->\n", encoding="utf-8")
    with pytest.raises(ContentValidationError):
        load_markdown(markdown_path)

    oversized = tmp_path / "large.yaml"
    oversized.write_bytes(b"a" * (1_048_576 + 1))
    with pytest.raises(ContentValidationError):
        load_yaml(oversized)


def test_authored_loader_rejects_growth_after_open(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    authored = tmp_path / "growing.yaml"
    authored.write_text("name: safe\n", encoding="utf-8")
    original_path_open = Path.open
    original_os_open = os.open
    grew = False

    def grow_after_open() -> None:
        nonlocal grew
        if grew:
            return
        grew = True
        with original_path_open(authored, "ab") as writer:
            writer.write(b"value: " + b"x" * 4_096 + b"\n")

    def racing_path_open(self: Path, *args: Any, **kwargs: Any) -> Any:
        handle = original_path_open(self, *args, **kwargs)
        mode = args[0] if args else kwargs.get("mode", "r")
        if self == authored and "r" in mode:
            grow_after_open()
        return handle

    def racing_os_open(path: Any, flags: int, *args: Any, **kwargs: Any) -> int:
        descriptor = original_os_open(path, flags, *args, **kwargs)
        if (
            isinstance(path, str | os.PathLike)
            and Path(path) == authored
            and flags & os.O_ACCMODE == os.O_RDONLY
        ):
            grow_after_open()
        return descriptor

    monkeypatch.setattr(Path, "open", racing_path_open)
    monkeypatch.setattr(os, "open", racing_os_open)
    with pytest.raises(ContentValidationError, match="64 byte limit"):
        load_yaml(authored, maximum_bytes=64)
    assert grew
