"""Non-executing prerequisite probe and progressive-hint validation."""
from __future__ import annotations

from .canonical import ContractError

FORBIDDEN = {"shell", "argv", "sql", "url", "writablePath", "environment"}


def validate_probe(probe: dict[str, object], result: str) -> str:
    if FORBIDDEN.intersection(probe): raise ContractError("PROBE_MUTATION_FORBIDDEN")
    if result == "unavailable" and probe.get("required") is True: raise ContractError("PROBE_REQUIRED_UNAVAILABLE")
    if result == "unavailable": return "not-run-optional"
    if result not in {"pass", "fail"}: raise ContractError("PROBE_OPTIONAL_FALSE_PASS")
    return result


def validate_hints(hints: list[dict[str, object]]) -> None:
    orders = [hint.get("order") for hint in hints]
    if orders != list(range(1, len(hints) + 1)): raise ContractError("HINT_ORDER_INVALID")
    if any(hint.get("completes") for hint in hints): raise ContractError("HINT_COMPLETION_FORBIDDEN")
    if any(hint.get("revealed") and not hint.get("preconditionMet") for hint in hints): raise ContractError("HINT_REVEAL_FORBIDDEN")
