"""Validation for authored Markdown accepted by v1."""

from __future__ import annotations

import re

from assessment.domain.errors import ContentValidationError

RAW_HTML = re.compile(r"(?:<\s*/?\s*[A-Za-z][^>]*>|<!--|<!DOCTYPE|<\?)", re.IGNORECASE)
OBJECT_CONSTRUCTOR = re.compile(r"!!python/|!<tag:yaml\.org,2002:python")


def validate_markdown(text: str, *, context: str = "Markdown") -> None:
    if "\x00" in text:
        raise ContentValidationError(f"{context}: NUL is not allowed")
    if RAW_HTML.search(text):
        raise ContentValidationError(f"{context}: raw HTML is not allowed")
    if OBJECT_CONSTRUCTOR.search(text):
        raise ContentValidationError(f"{context}: object constructors are not allowed")
