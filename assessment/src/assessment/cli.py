"""Small offline CLI for Phase 2 contracts and portability operations."""

from __future__ import annotations

import argparse
import json
import sys
from importlib import resources
from importlib.resources.abc import Traversable
from pathlib import Path
from typing import Any

from assessment.content.schemas import load_schema
from assessment.domain.errors import ContentValidationError
from assessment.storage.archive import export_engagement, import_engagement
from assessment.storage.migrations import migrate_prototype_fixture

PUBLIC_SCHEMA_FILENAMES = (
    "ai-ready-dataset-manifest-v1.schema.json",
    "answer-v1.schema.json",
    "demo-stage-manifest-v1.schema.json",
    "engagement-v1.schema.json",
    "framework-v1.schema.json",
    "recipe-v1.schema.json",
    "report-v1.schema.json",
)


def _require_complete_schema_authority(
    paths: list[Path | Traversable], *, context: str
) -> list[Path | Traversable]:
    discovered = {path.name for path in paths}
    expected = set(PUBLIC_SCHEMA_FILENAMES)
    if not paths:
        raise ContentValidationError(f"{context}: no public JSON Schema authority found")
    if discovered != expected:
        missing = ", ".join(sorted(expected - discovered))
        unexpected = ", ".join(sorted(discovered - expected))
        details = "; ".join(
            detail
            for detail in (
                f"missing: {missing}" if missing else "",
                f"unexpected: {unexpected}" if unexpected else "",
            )
            if detail
        )
        raise ContentValidationError(
            f"{context}: incomplete public JSON Schema authority ({details})"
        )
    return sorted(paths, key=lambda path: path.name)


def _schema_paths(repository_root: Path | None) -> list[Path | Traversable]:
    if repository_root is None:
        packaged_root = resources.files("assessment.public_schemas")
        packaged = [
            packaged_root.joinpath(filename) for filename in PUBLIC_SCHEMA_FILENAMES
        ]
        existing = [path for path in packaged if path.is_file()]
        return _require_complete_schema_authority(existing, context="installed package")
    repository = [
        *(
            repository_root / "assessment" / "contracts" / filename
            for filename in PUBLIC_SCHEMA_FILENAMES
            if filename
            not in {
                "ai-ready-dataset-manifest-v1.schema.json",
                "demo-stage-manifest-v1.schema.json",
            }
        ),
        *(
            repository_root / "demo" / "contracts" / filename
            for filename in PUBLIC_SCHEMA_FILENAMES
            if filename
            in {
                "ai-ready-dataset-manifest-v1.schema.json",
                "demo-stage-manifest-v1.schema.json",
            }
        ),
    ]
    existing = [path for path in repository if path.is_file()]
    return _require_complete_schema_authority(existing, context=str(repository_root))


def _emit(value: Any) -> None:
    print(json.dumps(value, ensure_ascii=False, sort_keys=True))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="python -m assessment")
    commands = parser.add_subparsers(dest="command", required=True)

    schema = commands.add_parser("schema", help="validate all v1 public JSON Schemas")
    schema.add_argument("--repo-root", type=Path)

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
        try:
            paths = _schema_paths(arguments.repo_root)
        except ContentValidationError as error:
            print(str(error), file=sys.stderr)
            return 2
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
