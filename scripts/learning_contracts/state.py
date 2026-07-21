"""One-authority learning state transitions."""

from __future__ import annotations

from typing import Any

from .schema import LearningContractError


def validate_progress_semantics(value: dict[str, Any]) -> None:
    """Enforce monotonic revisions and the sole completion authority beyond JSON shape."""
    revision = value.get("revision")
    events = value.get("events")
    if not isinstance(revision, int) or not isinstance(events, list):
        raise LearningContractError("PROGRESS_SEMANTICS_INVALID")
    revisions = [event.get("revision") for event in events if isinstance(event, dict)]
    if revisions != sorted(set(revisions)) or any(not isinstance(item, int) or item > revision for item in revisions):
        raise LearningContractError("PROGRESS_EVENT_ORDER_INVALID")
    completion = value.get("completion")
    if completion is not None and (value.get("state") != "completed" or completion.get("authority") != "learning-progress-authority-v1"):
        raise LearningContractError("COMPLETION_AUTHORITY_INVALID")


def validate_state_semantics(value: dict[str, Any]) -> None:
    """Validate idempotency, transition, and CAS invariants on persisted state."""
    if value.get("effectCount", 0) > 1:
        raise LearningContractError("IDEMPOTENCY_DUPLICATE_EFFECT")
    if "storedRequestSha256" in value and value.get("storedRequestSha256") != value.get("requestSha256"):
        raise LearningContractError("IDEMPOTENCY_KEY_REUSE")
    if value.get("from") == "not_started" and value.get("to") == "completed":
        raise LearningContractError("STATE_TRANSITION_FORBIDDEN")
    if "expectedRevision" in value and value.get("expectedRevision") != value.get("actualRevision"):
        raise LearningContractError("PROGRESS_VERSION_CONFLICT")


def execute_operation(state: dict[str, Any], request: dict[str, Any]) -> dict[str, Any]:
    if request.get("expectedRevision") != state.get("revision"):
        raise LearningContractError("PROGRESS_VERSION_CONFLICT")
    action = request.get("action")
    if action == "start":
        if not request.get("prerequisitesSatisfied"):
            raise LearningContractError("PREREQUISITE_REQUIRED")
        if state.get("state") not in {"not-started", "reset"}:
            raise LearningContractError("STATE_TRANSITION_INVALID")
        target = "in-progress"
    elif action == "verify":
        if state.get("state") != "in-progress":
            raise LearningContractError("STATE_TRANSITION_INVALID")
        target = "verified"
    elif action in {"reset", "rollback"}:
        target = "not-started"
    else:
        raise LearningContractError("STATE_OPERATION_UNKNOWN")
    state["state"] = target
    state["revision"] += 1
    state.setdefault("effects", []).append({"kind": action, "revision": state["revision"]})
    return {"state": target, "revision": state["revision"]}
