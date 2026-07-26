from __future__ import annotations

from pathlib import Path

import pytest

from assessment.web.runtime_smoke import run_browser_journey


@pytest.mark.e2e
def test_complete_solution_architect_journey(tmp_path: Path) -> None:
    result = run_browser_journey(
        tmp_path / "browser-evidence",
        repository_root=Path(__file__).resolve().parents[3],
    )
    assert result["status"] == "pass"
    assert result["answers"] == 30
    assert result["gate_traces"] == 7
    assert result["report_sections"] == 12
    assert result["remote_requests"] == []
    assert result["console_errors"] == []
    assert result["page_errors"] == []
    assert result["unexpected_request_failures"] == []
    assert result["server_logs_clean"] is True
    assert result["clean_teardown"] is True
