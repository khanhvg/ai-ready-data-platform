"""Thin server-rendered routes over injected store, engine, report, and archive services."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from fastapi import APIRouter, Request
from fastapi.responses import (
    HTMLResponse,
    JSONResponse,
    RedirectResponse,
    Response,
)
from fastapi.templating import Jinja2Templates
from starlette.datastructures import UploadFile

from assessment.domain.errors import AssessmentError
from assessment.domain.models import validate_identifier, validate_relative_posix_path
from assessment.storage.archive import (
    IMAGE_EXTENSIONS,
    canonicalize_evidence_attachment,
)
from assessment.web.dependencies import RevisionConflictError, WebServices
from assessment.web.forms import (
    EVIDENCE_STATUSES,
    AnswerForm,
    parse_answer,
    parse_revision,
)

router = APIRouter()
templates = Jinja2Templates(directory=Path(__file__).with_name("templates"))
SAFE_UPLOAD_NAME = re.compile(r"[^A-Za-z0-9._-]+")
EVIDENCE_SUFFIXES = {".json", ".txt", ".csv"} | IMAGE_EXTENSIONS


def services(request: Request) -> WebServices:
    return request.app.state.services


def csrf_token(request: Request) -> str:
    return str(request.app.state.csrf.issue(request))


def _csrf_or_403(request: Request, form: Any) -> JSONResponse | None:
    token = str(form.get("csrf_token", ""))
    if request.app.state.csrf.verify(request, token):
        return None
    return JSONResponse(
        {"error": {"code": "invalid_csrf", "message": "CSRF token is invalid."}},
        status_code=403,
    )


def _context(request: Request, **values: Any) -> dict[str, Any]:
    return {"request": request, "csrf_token": csrf_token(request), **values}


def _error(
    request: Request,
    message: str,
    *,
    status_code: int = 422,
    engagement_id: str | None = None,
) -> HTMLResponse:
    return templates.TemplateResponse(
        request,
        "error.html",
        _context(
            request,
            title="Unable to complete the request",
            message=message,
            engagement_id=engagement_id,
        ),
        status_code=status_code,
    )


@router.get("/healthz")
async def health() -> JSONResponse:
    return JSONResponse({"status": "ok"})


@router.get("/")
async def root() -> RedirectResponse:
    return RedirectResponse("/engagements", status_code=303)


@router.get("/engagements")
async def engagement_index(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        request,
        "index.html",
        _context(
            request,
            title="Local engagements",
            engagement_ids=services(request).list_engagements(),
        ),
    )


@router.post("/engagements")
async def create_engagement(request: Request) -> Response:
    form = await request.form()
    if forbidden := _csrf_or_403(request, form):
        return forbidden
    try:
        engagement_id = validate_identifier(str(form.get("engagement_id", "")))
        services(request).create_engagement(engagement_id)
    except (AssessmentError, ValueError) as error:
        return _error(request, str(error))
    return RedirectResponse(
        f"/engagements/{engagement_id}/quick",
        status_code=303,
    )


@router.get("/engagements/{engagement_id}")
async def open_engagement(engagement_id: str) -> RedirectResponse:
    return RedirectResponse(f"/engagements/{engagement_id}/quick", status_code=303)


def _quick_context(
    request: Request,
    engagement_id: str,
    domain_id: str | None,
    *,
    conflict: str | None = None,
    draft_answer: AnswerForm | None = None,
    draft_facts: dict[str, int | bool] | None = None,
) -> dict[str, Any]:
    web = services(request)
    web.store.open(engagement_id)
    framework = web.framework
    domain_ids = [str(domain["id"]) for domain in framework.domains]
    selected_domain = domain_id if domain_id in domain_ids else domain_ids[0]
    document = web.quick_document(engagement_id)
    answers = {
        str(answer["question_id"]): answer for answer in document.get("answers", [])
    }
    if draft_answer is not None:
        answers[draft_answer.question_id] = {
            "question_id": draft_answer.question_id,
            "rating": draft_answer.rating,
            "evidence_status": draft_answer.evidence_status,
            "note": draft_answer.note,
            "evidence_refs": answers.get(draft_answer.question_id, {}).get(
                "evidence_refs", []
            ),
        }
    answered = len(answers)
    return _context(
        request,
        title="Quick assessment",
        engagement_id=engagement_id,
        framework_version=framework.version,
        domains=framework.domains,
        selected_domain=selected_domain,
        questions=[
            question
            for question in framework.questions
            if question["domain_id"] == selected_domain
        ],
        answers=answers,
        evidence_statuses=EVIDENCE_STATUSES,
        diagnostic_facts=framework.diagnostic_facts,
        fact_values=(
            draft_facts
            if draft_facts is not None
            else document.get("diagnostic_facts", {})
        ),
        answered=answered,
        total=len(framework.questions),
        progress_percent=round(answered * 100 / len(framework.questions)),
        state=web.state(engagement_id),
        conflict=conflict,
    )


@router.get("/engagements/{engagement_id}/quick")
async def quick_assessment(
    request: Request,
    engagement_id: str,
    domain: str | None = None,
) -> HTMLResponse:
    try:
        context = _quick_context(request, engagement_id, domain)
    except (AssessmentError, ValueError, FileNotFoundError) as error:
        return _error(request, str(error), status_code=404)
    return templates.TemplateResponse(request, "quick.html", context)


@router.post("/engagements/{engagement_id}/quick")
async def save_quick_answer(
    request: Request,
    engagement_id: str,
) -> Response:
    form = await request.form()
    if forbidden := _csrf_or_403(request, form):
        return forbidden
    domain = str(form.get("domain", ""))
    try:
        web = services(request)
        answer = parse_answer(
            form.get("question_id"),
            form.get("rating"),
            form.get("evidence_status"),
            form.get("note", ""),
            allowed_question_ids={str(item["id"]) for item in web.framework.questions},
        )
        web.save_answer(
            engagement_id,
            expected_revision=parse_revision(form.get("revision")),
            answer=answer,
        )
    except RevisionConflictError as error:
        return templates.TemplateResponse(
            request,
            "quick.html",
            _quick_context(
                request,
                engagement_id,
                domain,
                conflict=str(error),
                draft_answer=answer,
            ),
            status_code=409,
        )
    except (AssessmentError, ValueError) as error:
        return _error(request, str(error), engagement_id=engagement_id)
    target = f"/engagements/{engagement_id}/quick"
    if domain:
        target = f"{target}?domain={domain}"
    return RedirectResponse(target, status_code=303)


@router.post("/engagements/{engagement_id}/quick/facts")
async def save_diagnostic_facts(
    request: Request,
    engagement_id: str,
) -> Response:
    form = await request.form()
    if forbidden := _csrf_or_403(request, form):
        return forbidden
    try:
        facts: dict[str, int | bool] = {}
        for fact in services(request).framework.diagnostic_facts:
            fact_id = str(fact["id"])
            value = str(form.get(fact_id, ""))
            if fact["type"] == "integer":
                parsed = int(value)
                if parsed not in range(5):
                    raise ValueError(f"{fact_id} must be from 0 to 4")
                facts[fact_id] = parsed
            else:
                if value not in {"true", "false"}:
                    raise ValueError(f"{fact_id} must be answered")
                facts[fact_id] = value == "true"
        services(request).save_diagnostic_facts(
            engagement_id,
            expected_revision=parse_revision(form.get("revision")),
            facts=facts,
        )
    except RevisionConflictError as error:
        return templates.TemplateResponse(
            request,
            "quick.html",
            _quick_context(
                request,
                engagement_id,
                None,
                conflict=str(error),
                draft_facts=facts,
            ),
            status_code=409,
        )
    except (AssessmentError, TypeError, ValueError) as error:
        return _error(request, str(error), engagement_id=engagement_id)
    return RedirectResponse(f"/engagements/{engagement_id}/quick", status_code=303)


@router.post("/engagements/{engagement_id}/evidence")
async def add_evidence(
    request: Request,
    engagement_id: str,
) -> Response:
    form = await request.form()
    if forbidden := _csrf_or_403(request, form):
        return forbidden
    upload = form.get("evidence_file")
    if not isinstance(upload, UploadFile) or not upload.filename:
        return _error(request, "Choose an evidence attachment.", engagement_id=engagement_id)
    try:
        question_id = validate_identifier(str(form.get("question_id", "")))
        web = services(request)
        if question_id not in {str(item["id"]) for item in web.framework.questions}:
            raise ValueError("evidence question is not part of the pinned framework")
        suffix = Path(upload.filename).suffix.lower()
        if suffix not in EVIDENCE_SUFFIXES:
            raise ValueError("evidence type is not admitted; use text, JSON, CSV, PNG, or JPEG")
        content = await upload.read(web.config.max_evidence_bytes + 1)
        if len(content) > web.config.max_evidence_bytes:
            raise ValueError("evidence attachment exceeds the configured limit")
        safe_name = SAFE_UPLOAD_NAME.sub("-", Path(upload.filename).name).strip(".-")
        if not safe_name:
            raise ValueError("evidence filename is invalid")
        key = f"evidence/files/{question_id}-{safe_name}"
        validate_relative_posix_path(key)
        content = canonicalize_evidence_attachment(key, content)
        web.attach_evidence(
            engagement_id,
            expected_revision=parse_revision(form.get("revision")),
            question_id=question_id,
            key=key,
            content=content,
        )
    except (AssessmentError, RevisionConflictError, ValueError) as error:
        return _error(
            request,
            str(error),
            status_code=409 if isinstance(error, RevisionConflictError) else 422,
            engagement_id=engagement_id,
        )
    return RedirectResponse(f"/engagements/{engagement_id}/quick", status_code=303)


@router.get("/engagements/{engagement_id}/evidence/{evidence_path:path}")
async def download_evidence(
    request: Request,
    engagement_id: str,
    evidence_path: str,
) -> Response:
    try:
        key = validate_relative_posix_path(f"evidence/files/{evidence_path}")
        content = services(request).store.read_payload(engagement_id, key)
    except (AssessmentError, ValueError, FileNotFoundError) as error:
        return _error(request, str(error), status_code=404, engagement_id=engagement_id)
    return Response(
        content=content,
        media_type="application/octet-stream",
        headers={
            "Content-Disposition": f'attachment; filename="{Path(evidence_path).name}"'
        },
    )


@router.get("/engagements/{engagement_id}/review")
async def review(request: Request, engagement_id: str) -> HTMLResponse:
    try:
        web = services(request)
        result = web.evaluate(engagement_id)
    except (AssessmentError, ValueError, FileNotFoundError) as error:
        return _error(
            request,
            f"Review is not ready: {error}",
            engagement_id=engagement_id,
        )
    return templates.TemplateResponse(
        request,
        "review.html",
        _context(
            request,
            title="Assessment review",
            engagement_id=engagement_id,
            result=web.result_view(result),
            state=web.state(engagement_id),
        ),
    )


@router.post("/engagements/{engagement_id}/review")
async def save_review(
    request: Request,
    engagement_id: str,
) -> Response:
    form = await request.form()
    if forbidden := _csrf_or_403(request, form):
        return forbidden
    try:
        services(request).save_review(
            engagement_id,
            expected_revision=parse_revision(form.get("revision")),
            finding_id=validate_identifier(str(form.get("finding_id", ""))),
            state=str(form.get("review_state", "")),
            edit_note=str(form.get("edit_note", "")),
        )
    except (AssessmentError, RevisionConflictError, ValueError) as error:
        return _error(
            request,
            str(error),
            status_code=409 if isinstance(error, RevisionConflictError) else 422,
            engagement_id=engagement_id,
        )
    return RedirectResponse(f"/engagements/{engagement_id}/review", status_code=303)


@router.get("/engagements/{engagement_id}/deep-dives")
async def deep_dives(request: Request, engagement_id: str) -> HTMLResponse:
    try:
        web = services(request)
        document = web.deep_dive_document(engagement_id)
        web.store.open(engagement_id)
    except (AssessmentError, ValueError, FileNotFoundError) as error:
        return _error(request, str(error), status_code=404)
    return templates.TemplateResponse(
        request,
        "deep-dive-select.html",
        _context(
            request,
            title="Plan deep dives",
            engagement_id=engagement_id,
            domains=web.framework.domains,
            selection=document,
            selected={
                str(item["capability_id"]) for item in document.get("selections", [])
            },
            state=web.state(engagement_id),
        ),
    )


@router.post("/engagements/{engagement_id}/deep-dives")
async def save_deep_dives(
    request: Request,
    engagement_id: str,
) -> Response:
    form = await request.form()
    if forbidden := _csrf_or_403(request, form):
        return forbidden
    try:
        services(request).save_deep_dive_selection(
            engagement_id,
            expected_revision=parse_revision(form.get("revision")),
            capability_ids=[str(item) for item in form.getlist("capability_id")],
            planning_note=str(form.get("planning_note", "")),
        )
    except (AssessmentError, RevisionConflictError, ValueError) as error:
        return _error(
            request,
            str(error),
            status_code=409 if isinstance(error, RevisionConflictError) else 422,
            engagement_id=engagement_id,
        )
    return RedirectResponse(f"/engagements/{engagement_id}/deep-dives", status_code=303)


@router.get("/engagements/{engagement_id}/report")
async def report_view(request: Request, engagement_id: str) -> HTMLResponse:
    try:
        web = services(request)
        web.store.open(engagement_id)
        report_status = web.report_status(engagement_id)
    except (AssessmentError, ValueError, FileNotFoundError) as error:
        return _error(request, str(error), status_code=404)
    return templates.TemplateResponse(
        request,
        "report.html",
        _context(
            request,
            title="Assessment report",
            engagement_id=engagement_id,
            report_status=report_status,
        ),
    )


@router.post("/engagements/{engagement_id}/report")
async def generate_report(
    request: Request,
    engagement_id: str,
) -> Response:
    form = await request.form()
    if forbidden := _csrf_or_403(request, form):
        return forbidden
    try:
        services(request).generate_report(engagement_id)
    except (AssessmentError, ValueError, FileNotFoundError) as error:
        return _error(request, str(error), engagement_id=engagement_id)
    return RedirectResponse(f"/engagements/{engagement_id}/report", status_code=303)


@router.get("/engagements/{engagement_id}/report/{name}")
async def download_report(
    request: Request,
    engagement_id: str,
    name: str,
) -> Response:
    if name not in {"report.json", "report.html"}:
        return _error(request, "report artifact is unavailable", status_code=404)
    report_status = services(request).report_status(engagement_id)
    if report_status.stale:
        return _error(
            request,
            "report is stale; regenerate before download",
            status_code=409,
            engagement_id=engagement_id,
        )
    artifact = report_status.artifact
    if artifact is None:
        return _error(request, "generate the report first", status_code=404)
    content = artifact.json_bytes if name.endswith(".json") else artifact.html_bytes
    return Response(
        content=content,
        media_type="application/octet-stream",
        headers={"Content-Disposition": f'attachment; filename="{name}"'},
    )


@router.get("/engagements/{engagement_id}/archive")
async def archive_page(request: Request, engagement_id: str) -> HTMLResponse:
    try:
        services(request).store.open(engagement_id)
    except (AssessmentError, ValueError, FileNotFoundError) as error:
        return _error(request, str(error), status_code=404)
    return templates.TemplateResponse(
        request,
        "archive.html",
        _context(
            request,
            title="Export engagement",
            engagement_id=engagement_id,
        ),
    )


@router.post("/engagements/{engagement_id}/archive")
async def export_archive(
    request: Request,
    engagement_id: str,
) -> Response:
    form = await request.form()
    if forbidden := _csrf_or_403(request, form):
        return forbidden
    try:
        archive_bytes, _ = services(request).export_archive(engagement_id)
    except (AssessmentError, ValueError, FileNotFoundError) as error:
        return _error(request, str(error), engagement_id=engagement_id)
    return Response(
        content=archive_bytes,
        media_type="application/zip",
        headers={
            "Content-Disposition": f'attachment; filename="{engagement_id}.zip"'
        },
    )


@router.get("/archive/import")
async def import_page(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        request,
        "import.html",
        _context(request, title="Import engagement", preflight=None),
    )


@router.post("/archive/import")
async def preflight_import(
    request: Request,
) -> Response:
    form = await request.form()
    if forbidden := _csrf_or_403(request, form):
        return forbidden
    upload = form.get("archive")
    if not isinstance(upload, UploadFile) or not upload.filename:
        return _error(request, "Choose an engagement ZIP archive.")
    try:
        web = services(request)
        content = await upload.read(web.config.max_upload_bytes + 1)
        token, manifest = web.stage_import(content)
    except (AssessmentError, ValueError, OSError) as error:
        return _error(request, f"Archive preflight failed: {error}")
    return templates.TemplateResponse(
        request,
        "import.html",
        _context(
            request,
            title="Confirm import",
            preflight=manifest,
            import_token=token,
        ),
    )


@router.post("/archive/import/confirm")
async def confirm_import(
    request: Request,
) -> Response:
    form = await request.form()
    if forbidden := _csrf_or_403(request, form):
        return forbidden
    try:
        engagement_id, _ = services(request).import_staged(
            str(form.get("import_token", ""))
        )
    except (AssessmentError, ValueError, OSError) as error:
        return _error(request, f"Import failed: {error}")
    return RedirectResponse(f"/engagements/{engagement_id}/quick", status_code=303)


@router.get("/catalog")
async def catalog(request: Request) -> HTMLResponse:
    framework = services(request).framework
    return templates.TemplateResponse(
        request,
        "catalog.html",
        _context(
            request,
            title="Catalog references",
            architectures=framework.architectures,
        ),
    )


@router.get("/demo")
async def demo(request: Request) -> HTMLResponse:
    references = sorted(
        {
            str(rule.get("demo_reference"))
            for rule in services(request).framework.finding_rules
            if rule.get("demo_reference")
        }
    )
    return templates.TemplateResponse(
        request,
        "demo.html",
        _context(
            request,
            title="Demo-stage artifacts",
            stage_ids=references,
        ),
    )
