"""Render engagement-pinned standalone HTML with no runtime fetches."""

from __future__ import annotations

import re
from html.parser import HTMLParser
from typing import Any

from jinja2 import Environment, StrictUndefined, select_autoescape
from markupsafe import Markup

from assessment.catalog.loader import load_catalog, read_catalog_asset
from assessment.domain.errors import ContentValidationError
from assessment.frameworks import load_report_asset

REMOTE_CSS = re.compile(r"(?i)(?:@font-face|@import|url\s*\()")
ACTIVE_TAGS = {
    "script",
    "form",
    "iframe",
    "object",
    "embed",
    "link",
    "base",
    "audio",
    "video",
}


class _SafetyParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.unsafe: str | None = None

    def handle_starttag(
        self,
        tag: str,
        attrs: list[tuple[str, str | None]],
    ) -> None:
        if tag.lower() in ACTIVE_TAGS:
            self.unsafe = f"active or remote-capable element present: {tag}"
            return
        for name, _ in attrs:
            lowered = name.lower()
            if lowered in {"src", "href"} or lowered.startswith("on"):
                self.unsafe = f"linked or executable attribute present: {name}"
                return


def render_report(report_document: dict[str, Any]) -> bytes:
    environment = Environment(
        undefined=StrictUndefined,
        autoescape=select_autoescape(("html", "xml"), default=True),
        keep_trailing_newline=True,
    )
    template = environment.from_string(load_report_asset("report.html.j2"))
    css = load_report_asset("report.css")
    if REMOTE_CSS.search(css):
        raise ContentValidationError("report.css: remote resource or font present")
    catalog = load_catalog()
    diagram_svgs = {
        # The catalog loader verifies the manifest digest and rejects active,
        # linked, remote, or inaccessible SVG content before it reaches Markup.
        diagram.id: Markup(  # noqa: S704
            read_catalog_asset(diagram.svg_path).decode("utf-8")
        )
        for diagram in catalog.diagrams
    }
    html = template.render(
        report=report_document,
        sections={section["id"]: section["content"] for section in report_document["sections"]},
        css=css,
        diagram_svgs=diagram_svgs,
    )
    parser = _SafetyParser()
    parser.feed(html)
    if parser.unsafe is not None:
        raise ContentValidationError(f"report.html: {parser.unsafe}")
    return html.encode("utf-8")
