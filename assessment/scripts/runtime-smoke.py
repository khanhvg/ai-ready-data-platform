#!/usr/bin/env python3
"""Produce retained Phase 4 browser/runtime evidence under an explicit root."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from assessment.web.runtime_smoke import run_browser_journey


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--evidence-root", type=Path, required=True)
    parser.add_argument("--repository-root", type=Path, required=True)
    arguments = parser.parse_args()
    result = run_browser_journey(
        arguments.evidence_root.absolute(),
        repository_root=arguments.repository_root.absolute(),
    )
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
