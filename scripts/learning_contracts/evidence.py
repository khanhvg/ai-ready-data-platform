"""Strict learner and fitness evidence integrity checks."""
from __future__ import annotations

import hashlib
import json
import os
import pathlib
import re
import stat
from typing import Any

from scripts.golden.canonical import dumps

SAFE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")
FORBIDDEN_FIELDS = {"rawSql", "shell", "command", "environment", "networkDestination", "absolutePath"}


def valid_locator(value: str, *, entry_type: str = "regular", link_count: int = 1) -> bool:
    if not isinstance(value, str) or not value or "\\" in value or "\x00" in value or "://" in value:
        return False
    path = pathlib.PurePosixPath(value)
    if path.is_absolute() or any(part in {"", ".", "..", ".ssh", "Users", "home", "private"} for part in path.parts):
        return False
    return entry_type == "regular" and link_count == 1 and all(SAFE.fullmatch(part) for part in path.parts)


def _contains_sensitive(value: Any) -> bool:
    if isinstance(value, str):
        lowered = value.lower()
        return any(marker in lowered for marker in ("token-private-canary", "begin private key", "pii-canary"))
    if isinstance(value, dict):
        return any(_contains_sensitive(key) or _contains_sensitive(child) for key, child in value.items())
    if isinstance(value, list):
        return any(_contains_sensitive(child) for child in value)
    return False


def code(value: dict[str, Any]) -> str:
    if "payload" in value and "payloadSha256" in value:
        actual = hashlib.sha256(dumps(value["payload"])).hexdigest()
        if actual != value["payloadSha256"]:
            return "EVIDENCE_PAYLOAD_HASH_MISMATCH"
    if "artifact" in value and value["artifact"].get("sha256") != value.get("actualSha256"):
        return "EVIDENCE_ARTIFACT_HASH_MISMATCH"
    if "locator" in value and not valid_locator(value["locator"], entry_type=value.get("entryType", "regular"), link_count=value.get("linkCount", 1)):
        return "EVIDENCE_LOCATOR_INVALID"
    if "verifierSha256" in value and value["verifierSha256"] != value.get("actualVerifierSha256"):
        return "EVIDENCE_VERIFIER_HASH_MISMATCH"
    if "indexedPayloadSha256" in value and value["indexedPayloadSha256"] != value.get("payloadSha256"):
        return "EVIDENCE_REPLAY_CONFLICT"
    if "dependencyMergeShas" in value and not value["dependencyMergeShas"]:
        return "EVIDENCE_PROVENANCE_INCOMPLETE"
    if value.get("testedTreeSha") == "self-containing-identity":
        return "EVIDENCE_RECURSIVE_IDENTITY"
    if _contains_sensitive(value):
        return "EVIDENCE_SENSITIVE_CONTENT"
    if FORBIDDEN_FIELDS.intersection(value):
        return "CONTRACT_INJECTION_FIELD_FORBIDDEN"
    return "OK"


def read_descriptor_bound(root: pathlib.Path, locator: str, limit: int = 2 * 1024 * 1024) -> bytes:
    if not valid_locator(locator):
        raise ValueError("EVIDENCE_LOCATOR_INVALID")
    before = root.lstat()
    if not stat.S_ISDIR(before.st_mode) or stat.S_ISLNK(before.st_mode):
        raise ValueError("EVIDENCE_ROOT_INVALID")
    current = os.open(root, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        for component in pathlib.PurePosixPath(locator).parts[:-1]:
            following = os.open(component, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=current)
            os.close(current); current = following
        fd = os.open(pathlib.PurePosixPath(locator).parts[-1], os.O_RDONLY | os.O_NOFOLLOW, dir_fd=current)
        try:
            info = os.fstat(fd)
            if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1 or info.st_size > limit:
                raise ValueError("EVIDENCE_LOCATOR_INVALID")
            data = os.read(fd, limit + 1)
            if len(data) > limit:
                raise ValueError("EVIDENCE_SIZE_LIMIT")
            return data
        finally:
            os.close(fd)
    except OSError as exc:
        raise ValueError("EVIDENCE_LOCATOR_INVALID") from exc
    finally:
        os.close(current)


def verify_result_bytes(raw: bytes) -> dict[str, Any]:
    value = json.loads(raw)
    claimed = value.pop("payloadSha256", None)
    actual = hashlib.sha256(dumps(value)).hexdigest()
    if claimed != actual:
        raise ValueError("EVIDENCE_PAYLOAD_HASH_MISMATCH")
    value["payloadSha256"] = claimed
    return value
