"""Strict I-JSON parsing and RFC 8785 canonical serialization."""

from __future__ import annotations

import json
import math
from typing import Any

from .schema import LearningContractError
from scripts.golden.canonical import dumps as _jcs_dumps


def _pairs(values: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in values:
        if key in result:
            raise LearningContractError("JSON_DUPLICATE_NAME")
        result[key] = value
    return result


def _constant(_: str) -> None:
    raise LearningContractError("JSON_NON_IJSON_NUMBER")


def _walk(value: Any) -> None:
    if isinstance(value, str) and any(0xD800 <= ord(character) <= 0xDFFF for character in value):
        raise LearningContractError("JSON_LONE_SURROGATE")
    if isinstance(value, int) and not isinstance(value, bool) and abs(value) > 9_007_199_254_740_991:
        raise LearningContractError("JSON_INTEGER_UNSAFE")
    if isinstance(value, float) and not math.isfinite(value):
        raise LearningContractError("JSON_NON_IJSON_NUMBER")
    children = value.values() if isinstance(value, dict) else value if isinstance(value, list) else ()
    for child in children:
        _walk(child)


def parse_json(raw: bytes) -> Any:
    if raw.startswith(b"\xef\xbb\xbf"):
        raise LearningContractError("JSON_BOM_REFUSED")
    try:
        text = raw.decode("utf-8", "strict")
        decoder = json.JSONDecoder(object_pairs_hook=_pairs, parse_constant=_constant)
        value, end = decoder.raw_decode(text)
    except LearningContractError:
        raise
    except UnicodeDecodeError as exc:
        raise LearningContractError("JSON_UTF8_INVALID") from exc
    except (json.JSONDecodeError, ValueError) as exc:
        raise LearningContractError("JSON_INVALID") from exc
    if text[end:].strip():
        raise LearningContractError("JSON_TRAILING_CONTENT")
    _walk(value)
    return value


def canonical_bytes(value: Any) -> bytes:
    _walk(value)
    try:
        return _jcs_dumps(value)
    except (TypeError, ValueError, UnicodeError) as exc:
        raise LearningContractError("JCS_AMBIGUOUS_VALUE") from exc
