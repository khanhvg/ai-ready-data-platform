"""Schema-, provenance-, and descriptor-bound evidence verification."""

from __future__ import annotations

import pathlib
import hashlib
import os
import stat
import subprocess
from typing import Any

from .canonical import canonical_bytes
from .references import resolve_reference
from .schema import LearningContractError, validate_document


def verify_evidence(
    value: dict[str, Any],
    *,
    root: pathlib.Path,
    seen_run_ids: set[str] | None = None,
    authoritative_root: pathlib.Path | None = None,
    replay_root: pathlib.Path | None = None,
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
    if authoritative_root is not None:
        for item in [*value["contractHashes"], *value["fixtureHashes"]]:
            try:
                resolve_reference(authoritative_root, item["path"], item["sha256"])
            except LearningContractError as exc:
                raise LearningContractError("EVIDENCE_PROVENANCE_TAMPER") from exc
        verifier_path = authoritative_root / "scripts/learning_contracts/check.py"
        if value["verifier"] != {
            "id": "learning-contracts-v1",
            "sha256": hashlib.sha256(verifier_path.read_bytes()).hexdigest(),
        }:
            raise LearningContractError("EVIDENCE_PROVENANCE_TAMPER")
        if value["officialGoldenMainSha"] != "24be3b34c6b0fcdbd07c5800dcab349054e34713" or value["dependencyMergeShas"] != [value["officialGoldenMainSha"]]:
            raise LearningContractError("EVIDENCE_PROVENANCE_TAMPER")
        result = subprocess.run(
            ["git", "cat-file", "-e", f"{value['inputGitSha']}^{{commit}}"],
            cwd=authoritative_root,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        )
        if result.returncode != 0:
            raise LearningContractError("EVIDENCE_PROVENANCE_TAMPER")
    for item in value["artifacts"]:
        try:
            raw = resolve_reference(root, item["locator"], item["sha256"])
        except LearningContractError as exc:
            raise LearningContractError("EVIDENCE_ARTIFACT_TAMPER") from exc
        if len(raw) != item["size"]:
            raise LearningContractError("EVIDENCE_ARTIFACT_TAMPER")
    if seen_run_ids is not None:
        seen_run_ids.add(run_id)
    if replay_root is not None:
        replay_root.mkdir(mode=0o700, parents=True, exist_ok=True)
        info = replay_root.lstat()
        if not stat.S_ISDIR(info.st_mode) or stat.S_ISLNK(info.st_mode):
            raise LearningContractError("EVIDENCE_REPLAY_STORE_UNSAFE")
        token = hashlib.sha256(run_id.encode("utf-8")).hexdigest()
        try:
            descriptor = os.open(replay_root / token, os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0), 0o600)
        except FileExistsError as exc:
            raise LearningContractError("EVIDENCE_REPLAY") from exc
        else:
            os.write(descriptor, (run_id + "\n").encode("utf-8"))
            os.fsync(descriptor)
            os.close(descriptor)


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
