#!/usr/bin/env python3
"""Pure CuratedReleaseManifest/current-pointer contract; no publisher."""
from __future__ import annotations
import copy, hashlib, json, pathlib, re
from typing import Any
import jsonschema
import rfc8785

ROOT=pathlib.Path(__file__).resolve().parents[2]
SCHEMA_PATH=ROOT/"contracts/data/curated-release-manifest.schema.json"

ASSET_IDS = (
 "mart_daily_revenue", "mart_top_products", "mart_customer_cohorts", "mart_fulfillment_performance",
 "mart_returns_analysis", "mart_promotion_effectiveness", "mart_channel_geography", "mart_inventory_health",
 "mart_web_funnel_conversion", "mart_supplier_purchasing", "mart_data_quality",
)
class ReleaseError(ValueError): pass

def example_manifest() -> dict[str, Any]:
    common = {"releaseId":"release-small-42-v1", "dataRunId":"data-small-42-v1", "testedTreeSha":"0"*40,
              "lockSha256":"f41c727b39f99106f95b7937b2811e8d27db89d1d5106e9f1d9effd4403143d2",
              "contractSetId":"golden-contract-set-v1", "engineSnapshotId":"duckdb-1.5.4"}
    assets=[]
    for asset_id in ASSET_IDS:
        asset=copy.deepcopy(common); asset.update({"assetId":asset_id,
          "logicalFqn":f"retail_duckdb.retail.main_marts.{asset_id}",
          "physicalFqn":f"retail_iceberg.default.retail.{asset_id}",
          "schemaSha256":"1"*64,"contentSha256":"2"*64,"rowCount":0,
          "stagedLocator":f"curated/releases/release-small-42-v1/{asset_id}"}); assets.append(asset)
    return {"schemaVersion":"curated-release-manifest-v1", **common, "profile":"small", "seed":42, "assets":assets}

def validate_manifest(value: dict[str, Any]) -> None:
    assets=value.get("assets", [])
    if not isinstance(assets,list) or any(not isinstance(item,dict) for item in assets) or tuple(item.get("assetId") for item in assets) != ASSET_IDS:
        raise ReleaseError("CURATED_ASSET_SET_MISMATCH")
    schema=json.loads(SCHEMA_PATH.read_text())
    try: jsonschema.Draft202012Validator(schema).validate(value)
    except jsonschema.ValidationError as exc: raise ReleaseError("CURATED_MANIFEST_SCHEMA_INVALID") from exc
    for item in assets:
        for key in ("releaseId","dataRunId","testedTreeSha","lockSha256","contractSetId","engineSnapshotId"):
            if item.get(key) != value.get(key): raise ReleaseError("CURATED_MIXED_GENERATION")
        asset_id=item["assetId"]
        if item["logicalFqn"]!=f"retail_duckdb.retail.main_marts.{asset_id}" or item["physicalFqn"]!=f"retail_iceberg.default.retail.{asset_id}":
            raise ReleaseError("CURATED_ASSET_IDENTITY_INVALID")
        if item["stagedLocator"]!=f"curated/releases/{value['releaseId']}/{asset_id}":
            raise ReleaseError("CURATED_LOCATOR_INVALID")

def validate_pointer(pointer: dict[str, Any], manifests: dict[str, dict[str, Any]]) -> None:
    schema=json.loads(SCHEMA_PATH.read_text()); schema["$ref"]="#/$defs/CuratedReleaseCurrentPointerV1"
    try: jsonschema.Draft202012Validator(schema).validate(pointer)
    except jsonschema.ValidationError as exc: raise ReleaseError("CURATED_POINTER_INVALID") from exc
    current=pointer.get("currentReleaseId")
    if current not in manifests: raise ReleaseError("CURATED_POINTER_TARGET_INVALID")
    manifest=manifests[current]; validate_manifest(manifest)
    if manifest.get("releaseId")!=current or pointer.get("manifestSha256")!=hashlib.sha256(rfc8785.dumps(manifest)).hexdigest(): raise ReleaseError("CURATED_POINTER_DIGEST_INVALID")
    previous=pointer.get("previousReleaseId")
    if previous is not None:
        if previous not in manifests: raise ReleaseError("CURATED_ROLLBACK_TARGET_INVALID")
        previous_manifest=manifests[previous]; validate_manifest(previous_manifest)
        if previous_manifest.get("releaseId")!=previous: raise ReleaseError("CURATED_ROLLBACK_TARGET_INVALID")
