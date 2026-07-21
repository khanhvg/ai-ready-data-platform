#!/usr/bin/env python3
"""Strict I-JSON parsing and RFC 8785 canonical serialization."""

from __future__ import annotations

import json
import math
from typing import Any

import rfc8785


class CanonicalizationError(ValueError):
    pass


def _pairs(values: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in values:
        if key in result:
            raise CanonicalizationError("JSON_DUPLICATE_NAME")
        result[key] = value
    return result


def _invalid_constant(value: str) -> None:
    raise CanonicalizationError(f"JSON_NON_IJSON_NUMBER:{value}")


def _validate(value: Any) -> None:
    if isinstance(value, str):
        if any(0xD800 <= ord(character) <= 0xDFFF for character in value):
            raise CanonicalizationError("JSON_LONE_SURROGATE")
    elif isinstance(value, float) and not math.isfinite(value):
        raise CanonicalizationError("JSON_NON_IJSON_NUMBER")
    elif isinstance(value, dict):
        for key, child in value.items():
            _validate(key); _validate(child)
    elif isinstance(value, (list, tuple)):
        for child in value: _validate(child)


def parse_json(raw: bytes) -> Any:
    if raw.startswith(b"\xef\xbb\xbf"):
        raise CanonicalizationError("JSON_BOM_REFUSED")
    try:
        text = raw.decode("utf-8", "strict")
        value = json.loads(text, object_pairs_hook=_pairs, parse_constant=_invalid_constant)
    except CanonicalizationError:
        raise
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise CanonicalizationError("JSON_INVALID") from exc
    _validate(value)
    return value


def dumps(value: Any) -> bytes:
    _validate(value)
    try:
        return rfc8785.dumps(value)
    except (rfc8785.CanonicalizationError, UnicodeError) as exc:
        raise CanonicalizationError("JCS_UNSUPPORTED_VALUE") from exc
