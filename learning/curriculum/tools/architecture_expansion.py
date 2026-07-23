"""Callable orchestration scaffold for bounded repository verification."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
from typing import Sequence

from .check_curriculum import check_repository
from .check_traceability import _verify_repository
from .content_io import (
    RepositoryLimits,
    RepositoryReport,
    controller_environment,
    evidence_index,
    _run_owned_process,
    sha256_file,
    validate_runtime,
)


_FOCUSED_TEST_PATHS = (
    "tests/learning/curriculum/test_architecture_expansion.py",
    "tests/learning/curriculum/test_curriculum_contract.py",
    "tests/learning/curriculum/test_security_and_bounds.py",
    "tests/learning/curriculum/test_traceability.py",
)


def _toolchain_verification(
    root: Path | str = Path.cwd(),
    limits: RepositoryLimits = RepositoryLimits(),
) -> dict[str, object]:
    """Verify fixed local tool inputs and the admitted interpreter identity."""

    root_path = Path(root).resolve()
    semantic = check_repository(root_path, limits)
    if not semantic.ok:
        raise RuntimeError(",".join(semantic.issues))
    runtime, interpreter, interpreter_digest = validate_runtime()
    locked_inputs = (
        root_path / "requirements/architecture/package-lock.json",
        root_path / "learning/curriculum/tools/architecture-render.mjs",
    )
    hashes = {
        item.relative_to(root_path).as_posix(): sha256_file(item, limits)
        for item in locked_inputs
        if item.is_file() and not item.is_symlink()
    }
    if len(hashes) != len(locked_inputs):
        raise RuntimeError("locked tool input is missing or linked")
    return {
        "runtime": str(runtime),
        "interpreter": str(interpreter),
        "interpreterSha256": interpreter_digest,
        "lockedInputs": hashes,
    }


def _repository_handoff(
    root: Path | str = Path.cwd(),
    limits: RepositoryLimits = RepositoryLimits(),
) -> dict[str, object]:
    """Read real Git porcelain and index an explicitly supplied evidence root."""

    root_path = Path(root).resolve()
    semantic = check_repository(root_path, limits)
    if not semantic.ok:
        raise RuntimeError(",".join(semantic.issues))
    runtime, _, digest = validate_runtime()
    environment = controller_environment(runtime, digest)
    receipt = _run_owned_process(
        ("/usr/bin/git", "status", "--porcelain=v1", "--untracked-files=all"),
        cwd=root_path,
        environment=environment,
        limits=limits,
    )
    if receipt.returncode != 0:
        raise RuntimeError("Git porcelain command failed")
    evidence_root = root_path / ".claude/evidence"
    evidence_limits = RepositoryLimits(
        max_files=limits.max_files,
        max_depth=limits.max_depth,
        max_file_bytes=max(limits.max_file_bytes, 16 * 1024 * 1024),
        max_total_bytes=limits.max_total_bytes,
        max_output_bytes=limits.max_output_bytes,
        timeout_seconds=limits.timeout_seconds,
    )
    indexed = evidence_index(evidence_root, evidence_limits) if evidence_root.is_dir() else []
    return {
        "gitStatusLength": len(receipt.stdout),
        "gitStatusSha256": hashlib.sha256(receipt.stdout).hexdigest(),
        "stderrBytes": len(receipt.stderr),
        "evidenceFiles": len(indexed),
        "durationMs": receipt.duration_ms,
    }


def _verify_expansions(root: Path) -> dict[str, object]:
    curriculum = check_repository(root)
    traceability = _verify_repository(root)
    tools = _toolchain_verification(root)
    return {
        "curriculum": curriculum.as_dict(),
        "traceability": traceability.as_dict(),
        "toolchain": tools,
    }


def _run_focused_tests(root: Path) -> int:
    report: RepositoryReport = check_repository(root)
    present = tuple(item for item in _FOCUSED_TEST_PATHS if (root / item).is_file())
    if present != _FOCUSED_TEST_PATHS:
        print(json.dumps({"scaffold": report.as_dict()}, sort_keys=True, separators=(",", ":")))
        return 0
    runtime, interpreter, digest = validate_runtime()
    environment = controller_environment(runtime, digest)
    receipt = _run_owned_process(
        (
            str(interpreter),
            "-m",
            "unittest",
            "discover",
            "-s",
            "tests/learning/curriculum",
            "-p",
            "test_*.py",
        ),
        cwd=root,
        environment=environment,
        limits=RepositoryLimits(timeout_seconds=180, max_output_bytes=8 * 1024 * 1024),
    )
    os.write(1, receipt.stdout)
    os.write(2, receipt.stderr)
    return receipt.returncode


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="architecture_expansion")
    parser.add_argument(
        "command",
        choices=("run-focused-tests", "verify-expansions", "clean-handoff"),
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    arguments = _parser().parse_args(argv)
    root = Path.cwd().resolve()
    validate_runtime()
    if arguments.command == "run-focused-tests":
        return _run_focused_tests(root)
    if arguments.command == "verify-expansions":
        print(json.dumps(_verify_expansions(root), sort_keys=True, separators=(",", ":")))
        return 0
    print(json.dumps(_repository_handoff(root), sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
