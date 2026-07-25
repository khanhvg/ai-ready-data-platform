from __future__ import annotations

import re
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from assessment.domain.errors import ArchiveValidationError, ContentValidationError
from assessment.storage.archive import build_engagement_archive
from assessment.storage.local import LocalEngagementStore
from assessment.web.app import create_app
from assessment.web.config import WebConfig
from assessment.web.dependencies import WebServices
from assessment.web.forms import AnswerForm

CSRF_PATTERN = re.compile(r'name="csrf_token" value="([^"]+)"')
REVISION_PATTERN = re.compile(r'name="revision" value="(\d+)"')


def client_for(tmp_path: Path, *, max_upload_bytes: int | None = None) -> TestClient:
    kwargs = {} if max_upload_bytes is None else {"max_upload_bytes": max_upload_bytes}
    config = WebConfig(
        engagement_root=(tmp_path / "engagements").absolute(),
        runtime_root=(tmp_path / "runtime").absolute(),
        **kwargs,
    )
    return TestClient(create_app(config=config), base_url="http://127.0.0.1")


def csrf_from(response_text: str) -> str:
    match = CSRF_PATTERN.search(response_text)
    assert match is not None
    return match.group(1)


def revision_from(response_text: str) -> str:
    match = REVISION_PATTERN.search(response_text)
    assert match is not None
    return match.group(1)


def test_health_and_secure_headers_disclose_no_customer_state(tmp_path: Path) -> None:
    with client_for(tmp_path) as client:
        response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
    assert response.headers["content-security-policy"].startswith("default-src 'self'")
    assert response.headers["x-content-type-options"] == "nosniff"
    assert response.headers["x-frame-options"] == "DENY"
    assert response.headers["referrer-policy"] == "no-referrer"


def test_host_origin_csrf_and_revision_boundaries(tmp_path: Path) -> None:
    with client_for(tmp_path) as client:
        page = client.get("/engagements")
        token = csrf_from(page.text)
        cookie = page.headers["set-cookie"].lower()
        assert "httponly" in cookie
        assert "samesite=strict" in cookie

        bad_host = client.get("/engagements", headers={"host": "example.invalid"})
        assert bad_host.status_code == 400

        missing_csrf = client.post(
            "/engagements",
            data={"engagement_id": "acme-local"},
        )
        assert missing_csrf.status_code == 403

        bad_origin = client.post(
            "/engagements",
            data={"engagement_id": "acme-local", "csrf_token": token},
            headers={"origin": "https://example.invalid"},
        )
        assert bad_origin.status_code == 403

        created = client.post(
            "/engagements",
            data={"engagement_id": "acme-local", "csrf_token": token},
            headers={"origin": "http://127.0.0.1"},
            follow_redirects=False,
        )
        assert created.status_code == 303

        quick = client.get(created.headers["location"])
        assert quick.status_code == 200
        assert "0 of 30 answered" in quick.text
        quick_token = csrf_from(quick.text)

        saved = client.post(
            "/engagements/acme-local/quick",
            data={
                "csrf_token": quick_token,
                "revision": "0",
                "question_id": "Q-STR-01",
                "rating": "2",
                "evidence_status": "Self-reported",
                "note": "Architect interview.",
            },
            headers={"origin": "http://127.0.0.1"},
            follow_redirects=False,
        )
        assert saved.status_code == 303

        stale = client.post(
            "/engagements/acme-local/quick",
            data={
                "csrf_token": quick_token,
                "revision": "0",
                "question_id": "Q-STR-02",
                "rating": "3",
                "evidence_status": "Partially evidenced",
                "note": "Preserve this unsaved draft.",
            },
            headers={"origin": "http://127.0.0.1"},
        )
        assert stale.status_code == 409
        assert "newer revision" in stale.text
        assert "Preserve this unsaved draft." in stale.text
        assert 'value="3" required' in stale.text


def test_not_assessed_answer_needs_no_contradictory_rating(tmp_path: Path) -> None:
    origin = {"origin": "http://127.0.0.1"}
    with client_for(tmp_path) as client:
        index = client.get("/engagements")
        created = client.post(
            "/engagements",
            data={"engagement_id": "not-assessed", "csrf_token": csrf_from(index.text)},
            headers=origin,
            follow_redirects=False,
        )
        quick = client.get(created.headers["location"])
        assert (
            '<input type="radio" name="rating" value="" required' in quick.text
        )
        saved = client.post(
            "/engagements/not-assessed/quick",
            data={
                "csrf_token": csrf_from(quick.text),
                "revision": revision_from(quick.text),
                "question_id": "Q-STR-01",
                "rating": "",
                "evidence_status": "Not assessed",
                "note": "Deferred to the workshop.",
            },
            headers=origin,
            follow_redirects=False,
        )
        assert saved.status_code == 303
        document = LocalEngagementStore(
            tmp_path / "engagements"
        ).read_document("not-assessed", "assessment/quick.json")
        assert document["answers"][0]["rating"] is None


def test_no_pipeline_command_or_cloud_control_surface(tmp_path: Path) -> None:
    forbidden = (
        "/run",
        "/pipeline",
        "/docker",
        "/sql",
        "/credentials",
        "/cloud",
        "/upload-to-s3",
    )
    with client_for(tmp_path) as client:
        for path in forbidden:
            response = client.get(path)
            assert response.status_code == 404


def test_escaped_notes_and_attachment_only_evidence(tmp_path: Path) -> None:
    origin = {"origin": "http://127.0.0.1"}
    with client_for(tmp_path) as client:
        index = client.get("/engagements")
        created = client.post(
            "/engagements",
            data={"engagement_id": "escaped-local", "csrf_token": csrf_from(index.text)},
            headers=origin,
            follow_redirects=False,
        )
        quick = client.get(created.headers["location"])
        saved = client.post(
            "/engagements/escaped-local/quick",
            data={
                "csrf_token": csrf_from(quick.text),
                "revision": revision_from(quick.text),
                "question_id": "Q-STR-01",
                "rating": "2",
                "evidence_status": "Self-reported",
                "note": "A & B < C",
            },
            headers=origin,
            follow_redirects=False,
        )
        assert saved.status_code == 303
        saved_page = client.get(saved.headers["location"])
        assert "A &amp; B &lt; C" in saved_page.text
        assert "A & B < C" not in saved_page.text

        rejected = client.post(
            "/engagements/escaped-local/evidence",
            data={
                "csrf_token": csrf_from(saved_page.text),
                "revision": revision_from(saved_page.text),
                "question_id": "Q-STR-01",
            },
            files={"evidence_file": ("unsafe.html", b"<script>alert(1)</script>")},
            headers=origin,
        )
        assert rejected.status_code == 422
        assert "type is not admitted" in rejected.text

        for filename, payload in (
            ("invalid.txt", b"\xff"),
            ("invalid.json", b"{not-json}"),
            ("fake.png", b"not-a-png"),
        ):
            invalid_content = client.post(
                "/engagements/escaped-local/evidence",
                data={
                    "csrf_token": csrf_from(saved_page.text),
                    "revision": revision_from(saved_page.text),
                    "question_id": "Q-STR-01",
                },
                files={"evidence_file": (filename, payload)},
                headers=origin,
            )
            assert invalid_content.status_code == 422

        attached = client.post(
            "/engagements/escaped-local/evidence",
            data={
                "csrf_token": csrf_from(saved_page.text),
                "revision": revision_from(saved_page.text),
                "question_id": "Q-STR-01",
            },
            files={"evidence_file": ("architect-note.txt", b"local evidence")},
            headers=origin,
            follow_redirects=False,
        )
        assert attached.status_code == 303
        evidence = client.get(
            "/engagements/escaped-local/evidence/Q-STR-01-architect-note.txt"
        )
        assert evidence.status_code == 200
        assert evidence.content == b"local evidence"
        assert evidence.headers["content-type"] == "application/octet-stream"
        assert evidence.headers["content-disposition"].startswith("attachment;")


def test_evidence_download_rejects_swapped_parent_symlink(tmp_path: Path) -> None:
    services = WebServices(
        WebConfig.for_roots(tmp_path / "engagements", tmp_path / "runtime")
    )
    services.create_engagement("swap-local")
    engagement_root = tmp_path / "engagements" / "swap-local"
    external = tmp_path / "external"
    external.mkdir()
    (external / "leak.txt").write_text("EXTERNAL-SECRET", encoding="utf-8")
    evidence_root = engagement_root / "evidence"
    evidence_root.mkdir()
    (evidence_root / "files").symlink_to(external, target_is_directory=True)

    with TestClient(
        create_app(config=services.config, services=services),
        base_url="http://127.0.0.1",
    ) as client:
        response = client.get("/engagements/swap-local/evidence/leak.txt")
    assert response.status_code == 404
    assert b"EXTERNAL-SECRET" not in response.content


def populated_services(tmp_path: Path, engagement_id: str = "report-local") -> WebServices:
    services = WebServices(
        WebConfig.for_roots(tmp_path / "engagements", tmp_path / "runtime")
    )
    services.create_engagement(engagement_id)
    revision = 0
    for question in services.framework.questions:
        revision = services.save_answer(
            engagement_id,
            expected_revision=revision,
            answer=AnswerForm(
                question_id=str(question["id"]),
                rating=1,
                evidence_status="Self-reported",
                note="Synthetic architect answer.",
            ),
        )
    facts = {
        str(fact["id"]): 1 if fact["type"] == "integer" else False
        for fact in services.framework.diagnostic_facts
    }
    services.save_diagnostic_facts(
        engagement_id,
        expected_revision=revision,
        facts=facts,
    )
    return services


def test_report_output_is_contained_and_manifest_verified(tmp_path: Path) -> None:
    services = populated_services(tmp_path)
    external = tmp_path / "external-report"
    external.mkdir()
    output = services.report_root / "report-local"
    output.symlink_to(external, target_is_directory=True)
    with pytest.raises(ValueError):
        services.generate_report("report-local")
    assert list(external.iterdir()) == []

    output.unlink()
    artifact = services.generate_report("report-local")
    assert artifact.json_bytes
    (output / "report.json").write_bytes(b"{}")
    with pytest.raises(ContentValidationError):
        services.existing_report("report-local")


def test_revision_write_rolls_back_all_payloads_on_failure(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    services = WebServices(
        WebConfig.for_roots(tmp_path / "engagements", tmp_path / "runtime")
    )
    services.create_engagement("rollback-local")
    from assessment.storage import local

    original = local.atomic_write_at
    failed = False

    def fail_state_once(descriptor: int, key: str, content: bytes) -> None:
        nonlocal failed
        if key == "web/state.json" and not failed:
            failed = True
            raise OSError("injected state write failure")
        original(descriptor, key, content)

    monkeypatch.setattr(local, "atomic_write_at", fail_state_once)
    with pytest.raises(OSError):
        services.save_answer(
            "rollback-local",
            expected_revision=0,
            answer=AnswerForm(
                question_id="Q-STR-01",
                rating=1,
                evidence_status="Self-reported",
                note="Must roll back.",
            ),
        )
    assert services.quick_document("rollback-local")["answers"] == []
    assert services.state("rollback-local")["revision"] == 0


def test_creation_failure_never_lists_partial_engagement(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    services = WebServices(
        WebConfig.for_roots(tmp_path / "engagements", tmp_path / "runtime")
    )
    from assessment.storage import local

    original = local.atomic_write_at
    failed = False

    def fail_initial_state_once(descriptor: int, key: str, content: bytes) -> None:
        nonlocal failed
        if key == "web/state.json" and not failed:
            failed = True
            raise OSError("injected creation failure")
        original(descriptor, key, content)

    monkeypatch.setattr(local, "atomic_write_at", fail_initial_state_once)
    with pytest.raises(OSError):
        services.create_engagement("partial-local")
    assert services.list_engagements() == []
    assert list((tmp_path / "engagements").iterdir()) == []


def test_legacy_archive_import_initializes_web_state_and_reopens(tmp_path: Path) -> None:
    source_store = LocalEngagementStore(tmp_path / "legacy")
    engagement_id = "legacy-local"
    engagement = {
        "schema_version": "1.0.0",
        "engagement_id": engagement_id,
        "framework_version": "1.0.0",
        "catalog_version": "1.0.0",
        "demo_content_version": "1.0.0",
        "assessment_profile_id": "quick-v1",
        "gate_bundle_version": 1,
    }
    source_store.create(
        engagement,
        initial_payloads={
            "assessment/quick.json": (
                b'{"answers":[],"diagnostic_facts":{},"engagement_id":"legacy-local",'
                b'"framework_version":"1.0.0","schema_version":"1.0.0"}\n'
            )
        },
    )
    archive_bytes, _ = build_engagement_archive(
        tmp_path / "legacy" / engagement_id
    )
    destination = WebServices(
        WebConfig.for_roots(tmp_path / "imported", tmp_path / "import-runtime")
    )
    token, _ = destination.stage_import(archive_bytes)
    imported_id, _ = destination.import_staged(token)
    assert imported_id == engagement_id
    assert destination.state(engagement_id)["last_saved_status"] == "Imported"

    with TestClient(
        create_app(config=destination.config, services=destination),
        base_url="http://127.0.0.1",
    ) as client:
        reopened = client.get(f"/engagements/{engagement_id}/quick")
    assert reopened.status_code == 200


def test_malformed_phase4_state_is_rejected_before_export(tmp_path: Path) -> None:
    services = WebServices(
        WebConfig.for_roots(tmp_path / "engagements", tmp_path / "runtime")
    )
    services.create_engagement("malformed-local")
    services.store.write_document(
        "malformed-local",
        "findings/review.json",
        {"schema_version": "1.0.0", "reviews": {"F-INVALID": {}}},
    )
    with pytest.raises(ArchiveValidationError):
        build_engagement_archive(tmp_path / "engagements" / "malformed-local")


def test_only_latest_archive_preflight_remains_staged(tmp_path: Path) -> None:
    source = populated_services(tmp_path / "source", engagement_id="bounded-import")
    archive_bytes, _ = source.export_archive("bounded-import")
    destination = WebServices(
        WebConfig.for_roots(tmp_path / "destination", tmp_path / "import-runtime")
    )
    first_token, _ = destination.stage_import(archive_bytes)
    second_token, _ = destination.stage_import(archive_bytes)
    with pytest.raises(ValueError, match="missing or expired"):
        destination.import_staged(first_token)
    assert destination.import_staged(second_token)[0] == "bounded-import"


def test_runtime_start_failure_terminates_spawned_server(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from assessment.web import runtime_smoke

    class FakeProcess:
        returncode: int | None = None

        def poll(self) -> int | None:
            return self.returncode

        def terminate(self) -> None:
            self.returncode = -15

        def kill(self) -> None:
            self.returncode = -9

        def communicate(self, timeout: float) -> tuple[str, None]:
            del timeout
            return "", None

    process = FakeProcess()

    def fail_health(_server: object) -> None:
        raise RuntimeError("injected health failure")

    monkeypatch.setattr(runtime_smoke, "_free_port", lambda: 8765)
    monkeypatch.setattr(runtime_smoke.subprocess, "Popen", lambda *args, **kwargs: process)
    monkeypatch.setattr(runtime_smoke, "_wait_for_health", fail_health)
    with pytest.raises(RuntimeError, match="injected health failure"):
        runtime_smoke._start_server(tmp_path / "failed-server")
    assert process.poll() == -15


def test_request_size_and_read_only_surface_boundaries(tmp_path: Path) -> None:
    with client_for(tmp_path, max_upload_bytes=1) as client:
        too_large = client.post(
            "/engagements",
            content=b"x",
            headers={
                "content-length": str(65_538),
                "origin": "http://127.0.0.1",
            },
        )
        assert too_large.status_code == 413
        assert too_large.json()["error"]["code"] == "request_too_large"
        assert too_large.headers["x-content-type-options"] == "nosniff"

        for path in ("/catalog", "/demo"):
            page = client.get(path)
            assert page.status_code == 200
            assert "not installed" in page.text.lower()
            assert "<button" not in page.text
            assert "<form" not in page.text
