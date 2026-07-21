"""Framework-neutral Stage A learning-contract public surface."""

from __future__ import annotations

from collections.abc import Sequence


def main(argv: Sequence[str] | None = None) -> int:
    """Load the command lazily so ``python -m`` has one module identity."""
    from .check import main as command_main

    return command_main(argv)


__all__ = ["main"]
