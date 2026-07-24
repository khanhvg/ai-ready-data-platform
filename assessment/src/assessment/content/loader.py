"""Bounded UTF-8 loaders for human-authored YAML and Markdown."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml
from yaml.tokens import AliasToken, AnchorToken

from assessment.content.markdown import validate_markdown
from assessment.domain.errors import ContentValidationError

MAX_AUTHORED_BYTES = 1_048_576


def _read_bounded_utf8(path: Path, *, maximum_bytes: int = MAX_AUTHORED_BYTES) -> str:
    try:
        size = path.stat().st_size
        if size > maximum_bytes:
            raise ContentValidationError(f"{path}: exceeds {maximum_bytes} byte limit")
        return path.read_bytes().decode("utf-8", errors="strict")
    except UnicodeDecodeError as error:
        raise ContentValidationError(f"{path}: content must be UTF-8") from error
    except OSError as error:
        raise ContentValidationError(f"{path}: cannot read content") from error


def load_yaml(path: Path, *, maximum_bytes: int = MAX_AUTHORED_BYTES) -> dict[str, Any]:
    text = _read_bounded_utf8(path, maximum_bytes=maximum_bytes)
    try:
        if any(isinstance(token, AliasToken | AnchorToken) for token in yaml.scan(text)):
            raise ContentValidationError(f"{path}: YAML anchors and aliases are not allowed")
        document = yaml.safe_load(text)
    except yaml.YAMLError as error:
        raise ContentValidationError(f"{path}: unsafe or malformed YAML") from error
    if not isinstance(document, dict):
        raise ContentValidationError(f"{path}: YAML document must be a mapping")
    return document


def load_markdown(path: Path, *, maximum_bytes: int = MAX_AUTHORED_BYTES) -> str:
    text = _read_bounded_utf8(path, maximum_bytes=maximum_bytes)
    validate_markdown(text, context=str(path))
    return text
