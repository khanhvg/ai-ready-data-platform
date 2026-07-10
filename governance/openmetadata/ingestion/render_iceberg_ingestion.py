#!/usr/bin/env python3
"""Render/verify the Iceberg ingestion table filter from lake/curated_assets.json.

`iceberg_ingestion.yaml`'s `tableFilterPattern.includes` must list exactly the
curated assets `lake/publish_iceberg.py` publishes to the `retail` Iceberg
namespace -- this script is the single point that keeps the two from drifting
(plan risk R7). The Iceberg *namespace* itself (`retail`) is fixed by
`publish_iceberg.py`'s `CREATE SCHEMA IF NOT EXISTS lake.retail` and is not
derived from curated_assets.json's `schema` field, which names the *DuckDB*
schema (`main_marts`) dbt materializes into -- an unrelated axis.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[3]
CURATED_ASSETS_PATH = REPO_ROOT / "lake" / "curated_assets.json"
INGESTION_YAML_PATH = Path(__file__).resolve().parent / "iceberg_ingestion.yaml"

TABLE_FILTER_PATH = ("source", "sourceConfig", "config", "tableFilterPattern", "includes")


def render_table_filter_includes(curated_assets_path: Path = CURATED_ASSETS_PATH) -> list[str]:
    """Anchored-regex filter entries, one per curated Iceberg asset, sorted for a stable diff."""
    with curated_assets_path.open() as f:
        assets = json.load(f)["assets"]
    names = sorted(asset["name"] for asset in assets)
    return [f"^{name}$" for name in names]


def _get_nested(doc: dict, path: tuple[str, ...]) -> list[str]:
    node = doc
    for key in path[:-1]:
        node = node[key]
    return node[path[-1]]


def _set_nested(doc: dict, path: tuple[str, ...], value: list[str]) -> None:
    node = doc
    for key in path[:-1]:
        node = node[key]
    node[path[-1]] = value


def check(ingestion_yaml_path: Path = INGESTION_YAML_PATH) -> bool:
    """Return True if the committed table filter matches lake/curated_assets.json."""
    expected = render_table_filter_includes()
    with ingestion_yaml_path.open() as f:
        doc = yaml.safe_load(f)
    actual = _get_nested(doc, TABLE_FILTER_PATH)
    if actual != expected:
        print(
            f"DRIFT: {ingestion_yaml_path}'s tableFilterPattern.includes does not match "
            "lake/curated_assets.json.",
            file=sys.stderr,
        )
        print(f"  expected: {expected}", file=sys.stderr)
        print(f"  actual:   {actual}", file=sys.stderr)
        return False
    return True


def render(ingestion_yaml_path: Path = INGESTION_YAML_PATH) -> None:
    """Rewrite the table filter in place; every other key is left untouched."""
    expected = render_table_filter_includes()
    with ingestion_yaml_path.open() as f:
        doc = yaml.safe_load(f)
    _set_nested(doc, TABLE_FILTER_PATH, expected)
    with ingestion_yaml_path.open("w") as f:
        yaml.safe_dump(doc, f, sort_keys=False, default_flow_style=False)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="Verify the committed table filter matches curated_assets.json without "
        "rewriting the file; exits non-zero on drift.",
    )
    args = parser.parse_args()

    if args.check:
        sys.exit(0 if check() else 1)

    render()
    print(
        f"Rendered {len(render_table_filter_includes())} curated Iceberg table filter(s) "
        f"into {INGESTION_YAML_PATH}"
    )


if __name__ == "__main__":
    main()
