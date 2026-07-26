from __future__ import annotations

from assessment.domain.deep_dives import (
    DEEP_DIVE_ORDER,
    load_deep_dive_registry,
)


def test_initial_deep_dives_have_exact_counts_complete_anchors_and_guidance() -> None:
    registry = load_deep_dive_registry()
    assert tuple(item.id for item in registry.deep_dives) == DEEP_DIVE_ORDER
    assert {item.id: len(item.questions) for item in registry.deep_dives} == {
        "data-quality": 20,
        "governance-metadata-lineage": 24,
        "security-privacy-policy": 20,
    }
    assert sum(len(item.questions) for item in registry.deep_dives) == 64

    for deep_dive in registry.deep_dives:
        assert 30 <= deep_dive.duration_minutes <= 180
        assert deep_dive.capability_ids
        assert deep_dive.linked_recommendation_ids
        for question in deep_dive.questions:
            assert set(question.anchors) == {"0", "1", "2", "3", "4"}
            assert all(len(anchor) >= 12 for anchor in question.anchors.values())
            assert question.evidence_guidance
            assert question.linked_recommendation_ids
            assert question.duration_minutes >= 2
            assert question.confidence_semantics == (
                "Use the existing evidence status independently from the maturity rating."
            )


def test_deep_dive_ids_and_question_ids_are_globally_unique_and_ordered() -> None:
    registry = load_deep_dive_registry()
    question_ids = [
        question.id
        for deep_dive in registry.deep_dives
        for question in deep_dive.questions
    ]
    assert len(question_ids) == len(set(question_ids)) == 64
    assert question_ids == sorted(question_ids)
