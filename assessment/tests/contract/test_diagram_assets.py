from __future__ import annotations

import hashlib
import json
import re
from importlib import resources
from pathlib import Path

import pytest

from assessment.catalog.loader import _validate_svg, load_catalog, read_catalog_asset
from assessment.domain.errors import ContentValidationError

DIAGRAM_IDS = {
    "executive-ai-readiness",
    "logical-platform-context",
    "engagement-lifecycle",
    "scoring-and-gates",
    "security-and-access",
    "metadata-and-lineage",
    "demo-evidence-mapping",
}
UNSAFE_SVG = re.compile(
    rb"<(?:script|foreignObject|image|iframe|object|embed)\b|"
    rb"\son[a-z]+\s*=|(?:href|src)\s*=\s*[\"'](?:https?:|//)|"
    rb"@font-face|@import|url\s*\(\s*[\"']?(?:https?:|//)",
    re.IGNORECASE,
)
REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
DIAGRAM_TOOL_ROOT = REPOSITORY_ROOT / "assessment" / "diagram-tools"


def test_exactly_seven_diagram_source_render_pairs_are_packaged() -> None:
    catalog = load_catalog()
    assert {diagram.id for diagram in catalog.diagrams} == DIAGRAM_IDS
    for diagram in catalog.diagrams:
        source = read_catalog_asset(diagram.source_path)
        rendered = read_catalog_asset(diagram.svg_path)
        assert source
        assert rendered.startswith(b"<svg")
        assert diagram.audience
        assert diagram.purpose
        assert diagram.text_alternative


def test_reviewed_svgs_are_accessible_and_contain_no_active_or_remote_content() -> None:
    combined_ids: list[str] = []
    for diagram in load_catalog().diagrams:
        rendered = read_catalog_asset(diagram.svg_path)
        text = rendered.decode("utf-8")
        assert '<svg xmlns="http://www.w3.org/2000/svg"' in text
        assert 'role="img"' in text
        assert 'aria-labelledby="' in text
        assert text.count("<title ") == 1
        assert text.count("<desc ") == 1
        assert diagram.accessible_title in text
        assert diagram.accessible_description in text
        assert not UNSAFE_SVG.search(rendered)
        assert "<metadata" not in text
        combined_ids.extend(re.findall(r'(?:^|[ <])id="([^"]+)"', text))
    assert len(combined_ids) == len(set(combined_ids))


def test_render_manifest_matches_committed_source_tool_and_output_digests() -> None:
    manifest = json.loads(read_catalog_asset("diagrams/render-manifest.json"))
    assert manifest["schema_version"] == "1.0.0"
    assert manifest["node_major"] == 22
    assert manifest["mermaid_cli_version"]
    assert len(manifest["diagrams"]) == 7
    assert {item["id"] for item in manifest["diagrams"]} == DIAGRAM_IDS
    for item in manifest["diagrams"]:
        assert hashlib.sha256(read_catalog_asset(item["source"])).hexdigest() == (
            item["source_sha256"]
        )
        assert hashlib.sha256(read_catalog_asset(item["output"])).hexdigest() == (
            item["output_sha256"]
        )
    assert set(manifest["tool_files"]) == {
        "mermaid-config.json",
        "package-lock.json",
        "package.json",
        "render.mjs",
        "render.test.mjs",
    }
    for name, digest in manifest["tool_files"].items():
        assert hashlib.sha256((DIAGRAM_TOOL_ROOT / name).read_bytes()).hexdigest() == digest


def test_diagram_toolchain_is_exact_hash_locked_and_build_only() -> None:
    package = json.loads((DIAGRAM_TOOL_ROOT / "package.json").read_bytes())
    lock = json.loads((DIAGRAM_TOOL_ROOT / "package-lock.json").read_bytes())
    assert package["engines"] == {"node": ">=22.12 <23", "npm": "10.9.8"}
    assert package["packageManager"] == "npm@10.9.8"
    assert package["devDependencies"] == {
        "@mermaid-js/mermaid-cli": "11.16.0",
        "puppeteer": "25.3.0",
    }
    assert lock["lockfileVersion"] == 3
    assert lock["packages"][""]["devDependencies"] == package["devDependencies"]
    assert "diagram-tools" not in str(resources.files("assessment.content"))


def test_runtime_svg_validation_rejects_tampered_active_or_remote_assets() -> None:
    catalog = load_catalog()
    diagram = catalog.diagrams[0]
    safe = read_catalog_asset(diagram.svg_path)
    for injection in (
        b"<script>alert(1)</script>",
        b'<image href="https://remote.invalid/a.png"/>',
        b'<rect onload="alert(1)"/>',
        b"<foreignObject>HTML</foreignObject>",
        b"<metadata>unexpected</metadata>",
        b"<text>/Users/example/private.txt</text>",
    ):
        hostile = safe.replace(b"</svg>", injection + b"</svg>")
        with pytest.raises(ContentValidationError):
            _validate_svg(
                hostile,
                title=diagram.accessible_title,
                description=diagram.accessible_description,
            )


def test_catalog_resources_are_available_through_importlib() -> None:
    package_root = resources.files("assessment.content")
    assert package_root.joinpath("catalog", "1.0.0", "catalog.yaml").is_file()
    assert package_root.joinpath("demo", "1.0.0", "demo-guide.yaml").is_file()
