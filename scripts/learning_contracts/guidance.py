"""Read-only prerequisite and hint evaluation."""

from __future__ import annotations

from typing import Any

from .schema import LearningContractError


def validate_probe(value: dict[str, Any]) -> None:
    required = {"probeId", "kind", "class", "expected", "remediation", "retry"}
    if set(value) != required or value.get("kind") not in {"contract", "fixture", "tool", "state"} or value.get("class") not in {"required", "optional"}:
        raise LearningContractError("PROBE_INVALID")
    forbidden = {"shell", "argv", "path", "sql", "url", "environment", "command"}
    if forbidden & set(value) or value.get("expected") not in {"pass", "fail", "unavailable"}:
        raise LearningContractError("PROBE_UNSAFE")


def validate_hints(value: list[dict[str, Any]]) -> None:
    expected = 1
    for hint in value:
        if set(hint) != {"hintId", "order", "revealAfter", "evidenceEvent"} or hint.get("order") != expected or hint.get("evidenceEvent") != "guidance-viewed":
            raise LearningContractError("HINT_ORDER_INVALID")
        expected += 1


def validate_guidance_semantics(value: dict[str, Any]) -> None:
    """Enforce read-only hints and declarative, non-mutating probes."""
    if value.get("completionMutation"):
        raise LearningContractError("HINT_COMPLETION_FORBIDDEN")
    if "command" in value:
        raise LearningContractError("PROBE_MUTATION_FORBIDDEN")
    if value.get("status") == "unavailable" and value.get("result") == "pass":
        code = "PROBE_REQUIRED_UNAVAILABLE" if value.get("required") else "PROBE_OPTIONAL_FALSE_PASS"
        raise LearningContractError(code)
    if value.get("revealed") and not value.get("revealAuthorized"):
        raise LearningContractError("HINT_REVEAL_FORBIDDEN")

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
