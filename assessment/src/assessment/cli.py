"""Offline CLI for contracts, portability, deterministic evaluation, and reports."""

from __future__ import annotations

import argparse
import dataclasses
import hashlib
import json
import os
import sys
from importlib import resources
from importlib.resources.abc import Traversable
from pathlib import Path
from typing import Any, Never

from assessment.content.schemas import load_schema
from assessment.domain.errors import AssessmentError, ContentValidationError
from assessment.engine.evaluator import evaluate_assessment
from assessment.frameworks import load_framework
from assessment.reporting.generator import generate_report, source_state_digest
from assessment.reporting.publication import publish_report
from assessment.reporting.renderer import render_report
from assessment.storage.archive import export_engagement, import_engagement
from assessment.storage.local import (
    LocalEngagementStore,
    _ensure_absolute_directory,
    atomic_write_at,
    canonical_json,
)
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


class MachineReadableArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> Never:
        raise ContentValidationError(f"invalid_arguments: {message}")


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
    parser = MachineReadableArgumentParser(prog="python -m assessment")
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

    for command_name, help_text in (
        ("evaluate", "evaluate one explicit engagement into deterministic JSON"),
        ("report", "generate canonical JSON and standalone HTML"),
    ):
        command = commands.add_parser(command_name, help=help_text)
        command.add_argument("--engagement-root", type=Path, required=True)
        command.add_argument("--output-root", type=Path, required=True)
    web = commands.add_parser("web", help="run the local server-rendered assessment workflow")
    web.add_argument("--engagement-root", type=Path, required=True)
    web.add_argument("--runtime-root", type=Path, required=True)
    web.add_argument(
        "--repository-root",
        type=Path,
        help="optional read-only repository root used only for demo artifact availability",
    )
    web.add_argument("--host", default="127.0.0.1")
    web.add_argument("--port", type=int, default=8765)
    web.add_argument(
        "--allow-unsupported-non-loopback",
        action="store_true",
        help="unsupported development override; never use for assessment data",
    )
    return parser


def _machine_error(code: str, error: Exception) -> int:
    print(
        json.dumps(
            {"error": {"code": code, "message": str(error)}},
            ensure_ascii=False,
            sort_keys=True,
        ),
        file=sys.stderr,
    )
    return 2


def _read_source(
    engagement_root: Path,
) -> tuple[
    dict[str, Any],
    dict[str, Any],
    dict[str, dict[str, str]],
    dict[str, str],
]:
    if engagement_root.is_symlink() or not engagement_root.is_dir():
        raise ValueError("engagement root must be a real local directory")
    store = LocalEngagementStore(engagement_root.parent)
    documents, source_snapshot = store.read_documents_and_snapshot(
        engagement_root.name,
        (
            "engagement.json",
            "assessment/quick.json",
            "findings/review.json",
        ),
    )
    engagement = documents["engagement.json"]
    answers = documents["assessment/quick.json"]
    if engagement is None or answers is None:
        raise ValueError("engagement and assessment answer documents are required")
    reviews: dict[str, dict[str, str]] = {}
    raw_reviews = documents["findings/review.json"]
    if raw_reviews is not None:
        records = raw_reviews.get("reviews", raw_reviews)
        if not isinstance(records, dict) or not all(
            isinstance(key, str) and isinstance(value, dict)
            for key, value in records.items()
        ):
            raise ValueError("findings/review.json: reviews must be an object")
        reviews = records
    return engagement, answers, reviews, source_snapshot


def _safe_output_root(engagement_root: Path, output_root: Path) -> int:
    engagement = engagement_root.resolve(strict=True)
    output = output_root.absolute()
    resolved_output = output.resolve(strict=False)
    if resolved_output == engagement or engagement in resolved_output.parents:
        raise ValueError("output root must not alias engagement source state")
    current = Path(output.anchor)
    for part in output.parts[1:]:
        current /= part
        if current.exists() and current.is_symlink():
            raise ValueError(f"output root contains a symlink component: {current.name}")
    try:
        return _ensure_absolute_directory(output)
    except (OSError, ValueError) as error:
        raise ValueError("output root must be a real local directory") from error


def _write_evaluation(
    engagement: dict[str, Any],
    answers: dict[str, Any],
    reviews: dict[str, dict[str, str]],
    source_snapshot: dict[str, str],
    output_descriptor: int,
) -> dict[str, Any]:
    framework = load_framework(str(engagement["framework_version"]))
    result = evaluate_assessment(
        answers,
        framework,
        reviews=reviews,
        expected_engagement_id=str(engagement["engagement_id"]),
    )
    source_digest = source_state_digest(
        engagement,
        answers,
        reviews,
        source_snapshot,
    )
    document = {
        "schema_version": "1.0.0",
        "framework_version": framework.version,
        "source_state_digest": source_digest,
        "result": dataclasses.asdict(result),
    }
    evaluation_bytes = canonical_json(document)
    atomic_write_at(output_descriptor, "assessment-result.json", evaluation_bytes)
    return {
        "artifact": "assessment-result.json",
        "sha256": hashlib.sha256(evaluation_bytes).hexdigest(),
        "source_state_digest": source_digest,
    }


def _run(arguments: argparse.Namespace) -> int:
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
    if arguments.command == "web":
        import uvicorn

        from assessment.web.app import create_app
        from assessment.web.config import WebConfig

        config = WebConfig.for_roots(
            arguments.engagement_root,
            arguments.runtime_root,
            repository_root=arguments.repository_root,
            host=str(arguments.host),
            port=int(arguments.port),
            allow_unsupported_non_loopback=bool(
                arguments.allow_unsupported_non_loopback
            ),
        )
        uvicorn.run(
            create_app(config=config),
            host=config.host,
            port=config.port,
            access_log=False,
            log_level="warning",
            workers=1,
        )
        return 0
    if arguments.command in {"evaluate", "report"}:
        engagement_root = arguments.engagement_root.absolute()
        engagement, answers, reviews, source_snapshot = _read_source(engagement_root)
        try:
            output_descriptor = _safe_output_root(
                engagement_root,
                arguments.output_root,
            )
        except ValueError as error:
            raise ContentValidationError(f"unsafe_output_root: {error}") from error
        try:
            if arguments.command == "evaluate":
                _emit(
                    _write_evaluation(
                        engagement,
                        answers,
                        reviews,
                        source_snapshot,
                        output_descriptor,
                    )
                )
                return 0
            generated = generate_report(
                engagement,
                answers,
                reviews=reviews,
                source_snapshot=source_snapshot,
            )
            report_document = json.loads(generated.json_bytes)
            html_bytes = render_report(report_document)
            artifact_digests = publish_report(
                output_descriptor,
                generated.json_bytes,
                html_bytes,
                generated.source_state_digest,
                writer=atomic_write_at,
            )
            _emit(
                {
                    "artifacts": artifact_digests,
                    "commit_manifest": "report-manifest.json",
                    "source_state_digest": generated.source_state_digest,
                }
            )
            return 0
        finally:
            os.close(output_descriptor)
    raise AssertionError("unreachable command")


def main(argv: list[str] | None = None) -> int:
    try:
        arguments = build_parser().parse_args(argv)
        return _run(arguments)
    except (AssessmentError, OSError, ValueError, KeyError, json.JSONDecodeError) as error:
        code = (
            "unsafe_output_root"
            if str(error).startswith("unsafe_output_root:")
            else "assessment_error"
        )
        return _machine_error(code, error)
