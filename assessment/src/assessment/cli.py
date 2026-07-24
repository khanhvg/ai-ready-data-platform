"""Small offline CLI for Phase 2 contracts and portability operations."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from assessment.content.schemas import load_schema
from assessment.storage.archive import export_engagement, import_engagement
from assessment.storage.migrations import migrate_prototype_fixture


def _schema_paths(repository_root: Path) -> list[Path]:
    return sorted((repository_root / "assessment/contracts").glob("*-v1.schema.json")) + sorted(
        (repository_root / "demo/contracts").glob("*-v1.schema.json")
    )


def _emit(value: Any) -> None:
    print(json.dumps(value, ensure_ascii=False, sort_keys=True))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="python -m assessment")
    commands = parser.add_subparsers(dest="command", required=True)

    schema = commands.add_parser("schema", help="validate all v1 public JSON Schemas")
    schema.add_argument("--repo-root", type=Path, default=Path.cwd())

    migrate = commands.add_parser("migrate", help="migrate a prototype fixture to v1")
    migrate.add_argument("source", type=Path)
    migrate.add_argument("destination", type=Path)

    export = commands.add_parser("export", help="export an engagement folder")
    export.add_argument("source", type=Path)
    export.add_argument("archive", type=Path)

    import_parser = commands.add_parser("import", help="safely import an engagement archive")
    import_parser.add_argument("archive", type=Path)
    import_parser.add_argument("destination", type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    arguments = build_parser().parse_args(argv)
    if arguments.command == "schema":
        paths = _schema_paths(arguments.repo_root)
        for path in paths:
            load_schema(path)
        _emit({"schema_version": "1.0.0", "schemas": len(paths)})
        return 0
    if arguments.command == "migrate":
        _emit(migrate_prototype_fixture(arguments.source, arguments.destination))
        return 0
    if arguments.command == "export":
        _emit(export_engagement(arguments.source, arguments.archive))
        return 0
    if arguments.command == "import":
        _emit(import_engagement(arguments.archive, arguments.destination))
        return 0
    raise AssertionError("unreachable command")
