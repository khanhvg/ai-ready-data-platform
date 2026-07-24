"""Narrow persistence boundary for portable engagement folders."""

from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path
from typing import Any, Protocol


class EngagementStore(Protocol):
    """Storage operations required by later assessment services."""

    def create(self, engagement: Mapping[str, Any]) -> Path: ...

    def open(self, engagement_id: str) -> Path: ...

    def read_document(self, engagement_id: str, key: str) -> dict[str, Any]: ...

    def write_document(self, engagement_id: str, key: str, document: Mapping[str, Any]) -> None: ...

    def add_evidence(self, engagement_id: str, key: str, content: bytes) -> None: ...

    def list_engagements(self) -> list[str]: ...

    def snapshot(self, engagement_id: str) -> dict[str, str]: ...
