"""Closed, descriptor-snapshotted promotion-trust Vite binding validator."""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import os
import pathlib
import stat
from typing import Any

import jsonschema

from . import LearningContractError
from .canonical import parse_json
from .schema import MAX_DOCUMENT_BYTES, ROOT, read_regular_bytes


BINDING_SCHEMA_PATH = "learning/contracts/promotion-trust-vite-binding-v1.schema.json"
BINDING_DOCUMENT_PATH = "learning/bindings/vite/promotion-trust-v1.json"
EXPECTED_STAGE_A = {
    "releaseSha": "fecf6bb8e5dfa7cc69f9766f72ac6f5b9301dad9",
    "contractSet": {
        "path": "learning/contracts/learning-contract-set-v1.json",
        "sha256": "92aaf9a573f5d23b5bf5d8d7db1e68150d4b0944f0e6ab6e651b1a3d34408638",
    },
    "promotionManifest": {
        "path": "learning/manifests/promotion-trust-v1.json",
        "sha256": "553b97ed5dc44b77564ae50b1a2211205cbd1a759f3578e5e4dfcefef99044ac",
    },
}
EXPECTED_ISSUE7 = {
    "mergeSha": "1806b6d515f2f7a2ace2be7077af84a745ff221f",
    "adr": {
        "path": "docs/decisions/0005-web-stack.md",
        "sha256": "6e26c48a027d226d8529fda939c07cca99e9f4e1d88cac12708deb98d6fe5eee",
    },
    "package": {
        "path": "spikes/web/candidates/vite/package.json",
        "sha256": "c80eab653ba83702e37dc41d19f18408714863bbb4c5e4d5d7e2da66a7f1b871",
    },
    "lock": {
        "path": "spikes/web/candidates/vite/package-lock.json",
        "sha256": "96feead881be424d4c0d8d4629d7da0312722a3d7c945d08ed071542ea5d443c",
    },
    "lessonContract": {
        "path": "spikes/web/candidates/vite/src/lesson-contract.mjs",
        "sha256": "32b19a5f2e25bd805f340917071c7935a70ae27397b366ca34f1a89054fc35d9",
    },
}
EXPECTED_FIXTURE = {
    "use": "build-time-validation-only",
    "evidence": {
        "path": "tests/fixtures/learning/promotion-trust/evidence-v1.json",
        "sha256": "2f4d90228fa2ea8859a8db630ff587b6cebdc10a0bf6b7db25e46c3dc27181d5",
    },
    "manifest": {
        "path": "tests/fixtures/learning/promotion-trust/manifest.json",
        "sha256": "0a1dcd4023648f52009bfd4dc5d529c00ce66f42cd0e725732b972b0b78df341",
    },
}
EXPECTED_ROWS = [
    ("promotion", "promotion", ["promo_name", "channel"], ["promo_name", "channel"]),
    ("fulfillment", "fulfillment", ["carrier", "region"], ["carrier", "region_name"]),
    ("returns", "returns", ["reason", "category", "region"], ["reason", "category_name", "region_name"]),
    ("dq", "data-quality", ["scenario"], ["scenario"]),
]
EXPECTED_TRUST = {
    "browserRole": "projection-only",
    "serverValidationAuthority": "stage-a-learning-contracts",
    "completionAuthority": "learning-progress-authority-v1",
    "authorize": False,
    "mutate": False,
    "validate": False,
    "complete": False,
    "emitEvidence": False,
}
REFERENCE_ROWS = [
    EXPECTED_STAGE_A["contractSet"], EXPECTED_STAGE_A["promotionManifest"],
    EXPECTED_ISSUE7["adr"], EXPECTED_ISSUE7["package"], EXPECTED_ISSUE7["lock"],
    EXPECTED_ISSUE7["lessonContract"], EXPECTED_FIXTURE["evidence"], EXPECTED_FIXTURE["manifest"],
]


@dataclass(frozen=True)
class ValidatedViteBinding:
    document: dict[str, Any]
    hashes: dict[str, str]


def _same_file(before: os.stat_result, after: os.stat_result) -> bool:
    return (before.st_dev, before.st_ino, stat.S_IFMT(before.st_mode), before.st_nlink) == (
        after.st_dev, after.st_ino, stat.S_IFMT(after.st_mode), after.st_nlink
    )


def _read_at(root_fd: int, relative: str) -> bytes:
    candidate = pathlib.PurePosixPath(relative)
    if candidate.is_absolute() or not candidate.parts or any(
        part in {"", ".", ".."} for part in candidate.parts
    ) or "\\" in relative:
        raise LearningContractError("BINDING_REFERENCE_FORBIDDEN")
    descriptor = os.dup(root_fd)
    nofollow = getattr(os, "O_NOFOLLOW", 0)
    try:
        for part in candidate.parts[:-1]:
            next_fd = os.open(
                part, os.O_RDONLY | os.O_DIRECTORY | os.O_NONBLOCK | nofollow, dir_fd=descriptor
            )
            os.close(descriptor)
            descriptor = next_fd
        name = candidate.parts[-1]
        before = os.stat(name, dir_fd=descriptor, follow_symlinks=False)
        if not stat.S_ISREG(before.st_mode) or before.st_nlink != 1:
            raise LearningContractError("DOCUMENT_SPECIAL_FILE")
        file_fd = os.open(name, os.O_RDONLY | os.O_NONBLOCK | nofollow, dir_fd=descriptor)
        try:
            after = os.fstat(file_fd)
            if not _same_file(before, after) or after.st_size > MAX_DOCUMENT_BYTES:
                raise LearningContractError("DOCUMENT_SPECIAL_FILE")
            chunks: list[bytes] = []
            remaining = MAX_DOCUMENT_BYTES + 1
            while remaining:
                chunk = os.read(file_fd, min(65536, remaining))
                if not chunk:
                    break
                chunks.append(chunk)
                remaining -= len(chunk)
            raw = b"".join(chunks)
            if len(raw) > MAX_DOCUMENT_BYTES:
                raise LearningContractError("DOCUMENT_TOO_LARGE")
            return raw
        finally:
            os.close(file_fd)
    except LearningContractError:
        raise
    except OSError as exc:
        raise LearningContractError("DOCUMENT_SPECIAL_FILE") from exc
    finally:
        os.close(descriptor)


def _capture_fixed() -> dict[str, bytes]:
    nofollow = getattr(os, "O_NOFOLLOW", 0)
    try:
        root_fd = os.open(ROOT, os.O_RDONLY | os.O_DIRECTORY | os.O_NONBLOCK | nofollow)
    except OSError as exc:
        raise LearningContractError("BINDING_ROOT_INVALID") from exc
    paths = [BINDING_SCHEMA_PATH, *(row["path"] for row in REFERENCE_ROWS)]
    try:
        return {path: _read_at(root_fd, path) for path in paths}
    finally:
        os.close(root_fd)


def _precheck(value: Any) -> None:
    if not isinstance(value, dict):
        raise LearningContractError("BINDING_SCHEMA_INVALID")
    if value.get("schemaVersion") not in {None, "promotion-trust-vite-binding-v1"}:
        raise LearningContractError("BINDING_VERSION_UNSUPPORTED")
    keys = set(value)
    if keys & {"records", "rawRecords", "payload", "data"}:
        raise LearningContractError("BINDING_DATA_PAYLOAD_FORBIDDEN")
    if keys & {"default", "transform", "operations", "schema", "properties", "canonicalizer"}:
        raise LearningContractError("BINDING_CONTRACT_FORK_FORBIDDEN")
    if keys & {"url", "uri", "command", "template", "expression"}:
        raise LearningContractError("BINDING_REFERENCE_FORBIDDEN")
    trust = value.get("trustBoundary")
    if isinstance(trust, dict) and trust != EXPECTED_TRUST:
        raise LearningContractError("BINDING_AUTHORITY_FORBIDDEN")
    rows = value.get("grainBindings")
    if isinstance(rows, list) and (
        len(rows) != 4
        or any(not isinstance(row, dict) for row in rows)
        or [(row.get("stageAGrain"), row.get("viteGrain")) for row in rows]
        != [(row[0], row[1]) for row in EXPECTED_ROWS]
    ):
        raise LearningContractError("BINDING_GRAIN_MISMATCH")
    for section in ("stageA", "issue7", "fixture"):
        child = value.get(section)
        if not isinstance(child, dict):
            continue
        for reference in child.values():
            if not isinstance(reference, dict) or "path" not in reference:
                continue
            path = reference["path"]
            if not isinstance(path, str) or path.startswith("/") or "\\" in path or ".." in pathlib.PurePosixPath(path).parts or "://" in path:
                raise LearningContractError("BINDING_REFERENCE_FORBIDDEN")


def _validate_schema(value: dict[str, Any], raw: bytes) -> None:
    try:
        schema = parse_json(raw)
        jsonschema.Draft202012Validator.check_schema(schema)
        jsonschema.Draft202012Validator(schema).validate(value)
    except (jsonschema.SchemaError, jsonschema.ValidationError, LearningContractError) as exc:
        raise LearningContractError("BINDING_SCHEMA_INVALID") from exc


def _validate_semantics(value: dict[str, Any], captured: dict[str, bytes]) -> None:
    if value.get("stageA") != EXPECTED_STAGE_A or value.get("issue7") != EXPECTED_ISSUE7 or value.get("fixture") != EXPECTED_FIXTURE:
        declared = [
            reference for section in ("stageA", "issue7", "fixture")
            for reference in (value.get(section, {}) or {}).values()
            if isinstance(reference, dict) and "path" in reference and "sha256" in reference
        ]
        if any(reference.get("path") != expected["path"] for reference, expected in zip(declared, REFERENCE_ROWS)):
            raise LearningContractError("BINDING_REFERENCE_FORBIDDEN")
        raise LearningContractError("BINDING_DEPENDENCY_HASH_MISMATCH")
    for reference in REFERENCE_ROWS:
        raw = captured[reference["path"]]
        if hashlib.sha256(raw).hexdigest() != reference["sha256"]:
            raise LearningContractError("BINDING_DEPENDENCY_HASH_MISMATCH")
    manifest = parse_json(captured[EXPECTED_STAGE_A["promotionManifest"]["path"]])
    evidence = parse_json(captured[EXPECTED_FIXTURE["evidence"]["path"]])
    expected_stage = [(row["grain"], row["keys"]) for row in manifest["sources"]]
    expected_vite_keys = [row["order"] for row in evidence["sources"]]
    rows = value["grainBindings"]
    if len(rows) != 4 or [(row["stageAGrain"], row["viteGrain"]) for row in rows] != [
        (row[0], row[1]) for row in EXPECTED_ROWS
    ]:
        raise LearningContractError("BINDING_GRAIN_MISMATCH")
    if [(row["stageAGrain"], row["stageAKeys"]) for row in rows] != expected_stage:
        raise LearningContractError("BINDING_STAGE_A_KEY_MISMATCH")
    if [row["viteKeys"] for row in rows] != expected_vite_keys:
        raise LearningContractError("BINDING_FIXTURE_KEY_MISMATCH")
    vite_text = captured[EXPECTED_ISSUE7["lessonContract"]["path"]].decode("utf-8", "strict")
    for grain, _, _, keys in EXPECTED_ROWS:
        vite_grain = dict((row[0], row[1]) for row in EXPECTED_ROWS)[grain]
        if f"id: '{vite_grain}'" not in vite_text or " × ".join(keys) not in vite_text:
            raise LearningContractError("BINDING_FIXTURE_KEY_MISMATCH")
    for row in rows:
        aliases = row["aliases"]
        if any(
            alias["kind"] == "identifier-alias"
            and alias["from"] in row["viteKeys"]
            and alias["to"] in row["stageAKeys"]
            for alias in aliases
        ):
            raise LearningContractError("BINDING_ALIAS_CYCLIC")
        sources = [alias["from"] for alias in aliases]
        targets = [alias["to"] for alias in aliases]
        if sources != row["stageAKeys"] or targets != row["viteKeys"] or len(targets) != len(set(targets)):
            raise LearningContractError("BINDING_ALIAS_NOT_BIJECTIVE")
        for alias in aliases:
            expected_kind = "identity" if alias["from"] == alias["to"] else "identifier-alias"
            if alias["kind"] != expected_kind:
                raise LearningContractError("BINDING_ALIAS_NOT_BIJECTIVE")
    expected_aliases = [("region", "region_name"), ("category", "category_name"), ("region", "region_name")]
    actual_aliases = [
        (alias["from"], alias["to"]) for row in rows for alias in row["aliases"]
        if alias["kind"] == "identifier-alias"
    ]
    if actual_aliases != expected_aliases or value["decision"] != "insufficient-evidence/no-common-grain":
        raise LearningContractError("BINDING_ALIAS_NOT_BIJECTIVE")
    for source, row in zip(evidence["sources"], rows):
        for record in source["records"]:
            if any(key not in record for key in row["viteKeys"]):
                raise LearningContractError("BINDING_FIXTURE_KEY_MISMATCH")


def _validate(value: Any, document_raw: bytes, captured: dict[str, bytes]) -> ValidatedViteBinding:
    _precheck(value)
    _validate_schema(value, captured[BINDING_SCHEMA_PATH])
    _validate_semantics(value, captured)
    hashes = {
        BINDING_DOCUMENT_PATH: hashlib.sha256(document_raw).hexdigest(),
        **{path: hashlib.sha256(raw).hexdigest() for path, raw in captured.items()},
    }
    return ValidatedViteBinding(value, hashes)


def validate_vite_binding_document(value: dict[str, Any]) -> ValidatedViteBinding:
    captured = _capture_fixed()
    raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return _validate(value, raw, captured)


def validate_vite_binding_path(path: pathlib.Path) -> ValidatedViteBinding:
    try:
        raw = read_regular_bytes(path)
    except LearningContractError as exc:
        if exc.code in {"DOCUMENT_SPECIAL_FILE", "DOCUMENT_UNREADABLE"}:
            raise LearningContractError("BINDING_DOCUMENT_SPECIAL_FILE") from exc
        raise
    return _validate(parse_json(raw), raw, _capture_fixed())


def validate_shipped_vite_binding() -> ValidatedViteBinding:
    captured = _capture_fixed()
    nofollow = getattr(os, "O_NOFOLLOW", 0)
    try:
        root_fd = os.open(ROOT, os.O_RDONLY | os.O_DIRECTORY | os.O_NONBLOCK | nofollow)
        try:
            raw = _read_at(root_fd, BINDING_DOCUMENT_PATH)
        finally:
            os.close(root_fd)
    except LearningContractError as exc:
        if exc.code in {"DOCUMENT_SPECIAL_FILE", "DOCUMENT_UNREADABLE"}:
            raise LearningContractError("VITE_BINDING_REQUIRED") from exc
        raise
    return _validate(parse_json(raw), raw, captured)
