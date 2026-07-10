#!/usr/bin/env python3
"""Idempotent DuckDB loader: data/raw/*.csv -> raw.* landing tables.

Reads the CSV files written by data-generator/generate.py and loads them into
a `raw` schema in a single-file DuckDB warehouse using `read_csv`, matching
the table shapes documented in data-generator/schema.md. Each run truncates
and reloads every table, so reruns are safe and reproducible.

The loader opens the DuckDB connection, writes, and closes before returning,
so it never holds a lock while dbt/Rill read the same file (single-writer
discipline per the plan's R2 risk).
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import duckdb

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_RAW_DIR = REPO_ROOT / "data" / "raw"
DEFAULT_DUCKDB_PATH = REPO_ROOT / "warehouse" / "retail.duckdb"

# Table name -> CSV filename. Landing tables mirror the raw CSVs 1:1;
# typing/cleaning happens later in dbt staging models.
TABLES = {
    "regions": "regions.csv",
    "stores": "stores.csv",
    "product_categories": "product_categories.csv",
    "products": "products.csv",
    "customers": "customers.csv",
    "promotions": "promotions.csv",
    "suppliers": "suppliers.csv",
    "purchase_orders": "purchase_orders.csv",
    "purchase_order_items": "purchase_order_items.csv",
    "orders": "orders.csv",
    "order_items": "order_items.csv",
    "payments": "payments.csv",
    "inventory_movements": "inventory_movements.csv",
    "returns_refunds": "returns_refunds.csv",
    "reviews": "reviews.csv",
    "shipments": "shipments.csv",
    "web_sessions": "web_sessions.csv",
    "web_events": "web_events.csv",
}


def load_raw(raw_dir: Path = DEFAULT_RAW_DIR, duckdb_path: Path = DEFAULT_DUCKDB_PATH) -> dict[str, int]:
    """Load every CSV in raw_dir into raw.<table> inside duckdb_path.

    Returns a dict of table name -> row count loaded. Raises FileNotFoundError
    if a CSV listed in TABLES is missing (run `make seed` first).
    """
    duckdb_path.parent.mkdir(parents=True, exist_ok=True)

    missing = [csv for csv in TABLES.values() if not (raw_dir / csv).exists()]
    if missing:
        raise FileNotFoundError(
            f"Missing raw CSV(s) in {raw_dir}: {missing}. Run 'make seed' first."
        )

    row_counts: dict[str, int] = {}
    con = duckdb.connect(str(duckdb_path))
    try:
        con.execute("CREATE SCHEMA IF NOT EXISTS raw")
        for table, csv_name in TABLES.items():
            csv_path = raw_dir / csv_name
            con.execute(f"DROP TABLE IF EXISTS raw.{table}")
            con.execute(
                f"CREATE TABLE raw.{table} AS "
                f"SELECT * FROM read_csv(?, header=true, sample_size=-1)",
                [str(csv_path)],
            )
            row_counts[table] = con.execute(f"SELECT count(*) FROM raw.{table}").fetchone()[0]
    finally:
        con.close()

    return row_counts


def _expected_counts(raw_dir: Path) -> dict[str, int]:
    manifest_path = raw_dir / "manifest.json"
    if not manifest_path.exists():
        return {}
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    return {
        csv_name.removesuffix(".csv"): info["row_count"]
        for csv_name, info in manifest.get("tables", {}).items()
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--raw-dir", type=Path, default=DEFAULT_RAW_DIR)
    parser.add_argument("--duckdb-path", type=Path, default=DEFAULT_DUCKDB_PATH)
    args = parser.parse_args()

    row_counts = load_raw(args.raw_dir, args.duckdb_path)
    expected = _expected_counts(args.raw_dir)

    print(f"Loaded raw.* into {args.duckdb_path}")
    mismatches = []
    for table, count in row_counts.items():
        exp = expected.get(table)
        marker = "OK" if exp is None or exp == count else f"MISMATCH (expected {exp})"
        if exp is not None and exp != count:
            mismatches.append(table)
        print(f"  raw.{table}: {count} rows [{marker}]")

    if mismatches:
        raise SystemExit(
            f"Row count mismatch vs manifest.json for: {', '.join(mismatches)}"
        )


if __name__ == "__main__":
    main()
