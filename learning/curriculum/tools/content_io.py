"""Strict, bounded and deterministic content I/O primitives.

This module deliberately knows nothing about curriculum acceptance semantics.  It
only establishes the safe public request/result boundary used by every checker.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import hashlib
import json
import math
from pathlib import Path, PurePosixPath
import stat
from typing import Any, Mapping
import unicodedata

MAX_BYTES = 256 * 1024
MAX_DEPTH = 16
MAX_ARRAY = 256
MAX_STRING = 8 * 1024


class ContentInputError(ValueError):
    """A request failed generic parsing or filesystem admission."""


@dataclass(frozen=True)
class NormalizedRequest:
    payload: Mapping[str, Any]
    source: str = "memory"


@dataclass(frozen=True)
class CheckResult:
    entrypoint_id: str
    reached: bool
    codes: tuple[str, ...] = ()
    details: Mapping[str, Any] = field(default_factory=dict)

    @property
    def ok(self) -> bool:
        return self.reached and not self.codes


def _pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in items:
        if key in result:
            raise ContentInputError("duplicate JSON member")
        result[key] = value
    return result


def _walk(value: Any, depth: int = 0) -> Any:
    if depth > MAX_DEPTH:
        raise ContentInputError("maximum nesting depth exceeded")
    if value is None or isinstance(value, bool):
        return value
    if isinstance(value, int) and not isinstance(value, bool):
        if abs(value) > 9_007_199_254_740_991:
            raise ContentInputError("unsafe integer")
        return value
    if isinstance(value, float):
        if not math.isfinite(value):
            raise ContentInputError("non-finite number")
        return value
    if isinstance(value, str):
        if len(value.encode("utf-8")) > MAX_STRING:
            raise ContentInputError("string bound exceeded")
        return unicodedata.normalize("NFC", value)
    if isinstance(value, list):
        if len(value) > MAX_ARRAY:
            raise ContentInputError("array bound exceeded")
        return [_walk(item, depth + 1) for item in value]
    if isinstance(value, dict):
        normalized: dict[str, Any] = {}
        for key, item in value.items():
            if not isinstance(key, str):
                raise ContentInputError("object member is not text")
            normalized[_walk(key, depth + 1)] = _walk(item, depth + 1)
        return normalized
    raise ContentInputError(f"unsupported value type: {type(value).__name__}")


def normalize_request(value: Mapping[str, Any], *, source: str = "memory") -> NormalizedRequest:
    normalized = _walk(dict(value))
    if not isinstance(normalized, dict):
        raise ContentInputError("request must be an object")
    return NormalizedRequest(normalized, source)


def load_json(path: Path, *, max_bytes: int = MAX_BYTES) -> NormalizedRequest:
    info = path.lstat()
    if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1 or info.st_size > max_bytes:
        raise ContentInputError("source must be one bounded regular file")
    raw = path.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf") or len(raw) > max_bytes:
        raise ContentInputError("invalid JSON byte envelope")
    try:
        value = json.loads(
            raw.decode("utf-8"), object_pairs_hook=_pairs,
            parse_constant=lambda token: (_ for _ in ()).throw(ContentInputError(token)),
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ContentInputError("invalid JSON") from exc
    if not isinstance(value, dict):
        raise ContentInputError("document root must be an object")
    return normalize_request(value, source=path.as_posix())


def safe_relative_path(value: str) -> PurePosixPath:
    path = PurePosixPath(value)
    if path.is_absolute() or not path.parts or any(part in {"", ".", ".."} for part in path.parts):
        raise ContentInputError("path must be normalized and relative")
    return path


def canonical_bytes(value: Any) -> bytes:
    normalized = _walk(value)
    return json.dumps(normalized, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def content_sha256(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()
