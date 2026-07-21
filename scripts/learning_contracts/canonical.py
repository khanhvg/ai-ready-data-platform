"""Strict I-JSON parsing and RFC 8785 canonicalization."""
from __future__ import annotations

import json
import math
from typing import Any

class ContractError(ValueError):
    def __init__(self, code: str, pointer: str = "") -> None:
        super().__init__(code)
        self.code = code
        self.pointer = pointer


def _pairs(values: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in values:
        if key in result:
            raise ContractError("JSON_DUPLICATE_NAME")
        result[key] = value
    return result


def _constant(_value: str) -> None:
    raise ContractError("JSON_NON_IJSON_NUMBER")


def _walk(value: Any, pointer: str = "") -> None:
    if isinstance(value, str):
        if any(0xD800 <= ord(character) <= 0xDFFF for character in value):
            raise ContractError("JSON_LONE_SURROGATE", pointer)
    elif isinstance(value, int) and not isinstance(value, bool):
        if abs(value) > 9007199254740991:
            raise ContractError("JSON_INTEGER_UNSAFE", pointer)
    elif isinstance(value, float):
        if not math.isfinite(value):
            raise ContractError("JSON_NON_IJSON_NUMBER", pointer)
    elif isinstance(value, dict):
        for key, child in value.items():
            _walk(key, pointer)
            _walk(child, pointer + "/" + key.replace("~", "~0").replace("/", "~1"))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            _walk(child, f"{pointer}/{index}")


def parse_json(raw: bytes) -> Any:
    if raw.startswith(b"\xef\xbb\xbf"):
        raise ContractError("JSON_BOM_FORBIDDEN")
    try:
        text = raw.decode("utf-8", "strict")
    except UnicodeDecodeError as exc:
        raise ContractError("JSON_UTF8_INVALID") from exc
    decoder = json.JSONDecoder(object_pairs_hook=_pairs, parse_constant=_constant)
    try:
        value, end = decoder.raw_decode(text)
    except ContractError:
        raise
    except json.JSONDecodeError as exc:
        raise ContractError("JSON_INVALID") from exc
    if text[end:].strip():
        raise ContractError("JSON_TRAILING_CONTENT")
    _walk(value)
    return value


def dumps(value: Any) -> bytes:
    _walk(value)
    try:
        from scripts.golden.canonical import dumps as golden_dumps

        return golden_dumps(value)
    except Exception as exc:
        raise ContractError("JCS_UNSUPPORTED_VALUE") from exc
