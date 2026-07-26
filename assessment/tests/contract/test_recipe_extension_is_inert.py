from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

from assessment.content.recipes import load_recipe_extension
from assessment.reporting.generator import generate_report
from assessment.storage.migrations import _prototype_to_v1
from prototype import run as prototype

ROOT = Path(__file__).resolve().parents[3]
FIXTURE = (
    ROOT
    / "assessment"
    / "tests"
    / "fixtures"
    / "recipes"
    / "manufacturing-maintenance-0.1.0"
)


def _tree_hash(paths: list[Path]) -> str:
    digest = hashlib.sha256()
    for path in sorted(paths):
        digest.update(path.relative_to(ROOT).as_posix().encode())
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def _scenario_report_hashes() -> dict[str, str]:
    framework = prototype.load_framework()
    hashes: dict[str, str] = {}
    for scenario_id, scenario in sorted(prototype.load_scenarios(framework).items()):
        documents = _prototype_to_v1(scenario["architect-a"], scenario_id)
        report = generate_report(
            documents["engagement.json"],
            documents["assessment/quick.json"],
        )
        hashes[scenario_id] = hashlib.sha256(report.json_bytes).hexdigest()
    return hashes


def test_manufacturing_recipe_loads_only_through_public_additive_extension() -> None:
    recipe = load_recipe_extension(FIXTURE)
    assert recipe.manifest.recipe_id == "manufacturing-maintenance-0.1.0"
    assert recipe.manifest.title.startswith("INERT NON-PRODUCTION")
    assert recipe.demo.status == "absent"
    assert recipe.demo.non_scoring is True
    assert recipe.production_supported is False
    assert recipe.pipeline_routes == ()


def test_recipe_add_remove_has_zero_engine_schema_scenario_and_report_delta(
    tmp_path: Path,
) -> None:
    engine_paths = list((ROOT / "assessment/src/assessment/engine").glob("*.py"))
    schema_paths = list((ROOT / "assessment/contracts").glob("*.schema.json"))
    engine_before = _tree_hash(engine_paths)
    schemas_before = _tree_hash(schema_paths)
    reports_before = _scenario_report_hashes()

    added_fixture = tmp_path / FIXTURE.name
    shutil.copytree(FIXTURE, added_fixture)
    loaded = load_recipe_extension(added_fixture)
    assert len(loaded.questions) > 0
    shutil.rmtree(added_fixture)
    assert not added_fixture.exists()

    assert _tree_hash(engine_paths) == engine_before
    assert _tree_hash(schema_paths) == schemas_before
    reports_after = _scenario_report_hashes()
    assert reports_after == reports_before
    proof = json.loads((FIXTURE / "inertness-proof.json").read_text())
    report_set_hash = hashlib.sha256(
        json.dumps(reports_before, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    assert proof["engine_tree_sha256"] == engine_before
    assert proof["core_schema_tree_sha256"] == schemas_before
    assert proof["scenario_report_sha256"] == reports_before
    assert proof["report_set_sha256"] == report_set_hash
    assert proof["engine_hash_unchanged"] is True
    assert proof["core_schema_hash_unchanged"] is True
    assert proof["scenario_hashes_unchanged"] is True
    assert proof["report_hashes_unchanged"] is True
