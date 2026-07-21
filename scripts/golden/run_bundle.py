#!/usr/bin/env python3
"""Verify a retained golden run as one marker- and descriptor-bound bundle."""
from __future__ import annotations

import hashlib
import json
import os
import pathlib
import stat
from dataclasses import dataclass
from typing import Any

import rfc8785

import schema_reader


ROOT = pathlib.Path(__file__).resolve().parents[2]
CORE_FILES = ("raw.json", "projection.json", "envelope.json", "result.json", "run-metadata.json")
VOLATILE_RAW_KEYS = ("runId", "startedAt", "finishedAt", "durationMs", "workspaceLocator")


class BundleError(ValueError):
    pass


@dataclass(frozen=True)
class VerifiedBundle:
    path: pathlib.Path
    run_id: str
    tested_tree_sha: str
    raw: dict[str, Any]
    projection: dict[str, Any]
    result: dict[str, Any]
    metadata: dict[str, Any]
    projection_bytes: bytes
    normalized_raw_bytes: bytes


def _sha(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def _json_bytes(payload: bytes) -> dict[str, Any]:
    try:
        value = json.loads(payload)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise BundleError("RUN_BUNDLE_JSON_INVALID") from exc
    if not isinstance(value, dict):
        raise BundleError("RUN_BUNDLE_JSON_INVALID")
    return value


def _open_directory_nofollow(path: pathlib.Path) -> tuple[pathlib.Path, int]:
    absolute = pathlib.Path(os.path.abspath(path))
    current = os.open("/", os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        for component in absolute.parts[1:]:
            following = os.open(component, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=current)
            os.close(current); current = following
        return absolute, current
    except OSError as exc:
        os.close(current)
        raise BundleError("RUN_BUNDLE_DIRECTORY_UNSAFE") from exc


def _read_entry(directory_fd: int, name: str) -> bytes:
    try:
        fd = os.open(name, os.O_RDONLY | os.O_NOFOLLOW, dir_fd=directory_fd)
    except OSError as exc:
        raise BundleError("RUN_BUNDLE_ENTRY_UNSAFE") from exc
    try:
        before = os.fstat(fd)
        if not stat.S_ISREG(before.st_mode) or before.st_nlink != 1:
            raise BundleError("RUN_BUNDLE_ENTRY_UNSAFE")
        chunks = []
        while True:
            chunk = os.read(fd, 1024 * 1024)
            if not chunk: break
            chunks.append(chunk)
        after = os.fstat(fd)
        if (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns) != (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns):
            raise BundleError("RUN_BUNDLE_ENTRY_CHANGED")
        return b"".join(chunks)
    finally:
        os.close(fd)


def _verify_owned_directory(path: pathlib.Path, run_id: str) -> tuple[pathlib.Path, int]:
    absolute, directory_fd = _open_directory_nofollow(path)
    try:
        info = os.fstat(directory_fd)
        if not stat.S_ISDIR(info.st_mode) or stat.S_IMODE(info.st_mode) & 0o077:
            raise BundleError("RUN_BUNDLE_DIRECTORY_UNSAFE")
        marker = _json_bytes(_read_entry(directory_fd, ".golden-owner.json"))
        expected = {"schemaVersion": "golden-owner-v1", "runId": run_id, "purpose": "golden-run"}
        if any(marker.get(key) != value for key, value in expected.items()):
            raise BundleError("RUN_BUNDLE_MARKER_MISMATCH")
        if marker.get("device") != info.st_dev or marker.get("inode") != info.st_ino:
            raise BundleError("RUN_BUNDLE_MARKER_IDENTITY_MISMATCH")
        if not isinstance(marker.get("nonce"), str) or len(marker["nonce"]) != 64:
            raise BundleError("RUN_BUNDLE_MARKER_MISMATCH")
        return absolute, directory_fd
    except BaseException:
        os.close(directory_fd)
        raise


def normalized_raw(value: dict[str, Any]) -> bytes:
    clone = json.loads(json.dumps(value))
    run = clone.get("run")
    if not isinstance(run, dict):
        raise BundleError("RUN_BUNDLE_RAW_INVALID")
    for key in VOLATILE_RAW_KEYS:
        run.pop(key, None)
    return rfc8785.dumps(clone)


def verify(path: pathlib.Path, expected_tested_tree_sha: str | None = None) -> VerifiedBundle:
    path = pathlib.Path(os.path.abspath(path))
    run_id = path.name
    if len(run_id) != 32 or any(character not in "0123456789abcdef" for character in run_id):
        raise BundleError("RUN_BUNDLE_ID_INVALID")
    path, evidence_fd = _verify_owned_directory(path, run_id)
    artifacts_root = path.parent.parent.parent if path.parent.name == "golden" and path.parent.parent.name == "evidence" and path.parent.parent.parent.name == ".artifacts" else ROOT / ".artifacts"
    workspace = artifacts_root / "workspaces/golden" / run_id
    try:
        _, workspace_fd = _verify_owned_directory(workspace, run_id)
    except BaseException:
        os.close(evidence_fd)
        raise
    try:
        payloads = {name: _read_entry(evidence_fd, name) for name in (*CORE_FILES, "completion.json")}
    finally:
        os.close(workspace_fd); os.close(evidence_fd)

    completion = _json_bytes(payloads["completion.json"])
    expected_completion = {
        "schemaVersion": "golden-run-completion-v1",
        "runId": run_id,
        "artifacts": [{"locator": name, "sha256": _sha(payloads[name])} for name in CORE_FILES],
    }
    if completion != expected_completion:
        raise BundleError("RUN_BUNDLE_COMPLETION_MISMATCH")

    raw = _json_bytes(payloads["raw.json"])
    projection = _json_bytes(payloads["projection.json"])
    envelope = _json_bytes(payloads["envelope.json"])
    result = _json_bytes(payloads["result.json"])
    metadata = _json_bytes(payloads["run-metadata.json"])
    schema_reader.validate("evidence-envelope", envelope)
    schema_reader.validate("fitness-result", result)

    tested = projection.get("testedTreeSha")
    if not isinstance(tested, str) or expected_tested_tree_sha not in (None, tested):
        raise BundleError("RUN_BUNDLE_TESTED_TREE_MISMATCH")
    if raw.get("testedTreeSha") != tested or envelope.get("payload", {}).get("testedTreeSha") != tested or result.get("testedTreeSha") != tested:
        raise BundleError("RUN_BUNDLE_TESTED_TREE_MISMATCH")
    if raw.get("run", {}).get("runId") != run_id or raw.get("run", {}).get("workspaceLocator") != f"golden/{run_id}":
        raise BundleError("RUN_BUNDLE_RUN_ID_MISMATCH")
    if metadata != {
        "schemaVersion": "golden-run-metadata-v1",
        "runId": run_id,
        "testedTreeSha": tested,
        "startedMonotonicNs": metadata.get("startedMonotonicNs"),
        "finishedMonotonicNs": metadata.get("finishedMonotonicNs"),
        "durationMs": metadata.get("durationMs"),
    }:
        raise BundleError("RUN_BUNDLE_METADATA_INVALID")
    start, finish, duration = (metadata.get(key) for key in ("startedMonotonicNs", "finishedMonotonicNs", "durationMs"))
    if not all(isinstance(value, int) and value >= 0 for value in (start, finish, duration)) or finish < start or duration != (finish - start) // 1_000_000 or duration > 300_000:
        raise BundleError("RUN_BUNDLE_METADATA_INVALID")

    projection_sha = _sha(payloads["projection.json"])
    if result.get("status") != "pass" or result.get("commandId") != "golden-clean" or result.get("projectionSha256") != projection_sha or raw.get("semanticProjectionSha256") != projection_sha:
        raise BundleError("RUN_BUNDLE_RESULT_MISMATCH")
    envelope_artifacts = {item.get("locator"): item.get("sha256") for item in envelope.get("payload", {}).get("artifacts", []) if isinstance(item, dict)}
    if envelope_artifacts != {"raw.json": _sha(payloads["raw.json"]), "projection.json": projection_sha}:
        raise BundleError("RUN_BUNDLE_ENVELOPE_GRAPH_MISMATCH")
    result_artifacts = {item.get("locator"): item.get("sha256") for item in result.get("artifacts", []) if isinstance(item, dict)}
    if result_artifacts != {name: _sha(payloads[name]) for name in ("raw.json", "projection.json", "envelope.json")}:
        raise BundleError("RUN_BUNDLE_RESULT_GRAPH_MISMATCH")
    if (result.get("rawLocator"), result.get("projectionLocator"), result.get("envelopeLocator")) != ("raw.json", "projection.json", "envelope.json"):
        raise BundleError("RUN_BUNDLE_RESULT_LOCATOR_MISMATCH")
    return VerifiedBundle(path, run_id, tested, raw, projection, result, metadata, payloads["projection.json"], normalized_raw(raw))
