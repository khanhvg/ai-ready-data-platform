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
  (allow network-inbound (local ip "localhost:*"))
  (allow network-outbound (remote ip "localhost:*"))'

capability='assessment-loopback-capability-v1'
exec 9<<<"$capability"
exec env -u PYTHONPATH \
  ASSESSMENT_LOOPBACK_SANDBOX=1 \
  ASSESSMENT_LOOPBACK_CAPABILITY_FD=9 \
  sandbox-exec -p "$profile" "$@"
