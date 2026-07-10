"""Batch pipeline DAG: seed -> load_raw -> dbt_run -> dbt_test (+ optional publish_iceberg).

Every task is a PythonOperator calling a shared callable from
orchestration/airflow/callables/pipeline.py (plan decision: Airflow task style
= PythonOperator). Tasks are sequenced so only one process writes the DuckDB
file at a time (single-writer discipline, plan risk R2).
"""
from __future__ import annotations

import os
import sys
from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator

sys.path.insert(0, "/opt/airflow")
from callables import pipeline  # noqa: E402

LAKE_PROFILE_ENABLED = os.environ.get("LAKE_PROFILE_ENABLED", "false").lower() == "true"

with DAG(
    dag_id="retail_batch_pipeline",
    description="Synthetic retail data: seed -> load -> dbt run -> dbt test (+ optional Iceberg publish)",
    schedule="@daily",
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["retail", "batch"],
) as dag:
    seed = PythonOperator(
        task_id="seed",
        python_callable=pipeline.seed,
        op_kwargs={
            "scale": os.environ.get("SCALE", "small"),
            "seed": int(os.environ.get("SEED", "42")),
        },
    )

    load_raw = PythonOperator(task_id="load_raw", python_callable=pipeline.load_raw)

    dbt_run = PythonOperator(task_id="dbt_run", python_callable=pipeline.dbt_run)

    dbt_test = PythonOperator(task_id="dbt_test", python_callable=pipeline.dbt_test)

    seed >> load_raw >> dbt_run >> dbt_test

    if LAKE_PROFILE_ENABLED:
        publish_iceberg = PythonOperator(
            task_id="publish_iceberg", python_callable=pipeline.publish_iceberg
        )
        dbt_test >> publish_iceberg
