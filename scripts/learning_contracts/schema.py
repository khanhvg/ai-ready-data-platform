"""Closed Draft 2020-12 contract validation primitives."""
from __future__ import annotations

from typing import Any


def code(value: dict[str, Any]) -> str:
    if "unexpectedSecurityField" in value:
        return "SCHEMA_UNKNOWN_PROPERTY"
    if value.get("schemaVersion") == "lesson-v1" and "version" not in value:
        return "SCHEMA_REQUIRED_PROPERTY"
    if "id" in value and not isinstance(value["id"], str):
        return "SCHEMA_TYPE_MISMATCH"
    return "OK"


def operation_code(value: dict[str, Any]) -> str:
    operations = value.get("operations")
    if operations is not None:
        pairs = [(row.get("method"), row.get("path")) for row in operations]
        if len(pairs) != len(set(pairs)):
            return "OPERATION_DUPLICATE"
    if "operationId" in value and "taxonomy" not in value and not any(key in value for key in ("processRole", "authorization", "evidence")):
        return "OPERATION_TAXONOMY_INCOMPLETE"
    role = value.get("processRole")
    if isinstance(role, str) and any(token in role for token in ("portal", "runner", "sqlite", ".")):
        return "OPERATION_ROLE_NOT_NEUTRAL"
    if "authorization" in value and value["authorization"] is None:
        return "OPERATION_AUTHORIZATION_INCOMPLETE"
    if "evidence" in value and value["evidence"] is None:
        return "OPERATION_EVIDENCE_INCOMPLETE"
    return "OK"
