"""Pure legal-transition, CAS, and idempotency decisions."""
from __future__ import annotations

from typing import Any

LEGAL = {
    "not_started": {"preparing"}, "preparing": {"ready", "reset_pending", "failed"},
    "ready": {"running", "reset_pending"}, "running": {"controlled_failure", "verifying", "reset_pending", "failed"},
    "controlled_failure": {"diagnosing", "reset_pending"}, "diagnosing": {"running", "reset_pending"},
    "verifying": {"verified", "reset_pending", "failed"}, "verified": {"evidenced"},
    "evidenced": {"completed"}, "reset_pending": {"resetting"}, "resetting": {"ready", "failed"},
    "failed": {"reset_pending", "recovering"}, "recovering": {"ready", "failed"}, "completed": set(),
}


def code(value: dict[str, Any]) -> str:
    if "from" in value and value.get("to") not in LEGAL.get(value["from"], set()):
        return "STATE_TRANSITION_FORBIDDEN"
    if "expectedRevision" in value and value.get("expectedRevision") != value.get("actualRevision"):
        return "PROGRESS_VERSION_CONFLICT"
    if "storedRequestSha256" in value and value.get("storedRequestSha256") != value.get("requestSha256"):
        return "IDEMPOTENCY_KEY_REUSE"
    if value.get("effectCount", 1) != 1:
        return "IDEMPOTENCY_DUPLICATE_EFFECT"
    return "OK"
