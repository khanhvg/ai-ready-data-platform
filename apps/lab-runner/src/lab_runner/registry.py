"""Closed semantic operation registry with no caller-controlled descriptors."""
from __future__ import annotations
from dataclasses import dataclass
from .contract import EXPECTED_COMMANDS


class RegistryError(ValueError):
    pass


@dataclass(frozen=True, slots=True)
class Operation:
    operation_id: str
    internal_argv: tuple[str, ...]
    timeout_seconds: int = 110


_REGISTRY = {name: Operation(name, ("python3.12", "-I", "-m", "lab_runner.container_supervisor", name)) for name in EXPECTED_COMMANDS}


def operation_ids() -> tuple[str, ...]:
    return tuple(_REGISTRY)


def resolve(operation_id: object) -> Operation:
    if type(operation_id) is not str or operation_id not in _REGISTRY:
        raise RegistryError("RUNNER_COMMAND_UNKNOWN")
    return _REGISTRY[operation_id]


def validate_request(value: object) -> dict[str, object]:
    if type(value) is not dict:
        raise RegistryError("RUNNER_REQUEST_INVALID")
    allowed = {"operationId", "idempotencyKey", "workspaceRevision"}
    if set(value) != allowed:
        raise RegistryError("RUNNER_REQUEST_FIELD_INVALID")
    op = resolve(value["operationId"])
    key = value["idempotencyKey"]
    revision = value["workspaceRevision"]
    if type(key) is not str or not (16 <= len(key) <= 128) or not key.replace("-", "").replace("_", "").isalnum():
        raise RegistryError("RUNNER_IDEMPOTENCY_KEY_INVALID")
    if type(revision) is not int or revision < 0:
        raise RegistryError("RUNNER_WORKSPACE_REVISION_INVALID")
    return {"operationId": op.operation_id, "idempotencyKey": key, "workspaceRevision": revision}
