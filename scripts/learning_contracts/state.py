"""Pure legal-transition, CAS and idempotency decisions."""
from __future__ import annotations

import hashlib
from dataclasses import dataclass

from .canonical import ContractError, dumps

LEGAL = {"draft": {"ready"}, "ready": {"running"}, "running": {"verified"}, "verified": {"evidenced"}, "evidenced": {"completed"}, "completed": set()}


def transition(current: str, target: str, revision: int, expected_revision: int) -> tuple[str, int]:
    if revision != expected_revision:
        raise ContractError("PROGRESS_VERSION_CONFLICT")
    if target not in LEGAL.get(current, set()):
        raise ContractError("STATE_TRANSITION_FORBIDDEN")
    return target, revision + 1


def request_hash(request: object) -> str:
    return hashlib.sha256(dumps(request)).hexdigest()


@dataclass(frozen=True)
class IdempotencyRecord:
    request_sha256: str
    response_sha256: str
    resulting_revision: int
    effect_id: str


def replay(record: IdempotencyRecord, request: object) -> IdempotencyRecord:
    if record.request_sha256 != request_hash(request):
        raise ContractError("IDEMPOTENCY_KEY_REUSE")
    return record
