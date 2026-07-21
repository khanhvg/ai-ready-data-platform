"""One-authority learning state transitions."""

from __future__ import annotations

from typing import Any

from .schema import LearningContractError


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
