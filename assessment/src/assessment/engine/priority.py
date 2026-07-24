"""Versioned ordinal finding priority."""

from __future__ import annotations

PRIORITY_ORDER = (
    "Critical blocker",
    "High-priority foundation",
    "Near-term improvement",
    "Strategic enhancement",
)


def select_priority(
    score: int | None,
    *,
    triggered_gate: bool = False,
    cross_domain_blocker: bool = False,
    target_level_four: bool = False,
) -> str | None:
    if triggered_gate:
        return PRIORITY_ORDER[0]
    if score is None:
        return None
    if score <= 1 or cross_domain_blocker:
        return PRIORITY_ORDER[1]
    if score == 2:
        return PRIORITY_ORDER[2]
    if score == 3 and target_level_four:
        return PRIORITY_ORDER[3]
    return None
