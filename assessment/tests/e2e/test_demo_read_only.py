from __future__ import annotations

from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from assessment.web.app import create_app
from assessment.web.config import WebConfig

PHASE_6_STAGE_MANIFESTS = (
    "demo/manifests/stages/ingestion.yaml",
    "demo/manifests/stages/quality-quarantine.yaml",
    "demo/manifests/stages/transformation.yaml",
    "demo/manifests/stages/metadata.yaml",
    "demo/manifests/stages/lineage.yaml",
    "demo/manifests/stages/governance.yaml",
    "demo/manifests/stages/access-control.yaml",
    "demo/manifests/stages/serving.yaml",
    "demo/manifests/stages/ai-ready-publication.yaml",
)


@pytest.mark.e2e
def test_catalog_and_demo_are_honest_read_only_surfaces(tmp_path: Path) -> None:
    config = WebConfig.for_roots(
        tmp_path / "engagements",
        tmp_path / "runtime",
        repository_root=Path(__file__).resolve().parents[3],
    )
    with TestClient(create_app(config=config), base_url="http://127.0.0.1") as client:
        catalog = client.get("/catalog")
        demo = client.get("/demo")
    assert catalog.status_code == 200
    assert "10 capability domains" in catalog.text
    assert "AWS first named implementation profile" in catalog.text
    assert "<button" not in catalog.text
    assert "<form" not in catalog.text
    assert demo.status_code == 200
    assert "9 read-only presenter stages" in demo.text
    assert "30/30 = 100%" in demo.text
    assert "current OpenMetadata execution is unexecuted" in demo.text
    assert "demo/manifests/ai-ready-customer-product.v1.yaml" in demo.text
    assert "demo/evidence/current/ai-ready-customer-product.csv" in demo.text
    for manifest_path in PHASE_6_STAGE_MANIFESTS:
        assert manifest_path in demo.text
    for control in ("<button", "<form", "<input", "<select", "<textarea"):
        assert control not in demo.text
    assert "action=" not in demo.text
    for forbidden in (
        "subprocess",
        "docker compose up",
        "terraform apply",
        "aws_access_key",
        "run pipeline",
    ):
        assert forbidden not in (catalog.text + demo.text).lower()
