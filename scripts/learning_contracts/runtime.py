"""No-shell bounded process-tree execution and owned cleanup."""

from __future__ import annotations

import argparse
import hashlib
import pathlib
import json
import os
import platform
import re
import resource
import signal
import stat
import subprocess
import sys
import tempfile
import time
from collections.abc import Sequence

from . import LearningContractError

MAX_DOCUMENT_BYTES = 2 * 1024 * 1024


ROOT = pathlib.Path(__file__).resolve().parents[2]
IMMUTABLE_INPUT_SHA = "abcaa2de7247d99c642fcad1535c24870f08c79f"
RUNTIME_MARKER = "runtime-admission.json"
RUNTIME_INTERPRETER = pathlib.PurePosixPath("venv/bin/python")
RUNTIME_LOCK = ROOT / "requirements/golden-py312-macos-arm64.lock"
RUNTIME_PLAN = ROOT / "plans/260721-008-version-learning-contracts/phase-05-stage-a-compatibility-release-and-staged-handoff.md"
_SHA256_PATTERN = frozenset("0123456789abcdef")


def _parse_json(raw: bytes) -> object:
    def pairs(items: list[tuple[str, object]]) -> dict[str, object]:
        value: dict[str, object] = {}
        for key, item in items:
            if key in value:
                raise LearningContractError("DOCUMENT_JSON_INVALID")
            value[key] = item
        return value

    try:
        return json.loads(
            raw.decode("utf-8"),
            object_pairs_hook=pairs,
            parse_constant=lambda _value: (_ for _ in ()).throw(ValueError()),
        )
    except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
        raise LearningContractError("DOCUMENT_JSON_INVALID") from exc


def _sha256_file(path: pathlib.Path) -> str:
    digest = hashlib.sha256()
    try:
        with path.open("rb") as source:
            for chunk in iter(lambda: source.read(1024 * 1024), b""):
                digest.update(chunk)
    except OSError as exc:
        raise LearningContractError("RUNTIME_IDENTITY_UNREADABLE") from exc
    return digest.hexdigest()


def _valid_sha256(value: object) -> bool:
    return isinstance(value, str) and len(value) == 64 and set(value).issubset(_SHA256_PATTERN)


def expected_runtime_identity(interpreter_sha256: str) -> dict[str, str]:
    if not _valid_sha256(interpreter_sha256):
        raise LearningContractError("RUNTIME_INTERPRETER_HASH_INVALID")
    return {
        "schemaVersion": "learning-runtime-admission-v1",
        "interpreterSha256": interpreter_sha256,
        "toolSha256": _sha256_file(pathlib.Path(__file__)),
        "lockSha256": _sha256_file(RUNTIME_LOCK),
        "planSha256": _sha256_file(RUNTIME_PLAN),
        "inputSha": IMMUTABLE_INPUT_SHA,
    }


def _admission_markers(root: pathlib.Path) -> list[pathlib.Path]:
    try:
        root_info = root.lstat()
        if not stat.S_ISDIR(root_info.st_mode) or stat.S_ISLNK(root_info.st_mode):
            raise LearningContractError("RUNTIME_ROOT_INVALID")
        return sorted(
            child / RUNTIME_MARKER
            for child in root.iterdir()
            if child.is_dir() and not child.is_symlink() and (child / RUNTIME_MARKER).exists()
        )
    except OSError as exc:
        raise LearningContractError("RUNTIME_ROOT_INVALID") from exc


def select_admitted_runtime(root: pathlib.Path, expected: dict[str, str]) -> pathlib.Path:
    """Return the sole hash-bound interpreter below *root*, or fail closed."""
    nofollow = getattr(os, "O_NOFOLLOW", 0)
    try:
        before = os.stat(root, follow_symlinks=False)
        root_fd = os.open(root, os.O_RDONLY | os.O_DIRECTORY | os.O_NONBLOCK | nofollow)
    except OSError as exc:
        raise LearningContractError("RUNTIME_ROOT_INVALID") from exc
    candidate_name: str | None = None
    marker: object = None
    try:
        after = os.fstat(root_fd)
        if not stat.S_ISDIR(before.st_mode) or not _same_file(before, after):
            raise LearningContractError("RUNTIME_ROOT_INVALID")
        for name in sorted(os.listdir(root_fd)):
            if pathlib.PurePath(name).parts != (name,):
                continue
            try:
                candidate_fd = os.open(
                    name, os.O_RDONLY | os.O_DIRECTORY | os.O_NONBLOCK | nofollow,
                    dir_fd=root_fd,
                )
            except OSError:
                continue
            try:
                try:
                    marker_before = os.stat(RUNTIME_MARKER, dir_fd=candidate_fd, follow_symlinks=False)
                    marker_fd = os.open(
                        RUNTIME_MARKER, os.O_RDONLY | os.O_NONBLOCK | nofollow,
                        dir_fd=candidate_fd,
                    )
                except FileNotFoundError:
                    continue
                except OSError as exc:
                    raise LearningContractError("RUNTIME_ADMISSION_MISMATCH") from exc
                try:
                    marker_after = os.fstat(marker_fd)
                    if (
                        not stat.S_ISREG(marker_before.st_mode)
                        or marker_before.st_nlink != 1
                        or marker_after.st_size > MAX_DOCUMENT_BYTES
                        or not _same_file(marker_before, marker_after)
                    ):
                        raise LearningContractError("RUNTIME_ADMISSION_MISMATCH")
                    raw = os.read(marker_fd, MAX_DOCUMENT_BYTES + 1)
                    if len(raw) > MAX_DOCUMENT_BYTES:
                        raise LearningContractError("RUNTIME_ADMISSION_MISMATCH")
                    if candidate_name is not None:
                        raise LearningContractError("RUNTIME_ADMISSION_COUNT")
                    candidate_name = name
                    marker = _parse_json(raw)
                finally:
                    os.close(marker_fd)
            finally:
                os.close(candidate_fd)
    finally:
        os.close(root_fd)
    if candidate_name is None:
        raise LearningContractError("RUNTIME_ADMISSION_COUNT")
    required = {
        "schemaVersion", "interpreterSha256", "toolSha256", "lockSha256", "planSha256", "inputSha",
    }
    if not isinstance(marker, dict) or set(marker) != required or marker != expected:
        raise LearningContractError("RUNTIME_ADMISSION_MISMATCH")
    interpreter = root / candidate_name / RUNTIME_INTERPRETER
    try:
        resolved = interpreter.resolve(strict=True)
        info = resolved.stat()
    except OSError as exc:
        raise LearningContractError("RUNTIME_INTERPRETER_MISMATCH") from exc
    if not stat.S_ISREG(info.st_mode) or info.st_nlink < 1 or _sha256_file(resolved) != expected["interpreterSha256"]:
        raise LearningContractError("RUNTIME_INTERPRETER_MISMATCH")
    return interpreter


def admit_runtime(root: pathlib.Path, candidate: pathlib.Path, interpreter_sha256: str) -> pathlib.Path:
    """Atomically admit one existing golden runtime using caller-pinned identity."""
    expected = expected_runtime_identity(interpreter_sha256)
    if _admission_markers(root):
        raise LearningContractError("RUNTIME_ADMISSION_COUNT")
    try:
        root_resolved = root.resolve(strict=True)
        candidate_resolved = candidate.resolve(strict=True)
    except OSError as exc:
        raise LearningContractError("RUNTIME_CANDIDATE_INVALID") from exc
    if candidate.parent.resolve() != root_resolved or candidate_resolved.parent != root_resolved:
        raise LearningContractError("RUNTIME_CANDIDATE_INVALID")
    interpreter = candidate / RUNTIME_INTERPRETER
    try:
        resolved_interpreter = interpreter.resolve(strict=True)
    except OSError as exc:
        raise LearningContractError("RUNTIME_CANDIDATE_INVALID") from exc
    if _sha256_file(resolved_interpreter) != interpreter_sha256:
        raise LearningContractError("RUNTIME_INTERPRETER_MISMATCH")
    marker = candidate / RUNTIME_MARKER
    raw = json.dumps(expected, sort_keys=True, separators=(",", ":")).encode("utf-8") + b"\n"
    try:
        descriptor = os.open(marker, os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0), 0o600)
        try:
            os.write(descriptor, raw)
            os.fsync(descriptor)
        finally:
            os.close(descriptor)
    except OSError as exc:
        raise LearningContractError("RUNTIME_ADMISSION_WRITE_FAILED") from exc
    select_admitted_runtime(root, expected)
    return marker


def _same_file(before: os.stat_result, after: os.stat_result) -> bool:
    return (
        before.st_dev,
        before.st_ino,
        stat.S_IFMT(before.st_mode),
        before.st_nlink,
    ) == (
        after.st_dev,
        after.st_ino,
        stat.S_IFMT(after.st_mode),
        after.st_nlink,
    )


def _process_snapshot() -> dict[int, tuple[int, int, int]]:
    result = subprocess.run(
        ["ps", "-axo", "pid=,ppid=,pgid=,rss=,state="],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True,
    )
    members: dict[int, tuple[int, int, int]] = {}
    for line in result.stdout.splitlines():
        fields = line.split()
        if len(fields) == 5 and not fields[4].startswith("Z"):
            members[int(fields[0])] = (int(fields[1]), int(fields[2]), int(fields[3]) * 1024)
    return members


def _owned_snapshot(root_pid: int, retained: set[int]) -> dict[int, int]:
    """Retain the complete observed lineage, including descendants that call setsid()."""
    snapshot = _process_snapshot()
    retained.add(root_pid)
    retained.update(pid for pid, (_parent, group, _rss) in snapshot.items() if group == root_pid)
    changed = True
    while changed:
        changed = False
        for pid, (parent, _group, _rss) in snapshot.items():
            if parent in retained and pid not in retained:
                retained.add(pid)
                changed = True
    return {pid: snapshot[pid][2] for pid in retained if pid in snapshot}


def _terminate_owned(process: subprocess.Popen[bytes], retained: set[int]) -> None:
    def signal_members(signum: signal.Signals) -> None:
        members = _owned_snapshot(process.pid, retained)
        for pid in sorted(members, reverse=True):
            try:
                os.kill(pid, signum)
            except ProcessLookupError:
                pass

    signal_members(signal.SIGTERM)
    deadline = time.monotonic() + 0.5
    while _owned_snapshot(process.pid, retained) and time.monotonic() < deadline:
        time.sleep(0.01)
    if _owned_snapshot(process.pid, retained):
        signal_members(signal.SIGKILL)
    try:
        process.wait(timeout=2)
    except subprocess.TimeoutExpired as exc:
        raise LearningContractError("PROCESS_CLEANUP_FAILED") from exc
    cleanup_deadline = time.monotonic() + 2
    while time.monotonic() < cleanup_deadline:
        try:
            members = _owned_snapshot(process.pid, retained)
        except subprocess.SubprocessError as exc:
            raise LearningContractError("PROCESS_CLEANUP_FAILED") from exc
        if not members:
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
        owned = {process.pid}
        while process.poll() is None:
            if time.monotonic() >= deadline:
                failure = "PROCESS_TIMEOUT"
                break
            if os.fstat(stdout_file.fileno()).st_size + os.fstat(stderr_file.fileno()).st_size > output_limit:
                failure = "PROCESS_OUTPUT_LIMIT"
                break
            if sum(_owned_snapshot(process.pid, owned).values()) > max_rss_bytes:
                failure = "PROCESS_RSS_LIMIT"
                break
            time.sleep(0.01)
        if failure is not None:
            _terminate_owned(process, owned)
            raise LearningContractError(failure)
        if _owned_snapshot(process.pid, owned):
            _terminate_owned(process, owned)
            raise LearningContractError("PROCESS_CLEANUP_FAILED")
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
    from .references import resolve_reference
    from .schema import LearningContractError as ContractError

    try:
        return resolve_reference(root, locator, sha256)
    except ContractError as exc:
        if exc.code in {"REFERENCE_SPECIAL_FILE", "REFERENCE_UNREADABLE"}:
            raise LearningContractError("LOCATOR_SPECIAL_FILE") from exc
        if exc.code == "REFERENCE_PATH_INVALID":
            raise LearningContractError("LOCATOR_PATH_INVALID") from exc
        if exc.code == "REFERENCE_HASH_MISMATCH":
            raise LearningContractError("LOCATOR_HASH_MISMATCH") from exc
        raise


def cleanup_owned(path: pathlib.Path, marker: dict[str, object], *, owned_root: pathlib.Path) -> None:
    if path.parent != owned_root or pathlib.PurePath(path.name).parts != (path.name,):
        raise LearningContractError("CLEANUP_ROOT_INVALID")
    nofollow = getattr(os, "O_NOFOLLOW", 0)
    try:
        root_before = os.stat(owned_root, follow_symlinks=False)
        root_fd = os.open(owned_root, os.O_RDONLY | os.O_DIRECTORY | os.O_NONBLOCK | nofollow)
    except OSError as exc:
        raise LearningContractError("CLEANUP_ROOT_INVALID") from exc
    try:
        root_after = os.fstat(root_fd)
        if (
            not stat.S_ISDIR(root_before.st_mode)
            or not stat.S_ISDIR(root_after.st_mode)
            or root_before.st_nlink < 1
            or not _same_file(root_before, root_after)
        ):
            raise LearningContractError("CLEANUP_ROOT_INVALID")
        try:
            directory_before = os.stat(path.name, dir_fd=root_fd, follow_symlinks=False)
            directory_fd = os.open(
                path.name,
                os.O_RDONLY | os.O_DIRECTORY | os.O_NONBLOCK | nofollow,
                dir_fd=root_fd,
            )
        except OSError as exc:
            raise LearningContractError("CLEANUP_OWNERSHIP_MISMATCH") from exc
        try:
            directory_after = os.fstat(directory_fd)
            if (
                not stat.S_ISDIR(directory_before.st_mode)
                or not stat.S_ISDIR(directory_after.st_mode)
                or directory_before.st_nlink < 1
                or not _same_file(directory_before, directory_after)
            ):
                raise LearningContractError("CLEANUP_OWNERSHIP_MISMATCH")
            try:
                marker_before = os.stat(".learning-owner.json", dir_fd=directory_fd, follow_symlinks=False)
                if not stat.S_ISREG(marker_before.st_mode) or marker_before.st_nlink != 1:
                    raise LearningContractError("CLEANUP_OWNERSHIP_MISMATCH")
                marker_fd = os.open(
                    ".learning-owner.json",
                    os.O_RDONLY | os.O_NONBLOCK | nofollow,
                    dir_fd=directory_fd,
                )
            except (OSError, LearningContractError) as exc:
                raise LearningContractError("CLEANUP_OWNERSHIP_MISMATCH") from exc
            try:
                marker_after = os.fstat(marker_fd)
                if (
                    not stat.S_ISREG(marker_after.st_mode)
                    or marker_after.st_nlink != 1
                    or not _same_file(marker_before, marker_after)
                    or marker_after.st_size > MAX_DOCUMENT_BYTES
                ):
                    raise LearningContractError("CLEANUP_OWNERSHIP_MISMATCH")
                chunks: list[bytes] = []
                remaining = MAX_DOCUMENT_BYTES + 1
                while remaining:
                    chunk = os.read(marker_fd, remaining)
                    if not chunk:
                        break
                    chunks.append(chunk)
                    remaining -= len(chunk)
                raw_marker = b"".join(chunks)
                if len(raw_marker) > MAX_DOCUMENT_BYTES:
                    raise LearningContractError("CLEANUP_OWNERSHIP_MISMATCH")
                retained = _parse_json(raw_marker)
            except LearningContractError as exc:
                raise LearningContractError("CLEANUP_OWNERSHIP_MISMATCH") from exc

            required = {"schemaVersion", "nonce", "device", "inode", "closed", "entries"}
            if (
                set(marker) != required
                or retained != marker
                or marker.get("schemaVersion") != "learning-owner-v1"
                or marker.get("closed") is not True
                or marker.get("device") != directory_after.st_dev
                or marker.get("inode") != directory_after.st_ino
                or not isinstance(marker.get("nonce"), str)
                or len(marker["nonce"]) != 64
                or any(character not in "0123456789abcdef" for character in marker["nonce"])
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
            actual = set(os.listdir(directory_fd)) - {".learning-owner.json"}
            if not actual.issubset(declared) or any(
                name not in actual for name, disposition in declared.items() if disposition == "preserve"
            ):
                raise LearningContractError("CLEANUP_MANIFEST_OPEN")

            removable: list[tuple[str, int, os.stat_result]] = []
            quarantine_name: str | None = None
            namespace_isolated = False
            namespace_conflict = False
            try:
                for name, disposition in declared.items():
                    if disposition != "mutable" or name not in actual:
                        continue
                    try:
                        before = os.stat(name, dir_fd=directory_fd, follow_symlinks=False)
                    except OSError as exc:
                        raise LearningContractError("CLEANUP_ENTRY_UNSAFE") from exc
                    if not stat.S_ISREG(before.st_mode) or before.st_nlink != 1:
                        raise LearningContractError("CLEANUP_ENTRY_UNSAFE")
                    try:
                        descriptor = os.open(
                            name,
                            os.O_RDONLY | os.O_NONBLOCK | nofollow,
                            dir_fd=directory_fd,
                        )
                    except OSError as exc:
                        raise LearningContractError("CLEANUP_ENTRY_UNSAFE") from exc
                    after = os.fstat(descriptor)
                    if (
                        not stat.S_ISREG(after.st_mode)
                        or after.st_nlink != 1
                        or not _same_file(before, after)
                    ):
                        os.close(descriptor)
                        raise LearningContractError("CLEANUP_ENTRY_UNSAFE")
                    removable.append((name, descriptor, after))

                # Revalidate the closed manifest and complete directory before the first unlink.
                if not _same_file(os.fstat(marker_fd), marker_after) or not _same_file(
                    os.fstat(directory_fd), directory_after
                ):
                    raise LearningContractError("CLEANUP_OWNERSHIP_MISMATCH")
                if set(os.listdir(directory_fd)) - {".learning-owner.json"} != actual:
                    raise LearningContractError("CLEANUP_MANIFEST_OPEN")
                for name, descriptor, held in removable:
                    try:
                        current = os.stat(name, dir_fd=directory_fd, follow_symlinks=False)
                    except OSError as exc:
                        raise LearningContractError("CLEANUP_ENTRY_UNSAFE") from exc
                    if not _same_file(current, held):
                        raise LearningContractError("CLEANUP_ENTRY_UNSAFE")
                # Quarantine the verified directory behind a held root descriptor,
                # then reserve its public name with an empty decoy. A concurrent
                # writer can only alter the decoy; it can never redirect deletion
                # inside the descriptor-held owned directory.
                quarantine_name = f".{path.name}.cleanup-{marker['nonce'][:16]}"
                try:
                    os.stat(quarantine_name, dir_fd=root_fd, follow_symlinks=False)
                except FileNotFoundError:
                    pass
                else:
                    raise LearningContractError("CLEANUP_OWNERSHIP_MISMATCH")
                try:
                    os.rename(
                        path.name, quarantine_name,
                        src_dir_fd=root_fd, dst_dir_fd=root_fd,
                    )
                    os.mkdir(path.name, 0o700, dir_fd=root_fd)
                    namespace_isolated = True
                except OSError as exc:
                    raise LearningContractError("CLEANUP_ENTRY_UNSAFE") from exc
                if not _same_file(os.fstat(directory_fd), directory_after):
                    raise LearningContractError("CLEANUP_OWNERSHIP_MISMATCH")
                for name, _, _ in removable:
                    try:
                        os.unlink(name, dir_fd=directory_fd)
                    except OSError as exc:
                        raise LearningContractError("CLEANUP_ENTRY_UNSAFE") from exc
                os.fsync(directory_fd)
            finally:
                for _, descriptor, _ in removable:
                    os.close(descriptor)
                os.close(marker_fd)
                if namespace_isolated and quarantine_name is not None:
                    try:
                        decoy_fd = os.open(
                            path.name,
                            os.O_RDONLY | os.O_DIRECTORY | os.O_NONBLOCK | nofollow,
                            dir_fd=root_fd,
                        )
                        try:
                            namespace_conflict = bool(os.listdir(decoy_fd))
                        finally:
                            os.close(decoy_fd)
                        if not namespace_conflict:
                            os.rmdir(path.name, dir_fd=root_fd)
                            os.rename(
                                quarantine_name, path.name,
                                src_dir_fd=root_fd, dst_dir_fd=root_fd,
                            )
                    except OSError as exc:
                        raise LearningContractError("CLEANUP_ENTRY_UNSAFE") from exc
                    if namespace_conflict:
                        raise LearningContractError("CLEANUP_ENTRY_UNSAFE")
        finally:
            os.close(directory_fd)
    finally:
        os.close(root_fd)


def _public_child_argv(arguments: Sequence[str]) -> list[str]:
    values = list(arguments)
    if values[:1] == ["--"]:
        values = values[1:]
    if values in (["check"], ["api"]):
        return ["-m", "scripts.learning_contracts.check", *values]
    if len(values) == 3 and values[0:2] == ["lesson", "--lesson"]:
        value = values[2]
        if re.fullmatch(r"[a-z0-9][a-z0-9-]{0,63}", value) is None:
            raise LearningContractError("PUBLIC_ARGUMENT_INVALID")
        return ["-m", "scripts.learning_contracts.check", *values]
    if len(values) == 3 and values[0:2] == ["evidence", "--evidence"]:
        value = values[2]
        candidate = pathlib.PurePosixPath(value)
        secret = re.search(r"(?:AKIA[0-9A-Z]{16}|[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,})", value)
        if (
            not value or len(value) > 256 or "\x00" in value or candidate.is_absolute()
            or any(part in {"", ".", ".."} for part in candidate.parts) or "\\" in value or secret
            or re.search(r"[;&|`$<>(){}!\n\r]", value)
        ):
            raise LearningContractError("PUBLIC_ARGUMENT_INVALID")
        return ["-m", "scripts.learning_contracts.check", *values]
    raise LearningContractError("PUBLIC_ARGUMENT_INVALID")


def launch_public(
    root: pathlib.Path,
    interpreter_sha256: str,
    child_arguments: Sequence[str],
    *,
    timeout: float,
) -> bytes:
    expected = expected_runtime_identity(interpreter_sha256)
    interpreter = select_admitted_runtime(root, expected)
    child = _public_child_argv(child_arguments)
    return run_bounded(
        [str(interpreter), *child],
        cwd=ROOT,
        timeout=timeout,
        output_limit=10 * 1024 * 1024,
        max_rss_bytes=512 * 1024 * 1024,
    )


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="learning-runtime")
    subparsers = parser.add_subparsers(dest="action", required=True)
    admit = subparsers.add_parser("admit")
    admit.add_argument("--runtime-root", required=True)
    admit.add_argument("--candidate", required=True)
    admit.add_argument("--interpreter-sha256", required=True)
    launch = subparsers.add_parser("launch")
    launch.add_argument("--runtime-root", required=True)
    launch.add_argument("--interpreter-sha256", required=True)
    launch.add_argument("--timeout", required=True, type=float)
    launch.add_argument("child", nargs=argparse.REMAINDER)
    arguments = parser.parse_args(argv)
    try:
        if arguments.action == "admit":
            marker = admit_runtime(
                pathlib.Path(arguments.runtime_root),
                pathlib.Path(arguments.candidate),
                arguments.interpreter_sha256,
            )
            print(json.dumps({"result": "admitted", "marker": str(marker)}, sort_keys=True))
        else:
            output = launch_public(
                pathlib.Path(arguments.runtime_root),
                arguments.interpreter_sha256,
                arguments.child,
                timeout=arguments.timeout,
            )
            os.write(sys.stdout.fileno(), output)
    except LearningContractError as exc:
        print(exc.code, file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
