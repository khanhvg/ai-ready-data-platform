from __future__ import annotations

from pathlib import Path

import pytest

from assessment.web.runtime_smoke import run_browser_journey


@pytest.mark.e2e
def test_complete_solution_architect_journey(tmp_path: Path) -> None:
    result = run_browser_journey(tmp_path / "browser-evidence")
    assert result["status"] == "pass"
    assert result["answers"] == 30
    assert result["gate_traces"] == 7
    assert result["report_sections"] == 12
    assert result["remote_requests"] == []
    assert result["console_errors"] == []
    assert result["server_logs_clean"] is True
