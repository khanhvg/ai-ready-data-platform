#!/usr/bin/env python3
"""Public Stage A command scaffold."""

from __future__ import annotations

import argparse
import pathlib
import re
from collections.abc import Sequence

from .schema import LearningContractError


def validate_public_value(name: str, value: str) -> str:
    if not isinstance(value, str) or not value or len(value) > 256 or "\x00" in value:
        raise LearningContractError("PUBLIC_ARGUMENT_INVALID")
    if name == "LESSON":
        if re.fullmatch(r"[a-z0-9][a-z0-9-]{0,63}", value) is None:
            raise LearningContractError("PUBLIC_ARGUMENT_INVALID")
        return value
    if name == "EVIDENCE":
        candidate = pathlib.PurePosixPath(value)
        secret = re.search(r"(?:AKIA[0-9A-Z]{16}|[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,})", value)
        if (
            candidate.is_absolute()
            or any(part in {"", ".", ".."} for part in candidate.parts)
            or "\\" in value
            or secret
            or re.search(r"[;&|`$<>(){}!\n\r]", value)
        ):
            raise LearningContractError("PUBLIC_ARGUMENT_INVALID")
        return value
    raise LearningContractError("PUBLIC_ARGUMENT_INVALID")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="learning-contracts")
    parser.add_argument("command", nargs="?", choices=("check", "api", "evidence"))
    parser.add_argument("--lesson")
    parser.add_argument("--evidence")
    arguments = parser.parse_args(argv)
    if arguments.lesson is not None:
        validate_public_value("LESSON", arguments.lesson)
    if arguments.evidence is not None:
        validate_public_value("EVIDENCE", arguments.evidence)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
