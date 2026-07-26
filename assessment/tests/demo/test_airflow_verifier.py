from __future__ import annotations

import ast
import importlib.util
import json
from pathlib import Path
from types import ModuleType
from unittest.mock import Mock

import pytest

ROOT = Path(__file__).resolve().parents[3]


def _load_verifier(name: str) -> ModuleType:
    path = ROOT / "demo" / "verify_airflow.py"
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _result(*, stdout: str = "", returncode: int = 0) -> Mock:
    return Mock(stdout=stdout, stderr="", returncode=returncode)


def _successful_task_rows(module: ModuleType) -> list[dict[str, str]]:
    return [
        {"task_id": task_id, "state": "success"}
        for task_id in sorted(module.EXPECTED_TASKS)
    ]


def test_scheduled_dag_serializes_single_writer_runs() -> None:
    dag_path = ROOT / "orchestration" / "airflow" / "dags" / "retail_batch_pipeline.py"
    tree = ast.parse(dag_path.read_text(encoding="utf-8"))
    dag_decorator = next(
        decorator
        for node in tree.body
        if isinstance(node, ast.FunctionDef) and node.name == "retail_batch_pipeline"
        for decorator in node.decorator_list
        if isinstance(decorator, ast.Call)
        and isinstance(decorator.func, ast.Name)
        and decorator.func.id == "dag"
    )
    keywords = {keyword.arg: keyword.value for keyword in dag_decorator.keywords}

    assert ast.literal_eval(keywords["schedule"]) == "@daily"
    assert ast.literal_eval(keywords["max_active_runs"]) == 1


def test_verifier_records_no_concurrent_running_dag_runs(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    module = _load_verifier("phase6_airflow_no_concurrent_runs")
    run_id = "phase6__20260726T141500Z"

    monkeypatch.setattr(module, "_wait_healthy", Mock())
    monkeypatch.setattr(
        module.dt,
        "datetime",
        Mock(
            now=Mock(
                return_value=Mock(
                    strftime=Mock(return_value="20260726T141500Z"),
                )
            )
        ),
    )

    def docker_exec(*arguments: str, timeout: int = 120) -> Mock:
        del timeout
        if arguments[:2] == ("dags", "list-import-errors"):
            return _result(stdout="[]")
        if arguments[:2] == ("tasks", "list"):
            return _result(stdout="\n".join(sorted(module.EXPECTED_TASKS)))
        if arguments[:2] == ("tasks", "states-for-dag-run"):
            return _result(stdout=json.dumps(_successful_task_rows(module)))
        if arguments[:2] == ("dags", "list-runs"):
            return _result(
                stdout=json.dumps(
                    [{"dag_id": module.DAG_ID, "run_id": run_id, "state": "running"}]
                )
            )
        return _result()

    monkeypatch.setattr(module, "_docker_exec", Mock(side_effect=docker_exec))
    monkeypatch.setattr(module, "_run", Mock(return_value=_result()))

    evidence = module.verify()

    assert evidence["run_id"] == run_id
    assert evidence["concurrent_writer_runs"] == 0
    assert any(
        call.args[:2] == ("dags", "list-runs")
        for call in module._docker_exec.call_args_list
    )


def test_verifier_fails_closed_if_two_dag_runs_are_running(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    module = _load_verifier("phase6_airflow_concurrent_runs")

    monkeypatch.setattr(module, "_wait_healthy", Mock())

    def docker_exec(*arguments: str, timeout: int = 120) -> Mock:
        del timeout
        if arguments[:2] == ("dags", "list-import-errors"):
            return _result(stdout="[]")
        if arguments[:2] == ("tasks", "list"):
            return _result(stdout="\n".join(sorted(module.EXPECTED_TASKS)))
        if arguments[:2] == ("tasks", "states-for-dag-run"):
            return _result(stdout=json.dumps(_successful_task_rows(module)))
        if arguments[:2] == ("dags", "list-runs"):
            return _result(
                stdout=json.dumps(
                    [
                        {"run_id": "scheduled__2026-07-26T00:00:00+00:00"},
                        {"run_id": "phase6__20260726T141500Z"},
                    ]
                )
            )
        return _result()

    monkeypatch.setattr(module, "_docker_exec", Mock(side_effect=docker_exec))
    monkeypatch.setattr(module, "_run", Mock(return_value=_result()))

    with pytest.raises(module.AirflowVerificationError, match="concurrent DAG runs"):
        module.verify()


def test_main_always_tears_down_after_verification_failure(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    module = _load_verifier("phase6_airflow_teardown")
    run = Mock(return_value=_result())
    monkeypatch.setattr(module, "_assert_no_other_heavy_profile", Mock())
    monkeypatch.setattr(
        module,
        "verify",
        Mock(side_effect=module.AirflowVerificationError("synthetic failure")),
    )
    monkeypatch.setattr(module, "_run", run)

    with pytest.raises(module.AirflowVerificationError, match="synthetic failure"):
        module.main()

    run.assert_called_once_with(["make", "down"], check=False, timeout=180)
