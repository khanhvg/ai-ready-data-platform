"""Pinned framework bundle loader for the deterministic v1 engine."""

from __future__ import annotations

import copy
import hashlib
from dataclasses import dataclass
from importlib import resources
from typing import Any

import yaml

from assessment.domain.errors import CompatibilityError, ContentValidationError
from prototype.run import load_framework as load_prototype_framework  # type: ignore

FRAMEWORK_VERSION = "1.0.0"


@dataclass(frozen=True)
class FrameworkBundle:
    """Immutable-by-convention content snapshot selected by an engagement."""

    version: str
    domains: list[dict[str, Any]]
    questions: list[dict[str, Any]]
    readiness: dict[str, Any]
    gate_rules: list[dict[str, Any]]
    diagnostic_facts: list[dict[str, Any]]
    finding_rules: list[dict[str, Any]]
    recommendations: list[dict[str, Any]]
    architectures: list[dict[str, Any]]


def _manifest() -> dict[str, Any]:
    raw = (
        resources.files("assessment")
        .joinpath("framework_assets", FRAMEWORK_VERSION, "bundle.yaml")
        .read_text(encoding="utf-8")
    )
    document = yaml.safe_load(raw)
    if not isinstance(document, dict):
        raise ContentValidationError("framework bundle manifest must be an object")
    if (
        document.get("schema_version") != FRAMEWORK_VERSION
        or document.get("framework_version") != FRAMEWORK_VERSION
        or document.get("assessment_profile_id") != "quick-v1"
        or document.get("gate_bundle_version") != 1
        or document.get("calibrated_content_base") != "0.1.0-prototype"
    ):
        raise ContentValidationError("framework bundle manifest identity is invalid")
    return document


def _verified_content() -> None:
    manifest = _manifest()
    expected = manifest.get("content")
    if not isinstance(expected, dict):
        raise ContentValidationError("framework bundle content inventory is invalid")
    prototype_root = resources.files("prototype").joinpath("0.1.0")
    for name, expected_digest in sorted(expected.items()):
        resource = prototype_root.joinpath(name)
        actual = hashlib.sha256(resource.read_bytes()).hexdigest()
        if actual != expected_digest:
            raise ContentValidationError(
                f"framework bundle content digest mismatch: {name}"
            )


def load_report_asset(name: str) -> str:
    manifest = _manifest()
    expected = manifest.get("report_assets")
    if not isinstance(expected, dict) or name not in expected:
        raise ContentValidationError(f"framework bundle has no report asset {name!r}")
    content = (
        resources.files("assessment")
        .joinpath("framework_assets", FRAMEWORK_VERSION, name)
        .read_bytes()
    )
    if hashlib.sha256(content).hexdigest() != expected[name]:
        raise ContentValidationError(f"framework report asset digest mismatch: {name}")
    return content.decode("utf-8")


def load_framework(version: str) -> FrameworkBundle:
    """Load the v1 bundle by mapping the frozen calibrated content into v1."""
    if version != FRAMEWORK_VERSION:
        raise CompatibilityError(f"framework: unsupported version {version!r}")
    _verified_content()
    source = load_prototype_framework()
    return FrameworkBundle(
        version=FRAMEWORK_VERSION,
        domains=copy.deepcopy(source.capabilities["domains"]),
        questions=copy.deepcopy(source.questions["questions"]),
        readiness=copy.deepcopy(dict(source.readiness)),
        gate_rules=copy.deepcopy(source.gates["rules"]),
        diagnostic_facts=copy.deepcopy(source.gates["diagnostic_facts"]),
        finding_rules=copy.deepcopy(source.finding_rules["rules"]),
        recommendations=copy.deepcopy(list(source.recommendations["recommendations"])),
        architectures=copy.deepcopy(list(source.recommendations["architectures"])),
    )
