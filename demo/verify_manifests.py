#!/usr/bin/env python3
"""Validate Phase 6 demo contracts, manifests, and current core evidence."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import re
from pathlib import Path
from typing import Any

import duckdb
import yaml
from jsonschema import Draft202012Validator

REPO_ROOT = Path(__file__).resolve().parents[1]
STAGE_ROOT = REPO_ROOT / "demo" / "manifests" / "stages"
DATASET_MANIFEST_PATH = (
    REPO_ROOT / "demo" / "manifests" / "ai-ready-customer-product.v1.yaml"
)
STAGE_SCHEMA_PATH = REPO_ROOT / "demo" / "contracts" / "demo-stage-manifest-v1.schema.json"
DATASET_SCHEMA_PATH = (
    REPO_ROOT / "demo" / "contracts" / "ai-ready-dataset-manifest-v1.schema.json"
)
WAREHOUSE_PATH = REPO_ROOT / "warehouse" / "retail.duckdb"
CURRENT_EVIDENCE = REPO_ROOT / "demo" / "evidence" / "current"
DEMO_GUIDE_PATH = (
    REPO_ROOT
    / "assessment"
    / "src"
    / "assessment"
    / "content"
    / "demo"
    / "1.0.0"
    / "demo-guide.yaml"
)
CURRENT_PROOF_REFERENCE = "docs/verification/GH-38-phase-6-evidence.md"
EXPECTED_STAGE_FILES = {
    "ingestion.yaml": "DEMO-INGESTION",
    "quality-quarantine.yaml": "DEMO-QUALITY-QUARANTINE",
    "transformation.yaml": "DEMO-TRANSFORMATION",
    "metadata.yaml": "DEMO-METADATA",
    "lineage.yaml": "DEMO-LINEAGE",
    "governance.yaml": "DEMO-GOVERNANCE",
    "access-control.yaml": "DEMO-POLICY-ACCESS",
    "serving.yaml": "DEMO-SERVING",
    "ai-ready-publication.yaml": "DEMO-AI-READY-PUBLICATION",
}
PHASE6_STAGE_FIELDS = {
    "schema_version",
    "demo_content_version",
    "stage_id",
    "status",
    "artifacts",
    "commands",
    "expected_contracts",
    "cleanup",
    "limitations",
    "provenance",
    "non_scoring",
}
PHASE6_DATASET_FIELDS = {
    "schema_version",
    "dataset_id",
    "dataset_version",
    "source_stage_ids",
    "artifact_path",
    "sha256",
    "row_count",
    "owner",
    "contract",
    "service_levels",
    "access",
    "lineage",
    "reproduction",
    "source_checksums",
    "limitations",
    "synthetic_data",
    "non_scoring",
}
EXPECTED_SAFE_COLUMNS = (
    "order_key",
    "customer_key",
    "email_pseudonym",
    "loyalty_tier",
    "is_active",
    "order_date",
    "channel",
    "accepted_order_status",
    "order_total",
)
FORBIDDEN_CONTENT = re.compile(
    r"(?:/Users/|/home/|[A-Za-z]:\\\\|file://|s3://|aws_access_key|"
    r"terraform\s+(?:apply|destroy)|docker\s+compose\s+down\s+-v)",
    re.IGNORECASE,
)


class ManifestError(RuntimeError):
    """Raised for invalid or dishonest demo evidence."""


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--contract-only",
        action="store_true",
        help="Validate tracked contracts and references without generated artifacts.",
    )
    return parser


def _load_yaml(path: Path) -> dict[str, Any]:
    try:
        document = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, yaml.YAMLError) as error:
        raise ManifestError(f"{path.relative_to(REPO_ROOT)} is unavailable or invalid") from error
    if not isinstance(document, dict):
        raise ManifestError(f"{path.relative_to(REPO_ROOT)} must contain a mapping")
    return document


def _load_json(path: Path) -> dict[str, Any]:
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise ManifestError(f"{path.relative_to(REPO_ROOT)} is unavailable or invalid") from error
    if not isinstance(document, dict):
        raise ManifestError(f"{path.relative_to(REPO_ROOT)} must contain an object")
    return document


def _validate_schema(document: dict[str, Any], schema: dict[str, Any], label: str) -> None:
    errors = sorted(
        Draft202012Validator(schema).iter_errors(document),
        key=lambda item: tuple(str(part) for part in item.absolute_path),
    )
    if errors:
        details = "; ".join(
            f"{'/'.join(str(part) for part in error.absolute_path) or '<root>'}: "
            f"{error.message}"
            for error in errors
        )
        raise ManifestError(f"{label}: {details}")


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _safe_relative_path(value: str) -> Path:
    if (
        not value
        or value.startswith("/")
        or "\\" in value
        or "\x00" in value
        or any(part in {"", ".", ".."} for part in value.split("/"))
    ):
        raise ManifestError(f"unsafe repository-relative path: {value!r}")
    candidate = REPO_ROOT.joinpath(*value.split("/"))
    if candidate.resolve(strict=False).parent != REPO_ROOT.resolve() and (
        REPO_ROOT.resolve() not in candidate.resolve(strict=False).parents
    ):
        raise ManifestError(f"path escapes repository root: {value!r}")
    return candidate


def _walk_strings(value: object) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, dict):
        return [
            item
            for nested in value.values()
            for item in _walk_strings(nested)
        ]
    if isinstance(value, list):
        return [item for nested in value for item in _walk_strings(nested)]
    return []


def _validate_artifact(artifact: dict[str, Any], *, contract_only: bool) -> None:
    path = _safe_relative_path(str(artifact["path"]))
    origin = artifact["origin"]
    availability = artifact["availability"]
    if origin == "tracked":
        if not path.is_file():
            raise ManifestError(f"tracked artifact is missing: {artifact['path']}")
        if _digest(path) != artifact["sha256"]:
            raise ManifestError(f"tracked artifact checksum mismatch: {artifact['path']}")
    elif not contract_only and availability == "current":
        if not path.is_file():
            raise ManifestError(f"current generated artifact is missing: {artifact['path']}")
        if _digest(path) != artifact["sha256"]:
            raise ManifestError(f"generated artifact checksum mismatch: {artifact['path']}")


def _automation_counts(stages: list[dict[str, Any]]) -> tuple[int, int]:
    steps = [
        step
        for stage in stages
        for section in ("commands", "cleanup")
        for step in stage[section]
    ]
    eligible = sum(step["eligible_for_automation"] for step in steps)
    automated = sum(
        step["eligible_for_automation"] and step["automated"] for step in steps
    )
    return automated, eligible


def validate_contracts(*, contract_only: bool) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    stage_schema = _load_json(STAGE_SCHEMA_PATH)
    dataset_schema = _load_json(DATASET_SCHEMA_PATH)
    Draft202012Validator.check_schema(stage_schema)
    Draft202012Validator.check_schema(dataset_schema)
    public_root = REPO_ROOT / "assessment" / "src" / "assessment" / "public_schemas"
    if STAGE_SCHEMA_PATH.read_bytes() != (
        public_root / STAGE_SCHEMA_PATH.name
    ).read_bytes():
        raise ManifestError("demo and packaged stage schema authorities differ")
    if DATASET_SCHEMA_PATH.read_bytes() != (
        public_root / DATASET_SCHEMA_PATH.name
    ).read_bytes():
        raise ManifestError("demo and packaged dataset schema authorities differ")
    actual_files = {path.name for path in STAGE_ROOT.glob("*.yaml")}
    if actual_files != set(EXPECTED_STAGE_FILES):
        raise ManifestError("exact nine-stage manifest file inventory is required")
    stages: list[dict[str, Any]] = []
    for filename, stage_id in EXPECTED_STAGE_FILES.items():
        path = STAGE_ROOT / filename
        document = _load_yaml(path)
        _validate_schema(document, stage_schema, path.relative_to(REPO_ROOT).as_posix())
        if set(document) != PHASE6_STAGE_FIELDS:
            raise ManifestError(f"{filename}: complete Phase 6 fields are required")
        if document["stage_id"] != stage_id:
            raise ManifestError(f"{filename}: stage identity differs from Phase 5")
        if document["non_scoring"] is not True:
            raise ManifestError(f"{filename}: demo evidence must be non-scoring")
        if any(
            step["automated"] and not step["eligible_for_automation"]
            for section in ("commands", "cleanup")
            for step in document[section]
        ):
            raise ManifestError(f"{filename}: ineligible step is declared automated")
        if document["provenance"]["input_sha"] != (
            "7687a666cce3f533d4adac542ada34037b91ed8c"
        ):
            raise ManifestError(f"{filename}: immutable input SHA is incorrect")
        if stage_id == "DEMO-METADATA" and (
            document["provenance"]["current_execution"] != "unexecuted"
            or document["status"] != "historical"
        ):
            raise ManifestError("current OpenMetadata evidence must remain visibly unexecuted")
        if stage_id != "DEMO-METADATA" and (
            document["status"] != "executed"
            or document["provenance"]["evidence_kind"] != "current"
            or document["provenance"]["current_execution"] != "executed"
            or CURRENT_PROOF_REFERENCE not in document["provenance"]["references"]
        ):
            raise ManifestError(
                f"{filename}: current execution must reference the Phase 6 proof record"
            )
        for reference in document["provenance"]["references"]:
            if not _safe_relative_path(reference).is_file():
                raise ManifestError(f"{filename}: provenance reference is unavailable")
        for artifact in document["artifacts"]:
            _validate_artifact(artifact, contract_only=contract_only)
        if FORBIDDEN_CONTENT.search("\n".join(_walk_strings(document))):
            raise ManifestError(f"{filename}: forbidden path, secret, cloud, or destructive action")
        stages.append(document)
    automated, eligible = _automation_counts(stages)
    guide = _load_yaml(DEMO_GUIDE_PATH)
    if (
        guide.get("automation_eligible_steps") != eligible
        or guide.get("automation_automated_steps") != automated
    ):
        raise ManifestError(
            "Demo Guide automation numerator/denominator differ from manifest rows"
        )
    if eligible == 0 or automated * 100 < eligible * 95:
        raise ManifestError(
            f"eligible automation below 95%: {automated}/{eligible}"
        )
    dataset = _load_yaml(DATASET_MANIFEST_PATH)
    _validate_schema(
        dataset,
        dataset_schema,
        DATASET_MANIFEST_PATH.relative_to(REPO_ROOT).as_posix(),
    )
    if set(dataset) != PHASE6_DATASET_FIELDS:
        raise ManifestError("dataset manifest: complete Phase 6 fields are required")
    if set(dataset["source_stage_ids"]) - set(EXPECTED_STAGE_FILES.values()):
        raise ManifestError("dataset manifest contains an unknown stage reference")
    if dataset["non_scoring"] is not True or dataset["synthetic_data"] is not True:
        raise ManifestError("dataset must be synthetic and non-scoring")
    if dataset["access"]["policy_path"] != "governance/policy/access-policy.yaml":
        raise ManifestError("dataset policy reference differs from the fixed boundary")
    if dataset["lineage"]["sources"] != ["accepted_orders", "stg_customers"]:
        raise ManifestError("dataset lineage sources differ from the accepted design")
    for artifact in dataset["source_checksums"]:
        _validate_artifact(artifact, contract_only=contract_only)
    if FORBIDDEN_CONTENT.search("\n".join(_walk_strings(dataset))):
        raise ManifestError("dataset manifest contains forbidden local, cloud, or destructive content")
    canonical = _load_json(REPO_ROOT / "lake" / "curated_assets.json")
    assets = canonical.get("assets")
    if not isinstance(assets, list) or len(assets) != 11:
        raise ManifestError("canonical legacy mart inventory must remain exactly eleven")
    if any(item.get("name") == "ai_ready_customer_product" for item in assets):
        raise ManifestError("AI-ready product must remain outside the canonical mart inventory")
    compose = _load_yaml(REPO_ROOT / "docker-compose.yml")
    services = compose.get("services", {})
    if (
        services.get("openmetadata-search", {}).get("mem_limit") != "1g"
        or services.get("openmetadata-server", {}).get("mem_limit") != "2g"
    ):
        raise ManifestError("OpenMetadata search/server limits must remain 1g/2g")
    return stages, dataset


def validate_current_data(dataset: dict[str, Any]) -> dict[str, Any]:
    if not WAREHOUSE_PATH.is_file():
        raise ManifestError("warehouse is unavailable; run the core pipeline first")
    connection = duckdb.connect(str(WAREHOUSE_PATH), read_only=True)
    try:
        staging = connection.execute(
            "select count(*) from main_staging.stg_orders"
        ).fetchone()[0]
        accepted = connection.execute(
            "select count(*) from main_curated.accepted_orders"
        ).fetchone()[0]
        quarantined = connection.execute(
            "select count(*) from main_quarantine.quarantine_orders"
        ).fetchone()[0]
        overlap = connection.execute(
            "select count(*) from main_curated.accepted_orders a "
            "join main_quarantine.quarantine_orders q using (order_id)"
        ).fetchone()[0]
        leaked = connection.execute(
            "select count(*) from main_quarantine.quarantine_orders q "
            "join main_products.ai_ready_customer_product p "
            "on p.order_key = 'order_' || substr("
            "sha256(cast(q.order_id as varchar) || ':ai-ready-order:v1'), 1, 24)"
        ).fetchone()[0]
        product_rows = connection.execute(
            "select count(*) from main_products.ai_ready_customer_product"
        ).fetchone()[0]
        mart_count = connection.execute(
            "select count(*) from information_schema.tables "
            "where table_schema = 'main_marts' and table_name like 'mart_%'"
        ).fetchone()[0]
    finally:
        connection.close()
    if quarantined <= 0 or overlap != 0 or staging != accepted + quarantined:
        raise ManifestError("accepted/quarantine partition invariants failed")
    if leaked != 0 or product_rows != accepted:
        raise ManifestError("quarantined-key exclusion or governed row count failed")
    if mart_count != 11:
        raise ManifestError("warehouse canonical mart count differs from eleven")
    artifact_path = _safe_relative_path(dataset["artifact_path"])
    if not artifact_path.is_file():
        raise ManifestError("governed dataset artifact is unavailable")
    if _digest(artifact_path) != dataset["sha256"]:
        raise ManifestError("governed dataset checksum differs from its manifest")
    with artifact_path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if not rows or tuple(rows[0]) != EXPECTED_SAFE_COLUMNS:
        raise ManifestError("governed dataset schema is empty or unexpected")
    if len(rows) != dataset["row_count"] or len(rows) != accepted:
        raise ManifestError("governed dataset row count differs from its manifest")
    if any(
        forbidden in row
        for row in rows
        for forbidden in ("email", "first_name", "last_name", "customer_id", "order_id")
    ):
        raise ManifestError("governed dataset exposes a prohibited raw field")
    return {
        "staging_orders": staging,
        "accepted_orders": accepted,
        "quarantine_orders": quarantined,
        "product_rows": product_rows,
        "canonical_marts": mart_count,
        "partition_complete": True,
        "quarantine_excluded": True,
        "raw_email_absent": True,
    }


def _write_current_evidence(document: dict[str, Any]) -> None:
    CURRENT_EVIDENCE.mkdir(parents=True, exist_ok=True)
    path = CURRENT_EVIDENCE / "demo-verification.json"
    temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    try:
        with temporary.open("w", encoding="utf-8") as handle:
            json.dump(document, handle, sort_keys=True, separators=(",", ":"))
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    stages, dataset = validate_contracts(contract_only=args.contract_only)
    automated, eligible = _automation_counts(stages)
    if args.contract_only:
        print(
            "demo contracts passed: "
            f"{len(stages)} stages, automation {automated}/{eligible} "
            f"({automated * 100 // eligible}%), canonical marts 11"
        )
        return 0
    data = validate_current_data(dataset)
    evidence = {
        "schema_version": "1.0.0",
        "manifest_evidence": {
            "stage_manifests": len(stages),
            "automation_numerator": automated,
            "automation_denominator": eligible,
            "automation_percent": automated * 100 // eligible,
            "ai_ready_manifest_valid": True,
        },
        "data_evidence": data,
        "non_scoring": True,
    }
    _write_current_evidence(evidence)
    print(
        "demo verification passed: "
        f"quarantine={data['quarantine_orders']}, accepted={data['accepted_orders']}, "
        f"automation={automated}/{eligible}, canonical_marts=11"
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ManifestError as error:
        print(f"demo verification failed: {error}", file=__import__("sys").stderr)
        raise SystemExit(1) from error
