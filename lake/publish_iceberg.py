#!/usr/bin/env python3
"""Publish curated marts to MinIO as Iceberg tables via the Lakekeeper REST catalog.

DuckDB's Iceberg writes require an attached Iceberg REST catalog -- a raw
MinIO/S3 path is not sufficient (plan risk R1). This script attaches
Lakekeeper, creates the retail namespace/tables if needed, and writes each
mart as an Iceberg table. Only runs meaningfully when the `lake` Docker
Compose profile is up (`make lake-up`).

This is a dedicated DuckDB-SQL export step (not a dbt materialization),
matching the plan's architecture: dbt-duckdb has no native Iceberg destination.
"""
from __future__ import annotations

import argparse
import json
import os
import urllib.error
import urllib.request
from pathlib import Path

import duckdb

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DUCKDB_PATH = REPO_ROOT / "warehouse" / "retail.duckdb"

# Resolved relative to this file (not sys.path/cwd) so `python lake/publish_iceberg.py`
# works standalone regardless of the invoking directory or whether `lake` is an
# importable package. Shared with serving/export_marts_snapshot.py and the
# OpenMetadata Iceberg ingestion YAML renderer to keep the curated-asset set
# from drifting between publish, export, and catalog ingestion.
CURATED_ASSETS_PATH = Path(__file__).resolve().parent / "curated_assets.json"
NIL_PROJECT_ID = "00000000-0000-0000-0000-000000000000"


def _load_curated_assets(path: Path = CURATED_ASSETS_PATH) -> list[dict[str, str]]:
    with path.open() as f:
        return json.load(f)["assets"]


CURATED_ASSETS = _load_curated_assets()


def _lakekeeper_env() -> dict[str, str]:
    return {
        "catalog_uri": os.environ.get("LAKEKEEPER_CATALOG_URI", "http://localhost:8181/catalog"),
        "catalog_name": os.environ.get("LAKEKEEPER_CATALOG_NAME", "retail"),
        "warehouse": os.environ.get("LAKEKEEPER_WAREHOUSE", "retail"),
        "s3_endpoint": os.environ.get("LAKE_S3_ENDPOINT", "http://localhost:9000"),
        # Lakekeeper (always a container) validates storage access itself when a
        # warehouse is created, so its storage-profile endpoint must be resolvable
        # from *inside* the `lake` Compose network -- the Docker Compose service
        # name, not the caller's own view of MinIO (which may be `localhost` from
        # the host or `minio` from another container). Kept separate from
        # `s3_endpoint`, which this script's own S3 secret uses for actual data
        # I/O (ACCESS_DELEGATION_MODE 'none' below) and does vary by caller.
        "lakekeeper_s3_endpoint": os.environ.get("LAKEKEEPER_STORAGE_ENDPOINT", "http://minio:9000"),
        "s3_bucket": os.environ.get("LAKE_S3_BUCKET", "retail-lake"),
        "s3_access_key": os.environ.get("MINIO_ROOT_USER", "minioadmin"),
        "s3_secret_key": os.environ.get("MINIO_ROOT_PASSWORD", "minioadmin_local_only"),
    }


def _management_api_base(catalog_uri: str) -> str:
    """Lakekeeper's warehouse management API lives alongside, not under, the Iceberg
    REST catalog path (catalog_uri is typically '<host>/catalog')."""
    return catalog_uri.rsplit("/catalog", 1)[0]


def _read_server_info(base: str) -> dict[str, object]:
    info_req = urllib.request.Request(f"{base}/management/v1/info")
    try:
        with urllib.request.urlopen(info_req, timeout=10) as response:
            return json.load(response)
    except urllib.error.URLError as exc:
        raise RuntimeError(
            f"Could not read Lakekeeper server status at {base}: {exc}. "
            "Is the `lake` profile up (`make lake-up`)?"
        ) from exc


def _assert_default_project(info: dict[str, object]) -> None:
    if (
        info.get("bootstrapped") is not True
        or info.get("default-project-id") != NIL_PROJECT_ID
    ):
        raise RuntimeError(
            "Lakekeeper bootstrap did not create the required local default project"
        )


def _ensure_bootstrapped(base: str) -> None:
    """Initialize a fresh local Lakekeeper server and its default project."""
    info = _read_server_info(base)
    if info.get("bootstrapped") is True:
        _assert_default_project(info)
        return

    payload = json.dumps({"accept-terms-of-use": True}).encode()
    bootstrap_req = urllib.request.Request(
        f"{base}/management/v1/bootstrap",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        urllib.request.urlopen(bootstrap_req, timeout=10)
    except urllib.error.HTTPError as exc:
        try:
            _assert_default_project(_read_server_info(base))
            return
        except RuntimeError:
            pass
        detail = exc.read().decode(errors="replace")
        raise RuntimeError(
            f"Failed to bootstrap the local Lakekeeper server: {exc.code} {detail}"
        ) from exc
    _assert_default_project(_read_server_info(base))


def _ensure_warehouse(cfg: dict[str, str]) -> None:
    """Create the Lakekeeper warehouse if it doesn't exist yet.

    Lakekeeper's Iceberg REST catalog protocol (what ATTACH speaks) does not
    auto-create warehouses -- they must exist via the separate management API
    first, or ATTACH fails with a 404 on the whole warehouse. This makes a fresh
    `make lake-up` + `make lake-publish` work without a manual bootstrap step.
    ACCESS_DELEGATION_MODE 'none' is used at ATTACH time (ATTACH mechanics above),
    so the storage profile's endpoint only needs to be reachable by Lakekeeper
    itself for its own S3 connectivity check; actual data reads/writes go through
    this script's own `lake_s3` secret instead.
    """
    base = _management_api_base(cfg["catalog_uri"])
    _ensure_bootstrapped(base)
    list_req = urllib.request.Request(f"{base}/management/v1/warehouse")
    try:
        with urllib.request.urlopen(list_req, timeout=10) as resp:
            warehouses = json.load(resp).get("warehouses", [])
    except urllib.error.URLError as exc:
        raise RuntimeError(
            f"Could not reach Lakekeeper management API at {base}: {exc}. "
            "Is the `lake` profile up (`make lake-up`)?"
        ) from exc

    if any(w["name"] == cfg["warehouse"] for w in warehouses):
        return

    payload = json.dumps(
        {
            "warehouse-name": cfg["warehouse"],
            "storage-profile": {
                "type": "s3",
                "bucket": cfg["s3_bucket"],
                "endpoint": cfg["lakekeeper_s3_endpoint"] + "/",
                "region": "local",
                "path-style-access": True,
                "flavor": "s3-compat",
                "sts-enabled": False,
            },
            "storage-credential": {
                "type": "s3",
                "credential-type": "access-key",
                "aws-access-key-id": cfg["s3_access_key"],
                "aws-secret-access-key": cfg["s3_secret_key"],
            },
        }
    ).encode()
    create_req = urllib.request.Request(
        f"{base}/management/v1/warehouse",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        urllib.request.urlopen(create_req, timeout=10)
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode(errors="replace")
        raise RuntimeError(
            f"Failed to create Lakekeeper warehouse '{cfg['warehouse']}': "
            f"{exc.code} {detail}"
        ) from exc


def publish(duckdb_path: Path = DEFAULT_DUCKDB_PATH) -> list[str]:
    cfg = _lakekeeper_env()
    _ensure_warehouse(cfg)
    con = duckdb.connect(str(duckdb_path), read_only=True)
    published = []
    try:
        con.execute("INSTALL iceberg")
        con.execute("LOAD iceberg")
        con.execute("INSTALL httpfs")
        con.execute("LOAD httpfs")

        con.execute(
            f"""
            CREATE SECRET IF NOT EXISTS lake_s3 (
                TYPE s3,
                ENDPOINT '{cfg['s3_endpoint'].removeprefix('http://').removeprefix('https://')}',
                KEY_ID '{cfg['s3_access_key']}',
                SECRET '{cfg['s3_secret_key']}',
                USE_SSL false,
                URL_STYLE 'path'
            )
            """
        )
        con.execute(
            f"""
            ATTACH '{cfg['warehouse']}' AS lake (
                TYPE iceberg,
                ENDPOINT '{cfg['catalog_uri']}',
                AUTHORIZATION_TYPE 'none',
                ACCESS_DELEGATION_MODE 'none',
                READ_ONLY false
            )
            """
        )
        con.execute("CREATE SCHEMA IF NOT EXISTS lake.retail")

        for asset in CURATED_ASSETS:
            name, schema = asset["name"], asset["schema"]
            # The DuckDB iceberg extension does not support CREATE OR REPLACE; drop
            # then create is the documented equivalent for re-publishing a table.
            con.execute(f"DROP TABLE IF EXISTS lake.retail.{name}")
            con.execute(f"CREATE TABLE lake.retail.{name} AS SELECT * FROM {schema}.{name}")
            published.append(name)
    finally:
        con.close()

    return published


def read_back(duckdb_path: Path = DEFAULT_DUCKDB_PATH) -> dict[str, int]:
    """Write->read-back smoke test: re-attach and count rows in each published table.

    Strict by design: raises if any curated asset is missing from the catalog or has
    a zero row count, since a silent gap here would surface downstream as a Rill
    explore or OpenMetadata table with no data, without a clear cause.
    """
    cfg = _lakekeeper_env()
    con = duckdb.connect(":memory:")
    counts: dict[str, int] = {}
    try:
        con.execute("INSTALL iceberg")
        con.execute("LOAD iceberg")
        con.execute("INSTALL httpfs")
        con.execute("LOAD httpfs")
        con.execute(
            f"""
            CREATE SECRET IF NOT EXISTS lake_s3 (
                TYPE s3,
                ENDPOINT '{cfg['s3_endpoint'].removeprefix('http://').removeprefix('https://')}',
                KEY_ID '{cfg['s3_access_key']}',
                SECRET '{cfg['s3_secret_key']}',
                USE_SSL false,
                URL_STYLE 'path'
            )
            """
        )
        con.execute(
            f"""
            ATTACH '{cfg['warehouse']}' AS lake (
                TYPE iceberg,
                ENDPOINT '{cfg['catalog_uri']}',
                AUTHORIZATION_TYPE 'none',
                ACCESS_DELEGATION_MODE 'none'
            )
            """
        )
        for asset in CURATED_ASSETS:
            name = asset["name"]
            try:
                count = con.execute(f"SELECT count(*) FROM lake.retail.{name}").fetchone()[0]
            except duckdb.Error as exc:
                raise RuntimeError(
                    f"Curated asset 'lake.retail.{name}' is missing from the Iceberg "
                    f"catalog (expected per curated_assets.json): {exc}"
                ) from exc
            if count == 0:
                raise RuntimeError(
                    f"Curated asset 'lake.retail.{name}' has 0 rows after publish; "
                    "expected every curated asset to be non-empty."
                )
            counts[name] = count
    finally:
        con.close()
    return counts


def _print_read_back_report(counts: dict[str, int]) -> None:
    print("Write->read-back smoke test:")
    for name, count in counts.items():
        print(f"  lake.retail.{name}: {count} rows")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--duckdb-path", type=Path, default=DEFAULT_DUCKDB_PATH)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--skip-read-back", action="store_true", help="Publish only, skip the read-back smoke test.")
    group.add_argument(
        "--read-back-only",
        action="store_true",
        help="Skip publish and only run the read-back smoke test against already-published assets "
        "(used by the Airflow iceberg_read_back task).",
    )
    args = parser.parse_args()

    if args.read_back_only:
        counts = read_back(args.duckdb_path)
        _print_read_back_report(counts)
        return

    published = publish(args.duckdb_path)
    print(f"Published to Lakekeeper/MinIO: {', '.join(published)}")

    if not args.skip_read_back:
        counts = read_back(args.duckdb_path)
        _print_read_back_report(counts)


if __name__ == "__main__":
    main()
