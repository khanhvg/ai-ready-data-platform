#!/usr/bin/env python3
"""Export DuckDB marts to a read-only Parquet snapshot for Rill.

Rill Developer ingests into its own embedded DuckDB; attaching the shared
pipeline warehouse/retail.duckdb directly is documented as dev/local-testing
only and risks single-writer lock contention with Airflow/dbt (plan risk R2).
The default, supported serving path is this exported Parquet snapshot, which
Rill reads as its source (serving/rill/).
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import duckdb

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DUCKDB_PATH = REPO_ROOT / "warehouse" / "retail.duckdb"
DEFAULT_EXPORT_DIR = REPO_ROOT / "serving" / "export"
CURATED_ASSETS_PATH = REPO_ROOT / "lake" / "curated_assets.json"


def load_marts(curated_assets_path: Path = CURATED_ASSETS_PATH) -> list[tuple[str, str]]:
    """Load the shared curated-asset list so the export, Rill explore, and
    Iceberg asset sets stay a single source of truth (no drift)."""
    assets = json.loads(curated_assets_path.read_text())["assets"]
    return [(asset["name"], asset["schema"]) for asset in assets]


def export_marts(duckdb_path: Path = DEFAULT_DUCKDB_PATH, export_dir: Path = DEFAULT_EXPORT_DIR) -> dict[str, int]:
    export_dir.mkdir(parents=True, exist_ok=True)
    row_counts: dict[str, int] = {}
    con = duckdb.connect(str(duckdb_path), read_only=True)
    try:
        for mart, schema in load_marts():
            out_path = export_dir / f"{mart}.parquet"
            con.execute(
                f"COPY (SELECT * FROM {schema}.{mart}) TO '{out_path}' (FORMAT parquet)"
            )
            row_counts[mart] = con.execute(f"SELECT count(*) FROM {schema}.{mart}").fetchone()[0]
    finally:
        con.close()
    return row_counts


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--duckdb-path", type=Path, default=DEFAULT_DUCKDB_PATH)
    parser.add_argument("--export-dir", type=Path, default=DEFAULT_EXPORT_DIR)
    args = parser.parse_args()

    row_counts = export_marts(args.duckdb_path, args.export_dir)
    print(f"Exported marts snapshot to {args.export_dir}")
    for mart, count in row_counts.items():
        print(f"  {mart}.parquet: {count} rows")


if __name__ == "__main__":
    main()
