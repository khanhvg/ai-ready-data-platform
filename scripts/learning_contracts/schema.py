"""Closed Draft 2020-12 schema loading and validation."""
from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any

from .canonical import ContractError, parse_json

ROOT = Path(__file__).resolve().parents[2]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(relative: str) -> Any:
    path = ROOT / relative
    if not path.is_file() or path.is_symlink() or path.stat().st_size > 2 * 1024 * 1024:
        raise ContractError("CONTRACT_DESCRIPTOR_INVALID")
    return parse_json(path.read_bytes())


def validate(document: Any, schema_relative: str) -> None:
    from jsonschema import Draft202012Validator

    schema = load_json(schema_relative)
    Draft202012Validator.check_schema(schema)
    errors = sorted(Draft202012Validator(schema).iter_errors(document), key=lambda e: list(e.absolute_path))
    if not errors:
        return
    error = errors[0]
    pointer = "".join("/" + str(part).replace("~", "~0").replace("/", "~1") for part in error.absolute_path)
    code = {"required": "SCHEMA_REQUIRED_PROPERTY", "type": "SCHEMA_TYPE_MISMATCH", "unevaluatedProperties": "SCHEMA_UNKNOWN_PROPERTY", "additionalProperties": "SCHEMA_UNKNOWN_PROPERTY"}.get(error.validator, "SCHEMA_VALIDATION_FAILED")
    raise ContractError(code, pointer)
