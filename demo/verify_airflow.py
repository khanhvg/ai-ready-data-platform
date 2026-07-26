#!/usr/bin/env python3
"""Run and verify the default Airflow DAG, always tearing profiles down."""

from __future__ import annotations

import datetime as dt
import json
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
EVIDENCE_PATH = REPO_ROOT / "demo" / "evidence" / "current" / "airflow-run.json"
CONTAINER = "retail-airflow"
DAG_ID = "retail_batch_pipeline"
EXPECTED_TASKS = {
    "generate.seed",
    "load.load_raw",
    "load.health_check",
    "transform.dbt_build",
    "transform.dbt_docs_generate",
    "serve.export_marts_snapshot",
}
TERMINAL_FAILURES = {
    "failed",
    "upstream_failed",
    "removed",
}


class AirflowVerificationError(RuntimeError):
    """Raised when the bounded Airflow proof does not reach terminal success."""


def _run(
    command: list[str],
    *,
    check: bool = True,
    timeout: int = 120,
) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        command,
        cwd=REPO_ROOT,
        env={
            "PATH": os.environ.get("PATH", ""),
            "SCALE": "small",
            "SEED": "42",
            "LAKE_PROFILE_ENABLED": "false",
        },
        text=True,
        capture_output=True,
        check=False,
        timeout=timeout,
    )
    if check and result.returncode != 0:
        raise AirflowVerificationError(
            f"{' '.join(command)} failed ({result.returncode}): "
            f"{result.stderr.strip() or result.stdout.strip()}"
        )
    return result


def _docker_exec(*arguments: str, timeout: int = 120) -> subprocess.CompletedProcess[str]:
    return _run(
        ["docker", "compose", "exec", "-T", "airflow", "airflow", *arguments],
        timeout=timeout,
    )


def _json_output(result: subprocess.CompletedProcess[str], context: str) -> Any:
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as error:
        raise AirflowVerificationError(
            f"{context} did not return JSON: {result.stdout.strip()}"
        ) from error


def _assert_no_other_heavy_profile() -> None:
    result = _run(
        [
            "docker",
            "ps",
            "--filter",
            "name=retail-minio",
            "--filter",
            "name=retail-lakekeeper",
            "--filter",
            "name=retail-openmetadata",
            "--filter",
            f"name={CONTAINER}",
            "--format",
            "{{.Names}}",
        ]
    )
    if result.stdout.strip():
        raise AirflowVerificationError(
            "Airflow, lake, or governance is already running; "
            "use make down before Airflow proof"
        )


def _wait_healthy() -> None:
    deadline = time.monotonic() + 300
    while time.monotonic() < deadline:
        result = _run(
            [
                "docker",
                "inspect",
                CONTAINER,
                "--format",
                "{{.State.Health.Status}}",
            ],
            check=False,
        )
        if result.returncode == 0 and result.stdout.strip() == "healthy":
            return
        if result.returncode == 0 and result.stdout.strip() == "unhealthy":
            raise AirflowVerificationError("Airflow container became unhealthy")
        time.sleep(5)
    raise AirflowVerificationError("Airflow did not become healthy within 300 seconds")


def _write_evidence(document: dict[str, Any]) -> None:
    EVIDENCE_PATH.parent.mkdir(parents=True, exist_ok=True)
    temporary = EVIDENCE_PATH.with_name(f".{EVIDENCE_PATH.name}.{os.getpid()}.tmp")
    try:
        with temporary.open("w", encoding="utf-8") as handle:
            json.dump(document, handle, sort_keys=True, separators=(",", ":"))
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, EVIDENCE_PATH)
    finally:
        temporary.unlink(missing_ok=True)


def verify() -> dict[str, Any]:
    _run(["docker", "compose", "--profile", "orchestration", "up", "-d"], timeout=900)
    _wait_healthy()
    import_errors = _json_output(
        _docker_exec("dags", "list-import-errors", "--output", "json"),
        "Airflow import-error check",
    )
    if not isinstance(import_errors, list):
        raise AirflowVerificationError("Airflow import-error check returned a non-list")
    if import_errors:
        raise AirflowVerificationError(f"Airflow DAG import errors: {import_errors!r}")
    task_result = _docker_exec("tasks", "list", DAG_ID)
    task_ids = {
        line.strip()
        for line in task_result.stdout.splitlines()
        if line.strip()
    }
    if task_ids != EXPECTED_TASKS:
        raise AirflowVerificationError(
            f"default DAG tasks differ: expected {sorted(EXPECTED_TASKS)}, got {sorted(task_ids)}"
        )
    _docker_exec("dags", "unpause", DAG_ID)
    run_id = "phase6__" + dt.datetime.now(dt.UTC).strftime("%Y%m%dT%H%M%SZ")
    _docker_exec("dags", "trigger", "--run-id", run_id, DAG_ID)
    deadline = time.monotonic() + 600
    task_states: dict[str, str] = {}
    while time.monotonic() < deadline:
        state_rows = _json_output(
            _docker_exec(
                "tasks",
                "states-for-dag-run",
                DAG_ID,
                run_id,
                "--output",
                "json",
            ),
            "Airflow task-state poll",
        )
        if not isinstance(state_rows, list):
            raise AirflowVerificationError(
                f"Airflow task-state poll returned a non-list: {state_rows!r}"
            )
        task_states = {
            str(item.get("task_id")): str(item.get("state"))
            for item in state_rows
            if isinstance(item, dict)
        }
        failures = {
            task_id: state
            for task_id, state in task_states.items()
            if state in TERMINAL_FAILURES
        }
        if failures:
            raise AirflowVerificationError(f"Airflow task failure: {failures}")
        if set(task_states) == EXPECTED_TASKS and set(task_states.values()) == {"success"}:
            return {
                "schema_version": "1.0.0",
                "dag_id": DAG_ID,
                "run_id": run_id,
                "task_states": task_states,
                "import_errors": 0,
                "scale": "small",
                "seed": 42,
                "lake_profile_enabled": False,
            }
        time.sleep(5)
    raise AirflowVerificationError(
        f"Airflow run {run_id} did not reach terminal success: {task_states}"
    )


def main() -> int:
    _assert_no_other_heavy_profile()
    try:
        evidence = verify()
        _write_evidence(evidence)
        print(
            f"Airflow DAG verification passed: {evidence['run_id']} "
            f"({len(evidence['task_states'])} tasks)"
        )
        return 0
    finally:
        teardown = _run(["make", "down"], check=False, timeout=180)
        if teardown.returncode != 0:
            error = AirflowVerificationError(
                "Airflow teardown failed: "
                f"{teardown.stderr.strip() or teardown.stdout.strip()}"
            )
            if sys.exc_info()[0] is not None:
                print(str(error), file=sys.stderr)
            else:
                raise error


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (AirflowVerificationError, subprocess.TimeoutExpired) as error:
        print(f"Airflow verification failed: {error}", file=sys.stderr)
        raise SystemExit(1) from error
