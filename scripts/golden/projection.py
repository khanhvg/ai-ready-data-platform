#!/usr/bin/env python3
"""Raw drift normalization separated from semantic projection."""

from __future__ import annotations

import copy
from typing import Any


ALLOWED_RAW_DRIFT = (
    "/run/runId",
    "/run/startedAt",
    "/run/finishedAt",
    "/run/durationMs",
    "/run/workspaceLocator",
)


class ProjectionError(ValueError):
    pass


def normalize_raw(value: dict[str, Any], pointers: tuple[str, ...] = ALLOWED_RAW_DRIFT) -> dict[str, Any]:
    if pointers != ALLOWED_RAW_DRIFT:
        raise ProjectionError("DRIFT_POLICY_VIOLATION")
    normalized = copy.deepcopy(value)
    for pointer in pointers:
        parent: Any = normalized
        parts = pointer.lstrip("/").split("/")
        for part in parts[:-1]:
            if not isinstance(parent, dict) or part not in parent:
                parent = None; break
            parent = parent[part]
        if isinstance(parent, dict): parent.pop(parts[-1], None)
    return normalized


def assert_unique(items: list[dict[str, Any]], key: str) -> None:
    identities = [item[key] for item in items]
    if len(identities) != len(set(identities)):
        raise ProjectionError("PROJECTION_DUPLICATE_ID")
