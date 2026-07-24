#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
lock_venv="$(mktemp -d)"
trap 'rm -rf "$lock_venv"' EXIT

python3.12 -m venv "$lock_venv"
"$lock_venv/bin/pip" install --quiet "pip==25.1.1" "pip-tools==7.5.0"
cd "$repo_root/assessment"
"$lock_venv/bin/pip-compile" --allow-unsafe --generate-hashes --resolver=backtracking \
  --output-file requirements.lock requirements.in
"$lock_venv/bin/pip-compile" --allow-unsafe --generate-hashes --resolver=backtracking \
  --output-file requirements-dev.lock requirements-dev.in
