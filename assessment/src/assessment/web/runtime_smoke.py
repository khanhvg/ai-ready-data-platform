"""Real loopback Chromium journey shared by E2E and artifact-producing smoke."""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlparse

from playwright.sync_api import (
    Browser,
    BrowserContext,
    ConsoleMessage,
    Page,
    Playwright,
    sync_playwright,
)

from assessment.frameworks import FrameworkBundle, load_framework
from assessment.storage.local import LocalEngagementStore, canonical_json

LOOPBACK_HOSTS = {"127.0.0.1", "::1", "localhost"}


@dataclass
class RunningServer:
    process: subprocess.Popen[str]
    base_url: str
    engagement_root: Path
    runtime_root: Path


def _free_port() -> int:
    with socket.socket() as probe:
        probe.bind(("127.0.0.1", 0))
        return int(probe.getsockname()[1])


def _wait_for_health(server: RunningServer) -> None:
    deadline = time.monotonic() + 20
    last_error: Exception | None = None
    while time.monotonic() < deadline:
        if server.process.poll() is not None:
            output = server.process.communicate(timeout=1)[0]
            raise RuntimeError(f"loopback server exited during startup: {output}")
        try:
            with urllib.request.urlopen(  # noqa: S310 -- fixed loopback URL
                f"{server.base_url}/healthz",
                timeout=0.5,
            ) as response:
                if response.status == 200:
                    return
        except (OSError, urllib.error.URLError) as error:
            last_error = error
            time.sleep(0.1)
    raise RuntimeError(f"loopback server did not become healthy: {last_error}")


def _start_server(root: Path, *, repository_root: Path | None = None) -> RunningServer:
    port = _free_port()
    engagement_root = root / "engagements"
    runtime_root = root / "runtime"
    command = [
        sys.executable,
        "-m",
        "assessment",
        "web",
        "--engagement-root",
        str(engagement_root),
        "--runtime-root",
        str(runtime_root),
    ]
    if repository_root is not None:
        command.extend(["--repository-root", str(repository_root)])
    command.extend(["--host", "127.0.0.1", "--port", str(port)])
    process = subprocess.Popen(  # noqa: S603 -- fixed local package lifecycle command
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        env={key: value for key, value in os.environ.items() if key != "PYTHONPATH"},
    )
    server = RunningServer(
        process=process,
        base_url=f"http://127.0.0.1:{port}",
        engagement_root=engagement_root,
        runtime_root=runtime_root,
    )
    try:
        _wait_for_health(server)
    except Exception:
        _stop_server(server)
        raise
    return server


def _stop_server(server: RunningServer) -> str:
    if server.process.poll() is None:
        server.process.terminate()
    try:
        output = server.process.communicate(timeout=10)[0]
    except subprocess.TimeoutExpired:
        server.process.kill()
        output = server.process.communicate(timeout=5)[0]
    try:
        urllib.request.urlopen(  # noqa: S310 -- fixed loopback teardown probe
            f"{server.base_url}/healthz",
            timeout=0.3,
        )
    except (OSError, urllib.error.URLError):
        return output
    raise RuntimeError("loopback server still accepted requests after teardown")


def _stop_servers(servers: tuple[RunningServer | None, ...]) -> list[str]:
    logs: list[str] = []
    errors: list[Exception] = []
    for server in servers:
        if server is None:
            continue
        try:
            logs.append(_stop_server(server))
        except Exception as error:
            errors.append(error)
    if errors:
        raise ExceptionGroup("one or more loopback servers failed to stop", errors)
    return logs


def _guard_context(
    context: BrowserContext,
    *,
    remote_requests: list[str],
    console_errors: list[str],
    page_errors: list[str],
    request_failures: list[dict[str, str]],
    allowed_file_urls: set[str] | None = None,
) -> None:
    allowed_files = allowed_file_urls or set()

    def route_request(route: Any) -> None:
        parsed = urlparse(route.request.url)
        local_file = route.request.url in allowed_files
        if (
            parsed.hostname not in LOOPBACK_HOSTS
            and parsed.scheme not in {"data", "about"}
            and not local_file
        ):
            remote_requests.append(route.request.url)
            route.abort()
            return
        route.continue_()

    context.route("**/*", route_request)
    def record_console(message: ConsoleMessage) -> None:
        if message.type == "error":
            console_errors.append(message.text)

    def record_page_error(error: Exception) -> None:
        page_errors.append(str(error))

    def record_request_failure(request: Any) -> None:
        request_failures.append(
            {
                "method": str(request.method),
                "url": str(request.url),
                "resource_type": str(request.resource_type),
                "failure": str(request.failure or "unknown failure"),
            }
        )

    context.on("console", record_console)
    context.on("page", lambda page: page.on("pageerror", record_page_error))
    context.on("requestfailed", record_request_failure)


def _partition_request_failures(
    failures: list[dict[str, str]],
) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    expected: list[dict[str, str]] = []
    unexpected: list[dict[str, str]] = []
    for failure in failures:
        path = urlparse(failure["url"]).path
        is_report_download = (
            failure["method"] == "GET"
            and path.endswith(("/report/report.html", "/report/report.json"))
        )
        is_archive_download = (
            failure["method"] == "POST" and path.endswith("/archive")
        )
        is_interrupted_stylesheet = (
            failure["method"] == "GET"
            and failure["resource_type"] == "stylesheet"
            and path == "/static/app.css"
        )
        if (
            failure["failure"] == "net::ERR_ABORTED"
            and (
                is_report_download
                or is_archive_download
                or is_interrupted_stylesheet
            )
        ):
            expected.append(
                {
                    **failure,
                    "reason": (
                        "document navigation interrupted the stylesheet request"
                        if is_interrupted_stylesheet
                        else "attachment download intentionally aborted navigation"
                    ),
                }
            )
        else:
            unexpected.append(failure)
    return expected, unexpected


def _assert_url_suffix(page: Page, suffix: str) -> None:
    if not page.url.endswith(suffix):
        raise AssertionError(f"expected URL suffix {suffix!r}, got {page.url!r}")


def _create_engagement(page: Page, base_url: str, engagement_id: str) -> None:
    page.goto(f"{base_url}/engagements")
    page.keyboard.press("Tab")
    if page.locator(":focus").inner_text() != "Skip to main content":
        raise AssertionError("keyboard focus did not begin at the skip link")
    page.keyboard.press("Enter")
    if page.locator(":focus").get_attribute("id") != "main":
        raise AssertionError("skip link did not move focus to main content")
    page.get_by_label("Stable engagement ID").fill(engagement_id)
    page.get_by_role("button", name="Create engagement").click()
    _assert_url_suffix(page, f"/engagements/{engagement_id}/quick")
    page.get_by_role("heading", name="Quick assessment").wait_for()


def _exercise_autosave(
    page: Page,
    framework: FrameworkBundle,
    transcript: list[dict[str, Any]],
) -> None:
    question = framework.questions[0]
    form = page.locator(
        f'form:has(input[name="question_id"][value="{question["id"]}"])'
    )
    status_control = form.get_by_label("Evidence status")
    status_control.select_option("Not assessed")
    page.locator("#autosave-status").get_by_text("revision 1", exact=False).wait_for(
        timeout=10_000
    )
    if not form.locator('input[name="rating"][value=""]').is_checked():
        raise AssertionError("Not assessed did not select the explicit no-rating state")

    first_rating = form.locator('input[name="rating"][value="0"]')
    first_rating.focus()
    page.keyboard.press("ArrowRight")
    if not form.locator('input[name="rating"][value="1"]').is_checked():
        raise AssertionError("keyboard arrow did not select the next rating")
    if status_control.input_value() != "Self-reported":
        raise AssertionError("selecting a rating did not restore an assessed status")
    page.locator("#autosave-status").get_by_text("revision 2", exact=False).wait_for(
        timeout=10_000
    )
    saved_status = page.locator("#autosave-status").inner_text()

    page.evaluate(
        "() => { window.__assessmentFetch = window.fetch; "
        "window.fetch = () => Promise.resolve({ok: false, status: 503, "
        "text: async () => ''}); }"
    )
    status_control.select_option("Partially evidenced")
    page.locator("#autosave-status").get_by_text("Save failed", exact=False).wait_for(
        timeout=10_000
    )
    page.evaluate(
        "() => { window.fetch = window.__assessmentFetch; "
        "delete window.__assessmentFetch; }"
    )
    form.get_by_role("button", name=f"Save {question['id']}").click()
    page.get_by_role("heading", name="Quick assessment").wait_for()
    transcript.append(
        {
            "step": "autosave",
            "status": saved_status,
            "manual_fallback": "saved",
        }
    )


def _exercise_accessibility(
    page: Page,
    base_url: str,
    engagement_id: str,
    transcript: list[dict[str, Any]],
    console_errors: list[str],
) -> None:
    page.goto(f"{base_url}/engagements")
    page.get_by_label("Stable engagement ID").fill(engagement_id)
    page.get_by_role("button", name="Create engagement").click()
    summary = page.locator("[data-error-summary]")
    summary.wait_for()
    page.wait_for_timeout(100)
    expected_validation_console = (
        "Failed to load resource: the server responded with a status of 422 "
        "(Unprocessable Entity)"
    )
    if expected_validation_console in console_errors:
        console_errors.remove(expected_validation_console)
    if not summary.evaluate("(node) => node === document.activeElement"):
        raise AssertionError("server validation error summary did not receive focus")

    page.goto(f"{base_url}/engagements/{engagement_id}/quick")
    unlabeled = page.locator(
        'input:not([type="hidden"]), select, textarea'
    ).evaluate_all(
        "(nodes) => nodes.filter((node) => !node.labels || node.labels.length === 0)"
        ".map((node) => node.outerHTML)"
    )
    if unlabeled:
        raise AssertionError(f"unlabelled form controls: {unlabeled}")

    page.set_viewport_size({"width": 640, "height": 900})
    page.evaluate("document.body.style.zoom = '200%'")
    overflow = page.evaluate(
        "document.documentElement.scrollWidth > document.documentElement.clientWidth"
    )
    if overflow:
        raise AssertionError("page overflowed horizontally at 200% zoom / 320px reflow")
    page.evaluate("document.body.style.zoom = ''")
    page.set_viewport_size({"width": 375, "height": 812})
    transcript.append(
        {
            "step": "accessibility",
            "error_summary_focus": True,
            "labeled_controls": True,
            "reflow_200_percent": True,
        }
    )


def _assert_report_reflow(
    page: Page,
    transcript: list[dict[str, Any]],
) -> None:
    digests = page.locator(".artifact-digest").all_inner_texts()
    if len(digests) != 2 or any(
        len(digest) != 64
        or any(character not in "0123456789abcdef" for character in digest)
        for digest in digests
    ):
        raise AssertionError(f"report page does not expose two full SHA-256 values: {digests}")
    measurements: dict[str, dict[str, int]] = {}
    page.set_viewport_size({"width": 375, "height": 812})
    measurements["375px"] = page.evaluate(
        "({scroll: document.documentElement.scrollWidth, "
        "client: document.documentElement.clientWidth})"
    )
    page.set_viewport_size({"width": 640, "height": 900})
    page.evaluate("document.body.style.zoom = '200%'")
    measurements["200%-320px-equivalent"] = page.evaluate(
        "({scroll: document.documentElement.scrollWidth, "
        "client: document.documentElement.clientWidth})"
    )
    page.evaluate("document.body.style.zoom = ''")
    page.set_viewport_size({"width": 1280, "height": 900})
    if any(item["scroll"] > item["client"] for item in measurements.values()):
        raise AssertionError(f"report page overflowed horizontally: {measurements}")
    transcript.append(
        {
            "step": "report-reflow",
            "measurements": measurements,
            "full_hashes_visible": True,
        }
    )


def _inspect_standalone_report(
    page: Page,
    html_path: Path,
    report_path: Path,
    evidence_root: Path,
    transcript: list[dict[str, Any]],
) -> None:
    page.goto(html_path.resolve().as_uri())
    if page.locator("#technology-options article table").count() != 3:
        raise AssertionError("standalone report does not contain all three profile tables")
    if page.locator(".diagram svg").count() != 7:
        raise AssertionError("standalone report does not contain all seven diagrams")
    if page.locator(".diagram p").count() != 7:
        raise AssertionError("standalone report does not contain seven text alternatives")
    if page.locator("script, form, a, button, input, select, textarea").count():
        raise AssertionError("standalone report unexpectedly exposes executable controls")

    report = json.loads(report_path.read_bytes())
    appendix = next(
        section["content"]
        for section in report["sections"]
        if section["id"] == "evidence-appendix"
    )
    visible_digests = page.locator("#evidence-appendix code").all_inner_texts()
    if appendix["source_state_digest"] not in visible_digests or any(
        len(digest) != 64 or any(character not in "0123456789abcdef" for character in digest)
        for digest in visible_digests
    ):
        raise AssertionError(
            "standalone report does not expose full source/revision digests: "
            f"{visible_digests}"
        )
    profile_statuses = page.locator("#technology-options article > p").all_inner_texts()
    if sum("content only · non-executable" in status for status in profile_statuses) != 3:
        raise AssertionError("standalone report omits a technology-profile safety status")
    if page.locator("#technology-options th, #technology-options td").evaluate_all(
        "(cells) => cells.some((cell) => !cell.innerText.trim())"
    ):
        raise AssertionError("standalone profile tables contain an empty visible cell")
    technology = next(
        section["content"]
        for section in report["sections"]
        if section["id"] == "technology-options"
    )
    expected_rows = [
        [
            [
                role["role"],
                role["selected_tool"] if role["selected_tool"] else ", ".join(role["alternatives"]),
                "; ".join(role["constraints"]),
            ]
            for role in profile["roles"]
        ]
        for profile in technology["profiles"]
    ]
    actual_rows = page.locator("#technology-options article table").evaluate_all(
        """(tables) => tables.map((table) =>
            [...table.tBodies[0].rows].map((row) =>
                [...row.cells].map((cell) => cell.innerText.trim())
            )
        )"""
    )
    if actual_rows != expected_rows:
        raise AssertionError("standalone profile tables differ from canonical report JSON")

    measurements: dict[str, Any] = {}
    viewports = (
        ("wide", 1280, 900, ""),
        ("375px", 375, 812, ""),
        ("200%-320px-equivalent", 640, 900, "200%"),
    )
    for name, width, height, zoom in viewports:
        page.set_viewport_size({"width": width, "height": height})
        page.evaluate("(zoom) => { document.body.style.zoom = zoom; }", zoom)
        measurements[name] = page.evaluate(
            """() => {
                const documentElement = document.documentElement;
                const profileTables = [...document.querySelectorAll(
                    "#technology-options article table"
                )];
                const tables = [...document.querySelectorAll("table")];
                const visibleNodes = [...document.querySelectorAll("th, td, code")];
                const rows = [...document.querySelectorAll(
                    "#technology-options article tr"
                )];
                const parseRgb = (value) =>
                    (value.match(/[0-9.]+/g) || []).slice(0, 3).map(Number);
                const luminance = (value) => {
                    const channels = parseRgb(value).map((channel) => {
                        const normalized = channel / 255;
                        return normalized <= 0.04045
                            ? normalized / 12.92
                            : ((normalized + 0.055) / 1.055) ** 2.4;
                    });
                    return (
                        0.2126 * channels[0] +
                        0.7152 * channels[1] +
                        0.0722 * channels[2]
                    );
                };
                const contrast = (foreground, background) => {
                    const first = luminance(foreground);
                    const second = luminance(background);
                    return (Math.max(first, second) + 0.05) /
                        (Math.min(first, second) + 0.05);
                };
                const section = document.querySelector("section");
                const bodyStyle = getComputedStyle(document.body);
                const sectionStyle = getComputedStyle(section);
                const mutedStyle = getComputedStyle(document.querySelector(".meta"));
                return {
                    scroll: documentElement.scrollWidth,
                    client: documentElement.clientWidth,
                    bodyFontSize: parseFloat(bodyStyle.fontSize),
                    bodyTextContrast: contrast(bodyStyle.color, sectionStyle.backgroundColor),
                    mutedTextContrast: contrast(
                        mutedStyle.color,
                        sectionStyle.backgroundColor
                    ),
                    tableRects: profileTables.map((table) => {
                        const rect = table.getBoundingClientRect();
                        return {
                            left: Math.round(rect.left),
                            right: Math.round(rect.right),
                            width: Math.round(rect.width),
                            scrollWidth: table.scrollWidth,
                            clientWidth: table.clientWidth,
                        };
                    }),
                    overflowingElements: [...document.body.querySelectorAll("*")]
                        .filter((node) => {
                            const rect = node.getBoundingClientRect();
                            return rect.width > 0 && (
                                rect.left < -0.5 ||
                                rect.right > documentElement.clientWidth + 0.5
                            );
                        })
                        .slice(0, 20)
                        .map((node) => {
                            const rect = node.getBoundingClientRect();
                            return {
                                tag: node.tagName,
                                id: node.id,
                                className: node.getAttribute("class") || "",
                                left: Math.round(rect.left),
                                right: Math.round(rect.right),
                                text: (node.textContent || "").trim().slice(0, 80),
                            };
                        }),
                    clippedCells: visibleNodes.filter((node) =>
                        node.scrollWidth > node.clientWidth ||
                        node.scrollHeight > node.clientHeight
                    ).length,
                    clippedTables: tables.filter((table) =>
                        table.scrollWidth > table.clientWidth
                    ).length,
                    overlappingRows: rows.slice(1).filter((row, index) =>
                        row.getBoundingClientRect().top <
                        rows[index].getBoundingClientRect().bottom - 0.5
                    ).length,
                };
            }"""
        )
        page.screenshot(
            path=evidence_root / f"standalone-report-{name}.png",
            full_page=True,
        )
        page.locator("#technology-options").screenshot(
            path=evidence_root / f"standalone-technology-options-{name}.png",
        )
    page.evaluate("document.body.style.zoom = ''")
    (evidence_root / "standalone-report-measurements.json").write_bytes(
        canonical_json(measurements)
    )

    failures: list[str] = []
    for name, measurement in measurements.items():
        if measurement["scroll"] > measurement["client"]:
            failures.append(f"{name}: document {measurement['scroll']}>{measurement['client']}")
        for index, table in enumerate(measurement["tableRects"], start=1):
            if (
                table["left"] < 0
                or table["right"] > measurement["client"]
                or table["scrollWidth"] > table["clientWidth"]
            ):
                failures.append(f"{name}: profile table {index} {table}")
        if measurement["clippedCells"]:
            failures.append(
                f"{name}: {measurement['clippedCells']} table cells or digests clip content"
            )
        if measurement["overflowingElements"]:
            failures.append(
                f"{name}: elements extend off-screen {measurement['overflowingElements']}"
            )
        if measurement["clippedTables"]:
            failures.append(f"{name}: {measurement['clippedTables']} tables clip content")
        if measurement["overlappingRows"]:
            failures.append(f"{name}: {measurement['overlappingRows']} profile rows overlap")
        if measurement["bodyFontSize"] < 14:
            failures.append(f"{name}: body text is only {measurement['bodyFontSize']}px")
        if measurement["bodyTextContrast"] < 4.5:
            failures.append(f"{name}: body text contrast is {measurement['bodyTextContrast']}")
        if measurement["mutedTextContrast"] < 4.5:
            failures.append(f"{name}: muted text contrast is {measurement['mutedTextContrast']}")
    if failures:
        raise AssertionError(
            "standalone report reflow failed: "
            + "; ".join(failures)
            + f"; measurements={measurements}"
        )
    transcript.append(
        {
            "step": "standalone-report-reflow",
            "measurements": measurements,
            "profile_tables": 3,
            "profile_rows": sum(len(rows) for rows in expected_rows),
            "canonical_profile_content": True,
            "full_source_digest": True,
            "diagram_text_alternatives": 7,
            "controls": 0,
        }
    )


def _save_answer(
    page: Page,
    base_url: str,
    engagement_id: str,
    question: dict[str, Any],
    *,
    note: str,
    rating: str = "1",
    evidence_status: str = "Self-reported",
) -> None:
    page.goto(
        f"{base_url}/engagements/{engagement_id}/quick?domain={question['domain_id']}"
    )
    form = page.locator(
        f'form:has(input[name="question_id"][value="{question["id"]}"])'
    )
    form.locator(f'input[name="rating"][value="{rating}"]').check()
    form.get_by_label("Evidence status").select_option(evidence_status)
    form.get_by_label("Architect note").fill(note)
    form.get_by_role("button", name=f"Save {question['id']}").click()
    _assert_url_suffix(page, f"/quick?domain={question['domain_id']}")


def _complete_plain_form_assessment(
    page: Page,
    base_url: str,
    engagement_id: str,
    framework: FrameworkBundle,
    evidence_root: Path,
    transcript: list[dict[str, Any]],
) -> None:
    first = framework.questions[0]
    page.goto(f"{base_url}/engagements/{engagement_id}/quick?domain={first['domain_id']}")
    first_form = page.locator(
        f'form:has(input[name="question_id"][value="{first["id"]}"])'
    )
    first_note = first_form.get_by_label("Architect note")
    first_note.fill("Unsaved reset probe")
    first_form.get_by_role("button", name="Reset unsaved changes").click()
    if first_note.input_value() != "":
        raise AssertionError("native form reset did not restore the saved value")

    for index, question in enumerate(framework.questions):
        note = "A & B < C" if index == 0 else f"Synthetic architect note {index + 1}"
        _save_answer(
            page,
            base_url,
            engagement_id,
            question,
            note=note,
        )
        if index == 0:
            page.go_back()
            page.reload()
            page.goto(
                f"{base_url}/engagements/{engagement_id}/quick?domain={question['domain_id']}"
            )

    page.goto(f"{base_url}/engagements/{engagement_id}/quick")
    facts_form = page.locator('form[action$="/quick/facts"]')
    facts_form.locator('input[name="privacy_control_level"][value="1"]').check()
    facts_form.locator('input[name="ownership_control_level"][value="1"]').check()
    facts_form.locator('input[name="critical_lineage"][value="false"]').check()
    facts_form.locator('input[name="reproducible_versioned"][value="false"]').check()
    facts_form.get_by_role("button", name="Save gate facts").click()
    _assert_url_suffix(page, f"/engagements/{engagement_id}/quick")
    if "30 of 30 answered" not in page.locator("main").inner_text():
        raise AssertionError("plain-form assessment did not retain all 30 answers")

    evidence_file = evidence_root / "synthetic-evidence.txt"
    evidence_file.write_text("Sanitized synthetic evidence.\n", encoding="utf-8")
    evidence_form = page.locator('form[action$="/evidence"]')
    evidence_form.get_by_label("Saved answer").select_option(str(first["id"]))
    evidence_form.get_by_label("Evidence file").set_input_files(evidence_file)
    evidence_form.get_by_role("button", name="Attach as evidence").click()
    _assert_url_suffix(page, f"/engagements/{engagement_id}/quick")
    transcript.append({"step": "plain-form-quick", "answers": 30, "facts": 4})


def _review_select_report_export(
    page: Page,
    base_url: str,
    engagement_id: str,
    framework: FrameworkBundle,
    evidence_root: Path,
    transcript: list[dict[str, Any]],
) -> tuple[Path, Path, Path]:
    page.goto(f"{base_url}/engagements/{engagement_id}/review")
    text = page.locator("main").inner_text()
    for expected in ("30/30", "All readiness gate traces", "Triggered", "Recommendation"):
        if expected not in text:
            raise AssertionError(f"review is missing visible state: {expected}")
    if page.locator('form[action$="/review"]').count():
        review_form = page.locator('form[action$="/review"]').first
        review_form.locator('input[value="accept"]').check()
        review_form.get_by_label("Architect edit note").fill(
            "Accepted for roadmap sequencing."
        )
        review_form.get_by_role("button", name="Save review record").click()
        _assert_url_suffix(page, f"/engagements/{engagement_id}/review")

    page.goto(f"{base_url}/engagements/{engagement_id}/deep-dives")
    page.get_by_text("Validated question banks are installed", exact=False).wait_for()
    page.locator('input[name="capability_id"][value="QUA"]').check()
    page.get_by_label("Workshop planning note").fill(
        "Complete the validated quality workshop with synthetic evidence."
    )
    page.get_by_role("button", name="Save workshop plan").click()
    _assert_url_suffix(page, f"/engagements/{engagement_id}/deep-dives")
    page.get_by_role("link", name="Open data-quality").click()
    _assert_url_suffix(
        page, f"/engagements/{engagement_id}/deep-dives/data-quality"
    )
    for index in range(1, 21):
        question_id = f"DQ-{index:02d}"
        page.locator(f"#rating-{question_id}").select_option("4")
        page.locator(f"#evidence-status-{question_id}").select_option("Evidenced")
        page.locator(f"#note-{question_id}").fill(
            "Sanitized synthetic deep-dive evidence."
        )
    page.get_by_role("button", name="Complete advisory deep dive").click()
    page.get_by_text("Advisory result · no readiness effect", exact=False).wait_for()
    source_values = parse_qs(urlparse(page.url).query).get("source", [])
    if len(source_values) != 1:
        raise AssertionError("deep-dive completion did not expose one source digest")
    source_digest = source_values[0]
    transcript.append(
        {
            "step": "deep-dive-advisory",
            "deep_dive_id": "data-quality",
            "answers": 20,
            "source_digest": source_digest,
            "readiness_effect": False,
        }
    )

    page.goto(f"{base_url}/engagements/{engagement_id}/report")
    page.get_by_role("button", name="Generate report").click()
    _assert_url_suffix(page, f"/engagements/{engagement_id}/report")
    page.get_by_text("Report generated", exact=False).wait_for()
    _assert_report_reflow(page, transcript)

    _save_answer(
        page,
        base_url,
        engagement_id,
        framework.questions[0],
        note="Changed after the initial report was generated.",
        rating="4",
        evidence_status="Evidenced",
    )
    page.goto(f"{base_url}/engagements/{engagement_id}/report")
    page.get_by_text("Report is stale", exact=False).wait_for()
    if page.get_by_role("link", name="Download canonical JSON").count():
        raise AssertionError("stale report still exposes a download link")
    stale_download = page.request.get(
        f"{base_url}/engagements/{engagement_id}/report/report.json"
    )
    if stale_download.status != 409:
        raise AssertionError(
            f"stale report download returned {stale_download.status}, expected 409"
        )
    page.get_by_role("button", name="Regenerate report").click()
    _assert_url_suffix(page, f"/engagements/{engagement_id}/report")
    page.get_by_text("Report generated", exact=False).wait_for()

    page.goto(
        f"{base_url}/engagements/{engagement_id}/deep-dives/data-quality"
        f"?source={source_digest}"
    )
    page.get_by_label("Include in reviewed promotion").check()
    page.get_by_label("Use deep-dive advisory").check()
    page.get_by_label("Reviewed by accountable architect").fill(
        "solution-architect"
    )
    page.get_by_label("Promotion rationale").fill(
        "Reviewed the complete synthetic quality deep dive and conflicts."
    )
    page.get_by_role("button", name="Create reviewed result revision").click()
    page.get_by_text("reviewed-promotion", exact=False).wait_for()
    if "retained" not in page.locator("main").inner_text():
        raise AssertionError("promotion did not retain the prior result revision")
    page.reload()
    page.go_back()
    page.goto(
        f"{base_url}/engagements/{engagement_id}/deep-dives/data-quality"
        f"?source={source_digest}"
    )
    page.get_by_text("reviewed-promotion", exact=False).wait_for()
    page.goto(f"{base_url}/engagements/{engagement_id}/review")
    review_text = page.locator("main").inner_text()
    for expected in (
        "Accountable roadmap action",
        "Vendor-neutral technology options",
        "reviewed-promotion",
        "retained",
    ):
        if expected not in review_text:
            raise AssertionError(
                f"promoted review is missing visible state: {expected}"
            )
    transcript.append(
        {
            "step": "reviewed-promotion",
            "source_digest": source_digest,
            "prior_revision_retained": True,
            "full_gate_traces": 7,
        }
    )

    page.goto(f"{base_url}/engagements/{engagement_id}/report")
    page.get_by_text("Report is stale", exact=False).wait_for()
    page.get_by_role("button", name="Regenerate report").click()
    _assert_url_suffix(page, f"/engagements/{engagement_id}/report")
    page.get_by_text("Report generated", exact=False).wait_for()

    with page.expect_download() as html_download:
        page.get_by_role("link", name="Download standalone HTML").click()
    html_path = evidence_root / "report.html"
    html_download.value.save_as(html_path)
    with page.expect_download() as json_download:
        page.get_by_role("link", name="Download canonical JSON").click()
    json_path = evidence_root / "report.json"
    json_download.value.save_as(json_path)
    standalone_page = page.context.new_page()
    try:
        _inspect_standalone_report(
            standalone_page,
            html_path,
            json_path,
            evidence_root,
            transcript,
        )
    finally:
        standalone_page.close()

    page.goto(f"{base_url}/engagements/{engagement_id}/archive")
    with page.expect_download() as archive_download:
        page.get_by_role("button", name="Download engagement archive").click()
    archive_path = evidence_root / "engagement.zip"
    archive_download.value.save_as(archive_path)
    transcript.append(
        {
            "step": "review-select-report-export",
            "report_sections": len(json.loads(json_path.read_bytes())["sections"]),
            "stale_after_mutation": True,
            "current_after_regeneration": True,
        }
    )
    return html_path, json_path, archive_path


def _import_reopen_compare(
    page: Page,
    server: RunningServer,
    source_server: RunningServer,
    engagement_id: str,
    archive_path: Path,
    original_report: Path,
    evidence_root: Path,
    transcript: list[dict[str, Any]],
) -> Path:
    page.goto(f"{server.base_url}/archive/import")
    page.get_by_label("Engagement ZIP archive").set_input_files(archive_path)
    page.get_by_role("button", name="Run non-mutating preflight").click()
    page.get_by_text("Preflight passed", exact=False).wait_for()
    page.get_by_role("button", name="Import into configured root").click()
    _assert_url_suffix(page, f"/engagements/{engagement_id}/quick")
    page.get_by_text("30 of 30 answered", exact=False).wait_for()

    source_snapshot = LocalEngagementStore(source_server.engagement_root).snapshot(
        engagement_id
    )
    imported_snapshot = LocalEngagementStore(server.engagement_root).snapshot(engagement_id)
    if source_snapshot != imported_snapshot:
        raise AssertionError("distinct-root imported engagement differs from source state")

    page.goto(f"{server.base_url}/engagements/{engagement_id}/deep-dives")
    if not page.locator('input[name="capability_id"][value="QUA"]').is_checked():
        raise AssertionError("deep-dive selection did not reopen after import")
    page.goto(f"{server.base_url}/engagements/{engagement_id}/review")
    if page.locator('input[value="accept"]:checked').count() != 1:
        raise AssertionError("architect review record did not reopen after import")

    page.goto(f"{server.base_url}/engagements/{engagement_id}/report")
    page.get_by_role("button", name="Generate report").click()
    _assert_url_suffix(page, f"/engagements/{engagement_id}/report")
    with page.expect_download() as imported_download:
        page.get_by_role("link", name="Download canonical JSON").click()
    imported_report = evidence_root / "imported-report.json"
    imported_download.value.save_as(imported_report)
    if imported_report.read_bytes() != original_report.read_bytes():
        raise AssertionError("distinct-root regenerated report JSON is not byte-identical")
    transcript.append(
        {
            "step": "import-reopen-compare",
            "source_files": len(source_snapshot),
            "report_equal": True,
        }
    )
    return imported_report


def _read_only_surfaces(
    page: Page,
    base_url: str,
    evidence_root: Path,
    transcript: list[dict[str, Any]],
) -> None:
    page.set_viewport_size({"width": 1280, "height": 900})
    page.goto(f"{base_url}/catalog")
    catalog_text = page.locator("main").inner_text().lower()
    if "10 capability domains" not in catalog_text:
        raise AssertionError("/catalog did not present the validated catalog")
    if page.locator("img.catalog-diagram").count() != 7:
        raise AssertionError("/catalog did not present exactly seven local diagrams")
    page.locator("img.catalog-diagram").last.scroll_into_view_if_needed()
    page.wait_for_load_state("networkidle")
    loaded_diagrams = page.locator("img.catalog-diagram").evaluate_all(
        "(images) => images.filter((image) => image.complete && image.naturalWidth > 0).length"
    )
    if loaded_diagrams != 7:
        raise AssertionError("/catalog did not render all seven local diagrams")
    diagram_sources = page.locator("img.catalog-diagram").evaluate_all(
        "(images) => images.map((image) => image.getAttribute('src'))"
    )
    if any(
        not isinstance(source, str)
        or not source.startswith("/catalog/diagrams/")
        for source in diagram_sources
    ):
        raise AssertionError("/catalog exposed a non-local diagram asset")
    if page.get_by_role("button").count() or page.locator("form").count():
        raise AssertionError("/catalog unexpectedly exposes a control action")
    page.screenshot(path=evidence_root / "catalog-wide.png", full_page=True)

    page.set_viewport_size({"width": 375, "height": 812})
    page.reload()
    if page.evaluate("document.documentElement.scrollWidth > window.innerWidth"):
        raise AssertionError("/catalog overflows the narrow viewport")
    page.screenshot(path=evidence_root / "catalog-narrow.png", full_page=True)

    page.set_viewport_size({"width": 640, "height": 900})
    page.goto(f"{base_url}/demo")
    demo_text = page.locator("main").inner_text().lower()
    for expected in (
        "9 read-only presenter stages",
        "30/30 = 100%",
        "artifact available",
        "demo artifacts are illustrations only",
        "current openmetadata execution is unexecuted",
        "demo/manifests/stages/ingestion.yaml",
        "demo/manifests/stages/quality-quarantine.yaml",
        "demo/manifests/stages/transformation.yaml",
        "demo/manifests/stages/metadata.yaml",
        "demo/manifests/stages/lineage.yaml",
        "demo/manifests/stages/governance.yaml",
        "demo/manifests/stages/access-control.yaml",
        "demo/manifests/stages/serving.yaml",
        "demo/manifests/stages/ai-ready-publication.yaml",
        "demo/manifests/ai-ready-customer-product.v1.yaml",
    ):
        if expected not in demo_text:
            raise AssertionError(f"/demo did not present expected status: {expected}")
    if page.locator("button, form, input, select, textarea").count():
        raise AssertionError("/demo unexpectedly exposes a control action")
    page.screenshot(path=evidence_root / "demo-200-percent-equivalent.png", full_page=True)

    page.set_viewport_size({"width": 375, "height": 812})
    page.reload()
    if page.evaluate("document.documentElement.scrollWidth > window.innerWidth"):
        raise AssertionError("/demo overflows the narrow viewport")
    page.screenshot(path=evidence_root / "demo-narrow.png", full_page=True)
    page.go_back()
    if not page.url.endswith("/catalog"):
        raise AssertionError("catalog/demo browser back state was not preserved")
    page.reload()
    if "10 capability domains" not in page.locator("main").inner_text().lower():
        raise AssertionError("catalog reload did not preserve read-only content")
    transcript.append(
        {
            "step": "catalog-demo-read-only",
            "catalog_diagrams": 7,
            "demo_stages": 9,
            "demo_automation": "30/30 = 100%",
            "demo_stage_manifests": 9,
            "narrow_viewport": 375,
            "zoom_equivalent_viewport": 640,
            "controls": 0,
        }
    )


def _unavailable_demo_surface(
    page: Page,
    base_url: str,
    evidence_root: Path,
    transcript: list[dict[str, Any]],
) -> None:
    page.goto(f"{base_url}/demo")
    demo_text = page.locator("main").inner_text().lower()
    if "artifact unavailable" not in demo_text:
        raise AssertionError("/demo did not render unavailable artifact state")
    if "current execution claims cannot be confirmed here" not in demo_text:
        raise AssertionError("/demo did not fail closed on unavailable provenance")
    if "demo/evidence/current/ai-ready-customer-product.csv" not in demo_text:
        raise AssertionError("/demo omitted the unavailable generated product")
    if page.locator("button, form, input, select, textarea").count():
        raise AssertionError("/demo unavailable state unexpectedly exposes a control action")
    page.screenshot(path=evidence_root / "demo-unavailable.png", full_page=True)
    transcript.append(
        {
            "step": "demo-unavailable-read-only",
            "generated_product": "unavailable",
            "controls": 0,
        }
    )


def _corrupt_demo_surface(
    page: Page,
    server: RunningServer,
    engagement_id: str,
    expected_snapshot: dict[str, str],
    evidence_root: Path,
    transcript: list[dict[str, Any]],
    console_errors: list[str],
) -> None:
    prior_console_error_count = len(console_errors)
    response = page.goto(f"{server.base_url}/demo")
    if response is None or response.status != 422:
        raise AssertionError("corrupt demo content did not fail validation")
    if "corrupt stage manifest" not in page.locator("main").inner_text().lower():
        raise AssertionError("corrupt demo validation failure was not explicit")
    expected_console_errors = console_errors[prior_console_error_count:]
    if expected_console_errors != [
        "Failed to load resource: the server responded with a status of 422 (Unprocessable Entity)"
    ]:
        raise AssertionError(
            f"corrupt demo emitted unexpected console errors: {expected_console_errors}"
        )
    del console_errors[prior_console_error_count:]
    page.goto(f"{server.base_url}/engagements/{engagement_id}/review")
    page.get_by_text("Active revision", exact=False).wait_for()
    recovered_snapshot = LocalEngagementStore(server.engagement_root).snapshot(
        engagement_id
    )
    if recovered_snapshot != expected_snapshot:
        raise AssertionError("corrupt demo validation changed recoverable assessment source")
    page.screenshot(path=evidence_root / "demo-corrupt.png", full_page=True)
    transcript.append(
        {
            "step": "demo-corrupt-fail-closed",
            "http_status": 422,
            "assessment_source_recoverable": True,
        }
    )


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_browser_journey(
    evidence_root: Path,
    *,
    repository_root: Path,
) -> dict[str, Any]:
    """Run the complete journey once, retain evidence, and tear down all processes."""
    evidence_root.mkdir(parents=True, exist_ok=True)
    work_root = evidence_root / "work"
    shutil.rmtree(work_root, ignore_errors=True)
    work_root.mkdir()
    source_server = _start_server(
        work_root / "source",
        repository_root=repository_root,
    )
    destination_server: RunningServer | None = None
    unavailable_server: RunningServer | None = None
    corrupt_server: RunningServer | None = None
    transcript: list[dict[str, Any]] = []
    remote_requests: list[str] = []
    console_errors: list[str] = []
    page_errors: list[str] = []
    request_failures: list[dict[str, str]] = []
    server_logs: list[str] = []
    framework = load_framework("1.0.0")
    engagement_id = "synthetic-architect-001"
    browser_version = ""
    try:
        with sync_playwright() as playwright:
            browser = _launch_browser(playwright)
            browser_version = browser.version
            try:
                js_context = browser.new_context(viewport={"width": 375, "height": 812})
                _guard_context(
                    js_context,
                    remote_requests=remote_requests,
                    console_errors=console_errors,
                    page_errors=page_errors,
                    request_failures=request_failures,
                )
                js_page = js_context.new_page()
                _create_engagement(js_page, source_server.base_url, engagement_id)
                _exercise_autosave(js_page, framework, transcript)
                _exercise_accessibility(
                    js_page,
                    source_server.base_url,
                    engagement_id,
                    transcript,
                    console_errors,
                )
                js_page.screenshot(
                    path=evidence_root / "autosave-narrow.png",
                    full_page=True,
                )
                js_context.close()

                plain_context = browser.new_context(
                    java_script_enabled=False,
                    viewport={"width": 1280, "height": 900},
                    accept_downloads=True,
                )
                _guard_context(
                    plain_context,
                    remote_requests=remote_requests,
                    console_errors=console_errors,
                    page_errors=page_errors,
                    request_failures=request_failures,
                    allowed_file_urls={
                        (evidence_root / "report.html").resolve().as_uri()
                    },
                )
                page = plain_context.new_page()
                _complete_plain_form_assessment(
                    page,
                    source_server.base_url,
                    engagement_id,
                    framework,
                    evidence_root,
                    transcript,
                )
                html_path, report_path, archive_path = _review_select_report_export(
                    page,
                    source_server.base_url,
                    engagement_id,
                    framework,
                    evidence_root,
                    transcript,
                )
                response = page.goto(f"{source_server.base_url}/engagements")
                if response is None or "default-src 'self'" not in (
                    response.headers.get("content-security-policy") or ""
                ):
                    raise AssertionError("live response is missing the restrictive CSP")
                _read_only_surfaces(
                    page,
                    source_server.base_url,
                    evidence_root,
                    transcript,
                )
                unavailable_repository = work_root / "unavailable-repository"
                unavailable_repository.mkdir()
                unavailable_server = _start_server(
                    work_root / "unavailable",
                    repository_root=unavailable_repository,
                )
                _unavailable_demo_surface(
                    page,
                    unavailable_server.base_url,
                    evidence_root,
                    transcript,
                )

                source_snapshot = LocalEngagementStore(
                    source_server.engagement_root
                ).snapshot(engagement_id)
                corrupt_repository = work_root / "corrupt-repository"
                corrupt_manifest = (
                    corrupt_repository
                    / "demo"
                    / "manifests"
                    / "stages"
                    / "ingestion.yaml"
                )
                corrupt_manifest.parent.mkdir(parents=True)
                corrupt_manifest.write_text(
                    "schema_version: 1.0.0\nstage_id: wrong\n",
                    encoding="utf-8",
                )
                corrupt_server_root = work_root / "corrupt"
                shutil.copytree(
                    source_server.engagement_root,
                    corrupt_server_root / "engagements",
                )
                corrupt_server = _start_server(
                    corrupt_server_root,
                    repository_root=corrupt_repository,
                )
                _corrupt_demo_surface(
                    page,
                    corrupt_server,
                    engagement_id,
                    source_snapshot,
                    evidence_root,
                    transcript,
                    console_errors,
                )

                destination_server = _start_server(
                    work_root / "destination",
                    repository_root=repository_root,
                )
                _import_reopen_compare(
                    page,
                    destination_server,
                    source_server,
                    engagement_id,
                    archive_path,
                    report_path,
                    evidence_root,
                    transcript,
                )
                page.screenshot(path=evidence_root / "imported-review.png", full_page=True)
                plain_context.close()
            finally:
                browser.close()
    finally:
        server_logs.extend(
            _stop_servers(
                (
                    destination_server,
                    corrupt_server,
                    unavailable_server,
                    source_server,
                )
            )
        )

    if remote_requests:
        raise AssertionError(f"browser attempted remote requests: {remote_requests}")
    if console_errors:
        raise AssertionError(f"browser console errors: {console_errors}")
    if page_errors:
        raise AssertionError(f"browser page errors: {page_errors}")
    expected_request_failures, unexpected_request_failures = (
        _partition_request_failures(request_failures)
    )
    if unexpected_request_failures:
        raise AssertionError(
            f"unexpected browser request failures: {unexpected_request_failures}"
        )
    server_logs_clean = all(
        "Traceback" not in log and "ERROR:" not in log for log in server_logs
    )
    if not server_logs_clean:
        raise AssertionError("loopback server emitted an error or traceback")
    html_path = evidence_root / "report.html"
    report_path = evidence_root / "report.json"
    archive_path = evidence_root / "engagement.zip"
    imported_report = evidence_root / "imported-report.json"
    digests = {
        path.name: _digest(path)
        for path in (html_path, report_path, archive_path, imported_report)
    }
    result = {
        "status": "pass",
        "browser": f"Chromium via Playwright {browser_version}",
        "engagement_id": engagement_id,
        "answers": 30,
        "gate_traces": 7,
        "report_sections": 12,
        "remote_requests": remote_requests,
        "console_errors": console_errors,
        "page_errors": page_errors,
        "expected_request_failures": expected_request_failures,
        "unexpected_request_failures": unexpected_request_failures,
        "digests": digests,
        "transcript": transcript,
        "server_logs_clean": server_logs_clean,
        "clean_teardown": True,
    }
    (evidence_root / "transcript.json").write_bytes(canonical_json(transcript))
    (evidence_root / "digests.json").write_bytes(canonical_json(digests))
    (evidence_root / "result.json").write_bytes(canonical_json(result))
    return result


def _launch_browser(playwright: Playwright) -> Browser:
    browser_root = Path(os.environ["PLAYWRIGHT_BROWSERS_PATH"])
    candidates = sorted(
        browser_root.glob(
            "chromium-*/chrome-mac-arm64/"
            "Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing"
        )
    )
    if len(candidates) != 1:
        raise RuntimeError(
            "the repository-local pinned macOS arm64 Chromium executable is unavailable"
        )
    return playwright.chromium.launch(
        headless=True,
        executable_path=str(candidates[0]),
    )
