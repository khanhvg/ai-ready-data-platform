from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from contextlib import nullcontext
from dataclasses import asdict
from pathlib import Path
from types import ModuleType
from unittest.mock import Mock

import pytest
import yaml

from assessment.catalog.loader import load_demo_catalog
from assessment.domain.errors import InvalidPathError
from assessment.domain.models import (
    validate_manifest_relative_posix_path,
    validate_relative_posix_path,
)
from assessment.engine.evaluator import evaluate_assessment
from assessment.frameworks import load_framework

ROOT = Path(__file__).resolve().parents[3]
EXPECTED_STAGE_FILES = {
    "ingestion.yaml",
    "quality-quarantine.yaml",
    "transformation.yaml",
    "metadata.yaml",
    "lineage.yaml",
    "governance.yaml",
    "access-control.yaml",
    "serving.yaml",
    "ai-ready-publication.yaml",
}
EXPECTED_STAGE_IDS = {
    "DEMO-INGESTION",
    "DEMO-QUALITY-QUARANTINE",
    "DEMO-TRANSFORMATION",
    "DEMO-METADATA",
    "DEMO-LINEAGE",
    "DEMO-GOVERNANCE",
    "DEMO-POLICY-ACCESS",
    "DEMO-SERVING",
    "DEMO-AI-READY-PUBLICATION",
}


def test_manifest_path_support_does_not_widen_answer_or_storage_paths() -> None:
    with pytest.raises(InvalidPathError):
        validate_relative_posix_path("evidence/files/_private.txt")
    assert (
        validate_manifest_relative_posix_path(
            "transform/dbt/models/products/_products__models.yml"
        )
        == "transform/dbt/models/products/_products__models.yml"
    )


def test_generated_current_evidence_is_ignored_and_cleanable() -> None:
    assert "demo/evidence/current/" in (ROOT / ".gitignore").read_text(encoding="utf-8")
    assert "pathlib.Path('demo/evidence/current')" in (ROOT / "Makefile").read_text(
        encoding="utf-8"
    )


def _load_module(path: Path, name: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _canonical_engine_projection(result: object) -> bytes:
    document = asdict(result)  # type: ignore[arg-type]
    projection = {
        "maturity": document["maturity"],
        "confidence": document["confidence"],
        "gates": document["gates"],
        "finding_priorities": [
            {"id": item["finding_id"], "priority": item["priority"]}
            for item in document["findings"]
        ],
    }
    return json.dumps(
        projection,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def test_phase6_stage_manifests_are_complete_rich_and_automated() -> None:
    stage_root = ROOT / "demo" / "manifests" / "stages"
    files = {path.name for path in stage_root.glob("*.yaml")}
    assert files == EXPECTED_STAGE_FILES
    documents = [
        yaml.safe_load((stage_root / filename).read_text(encoding="utf-8"))
        for filename in sorted(files)
    ]
    assert {document["stage_id"] for document in documents} == EXPECTED_STAGE_IDS
    for document in documents:
        assert document["schema_version"] == "1.0.0"
        assert document["non_scoring"] is True
        assert document["commands"]
        assert document["expected_contracts"]
        assert document["cleanup"]
        assert document["limitations"]
        assert document["provenance"]
        assert all(
            not step["automated"] or step["eligible_for_automation"]
            for section in ("commands", "cleanup")
            for step in document[section]
        )
        for artifact in document["artifacts"]:
            path = artifact["path"]
            assert not path.startswith("/")
            assert "\\" not in path
            assert ".." not in path.split("/")
            assert len(artifact["sha256"]) == 64
    eligible = sum(
        step["eligible_for_automation"]
        for document in documents
        for section in ("commands", "cleanup")
        for step in document[section]
    )
    automated = sum(
        step["eligible_for_automation"] and step["automated"]
        for document in documents
        for section in ("commands", "cleanup")
        for step in document[section]
    )
    assert eligible > 0
    assert automated <= eligible
    assert automated * 100 >= eligible * 95


def test_ai_ready_manifest_has_governed_publication_contract() -> None:
    document = yaml.safe_load(
        (ROOT / "demo" / "manifests" / "ai-ready-customer-product.v1.yaml").read_text(
            encoding="utf-8"
        )
    )
    assert document["owner"]["name"]
    assert document["contract"]["schema"]
    assert document["service_levels"]["quality"]
    assert document["service_levels"]["freshness"]
    assert document["access"]["classification"] == "synthetic-pii-derived"
    assert document["access"]["policy_path"] == "governance/policy/access-policy.yaml"
    assert document["lineage"]["sources"] == ["accepted_orders", "stg_customers"]
    assert document["reproduction"]
    assert document["limitations"]
    assert document["non_scoring"] is True
    assert document["artifact_path"] == (
        "demo/evidence/current/ai-ready-customer-product.csv"
    )


def test_policy_cli_parser_accepts_no_sql_or_path_inputs() -> None:
    module = _load_module(
        ROOT / "governance" / "policy" / "export_authorized_dataset.py",
        "phase6_policy_export",
    )
    parser = module.build_parser()
    assert isinstance(parser, argparse.ArgumentParser)
    with pytest.raises(SystemExit):
        parser.parse_args(
            [
                "--role-id",
                "demo-ai-consumer",
                "--asset-id",
                "ai-ready-customer-product",
                "--sql",
                "select * from raw.customers",
            ]
        )
    with pytest.raises(SystemExit):
        parser.parse_args(
            [
                "--role-id",
                "demo-ai-consumer",
                "--asset-id",
                "ai-ready-customer-product",
                "--output-path",
                "/tmp/bypass.csv",
            ]
        )
    assert {action.dest for action in parser._actions} == {
        "help",
        "role_id",
        "asset_id",
    }


def test_policy_export_rejects_symlinked_fixed_output_root(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    module = _load_module(
        ROOT / "governance" / "policy" / "export_authorized_dataset.py",
        "phase6_policy_symlink",
    )
    repository = tmp_path / "repository"
    (repository / "demo").mkdir(parents=True)
    outside = tmp_path / "outside"
    outside.mkdir()
    (repository / "demo" / "evidence").symlink_to(outside, target_is_directory=True)
    monkeypatch.setattr(module, "REPO_ROOT", repository)
    monkeypatch.setattr(
        module,
        "OUTPUT_ROOT",
        repository / "demo" / "evidence" / "current",
    )

    with pytest.raises(module.PolicyError, match="symbolic link"):
        module._prepare_output_root()


def test_lakekeeper_bootstrap_is_idempotent_before_warehouse_creation(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setitem(sys.modules, "duckdb", Mock())
    module = _load_module(
        ROOT / "lake" / "publish_iceberg.py",
        "phase6_lake_publish",
    )
    responses = [
        nullcontext(
            Mock(
                read=lambda: json.dumps(
                    {"bootstrapped": False, "default-project-id": None}
                ).encode()
            )
        ),
        nullcontext(Mock(read=lambda: b"")),
        nullcontext(
            Mock(
                read=lambda: json.dumps(
                    {
                        "bootstrapped": True,
                        "default-project-id": module.NIL_PROJECT_ID,
                    }
                ).encode()
            )
        ),
    ]
    urlopen = Mock(side_effect=responses)
    monkeypatch.setattr(module.urllib.request, "urlopen", urlopen)

    module._ensure_bootstrapped("http://localhost:8181")

    bootstrap_request = urlopen.call_args_list[1].args[0]
    assert bootstrap_request.full_url.endswith("/management/v1/bootstrap")
    assert bootstrap_request.method == "POST"
    assert json.loads(bootstrap_request.data) == {"accept-terms-of-use": True}
    assert urlopen.call_count == 3


def test_lakekeeper_bootstrap_rejects_missing_default_project(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setitem(sys.modules, "duckdb", Mock())
    module = _load_module(
        ROOT / "lake" / "publish_iceberg.py",
        "phase6_lake_publish_missing_project",
    )
    urlopen = Mock(
        return_value=nullcontext(
            Mock(
                read=lambda: json.dumps(
                    {"bootstrapped": True, "default-project-id": None}
                ).encode()
            )
        )
    )
    monkeypatch.setattr(module.urllib.request, "urlopen", urlopen)

    with pytest.raises(RuntimeError, match="required local default project"):
        module._ensure_bootstrapped("http://localhost:8181")

    assert urlopen.call_count == 1


def test_lakekeeper_bootstrap_accepts_a_concurrent_successful_bootstrap(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setitem(sys.modules, "duckdb", Mock())
    module = _load_module(
        ROOT / "lake" / "publish_iceberg.py",
        "phase6_lake_publish_concurrent_bootstrap",
    )
    responses = [
        nullcontext(
            Mock(
                read=lambda: json.dumps(
                    {"bootstrapped": False, "default-project-id": None}
                ).encode()
            )
        ),
        module.urllib.error.HTTPError(
            "http://localhost:8181/management/v1/bootstrap",
            409,
            "Conflict",
            {},
            None,
        ),
        nullcontext(
            Mock(
                read=lambda: json.dumps(
                    {
                        "bootstrapped": True,
                        "default-project-id": module.NIL_PROJECT_ID,
                    }
                ).encode()
            )
        ),
    ]
    urlopen = Mock(side_effect=responses)
    monkeypatch.setattr(module.urllib.request, "urlopen", urlopen)

    module._ensure_bootstrapped("http://localhost:8181")

    assert urlopen.call_count == 3


def test_airflow_preflight_does_not_teardown_a_profile_it_did_not_start(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    module = _load_module(
        ROOT / "demo" / "verify_airflow.py",
        "phase6_airflow_preflight",
    )
    run = Mock(return_value=Mock(returncode=0, stdout="retail-airflow\n", stderr=""))
    monkeypatch.setattr(module, "_run", run)

    with pytest.raises(module.AirflowVerificationError, match="already running"):
        module.main()

    run.assert_called_once()
    command = run.call_args.args[0]
    assert command[:2] == ["docker", "ps"]
    assert f"name={module.CONTAINER}" in command


def test_demo_manifest_mutation_cannot_change_assessment_truth(tmp_path: Path) -> None:
    framework = load_framework("1.0.0")
    answers = {
        "schema_version": "1.0.0",
        "engagement_id": "demo-manifest-isolation",
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
    manifest_path = tmp_path / "demo" / "manifests" / "stages" / "ingestion.yaml"
    manifest_path.parent.mkdir(parents=True)
    manifest_path.write_bytes(
        (ROOT / "demo" / "manifests" / "stages" / "ingestion.yaml").read_bytes()
    )
    available_demo = load_demo_catalog(repository_root=tmp_path)
    baseline = _canonical_engine_projection(evaluate_assessment(answers, framework))
    manifest_path.unlink()
    unavailable_demo = load_demo_catalog(repository_root=tmp_path)
    after = _canonical_engine_projection(evaluate_assessment(answers, framework))

    assert after == baseline
    available_document = available_demo.model_dump(mode="json")
    unavailable_document = unavailable_demo.model_dump(mode="json")
    available_statuses = {
        artifact["path"]: artifact["status"]
        for stage in available_document["stages"]
        for artifact in stage["artifacts"]
    }
    unavailable_statuses = {
        artifact["path"]: artifact["status"]
        for stage in unavailable_document["stages"]
        for artifact in stage["artifacts"]
    }
    assert available_statuses["demo/manifests/stages/ingestion.yaml"] == "available"
    assert unavailable_statuses["demo/manifests/stages/ingestion.yaml"] == "unavailable"
    for stage in available_document["stages"]:
        for artifact in stage["artifacts"]:
            artifact["status"] = "unavailable"
    assert available_document == unavailable_document
