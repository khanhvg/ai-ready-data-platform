"""Single CAS completion authority with canonical idempotency."""

from __future__ import annotations

import copy
import hashlib
from typing import Any

from .canonical import canonical_bytes
from .schema import LearningContractError


def validate_completion_contract(value: dict[str, Any]) -> None:
    """Validate the one-authority machine document and its semantic ordering."""
    from .schema import validate_document
    validate_document(value, family="completion-reconciliation")
    if value.get("authorityId") != "learning-progress-authority-v1":
        raise LearningContractError("COMPLETION_AUTHORITY_INVALID")
    order = value.get("commitOrder", [])
    if [item.get("id") for item in order if isinstance(item, dict)] != ["result", "evidence-fsync-rename", "progress-cas", "acknowledgment"] or [item.get("order") for item in order] != [1, 2, 3, 4]:
        raise LearningContractError("COMPLETION_ORDER_INVALID")
    if {item.get("id") for item in value.get("reconciliation", []) if isinstance(item, dict)} != {"already-attached", "attachable-orphan", "invalid-or-conflicting-orphan"}:
        raise LearningContractError("RECONCILIATION_INVALID")


def reconcile(progress: dict[str, Any], orphan: dict[str, Any]) -> str:
    """Return a deterministic disposition; only `complete` may attach an orphan."""
    evidence_id = orphan.get("evidenceId")
    completion_value = progress.get("completion")
    if isinstance(completion_value, dict) and completion_value.get("evidenceId") == evidence_id:
        return "already-attached"
    if orphan.get("operationCommitted") is True and orphan.get("evidenceVerified") is True and orphan.get("expectedRevision") == progress.get("revision"):
        complete(progress, {"expectedRevision": progress["revision"], "idempotencyKey": orphan.get("idempotencyKey"), "evidenceId": evidence_id})
        return "attachable-orphan"
    return "invalid-or-conflicting-orphan"


def validate_completion_semantics(value: dict[str, Any]) -> None:
    """Reject alternate completion authorities and unsafe orphan attachment."""
    source = value.get("completionSource")
    if source == "browser":
        raise LearningContractError("COMPLETION_AUTHORITY_REQUIRED")
    if source in {"evidence-presence", "operation-result"}:
        raise LearningContractError("COMPLETION_DUAL_TRUTH")
    if value.get("orphan") and value.get("attemptsCompletion"):
        raise LearningContractError("RECONCILIATION_ORPHAN_CANNOT_COMPLETE")
    if value.get("orphan") and value.get("declaredSha256") != value.get("actualSha256"):
        raise LearningContractError("RECONCILIATION_HASH_MISMATCH")


def complete(state: dict[str, Any], request: dict[str, Any]) -> dict[str, Any]:
    key = request.get("idempotencyKey")
    if not isinstance(key, str) or not key:
        raise LearningContractError("IDEMPOTENCY_KEY_REQUIRED")
    request_hash = hashlib.sha256(canonical_bytes(request)).hexdigest()
    idempotency = state.get("idempotency", {})
    if not isinstance(idempotency, dict):
        raise LearningContractError("IDEMPOTENCY_STATE_INVALID")
    retained = idempotency.get(key)
    if retained is not None:
        if retained["requestSha256"] != request_hash:
            raise LearningContractError("IDEMPOTENCY_KEY_REUSE")
        return copy.deepcopy(retained["result"])
    if request.get("expectedRevision") != state.get("revision"):
        raise LearningContractError("PROGRESS_VERSION_CONFLICT")
    if state.get("state") != "verified" or not request.get("evidenceId"):
        raise LearningContractError("COMPLETION_PRECONDITION_FAILED")
    result = {
        "state": "completed",
        "revision": state["revision"] + 1,
        "evidenceId": request["evidenceId"],
    }
    state["state"] = "completed"
    state["revision"] = result["revision"]
    state.setdefault("effects", []).append({"kind": "completion", "evidenceId": request["evidenceId"]})
    state.setdefault("idempotency", {})[key] = {"requestSha256": request_hash, "result": copy.deepcopy(result)}
    return result
