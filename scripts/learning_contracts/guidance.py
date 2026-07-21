"""Non-mutating prerequisite probe and ordered hint semantics."""
from __future__ import annotations

from typing import Any

PROMOTION_FIXTURE_SHA = "0a1dcd4023648f52009bfd4dc5d529c00ce66f42cd0e725732b972b0b78df341"


def code(value: dict[str, Any]) -> str:
    if any(key in value for key in ("command", "argv", "writablePath", "rawSql", "networkDestination", "environment")):
        return "PROBE_MUTATION_FORBIDDEN"
    if "hints" in value:
        orders = [hint.get("order") for hint in value["hints"]]
        if orders != sorted(orders) or orders != list(range(1, len(orders) + 1)):
            return "HINT_ORDER_INVALID"
    if value.get("completionMutation"):
        return "HINT_COMPLETION_FORBIDDEN"
    if value.get("required") and value.get("status") == "unavailable":
        return "PROBE_REQUIRED_UNAVAILABLE"
    if value.get("required") is False and value.get("status") == "unavailable" and value.get("result") == "pass":
        return "PROBE_OPTIONAL_FALSE_PASS"
    if value.get("revealed") and not value.get("revealAuthorized"):
        return "HINT_REVEAL_FORBIDDEN"
    return "OK"


def promotion_code(value: dict[str, Any]) -> str:
    if value.get("commonGrain"):
        return "PROMOTION_COMMON_GRAIN_FORBIDDEN"
    if "limitations" in value and not value["limitations"]:
        return "PROMOTION_LIMITATION_REQUIRED"
    if "fixtureSha256" in value and value["fixtureSha256"] != PROMOTION_FIXTURE_SHA:
        return "PROMOTION_FIXTURE_HASH_MISMATCH"
    return "OK"
