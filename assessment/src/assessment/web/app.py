"""Dependency-injected FastAPI application factory."""

from __future__ import annotations

import secrets
from pathlib import Path
from urllib.parse import urlsplit

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, Response
from fastapi.staticfiles import StaticFiles
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from starlette.types import ASGIApp

from assessment.web.config import WebConfig
from assessment.web.csrf import CsrfProtection
from assessment.web.dependencies import WebServices
from assessment.web.routes import router

SECURITY_HEADERS = {
    "Content-Security-Policy": (
        "default-src 'self'; base-uri 'none'; frame-ancestors 'none'; "
        "form-action 'self'; object-src 'none'; img-src 'self' data:; "
        "style-src 'self'; script-src 'self'"
    ),
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "Referrer-Policy": "no-referrer",
    "Permissions-Policy": "camera=(), microphone=(), geolocation=()",
    "Cross-Origin-Opener-Policy": "same-origin",
    "Cross-Origin-Resource-Policy": "same-origin",
}


class RequestBoundaryMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app: ASGIApp,
        *,
        allowed_origins: frozenset[str],
        max_request_bytes: int,
    ) -> None:
        super().__init__(app)
        self.allowed_origins = allowed_origins
        self.max_request_bytes = max_request_bytes

    async def dispatch(
        self,
        request: Request,
        call_next: RequestResponseEndpoint,
    ) -> Response:
        response: Response | None = None
        if request.method not in {"GET", "HEAD", "OPTIONS"}:
            content_length = request.headers.get("content-length")
            if content_length is None:
                response = JSONResponse(
                    {
                        "error": {
                            "code": "length_required",
                            "message": "A bounded Content-Length is required.",
                        }
                    },
                    status_code=411,
                )
            else:
                try:
                    request_bytes = int(content_length)
                except ValueError:
                    request_bytes = -1
                if request_bytes < 0:
                    response = JSONResponse(
                        {
                            "error": {
                                "code": "invalid_content_length",
                                "message": "Content-Length is invalid.",
                            }
                        },
                        status_code=400,
                    )
                elif request_bytes > self.max_request_bytes:
                    response = JSONResponse(
                        {
                            "error": {
                                "code": "request_too_large",
                                "message": "Request exceeds the configured local limit.",
                            }
                        },
                        status_code=413,
                    )
            origin = request.headers.get("origin")
            if origin is None:
                referer = request.headers.get("referer")
                if referer:
                    parsed = urlsplit(referer)
                    origin = f"{parsed.scheme}://{parsed.netloc}"
            opaque_same_origin_navigation = (
                origin == "null"
                and request.headers.get("sec-fetch-site") == "same-origin"
                and request.headers.get("sec-fetch-mode") == "navigate"
            )
            if (
                response is None
                and origin not in self.allowed_origins
                and not opaque_same_origin_navigation
            ):
                response = JSONResponse(
                    {"error": {"code": "invalid_origin", "message": "Origin is not allowed."}},
                    status_code=403,
                )
        if response is None:
            response = await call_next(request)
        for name, value in SECURITY_HEADERS.items():
            response.headers[name] = value
        response.headers["Cache-Control"] = "no-store"
        return response


def create_app(
    *,
    config: WebConfig,
    services: WebServices | None = None,
    session_secret: bytes | None = None,
) -> FastAPI:
    """Build one local application from explicit runtime dependencies."""
    secret = session_secret or secrets.token_bytes(32)
    app = FastAPI(
        title="AI-ready assessment",
        docs_url=None,
        redoc_url=None,
        openapi_url=None,
    )
    app.state.config = config
    app.state.services = services or WebServices(config)
    app.state.csrf = CsrfProtection(secret)
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=config.allowed_hosts)
    app.add_middleware(
        SessionMiddleware,
        secret_key=secret.hex(),
        session_cookie="assessment_session",
        same_site="strict",
        https_only=False,
        max_age=14_400,
    )
    app.add_middleware(
        RequestBoundaryMiddleware,
        allowed_origins=config.allowed_origins,
        max_request_bytes=config.max_upload_bytes + 64 * 1024,
    )
    static_root = Path(__file__).with_name("static")
    app.mount("/static", StaticFiles(directory=static_root), name="static")
    app.include_router(router)
    return app
