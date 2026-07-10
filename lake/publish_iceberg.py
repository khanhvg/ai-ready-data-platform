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
import os
from pathlib import Path

import duckdb

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DUCKDB_PATH = REPO_ROOT / "warehouse" / "retail.duckdb"

MARTS = ["mart_daily_revenue", "mart_top_products", "mart_customer_cohorts"]


def _lakekeeper_env() -> dict[str, str]:
    return {
        "catalog_uri": os.environ.get("LAKEKEEPER_CATALOG_URI", "http://localhost:8181/catalog"),
        "catalog_name": os.environ.get("LAKEKEEPER_CATALOG_NAME", "retail"),
        "warehouse": os.environ.get("LAKEKEEPER_WAREHOUSE", "retail"),
        "s3_endpoint": os.environ.get("LAKE_S3_ENDPOINT", "http://localhost:9000"),
        "s3_access_key": os.environ.get("MINIO_ROOT_USER", "minioadmin"),
        "s3_secret_key": os.environ.get("MINIO_ROOT_PASSWORD", "minioadmin_local_only"),
    }


def publish(duckdb_path: Path = DEFAULT_DUCKDB_PATH) -> list[str]:
    cfg = _lakekeeper_env()
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
                ENDPOINT '{cfg['catalog_uri']}'
            )
            """
        )
        con.execute("CREATE SCHEMA IF NOT EXISTS lake.retail")

        for mart in MARTS:
            con.execute(
                f"CREATE OR REPLACE TABLE lake.retail.{mart} AS SELECT * FROM main_marts.{mart}"
            )
            published.append(mart)
    finally:
        con.close()

    return published


def read_back(duckdb_path: Path = DEFAULT_DUCKDB_PATH) -> dict[str, int]:
    """Write->read-back smoke test: re-attach and count rows in each published table."""
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
                ENDPOINT '{cfg['catalog_uri']}'
            )
            """
        )
        for mart in MARTS:
            counts[mart] = con.execute(f"SELECT count(*) FROM lake.retail.{mart}").fetchone()[0]
    finally:
        con.close()
    return counts


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--duckdb-path", type=Path, default=DEFAULT_DUCKDB_PATH)
    parser.add_argument("--skip-read-back", action="store_true")
    args = parser.parse_args()

    published = publish(args.duckdb_path)
    print(f"Published to Lakekeeper/MinIO: {', '.join(published)}")

    if not args.skip_read_back:
        counts = read_back(args.duckdb_path)
        print("Write->read-back smoke test:")
        for mart, count in counts.items():
            print(f"  lake.retail.{mart}: {count} rows")


if __name__ == "__main__":
    main()
