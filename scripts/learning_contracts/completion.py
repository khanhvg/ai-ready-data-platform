"""One-authority completion and orphan reconciliation decisions."""
from __future__ import annotations

from .canonical import ContractError

AUTHORITY = "learning-progress-authority-v1"


def commit(authority_id: str, operation_committed: bool, evidence_hash_valid: bool, expected_revision: bool) -> str:
    if authority_id != AUTHORITY:
        raise ContractError("COMPLETION_AUTHORITY_REQUIRED")
    if not operation_committed or not evidence_hash_valid:
        raise ContractError("COMPLETION_DUAL_TRUTH")
    if not expected_revision:
        raise ContractError("PROGRESS_VERSION_CONFLICT")
    return "completed"


def reconcile(attached: bool, hashes_valid: bool, identity_conflict: bool) -> str:
    if attached: return "already-attached"
    if hashes_valid and not identity_conflict: return "attachable-orphan"
    return "invalid-or-conflicting-orphan"
