"""Typed canonical report artifact."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class GeneratedReport:
    json_bytes: bytes
    source_state_digest: str
