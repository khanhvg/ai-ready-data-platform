#!/usr/bin/env python3
"""Private, descriptor-bound storage used by issue #6 fitness commands."""

from __future__ import annotations

import json
import os
import pathlib
import re
import secrets
import stat
from typing import Any


ROOT = pathlib.Path(__file__).resolve().parents[2]
MARKER = ".golden-owner.json"
SAFE_COMPONENT = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")


class WorkspaceError(RuntimeError):
    """A typed refusal to operate on state that is not proven issue-owned."""


def validate_relative_path(value: str) -> tuple[str, ...]:
    if not isinstance(value, str) or not value or "\x00" in value or "\\" in value:
        raise WorkspaceError("WORKSPACE_PATH_INVALID")
    path = pathlib.PurePosixPath(value)
    if path.is_absolute() or any(part in {"", ".", ".."} for part in path.parts):
        raise WorkspaceError("WORKSPACE_PATH_INVALID")
    if any(not SAFE_COMPONENT.fullmatch(part) for part in path.parts):
        raise WorkspaceError("WORKSPACE_PATH_INVALID")
    return path.parts


def open_private_parent(path: pathlib.Path) -> int:
    try:
        before = path.lstat()
    except OSError as exc:
        raise WorkspaceError("WORKSPACE_PARENT_INVALID") from exc
    if stat.S_ISLNK(before.st_mode):
        raise WorkspaceError("WORKSPACE_LINK_REFUSED")
    if not stat.S_ISDIR(before.st_mode):
        raise WorkspaceError("WORKSPACE_PARENT_INVALID")
    fd = os.open(path, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    after = os.fstat(fd)
    if (before.st_dev, before.st_ino) != (after.st_dev, after.st_ino):
        os.close(fd)
        raise WorkspaceError("WORKSPACE_IDENTITY_CHANGED")
    if stat.S_IMODE(after.st_mode) & 0o077:
        os.close(fd)
        raise WorkspaceError("WORKSPACE_PERMISSIONS_UNSAFE")
    return fd


def _write_exclusive(parent_fd: int, name: str, payload: bytes) -> None:
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW
    fd = os.open(name, flags, 0o600, dir_fd=parent_fd)
    try:
        os.write(fd, payload)
        os.fsync(fd)
        info = os.fstat(fd)
        if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1:
            raise WorkspaceError("WORKSPACE_ENTRY_UNSAFE")
    finally:
        os.close(fd)


class OwnedWorkspace:
    def __init__(self, path: pathlib.Path, parent_fd: int, run_fd: int, marker: dict[str, Any]):
        self.path = path
        self.parent_fd = parent_fd
        self.run_fd = run_fd
        self.marker = marker

    def close(self) -> None:
        for name in ("run_fd", "parent_fd"):
            fd = getattr(self, name, -1)
            if fd >= 0:
                os.close(fd)
                setattr(self, name, -1)


def allocate_at_for_test(parent: pathlib.Path, run_id: str, purpose: str) -> OwnedWorkspace:
    validate_relative_path(run_id)
    validate_relative_path(purpose)
    parent_fd = open_private_parent(parent)
    try:
        os.mkdir(run_id, 0o700, dir_fd=parent_fd)
    except FileExistsError as exc:
        os.close(parent_fd)
        raise WorkspaceError("WORKSPACE_FOREIGN_DESTINATION") from exc
    try:
        run_fd = os.open(run_id, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=parent_fd)
        info = os.fstat(run_fd)
        marker = {
            "schemaVersion": "golden-owner-v1",
            "nonce": secrets.token_hex(32),
            "runId": run_id,
            "purpose": purpose,
            "device": info.st_dev,
            "inode": info.st_ino,
        }
        _write_exclusive(
            run_fd,
            MARKER,
            (json.dumps(marker, sort_keys=True, separators=(",", ":")) + "\n").encode(),
        )
        os.fsync(run_fd)
        return OwnedWorkspace(parent / run_id, parent_fd, run_fd, marker)
    except BaseException:
        os.close(parent_fd)
        raise


def allocate(family: str, purpose: str) -> OwnedWorkspace:
    parts = validate_relative_path(family)
    if parts not in {("workspaces", "golden"), ("evidence", "golden")}:
        raise WorkspaceError("WORKSPACE_FAMILY_INVALID")
    old_umask = os.umask(0o077)
    try:
        run_id = secrets.token_hex(16)
        return allocate_family(parts, purpose, run_id)
    finally:
        os.umask(old_umask)


def _open_family(parts: tuple[str, ...]) -> tuple[pathlib.Path, int]:
    if not parts or any(not SAFE_COMPONENT.fullmatch(part) for part in parts):
        raise WorkspaceError("WORKSPACE_FAMILY_INVALID")
    current_fd = os.open(ROOT, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    current_path = ROOT
    try:
        for part in (".artifacts", *parts):
            try:
                os.mkdir(part, 0o700, dir_fd=current_fd)
            except FileExistsError:
                pass
            next_fd = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=current_fd)
            info = os.fstat(next_fd)
            if not stat.S_ISDIR(info.st_mode) or stat.S_IMODE(info.st_mode) & 0o077:
                os.close(next_fd)
                raise WorkspaceError("WORKSPACE_PERMISSIONS_UNSAFE")
            os.close(current_fd)
            current_fd = next_fd
            current_path = current_path / part
        return current_path, current_fd
    except BaseException:
        os.close(current_fd)
        raise


def allocate_family(parts: tuple[str, ...], purpose: str, run_id: str | None = None) -> OwnedWorkspace:
    validate_relative_path(purpose)
    run_id = run_id or secrets.token_hex(16)
    validate_relative_path(run_id)
    parent, parent_fd = _open_family(parts)
    try:
        os.mkdir(run_id, 0o700, dir_fd=parent_fd)
    except FileExistsError as exc:
        os.close(parent_fd)
        raise WorkspaceError("WORKSPACE_FOREIGN_DESTINATION") from exc
    run_fd = os.open(run_id, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=parent_fd)
    info = os.fstat(run_fd)
    marker = {"schemaVersion":"golden-owner-v1","nonce":secrets.token_hex(32),"runId":run_id,"purpose":purpose,"device":info.st_dev,"inode":info.st_ino}
    _write_exclusive(run_fd, MARKER, (json.dumps(marker,sort_keys=True,separators=(",",":"))+"\n").encode())
    os.fsync(run_fd)
    return OwnedWorkspace(parent/run_id,parent_fd,run_fd,marker)


class PublicationLease:
    def __init__(self, parent: pathlib.Path, fd: int, identity: tuple[int, int]):
        self.parent = parent
        self.fd = fd
        self.identity = identity

    def close(self) -> None:
        if self.fd < 0:
            return
        current = os.fstat(self.fd)
        observed = self.parent.joinpath(".publication.lease").lstat()
        if (current.st_dev, current.st_ino) != self.identity or self.identity != (observed.st_dev, observed.st_ino):
            raise WorkspaceError("PUBLICATION_LEASE_IDENTITY_CHANGED")
        os.close(self.fd)
        self.fd = -1
        parent_fd = open_private_parent(self.parent)
        try:
            os.unlink(".publication.lease", dir_fd=parent_fd)
            os.fsync(parent_fd)
        finally:
            os.close(parent_fd)


def acquire_publication_lease(parent: pathlib.Path, owner_nonce: str) -> PublicationLease:
    validate_relative_path(owner_nonce)
    parent_fd = open_private_parent(parent)
    try:
        fd = os.open(
            ".publication.lease",
            os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
            0o600,
            dir_fd=parent_fd,
        )
        os.write(fd, (owner_nonce + "\n").encode())
        os.fsync(fd)
        info = os.fstat(fd)
        return PublicationLease(parent, fd, (info.st_dev, info.st_ino))
    except FileExistsError as exc:
        raise WorkspaceError("PUBLICATION_LEASE_HELD") from exc
    finally:
        os.close(parent_fd)


def atomic_write(parent_fd: int, name: str, payload: bytes) -> None:
    validate_relative_path(name)
    temporary = f".{name}.{secrets.token_hex(12)}.tmp"
    _write_exclusive(parent_fd, temporary, payload)
    try:
        os.replace(temporary, name, src_dir_fd=parent_fd, dst_dir_fd=parent_fd)
        os.fsync(parent_fd)
    except BaseException:
        try:
            os.unlink(temporary, dir_fd=parent_fd)
        except FileNotFoundError:
            pass
        raise
