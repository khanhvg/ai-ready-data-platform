"""Strict I-JSON parsing with the shipped RFC 8785 serializer."""
from __future__ import annotations

import json
import math
from typing import Any

from scripts.golden.canonical import dumps


class _Duplicate(ValueError):
    pass


def _pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in items:
        if key in result:
            raise _Duplicate
        result[key] = value
    return result


def _walk(value: Any) -> str:
    if isinstance(value, str) and any(0xD800 <= ord(character) <= 0xDFFF for character in value):
        return "JSON_LONE_SURROGATE"
    if isinstance(value, bool) or value is None:
        return "OK"
    if isinstance(value, float) and not math.isfinite(value):
        return "JSON_NON_IJSON_NUMBER"
    if isinstance(value, int) and abs(value) > 9007199254740991:
        return "JSON_INTEGER_UNSAFE"
    children = value.values() if isinstance(value, dict) else value if isinstance(value, list) else ()
    for child in children:
        code = _walk(child)
        if code != "OK":
            return code
    return "OK"


def parse(raw: bytes) -> tuple[str, Any | None]:
    if raw.startswith(b"\xef\xbb\xbf"):
        return "JSON_BOM_FORBIDDEN", None
    try:
        text = raw.decode("utf-8", "strict")
    except UnicodeDecodeError:
        return "JSON_UTF8_INVALID", None
    decoder = json.JSONDecoder(object_pairs_hook=_pairs, parse_constant=lambda _: (_ for _ in ()).throw(ValueError()))
    try:
        value, end = decoder.raw_decode(text)
    except _Duplicate:
        return "JSON_DUPLICATE_NAME", None
    except ValueError:
        if any(token in text for token in ("NaN", "Infinity")):
            return "JSON_NON_IJSON_NUMBER", None
        return "JSON_INVALID", None
    if text[end:].strip():
        return "JSON_TRAILING_CONTENT", None
    code = _walk(value)
    return code, value if code == "OK" else None


def code(value: Any) -> str:
    if isinstance(value, bytes):
        return parse(value)[0]
    return _walk(value)
