"""Generic bounded curriculum repository entry point."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Sequence

from .content_io import RepositoryLimits, RepositoryReport, inspect_repository, validate_runtime


def check_repository(
    root: Path | str = Path.cwd(),
    limits: RepositoryLimits = RepositoryLimits(),
) -> RepositoryReport:
    """Traverse and parse a repository without applying curriculum semantics."""

    return inspect_repository(Path(root), limits)


def main(argv: Sequence[str] | None = None) -> int:
    argv = tuple(sys.argv[1:] if argv is None else argv)
    if argv:
        raise SystemExit("check_curriculum accepts no arguments")
    validate_runtime()
    report = check_repository(Path.cwd())
    print(json.dumps(report.as_dict(), sort_keys=True, separators=(",", ":")))
    return 0 if report.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
