from __future__ import annotations

import hashlib
import json
import os
import stat
import zipfile
from collections.abc import Callable
from io import BytesIO
from pathlib import Path

import pytest
from PIL import Image, PngImagePlugin

from assessment.domain.deep_dives import (
    ConflictChoice,
    DeepDiveAnswer,
    DeepDiveService,
    PromotionRequest,
)
from assessment.domain.errors import ArchiveValidationError, CompatibilityError
from assessment.storage.archive import export_engagement, import_engagement
from assessment.storage.local import LocalEngagementStore
from assessment.storage.local import promote_directory_no_replace as real_promote
from assessment.storage.migrations import _prototype_to_v1
from assessment.web.config import WebConfig
from assessment.web.dependencies import WebServices
from prototype import run as prototype


def engagement_document() -> dict[str, object]:
    return {
        "schema_version": "1.0.0",
        "engagement_id": "portable-001",
        "framework_version": "1.0.0",
        "catalog_version": "1.0.0",
        "demo_content_version": "1.0.0",
        "assessment_profile_id": "quick-v1",
        "gate_bundle_version": 1,
    }


def create_engagement(root: Path) -> Path:
    store = LocalEngagementStore(root)
    path = store.create(engagement_document())
    store.write_document(
        "portable-001",
        "assessment/quick.json",
        {
            "schema_version": "1.0.0",
            "engagement_id": "portable-001",
            "framework_version": "1.0.0",
            "answers": [],
            "diagnostic_facts": {},
        },
    )
    store.add_evidence("portable-001", "evidence/files/notes.txt", b"Sanitized local evidence.\r\n")
    return path


def create_promoted_phase7_engagement(tmp_path: Path) -> Path:
    engagement_root = tmp_path / "phase7-engagements"
    runtime_root = tmp_path / "phase7-runtime"
    engagement_root.mkdir()
    runtime_root.mkdir()
    services = WebServices(
        WebConfig(
            engagement_root=engagement_root,
            runtime_root=runtime_root,
            repository_root=Path(__file__).resolve().parents[3],
            host="127.0.0.1",
            port=8765,
        ),
        store=LocalEngagementStore(engagement_root),
    )
    services.create_engagement("phase7-portable")
    framework = prototype.load_framework()
    fixture = prototype.load_scenarios(framework)["startup-no-governance"][
        "architect-a"
    ]
    quick = _prototype_to_v1(fixture, "phase7-portable")["assessment/quick.json"]
    services.store.write_document(
        "phase7-portable", "assessment/quick.json", quick
    )
    deep_dives = DeepDiveService(services.store, services.framework)
    definition = deep_dives.registry.by_id("data-quality")
    advisory = deep_dives.save_advisory(
        "phase7-portable",
        deep_dive_id=definition.id,
        answers=[
            DeepDiveAnswer(
                question_id=question.id,
                rating=4,
                evidence_status="Evidenced",
                note="Synthetic portable evidence.",
                evidence_refs=[],
            )
            for question in definition.questions
        ],
    )
    deep_dives.promote(
        "phase7-portable",
        PromotionRequest(
            source_digest=advisory.document_digest,
            target_digest=deep_dives.promotion_target_digest("phase7-portable"),
            capability_ids=["QUA"],
            rationale="Architect reviewed portable synthetic evidence.",
            reviewed_by="solution-architect",
            review_timestamp=deep_dives.engagement_timestamp("phase7-portable"),
            conflict_choices=[
                ConflictChoice(
                    capability_id="QUA",
                    choice="use-deep-dive",
                    rationale="Use the reviewed deep-dive evidence.",
                )
            ],
        ),
    )
    return services.store.open("phase7-portable")


def rewrite_archive(
    source: Path,
    destination: Path,
    mutate: Callable[[zipfile.ZipInfo, bytes], tuple[zipfile.ZipInfo, bytes] | None],
) -> None:
    with (
        zipfile.ZipFile(source) as original,
        zipfile.ZipFile(destination, "w", compression=zipfile.ZIP_STORED) as changed,
    ):
        for info in original.infolist():
            data = original.read(info)
            result = mutate(info, data)
            if result is None:
                continue
            new_info, new_data = result
            changed.writestr(new_info, new_data)


def rewrite_with_consistent_manifest(
    source: Path,
    destination: Path,
    mutate_entries: Callable[[dict[str, bytes]], None],
) -> None:
    with zipfile.ZipFile(source) as handle:
        entries = {info.filename: handle.read(info) for info in handle.infolist()}
    manifest = json.loads(entries.pop("manifest.json"))
    mutate_entries(entries)
    checksums = {
        "schema_version": "1.0.0",
        "algorithm": "sha256",
        "files": {
            key: hashlib.sha256(content).hexdigest()
            for key, content in sorted(entries.items())
            if key != "metadata/checksums.json"
        },
    }
    entries["metadata/checksums.json"] = (
        json.dumps(checksums, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    ).encode()
    records = [
        {
            "path": key,
            "size": len(content),
            "sha256": hashlib.sha256(content).hexdigest(),
            "mode": "0644",
        }
        for key, content in sorted(entries.items())
    ]
    manifest["entries"] = records
    manifest["digest"] = hashlib.sha256(
        (json.dumps(records, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode()
    ).hexdigest()
    entries["manifest.json"] = (
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    ).encode()
    with zipfile.ZipFile(destination, "w", compression=zipfile.ZIP_STORED) as handle:
        for key, content in sorted(entries.items()):
            handle.writestr(key, content)


def test_export_is_byte_stable_and_distinct_path_roundtrip_preserves_digest(
    tmp_path: Path,
) -> None:
    source = create_engagement(tmp_path / "source-root")
    first = tmp_path / "first.zip"
    second = tmp_path / "second.zip"
    first_manifest = export_engagement(source, first)
    second_manifest = export_engagement(source, second)
    assert first.read_bytes() == second.read_bytes()
    assert first_manifest["digest"] == second_manifest["digest"]

    destination = tmp_path / "different/absolute/location/portable-001"
    imported_manifest = import_engagement(first, destination)
    third = tmp_path / "third.zip"
    third_manifest = export_engagement(destination, third)
    assert imported_manifest["digest"] == first_manifest["digest"]
    assert third_manifest["digest"] == first_manifest["digest"]
    assert third.read_bytes() == first.read_bytes()


def test_import_rejects_consistently_rehashed_broken_phase7_revision_graph(
    tmp_path: Path,
) -> None:
    source = create_promoted_phase7_engagement(tmp_path)
    valid = tmp_path / "phase7-valid.zip"
    corrupt = tmp_path / "phase7-corrupt.zip"
    export_engagement(source, valid)

    def break_active_pointer(entries: dict[str, bytes]) -> None:
        entries["results/active.json"] = (
            json.dumps(
                {"active_revision": 999, "schema_version": "1.0.0"},
                ensure_ascii=False,
                indent=2,
                sort_keys=True,
            )
            + "\n"
        ).encode()

    rewrite_with_consistent_manifest(valid, corrupt, break_active_pointer)
    destination = tmp_path / "phase7-imported"
    with pytest.raises(ArchiveValidationError, match="revision graph"):
        import_engagement(corrupt, destination)
    assert not destination.exists()


def test_export_rejects_content_that_exceeds_limit_after_canonicalization(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    source = create_engagement(tmp_path / "source")
    evidence = source / "evidence/files/canonical-expansion.json"
    document = {f"k{index:03d}": "v" for index in range(70)}
    compact = json.dumps(document, separators=(",", ":"), sort_keys=True).encode()
    canonical = (json.dumps(document, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode()
    assert len(compact) < 1_024 < len(canonical)
    evidence.write_bytes(compact)
    monkeypatch.setattr("assessment.storage.archive.MAX_FILE_BYTES", 1_024)

    archive = tmp_path / "canonical-expansion.zip"
    with pytest.raises(ArchiveValidationError, match="canonical file exceeds"):
        export_engagement(source, archive)
    assert not archive.exists()

    evidence.unlink()
    manifest = export_engagement(source, archive)
    destination = tmp_path / "roundtrip-destination"
    imported = import_engagement(archive, destination)
    assert imported["digest"] == manifest["digest"]
    with zipfile.ZipFile(archive) as handle:
        sizes = {info.filename: info.file_size for info in handle.infolist()}
    assert max(sizes.values()) <= 1_024

    archive.unlink()
    without_manifest = sum(
        size for filename, size in sizes.items() if filename != "manifest.json"
    )
    monkeypatch.setattr("assessment.storage.archive.MAX_TOTAL_BYTES", without_manifest)
    with pytest.raises(ArchiveValidationError, match="expanded-size limit"):
        export_engagement(source, archive)
    assert not archive.exists()

    monkeypatch.setattr("assessment.storage.archive.MAX_TOTAL_BYTES", 128 * 1_024 * 1_024)
    monkeypatch.setattr("assessment.storage.archive.MAX_FILE_BYTES", 500)
    with pytest.raises(ArchiveValidationError, match="manifest.json: canonical file exceeds"):
        export_engagement(source, archive)
    assert not archive.exists()


@pytest.mark.parametrize(
    ("target_key", "restore_after_legacy_read", "replacement_kind"),
    (
        ("engagement.json", True, "regular"),
        ("engagement.json", True, "symlink"),
        ("evidence/files/proof.txt", False, "regular"),
        ("evidence/files/proof.txt", False, "symlink"),
    ),
)
def test_export_rejects_path_replacement_between_scan_and_descriptor_open(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    target_key: str,
    restore_after_legacy_read: bool,
    replacement_kind: str,
) -> None:
    source = create_engagement(tmp_path / "source")
    target = source.joinpath(*target_key.split("/"))
    if target_key.startswith("evidence/"):
        target.write_bytes(b"Original proof.\n")
        external_content = b"Sanitized external proof.\n"
    else:
        external_content = target.read_bytes()
    external = tmp_path / "external.txt"
    external.write_bytes(external_content)
    held = target.with_name(f"{target.name}.held")
    original_read_bytes = Path.read_bytes
    original_os_open = os.open
    state = {"swapped": False}

    def swap_to_symlink() -> bool:
        if state["swapped"]:
            return False
        state["swapped"] = True
        target.rename(held)
        if replacement_kind == "symlink":
            target.symlink_to(external)
        else:
            target.write_bytes(external_content)
        return True

    def swap_then_legacy_read(path: Path) -> bytes:
        if path != target:
            return original_read_bytes(path)
        swapped = swap_to_symlink()
        content = original_read_bytes(path)
        if swapped and restore_after_legacy_read:
            target.unlink()
            held.rename(target)
        return content

    def swap_then_descriptor_open(
        path: str | bytes | os.PathLike[str] | os.PathLike[bytes],
        flags: int,
        mode: int = 0o777,
        *,
        dir_fd: int | None = None,
    ) -> int:
        if dir_fd is not None and os.fsdecode(path) == target.name:
            swap_to_symlink()
        return original_os_open(path, flags, mode, dir_fd=dir_fd)

    monkeypatch.setattr(Path, "read_bytes", swap_then_legacy_read)
    monkeypatch.setattr(os, "open", swap_then_descriptor_open)
    archive = tmp_path / "replacement.zip"
    with pytest.raises(ArchiveValidationError, match="changed|symlink"):
        export_engagement(source, archive)
    assert state["swapped"]
    assert not archive.exists()


@pytest.mark.parametrize(
    ("entry_name", "content"),
    [
        ("../escape.txt", b"safe"),
        ("/Users/person/private.txt", b"safe"),
        ("/home/person/private.txt", b"safe"),
        (r"C:\Users\person\private.txt", b"safe"),
        (r"\\server\share\private.txt", b"safe"),
        ("file.txt", b"password=very-secret-password"),
        ("file.txt", b"https://person:secret@example.invalid/data"),
        ("file.txt", b"/Users/person/private/source.csv"),
    ],
)
def test_hostile_names_and_content_are_rejected_without_destination_mutation(
    tmp_path: Path, entry_name: str, content: bytes
) -> None:
    archive = tmp_path / "hostile.zip"
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_STORED) as handle:
        handle.writestr(entry_name, content)
    destination = tmp_path / "destination"
    with pytest.raises(ArchiveValidationError):
        import_engagement(archive, destination)
    assert not destination.exists()


def test_duplicates_unicode_casefold_symlink_and_unsupported_features_are_rejected(
    tmp_path: Path,
) -> None:
    cases: list[Path] = []
    duplicate = tmp_path / "duplicate.zip"
    with pytest.warns(UserWarning, match="Duplicate name"):
        with zipfile.ZipFile(duplicate, "w") as handle:
            handle.writestr("same.txt", "one")
            handle.writestr("same.txt", "two")
    cases.append(duplicate)

    unicode_collision = tmp_path / "unicode.zip"
    with zipfile.ZipFile(unicode_collision, "w") as handle:
        handle.writestr("caf\u00e9.txt", "one")
        handle.writestr("cafe\u0301.txt", "two")
    cases.append(unicode_collision)

    case_collision = tmp_path / "case.zip"
    with zipfile.ZipFile(case_collision, "w") as handle:
        handle.writestr("FILE.txt", "one")
        handle.writestr("file.txt", "two")
    cases.append(case_collision)

    symlink = tmp_path / "symlink.zip"
    with zipfile.ZipFile(symlink, "w") as handle:
        info = zipfile.ZipInfo("link")
        info.create_system = 3
        info.external_attr = (stat.S_IFLNK | 0o777) << 16
        handle.writestr(info, "target")
    cases.append(symlink)

    unsupported = tmp_path / "unsupported.zip"
    with zipfile.ZipFile(unsupported, "w", compression=zipfile.ZIP_BZIP2) as handle:
        handle.writestr("file.txt", "safe")
    cases.append(unsupported)

    for index, archive in enumerate(cases):
        destination = tmp_path / f"destination-{index}"
        with pytest.raises(ArchiveValidationError):
            import_engagement(archive, destination)
        assert not destination.exists()


def test_destination_collisions_and_symlinks_are_non_mutating(tmp_path: Path) -> None:
    source = create_engagement(tmp_path / "source")
    archive = tmp_path / "export.zip"
    export_engagement(source, archive)

    existing = tmp_path / "existing"
    existing.mkdir()
    marker = existing / "marker"
    marker.write_text("preserve", encoding="utf-8")
    with pytest.raises(ArchiveValidationError):
        import_engagement(archive, existing)
    assert marker.read_text() == "preserve"

    real_parent = tmp_path / "real-parent"
    real_parent.mkdir()
    linked_parent = tmp_path / "linked-parent"
    linked_parent.symlink_to(real_parent, target_is_directory=True)
    with pytest.raises(ArchiveValidationError):
        import_engagement(archive, linked_parent / "destination")
    assert not (real_parent / "destination").exists()

    linked_archive = tmp_path / "linked.zip"
    linked_archive.symlink_to(archive)
    with pytest.raises(ArchiveValidationError):
        import_engagement(linked_archive, tmp_path / "archive-link-destination")
    assert not (tmp_path / "archive-link-destination").exists()


def test_corrupt_hash_unknown_newer_and_opaque_evidence_fail_closed(tmp_path: Path) -> None:
    source = create_engagement(tmp_path / "source")
    archive = tmp_path / "export.zip"
    export_engagement(source, archive)

    corrupt = tmp_path / "corrupt.zip"
    rewrite_archive(
        archive,
        corrupt,
        lambda info, data: (info, b"changed")
        if info.filename == "assessment/quick.json"
        else (info, data),
    )
    corrupt_destination = tmp_path / "corrupt-destination"
    with pytest.raises(ArchiveValidationError):
        import_engagement(corrupt, corrupt_destination)
    assert not corrupt_destination.exists()

    newer = tmp_path / "newer.zip"

    def make_newer(info: zipfile.ZipInfo, data: bytes) -> tuple[zipfile.ZipInfo, bytes]:
        if info.filename == "manifest.json":
            manifest = json.loads(data)
            manifest["format_version"] = "2.0.0"
            data = (json.dumps(manifest, indent=2, sort_keys=True) + "\n").encode()
        return info, data

    rewrite_archive(archive, newer, make_newer)
    with pytest.raises(CompatibilityError):
        import_engagement(newer, tmp_path / "newer-destination")
    assert not (tmp_path / "newer-destination").exists()

    nested_newer = tmp_path / "nested-newer.zip"

    def change_quick_version(entries: dict[str, bytes]) -> None:
        quick = json.loads(entries["assessment/quick.json"])
        quick["schema_version"] = "2.0.0"
        entries["assessment/quick.json"] = (
            json.dumps(quick, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
        ).encode()

    rewrite_with_consistent_manifest(archive, nested_newer, change_quick_version)
    with pytest.raises(CompatibilityError):
        import_engagement(nested_newer, tmp_path / "nested-newer-destination")
    assert not (tmp_path / "nested-newer-destination").exists()

    unknown_document_source = create_engagement(tmp_path / "unknown-document-source")
    LocalEngagementStore(tmp_path / "unknown-document-source").write_document(
        "portable-001",
        "assessment/quick.json",
        {
            "schema_version": "2.0.0",
            "engagement_id": "portable-001",
            "framework_version": "1.0.0",
            "answers": [],
            "diagnostic_facts": {},
        },
    )
    with pytest.raises(CompatibilityError):
        export_engagement(unknown_document_source, tmp_path / "unknown-document.zip")
    assert not (tmp_path / "unknown-document.zip").exists()

    (source / "evidence/files/document.pdf").write_bytes(b"%PDF-1.7 opaque")
    with pytest.raises(ArchiveValidationError, match="evidence"):
        export_engagement(source, tmp_path / "opaque.zip")


def test_manifest_secrets_and_unexpected_fields_fail_before_destination_mutation(
    tmp_path: Path,
) -> None:
    source = create_engagement(tmp_path / "source")
    archive = tmp_path / "export.zip"
    export_engagement(source, archive)
    hostile = tmp_path / "hostile-manifest.zip"

    def add_manifest_secret(info: zipfile.ZipInfo, data: bytes) -> tuple[zipfile.ZipInfo, bytes]:
        if info.filename == "manifest.json":
            manifest = json.loads(data)
            manifest["password"] = "very-secret-password"  # noqa: S105 -- hostile fixture
            data = (json.dumps(manifest, indent=2, sort_keys=True) + "\n").encode()
        return info, data

    rewrite_archive(archive, hostile, add_manifest_secret)
    destination = tmp_path / "hostile-manifest-destination"
    with pytest.raises(ArchiveValidationError):
        import_engagement(hostile, destination)
    assert not destination.exists()


def test_noncanonical_or_reordered_manifest_is_rejected_before_mutation(
    tmp_path: Path,
) -> None:
    source = create_engagement(tmp_path / "source")
    archive = tmp_path / "export.zip"
    export_engagement(source, archive)
    hostile = tmp_path / "reordered-manifest.zip"

    def reverse_manifest_records(
        info: zipfile.ZipInfo, data: bytes
    ) -> tuple[zipfile.ZipInfo, bytes]:
        if info.filename == "manifest.json":
            manifest = json.loads(data)
            manifest["entries"].reverse()
            manifest["digest"] = hashlib.sha256(
                (
                    json.dumps(
                        manifest["entries"],
                        ensure_ascii=False,
                        indent=2,
                        sort_keys=True,
                    )
                    + "\n"
                ).encode()
            ).hexdigest()
            data = (
                json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
            ).encode()
        return info, data

    rewrite_archive(archive, hostile, reverse_manifest_records)
    destination = tmp_path / "reordered-destination"
    with pytest.raises(ArchiveValidationError, match="canonical"):
        import_engagement(hostile, destination)
    assert not destination.exists()


def test_container_size_limit_precedes_archive_parsing(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    source = create_engagement(tmp_path / "source")
    archive = tmp_path / "export.zip"
    export_engagement(source, archive)
    monkeypatch.setattr("assessment.storage.archive.MAX_ARCHIVE_BYTES", 64)
    destination = tmp_path / "oversized-container-destination"
    with pytest.raises(ArchiveValidationError, match="container-size"):
        import_engagement(archive, destination)
    assert not destination.exists()


def test_import_promotion_preserves_concurrent_destination(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    source = create_engagement(tmp_path / "source")
    archive = tmp_path / "export.zip"
    export_engagement(source, archive)
    destination = tmp_path / "concurrent-destination"

    def collide_then_promote(staging: Path, target: Path) -> None:
        target.mkdir()
        (target / "marker").write_text("preserve", encoding="utf-8")
        real_promote(staging, target)

    monkeypatch.setattr(
        "assessment.storage.archive.promote_directory_no_replace",
        collide_then_promote,
    )
    with pytest.raises(ArchiveValidationError, match="appeared"):
        import_engagement(archive, destination)
    assert (destination / "marker").read_text(encoding="utf-8") == "preserve"


@pytest.mark.parametrize("suffix", (".md", ".yaml", ".yml", ".html", ".css"))
def test_non_v1_evidence_text_formats_are_rejected(tmp_path: Path, suffix: str) -> None:
    source = create_engagement(tmp_path / "source")
    (source / f"evidence/files/unsupported{suffix}").write_text(
        "Inspectable but outside the v1 evidence allowlist.\n",
        encoding="utf-8",
    )
    archive = tmp_path / "unsupported-evidence.zip"
    with pytest.raises(ArchiveValidationError, match="opaque evidence"):
        export_engagement(source, archive)
    assert not archive.exists()


def test_limits_and_ratio_bombs_fail_before_destination_mutation(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    oversized = tmp_path / "oversized.zip"
    with zipfile.ZipFile(oversized, "w", compression=zipfile.ZIP_STORED) as handle:
        handle.writestr("large.txt", b"a" * (32 * 1024 * 1024 + 1))
    with pytest.raises(ArchiveValidationError):
        import_engagement(oversized, tmp_path / "oversized-destination")
    assert not (tmp_path / "oversized-destination").exists()

    ratio = tmp_path / "ratio.zip"
    with zipfile.ZipFile(ratio, "w", compression=zipfile.ZIP_DEFLATED) as handle:
        handle.writestr("bomb.txt", b"a" * (1024 * 1024))
    with pytest.raises(ArchiveValidationError):
        import_engagement(ratio, tmp_path / "ratio-destination")
    assert not (tmp_path / "ratio-destination").exists()

    depth = tmp_path / "depth.zip"
    with zipfile.ZipFile(depth, "w") as handle:
        handle.writestr("/".join(["a"] * 17) + ".txt", "safe")
    with pytest.raises(ArchiveValidationError):
        import_engagement(depth, tmp_path / "depth-destination")
    assert not (tmp_path / "depth-destination").exists()

    count = tmp_path / "count.zip"
    with zipfile.ZipFile(count, "w") as handle:
        for index in range(1_026):
            handle.writestr(f"files/{index:04d}.txt", "safe")
    with pytest.raises(ArchiveValidationError):
        import_engagement(count, tmp_path / "count-destination")
    assert not (tmp_path / "count-destination").exists()

    total = tmp_path / "total.zip"
    with zipfile.ZipFile(total, "w", compression=zipfile.ZIP_STORED) as handle:
        handle.writestr("one.txt", b"a" * 700)
        handle.writestr("two.txt", b"b" * 700)
    monkeypatch.setattr("assessment.storage.archive.MAX_TOTAL_BYTES", 1_024)
    with pytest.raises(ArchiveValidationError):
        import_engagement(total, tmp_path / "total-destination")
    assert not (tmp_path / "total-destination").exists()


def test_encrypted_flag_is_rejected_before_destination_mutation(tmp_path: Path) -> None:
    source = create_engagement(tmp_path / "source")
    archive = tmp_path / "plain.zip"
    export_engagement(source, archive)
    encrypted = bytearray(archive.read_bytes())
    local = encrypted.find(b"PK\x03\x04")
    central = encrypted.find(b"PK\x01\x02")
    assert local >= 0 and central >= 0
    local_flags = int.from_bytes(encrypted[local + 6 : local + 8], "little") | 0x1
    central_flags = int.from_bytes(encrypted[central + 8 : central + 10], "little") | 0x1
    encrypted[local + 6 : local + 8] = local_flags.to_bytes(2, "little")
    encrypted[central + 8 : central + 10] = central_flags.to_bytes(2, "little")
    hostile = tmp_path / "encrypted.zip"
    hostile.write_bytes(encrypted)
    destination = tmp_path / "encrypted-destination"
    with pytest.raises(ArchiveValidationError, match="encrypted"):
        import_engagement(hostile, destination)
    assert not destination.exists()


def test_image_evidence_is_metadata_free_and_source_symlinks_are_rejected(
    tmp_path: Path,
) -> None:
    source = create_engagement(tmp_path / "source")
    metadata = PngImagePlugin.PngInfo()
    metadata.add_text("author", "synthetic")
    image_path = source / "evidence/files/proof.png"
    Image.new("RGB", (4, 4), color=(10, 20, 30)).save(image_path, pnginfo=metadata)
    archive = tmp_path / "image.zip"
    export_engagement(source, archive)
    with zipfile.ZipFile(archive) as handle:
        canonical = handle.read("evidence/files/proof.png")
    with Image.open(BytesIO(canonical)) as image:
        assert image.info == {}

    linked_source = tmp_path / "linked-source"
    linked_source.symlink_to(source, target_is_directory=True)
    with pytest.raises(ArchiveValidationError, match="real engagement directory"):
        export_engagement(linked_source, tmp_path / "linked-source-export.zip")

    linked = source / "evidence/files/linked.txt"
    linked.symlink_to(source / "evidence/files/notes.txt")
    with pytest.raises(ArchiveValidationError, match="symlink"):
        export_engagement(source, tmp_path / "symlink-export.zip")


@pytest.mark.skip(reason="ObjectEngagementStore/S3 remains a Phase 2 documentation-only boundary")
def test_future_object_store_contract_placeholder() -> None:
    raise AssertionError("No S3 implementation is authorized")
