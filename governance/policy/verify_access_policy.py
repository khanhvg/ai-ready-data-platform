#!/usr/bin/env python3
"""Exercise the real fixed-interface policy CLI and retain bounded evidence."""

from __future__ import annotations

import csv
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

import duckdb

REPO_ROOT = Path(__file__).resolve().parents[2]
PYTHON = REPO_ROOT / ".venv" / "bin" / "python3"
CLI = REPO_ROOT / "governance" / "policy" / "export_authorized_dataset.py"
WAREHOUSE = REPO_ROOT / "warehouse" / "retail.duckdb"
OUTPUT = REPO_ROOT / "demo" / "evidence" / "current" / "ai-ready-customer-product.csv"
EVIDENCE = REPO_ROOT / "demo" / "evidence" / "current" / "policy-decisions.json"
SAFE_COLUMNS = (
    "order_key",
    "customer_key",
    "email_pseudonym",
    "loyalty_tier",
    "is_active",
    "order_date",
    "channel",
    "accepted_order_status",
    "order_total",
)


def _run(*arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [str(PYTHON), str(CLI), *arguments],
        cwd=REPO_ROOT,
        env={"PATH": os.environ.get("PATH", "")},
        text=True,
        capture_output=True,
        check=False,
    )


def _assert_denied(label: str, *arguments: str) -> dict[str, object]:
    result = _run(*arguments)
    if result.returncode == 0:
        raise AssertionError(f"{label} unexpectedly succeeded")
    return {"case": label, "exit_code": result.returncode, "decision": "denied"}


def main() -> int:
    if not WAREHOUSE.is_file():
        raise SystemExit("warehouse is unavailable; run make seed/load/dbt first")
    cases = [
        _assert_denied(
            "raw-denied",
            "--role-id",
            "demo-ai-consumer",
            "--asset-id",
            "raw-customers",
        ),
        _assert_denied(
            "staging-denied",
            "--role-id",
            "demo-ai-consumer",
            "--asset-id",
            "staging-customers",
        ),
        _assert_denied(
            "classified-email-denied",
            "--role-id",
            "demo-ai-consumer",
            "--asset-id",
            "customer-email-pii",
        ),
        _assert_denied(
            "unknown-role-denied",
            "--role-id",
            "unknown-role",
            "--asset-id",
            "ai-ready-customer-product",
        ),
        _assert_denied(
            "unknown-asset-denied",
            "--role-id",
            "demo-ai-consumer",
            "--asset-id",
            "unknown-asset",
        ),
        _assert_denied(
            "sql-input-rejected",
            "--role-id",
            "demo-ai-consumer",
            "--asset-id",
            "ai-ready-customer-product",
            "--sql",
            "select * from raw.customers",
        ),
        _assert_denied(
            "path-input-rejected",
            "--role-id",
            "demo-ai-consumer",
            "--asset-id",
            "ai-ready-customer-product",
            "--output-path",
            "/tmp/bypass.csv",
        ),
    ]
    allowed = _run(
        "--role-id",
        "demo-ai-consumer",
        "--asset-id",
        "ai-ready-customer-product",
    )
    if allowed.returncode != 0:
        raise AssertionError(f"safe export failed: {allowed.stderr.strip()}")
    with OUTPUT.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if not rows or tuple(rows[0]) != SAFE_COLUMNS:
        raise AssertionError("safe export is empty or has an unexpected schema")
    connection = duckdb.connect(str(WAREHOUSE), read_only=True)
    try:
        raw_emails = {
            row[0]
            for row in connection.execute(
                "select email from main_staging.stg_customers where email is not null"
            ).fetchall()
        }
    finally:
        connection.close()
    if any(value in raw_emails for row in rows for value in row.values()):
        raise AssertionError("safe export contains a raw customer email")
    cases.append({"case": "safe-product-allowed", "exit_code": 0, "decision": "allowed"})
    evidence = {
        "schema_version": "1.0.0",
        "runtime": {
            "python": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
            "duckdb": duckdb.__version__,
        },
        "cases": cases,
        "output": {
            "path": OUTPUT.relative_to(REPO_ROOT).as_posix(),
            "columns": list(SAFE_COLUMNS),
            "rows": len(rows),
            "sha256": hashlib.sha256(OUTPUT.read_bytes()).hexdigest(),
            "raw_email_absent": True,
        },
        "limitations": [
            "Application-level local demonstration only; this is not DuckDB IAM.",
            "A local machine owner can open DuckDB directly and bypass this entrypoint.",
        ],
    }
    EVIDENCE.parent.mkdir(parents=True, exist_ok=True)
    temporary = EVIDENCE.with_name(f".{EVIDENCE.name}.{os.getpid()}.tmp")
    try:
        with temporary.open("w", encoding="utf-8") as handle:
            json.dump(evidence, handle, sort_keys=True, separators=(",", ":"))
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, EVIDENCE)
    finally:
        temporary.unlink(missing_ok=True)
    print(
        "policy verification passed: "
        f"{len(cases) - 1} denied, 1 allowed, {len(rows)} safe rows"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
