"""Schema-, provenance-, and descriptor-bound evidence verification."""

from __future__ import annotations

import pathlib
import hashlib
from typing import Any

from .canonical import canonical_bytes
from .references import resolve_reference
from .schema import LearningContractError, validate_document


def verify_evidence(
    value: dict[str, Any],
    *,
    root: pathlib.Path,
    seen_run_ids: set[str] | None = None,
) -> None:
    try:
        validate_document(value, family="learning-evidence")
    except LearningContractError as exc:
        if exc.code == "SCHEMA_INVALID":
            raise LearningContractError("EVIDENCE_SCHEMA_INVALID") from exc
        raise
    run_id = value["runId"]
    if seen_run_ids is not None and run_id in seen_run_ids:
        raise LearningContractError("EVIDENCE_REPLAY")
    payload = {key: child for key, child in value.items() if key != "integrity"}
    if hashlib.sha256(canonical_bytes(payload)).hexdigest() != value["integrity"]["payloadSha256"]:
        raise LearningContractError("EVIDENCE_PAYLOAD_TAMPER")
    for item in value["artifacts"]:
        try:
            raw = resolve_reference(root, item["locator"], item["sha256"])
        except LearningContractError as exc:
            raise LearningContractError("EVIDENCE_ARTIFACT_TAMPER") from exc
        if len(raw) != item["size"]:
            raise LearningContractError("EVIDENCE_ARTIFACT_TAMPER")
    if seen_run_ids is not None:
        seen_run_ids.add(run_id)


def verify_manifest(value: dict[str, Any], *, root: pathlib.Path) -> None:
    if set(value) != {"schemaVersion", "entries"} or value.get("schemaVersion") != "evidence-manifest-v1":
        raise LearningContractError("MANIFEST_SCHEMA_INVALID")
    entries = value.get("entries")
    if not isinstance(entries, list) or not entries:
        raise LearningContractError("MANIFEST_SCHEMA_INVALID")
    locators = [item.get("locator") for item in entries if isinstance(item, dict)]
    actual = sorted(path.name for path in root.iterdir() if path.is_file() and not path.is_symlink())
    if sorted(locators) != actual or len(locators) != len(set(locators)):
        raise LearningContractError("MANIFEST_INCOMPLETE")
    for item in entries:
        raw = resolve_reference(root, item["locator"], item["sha256"])
        if len(raw) != item["size"]:
            raise LearningContractError("MANIFEST_ENTRY_TAMPER")
