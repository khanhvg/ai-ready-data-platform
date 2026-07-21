"""Read-only prerequisite and hint evaluation."""

from __future__ import annotations

from typing import Any

def evaluate_guidance(state: dict[str, Any], request: dict[str, Any]) -> dict[str, Any]:
    action = request.get("action")
    if action not in {"hint", "reflection", "prerequisites"}:
        return {"allowed": False, "completes": False, "reason": "GUIDANCE_ACTION_UNKNOWN"}
    prerequisites = request.get("prerequisites", [])
    satisfied = set(state.get("satisfiedPrerequisites", []))
    missing = [item for item in prerequisites if item not in satisfied]
    return {
        "allowed": not missing,
        "completes": False,
        "missingPrerequisites": missing,
        "hint": "inspect-grains" if action == "hint" else None,
    }
