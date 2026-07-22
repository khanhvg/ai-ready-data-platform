"""Public trace checker entrypoint; semantic rules are added after RED."""

from __future__ import annotations

from typing import Any

from .content_io import CheckResult, NormalizedRequest, content_sha256

ENTRYPOINT_ID = "I11-EP-TRACE"


def run(request: NormalizedRequest) -> CheckResult:
    projection: dict[str, Any] = {"trace": request.payload, "sourceClass": request.source.split(":", 1)[0]}
    return CheckResult(ENTRYPOINT_ID, True, details={"projectionSha256": content_sha256(projection)})
