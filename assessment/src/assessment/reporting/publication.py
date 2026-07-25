"""Coherent publication and validation for deterministic report bundles."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from collections.abc import Callable
from typing import Any

from assessment.domain.errors import ContentValidationError
from assessment.storage.local import (
    _fsync_directory_descriptor,
    atomic_write_at,
    canonical_json,
)


def read_bound_artifact(output_descriptor: int, name: str) -> bytes | None:
    """Read a regular artifact relative to an already validated output directory."""
    flags = os.O_RDONLY
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    try:
        descriptor = os.open(name, flags, dir_fd=output_descriptor)
    except FileNotFoundError:
        return None
    try:
        if not stat.S_ISREG(os.fstat(descriptor).st_mode):
            raise ContentValidationError(f"output artifact must be a regular file: {name}")
        with os.fdopen(descriptor, "rb", closefd=False) as handle:
            return handle.read()
    finally:
        os.close(descriptor)


def publish_report(
    output_descriptor: int,
    json_bytes: bytes,
    html_bytes: bytes,
    source_digest: str,
    *,
    writer: Callable[[int, str, bytes], None] = atomic_write_at,
) -> dict[str, str]:
    """Publish a report bundle and restore the prior coherent set on failure."""
    digests = {
        "report.json": hashlib.sha256(json_bytes).hexdigest(),
        "report.html": hashlib.sha256(html_bytes).hexdigest(),
    }
    manifest_bytes = canonical_json(
        {
            "schema_version": "1.0.0",
            "source_state_digest": source_digest,
            "artifacts": digests,
        }
    )
    payloads = {
        "report.json": json_bytes,
        "report.html": html_bytes,
        "report-manifest.json": manifest_bytes,
    }
    previous = {name: read_bound_artifact(output_descriptor, name) for name in payloads}
    try:
        for name, content in payloads.items():
            writer(output_descriptor, name, content)
    except Exception:
        for name, previous_content in previous.items():
            if previous_content is None:
                try:
                    os.unlink(name, dir_fd=output_descriptor)
                except FileNotFoundError:
                    pass
            else:
                writer(output_descriptor, name, previous_content)
        _fsync_directory_descriptor(output_descriptor)
        raise
    return digests


def read_published_report(
    output_descriptor: int,
) -> tuple[dict[str, Any], dict[str, Any], bytes, bytes] | None:
    """Return only a complete report whose bytes match its commit manifest."""
    json_bytes = read_bound_artifact(output_descriptor, "report.json")
    html_bytes = read_bound_artifact(output_descriptor, "report.html")
    manifest_bytes = read_bound_artifact(output_descriptor, "report-manifest.json")
    if json_bytes is None and html_bytes is None and manifest_bytes is None:
        return None
    if json_bytes is None or html_bytes is None or manifest_bytes is None:
        raise ContentValidationError("published report bundle is incomplete")
    report = json.loads(json_bytes)
    manifest = json.loads(manifest_bytes)
    expected = {
        "report.json": hashlib.sha256(json_bytes).hexdigest(),
        "report.html": hashlib.sha256(html_bytes).hexdigest(),
    }
    if not isinstance(report, dict) or not isinstance(manifest, dict):
        raise ContentValidationError("published report bundle must contain JSON objects")
    if manifest.get("artifacts") != expected:
        raise ContentValidationError("published report bundle does not match its manifest")
    return report, manifest, json_bytes, html_bytes
