from __future__ import annotations

import errno
import hashlib
import json
from pathlib import Path

import pytest

from assessment.domain.errors import (
    CompatibilityError,
    ConcurrentWriteError,
    EngagementExistsError,
    InvalidPathError,
)
from assessment.storage.local import LocalEngagementStore, fsync_directory
from assessment.storage.local import _open_absolute_directory as real_open_absolute_directory
from assessment.storage.local import _open_child_directory as real_open_child_directory
from assessment.storage.local import atomic_write_at as real_atomic_write_at
from assessment.storage.local import promote_directory_no_replace as real_promote
from assessment.storage.migrations import migrate_prototype_fixture

ROOT = Path(__file__).resolve().parents[3]


def engagement_document(engagement_id: str = "engagement-001") -> dict[str, object]:
    return {
        "schema_version": "1.0.0",
        "engagement_id": engagement_id,
        "framework_version": "1.0.0",
        "catalog_version": "1.0.0",
        "demo_content_version": "1.0.0",
        "assessment_profile_id": "quick-v1",
        "gate_bundle_version": 1,
    }


def test_local_store_uses_relative_posix_keys_canonical_json_and_checksums(
    tmp_path: Path,
) -> None:
    store = LocalEngagementStore(tmp_path / "engagements")
    store.create(engagement_document())
    store.write_document(
        "engagement-001",
        "assessment/quick.json",
        {"schema_version": "1.0.0", "z": 1, "a": "é"},
    )
    raw = (tmp_path / "engagements/engagement-001/assessment/quick.json").read_bytes()
    assert raw == b'{\n  "a": "\xc3\xa9",\n  "schema_version": "1.0.0",\n  "z": 1\n}\n'
    snapshot = store.snapshot("engagement-001")
    assert snapshot["assessment/quick.json"] == hashlib.sha256(raw).hexdigest()
    assert store.list_engagements() == ["engagement-001"]

    for unsafe in ("../outside.json", "/tmp/outside.json", r"C:\outside.json", "a\\b.json"):
        with pytest.raises(InvalidPathError):
            store.write_document("engagement-001", unsafe, {})


def test_atomic_replace_failure_preserves_previous_valid_document(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    store = LocalEngagementStore(tmp_path / "engagements")
    store.create(engagement_document())
    store.write_document("engagement-001", "assessment/quick.json", {"value": "before"})
    target = tmp_path / "engagements/engagement-001/assessment/quick.json"
    before = target.read_bytes()

    def fail_replace(*args: object, **kwargs: object) -> None:
        raise OSError("simulated interrupted replace")

    monkeypatch.setattr("assessment.storage.local.os.rename", fail_replace)
    with pytest.raises(OSError, match="interrupted"):
        store.write_document("engagement-001", "assessment/quick.json", {"value": "after"})
    assert target.read_bytes() == before
    assert not list(target.parent.glob(".*.tmp-*"))


def test_lock_refuses_competing_writer_and_recovery_removes_stale_temps(
    tmp_path: Path,
) -> None:
    store = LocalEngagementStore(tmp_path / "engagements")
    store.create(engagement_document())
    engagement_root = tmp_path / "engagements/engagement-001"
    stale = engagement_root / "assessment/.quick.json.tmp-stale"
    stale.parent.mkdir(parents=True, exist_ok=True)
    stale.write_text("partial", encoding="utf-8")

    with store.lock("engagement-001"):
        with pytest.raises(ConcurrentWriteError):
            with store.lock("engagement-001"):
                pass
    store.recover("engagement-001")
    assert not stale.exists()


def test_parent_directory_fsync_is_used_or_reports_platform_non_support(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    assert fsync_directory(tmp_path) is True

    def unsupported(descriptor: int) -> None:
        raise OSError(errno.EINVAL, "directory fsync unsupported")

    monkeypatch.setattr("assessment.storage.local.os.fsync", unsupported)
    assert fsync_directory(tmp_path) is False


def test_store_rejects_planted_parent_and_lock_symlinks_without_external_write(
    tmp_path: Path,
) -> None:
    store = LocalEngagementStore(tmp_path / "engagements")
    store.create(engagement_document())
    engagement_root = tmp_path / "engagements/engagement-001"
    outside = tmp_path / "outside"
    outside.mkdir()
    (engagement_root / "assessment").symlink_to(outside, target_is_directory=True)
    with pytest.raises(InvalidPathError):
        store.write_document("engagement-001", "assessment/quick.json", {"unsafe": True})
    assert not (outside / "quick.json").exists()

    (engagement_root / "assessment").unlink()
    (engagement_root / ".engagement.lock").unlink()
    lock_target = outside / "lock-target"
    lock_target.write_text("preserve", encoding="utf-8")
    (engagement_root / ".engagement.lock").symlink_to(lock_target)
    with pytest.raises(InvalidPathError):
        store.write_document("engagement-001", "assessment/quick.json", {"unsafe": True})
    assert lock_target.read_text(encoding="utf-8") == "preserve"


def test_store_descriptor_binding_blocks_parent_swap_race(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    store = LocalEngagementStore(tmp_path / "engagements")
    store.create(engagement_document())
    engagement_root = tmp_path / "engagements/engagement-001"
    outside = tmp_path / "outside"
    outside.mkdir()
    swapped = False

    def swap_parent_then_write(root_descriptor: int, key: str, content: bytes) -> None:
        nonlocal swapped
        if key == "assessment/quick.json" and not swapped:
            swapped = True
            (engagement_root / "assessment").symlink_to(
                outside,
                target_is_directory=True,
            )
        real_atomic_write_at(root_descriptor, key, content)

    monkeypatch.setattr(
        "assessment.storage.local.atomic_write_at",
        swap_parent_then_write,
    )
    with pytest.raises(InvalidPathError):
        store.write_document("engagement-001", "assessment/quick.json", {"unsafe": True})
    assert not (outside / "quick.json").exists()


def test_store_root_binding_rejects_intermediate_ancestor_symlink_swap(
    tmp_path: Path,
) -> None:
    trusted = tmp_path / "trusted"
    store = LocalEngagementStore(trusted / "store")
    held = tmp_path / "trusted-held"
    trusted.rename(held)
    external = tmp_path / "external"
    (external / "store").mkdir(parents=True)
    trusted.symlink_to(external, target_is_directory=True)

    with pytest.raises(InvalidPathError):
        store.create(engagement_document())
    assert not (external / "store/engagement-001").exists()


def test_create_crash_before_promotion_leaves_no_visible_engagement(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    store = LocalEngagementStore(tmp_path / "engagements")

    def fail_checksums(root_descriptor: int, key: str, content: bytes) -> None:
        if key == "metadata/checksums.json":
            raise OSError("simulated create crash")
        real_atomic_write_at(root_descriptor, key, content)

    monkeypatch.setattr("assessment.storage.local.atomic_write_at", fail_checksums)
    with pytest.raises(OSError, match="create crash"):
        store.create(engagement_document())
    assert not (tmp_path / "engagements/engagement-001").exists()
    assert not list((tmp_path / "engagements").glob(".engagement-001.create-*"))


def test_create_failure_cleanup_cannot_delete_through_swapped_root_ancestor(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    trusted = tmp_path / "trusted"
    store = LocalEngagementStore(trusted / "store")
    held = tmp_path / "trusted-held"
    external = tmp_path / "external"
    external_store = external / "store"
    marker: Path | None = None

    def swap_root_then_fail(root_descriptor: int, key: str, content: bytes) -> None:
        nonlocal marker
        if key == "metadata/checksums.json":
            trusted.rename(held)
            external_store.mkdir(parents=True)
            stage_name = next((held / "store").glob(".engagement-001.create-*")).name
            external_stage = external_store / stage_name
            external_stage.mkdir()
            marker = external_stage / "marker"
            marker.write_text("preserve", encoding="utf-8")
            trusted.symlink_to(external, target_is_directory=True)
            raise OSError("simulated create crash after ancestor swap")
        real_atomic_write_at(root_descriptor, key, content)

    monkeypatch.setattr("assessment.storage.local.atomic_write_at", swap_root_then_fail)
    with pytest.raises(OSError, match="ancestor swap"):
        store.create(engagement_document())
    assert marker is not None
    assert marker.read_text(encoding="utf-8") == "preserve"
    assert not list((held / "store").glob(".engagement-001.create-*"))


def test_recovery_descriptor_binding_preserves_external_temporary_file(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    store = LocalEngagementStore(tmp_path / "engagements")
    store.create(engagement_document())
    engagement_root = tmp_path / "engagements/engagement-001"
    nested = engagement_root / "nested"
    nested.mkdir()
    (nested / ".internal.tmp-stale").write_text("internal", encoding="utf-8")
    outside = tmp_path / "outside"
    outside.mkdir()
    external = outside / ".external.tmp-stale"
    external.write_text("preserve", encoding="utf-8")
    held = engagement_root / "nested-held"
    swapped = False

    def swap_before_open(parent_descriptor: int, name: str, *, create: bool) -> int:
        nonlocal swapped
        if name == "nested" and not swapped:
            swapped = True
            nested.rename(held)
            nested.symlink_to(outside, target_is_directory=True)
        return real_open_child_directory(parent_descriptor, name, create=create)

    monkeypatch.setattr(
        "assessment.storage.local._open_child_directory",
        swap_before_open,
    )
    with pytest.raises(InvalidPathError):
        store.recover("engagement-001")
    assert external.read_text(encoding="utf-8") == "preserve"


def test_no_replace_promotion_rejects_intermediate_ancestor_swap(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    trusted = tmp_path / "trusted"
    source_parent = trusted / "source-parent"
    source_parent.mkdir(parents=True)
    source = source_parent / "payload"
    source.mkdir()
    external = tmp_path / "external"
    external.mkdir()
    held = tmp_path / "trusted-held"
    calls = 0

    def swap_ancestor_before_second_open(path: Path) -> int:
        nonlocal calls
        calls += 1
        if calls == 2:
            trusted.rename(held)
            trusted.symlink_to(external, target_is_directory=True)
        return real_open_absolute_directory(path)

    monkeypatch.setattr(
        "assessment.storage.local._open_absolute_directory",
        swap_ancestor_before_second_open,
    )
    with pytest.raises(InvalidPathError):
        real_promote(source, trusted / "destination")
    assert not (external / "destination").exists()


def test_migration_is_pure_idempotent_and_preserves_frozen_source(tmp_path: Path) -> None:
    source = (
        ROOT / "assessment/tests/fixtures/scenarios/0.1.0/startup-no-governance/architect-a.json"
    )
    source_before = source.read_bytes()
    destination = tmp_path / "migrated"
    receipt = migrate_prototype_fixture(source, destination)
    first_state = {
        path.relative_to(destination).as_posix(): path.read_bytes()
        for path in destination.rglob("*")
        if path.is_file()
    }
    second_receipt = migrate_prototype_fixture(source, destination)
    second_state = {
        path.relative_to(destination).as_posix(): path.read_bytes()
        for path in destination.rglob("*")
        if path.is_file()
    }
    assert source.read_bytes() == source_before
    assert receipt == second_receipt
    assert first_state == second_state
    assert receipt["source_version"] == "0.1.0-prototype"
    assert receipt["target_version"] == "1.0.0"
    assert json.loads((destination / "engagement.json").read_text())["schema_version"] == "1.0.0"


def test_migration_idempotence_rejects_corrupted_existing_target(tmp_path: Path) -> None:
    source = (
        ROOT / "assessment/tests/fixtures/scenarios/0.1.0/startup-no-governance/architect-a.json"
    )
    destination = tmp_path / "migrated"
    migrate_prototype_fixture(source, destination)
    (destination / "assessment/quick.json").write_text("{}\n", encoding="utf-8")

    with pytest.raises(EngagementExistsError, match="differs"):
        migrate_prototype_fixture(source, destination)
    assert (destination / "assessment/quick.json").read_bytes() == b"{}\n"


def test_migration_idempotence_rejects_root_symlink_and_unexpected_directory(
    tmp_path: Path,
) -> None:
    source = (
        ROOT / "assessment/tests/fixtures/scenarios/0.1.0/startup-no-governance/architect-a.json"
    )
    real_destination = tmp_path / "real/migrated"
    real_destination.parent.mkdir()
    migrate_prototype_fixture(source, real_destination)

    linked_destination = tmp_path / "linked/migrated"
    linked_destination.parent.mkdir()
    linked_destination.symlink_to(real_destination, target_is_directory=True)
    with pytest.raises(EngagementExistsError):
        migrate_prototype_fixture(source, linked_destination)

    (real_destination / "unexpected-empty").mkdir()
    with pytest.raises(EngagementExistsError, match="state differs"):
        migrate_prototype_fixture(source, real_destination)


def test_migration_promotion_preserves_concurrent_destination(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    source = (
        ROOT / "assessment/tests/fixtures/scenarios/0.1.0/startup-no-governance/architect-a.json"
    )
    destination = tmp_path / "migrated"

    def collide_then_promote(staged: Path, target: Path) -> None:
        target.mkdir()
        (target / "marker").write_text("preserve", encoding="utf-8")
        real_promote(staged, target)

    monkeypatch.setattr(
        "assessment.storage.migrations.promote_directory_no_replace",
        collide_then_promote,
    )
    with pytest.raises(EngagementExistsError, match="appeared"):
        migrate_prototype_fixture(source, destination)
    assert (destination / "marker").read_text(encoding="utf-8") == "preserve"


def test_unknown_newer_migration_fails_before_destination_mutation(tmp_path: Path) -> None:
    source = tmp_path / "newer.json"
    source.write_text('{"schema_version":"2.0.0"}\n', encoding="utf-8")
    destination = tmp_path / "destination"
    with pytest.raises(CompatibilityError):
        migrate_prototype_fixture(source, destination)
    assert not destination.exists()


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("organization_name", "<script>unsafe</script>"),
        ("duration_minutes", 61),
        ("evidence_statuses", ["Unknown"] * 30),
        (
            "diagnostic_facts",
            {
                "privacy_control_level": "not-an-integer",
                "ownership_control_level": 1,
                "critical_lineage": False,
                "reproducible_versioned": False,
            },
        ),
    ],
)
def test_invalid_known_old_source_fails_before_destination_mutation(
    tmp_path: Path, field: str, value: object
) -> None:
    source_fixture = (
        ROOT / "assessment/tests/fixtures/scenarios/0.1.0/startup-no-governance/architect-a.json"
    )
    document = json.loads(source_fixture.read_text(encoding="utf-8"))
    document[field] = value
    source = tmp_path / "invalid.json"
    source.write_text(json.dumps(document), encoding="utf-8")
    destination = tmp_path / "destination"
    with pytest.raises(CompatibilityError):
        migrate_prototype_fixture(source, destination)
    assert not destination.exists()
