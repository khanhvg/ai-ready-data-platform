"""Pure, exact-version migration registry for Phase 1 prototype fixtures."""

from __future__ import annotations

import hashlib
import json
import shutil
import tempfile
from collections.abc import Callable, Mapping
from pathlib import Path
from typing import Any

from assessment.domain.errors import CompatibilityError, EngagementExistsError
from assessment.domain.models import AnswerEvidenceDocument, Engagement
from assessment.domain.versions import PROTOTYPE_VERSION, SCHEMA_VERSION
from assessment.storage.hygiene import scan_bytes
from assessment.storage.local import (
    atomic_write,
    canonical_json,
    promote_directory_no_replace,
)

Migration = Callable[[Mapping[str, Any], str], dict[str, dict[str, Any]]]

DOMAIN_ORDER = ("STR", "ING", "STO", "TRN", "QUA", "LIN", "GOV", "SEC", "OPS", "AID")
QUESTION_IDS = tuple(
    f"Q-{domain_id}-{number:02d}" for domain_id in DOMAIN_ORDER for number in range(1, 4)
)
TRANSFORM_ID = "prototype-fixture-to-v1"
PROTOTYPE_FIELDS = {
    "schema_version",
    "scenario_id",
    "rater_id",
    "organization_name",
    "duration_minutes",
    "ratings",
    "evidence_statuses",
    "notes",
    "diagnostic_facts",
    "actionability_review",
}
EVIDENCE_STATUSES = {
    "Self-reported",
    "Partially evidenced",
    "Evidenced",
    "Conflicting evidence",
    "Not assessed",
}


def _validate_prototype_source(source: Mapping[str, Any]) -> None:
    if set(source) != PROTOTYPE_FIELDS:
        raise CompatibilityError("prototype fixture: missing or unexpected fields")
    for field in ("scenario_id", "rater_id", "organization_name"):
        if not isinstance(source.get(field), str) or not source[field]:
            raise CompatibilityError(f"prototype fixture: {field} is required")
    if source.get("rater_id") not in {"architect-a", "architect-b"}:
        raise CompatibilityError("prototype fixture: rater is unsupported")
    duration = source.get("duration_minutes")
    if type(duration) is not int or not 0 < duration <= 60:
        raise CompatibilityError("prototype fixture: duration must be an integer from 1 to 60")
    ratings = source.get("ratings")
    statuses = source.get("evidence_statuses")
    notes = source.get("notes")
    if (
        not isinstance(ratings, list)
        or not isinstance(statuses, list)
        or not isinstance(notes, list)
        or len(ratings) != 30
        or len(statuses) != 30
        or len(notes) != 30
    ):
        raise CompatibilityError(
            "prototype fixture: ratings/statuses/notes must each contain 30 items"
        )
    for index, (rating, status, note) in enumerate(zip(ratings, statuses, notes, strict=True)):
        if rating is not None and (type(rating) is not int or not 0 <= rating <= 4):
            raise CompatibilityError(f"prototype fixture: invalid rating at {index}")
        if status not in EVIDENCE_STATUSES:
            raise CompatibilityError(f"prototype fixture: invalid evidence status at {index}")
        if (rating is None) != (status == "Not assessed"):
            raise CompatibilityError(f"prototype fixture: rating/status mismatch at {index}")
        if not isinstance(note, str) or not note.strip():
            raise CompatibilityError(f"prototype fixture: missing note at {index}")
    diagnostic_facts = source.get("diagnostic_facts")
    if not isinstance(diagnostic_facts, dict) or set(diagnostic_facts) != {
        "privacy_control_level",
        "ownership_control_level",
        "critical_lineage",
        "reproducible_versioned",
    }:
        raise CompatibilityError("prototype fixture: diagnostic facts are malformed")
    for fact_id in ("privacy_control_level", "ownership_control_level"):
        value = diagnostic_facts[fact_id]
        if type(value) is not int or not 0 <= value <= 4:
            raise CompatibilityError(f"prototype fixture: {fact_id} must be an integer from 0 to 4")
    for fact_id in ("critical_lineage", "reproducible_versioned"):
        if type(diagnostic_facts[fact_id]) is not bool:
            raise CompatibilityError(f"prototype fixture: {fact_id} must be boolean")
    review = source.get("actionability_review")
    if (
        not isinstance(review, dict)
        or set(review)
        != {
            "recommendations_actionable",
            "gate_outcome_reasonable",
            "report_usable",
        }
        or any(value is not True for value in review.values())
    ):
        raise CompatibilityError("prototype fixture: actionability review is malformed")
    try:
        scan_bytes(canonical_json(source), context="prototype fixture")
    except ValueError as error:
        raise CompatibilityError("prototype fixture: unsafe authored content") from error
    if any("<" in value or ">" in value for value in _iter_source_strings(source)):
        raise CompatibilityError("prototype fixture: raw HTML-like content is not allowed")


def _iter_source_strings(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, dict):
        return [
            text
            for key, item in value.items()
            for text in (_iter_source_strings(key) + _iter_source_strings(item))
        ]
    if isinstance(value, list):
        return [text for item in value for text in _iter_source_strings(item)]
    return []


def _prototype_to_v1(source: Mapping[str, Any], engagement_id: str) -> dict[str, dict[str, Any]]:
    ratings = source.get("ratings")
    statuses = source.get("evidence_statuses")
    notes = source.get("notes")
    if (
        not isinstance(ratings, list)
        or not isinstance(statuses, list)
        or not isinstance(notes, list)
        or len(ratings) != 30
        or len(statuses) != 30
        or len(notes) != 30
    ):
        raise CompatibilityError(
            "prototype fixture: ratings/statuses/notes must each contain 30 items"
        )
    engagement = Engagement(
        schema_version="1.0.0",
        engagement_id=engagement_id,
        framework_version="1.0.0",
        catalog_version="1.0.0",
        demo_content_version="1.0.0",
        assessment_profile_id="quick-v1",
        gate_bundle_version=1,
    ).model_dump()
    answers = AnswerEvidenceDocument.model_validate(
        {
            "schema_version": "1.0.0",
            "engagement_id": engagement_id,
            "framework_version": "1.0.0",
            "answers": [
                {
                    "question_id": question_id,
                    "rating": ratings[index],
                    "evidence_status": statuses[index],
                    "note": notes[index],
                    "evidence_refs": [],
                }
                for index, question_id in enumerate(QUESTION_IDS)
            ],
            "diagnostic_facts": dict(source.get("diagnostic_facts", {})),
        }
    ).model_dump()
    return {"engagement.json": engagement, "assessment/quick.json": answers}


MIGRATION_REGISTRY: dict[tuple[str, str], Migration] = {
    (PROTOTYPE_VERSION, SCHEMA_VERSION): _prototype_to_v1
}


def _validate_existing_migration(
    destination: Path,
    receipt: Mapping[str, Any],
    documents: Mapping[str, Mapping[str, Any]],
) -> None:
    if destination.is_symlink() or not destination.is_dir():
        raise EngagementExistsError(
            f"migration destination is not a real local directory: {destination}"
        )
    expected_directories = {"assessment", "metadata"}
    expected_files = {
        *documents,
        "metadata/migration-receipt.json",
        "metadata/checksums.json",
    }
    for path in destination.rglob("*"):
        if path.is_symlink():
            raise EngagementExistsError(f"migration destination contains a symlink: {destination}")
    actual_files = {
        path.relative_to(destination).as_posix()
        for path in destination.rglob("*")
        if path.is_file()
    }
    actual_directories = {
        path.relative_to(destination).as_posix()
        for path in destination.rglob("*")
        if path.is_dir() and not path.is_symlink()
    }
    if actual_files != expected_files or actual_directories != expected_directories:
        raise EngagementExistsError(
            f"migration destination state differs from receipt: {destination}"
        )

    expected_payloads = {key: canonical_json(value) for key, value in sorted(documents.items())}
    expected_payloads["metadata/migration-receipt.json"] = canonical_json(receipt)
    for key, expected in expected_payloads.items():
        if destination.joinpath(*key.split("/")).read_bytes() != expected:
            raise EngagementExistsError(
                f"migration destination document differs from receipt: {key}"
            )

    expected_checksums = {
        "schema_version": "1.0.0",
        "algorithm": "sha256",
        "files": {
            key: hashlib.sha256(content).hexdigest()
            for key, content in sorted(expected_payloads.items())
        },
    }
    if (destination / "metadata/checksums.json").read_bytes() != canonical_json(expected_checksums):
        raise EngagementExistsError(
            f"migration destination checksums differ from receipt: {destination}"
        )


def migrate_prototype_fixture(source: Path, destination: Path) -> dict[str, Any]:
    """Copy a frozen prototype fixture into a deterministic v1 engagement folder."""
    source_bytes = source.read_bytes()
    try:
        document = json.loads(source_bytes.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise CompatibilityError("migration source must be UTF-8 JSON") from error
    if not isinstance(document, dict):
        raise CompatibilityError("migration source must be an object")
    source_version = document.get("schema_version")
    transform = MIGRATION_REGISTRY.get((str(source_version), SCHEMA_VERSION))
    if transform is None:
        raise CompatibilityError(
            f"migration: no registry entry for {source_version!r} -> {SCHEMA_VERSION!r}"
        )
    _validate_prototype_source(document)

    engagement_id = destination.name
    try:
        documents = transform(document, engagement_id)
    except ValueError as error:
        raise CompatibilityError(
            "prototype fixture: source or v1 target validation failed"
        ) from error
    source_digest = hashlib.sha256(source_bytes).hexdigest()
    document_records = [
        {
            "path": key,
            "sha256": hashlib.sha256(canonical_json(value)).hexdigest(),
        }
        for key, value in sorted(documents.items())
    ]
    receipt: dict[str, Any] = {
        "schema_version": "1.0.0",
        "migration_id": TRANSFORM_ID,
        "source_version": str(source_version),
        "target_version": SCHEMA_VERSION,
        "source_sha256": source_digest,
        "documents": document_records,
    }
    receipt["receipt_sha256"] = hashlib.sha256(canonical_json(receipt)).hexdigest()

    if destination.exists() or destination.is_symlink():
        receipt_path = destination / "metadata/migration-receipt.json"
        try:
            existing_receipt = (
                json.loads(receipt_path.read_text(encoding="utf-8"))
                if receipt_path.is_file() and not receipt_path.is_symlink()
                else None
            )
        except (UnicodeDecodeError, json.JSONDecodeError, OSError):
            existing_receipt = None
        if existing_receipt == receipt:
            _validate_existing_migration(destination, receipt, documents)
            return receipt
        raise EngagementExistsError(f"migration destination exists: {destination}")

    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary_parent = Path(
        tempfile.mkdtemp(prefix=f".{destination.name}.migration-", dir=destination.parent)
    )
    staged = temporary_parent / destination.name
    try:
        staged.mkdir(mode=0o700)
        for key, value in sorted(documents.items()):
            atomic_write(staged.joinpath(*key.split("/")), canonical_json(value))
        atomic_write(staged / "metadata/migration-receipt.json", canonical_json(receipt))
        checksums = {
            path.relative_to(staged).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in sorted(staged.rglob("*"))
            if path.is_file() and path.name != "checksums.json"
        }
        atomic_write(
            staged / "metadata/checksums.json",
            canonical_json({"schema_version": "1.0.0", "algorithm": "sha256", "files": checksums}),
        )
        try:
            promote_directory_no_replace(staged, destination)
        except FileExistsError as error:
            raise EngagementExistsError(
                f"migration destination appeared during promotion: {destination}"
            ) from error
    finally:
        shutil.rmtree(temporary_parent, ignore_errors=True)
    return receipt
