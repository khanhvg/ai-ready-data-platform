from __future__ import annotations

import copy
from pathlib import Path

import pytest

from assessment.catalog.loader import load_catalog, load_demo_catalog
from assessment.catalog.mapping import (
    CRITICAL_FINDING_FAMILIES,
    MappingResolver,
    load_mapping_registry,
)
from assessment.domain.errors import ContentValidationError
from assessment.frameworks import load_framework

ROOT = Path(__file__).resolve().parents[3]


def test_every_critical_finding_family_has_one_complete_deterministic_chain() -> None:
    framework = load_framework("1.0.0")
    catalog = load_catalog("1.0.0")
    demo = load_demo_catalog("1.0.0")
    resolver = MappingResolver(framework, catalog, demo, load_mapping_registry())

    first = resolver.resolve_all()
    second = resolver.resolve_all()

    assert first == second
    assert tuple(chain.finding_id for chain in first) == CRITICAL_FINDING_FAMILIES
    assert len(first) == len(CRITICAL_FINDING_FAMILIES) == 8
    for chain in first:
        assert chain.gap.text and chain.gap.provenance.kind == "generated-assessment-fact"
        assert chain.impact.text and chain.impact.provenance.kind == "catalog-reference"
        assert (
            chain.priority.label
            and chain.priority.provenance.kind == "generated-assessment-fact"
        )
        assert (
            chain.recommendation.id
            and chain.recommendation.provenance.kind == "catalog-reference"
        )
        assert chain.architecture.id and chain.architecture.provenance.kind == "catalog-reference"
        assert chain.technology_options
        assert all(
            option.id
            and option.alternatives
            and option.vendor_neutral
            and option.provenance.reference.startswith(
                "technology-profile:deferred-alternatives:"
            )
            for option in chain.technology_options
        )
        assert chain.profile_options
        assert all(
            option.content_only and not option.executable
            for option in chain.profile_options
        )
        assert chain.action.owner_role and chain.action.horizon and chain.action.success_measure
        assert chain.action.provenance.kind == "catalog-reference"
        if chain.demo is not None:
            assert chain.demo.non_scoring is True
            assert chain.demo.provenance.kind == "demo-illustration"


def test_mapping_resolver_is_read_only_and_demo_leaf_never_changes_assessment_edges() -> None:
    framework = load_framework("1.0.0")
    catalog = load_catalog("1.0.0")
    demo = load_demo_catalog("1.0.0")
    before_framework = copy.deepcopy(framework)
    before_catalog = copy.deepcopy(catalog)
    before_demo = copy.deepcopy(demo)
    baseline = MappingResolver(
        framework, catalog, demo, load_mapping_registry()
    ).resolve_all()

    mutated_demo = demo.model_copy(
        update={"non_scoring_disclaimer": "Different inert presentation text."}
    )
    changed = MappingResolver(
        framework, catalog, mutated_demo, load_mapping_registry()
    ).resolve_all()

    assert framework == before_framework
    assert catalog == before_catalog
    assert demo == before_demo
    assert [
        chain.model_dump(mode="json", exclude={"demo"}) for chain in baseline
    ] == [chain.model_dump(mode="json", exclude={"demo"}) for chain in changed]


def test_mapping_registry_rejects_unresolved_or_cyclic_graphs() -> None:
    registry = load_mapping_registry()
    unresolved = registry.model_copy(deep=True)
    unresolved.chains[0].architecture_id = "ARCH-DOES-NOT-EXIST"
    with pytest.raises(ContentValidationError, match="architecture"):
        MappingResolver(
            load_framework("1.0.0"),
            load_catalog("1.0.0"),
            load_demo_catalog("1.0.0"),
            unresolved,
        )

    unresolved_option = registry.model_copy(deep=True)
    unresolved_option.chains[0].technology_option_ids[0] = "does-not-exist"
    with pytest.raises(ContentValidationError, match="technology"):
        MappingResolver(
            load_framework("1.0.0"),
            load_catalog("1.0.0"),
            load_demo_catalog("1.0.0"),
            unresolved_option,
        )

    cyclic = registry.model_copy(deep=True)
    cyclic.chains[0].edges.append(
        cyclic.chains[0].edges[0].model_copy(
            update={"source": "action", "target": "gap"}
        )
    )
    with pytest.raises(ContentValidationError, match="edge|cycle"):
        MappingResolver(
            load_framework("1.0.0"),
            load_catalog("1.0.0"),
            load_demo_catalog("1.0.0"),
            cyclic,
        )


def test_demo_leaves_report_present_absent_and_corrupt_without_scoring(
    tmp_path: Path,
) -> None:
    framework = load_framework("1.0.0")
    catalog = load_catalog("1.0.0")
    absent = MappingResolver(
        framework,
        catalog,
        load_demo_catalog("1.0.0"),
        load_mapping_registry(),
    ).resolve_all()
    assert {chain.demo.status for chain in absent if chain.demo} == {"unavailable"}
    present = MappingResolver(
        framework,
        catalog,
        load_demo_catalog("1.0.0", repository_root=ROOT),
        load_mapping_registry(),
    ).resolve_all()
    assert {chain.demo.status for chain in present if chain.demo} <= {
        "available",
        "mixed",
    }
    assert all(chain.demo is None or chain.demo.non_scoring for chain in present)

    corrupt = tmp_path / "demo/manifests/stages"
    corrupt.mkdir(parents=True)
    (corrupt / "ingestion.yaml").write_text(
        "schema_version: 1.0.0\nstage_id: wrong\n", encoding="utf-8"
    )
    with pytest.raises(ContentValidationError, match="corrupt stage manifest"):
        load_demo_catalog("1.0.0", repository_root=tmp_path)
