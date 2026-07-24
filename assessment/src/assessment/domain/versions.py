"""Supported public contract versions."""

from __future__ import annotations

import re

from assessment.domain.errors import CompatibilityError

SCHEMA_VERSION = "1.0.0"
FRAMEWORK_VERSION = "1.0.0"
CATALOG_VERSION = "1.0.0"
DEMO_CONTENT_VERSION = "1.0.0"
PROTOTYPE_VERSION = "0.1.0-prototype"
ARCHIVE_FORMAT_VERSION = "1.0.0"

SEMVER = re.compile(r"^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)$")


def require_supported_version(actual: object, expected: str, *, context: str) -> None:
    """Reject unsupported and unknown-newer versions with a typed error."""
    if actual == expected:
        return
    if isinstance(actual, str) and SEMVER.fullmatch(actual):
        actual_major = int(actual.split(".", 1)[0])
        expected_major = int(expected.split(".", 1)[0])
        relation = "newer" if actual_major > expected_major else "unsupported"
        raise CompatibilityError(f"{context}: {relation} version {actual!r}")
    raise CompatibilityError(f"{context}: unsupported version {actual!r}")
