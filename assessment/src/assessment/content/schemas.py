"""Load and apply authoritative JSON Schemas."""

from __future__ import annotations

import json
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError

from assessment.domain.errors import ContentValidationError


def load_schema(path: Path) -> dict[str, Any]:
    try:
        schema = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ContentValidationError(f"{path}: invalid JSON Schema document") from error
    if not isinstance(schema, dict):
        raise ContentValidationError(f"{path}: schema must be an object")
    try:
        Draft202012Validator.check_schema(schema)
    except SchemaError as error:
        raise ContentValidationError(f"{path}: invalid JSON Schema") from error
    return schema


def validate_document(document: Mapping[str, Any], schema_path: Path) -> None:
    validator = Draft202012Validator(load_schema(schema_path))
    errors = sorted(validator.iter_errors(document), key=lambda item: list(item.absolute_path))
    if errors:
        first = errors[0]
        location = ".".join(str(part) for part in first.absolute_path) or "<root>"
        raise ContentValidationError(f"{schema_path.name}:{location}: {first.message}")
