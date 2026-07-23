"""Generic bounded traceability repository entry point."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Sequence

from .check_curriculum import check_repository
from .content_io import RepositoryLimits, RepositoryReport, validate_runtime


def _verify_repository(
    root: Path | str = Path.cwd(),
    limits: RepositoryLimits = RepositoryLimits(),
) -> RepositoryReport:
    """Verify that traceability inputs are bounded and parseable."""

    return check_repository(Path(root), limits)


def main(argv: Sequence[str] | None = None) -> int:
    argv = tuple(sys.argv[1:] if argv is None else argv)
    if argv:
        raise SystemExit("check_traceability accepts no arguments")
    validate_runtime()
    report = _verify_repository(Path.cwd())
    print(json.dumps(report.as_dict(), sort_keys=True, separators=(",", ":")))
    return 0 if report.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
