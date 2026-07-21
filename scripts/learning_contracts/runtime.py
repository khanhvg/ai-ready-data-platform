"""No-shell bounded process-tree execution and owned cleanup."""

from __future__ import annotations

import pathlib
import json
import os
import platform
import resource
import signal
import stat
import subprocess
import tempfile
import time
from collections.abc import Sequence

from .canonical import parse_json
from .references import resolve_reference
from .schema import LearningContractError, read_regular_bytes


def _process_group_rss(process_group: int) -> int:
    result = subprocess.run(
        ["ps", "-axo", "pgid=,rss="],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True,
    )
    total_kib = 0
    for line in result.stdout.splitlines():
        fields = line.split()
        if len(fields) == 2 and int(fields[0]) == process_group:
            total_kib += int(fields[1])
    return total_kib * 1024


def _terminate_group(process: subprocess.Popen[bytes]) -> None:
    try:
        os.killpg(process.pid, signal.SIGTERM)
    except ProcessLookupError:
        pass
    deadline = time.monotonic() + 0.5
    while process.poll() is None and time.monotonic() < deadline:
        time.sleep(0.01)
    if process.poll() is None:
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
    try:
        process.wait(timeout=2)
    except subprocess.TimeoutExpired as exc:
        raise LearningContractError("PROCESS_CLEANUP_FAILED") from exc
    cleanup_deadline = time.monotonic() + 2
    while time.monotonic() < cleanup_deadline:
        try:
            result = subprocess.run(
                ["ps", "-axo", "pgid="],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
                text=True,
            )
        except subprocess.SubprocessError as exc:
            raise LearningContractError("PROCESS_CLEANUP_FAILED") from exc
        if process.pid not in {int(line.strip()) for line in result.stdout.splitlines() if line.strip()}:
            return
        time.sleep(0.02)
    raise LearningContractError("PROCESS_CLEANUP_FAILED")


def run_bounded(
    command: Sequence[str],
    *,
    cwd: pathlib.Path,
    timeout: float = 120,
    output_limit: int = 2 * 1024 * 1024,
    max_rss_bytes: int = 512 * 1024 * 1024,
) -> bytes:
    if (
        not command
        or any(not isinstance(item, str) or not item or "\x00" in item for item in command)
        or timeout <= 0
        or timeout > 120
        or output_limit <= 0
        or max_rss_bytes <= 0
    ):
        raise LearningContractError("PROCESS_ARGUMENT_INVALID")
    if not cwd.is_dir() or cwd.is_symlink():
        raise LearningContractError("PROCESS_CWD_INVALID")
    with tempfile.TemporaryFile(dir=cwd) as stdout_file, tempfile.TemporaryFile(dir=cwd) as stderr_file:
        process = subprocess.Popen(
            list(command),
            cwd=cwd,
            stdin=subprocess.DEVNULL,
            stdout=stdout_file,
            stderr=stderr_file,
            start_new_session=True,
        )
        deadline = time.monotonic() + timeout
        failure: str | None = None
        while process.poll() is None:
            if time.monotonic() >= deadline:
                failure = "PROCESS_TIMEOUT"
                break
            if os.fstat(stdout_file.fileno()).st_size + os.fstat(stderr_file.fileno()).st_size > output_limit:
                failure = "PROCESS_OUTPUT_LIMIT"
                break
            if _process_group_rss(process.pid) > max_rss_bytes:
                failure = "PROCESS_RSS_LIMIT"
                break
            time.sleep(0.01)
        if failure is not None:
            _terminate_group(process)
            raise LearningContractError(failure)
        stdout_file.seek(0)
        stderr_file.seek(0)
        stdout = stdout_file.read(output_limit + 1)
        stderr = stderr_file.read(output_limit + 1)
        if len(stdout) + len(stderr) > output_limit:
            raise LearningContractError("PROCESS_OUTPUT_LIMIT")
        child_peak = resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss
        child_peak_bytes = int(child_peak if platform.system() == "Darwin" else child_peak * 1024)
        if child_peak_bytes > max_rss_bytes:
            raise LearningContractError("PROCESS_RSS_LIMIT")
        if process.returncode != 0:
            raise LearningContractError("PROCESS_FAILED")
        return stdout


def validate_evidence_locator(root: pathlib.Path, locator: str, sha256: str) -> bytes:
    try:
        return resolve_reference(root, locator, sha256)
    except LearningContractError as exc:
        if exc.code in {"REFERENCE_SPECIAL_FILE", "REFERENCE_UNREADABLE"}:
            raise LearningContractError("LOCATOR_SPECIAL_FILE") from exc
        if exc.code == "REFERENCE_PATH_INVALID":
            raise LearningContractError("LOCATOR_PATH_INVALID") from exc
        if exc.code == "REFERENCE_HASH_MISMATCH":
            raise LearningContractError("LOCATOR_HASH_MISMATCH") from exc
        raise


def cleanup_owned(path: pathlib.Path, marker: dict[str, object]) -> None:
    try:
        directory_before = path.lstat()
    except OSError as exc:
        raise LearningContractError("CLEANUP_OWNERSHIP_MISMATCH") from exc
    if not stat.S_ISDIR(directory_before.st_mode) or stat.S_ISLNK(directory_before.st_mode):
        raise LearningContractError("CLEANUP_OWNERSHIP_MISMATCH")
    marker_path = path / ".learning-owner.json"
    try:
        retained = parse_json(read_regular_bytes(marker_path))
    except LearningContractError as exc:
        raise LearningContractError("CLEANUP_OWNERSHIP_MISMATCH") from exc
    required = {"schemaVersion", "nonce", "device", "inode", "closed", "entries"}
    if (
        set(marker) != required
        or retained != marker
        or marker.get("schemaVersion") != "learning-owner-v1"
        or marker.get("closed") is not True
        or marker.get("device") != directory_before.st_dev
        or marker.get("inode") != directory_before.st_ino
        or not isinstance(marker.get("nonce"), str)
        or len(marker["nonce"]) != 64
    ):
        raise LearningContractError("CLEANUP_OWNERSHIP_MISMATCH")
    entries = marker.get("entries")
    if not isinstance(entries, list):
        raise LearningContractError("CLEANUP_MANIFEST_OPEN")
    declared: dict[str, str] = {}
    for item in entries:
        if not isinstance(item, dict) or set(item) != {"path", "disposition"}:
            raise LearningContractError("CLEANUP_MANIFEST_OPEN")
        name = item.get("path")
        disposition = item.get("disposition")
        if (
            not isinstance(name, str)
            or pathlib.PurePosixPath(name).parts != (name,)
            or name == ".learning-owner.json"
            or disposition not in {"mutable", "preserve"}
            or name in declared
        ):
            raise LearningContractError("CLEANUP_MANIFEST_OPEN")
        declared[name] = disposition
    actual = {child.name for child in path.iterdir() if child.name != ".learning-owner.json"}
    if not actual.issubset(declared) or any(name not in actual for name, disposition in declared.items() if disposition == "preserve"):
        raise LearningContractError("CLEANUP_MANIFEST_OPEN")
    directory_fd = os.open(path, os.O_RDONLY | os.O_DIRECTORY | getattr(os, "O_NOFOLLOW", 0))
    try:
        directory_after = os.fstat(directory_fd)
        if (directory_before.st_dev, directory_before.st_ino) != (directory_after.st_dev, directory_after.st_ino):
            raise LearningContractError("CLEANUP_OWNERSHIP_MISMATCH")
        for name, disposition in declared.items():
            if disposition != "mutable" or name not in actual:
                continue
            before = os.stat(name, dir_fd=directory_fd, follow_symlinks=False)
            if not stat.S_ISREG(before.st_mode) or before.st_nlink != 1:
                raise LearningContractError("CLEANUP_ENTRY_UNSAFE")
            descriptor = os.open(name, os.O_RDONLY | os.O_NONBLOCK | getattr(os, "O_NOFOLLOW", 0), dir_fd=directory_fd)
            try:
                after = os.fstat(descriptor)
                if (before.st_dev, before.st_ino) != (after.st_dev, after.st_ino):
                    raise LearningContractError("CLEANUP_ENTRY_UNSAFE")
            finally:
                os.close(descriptor)
            os.unlink(name, dir_fd=directory_fd)
        os.fsync(directory_fd)
    finally:
        os.close(directory_fd)
