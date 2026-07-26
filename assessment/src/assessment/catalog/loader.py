"""Bounded package-resource loaders for the versioned advisory and demo catalogs."""

from __future__ import annotations

import hashlib
import json
import re
from importlib import resources
from importlib.resources.abc import Traversable
from pathlib import Path
from typing import Any
from xml.etree import ElementTree

import yaml
from yaml.tokens import AliasToken, AnchorToken

from assessment.catalog.models import (
    CatalogBundle,
    DemoCatalog,
    validate_catalog_relative_path,
)
from assessment.content.loader import MAX_AUTHORED_BYTES
from assessment.domain.errors import ContentValidationError

CATALOG_VERSION = "1.0.0"
CATALOG_ROOT = ("catalog", CATALOG_VERSION)
DEMO_ROOT = ("demo", CATALOG_VERSION)
SVG_NAMESPACE = "http://www.w3.org/2000/svg"
FORBIDDEN_SVG_TAGS = {
    "a",
    "animate",
    "audio",
    "embed",
    "foreignObject",
    "iframe",
    "image",
    "metadata",
    "object",
    "script",
    "set",
    "use",
    "video",
}
ALLOWED_SVG_TAGS = {
    "circle",
    "defs",
    "desc",
    "feDropShadow",
    "filter",
    "g",
    "linearGradient",
    "marker",
    "path",
    "polygon",
    "rect",
    "stop",
    "style",
    "svg",
    "text",
    "title",
    "tspan",
}
ALLOWED_SVG_ATTRIBUTES = {
    "aria-labelledby",
    "class",
    "cx",
    "cy",
    "d",
    "data-edge",
    "data-et",
    "data-id",
    "data-look",
    "data-points",
    "dx",
    "dy",
    "flood-color",
    "flood-opacity",
    "font-style",
    "font-weight",
    "gradientUnits",
    "height",
    "id",
    "marker-end",
    "markerHeight",
    "markerUnits",
    "markerWidth",
    "offset",
    "orient",
    "points",
    "r",
    "refX",
    "refY",
    "role",
    "stdDeviation",
    "stop-color",
    "stop-opacity",
    "style",
    "text-anchor",
    "transform",
    "viewBox",
    "width",
    "x",
    "x1",
    "x2",
    "y",
    "y1",
    "y2",
}
FORBIDDEN_SVG_BYTES = re.compile(
    rb"<!DOCTYPE|<!ENTITY|<\?|<!--|javascript:|data:|file:|https?://|"
    rb"@import|@font-face|/(?:Users|home|private|tmp)/|[A-Z]:\\",
    re.IGNORECASE,
)


def _resource(*parts: str) -> Traversable:
    resource = resources.files("assessment.content")
    for part in parts:
        resource = resource.joinpath(part)
    return resource


def _read_bounded(resource: Traversable, *, maximum_bytes: int = MAX_AUTHORED_BYTES) -> bytes:
    try:
        content = resource.read_bytes()
    except (OSError, FileNotFoundError) as error:
        raise ContentValidationError(f"{resource}: catalog resource is unavailable") from error
    if len(content) > maximum_bytes:
        raise ContentValidationError(f"{resource}: exceeds {maximum_bytes} byte limit")
    return content


def _load_yaml(resource: Traversable) -> dict[str, Any]:
    try:
        text = _read_bounded(resource).decode("utf-8", errors="strict")
        if any(isinstance(token, AliasToken | AnchorToken) for token in yaml.scan(text)):
            raise ContentValidationError(f"{resource}: YAML anchors and aliases are not allowed")
        document = yaml.safe_load(text)
    except UnicodeDecodeError as error:
        raise ContentValidationError(f"{resource}: content must be UTF-8") from error
    except yaml.YAMLError as error:
        raise ContentValidationError(f"{resource}: unsafe or malformed YAML") from error
    if not isinstance(document, dict):
        raise ContentValidationError(f"{resource}: YAML document must be a mapping")
    return document


def _manifest_paths(document: dict[str, Any], key: str) -> list[str]:
    values = document.get(key)
    if not isinstance(values, list) or not values:
        raise ContentValidationError(f"catalog manifest {key}: non-empty list required")
    paths: list[str] = []
    for value in values:
        if not isinstance(value, str):
            raise ContentValidationError(f"catalog manifest {key}: paths must be strings")
        paths.append(validate_catalog_relative_path(value))
    if len(paths) != len(set(paths)):
        raise ContentValidationError(f"catalog manifest {key}: duplicate paths")
    return paths


def _diagram_manifest() -> dict[str, Any]:
    resource = _resource(*CATALOG_ROOT, "diagrams", "render-manifest.json")
    try:
        document = json.loads(_read_bounded(resource, maximum_bytes=262_144))
    except (json.JSONDecodeError, UnicodeDecodeError) as error:
        raise ContentValidationError("diagram render manifest is malformed") from error
    if not isinstance(document, dict) or document.get("schema_version") != CATALOG_VERSION:
        raise ContentValidationError("diagram render manifest identity is invalid")
    diagrams = document.get("diagrams")
    if not isinstance(diagrams, list) or len(diagrams) != 7:
        raise ContentValidationError("diagram render manifest must contain seven entries")
    return document


def _diagram_manifest_entry(
    relative_path: str,
    *,
    manifest: dict[str, Any] | None = None,
) -> dict[str, Any]:
    manifest_document = manifest or _diagram_manifest()
    matches = [
        item
        for item in manifest_document["diagrams"]
        if isinstance(item, dict)
        and relative_path in {item.get("source"), item.get("output")}
    ]
    if len(matches) != 1:
        raise ContentValidationError(
            f"diagram asset {relative_path}: render manifest entry is missing or ambiguous"
        )
    return matches[0]


def _validate_svg(
    content: bytes,
    *,
    title: str | None = None,
    description: str | None = None,
) -> None:
    if FORBIDDEN_SVG_BYTES.search(
        content.replace(b"http://www.w3.org/2000/svg", b"")
        .replace(b"http://www.w3.org/1999/xlink", b"")
        .replace(b"http://www.w3.org/XML/1998/namespace", b"")
    ):
        raise ContentValidationError("catalog SVG contains active, remote, or local-path content")
    try:
        # The bounded package resource is pre-scanned above to reject DTDs,
        # entities, processing instructions, remote content, and local paths.
        root = ElementTree.fromstring(content)  # noqa: S314
    except ElementTree.ParseError as error:
        raise ContentValidationError("catalog SVG is malformed") from error
    if root.tag != f"{{{SVG_NAMESPACE}}}svg" or root.attrib.get("role") != "img":
        raise ContentValidationError("catalog SVG root accessibility contract is invalid")
    if any(
        attribute.lower().startswith("on")
        or attribute.split("}")[-1].lower() in {"href", "src"}
        for element in root.iter()
        for attribute in element.attrib
    ):
        raise ContentValidationError("catalog SVG contains executable or linked attributes")
    if any(element.tag.split("}")[-1] in FORBIDDEN_SVG_TAGS for element in root.iter()):
        raise ContentValidationError("catalog SVG contains a forbidden element")
    if any(
        not element.tag.startswith(f"{{{SVG_NAMESPACE}}}")
        or element.tag.split("}")[-1] not in ALLOWED_SVG_TAGS
        or any(attribute not in ALLOWED_SVG_ATTRIBUTES for attribute in element.attrib)
        for element in root.iter()
    ):
        raise ContentValidationError(
            "catalog SVG contains an unexpected element, namespace, or attribute"
        )
    titles = [
        element
        for element in root
        if element.tag == f"{{{SVG_NAMESPACE}}}title"
    ]
    descriptions = [
        element
        for element in root
        if element.tag == f"{{{SVG_NAMESPACE}}}desc"
    ]
    if (
        len(titles) != 1
        or len(descriptions) != 1
        or not titles[0].text
        or not descriptions[0].text
        or (title is not None and titles[0].text != title)
        or (description is not None and descriptions[0].text != description)
    ):
        raise ContentValidationError("catalog SVG title or description does not match metadata")
    labelled = set(root.attrib.get("aria-labelledby", "").split())
    if {titles[0].attrib.get("id"), descriptions[0].attrib.get("id")} != labelled:
        raise ContentValidationError("catalog SVG aria-labelledby contract is invalid")


def _validated_diagram_asset(
    relative_path: str,
    *,
    title: str | None = None,
    description: str | None = None,
    manifest: dict[str, Any] | None = None,
) -> bytes:
    entry = _diagram_manifest_entry(relative_path, manifest=manifest)
    content = _read_bounded(
        _resource(*CATALOG_ROOT, *relative_path.split("/")),
        maximum_bytes=4_194_304,
    )
    digest_key = "source_sha256" if relative_path.endswith(".mmd") else "output_sha256"
    if hashlib.sha256(content).hexdigest() != entry.get(digest_key):
        raise ContentValidationError(f"diagram asset {relative_path}: digest mismatch")
    if relative_path.endswith(".svg"):
        _validate_svg(content, title=title, description=description)
    return content


def load_catalog(version: str = CATALOG_VERSION) -> CatalogBundle:
    if version != CATALOG_VERSION:
        raise ContentValidationError(f"catalog: unsupported version {version!r}")
    manifest = _load_yaml(_resource(*CATALOG_ROOT, "catalog.yaml"))
    if (
        manifest.get("schema_version") != CATALOG_VERSION
        or manifest.get("catalog_version") != CATALOG_VERSION
    ):
        raise ContentValidationError("catalog manifest identity is invalid")
    capabilities: list[dict[str, Any]] = []
    architectures: list[dict[str, Any]] = []
    technology_profiles: list[dict[str, Any]] = []
    for filename in _manifest_paths(manifest, "capability_files"):
        document = _load_yaml(_resource(*CATALOG_ROOT, filename))
        value = document.get("capability")
        if not isinstance(value, dict):
            raise ContentValidationError(f"{filename}: capability mapping required")
        capabilities.append(value)
    for filename in _manifest_paths(manifest, "architecture_files"):
        document = _load_yaml(_resource(*CATALOG_ROOT, filename))
        values = document.get("architectures")
        if not isinstance(values, list):
            raise ContentValidationError(f"{filename}: architectures list required")
        architectures.extend(values)
    for filename in _manifest_paths(manifest, "technology_mapping_files"):
        document = _load_yaml(_resource(*CATALOG_ROOT, filename))
        value = document.get("technology_profile")
        if not isinstance(value, dict):
            raise ContentValidationError(f"{filename}: technology_profile mapping required")
        technology_profiles.append(value)
    diagrams = manifest.get("diagrams")
    if not isinstance(diagrams, list):
        raise ContentValidationError("catalog manifest diagrams: list required")
    bundle = CatalogBundle.validate_semantics(
        {
            "version": version,
            "capabilities": capabilities,
            "architectures": architectures,
            "technology_profiles": technology_profiles,
            "diagrams": diagrams,
        }
    )
    diagram_manifest = _diagram_manifest()
    manifest_entries = diagram_manifest["diagrams"]
    if sorted(
        [
        (
            item.get("id"),
            item.get("source"),
            item.get("output"),
        )
        for item in manifest_entries
        if isinstance(item, dict)
        ]
    ) != sorted(
        [
        (diagram.id, diagram.source_path, diagram.svg_path)
        for diagram in bundle.diagrams
        ]
    ):
        raise ContentValidationError("diagram manifest and catalog metadata differ")
    for diagram in bundle.diagrams:
        _validated_diagram_asset(
            diagram.source_path,
            manifest=diagram_manifest,
        )
        _validated_diagram_asset(
            diagram.svg_path,
            title=diagram.accessible_title,
            description=diagram.accessible_description,
            manifest=diagram_manifest,
        )
    return bundle


def _artifact_status(repository_root: Path | None, relative_path: str) -> str:
    validate_catalog_relative_path(relative_path)
    if repository_root is None:
        return "unavailable"
    root = repository_root.absolute()
    if root.is_symlink() or not root.is_dir():
        raise ContentValidationError("repository root must be a real absolute directory")
    candidate = root.joinpath(*relative_path.split("/"))
    try:
        resolved_root = root.resolve(strict=True)
        resolved_candidate = candidate.resolve(strict=True)
    except FileNotFoundError:
        return "unavailable"
    if (
        resolved_candidate.parent != resolved_root
        and resolved_root not in resolved_candidate.parents
    ):
        raise ContentValidationError(f"demo artifact {relative_path}: escapes repository root")
    return "available" if resolved_candidate.is_file() else "unavailable"


def load_demo_catalog(
    version: str = CATALOG_VERSION,
    *,
    repository_root: Path | None = None,
) -> DemoCatalog:
    if version != CATALOG_VERSION:
        raise ContentValidationError(f"demo catalog: unsupported version {version!r}")
    stages_document = _load_yaml(_resource(*DEMO_ROOT, "stages.yaml"))
    guide_document = _load_yaml(_resource(*DEMO_ROOT, "demo-guide.yaml"))
    links_document = _load_yaml(_resource(*DEMO_ROOT, "evidence-links.yaml"))
    if any(
        document.get("demo_content_version") != version
        for document in (stages_document, guide_document, links_document)
    ):
        raise ContentValidationError("demo catalog version identity is invalid")
    raw_stages = stages_document.get("stages")
    if not isinstance(raw_stages, list):
        raise ContentValidationError("demo stages: list required")
    stages: list[dict[str, Any]] = []
    for raw_stage in raw_stages:
        if not isinstance(raw_stage, dict):
            raise ContentValidationError("demo stage: mapping required")
        stage = dict(raw_stage)
        raw_artifacts = stage.get("artifacts")
        if not isinstance(raw_artifacts, list):
            raise ContentValidationError(f"demo stage {stage.get('id')}: artifacts list required")
        stage["artifacts"] = [
            {
                **artifact,
                "status": _artifact_status(repository_root, str(artifact.get("path", ""))),
            }
            for artifact in raw_artifacts
            if isinstance(artifact, dict)
        ]
        if len(stage["artifacts"]) != len(raw_artifacts):
            raise ContentValidationError(f"demo stage {stage.get('id')}: invalid artifact entry")
        stages.append(stage)
    evidence_links = links_document.get("evidence_links")
    if not isinstance(evidence_links, list):
        raise ContentValidationError("demo evidence links: list required")
    return DemoCatalog.validate_semantics(
        {
            "version": version,
            "title": guide_document.get("title"),
            "presenter_purpose": guide_document.get("presenter_purpose"),
            "non_scoring_disclaimer": guide_document.get("non_scoring_disclaimer"),
            "automation_eligible_steps": guide_document.get(
                "automation_eligible_steps"
            ),
            "automation_automated_steps": guide_document.get(
                "automation_automated_steps"
            ),
            "operating_boundary": guide_document.get("operating_boundary"),
            "stage_order": guide_document.get("stage_order"),
            "stages": stages,
            "evidence_links": evidence_links,
        }
    )


def read_catalog_asset(relative_path: str) -> bytes:
    safe_path = validate_catalog_relative_path(relative_path)
    if not safe_path.startswith("diagrams/"):
        raise ContentValidationError("catalog asset path must be beneath diagrams/")
    if safe_path.endswith((".mmd", ".svg")):
        return _validated_diagram_asset(safe_path)
    return _read_bounded(
        _resource(*CATALOG_ROOT, *safe_path.split("/")),
        maximum_bytes=4_194_304,
    )
