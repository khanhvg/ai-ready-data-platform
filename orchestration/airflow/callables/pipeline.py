"""Thin delegate callables wrapping the same scripts `make` targets call.

Every function shells out to the identical entrypoint used by the Makefile
(data-generator/generate.py, ingestion/load_raw.py, dbt CLI, lake/publish_iceberg.py)
so the batch pipeline has a single source of truth whether it's driven by
Airflow TaskFlow tasks or run directly on the host (plan decision: "no-Airflow
demo path"). This module keeps zero top-level optional imports (no pyiceberg,
no MinIO client) so importing it never fails Airflow DAG parsing regardless of
which optional services/deps are present -- everything heavier runs in the
subprocess `_run` shells out to, not in this process.
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(os.environ.get("RETAIL_PROJECT_ROOT", "/opt/airflow/project"))
DBT_PROJECT_DIR = PROJECT_ROOT / "transform" / "dbt"


def _run(cmd: list[str], cwd: Path | None = None, extra_env: dict | None = None) -> str:
    env = {**os.environ, **(extra_env or {})}
    result = subprocess.run(
        cmd, cwd=str(cwd or PROJECT_ROOT), env=env, capture_output=True, text=True
    )
    print(result.stdout)
    if result.returncode != 0:
        print(result.stderr, file=sys.stderr)
        raise RuntimeError(f"Command failed ({result.returncode}): {' '.join(cmd)}\n{result.stderr}")
    return result.stdout


def seed(scale: str = "small", seed: int = 42) -> None:
    _run(
        [
            sys.executable,
            str(PROJECT_ROOT / "data-generator" / "generate.py"),
            "--profile",
            scale,
            "--seed",
            str(seed),
        ]
    )


def load_raw() -> None:
    _run([sys.executable, str(PROJECT_ROOT / "ingestion" / "load_raw.py")])


def health_check() -> None:
    """Assert the DuckDB file exists and the `raw` schema has tables, matching
    the check `make health` runs on the host."""
    import duckdb

    duckdb_path = Path(os.environ.get("DUCKDB_PATH", str(PROJECT_ROOT / "warehouse" / "retail.duckdb")))
    if not duckdb_path.is_absolute():
        duckdb_path = PROJECT_ROOT / duckdb_path
    assert duckdb_path.exists(), f"DuckDB file missing: {duckdb_path}"
    con = duckdb.connect(str(duckdb_path), read_only=True)
    try:
        tables = con.sql(
            "select table_schema, table_name from information_schema.tables where table_schema='raw'"
        ).fetchall()
    finally:
        con.close()
    assert tables, "raw schema has no tables -- run load_raw first"
    print(f"OK: {duckdb_path} opens read-only, raw schema has {len(tables)} tables")


def dbt_build() -> None:
    _run(["dbt", "build"], cwd=DBT_PROJECT_DIR, extra_env={"DBT_PROFILES_DIR": str(DBT_PROJECT_DIR)})


def dbt_docs_generate() -> None:
    _run(
        ["dbt", "docs", "generate"],
        cwd=DBT_PROJECT_DIR,
        extra_env={"DBT_PROFILES_DIR": str(DBT_PROJECT_DIR)},
    )


def export_marts_snapshot() -> None:
    _run([sys.executable, str(PROJECT_ROOT / "serving" / "export_marts_snapshot.py")])


def publish_iceberg() -> None:
    _run([sys.executable, str(PROJECT_ROOT / "lake" / "publish_iceberg.py"), "--skip-read-back"])


def iceberg_read_back() -> None:
    _run([sys.executable, str(PROJECT_ROOT / "lake" / "publish_iceberg.py"), "--read-back-only"])
