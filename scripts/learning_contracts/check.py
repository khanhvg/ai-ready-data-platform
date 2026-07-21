#!/usr/bin/env python3
"""Public Stage A command scaffold."""

from __future__ import annotations

import argparse
from collections.abc import Sequence

from .schema import LearningContractError


def validate_public_value(name: str, value: str) -> str:
    del name, value
    raise LearningContractError("LEARNING_PUBLIC_VALUE_NOT_IMPLEMENTED")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="learning-contracts")
    parser.add_argument("command", nargs="?", choices=("check", "api", "evidence"))
    parser.parse_args(argv)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
