"""Injected Phase 1–3 services used by thin web routes."""

from __future__ import annotations

import json
import os
import secrets
import tempfile
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from assessment.catalog.loader import (
    load_catalog,
    load_demo_catalog,
    read_catalog_asset,
)
from assessment.catalog.renderer import catalog_view, demo_view
from assessment.domain.errors import ConcurrentWriteError
from assessment.domain.models import AnswerEvidenceDocument, Engagement
from assessment.engine.evaluator import AssessmentResult, evaluate_assessment
from assessment.frameworks import FrameworkBundle, load_framework
from assessment.reporting.generator import generate_report, source_state_digest
from assessment.reporting.publication import publish_report, read_published_report
from assessment.reporting.renderer import render_report
from assessment.storage.archive import (
    build_engagement_archive,
    import_engagement,
    preflight_engagement_archive,
)
from assessment.storage.local import (
    LocalEngagementStore,
    _ensure_absolute_directory,
    canonical_json,
    validate_identifier,
)
from assessment.web.config import WebConfig
from assessment.web.forms import AnswerForm


class RevisionConflictError(ValueError):
    pass


@dataclass(frozen=True)
class ReportArtifacts:
    report: dict[str, Any]
    json_bytes: bytes
    html_bytes: bytes
    digests: dict[str, str]


@dataclass(frozen=True)
class ReportStatus:
    artifact: ReportArtifacts | None
    stale: bool


class WebServices:
    """Application service boundary; routes do not contain assessment rules."""

    def __init__(
        self,
        config: WebConfig,
        *,
        store: LocalEngagementStore | None = None,
        framework: FrameworkBundle | None = None,
    ) -> None:
        self.config = config
        self.store = store or LocalEngagementStore(config.engagement_root)
        self.framework = framework or load_framework("1.0.0")
        self.catalog = load_catalog("1.0.0")
        self.demo_catalog = load_demo_catalog(
            "1.0.0",
            repository_root=config.repository_root,
        )
        self._imports: dict[str, tuple[bytes, dict[str, Any]]] = {}
        for root in (
            self.config.runtime_root,
            self.report_root,
        ):
            descriptor = _ensure_absolute_directory(root)
            os.close(descriptor)

    @property
    def report_root(self) -> Path:
        return self.config.runtime_root / "reports"

    def catalog_view(self) -> dict[str, Any]:
        return catalog_view(self.catalog)

    def demo_view(self) -> dict[str, Any]:
        return demo_view(self.demo_catalog)

    def catalog_diagram(self, name: str) -> bytes:
        allowed = {
            f"{diagram.id}.svg": diagram.svg_path
            for diagram in self.catalog.diagrams
        }
        path = allowed.get(name)
        if path is None:
            raise ValueError("catalog diagram is not installed")
        return read_catalog_asset(path)

    def create_engagement(self, engagement_id: str) -> Path:
        engagement = Engagement.model_validate(
            {
                "schema_version": "1.0.0",
                "engagement_id": engagement_id,
                "framework_version": self.framework.version,
                "catalog_version": "1.0.0",
                "demo_content_version": "1.0.0",
                "assessment_profile_id": "quick-v1",
                "gate_bundle_version": 1,
            }
        )
        return self.store.create(
            engagement.model_dump(mode="json"),
            initial_payloads={
                "assessment/quick.json": canonical_json(
                    {
                        "schema_version": "1.0.0",
                        "engagement_id": engagement_id,
                        "framework_version": self.framework.version,
                        "answers": [],
                        "diagnostic_facts": {},
                    }
                ),
                "web/state.json": canonical_json(
                    {
                        "schema_version": "1.0.0",
                        "revision": 0,
                        "last_saved_status": "Created",
                    }
                ),
            },
        )

    def list_engagements(self) -> list[str]:
        return self.store.list_engagements()

    def state(self, engagement_id: str) -> dict[str, Any]:
        return self.store.read_document(engagement_id, "web/state.json")

    def quick_document(self, engagement_id: str) -> dict[str, Any]:
        return self.store.read_document(engagement_id, "assessment/quick.json")

    @staticmethod
    def _next_state(revision: int, status: str) -> dict[str, Any]:
        return {
            "schema_version": "1.0.0",
            "revision": revision + 1,
            "last_saved_status": status,
        }

    def _commit(
        self,
        engagement_id: str,
        *,
        expected_revision: int,
        payloads: dict[str, bytes],
        status: str,
    ) -> int:
        updated = expected_revision + 1
        payloads["web/state.json"] = canonical_json(
            self._next_state(expected_revision, status)
        )
        try:
            self.store.write_payloads_if_revision(
                engagement_id,
                revision_key="web/state.json",
                expected_revision=expected_revision,
                payloads=payloads,
            )
        except ConcurrentWriteError as error:
            raise RevisionConflictError(
                "A newer revision is already saved. Reload before applying this change."
            ) from error
        return updated

    def save_answer(
        self,
        engagement_id: str,
        *,
        expected_revision: int,
        answer: AnswerForm,
    ) -> int:
        document = self.quick_document(engagement_id)
        records = {
            str(item["question_id"]): dict(item)
            for item in document.get("answers", [])
        }
        evidence_refs = records.get(answer.question_id, {}).get("evidence_refs", [])
        records[answer.question_id] = {
            "question_id": answer.question_id,
            "rating": answer.rating,
            "evidence_status": answer.evidence_status,
            "note": answer.note,
            "evidence_refs": evidence_refs,
        }
        document["answers"] = [
            records[question["id"]]
            for question in self.framework.questions
            if question["id"] in records
        ]
        AnswerEvidenceDocument.model_validate(document)
        return self._commit(
            engagement_id,
            expected_revision=expected_revision,
            payloads={"assessment/quick.json": canonical_json(document)},
            status=f"Saved {answer.question_id}",
        )

    def save_diagnostic_facts(
        self,
        engagement_id: str,
        *,
        expected_revision: int,
        facts: dict[str, int | bool],
    ) -> int:
        document = self.quick_document(engagement_id)
        document["diagnostic_facts"] = facts
        return self._commit(
            engagement_id,
            expected_revision=expected_revision,
            payloads={"assessment/quick.json": canonical_json(document)},
            status="Saved readiness gate facts",
        )

    def attach_evidence(
        self,
        engagement_id: str,
        *,
        expected_revision: int,
        question_id: str,
        key: str,
        content: bytes,
    ) -> int:
        document = self.quick_document(engagement_id)
        answer = next(
            (
                item
                for item in document.get("answers", [])
                if item["question_id"] == question_id
            ),
            None,
        )
        if answer is None:
            raise ValueError("save the answer before attaching evidence")
        refs = list(answer.get("evidence_refs", []))
        if key not in refs:
            refs.append(key)
        answer["evidence_refs"] = refs
        AnswerEvidenceDocument.model_validate(document)
        return self._commit(
            engagement_id,
            expected_revision=expected_revision,
            payloads={
                key: content,
                "assessment/quick.json": canonical_json(document),
            },
            status=f"Attached evidence to {question_id}",
        )

    def evaluate(self, engagement_id: str) -> AssessmentResult:
        engagement, quick, reviews, _ = self._coherent_assessment(engagement_id)
        return evaluate_assessment(
            quick,
            self.framework,
            reviews=reviews,
            expected_engagement_id=str(engagement["engagement_id"]),
        )

    def _coherent_assessment(
        self,
        engagement_id: str,
    ) -> tuple[
        dict[str, Any],
        dict[str, Any],
        dict[str, dict[str, str]],
        dict[str, str],
    ]:
        documents, snapshot = self.store.read_documents_and_snapshot(
            engagement_id,
            (
                "engagement.json",
                "assessment/quick.json",
                "findings/review.json",
            ),
        )
        engagement = documents["engagement.json"]
        quick = documents["assessment/quick.json"]
        if engagement is None or quick is None:
            raise ValueError("engagement and quick assessment documents are required")
        raw_review = documents["findings/review.json"]
        raw_records = {} if raw_review is None else raw_review.get("reviews", {})
        if not isinstance(raw_records, dict):
            raise ValueError("finding reviews must be an object")
        reviews = {
            str(key): {
                "state": str(value["state"]),
                "edit_note": str(value["edit_note"]),
            }
            for key, value in raw_records.items()
            if isinstance(value, dict)
        }
        return engagement, quick, reviews, snapshot

    def review_records(self, engagement_id: str) -> dict[str, dict[str, str]]:
        try:
            document = self.store.read_document(engagement_id, "findings/review.json")
        except FileNotFoundError:
            return {}
        records = document.get("reviews", {})
        if not isinstance(records, dict):
            raise ValueError("finding reviews must be an object")
        return {
            str(key): {"state": str(value["state"]), "edit_note": str(value["edit_note"])}
            for key, value in records.items()
            if isinstance(value, dict)
        }

    def save_review(
        self,
        engagement_id: str,
        *,
        expected_revision: int,
        finding_id: str,
        state: str,
        edit_note: str,
    ) -> int:
        if state not in {"accept", "defer", "edit-note"}:
            raise ValueError("review state is invalid")
        if len(edit_note) > 4096:
            raise ValueError("review note exceeds 4096 characters")
        generated_ids = {finding.id for finding in self.evaluate(engagement_id).findings}
        if finding_id not in generated_ids:
            raise ValueError("finding is not part of the current generated result")
        reviews = self.review_records(engagement_id)
        reviews[finding_id] = {"state": state, "edit_note": edit_note}
        return self._commit(
            engagement_id,
            expected_revision=expected_revision,
            payloads={
                "findings/review.json": canonical_json(
                    {
                    "schema_version": "1.0.0",
                    "reviews": reviews,
                    }
                )
            },
            status=f"Saved review for {finding_id}",
        )

    def deep_dive_document(self, engagement_id: str) -> dict[str, Any]:
        try:
            return self.store.read_document(
                engagement_id,
                "selections/deep-dives.json",
            )
        except FileNotFoundError:
            return {
                "schema_version": "1.0.0",
                "engagement_id": engagement_id,
                "framework_version": self.framework.version,
                "content_status": "not-installed",
                "selections": [],
            }

    def save_deep_dive_selection(
        self,
        engagement_id: str,
        *,
        expected_revision: int,
        capability_ids: list[str],
        planning_note: str,
    ) -> int:
        domain_order = {
            str(domain["id"]): index
            for index, domain in enumerate(self.framework.domains)
        }
        allowed = set(domain_order)
        selected = sorted(set(capability_ids), key=domain_order.__getitem__)
        if not set(selected) <= allowed:
            raise ValueError("deep-dive selection contains an unknown capability")
        if len(planning_note) > 4096:
            raise ValueError("planning note exceeds 4096 characters")
        return self._commit(
            engagement_id,
            expected_revision=expected_revision,
            payloads={
                "selections/deep-dives.json": canonical_json(
                    {
                    "schema_version": "1.0.0",
                    "engagement_id": engagement_id,
                    "framework_version": self.framework.version,
                    "content_status": "not-installed",
                    "planning_note": planning_note,
                    "selections": [
                        {
                            "capability_id": item,
                            "status": "planned-content-pending",
                        }
                        for item in selected
                    ],
                    }
                )
            },
            status="Saved deep-dive workshop plan",
        )

    def generate_report(self, engagement_id: str) -> ReportArtifacts:
        validate_identifier(engagement_id)
        engagement, quick, reviews, source_snapshot = self._coherent_assessment(
            engagement_id
        )
        generated = generate_report(
            engagement,
            quick,
            reviews=reviews,
            source_snapshot=source_snapshot,
        )
        report = json.loads(generated.json_bytes)
        html = render_report(report)
        output = self.report_root / engagement_id
        output_descriptor = _ensure_absolute_directory(output)
        try:
            digests = publish_report(
                output_descriptor,
                generated.json_bytes,
                html,
                generated.source_state_digest,
            )
        finally:
            os.close(output_descriptor)
        return ReportArtifacts(
            report=report,
            json_bytes=generated.json_bytes,
            html_bytes=html,
            digests=digests,
        )

    def report_status(self, engagement_id: str) -> ReportStatus:
        validate_identifier(engagement_id)
        output = self.report_root / engagement_id
        if not output.exists():
            return ReportStatus(artifact=None, stale=False)
        output_descriptor = _ensure_absolute_directory(output)
        try:
            published = read_published_report(output_descriptor)
        finally:
            os.close(output_descriptor)
        if published is None:
            return ReportStatus(artifact=None, stale=False)
        report, manifest, json_bytes, html_bytes = published
        engagement, quick, reviews, source_snapshot = self._coherent_assessment(
            engagement_id
        )
        current_digest = source_state_digest(
            engagement,
            quick,
            reviews,
            source_snapshot,
        )
        if manifest.get("source_state_digest") != current_digest:
            return ReportStatus(artifact=None, stale=True)
        return ReportStatus(
            artifact=ReportArtifacts(
                report=report,
                json_bytes=json_bytes,
                html_bytes=html_bytes,
                digests=dict(manifest["artifacts"]),
            ),
            stale=False,
        )

    def existing_report(self, engagement_id: str) -> ReportArtifacts | None:
        """Return only a complete report bound to the current source state."""
        return self.report_status(engagement_id).artifact

    def export_archive(self, engagement_id: str) -> tuple[bytes, dict[str, Any]]:
        root = self.store.open(engagement_id)
        with self.store.lock(engagement_id):
            return build_engagement_archive(root)

    @staticmethod
    def _with_temporary_archive(
        content: bytes,
        operation: Any,
    ) -> Any:
        with tempfile.NamedTemporaryFile(
            mode="w+b",
            prefix="assessment-import-",
            suffix=".zip",
        ) as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
            return operation(Path(handle.name))

    def stage_import(self, content: bytes) -> tuple[str, dict[str, Any]]:
        if len(content) > self.config.max_upload_bytes:
            raise ValueError("archive exceeds the configured upload limit")
        token = secrets.token_urlsafe(24)
        manifest = self._with_temporary_archive(
            content,
            preflight_engagement_archive,
        )
        self._imports.clear()
        self._imports[token] = (content, manifest)
        return token, manifest

    def import_staged(self, token: str) -> tuple[str, dict[str, Any]]:
        staged = self._imports.pop(token, None)
        if staged is None:
            raise ValueError("import preflight token is missing or expired")
        content, manifest = staged
        engagement_id = str(manifest["engagement_id"])
        destination = self.config.engagement_root / engagement_id
        imported = self._with_temporary_archive(
            content,
            lambda path: import_engagement(path, destination),
        )
        try:
            self.store.read_document(engagement_id, "web/state.json")
        except FileNotFoundError:
            self.store.write_document(
                engagement_id,
                "web/state.json",
                {
                    "schema_version": "1.0.0",
                    "revision": 0,
                    "last_saved_status": "Imported",
                },
            )
        return engagement_id, imported

    def result_view(self, result: AssessmentResult) -> dict[str, Any]:
        view = asdict(result)
        view["blockers"] = [
            finding
            for finding in view["findings"]
            if finding["priority"] == "Critical blocker"
        ]
        return view
