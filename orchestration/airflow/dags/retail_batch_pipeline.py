"""Batch pipeline DAG: generate -> load -> transform -> serve (+ optional publish).

Authored exclusively with the Airflow 3 public TaskFlow API (`airflow.sdk`
`dag`/`task`/`task_group`) -- no legacy operator-based task construction and no
deprecated decorator-module imports (binding project decision, issue #3).
Every `@task` body is a one-line delegate into `orchestration/airflow/callables/pipeline.py`,
the same reusable entrypoints the `make` targets call, so no orchestration
logic is duplicated here. Task groups give each pipeline stage a visible
boundary in the Airflow UI: generate -> load -> transform -> serve, then an
optional publish stage gated by `LAKE_PROFILE_ENABLED`. Groups are chained
with `>>` (not XCom) so only one process writes the DuckDB file at a time
(single-writer discipline, plan risk R2).
"""
from __future__ import annotations

import os
import sys
from datetime import datetime

from airflow.sdk import dag, task, task_group

sys.path.insert(0, "/opt/airflow")

_TRUTHY = {"1", "true", "yes", "on"}
# Read at DAG parse time; changing it requires the Airflow container/scheduler
# to reparse the DAG (recreate the orchestration service with the new value),
# not just a re-trigger of an existing run.
LAKE_PROFILE_ENABLED = os.environ.get("LAKE_PROFILE_ENABLED", "false").strip().lower() in _TRUTHY


@dag(
    dag_id="retail_batch_pipeline",
    description="Synthetic retail data: generate -> load -> transform -> serve (+ optional Iceberg publish)",
    schedule="@daily",
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["retail", "batch"],
)
def retail_batch_pipeline():
    from callables import pipeline

    @task_group(group_id="generate")
    def generate():
        @task(task_id="seed")
        def seed():
            pipeline.seed(
                scale=os.environ.get("SCALE", "small"),
                seed=int(os.environ.get("SEED", "42")),
            )

        seed()

    @task_group(group_id="load")
    def load():
        @task(task_id="load_raw")
        def load_raw():
            pipeline.load_raw()

        @task(task_id="health_check")
        def health_check():
            pipeline.health_check()

        load_raw() >> health_check()

    @task_group(group_id="transform")
    def transform():
        @task(task_id="dbt_build")
        def dbt_build():
            pipeline.dbt_build()

        @task(task_id="dbt_docs_generate")
        def dbt_docs_generate():
            pipeline.dbt_docs_generate()

        dbt_build() >> dbt_docs_generate()

    @task_group(group_id="serve")
    def serve():
        @task(task_id="export_marts_snapshot")
        def export_marts_snapshot():
            pipeline.export_marts_snapshot()

        export_marts_snapshot()

    @task_group(group_id="publish")
    def publish():
        @task(task_id="publish_iceberg")
        def publish_iceberg():
            pipeline.publish_iceberg()

        @task(task_id="iceberg_read_back")
        def iceberg_read_back():
            pipeline.iceberg_read_back()

        publish_iceberg() >> iceberg_read_back()

    chain = generate() >> load() >> transform() >> serve()
    if LAKE_PROFILE_ENABLED:
        chain >> publish()


retail_batch_pipeline()
