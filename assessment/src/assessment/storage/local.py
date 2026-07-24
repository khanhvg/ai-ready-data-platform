"""Atomic local implementation of the authoritative engagement-folder store."""

from __future__ import annotations

import ctypes
import errno
import fcntl
import hashlib
import json
import os
import stat
import sys
import uuid
from collections.abc import Iterator, Mapping
from contextlib import contextmanager
from pathlib import Path
from typing import Any, BinaryIO

from assessment.domain.errors import (
    ConcurrentWriteError,
    EngagementExistsError,
    EngagementNotFoundError,
    InvalidPathError,
)
from assessment.domain.models import Engagement, validate_identifier, validate_relative_posix_path

IGNORED_RUNTIME_NAMES = {".engagement.lock", ".DS_Store"}


def canonical_json(document: Any) -> bytes:
    return (
        json.dumps(document, ensure_ascii=False, indent=2, sort_keys=True, allow_nan=False) + "\n"
    ).encode("utf-8")


def sha256_bytes(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def fsync_directory(path: Path) -> bool:
    """Persist a directory entry where the platform supports directory fsync."""
    flags = os.O_RDONLY
    if hasattr(os, "O_DIRECTORY"):
        flags |= os.O_DIRECTORY
    try:
        descriptor = os.open(path, flags)
    except OSError as error:
        if error.errno in {errno.EINVAL, errno.ENOTSUP, errno.EACCES}:
            return False
        raise
    try:
        os.fsync(descriptor)
        return True
    except OSError as error:
        if error.errno in {errno.EINVAL, errno.ENOTSUP, errno.EROFS}:
            return False
        raise
    finally:
        os.close(descriptor)


def atomic_write(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.tmp-{uuid.uuid4().hex}")
    try:
        with temporary.open("xb") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.chmod(temporary, 0o600)
        os.replace(temporary, path)
        fsync_directory(path.parent)
    finally:
        temporary.unlink(missing_ok=True)


def _directory_flags() -> int:
    flags = os.O_RDONLY
    if hasattr(os, "O_DIRECTORY"):
        flags |= os.O_DIRECTORY
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    return flags


def _fsync_directory_descriptor(descriptor: int) -> bool:
    try:
        os.fsync(descriptor)
        return True
    except OSError as error:
        if error.errno in {errno.EINVAL, errno.ENOTSUP, errno.EROFS}:
            return False
        raise


def _open_child_directory(parent_descriptor: int, name: str, *, create: bool) -> int:
    try:
        return os.open(name, _directory_flags(), dir_fd=parent_descriptor)
    except FileNotFoundError:
        if not create:
            raise
    except OSError as error:
        raise InvalidPathError(
            f"directory component is not a safe local directory: {name}"
        ) from error
    try:
        os.mkdir(name, 0o700, dir_fd=parent_descriptor)
    except FileExistsError:
        pass
    try:
        return os.open(name, _directory_flags(), dir_fd=parent_descriptor)
    except OSError as error:
        raise InvalidPathError(
            f"directory component is not a safe local directory: {name}"
        ) from error


def atomic_write_at(root_descriptor: int, key: str, content: bytes) -> None:
    """Atomically write below a bound directory without following path symlinks."""
    normalized = validate_relative_posix_path(key)
    parts = normalized.split("/")
    parent_descriptor = os.dup(root_descriptor)
    temporary_name = f".{parts[-1]}.tmp-{uuid.uuid4().hex}"
    try:
        for part in parts[:-1]:
            child_descriptor = _open_child_directory(
                parent_descriptor,
                part,
                create=True,
            )
            os.close(parent_descriptor)
            parent_descriptor = child_descriptor
        flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
        if hasattr(os, "O_NOFOLLOW"):
            flags |= os.O_NOFOLLOW
        file_descriptor = os.open(
            temporary_name,
            flags,
            0o600,
            dir_fd=parent_descriptor,
        )
        try:
            with os.fdopen(file_descriptor, "wb", closefd=False) as handle:
                handle.write(content)
                handle.flush()
                os.fsync(handle.fileno())
        finally:
            os.close(file_descriptor)
        os.rename(
            temporary_name,
            parts[-1],
            src_dir_fd=parent_descriptor,
            dst_dir_fd=parent_descriptor,
        )
        _fsync_directory_descriptor(parent_descriptor)
    finally:
        try:
            os.unlink(temporary_name, dir_fd=parent_descriptor)
        except FileNotFoundError:
            pass
        os.close(parent_descriptor)


def _rename_directory_no_replace_at(
    source_parent: int,
    source_name: str,
    destination_parent: int,
    destination_name: str,
) -> None:
    libc = ctypes.CDLL(None, use_errno=True)
    if sys.platform == "darwin":
        rename = libc.renameatx_np
        rename.argtypes = [
            ctypes.c_int,
            ctypes.c_char_p,
            ctypes.c_int,
            ctypes.c_char_p,
            ctypes.c_uint,
        ]
        rename.restype = ctypes.c_int
        result = rename(
            source_parent,
            os.fsencode(source_name),
            destination_parent,
            os.fsencode(destination_name),
            0x00000004,
        )
    elif sys.platform.startswith("linux") and hasattr(libc, "renameat2"):
        rename = libc.renameat2
        rename.argtypes = [
            ctypes.c_int,
            ctypes.c_char_p,
            ctypes.c_int,
            ctypes.c_char_p,
            ctypes.c_uint,
        ]
        rename.restype = ctypes.c_int
        result = rename(
            source_parent,
            os.fsencode(source_name),
            destination_parent,
            os.fsencode(destination_name),
            0x00000001,
        )
    else:
        raise OSError(errno.ENOTSUP, "atomic no-replace directory promotion is unsupported")
    if result != 0:
        error_number = ctypes.get_errno()
        raise OSError(error_number, os.strerror(error_number), destination_name)


def _open_absolute_directory(path: Path) -> int:
    absolute = path.absolute()
    descriptor = os.open(absolute.anchor, _directory_flags())
    try:
        for part in absolute.parts[1:]:
            child_descriptor = _open_child_directory(
                descriptor,
                part,
                create=False,
            )
            os.close(descriptor)
            descriptor = child_descriptor
    except Exception:
        os.close(descriptor)
        raise
    return descriptor


def _ensure_absolute_directory(path: Path) -> int:
    absolute = path.absolute()
    descriptor = os.open(absolute.anchor, _directory_flags())
    try:
        for part in absolute.parts[1:]:
            child_descriptor = _open_child_directory(
                descriptor,
                part,
                create=True,
            )
            os.close(descriptor)
            descriptor = child_descriptor
    except Exception:
        os.close(descriptor)
        raise
    return descriptor


def promote_directory_no_replace(source: Path, destination: Path) -> None:
    """Atomically promote a directory while preserving a concurrent destination."""
    source_parent_path = source.parent.absolute()
    destination_parent_path = destination.parent.absolute()
    source_parent = _open_absolute_directory(source_parent_path)
    try:
        destination_parent = (
            os.dup(source_parent)
            if source_parent_path == destination_parent_path
            else _open_absolute_directory(destination_parent_path)
        )
        try:
            _rename_directory_no_replace_at(
                source_parent,
                source.name,
                destination_parent,
                destination.name,
            )
            _fsync_directory_descriptor(destination_parent)
        finally:
            os.close(destination_parent)
    finally:
        os.close(source_parent)


def _read_file_at(parent_descriptor: int, name: str) -> bytes:
    flags = os.O_RDONLY
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    descriptor = os.open(name, flags, dir_fd=parent_descriptor)
    try:
        metadata = os.fstat(descriptor)
        if not stat.S_ISREG(metadata.st_mode):
            raise InvalidPathError(f"engagement entry is not a regular file: {name}")
        with os.fdopen(descriptor, "rb", closefd=False) as handle:
            return handle.read()
    finally:
        os.close(descriptor)


def _read_relative_at(root_descriptor: int, key: str) -> bytes:
    normalized = validate_relative_posix_path(key)
    parts = normalized.split("/")
    parent_descriptor = os.dup(root_descriptor)
    try:
        for part in parts[:-1]:
            child_descriptor = _open_child_directory(
                parent_descriptor,
                part,
                create=False,
            )
            os.close(parent_descriptor)
            parent_descriptor = child_descriptor
        return _read_file_at(parent_descriptor, parts[-1])
    finally:
        os.close(parent_descriptor)


def _recover_temporary_files_at(directory_descriptor: int) -> None:
    with os.scandir(directory_descriptor) as entries:
        for entry in sorted(entries, key=lambda item: item.name):
            metadata = entry.stat(follow_symlinks=False)
            if stat.S_ISLNK(metadata.st_mode):
                continue
            if stat.S_ISDIR(metadata.st_mode):
                child_descriptor = _open_child_directory(
                    directory_descriptor,
                    entry.name,
                    create=False,
                )
                try:
                    _recover_temporary_files_at(child_descriptor)
                finally:
                    os.close(child_descriptor)
            elif stat.S_ISREG(metadata.st_mode) and (
                entry.name.startswith(".") and ".tmp-" in entry.name
            ):
                os.unlink(entry.name, dir_fd=directory_descriptor)


def _remove_directory_tree_at(parent_descriptor: int, name: str) -> None:
    try:
        directory_descriptor = _open_child_directory(
            parent_descriptor,
            name,
            create=False,
        )
    except FileNotFoundError:
        return
    try:
        with os.scandir(directory_descriptor) as entries:
            for entry in sorted(entries, key=lambda item: item.name):
                metadata = entry.stat(follow_symlinks=False)
                if stat.S_ISDIR(metadata.st_mode) and not stat.S_ISLNK(metadata.st_mode):
                    _remove_directory_tree_at(directory_descriptor, entry.name)
                else:
                    os.unlink(entry.name, dir_fd=directory_descriptor)
    finally:
        os.close(directory_descriptor)
    os.rmdir(name, dir_fd=parent_descriptor)


class LocalEngagementStore:
    """One explicit local root containing authoritative engagement folders."""

    def __init__(self, root: Path) -> None:
        self.root = root.absolute()
        root_descriptor = _ensure_absolute_directory(self.root)
        os.close(root_descriptor)

    def _engagement_root(self, engagement_id: str) -> Path:
        validate_identifier(engagement_id)
        return self.root / engagement_id

    def create(self, engagement: Mapping[str, Any]) -> Path:
        validated = Engagement.model_validate(dict(engagement))
        engagement_root = self._engagement_root(validated.engagement_id)
        stage_name = f".{validated.engagement_id}.create-{uuid.uuid4().hex}"
        root_descriptor = _open_absolute_directory(self.root)
        try:
            os.mkdir(stage_name, 0o700, dir_fd=root_descriptor)
            stage_descriptor = _open_child_directory(root_descriptor, stage_name, create=False)
            try:
                atomic_write_at(
                    stage_descriptor,
                    "engagement.json",
                    canonical_json(validated.model_dump()),
                )
                self._write_checksums_at(stage_descriptor)
                _fsync_directory_descriptor(stage_descriptor)
                try:
                    _rename_directory_no_replace_at(
                        root_descriptor,
                        stage_name,
                        root_descriptor,
                        validated.engagement_id,
                    )
                except FileExistsError as error:
                    raise EngagementExistsError(validated.engagement_id) from error
                _fsync_directory_descriptor(root_descriptor)
            finally:
                os.close(stage_descriptor)
        except Exception:
            try:
                _remove_directory_tree_at(root_descriptor, stage_name)
            except (FileNotFoundError, InvalidPathError, OSError):
                pass
            raise
        finally:
            os.close(root_descriptor)
        return engagement_root

    def _open_engagement_descriptor(self, engagement_id: str) -> int:
        validate_identifier(engagement_id)
        root_descriptor = _open_absolute_directory(self.root)
        try:
            engagement_descriptor = _open_child_directory(
                root_descriptor,
                engagement_id,
                create=False,
            )
        except (FileNotFoundError, NotADirectoryError, InvalidPathError) as error:
            raise EngagementNotFoundError(engagement_id) from error
        finally:
            os.close(root_descriptor)
        try:
            document = json.loads(_read_file_at(engagement_descriptor, "engagement.json"))
            validated = Engagement.model_validate(document)
            if validated.engagement_id != engagement_id:
                raise InvalidPathError("engagement folder and document IDs differ")
        except Exception:
            os.close(engagement_descriptor)
            raise
        return engagement_descriptor

    def open(self, engagement_id: str) -> Path:
        engagement_descriptor = self._open_engagement_descriptor(engagement_id)
        os.close(engagement_descriptor)
        return self._engagement_root(engagement_id)

    def read_document(self, engagement_id: str, key: str) -> dict[str, Any]:
        engagement_descriptor = self._open_engagement_descriptor(engagement_id)
        try:
            document = json.loads(_read_relative_at(engagement_descriptor, key))
            if not isinstance(document, dict):
                raise ValueError(f"{key}: expected a JSON object")
            return document
        finally:
            os.close(engagement_descriptor)

    def write_document(self, engagement_id: str, key: str, document: Mapping[str, Any]) -> None:
        validate_relative_posix_path(key)
        if key == "engagement.json":
            validated = Engagement.model_validate(dict(document))
            if validated.engagement_id != engagement_id:
                raise InvalidPathError("engagement ID cannot change")
        self.open(engagement_id)
        with self.lock(engagement_id) as engagement_descriptor:
            atomic_write_at(engagement_descriptor, key, canonical_json(dict(document)))
            self._write_checksums_at(engagement_descriptor)

    def add_evidence(self, engagement_id: str, key: str, content: bytes) -> None:
        normalized = validate_relative_posix_path(key)
        if not normalized.startswith("evidence/files/"):
            raise InvalidPathError("evidence must be stored below evidence/files/")
        self.open(engagement_id)
        with self.lock(engagement_id) as engagement_descriptor:
            atomic_write_at(engagement_descriptor, normalized, content)
            self._write_checksums_at(engagement_descriptor)

    def list_engagements(self) -> list[str]:
        result: list[str] = []
        for candidate in self.root.iterdir():
            if candidate.is_dir() and not candidate.is_symlink():
                try:
                    self.open(candidate.name)
                except (ValueError, FileNotFoundError):
                    continue
                result.append(candidate.name)
        return sorted(result)

    def snapshot(self, engagement_id: str) -> dict[str, str]:
        engagement_descriptor = self._open_engagement_descriptor(engagement_id)
        try:
            return self._snapshot_at(engagement_descriptor)
        finally:
            os.close(engagement_descriptor)

    @contextmanager
    def lock(self, engagement_id: str) -> Iterator[int]:
        root_descriptor = self._open_engagement_descriptor(engagement_id)
        flags = os.O_RDWR | os.O_CREAT
        if hasattr(os, "O_NOFOLLOW"):
            flags |= os.O_NOFOLLOW
        try:
            descriptor = os.open(
                ".engagement.lock",
                flags,
                0o600,
                dir_fd=root_descriptor,
            )
        except OSError as error:
            os.close(root_descriptor)
            raise InvalidPathError("engagement lock must be a regular local file") from error
        if not stat.S_ISREG(os.fstat(descriptor).st_mode):
            os.close(descriptor)
            os.close(root_descriptor)
            raise InvalidPathError("engagement lock must be a regular local file")
        handle: BinaryIO = os.fdopen(descriptor, "r+b")
        try:
            try:
                fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError as error:
                raise ConcurrentWriteError(f"{engagement_id}: writer lock is held") from error
            yield root_descriptor
        finally:
            try:
                fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
            finally:
                handle.close()
                os.close(root_descriptor)

    def recover(self, engagement_id: str) -> None:
        with self.lock(engagement_id) as engagement_descriptor:
            _recover_temporary_files_at(engagement_descriptor)
            self._write_checksums_at(engagement_descriptor)

    @staticmethod
    def _ignored_runtime_key(key: str) -> bool:
        name = key.rsplit("/", 1)[-1]
        return (
            name in IGNORED_RUNTIME_NAMES
            or ".tmp-" in name
            or key.startswith("cache/")
            or key.startswith(".cache/")
        )

    def _snapshot_at(
        self,
        directory_descriptor: int,
        prefix: str = "",
    ) -> dict[str, str]:
        snapshot: dict[str, str] = {}
        with os.scandir(directory_descriptor) as entries:
            for entry in sorted(entries, key=lambda item: item.name):
                key = f"{prefix}/{entry.name}" if prefix else entry.name
                metadata = entry.stat(follow_symlinks=False)
                if stat.S_ISLNK(metadata.st_mode):
                    raise InvalidPathError(f"engagement state contains a symlink: {key}")
                if stat.S_ISDIR(metadata.st_mode):
                    child_descriptor = _open_child_directory(
                        directory_descriptor,
                        entry.name,
                        create=False,
                    )
                    try:
                        snapshot.update(self._snapshot_at(child_descriptor, key))
                    finally:
                        os.close(child_descriptor)
                elif stat.S_ISREG(metadata.st_mode):
                    if self._ignored_runtime_key(key) or key == "metadata/checksums.json":
                        continue
                    snapshot[key] = sha256_bytes(_read_file_at(directory_descriptor, entry.name))
        return snapshot

    def _write_checksums_at(self, engagement_descriptor: int) -> None:
        atomic_write_at(
            engagement_descriptor,
            "metadata/checksums.json",
            canonical_json(
                {
                    "schema_version": "1.0.0",
                    "algorithm": "sha256",
                    "files": self._snapshot_at(engagement_descriptor),
                }
            ),
        )
