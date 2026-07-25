from __future__ import annotations

from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from assessment.web.app import create_app
from assessment.web.config import WebConfig


@pytest.mark.e2e
def test_catalog_and_demo_are_honest_read_only_surfaces(tmp_path: Path) -> None:
    config = WebConfig.for_roots(tmp_path / "engagements", tmp_path / "runtime")
    with TestClient(create_app(config=config), base_url="http://127.0.0.1") as client:
        catalog = client.get("/catalog")
        demo = client.get("/demo")
    assert catalog.status_code == 200
    assert "details not installed" in catalog.text
    assert "<button" not in catalog.text
    assert demo.status_code == 200
    assert "not installed" in demo.text
    assert "<button" not in demo.text
    for forbidden in ("subprocess", "docker", "run pipeline", "credential"):
        assert forbidden not in (catalog.text + demo.text).lower()
