"""Single CAS completion authority with canonical idempotency."""

from __future__ import annotations

import copy
import hashlib
from typing import Any

from .canonical import canonical_bytes
from .schema import LearningContractError


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
