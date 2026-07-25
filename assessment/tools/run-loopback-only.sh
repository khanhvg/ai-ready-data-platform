#!/usr/bin/env bash
set -euo pipefail

if ! command -v sandbox-exec >/dev/null 2>&1; then
  echo "Loopback browser verification requires macOS sandbox-exec." >&2
  exit 2
fi

profile='(version 1)
  (allow default)
  (deny network*)
  (allow network* (local unix-socket))
  (allow network* (local ip "localhost:*"))
  (allow network-outbound (remote ip "localhost:*"))'

exec env -u PYTHONPATH sandbox-exec -p "$profile" "$@"
