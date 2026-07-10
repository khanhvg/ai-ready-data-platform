"""Thin PythonOperator callables wrapping the same scripts `make` targets call.

Every function shells out to the identical entrypoint used by the Makefile
(data-generator/generate.py, ingestion/load_raw.py, dbt CLI, lake/publish_iceberg.py)
so the batch pipeline has a single source of truth whether it's driven by
Airflow or run directly on the host (plan decision: "no-Airflow demo path").
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


def dbt_run() -> None:
    _run(["dbt", "run"], cwd=DBT_PROJECT_DIR, extra_env={"DBT_PROFILES_DIR": str(DBT_PROJECT_DIR)})


def dbt_test() -> None:
    _run(["dbt", "test"], cwd=DBT_PROJECT_DIR, extra_env={"DBT_PROFILES_DIR": str(DBT_PROJECT_DIR)})


def export_marts_snapshot() -> None:
    _run([sys.executable, str(PROJECT_ROOT / "serving" / "export_marts_snapshot.py")])


def publish_iceberg() -> None:
    _run([sys.executable, str(PROJECT_ROOT / "lake" / "publish_iceberg.py")])
