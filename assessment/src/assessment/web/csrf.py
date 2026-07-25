"""Signed session-bound CSRF tokens backed by an ephemeral process secret."""

from __future__ import annotations

import secrets

from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer
from starlette.requests import Request


class CsrfProtection:
    def __init__(self, secret: bytes, *, max_age_seconds: int = 14_400) -> None:
        self._serializer = URLSafeTimedSerializer(secret, salt="assessment-csrf-v1")
        self._max_age_seconds = max_age_seconds

    @staticmethod
    def _session_id(request: Request) -> str:
        session_id = request.session.get("sid")
        if not isinstance(session_id, str):
            session_id = secrets.token_urlsafe(24)
            request.session["sid"] = session_id
        return session_id

    def issue(self, request: Request) -> str:
        return str(self._serializer.dumps(self._session_id(request)))

    def verify(self, request: Request, token: str) -> bool:
        try:
            signed_session = self._serializer.loads(
                token,
                max_age=self._max_age_seconds,
            )
        except (BadSignature, SignatureExpired):
            return False
        session_id = request.session.get("sid")
        return (
            isinstance(session_id, str)
            and isinstance(signed_session, str)
            and secrets.compare_digest(session_id, signed_session)
        )
