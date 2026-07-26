#!/usr/bin/env python3
"""Export the one allowlisted governed product through a fixed local boundary."""

from __future__ import annotations

import argparse
import csv
import os
import re
import sys
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
POLICY_PATH = REPO_ROOT / "governance" / "policy" / "access-policy.yaml"
WAREHOUSE_PATH = REPO_ROOT / "warehouse" / "retail.duckdb"
OUTPUT_ROOT = REPO_ROOT / "demo" / "evidence" / "current"
SAFE_ASSET_ID = "ai-ready-customer-product"
SAFE_RELATION = "main_products.ai_ready_customer_product"
SAFE_OUTPUT_NAME = "ai-ready-customer-product.csv"
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
IDENTIFIER = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")


class PolicyError(RuntimeError):
    """Raised when checked policy content or an access decision is invalid."""


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Export the fixed governed AI-ready customer product. "
            "No SQL or filesystem path input is accepted."
        )
    )
    parser.add_argument("--role-id", required=True)
    parser.add_argument("--asset-id", required=True)
    return parser


def _mapping(value: object, context: str) -> dict[str, Any]:
    if not isinstance(value, dict) or any(not isinstance(key, str) for key in value):
        raise PolicyError(f"{context} must be a string-keyed mapping")
    return value


def _string_list(value: object, context: str) -> list[str]:
    if (
        not isinstance(value, list)
        or not value
        or any(not isinstance(item, str) or not IDENTIFIER.fullmatch(item) for item in value)
        or len(value) != len(set(value))
    ):
        raise PolicyError(f"{context} must be a non-empty unique stable-ID list")
    return value


def load_policy() -> dict[str, Any]:
    if (
        POLICY_PATH.is_symlink()
        or not POLICY_PATH.is_file()
        or POLICY_PATH.resolve(strict=True).parent
        != (REPO_ROOT / "governance" / "policy").resolve(strict=True)
    ):
        raise PolicyError("checked access policy path is unavailable or unsafe")
    try:
        document = yaml.safe_load(POLICY_PATH.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, yaml.YAMLError) as error:
        raise PolicyError("checked access policy is unavailable or invalid") from error
    policy = _mapping(document, "policy")
    if set(policy) != {
        "schema_version",
        "policy_id",
        "policy_version",
        "roles",
        "assets",
        "limitations",
    }:
        raise PolicyError("policy has unexpected or missing top-level keys")
    if (
        policy["schema_version"] != "1.0.0"
        or policy["policy_id"] != "local-ai-ready-customer-export"
        or policy["policy_version"] != "1.0.0"
    ):
        raise PolicyError("policy identity is invalid")
    roles = _mapping(policy["roles"], "roles")
    assets = _mapping(policy["assets"], "assets")
    if set(roles) != {"demo-ai-consumer"}:
        raise PolicyError("policy must define exactly the fixed demo role")
    role = _mapping(roles["demo-ai-consumer"], "demo role")
    if set(role) != {"allow", "deny"}:
        raise PolicyError("demo role decision keys are invalid")
    allowed = _string_list(role["allow"], "demo role allow list")
    denied = _string_list(role["deny"], "demo role deny list")
    if allowed != [SAFE_ASSET_ID] or set(allowed) & set(denied):
        raise PolicyError("policy allow list is not the fixed safe asset")
    if set(denied) != {"raw-customers", "staging-customers", "customer-email-pii"}:
        raise PolicyError("policy deny list is incomplete")
    if set(assets) != set(allowed + denied):
        raise PolicyError("policy role and asset inventories differ")
    safe = _mapping(assets[SAFE_ASSET_ID], "safe asset")
    if safe != {
        "decision": "governed-export",
        "relation": SAFE_RELATION,
        "output": "demo/evidence/current/ai-ready-customer-product.csv",
        "columns": list(SAFE_COLUMNS),
    }:
        raise PolicyError("safe asset contract differs from the fixed implementation")
    for asset_id in denied:
        denied_asset = _mapping(assets[asset_id], f"denied asset {asset_id}")
        if denied_asset.get("decision") != "deny":
            raise PolicyError(f"denied asset {asset_id} is not fail-closed")
    limitations = policy["limitations"]
    if not isinstance(limitations, list) or len(limitations) < 3:
        raise PolicyError("policy limitations are incomplete")
    return policy


def authorize(policy: dict[str, Any], role_id: str, asset_id: str) -> None:
    if not IDENTIFIER.fullmatch(role_id) or not IDENTIFIER.fullmatch(asset_id):
        raise PolicyError("role and asset IDs must be stable identifiers")
    roles = _mapping(policy["roles"], "roles")
    role = roles.get(role_id)
    if not isinstance(role, dict):
        raise PolicyError("access denied: unknown role")
    denied = role.get("deny", [])
    allowed = role.get("allow", [])
    if asset_id in denied:
        raise PolicyError("access denied: classified raw or staging asset")
    if asset_id not in allowed:
        raise PolicyError("access denied: unknown or unapproved asset")
    asset = _mapping(_mapping(policy["assets"], "assets").get(asset_id), "asset")
    if asset.get("decision") != "governed-export" or asset_id != SAFE_ASSET_ID:
        raise PolicyError("access denied: asset has no governed export")


def _prepare_output_root() -> None:
    for candidate in (OUTPUT_ROOT.parent, OUTPUT_ROOT):
        if candidate.is_symlink():
            raise PolicyError("fixed output root cannot contain a symbolic link")
    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
    expected_root = REPO_ROOT.resolve(strict=True).joinpath(
        "demo", "evidence", "current"
    )
    if OUTPUT_ROOT.is_symlink() or OUTPUT_ROOT.resolve(strict=True) != expected_root:
        raise PolicyError("fixed output root resolved outside the repository")


def export_safe_product() -> Path:
    import duckdb

    if (
        WAREHOUSE_PATH.is_symlink()
        or not WAREHOUSE_PATH.is_file()
        or WAREHOUSE_PATH.resolve(strict=True).parent
        != (REPO_ROOT / "warehouse").resolve(strict=True)
    ):
        raise PolicyError("warehouse is unavailable; run the core pipeline first")
    _prepare_output_root()
    output_path = OUTPUT_ROOT / SAFE_OUTPUT_NAME
    if output_path.is_symlink():
        raise PolicyError("fixed output file cannot be a symbolic link")
    temporary_path = OUTPUT_ROOT / f".{SAFE_OUTPUT_NAME}.{os.getpid()}.tmp"
    try:
        try:
            connection = duckdb.connect(str(WAREHOUSE_PATH), read_only=True)
            try:
                cursor = connection.execute(
                    "select "
                    + ", ".join(SAFE_COLUMNS)
                    + f" from {SAFE_RELATION} order by order_key"
                )
                rows = cursor.fetchall()
                actual_columns = tuple(item[0] for item in cursor.description)
            finally:
                connection.close()
        except duckdb.Error as error:
            raise PolicyError("governed product query failed") from error
        if actual_columns != SAFE_COLUMNS:
            raise PolicyError("safe product output schema differs from the allowlist")
        with temporary_path.open("x", encoding="utf-8", newline="") as handle:
            writer = csv.writer(handle, lineterminator="\n")
            writer.writerow(SAFE_COLUMNS)
            writer.writerows(rows)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary_path, output_path)
        directory_fd = os.open(OUTPUT_ROOT, os.O_RDONLY)
        try:
            os.fsync(directory_fd)
        finally:
            os.close(directory_fd)
    finally:
        temporary_path.unlink(missing_ok=True)
    return output_path


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        policy = load_policy()
        authorize(policy, args.role_id, args.asset_id)
        output_path = export_safe_product()
    except PolicyError as error:
        print(f"policy export failed: {error}", file=sys.stderr)
        return 3
    print(output_path.relative_to(REPO_ROOT).as_posix())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
