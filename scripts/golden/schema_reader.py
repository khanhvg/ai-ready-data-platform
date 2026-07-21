#!/usr/bin/env python3
"""Registry-based JSON Schema reader and lossless private migration vector."""

from __future__ import annotations

import hashlib
import json
import pathlib
from typing import Any

import jsonschema
import rfc8785


ROOT = pathlib.Path(__file__).resolve().parents[2]
REGISTRY = ROOT / "learning/contracts/schema-version-registry.json"


class SchemaError(ValueError): pass


def registry() -> dict[str, Any]:
    return json.loads(REGISTRY.read_text(encoding="utf-8"))


def validate(family: str, value: Any) -> None:
    entries = [item for item in registry()["families"] if item["family"] == family]
    if len(entries) != 1: raise SchemaError("SCHEMA_FAMILY_UNREGISTERED")
    entry = entries[0]
    version = value.get("schemaVersion") if isinstance(value, dict) else None
    readable = {item["version"]: item for item in entry["readableVersions"]}
    if version not in readable: raise SchemaError("SCHEMA_VERSION_UNREADABLE")
    registered = readable[version]
    path = ROOT / registered["schemaPath"]
    if hashlib.sha256(path.read_bytes()).hexdigest() != registered["schemaSha256"]:
        raise SchemaError("SCHEMA_HASH_MISMATCH")
    jsonschema.Draft202012Validator(json.loads(path.read_text())).validate(value)
    if family == "evidence-envelope": verify_envelope(value)


def verify_envelope(value: dict[str, Any]) -> None:
    if any(key in value for key in ("attestationCommitSha","mergeOrTagSha","selfSha256")):
        raise SchemaError("ENVELOPE_RECURSIVE_IDENTITY")
    payload=value.get("payload"); integrity=value.get("integrity",{})
    if not isinstance(payload,dict) or hashlib.sha256(rfc8785.dumps(payload)).hexdigest()!=integrity.get("payloadSha256"):
        raise SchemaError("ENVELOPE_PAYLOAD_HASH_MISMATCH")


def private_migrate(value: dict[str, Any], target: str) -> dict[str, Any]:
    current = value.get("schemaVersion")
    if (current, target) not in {("private-v0", "private-v1"), ("private-v1", "private-v0")}:
        raise SchemaError("MIGRATION_EDGE_UNREGISTERED")
    migrated = dict(value); migrated["schemaVersion"] = target
    return migrated
