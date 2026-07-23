"""Generic bounded I/O, process, evidence, and ownership primitives."""

from __future__ import annotations

import hashlib
import json
import os
import secrets
import shutil
import signal
import stat
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Mapping, Sequence


class RepositoryInputError(RuntimeError):
    """Raised when generic repository or runtime admission fails."""


@dataclass(frozen=True)
class RepositoryLimits:
    max_files: int = 4_096
    max_depth: int = 16
    max_file_bytes: int = 2 * 1024 * 1024
    max_total_bytes: int = 64 * 1024 * 1024
    max_output_bytes: int = 2 * 1024 * 1024
    timeout_seconds: float = 30.0


@dataclass(frozen=True)
class RepositoryReport:
    root: str
    files: int
    bytes_read: int
    parsed_json: int
    issues: tuple[str, ...] = ()

    @property
    def ok(self) -> bool:
        return not self.issues

    def as_dict(self) -> dict[str, object]:
        return {
            "root": self.root,
            "files": self.files,
            "bytesRead": self.bytes_read,
            "parsedJson": self.parsed_json,
            "issues": list(self.issues),
            "ok": self.ok,
        }


@dataclass(frozen=True)
class ProcessReceipt:
    argv: tuple[str, ...]
    returncode: int
    stdout: bytes
    stderr: bytes
    duration_ms: int


@dataclass(frozen=True)
class OwnedDirectory:
    path: Path
    parent: Path
    nonce: str
    device: int
    inode: int


_SKIPPED_DIRECTORIES = frozenset({".git", ".claude", ".artifacts", "__pycache__"})
_CONTROLLER_KEYS = frozenset(
    {
        "PATH",
        "HOME",
        "TMPDIR",
        "XDG_CACHE_HOME",
        "PIP_CACHE_DIR",
        "TZ",
        "LC_ALL",
        "LANG",
        "PYTHONNOUSERSITE",
        "PYTHONDONTWRITEBYTECODE",
        "PIP_DISABLE_PIP_VERSION_CHECK",
        "PIP_NO_INPUT",
        "PIP_REQUIRE_VIRTUALENV",
        "GIT_CONFIG_NOSYSTEM",
        "GIT_CONFIG_GLOBAL",
        "GIT_OPTIONAL_LOCKS",
        "GIT_PAGER",
        "PAGER",
        "NO_COLOR",
        "CI",
        "I11_RUNTIME",
        "I11_RUNTIME_SHA256",
    }
)


def _resolved_directory(value: Path) -> Path:
    if not value.is_absolute():
        value = (Path.cwd() / value).resolve()
    else:
        value = value.resolve()
    if not value.is_dir() or value.is_symlink():
        raise RepositoryInputError("repository root must be a real directory")
    return value


def repository_files(
    root: Path,
    limits: RepositoryLimits = RepositoryLimits(),
) -> tuple[Path, ...]:
    root = _resolved_directory(root)
    found: list[Path] = []
    total = 0
    pending = [root]
    while pending:
        directory = pending.pop()
        relative = directory.relative_to(root)
        if len(relative.parts) > limits.max_depth:
            raise RepositoryInputError("repository depth limit exceeded")
        for entry in sorted(directory.iterdir(), key=lambda item: item.name, reverse=True):
            entry_stat = entry.lstat()
            mode = entry_stat.st_mode
            if stat.S_ISLNK(mode) or not (stat.S_ISDIR(mode) or stat.S_ISREG(mode)):
                raise RepositoryInputError("repository contains a linked or special entry")
            if stat.S_ISDIR(mode):
                if entry.name not in _SKIPPED_DIRECTORIES:
                    pending.append(entry)
                continue
            if entry_stat.st_size > limits.max_file_bytes:
                raise RepositoryInputError("repository file size limit exceeded")
            total += entry_stat.st_size
            if total > limits.max_total_bytes:
                raise RepositoryInputError("repository aggregate size limit exceeded")
            found.append(entry)
            if len(found) > limits.max_files:
                raise RepositoryInputError("repository file count limit exceeded")
    return tuple(sorted(found))


def read_bounded(path: Path, limits: RepositoryLimits = RepositoryLimits()) -> bytes:
    entry_stat = path.lstat()
    if not stat.S_ISREG(entry_stat.st_mode) or path.is_symlink():
        raise RepositoryInputError("input must be a regular file")
    if entry_stat.st_size > limits.max_file_bytes:
        raise RepositoryInputError("input file size limit exceeded")
    data = path.read_bytes()
    if len(data) != entry_stat.st_size:
        raise RepositoryInputError("input changed while being read")
    return data


def parse_json(path: Path, limits: RepositoryLimits = RepositoryLimits()) -> object:
    try:
        return json.loads(read_bounded(path, limits))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise RepositoryInputError(f"invalid JSON input: {path.name}") from exc


def inspect_repository(
    root: Path,
    limits: RepositoryLimits = RepositoryLimits(),
) -> RepositoryReport:
    root = _resolved_directory(root)
    files = repository_files(root, limits)
    parsed = 0
    bytes_read = 0
    for file_path in files:
        relative = file_path.relative_to(root)
        parse_scope = relative.parts[:2] in {
            ("learning", "curriculum"),
            ("architecture", "expansions"),
        }
        if file_path.suffix == ".json" and parse_scope:
            parse_json(file_path, limits)
            parsed += 1
        bytes_read += file_path.stat().st_size
        if ".." in relative.parts:
            raise RepositoryInputError("repository path escaped its root")
    return RepositoryReport(str(root), len(files), bytes_read, parsed)


def sha256_file(path: Path, limits: RepositoryLimits = RepositoryLimits()) -> str:
    return hashlib.sha256(read_bounded(path, limits)).hexdigest()


def evidence_index(
    root: Path,
    limits: RepositoryLimits = RepositoryLimits(),
    excluded: Iterable[str] = ("index.json", "index.sha256"),
) -> list[dict[str, object]]:
    root = _resolved_directory(root)
    excluded_names = frozenset(excluded)
    rows: list[dict[str, object]] = []
    for file_path in repository_files(root, limits):
        relative = file_path.relative_to(root).as_posix()
        if relative in excluded_names:
            continue
        entry_stat = file_path.lstat()
        rows.append(
            {
                "path": relative,
                "mediaType": "application/json" if file_path.suffix == ".json" else "application/octet-stream",
                "bytes": entry_stat.st_size,
                "mode": f"{stat.S_IMODE(entry_stat.st_mode):04o}",
                "type": "regular",
                "sha256": sha256_file(file_path, limits),
            }
        )
    return rows


def write_evidence_index(root: Path, limits: RepositoryLimits = RepositoryLimits()) -> tuple[Path, Path]:
    root = _resolved_directory(root)
    index_path = root / "index.json"
    digest_path = root / "index.sha256"
    payload = json.dumps(evidence_index(root, limits), sort_keys=True, separators=(",", ":")).encode() + b"\n"
    _write_owned_file(index_path, payload)
    _write_owned_file(digest_path, (hashlib.sha256(payload).hexdigest() + "\n").encode())
    return index_path, digest_path


def _write_owned_file(path: Path, data: bytes) -> None:
    if path.exists() and (path.is_symlink() or not path.is_file()):
        raise RepositoryInputError("owned output is not a regular file")
    flags = os.O_WRONLY | os.O_CREAT | os.O_TRUNC
    descriptor = os.open(path, flags, 0o600)
    try:
        os.write(descriptor, data)
        os.fsync(descriptor)
    finally:
        os.close(descriptor)
    os.chmod(path, 0o600)


def allocate_owned_directory(parent: Path, purpose: str) -> OwnedDirectory:
    parent = _resolved_directory(parent)
    if stat.S_IMODE(parent.stat().st_mode) != 0o700:
        raise RepositoryInputError("ownership parent must use mode 0700")
    if not purpose or not purpose.replace("-", "").isalnum():
        raise RepositoryInputError("invalid ownership purpose")
    nonce = secrets.token_hex(16)
    owned_path = parent / f"{purpose}-{nonce}"
    owned_path.mkdir(mode=0o700)
    owned_stat = owned_path.stat()
    marker = {
        "nonce": nonce,
        "purpose": purpose,
        "device": owned_stat.st_dev,
        "inode": owned_stat.st_ino,
    }
    _write_owned_file(
        owned_path / "owner.json",
        json.dumps(marker, sort_keys=True, separators=(",", ":")).encode() + b"\n",
    )
    return OwnedDirectory(owned_path, parent, nonce, owned_stat.st_dev, owned_stat.st_ino)


def remove_owned_directory(owned: OwnedDirectory) -> None:
    parent = _resolved_directory(owned.parent)
    candidate = owned.path
    if candidate.parent.resolve() != parent or candidate.is_symlink():
        raise RepositoryInputError("cleanup target escaped its ownership parent")
    candidate_stat = candidate.stat()
    marker = parse_json(candidate / "owner.json")
    expected = {
        "nonce": owned.nonce,
        "device": owned.device,
        "inode": owned.inode,
    }
    if (
        not isinstance(marker, dict)
        or any(marker.get(key) != value for key, value in expected.items())
        or candidate_stat.st_dev != owned.device
        or candidate_stat.st_ino != owned.inode
    ):
        raise RepositoryInputError("cleanup ownership changed")
    shutil.rmtree(candidate)


def controller_environment(runtime: Path, interpreter_sha256: str | None) -> dict[str, str]:
    runtime = _resolved_directory(runtime)
    interpreter = runtime / "venv/bin/python"
    admitted_python = Path(getattr(sys, "_base_executable", sys.executable)).resolve()
    admitted_parent = str(admitted_python.parent)
    environment = {
        "PATH": f"{admitted_parent}:/usr/bin:/bin:/usr/sbin:/sbin",
        "HOME": str(runtime / "home"),
        "TMPDIR": str(runtime / "tmp"),
        "XDG_CACHE_HOME": str(runtime / "cache"),
        "PIP_CACHE_DIR": str(runtime / "pip-cache"),
        "TZ": "UTC",
        "LC_ALL": "C.UTF-8",
        "LANG": "C.UTF-8",
        "PYTHONNOUSERSITE": "1",
        "PYTHONDONTWRITEBYTECODE": "1",
        "PIP_DISABLE_PIP_VERSION_CHECK": "1",
        "PIP_NO_INPUT": "1",
        "PIP_REQUIRE_VIRTUALENV": "1",
        "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_CONFIG_GLOBAL": "/dev/null",
        "GIT_OPTIONAL_LOCKS": "0",
        "GIT_PAGER": "cat",
        "PAGER": "cat",
        "NO_COLOR": "1",
        "CI": "1",
        "I11_RUNTIME": str(runtime),
    }
    if interpreter_sha256 is not None:
        environment["I11_RUNTIME_SHA256"] = interpreter_sha256
    if interpreter.parent != runtime / "venv/bin" or sys.version_info[:2] != (3, 12):
        raise RepositoryInputError("runtime interpreter escaped the candidate")
    return environment


def validate_runtime() -> tuple[Path, Path, str]:
    runtime_value = os.environ.get("I11_RUNTIME")
    expected_digest = os.environ.get("I11_RUNTIME_SHA256")
    if not runtime_value or not expected_digest:
        raise RepositoryInputError("admitted runtime variables are required")
    runtime = Path(runtime_value)
    if not runtime.is_absolute():
        raise RepositoryInputError("runtime candidate must be absolute")
    runtime = _resolved_directory(runtime)
    if stat.S_IMODE(runtime.stat().st_mode) != 0o700:
        raise RepositoryInputError("runtime candidate must use mode 0700")
    interpreter = runtime / "venv/bin/python"
    if not interpreter.is_file():
        raise RepositoryInputError("runtime interpreter must resolve to a regular file")
    digest = hashlib.sha256(interpreter.read_bytes()).hexdigest()
    if digest != expected_digest:
        raise RepositoryInputError("runtime interpreter identity mismatch")
    if Path(os.path.realpath(os.sys.executable)) != interpreter.resolve():
        raise RepositoryInputError("process is not using the admitted interpreter")
    return runtime, interpreter, digest


def _run_owned_process(
    argv: Sequence[str],
    *,
    cwd: Path,
    environment: Mapping[str, str],
    limits: RepositoryLimits = RepositoryLimits(),
) -> ProcessReceipt:
    if not argv or not Path(argv[0]).is_absolute() or not Path(argv[0]).is_file():
        raise RepositoryInputError("owned process executable must be an absolute regular file")
    if set(environment) != _CONTROLLER_KEYS:
        raise RepositoryInputError("owned process environment differs from the controller table")
    started = time.monotonic()
    process = subprocess.Popen(
        tuple(argv),
        cwd=_resolved_directory(cwd),
        env=dict(environment),
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        start_new_session=True,
    )
    try:
        stdout, stderr = process.communicate(timeout=limits.timeout_seconds)
    except subprocess.TimeoutExpired:
        os.killpg(process.pid, signal.SIGTERM)
        try:
            stdout, stderr = process.communicate(timeout=2)
        except subprocess.TimeoutExpired:
            os.killpg(process.pid, signal.SIGKILL)
            stdout, stderr = process.communicate(timeout=2)
    if len(stdout) + len(stderr) > limits.max_output_bytes:
        raise RepositoryInputError("owned process output limit exceeded")
    return ProcessReceipt(
        tuple(argv),
        process.returncode,
        stdout,
        stderr,
        round((time.monotonic() - started) * 1000),
    )
