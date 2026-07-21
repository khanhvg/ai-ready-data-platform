#!/usr/bin/env python3
"""Public Stage A command scaffold."""

from __future__ import annotations

import argparse
from collections.abc import Sequence


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="learning-contracts")
    parser.add_argument("command", nargs="?", choices=("check", "api", "evidence"))
    parser.parse_args(argv)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
