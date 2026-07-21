"""Descriptor-bound evidence locator and integrity checks."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import PurePosixPath
import re
import stat
import secrets

from .canonical import ContractError, dumps
from .schema import ROOT

SAFE = re.compile(r"^[A-Za-z0-9._-]{1,128}$")
SENSITIVE = re.compile(rb"(?i)(BEGIN [A-Z ]*PRIVATE KEY|aws_secret_access_key|authorization:\s*bearer|password\s*=|/Users/|/home/)")


def components(locator: str) -> tuple[str, ...]:
    if not isinstance(locator, str) or not locator or "\x00" in locator or "\\" in locator or "://" in locator:
        raise ContractError("EVIDENCE_LOCATOR_INVALID")
    path = PurePosixPath(locator)
    if path.is_absolute() or any(part in {"", ".", "..", "~"} or not SAFE.fullmatch(part) for part in path.parts):
        raise ContractError("EVIDENCE_LOCATOR_INVALID")
    return path.parts


def read_regular(locator: str, limit: int = 2 * 1024 * 1024) -> bytes:
    parts = components(locator)
    fd = os.open(ROOT, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        for index, part in enumerate(parts):
            last = index == len(parts) - 1
            flags = os.O_RDONLY | os.O_NOFOLLOW
            if not last: flags |= os.O_DIRECTORY
            else: flags |= os.O_NONBLOCK
            next_fd = os.open(part, flags, dir_fd=fd)
            os.close(fd); fd = next_fd
        info = os.fstat(fd)
        if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1 or info.st_size > limit:
            raise ContractError("EVIDENCE_LOCATOR_INVALID")
        chunks: list[bytes] = []
        total = 0
        while True:
            chunk = os.read(fd, min(65536, limit + 1 - total))
            if not chunk: break
            chunks.append(chunk); total += len(chunk)
            if total > limit: raise ContractError("EVIDENCE_SIZE_LIMIT")
        return b"".join(chunks)
    except OSError as exc:
        raise ContractError("EVIDENCE_LOCATOR_INVALID") from exc
    finally:
        try: os.close(fd)
        except OSError: pass


def verify_locator(locator: str, declared_size: int | None = None, declared_sha256: str | None = None) -> str:
    raw = read_regular(locator)
    if SENSITIVE.search(raw): raise ContractError("EVIDENCE_SENSITIVE_CONTENT")
    digest = hashlib.sha256(raw).hexdigest()
    if declared_size is not None and declared_size != len(raw): raise ContractError("EVIDENCE_ARTIFACT_HASH_MISMATCH")
    if declared_sha256 is not None and declared_sha256 != digest: raise ContractError("EVIDENCE_ARTIFACT_HASH_MISMATCH")
    return digest


def payload_sha256(document: dict[str, object], digest_field: str = "payloadSha256") -> str:
    payload = {key: value for key, value in document.items() if key != digest_field}
    return hashlib.sha256(dumps(payload)).hexdigest()


def rehearse_s3() -> None:
    """Exercise descriptor, sensitive-content and closed cleanup refusals."""
    parent = ROOT / ".artifacts" / "workspaces" / "learning-contracts"
    parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    run_id = secrets.token_hex(16)
    root = parent / run_id
    root.mkdir(mode=0o700)
    info = root.stat()
    nonce = secrets.token_hex(32)
    marker = root / ".learning-contract-owner.json"
    marker.write_text(json.dumps({"runId": run_id, "nonce": nonce, "device": info.st_dev, "inode": info.st_ino, "files": ["regular", "link", "hard", "fifo"]}) + "\n")
    regular = root / "regular"
    regular.write_bytes(b"safe-evidence")
    locator = regular.relative_to(ROOT).as_posix()
    verify_locator(locator, len(b"safe-evidence"), hashlib.sha256(b"safe-evidence").hexdigest())
    regular.write_bytes(b"Authorization: Bearer private-canary")
    try: verify_locator(locator)
    except ContractError as exc:
        if exc.code != "EVIDENCE_SENSITIVE_CONTENT": raise
    else: raise AssertionError("sensitive evidence accepted")
    regular.write_bytes(b"safe-evidence")
    (root / "link").symlink_to(regular)
    os.link(regular, root / "hard")
    os.mkfifo(root / "fifo", 0o600)
    for name in ("link", "hard", "fifo"):
        try: verify_locator((root / name).relative_to(ROOT).as_posix())
        except ContractError as exc:
            if exc.code != "EVIDENCE_LOCATOR_INVALID": raise
        else: raise AssertionError(f"unsafe evidence entry accepted: {name}")
    try: components("../outside")
    except ContractError: pass
    else: raise AssertionError("traversal locator accepted")
    current = root.stat()
    recorded = json.loads(marker.read_text())
    if (current.st_dev, current.st_ino, recorded["nonce"]) != (info.st_dev, info.st_ino, nonce):
        raise ContractError("ROLLBACK_SCOPE_UNOWNED")
    for name in ("link", "hard", "fifo", "regular", marker.name):
        (root / name).unlink()
    root.rmdir()
