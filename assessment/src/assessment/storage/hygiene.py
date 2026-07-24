"""Fail-closed secret, credentialed-URI, and absolute-path checks."""

from __future__ import annotations

import math
import re
from collections import Counter
from typing import Any

from assessment.domain.errors import ArchiveValidationError

SECRET = re.compile(
    rb"(?:AKIA[0-9A-Z]{16}|ghp_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,}|"
    rb"sk_(?:live|test)_[A-Za-z0-9]{16,}|xox[baprs]-[A-Za-z0-9-]{16,}|"
    rb"-----BEGIN [A-Z ]*PRIVATE KEY-----|"
    rb"(?i:(?:password|secret|token|credential|private[_-]?key)\s*[:=]\s*[\"']?[^,\s\"']{8,}))"
)
CREDENTIALED_URI = re.compile(rb"(?i)\b[a-z][a-z0-9+.-]*://[^/\s:@]+:[^/\s@]+@")
ABSOLUTE_PATH = re.compile(
    rb"(?i)(?:file://(?:localhost)?/|(?:^|[\s\"'=])/(?!/)"
    rb"[A-Za-z0-9._~+-]+(?:/[A-Za-z0-9._~+-]+)+|"
    rb"\b[A-Z]:[\\/][^\s\"'<>]+|\\\\[A-Za-z0-9_.-]+[\\/][^\s\"'<>]+)"
)
HIGH_RISK_KEY = re.compile(r"(?i)(?:password|secret|token|credential|private[_-]?key)")


def _entropy(value: str) -> float:
    if not value:
        return 0.0
    counts = Counter(value)
    return -sum((count / len(value)) * math.log2(count / len(value)) for count in counts.values())


def scan_bytes(content: bytes, *, context: str) -> None:
    if SECRET.search(content):
        raise ArchiveValidationError(f"{context}: secret-like content is not portable")
    if CREDENTIALED_URI.search(content):
        raise ArchiveValidationError(f"{context}: credentialed URI is not portable")
    if ABSOLUTE_PATH.search(content):
        raise ArchiveValidationError(f"{context}: absolute machine path is not portable")
    if b"\x00" in content:
        raise ArchiveValidationError(f"{context}: NUL content is not allowed")


def scan_json_keys(value: Any, *, context: str) -> None:
    if isinstance(value, dict):
        for key, item in value.items():
            if (
                HIGH_RISK_KEY.search(str(key))
                and item is not None
                and item is not False
                and item != ""
            ):
                raise ArchiveValidationError(f"{context}: populated high-risk key {key!r}")
            scan_json_keys(item, context=context)
    elif isinstance(value, list):
        for item in value:
            scan_json_keys(item, context=context)
    elif isinstance(value, str) and len(value) >= 32 and _entropy(value) >= 4.5:
        if SECRET.search(value.encode("utf-8", errors="ignore")):
            raise ArchiveValidationError(f"{context}: high-entropy secret-like value")
