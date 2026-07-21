"""Single completion authority and deterministic orphan reconciliation."""
from __future__ import annotations

from typing import Any

AUTHORITY = "learning-progress-authority-v1"


def code(value: dict[str, Any]) -> str:
    source = value.get("completionSource")
    if source == "browser":
        return "COMPLETION_AUTHORITY_REQUIRED"
    if source in {"operation-result", "evidence-presence"}:
        return "COMPLETION_DUAL_TRUTH"
    if value.get("orphan") and value.get("attemptsCompletion"):
        return "RECONCILIATION_ORPHAN_CANNOT_COMPLETE"
    if value.get("orphan") and value.get("declaredSha256") != value.get("actualSha256"):
        return "RECONCILIATION_HASH_MISMATCH"
    return "OK"
