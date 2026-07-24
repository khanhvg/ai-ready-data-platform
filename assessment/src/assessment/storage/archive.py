"""Deterministic export and fully preflighted staged import for engagement folders."""

from __future__ import annotations

import io
import json
import os
import shutil
import stat
import struct
import tempfile
import unicodedata
import uuid
import zipfile
from collections.abc import Iterator, Mapping
from pathlib import Path
from typing import Any

from PIL import Image

from assessment.domain.errors import ArchiveValidationError, CompatibilityError
from assessment.domain.models import (
    AnswerEvidenceDocument,
    Engagement,
    Report,
    validate_relative_posix_path,
)
from assessment.domain.versions import (
    ARCHIVE_FORMAT_VERSION,
    SCHEMA_VERSION,
    require_supported_version,
)
from assessment.storage.hygiene import scan_bytes, scan_json_keys
from assessment.storage.limits import (
    MAX_ARCHIVE_BYTES,
    MAX_ARCHIVE_ENTRIES,
    MAX_COMPRESSION_RATIO,
    MAX_FILE_BYTES,
    MAX_PATH_DEPTH,
    MAX_TOTAL_BYTES,
    STREAM_CHUNK_BYTES,
)
from assessment.storage.local import (
    canonical_json,
    fsync_directory,
    promote_directory_no_replace,
    sha256_bytes,
)

MANIFEST_NAME = "manifest.json"
CHECKSUMS_NAME = "metadata/checksums.json"
FIXED_ZIP_TIME = (1980, 1, 1, 0, 0, 0)
NORMALIZED_FILE_MODE = 0o100644
SUPPORTED_COMPRESSION = {zipfile.ZIP_STORED, zipfile.ZIP_DEFLATED}
TEXT_EXTENSIONS = {
    ".json",
    ".txt",
    ".md",
    ".csv",
    ".yaml",
    ".yml",
    ".html",
    ".css",
}
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg"}
EVIDENCE_TEXT_EXTENSIONS = {".json", ".txt", ".csv"}
EXCLUDED_NAMES = {".engagement.lock", ".DS_Store"}


def _canonical_text(content: bytes, *, context: str) -> bytes:
    try:
        text = content.decode("utf-8", errors="strict")
    except UnicodeDecodeError as error:
        raise ArchiveValidationError(f"{context}: text must be UTF-8") from error
    text = unicodedata.normalize("NFC", text.replace("\r\n", "\n").replace("\r", "\n"))
    return text.encode("utf-8")


def _canonical_image(content: bytes, *, suffix: str, context: str) -> bytes:
    try:
        with Image.open(io.BytesIO(content)) as image:
            image.load()
            if image.width * image.height > 40_000_000:
                raise ArchiveValidationError(f"{context}: image dimensions are too large")
            output = io.BytesIO()
            if suffix == ".png":
                converted = (
                    image.convert("RGBA") if "A" in image.getbands() else image.convert("RGB")
                )
                converted.save(output, format="PNG", optimize=False, compress_level=9)
            else:
                image.convert("RGB").save(
                    output,
                    format="JPEG",
                    quality=95,
                    optimize=False,
                    progressive=False,
                    subsampling=0,
                )
    except ArchiveValidationError:
        raise
    except Exception as error:
        raise ArchiveValidationError(f"{context}: invalid image evidence") from error
    return output.getvalue()


def _canonical_entry(key: str, content: bytes) -> bytes:
    suffix = Path(key).suffix.lower()
    is_evidence = key.startswith("evidence/files/")
    if is_evidence and suffix not in EVIDENCE_TEXT_EXTENSIONS | IMAGE_EXTENSIONS:
        raise ArchiveValidationError(f"{key}: opaque evidence format is not admitted by v1")
    if suffix in TEXT_EXTENSIONS:
        normalized = _canonical_text(content, context=key)
        if suffix == ".json":
            try:
                document = json.loads(normalized)
            except json.JSONDecodeError as error:
                raise ArchiveValidationError(f"{key}: invalid JSON") from error
            scan_json_keys(document, context=key)
            normalized = canonical_json(document)
        scan_bytes(normalized, context=key)
        return normalized
    if is_evidence and suffix in IMAGE_EXTENSIONS:
        scan_bytes(content.replace(b"\x00", b""), context=key)
        normalized = _canonical_image(content, suffix=suffix, context=key)
        if len(normalized) > MAX_FILE_BYTES:
            raise ArchiveValidationError(f"{key}: canonical image exceeds per-file limit")
        return normalized
    raise ArchiveValidationError(f"{key}: unsupported portable file format")


def _excluded_key(key: str) -> bool:
    name = key.rsplit("/", 1)[-1]
    return (
        name in EXCLUDED_NAMES
        or ".tmp-" in name
        or key.startswith("cache/")
        or key.startswith(".cache/")
        or key == CHECKSUMS_NAME
    )


def _validate_export_source(root: Path) -> Engagement:
    if root.is_symlink() or not root.is_dir():
        raise ArchiveValidationError("export source must be a real engagement directory")
    engagement_path = root / "engagement.json"
    if not engagement_path.is_file() or engagement_path.is_symlink():
        raise ArchiveValidationError("engagement.json is missing or is a symlink")
    try:
        return Engagement.model_validate_json(engagement_path.read_bytes())
    except ValueError as error:
        raise ArchiveValidationError("engagement.json violates the v1 contract") from error


def _collect_export_entries(root: Path) -> dict[str, bytes]:
    entries: dict[str, bytes] = {}
    folded: set[str] = set()
    for path in sorted(root.rglob("*")):
        if path.is_symlink():
            raise ArchiveValidationError(
                f"{path.relative_to(root).as_posix()}: archive source symlinks are forbidden"
            )
        if not path.is_file():
            continue
        key = unicodedata.normalize("NFC", path.relative_to(root).as_posix())
        if _excluded_key(key):
            continue
        validate_relative_posix_path(key)
        if len(key.split("/")) > MAX_PATH_DEPTH:
            raise ArchiveValidationError(f"{key}: path depth exceeds v1 limit")
        collision_key = key.casefold()
        if key in entries or collision_key in folded:
            raise ArchiveValidationError(f"{key}: duplicate Unicode/case-fold key")
        content = path.read_bytes()
        if len(content) > MAX_FILE_BYTES:
            raise ArchiveValidationError(f"{key}: file exceeds v1 limit")
        entries[key] = _canonical_entry(key, content)
        folded.add(collision_key)
    checksums = {
        "schema_version": "1.0.0",
        "algorithm": "sha256",
        "files": {key: sha256_bytes(content) for key, content in sorted(entries.items())},
    }
    entries[CHECKSUMS_NAME] = canonical_json(checksums)
    _validate_portable_documents(entries)
    return dict(sorted(entries.items()))


def _validate_portable_documents(entries: Mapping[str, bytes]) -> None:
    for key, content in entries.items():
        if Path(key).suffix.lower() != ".json" or key.startswith("evidence/files/"):
            continue
        try:
            document = json.loads(content)
        except json.JSONDecodeError as error:
            raise ArchiveValidationError(f"{key}: invalid portable JSON state") from error
        if not isinstance(document, dict) or "schema_version" not in document:
            raise ArchiveValidationError(f"{key}: portable state requires schema_version")
        require_supported_version(
            document["schema_version"],
            SCHEMA_VERSION,
            context=key,
        )
        try:
            if key == "engagement.json":
                Engagement.model_validate(document)
            elif key == "assessment/quick.json":
                AnswerEvidenceDocument.model_validate(document)
            elif key == "reports/report.json":
                Report.model_validate(document)
        except ValueError as error:
            raise ArchiveValidationError(f"{key}: document violates its v1 contract") from error


def _entry_records(entries: Mapping[str, bytes]) -> list[dict[str, Any]]:
    return [
        {
            "path": key,
            "size": len(content),
            "sha256": sha256_bytes(content),
            "mode": "0644",
        }
        for key, content in sorted(entries.items())
    ]


def _build_manifest(engagement: Engagement, entries: Mapping[str, bytes]) -> dict[str, Any]:
    records = _entry_records(entries)
    return {
        "format_version": ARCHIVE_FORMAT_VERSION,
        "engagement_id": engagement.engagement_id,
        "schema_version": engagement.schema_version,
        "framework_version": engagement.framework_version,
        "catalog_version": engagement.catalog_version,
        "demo_content_version": engagement.demo_content_version,
        "entries": records,
        "digest": sha256_bytes(canonical_json(records)),
    }


def _zip_info(key: str) -> zipfile.ZipInfo:
    info = zipfile.ZipInfo(filename=key, date_time=FIXED_ZIP_TIME)
    info.compress_type = zipfile.ZIP_STORED
    info.create_system = 3
    info.external_attr = NORMALIZED_FILE_MODE << 16
    info.flag_bits = 0x800
    return info


def export_engagement(root: Path, archive_path: Path) -> dict[str, Any]:
    """Export canonical state as a byte-stable ZIP_STORED archive."""
    engagement = _validate_export_source(root)
    entries = _collect_export_entries(root)
    if len(entries) > MAX_ARCHIVE_ENTRIES:
        raise ArchiveValidationError("archive entry-count limit exceeded")
    total = sum(len(content) for content in entries.values())
    if total > MAX_TOTAL_BYTES:
        raise ArchiveValidationError("archive expanded-size limit exceeded")
    manifest = _build_manifest(engagement, entries)
    payloads = {**entries, MANIFEST_NAME: canonical_json(manifest)}
    archive_path.parent.mkdir(parents=True, exist_ok=True)
    temporary = archive_path.with_name(f".{archive_path.name}.tmp-{uuid.uuid4().hex}")
    try:
        with temporary.open("xb") as raw:
            with zipfile.ZipFile(
                raw,
                "w",
                compression=zipfile.ZIP_STORED,
                allowZip64=False,
            ) as handle:
                for key, content in sorted(payloads.items()):
                    handle.writestr(_zip_info(key), content)
            raw.flush()
            os.fsync(raw.fileno())
        os.chmod(temporary, 0o600)
        os.replace(temporary, archive_path)
        fsync_directory(archive_path.parent)
    finally:
        temporary.unlink(missing_ok=True)
    return manifest


def _raw_central_names(archive_path: Path) -> list[tuple[bytes, int, int, int]]:
    """Read raw central-directory names/flags/method/attributes before decoding."""
    archive_size = archive_path.stat().st_size
    if archive_size > MAX_ARCHIVE_BYTES:
        raise ArchiveValidationError("archive container-size limit exceeded")
    tail_size = min(archive_size, 65_557)
    with archive_path.open("rb") as source:
        source.seek(archive_size - tail_size)
        tail = source.read(tail_size)
    eocd_in_tail = tail.rfind(b"PK\x05\x06")
    if eocd_in_tail < 0 or eocd_in_tail + 22 > len(tail):
        raise ArchiveValidationError("ZIP end-of-central-directory record is missing")
    eocd = archive_size - tail_size + eocd_in_tail
    disk_number, central_disk, disk_entries, total_entries = struct.unpack_from(
        "<HHHH", tail, eocd_in_tail + 4
    )
    central_size, central_offset = struct.unpack_from("<II", tail, eocd_in_tail + 12)
    comment_length = struct.unpack_from("<H", tail, eocd_in_tail + 20)[0]
    if (
        disk_number
        or central_disk
        or disk_entries != total_entries
        or total_entries == 0xFFFF
        or central_size == 0xFFFFFFFF
        or central_offset == 0xFFFFFFFF
        or comment_length
        or eocd + 22 != archive_size
        or central_offset + central_size != eocd
    ):
        raise ArchiveValidationError("multi-disk, ZIP64, comments, or ambiguous layout unsupported")
    with archive_path.open("rb") as source:
        source.seek(central_offset)
        data = source.read(central_size)
    if len(data) != central_size:
        raise ArchiveValidationError("truncated ZIP central directory")
    records: list[tuple[bytes, int, int, int]] = []
    offset = 0
    for _ in range(total_entries):
        if data[offset : offset + 4] != b"PK\x01\x02":
            raise ArchiveValidationError("ZIP central-directory signature is invalid")
        if offset + 46 > len(data):
            raise ArchiveValidationError("truncated ZIP central directory")
        flag_bits = struct.unpack_from("<H", data, offset + 8)[0]
        compression = struct.unpack_from("<H", data, offset + 10)[0]
        name_length = struct.unpack_from("<H", data, offset + 28)[0]
        extra_length = struct.unpack_from("<H", data, offset + 30)[0]
        comment_length = struct.unpack_from("<H", data, offset + 32)[0]
        external_attr = struct.unpack_from("<I", data, offset + 38)[0]
        name_start = offset + 46
        name_end = name_start + name_length
        if name_end > len(data):
            raise ArchiveValidationError("truncated ZIP entry name")
        records.append((data[name_start:name_end], flag_bits, compression, external_attr))
        offset = name_end + extra_length + comment_length
    if not records or offset != central_size:
        raise ArchiveValidationError("ZIP central directory is missing")
    return records


def _decode_raw_name(raw: bytes, flag_bits: int) -> str:
    if b"\x00" in raw or b"\\" in raw:
        raise ArchiveValidationError("ZIP entry name contains NUL or backslash ambiguity")
    encoding = "utf-8" if flag_bits & 0x800 else "cp437"
    try:
        return raw.decode(encoding, errors="strict")
    except UnicodeDecodeError as error:
        raise ArchiveValidationError("ZIP entry name encoding is invalid") from error


def _safe_archive_key(name: str) -> str:
    if name.startswith("/") or name.startswith("\\") or "\x00" in name or "\\" in name:
        raise ArchiveValidationError(f"unsafe archive path: {name!r}")
    if len(name) >= 2 and name[0].isalpha() and name[1] == ":":
        raise ArchiveValidationError(f"unsafe drive path: {name!r}")
    normalized = unicodedata.normalize("NFC", name)
    try:
        validate_relative_posix_path(normalized)
    except ValueError as error:
        raise ArchiveValidationError(f"unsafe archive path: {name!r}") from error
    if len(normalized.split("/")) > MAX_PATH_DEPTH:
        raise ArchiveValidationError(f"{name}: path-depth limit exceeded")
    return normalized


def _regular_entry(info: zipfile.ZipInfo) -> bool:
    if info.is_dir():
        return False
    if info.create_system != 3:
        return True
    mode = (info.external_attr >> 16) & 0xFFFF
    file_type = stat.S_IFMT(mode)
    return file_type in {0, stat.S_IFREG}


def _stream_entry(handle: zipfile.ZipFile, info: zipfile.ZipInfo) -> Iterator[bytes]:
    expanded = 0
    with handle.open(info, "r") as source:
        while True:
            chunk = source.read(STREAM_CHUNK_BYTES)
            if not chunk:
                break
            expanded += len(chunk)
            if expanded > MAX_FILE_BYTES:
                raise ArchiveValidationError(f"{info.filename}: expanded file limit exceeded")
            yield chunk
    if expanded != info.file_size:
        raise ArchiveValidationError(f"{info.filename}: expanded size differs from directory")


def _read_entry_bounded(handle: zipfile.ZipFile, info: zipfile.ZipInfo) -> bytes:
    output = io.BytesIO()
    for chunk in _stream_entry(handle, info):
        output.write(chunk)
    return output.getvalue()


def _preflight(
    archive_path: Path,
) -> tuple[dict[str, Any], dict[str, bytes]]:
    if archive_path.is_symlink() or not archive_path.is_file():
        raise ArchiveValidationError("archive path must be a regular non-symlink file")
    raw_records = _raw_central_names(archive_path)
    if len(raw_records) > MAX_ARCHIVE_ENTRIES + 1:
        raise ArchiveValidationError("archive entry-count limit exceeded")

    entries: dict[str, bytes] = {}
    casefolded: set[str] = set()
    total_expanded = 0
    try:
        with zipfile.ZipFile(archive_path, "r") as handle:
            infos = handle.infolist()
            if len(infos) != len(raw_records):
                raise ArchiveValidationError("central-directory entry count mismatch")
            for info, (raw_name, raw_flags, raw_method, raw_attr) in zip(
                infos, raw_records, strict=False
            ):
                decoded = _decode_raw_name(raw_name, raw_flags)
                if decoded != info.filename:
                    raise ArchiveValidationError("raw and decoded ZIP names differ")
                if raw_method != info.compress_type or raw_attr != info.external_attr:
                    raise ArchiveValidationError("raw ZIP metadata mismatch")
                if info.flag_bits & 0x1:
                    raise ArchiveValidationError(f"{decoded}: encrypted entries are forbidden")
                if info.flag_bits & ~(0x800 | 0x8):
                    raise ArchiveValidationError(f"{decoded}: unsupported ZIP flags")
                if info.compress_type not in SUPPORTED_COMPRESSION:
                    raise ArchiveValidationError(f"{decoded}: unsupported compression")
                if info.extra:
                    raise ArchiveValidationError(f"{decoded}: unsupported ZIP extra fields")
                if not _regular_entry(info):
                    raise ArchiveValidationError(f"{decoded}: non-regular or symlink entry")
                key = _safe_archive_key(decoded)
                collision = key.casefold()
                if key in entries or collision in casefolded:
                    raise ArchiveValidationError(f"{key}: duplicate Unicode/case-fold collision")
                if info.file_size > MAX_FILE_BYTES:
                    raise ArchiveValidationError(f"{key}: declared file-size limit exceeded")
                if info.file_size and info.compress_size == 0:
                    raise ArchiveValidationError(f"{key}: invalid zero compressed size")
                if info.file_size > info.compress_size * MAX_COMPRESSION_RATIO:
                    raise ArchiveValidationError(f"{key}: compression-ratio limit exceeded")
                total_expanded += info.file_size
                if total_expanded > MAX_TOTAL_BYTES:
                    raise ArchiveValidationError("archive expanded-size limit exceeded")
                content = _read_entry_bounded(handle, info)
                entries[key] = content
                casefolded.add(collision)
    except (zipfile.BadZipFile, RuntimeError, NotImplementedError) as error:
        raise ArchiveValidationError("corrupt or unsupported ZIP archive") from error

    manifest_bytes = entries.pop(MANIFEST_NAME, None)
    if manifest_bytes is None:
        raise ArchiveValidationError("archive manifest is missing")
    try:
        manifest = json.loads(manifest_bytes.decode("utf-8", errors="strict"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ArchiveValidationError("archive manifest must be UTF-8 JSON") from error
    if not isinstance(manifest, dict):
        raise ArchiveValidationError("archive manifest must be an object")
    if set(manifest) != {
        "format_version",
        "engagement_id",
        "schema_version",
        "framework_version",
        "catalog_version",
        "demo_content_version",
        "entries",
        "digest",
    }:
        raise ArchiveValidationError("archive manifest has missing or unexpected fields")
    scan_bytes(manifest_bytes, context=MANIFEST_NAME)
    scan_json_keys(manifest, context=MANIFEST_NAME)
    if manifest_bytes != canonical_json(manifest):
        raise ArchiveValidationError("archive manifest is not canonically encoded")
    if manifest.get("format_version") != ARCHIVE_FORMAT_VERSION:
        raise CompatibilityError(
            f"archive: unsupported format version {manifest.get('format_version')!r}"
        )
    records = manifest.get("entries")
    if not isinstance(records, list):
        raise ArchiveValidationError("archive manifest entries are malformed")
    if records != _entry_records(entries):
        raise ArchiveValidationError("archive manifest entries are not canonical")
    if manifest.get("digest") != sha256_bytes(canonical_json(records)):
        raise ArchiveValidationError("archive manifest digest is corrupt")
    expected: dict[str, dict[str, Any]] = {}
    for record in records:
        if not isinstance(record, dict) or set(record) != {"path", "size", "sha256", "mode"}:
            raise ArchiveValidationError("archive manifest entry is malformed")
        key = _safe_archive_key(str(record["path"]))
        if key in expected:
            raise ArchiveValidationError("archive manifest has duplicate entries")
        expected[key] = record
    if set(expected) != set(entries):
        raise ArchiveValidationError("archive manifest and central directory differ")
    for key, content in entries.items():
        record = expected[key]
        if (
            record["size"] != len(content)
            or record["sha256"] != sha256_bytes(content)
            or record["mode"] != "0644"
        ):
            raise ArchiveValidationError(f"{key}: checksum, size, or mode mismatch")
        canonical = _canonical_entry(key, content)
        if canonical != content:
            raise ArchiveValidationError(f"{key}: entry is not canonically encoded")
    try:
        checksums = json.loads(entries[CHECKSUMS_NAME])
    except (KeyError, json.JSONDecodeError) as error:
        raise ArchiveValidationError(
            "portable checksum document is missing or malformed"
        ) from error
    expected_checksums = {
        key: sha256_bytes(content)
        for key, content in sorted(entries.items())
        if key != CHECKSUMS_NAME
    }
    if checksums != {
        "schema_version": "1.0.0",
        "algorithm": "sha256",
        "files": expected_checksums,
    }:
        raise ArchiveValidationError("portable checksum document does not match entries")
    _validate_portable_documents(entries)
    try:
        engagement = Engagement.model_validate_json(entries["engagement.json"])
    except (KeyError, ValueError) as error:
        raise ArchiveValidationError("archive engagement.json violates v1") from error
    if engagement.engagement_id != manifest.get("engagement_id"):
        raise ArchiveValidationError("manifest and engagement IDs differ")
    for field in (
        "schema_version",
        "framework_version",
        "catalog_version",
        "demo_content_version",
    ):
        if getattr(engagement, field) != manifest.get(field):
            raise ArchiveValidationError(f"manifest {field} differs from engagement")
    return manifest, entries


def _reject_destination_path(destination: Path) -> None:
    absolute = destination.absolute()
    if absolute.exists() or absolute.is_symlink():
        raise ArchiveValidationError("import destination already exists")
    current = absolute.parent
    while True:
        if current.is_symlink():
            raise ArchiveValidationError("import destination traverses a symlink")
        if current.exists():
            if not current.is_dir():
                raise ArchiveValidationError("import destination parent is not a directory")
            break
        parent = current.parent
        if parent == current:
            raise ArchiveValidationError("import destination has no existing trusted parent")
        current = parent


def import_engagement(archive_path: Path, destination: Path) -> dict[str, Any]:
    """Validate every byte first, then write a sibling stage and atomically promote it."""
    _reject_destination_path(destination)
    manifest, entries = _preflight(archive_path)
    _reject_destination_path(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    staging = Path(tempfile.mkdtemp(prefix=f".{destination.name}.import-", dir=destination.parent))
    try:
        os.chmod(staging, 0o700)
        for key, content in sorted(entries.items()):
            target = staging.joinpath(*key.split("/"))
            target.parent.mkdir(parents=True, exist_ok=True)
            if target.parent.is_symlink():
                raise ArchiveValidationError(f"{key}: staging parent became a symlink")
            with target.open("xb") as handle:
                handle.write(content)
                handle.flush()
                os.fsync(handle.fileno())
            os.chmod(target, 0o600)
        for directory in sorted(
            (path for path in staging.rglob("*") if path.is_dir()), reverse=True
        ):
            fsync_directory(directory)
        fsync_directory(staging)
        _reject_destination_path(destination)
        try:
            promote_directory_no_replace(staging, destination)
        except FileExistsError as error:
            raise ArchiveValidationError("import destination appeared during promotion") from error
    except Exception:
        shutil.rmtree(staging, ignore_errors=True)
        raise
    return manifest
