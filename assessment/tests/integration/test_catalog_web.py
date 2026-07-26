from __future__ import annotations

import re
from pathlib import Path

from fastapi.testclient import TestClient

from assessment.web.app import create_app
from assessment.web.config import WebConfig

REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
UNSAFE_SVG = re.compile(
    rb"<(?:script|foreignObject|image|iframe|object|embed)\b|"
    rb"\son[a-z]+\s*=|(?:href|src)\s*=\s*[\"'](?:https?:|//)",
    re.IGNORECASE,
)


def catalog_client(tmp_path: Path) -> TestClient:
    config = WebConfig.for_roots(
        tmp_path / "engagements",
        tmp_path / "runtime",
        repository_root=REPOSITORY_ROOT,
    )
    return TestClient(create_app(config=config), base_url="http://127.0.0.1")


def test_catalog_view_presents_validated_domains_patterns_profiles_and_diagrams(
    tmp_path: Path,
) -> None:
    with catalog_client(tmp_path) as client:
        response = client.get("/catalog")
    assert response.status_code == 200
    assert "10 capability domains" in response.text
    assert "Strategy, ownership, and operating model" in response.text
    assert "Quality gate with quarantine and accepted boundary" in response.text
    assert "AWS first named implementation profile" in response.text
    assert "Existing sandbox read-only demo evidence mapping" in response.text
    assert response.text.count('class="catalog-diagram"') == 7
    assert "Demo artifacts are illustrations only" in response.text
    assert "<button" not in response.text
    assert "<form" not in response.text


def test_catalog_diagram_route_is_allowlisted_local_and_safe(tmp_path: Path) -> None:
    with catalog_client(tmp_path) as client:
        response = client.get("/catalog/diagrams/security-and-access.svg")
        missing = client.get("/catalog/diagrams/not-installed.svg")
        traversal = client.get("/catalog/diagrams/..%2F..%2Fengagement.json")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("image/svg+xml")
    assert response.content.startswith(b"<svg")
    assert not UNSAFE_SVG.search(response.content)
    assert missing.status_code == 404
    assert traversal.status_code in {404, 422}


def test_demo_view_shows_available_and_unavailable_artifacts_without_controls(
    tmp_path: Path,
) -> None:
    with catalog_client(tmp_path) as client:
        response = client.get("/demo")
    assert response.status_code == 200
    assert "9 read-only presenter stages" in response.text
    assert "artifact available" in response.text
    assert "artifact unavailable" in response.text
    assert "Demo artifacts are illustrations only" in response.text
    assert "does not execute" in response.text
    assert "<button" not in response.text
    assert "<form" not in response.text


def test_catalog_and_demo_routes_offer_no_mutating_method(tmp_path: Path) -> None:
    app = create_app(
        config=WebConfig.for_roots(
            tmp_path / "engagements",
            tmp_path / "runtime",
            repository_root=REPOSITORY_ROOT,
        )
    )
    pending = list(app.routes)
    flattened = []
    while pending:
        route = pending.pop()
        included = getattr(route, "original_router", None)
        if included is not None:
            pending.extend(included.routes)
            continue
        nested = getattr(route, "routes", None)
        if nested is not None:
            pending.extend(nested)
        else:
            flattened.append(route)
    route_methods = {
        route.path: set(route.methods or set())
        for route in flattened
        if hasattr(route, "path")
        and (
            route.path.startswith("/catalog")
            or route.path.startswith("/demo")
        )
    }
    assert route_methods["/catalog"] == {"GET"}
    assert route_methods["/demo"] == {"GET"}
    assert route_methods["/catalog/diagrams/{name}"] == {"GET"}
