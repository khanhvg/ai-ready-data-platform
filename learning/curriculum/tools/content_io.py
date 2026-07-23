"""Generic bounded I/O, process, evidence, and ownership primitives."""

from __future__ import annotations

import hashlib
import json
import os
import secrets
import selectors
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
    max_processes: int = 32
    max_rss_bytes: int = 512 * 1024 * 1024
    max_created_files: int = 4_096
    max_created_bytes: int = 64 * 1024 * 1024


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
    peak_processes: int
    peak_rss_bytes: int
    created_files: int
    created_bytes: int
    term_sent: bool
    kill_sent: bool
    descendants_after_reap: int


@dataclass(frozen=True)
class OwnedDirectory:
    path: Path
    parent: Path
    nonce: str
    device: int
    inode: int


_SKIPPED_DIRECTORIES = frozenset({".git", ".claude", ".artifacts", ".hermes", "__pycache__"})
_PROCESS_SKIPPED_DIRECTORIES = frozenset({".git", "__pycache__"})
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
    def reject_duplicates(pairs: list[tuple[str, object]]) -> dict[str, object]:
        result: dict[str, object] = {}
        for key, value in pairs:
            if key in result:
                raise RepositoryInputError("I11_BOUND_DUPLICATE_KEY")
            result[key] = value
        return result

    try:
        return json.loads(read_bounded(path, limits), object_pairs_hook=reject_duplicates)
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
    baseline_files = _file_snapshot(_resolved_directory(cwd))
    started = time.monotonic()
    deadline = started + limits.timeout_seconds
    process = subprocess.Popen(
        tuple(argv),
        cwd=_resolved_directory(cwd),
        env=dict(environment),
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        start_new_session=True,
    )
    if process.stdout is None or process.stderr is None:
        raise RepositoryInputError("owned process pipes are unavailable")
    for stream in (process.stdout, process.stderr):
        os.set_blocking(stream.fileno(), False)
    selector = selectors.DefaultSelector()
    selector.register(process.stdout, selectors.EVENT_READ, "stdout")
    selector.register(process.stderr, selectors.EVENT_READ, "stderr")
    output = {"stdout": bytearray(), "stderr": bytearray()}
    peak_processes = 0
    peak_rss_bytes = 0
    created_files = 0
    created_bytes = 0
    tracked_pids: set[int] = set()
    violation: str | None = None
    next_file_sample = started
    while True:
        for key, _ in selector.select(timeout=0.05):
            while True:
                try:
                    chunk = os.read(key.fileobj.fileno(), 64 * 1024)
                except BlockingIOError:
                    break
                if not chunk:
                    selector.unregister(key.fileobj)
                    break
                _append_bounded_output(output, str(key.data), chunk, limits.max_output_bytes)
                if len(output["stdout"]) + len(output["stderr"]) > limits.max_output_bytes:
                    violation = "I11_RESOURCE_OUTPUT"
                    break
            if violation is not None:
                break
        if violation is not None:
            break
        processes, rss_bytes, observed_pids = _process_tree_usage(process.pid, tracked_pids)
        tracked_pids.update(observed_pids)
        peak_processes = max(peak_processes, processes)
        peak_rss_bytes = max(peak_rss_bytes, rss_bytes)
        if processes > limits.max_processes:
            violation = violation or "I11_RESOURCE_PROCESS_COUNT"
        if rss_bytes > limits.max_rss_bytes:
            violation = violation or "I11_RESOURCE_RSS"
        now = time.monotonic()
        if now >= next_file_sample:
            current_files = _file_snapshot(_resolved_directory(cwd))
            created = {
                path: size
                for path, size in current_files.items()
                if path not in baseline_files
            }
            created_files = max(created_files, len(created))
            created_bytes = max(created_bytes, sum(created.values()))
            if created_files > limits.max_created_files:
                violation = violation or "I11_RESOURCE_FILE_COUNT"
            if created_bytes > limits.max_created_bytes:
                violation = violation or "I11_RESOURCE_FILE_BYTES"
            next_file_sample = now + 0.25
        if now >= deadline and process.poll() is None:
            violation = violation or "I11_RESOURCE_DEADLINE"
        if violation is not None:
            break
        if process.poll() is not None and not selector.get_map():
            break
    term_sent, kill_sent, descendants = _terminate_and_reap(
        process,
        selector,
        output,
        tracked_pids,
        limits.max_output_bytes,
    )
    selector.close()
    process.stdout.close()
    process.stderr.close()
    if descendants:
        raise RepositoryInputError("I11_RESOURCE_REAP")
    if violation is not None:
        raise RepositoryInputError(violation)
    stdout = bytes(output["stdout"])
    stderr = bytes(output["stderr"])
    return ProcessReceipt(
        tuple(argv),
        process.returncode,
        stdout,
        stderr,
        round((time.monotonic() - started) * 1000),
        peak_processes,
        peak_rss_bytes,
        created_files,
        created_bytes,
        term_sent,
        kill_sent,
        descendants,
    )


def _file_snapshot(root: Path) -> dict[str, int]:
    snapshot: dict[str, int] = {}
    pending = [root]
    while pending:
        directory = pending.pop()
        for entry in directory.iterdir():
            try:
                metadata = entry.lstat()
            except FileNotFoundError:
                continue
            if stat.S_ISDIR(metadata.st_mode):
                if entry.name not in _PROCESS_SKIPPED_DIRECTORIES:
                    pending.append(entry)
            elif stat.S_ISREG(metadata.st_mode):
                snapshot[entry.relative_to(root).as_posix()] = metadata.st_size
    return snapshot


def _process_tree_usage(root_pid: int, known_pids: set[int]) -> tuple[int, int, set[int]]:
    result = subprocess.run(
        ("/bin/ps", "-axo", "pid=,ppid=,pgid=,rss=,state="),
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        timeout=2,
        check=False,
    )
    rows: dict[int, tuple[int, int, int]] = {}
    for line in result.stdout.splitlines():
        fields = line.split()
        if len(fields) != 5 or fields[4].startswith(b"Z"):
            continue
        try:
            pid, parent_pid, process_group, rss_kib = map(int, fields[:4])
        except ValueError:
            continue
        rows[pid] = (parent_pid, process_group, rss_kib)
    observed = {
        pid
        for pid, (_parent_pid, process_group, _rss_kib) in rows.items()
        if pid == root_pid or process_group == root_pid
    }
    observed.update(pid for pid in known_pids if pid in rows)
    changed = True
    while changed:
        changed = False
        for pid, (parent_pid, _process_group, _rss_kib) in rows.items():
            if parent_pid in observed and pid not in observed:
                observed.add(pid)
                changed = True
    rss_bytes = sum(rows[pid][2] * 1024 for pid in observed)
    return len(observed), rss_bytes, observed


def _signal_processes(process_group: int, pids: set[int], selected_signal: int) -> bool:
    sent = False
    try:
        os.killpg(process_group, selected_signal)
        sent = True
    except ProcessLookupError:
        pass
    for pid in pids:
        try:
            os.kill(pid, selected_signal)
            sent = True
        except ProcessLookupError:
            pass
    return sent


def _drain_process_pipes(
    selector: selectors.BaseSelector,
    output: dict[str, bytearray],
    max_output_bytes: int,
) -> None:
    for key, _ in selector.select(timeout=0):
        try:
            chunk = os.read(key.fileobj.fileno(), 64 * 1024)
        except BlockingIOError:
            continue
        if chunk:
            _append_bounded_output(output, str(key.data), chunk, max_output_bytes)
        else:
            selector.unregister(key.fileobj)


def _append_bounded_output(
    output: dict[str, bytearray],
    stream: str,
    chunk: bytes,
    max_output_bytes: int,
) -> None:
    retained = len(output["stdout"]) + len(output["stderr"])
    remaining = max(0, max_output_bytes + 1 - retained)
    output[stream].extend(chunk[:remaining])


def _terminate_and_reap(
    process: subprocess.Popen[bytes],
    selector: selectors.BaseSelector,
    output: dict[str, bytearray],
    tracked_pids: set[int],
    max_output_bytes: int,
) -> tuple[bool, bool, int]:
    term_sent = False
    kill_sent = False
    descendants, _rss, observed = _process_tree_usage(process.pid, tracked_pids)
    tracked_pids.update(observed)
    if process.poll() is None or descendants:
        term_sent = _signal_processes(process.pid, tracked_pids, signal.SIGTERM)
        grace_deadline = time.monotonic() + 5.0
        while time.monotonic() < grace_deadline:
            _drain_process_pipes(selector, output, max_output_bytes)
            descendants, _rss, observed = _process_tree_usage(process.pid, tracked_pids)
            tracked_pids.update(observed)
            if process.poll() is not None and descendants == 0:
                break
            time.sleep(0.05)
        descendants, _rss, observed = _process_tree_usage(process.pid, tracked_pids)
        tracked_pids.update(observed)
        if descendants:
            kill_sent = _signal_processes(process.pid, tracked_pids, signal.SIGKILL)
    try:
        process.wait(timeout=2)
    except subprocess.TimeoutExpired:
        kill_sent = _signal_processes(process.pid, tracked_pids, signal.SIGKILL)
        process.wait(timeout=2)
    reap_deadline = time.monotonic() + 2.0
    descendants, _rss, observed = _process_tree_usage(process.pid, tracked_pids)
    tracked_pids.update(observed)
    while descendants and time.monotonic() < reap_deadline:
        _drain_process_pipes(selector, output, max_output_bytes)
        time.sleep(0.05)
        descendants, _rss, observed = _process_tree_usage(process.pid, tracked_pids)
        tracked_pids.update(observed)
    _drain_process_pipes(selector, output, max_output_bytes)
    return term_sent, kill_sent, descendants
