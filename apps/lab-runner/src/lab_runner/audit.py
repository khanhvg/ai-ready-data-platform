"""Canonical hash-chain helpers."""
from __future__ import annotations
import hashlib, json
from typing import Any


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")


def chained(previous: str, sequence: int, event: dict[str, Any]) -> tuple[bytes, str]:
    payload = canonical({"sequence": sequence, "previousSha256": previous, "event": event})
    return payload, hashlib.sha256(payload).hexdigest()
