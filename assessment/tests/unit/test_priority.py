from __future__ import annotations

from assessment.engine.priority import select_priority


def test_priority_table_boundaries_are_ordinal_and_deterministic() -> None:
    assert select_priority(4) is None
    assert select_priority(3, target_level_four=True) == "Strategic enhancement"
    assert select_priority(2) == "Near-term improvement"
    assert select_priority(1) == "High-priority foundation"
    assert select_priority(0) == "High-priority foundation"
    assert select_priority(3, triggered_gate=True) == "Critical blocker"
    assert select_priority(3, cross_domain_blocker=True) == "High-priority foundation"
