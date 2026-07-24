#!/usr/bin/env bash
set -euo pipefail

if ! command -v sandbox-exec >/dev/null 2>&1; then
  echo "Phase 1 offline verification requires macOS sandbox-exec." >&2
  exit 2
fi

exec sandbox-exec -p '(version 1) (allow default) (deny network*)' "$@"
