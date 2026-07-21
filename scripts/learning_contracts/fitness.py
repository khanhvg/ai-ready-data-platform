"""Activation-bound fitness-result-v2 builder."""
from __future__ import annotations

import hashlib
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from .evidence import payload_sha256
from .schema import ROOT, load_json, sha256, validate

BASE_COMMAND_SHA = "a94ac86bda0b70643edef9f144a59d8753d91f963b83d22cd510adbc31970e80"


def activation(command: str) -> dict[str, object]:
    document = load_json("learning/contracts/command-owner-activation-i5-03-v1.json")
    validate(document, "learning/contracts/command-owner-activation-v1.schema.json")
    if sha256(ROOT / document["baseRegistryPath"]) != BASE_COMMAND_SHA or document["baseRegistrySha256"] != BASE_COMMAND_SHA:
        raise ValueError("COMMAND_ACTIVATION_BASE_MISMATCH")
    return next(row for row in document["commands"] if row["command"] == command)


def build(command: str, status: str, started: datetime, locator: str | None = None, failure: str | None = None) -> dict[str, object]:
    row = activation(command)
    now = datetime.now(timezone.utc)
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    tree = subprocess.check_output(["git", "rev-parse", "HEAD^{tree}"], cwd=ROOT, text=True).strip()
    result: dict[str, object] = {
        "schemaVersion": "fitness-result-v2", "commandId": command, "owner": "I5-03",
        "requested": {"subjectType": "contract-release", "subjectId": "stage-a", "parameters": []},
        "status": status, "failureCode": failure, "remediation": None,
        "inputSha": "c23106ad89d45370b06c3329f7d8963b2c62a064", "testedTreeSha": tree,
        "dependencyMergeShas": ["24be3b34c6b0fcdbd07c5800dcab349054e34713"],
        "contractHashes": ["learning-contract-set-v1"], "fixtureHashes": ["promotion-trust-v1"],
        "schemaHashes": ["fitness-result-v2"], "toolchain": ["cpython=3.12.3", "jsonschema=4.26.0", "rfc8785=0.1.4", "PyYAML=6.0.3"],
        "lockSha256": "f41c727b39f99106f95b7937b2811e8d27db89d1d5106e9f1d9effd4403143d2",
        "invocation": {"publicArgv": ["make", command], "canonicalChildArgv": ["python3.12", "-m", "scripts.learning_contracts.check", command], "actualChildArgvSha256": None, "cwdRole": "repository-root"},
        "startedAt": started.isoformat(), "finishedAt": now.isoformat(), "durationMs": int((now-started).total_seconds()*1000),
        "rawLocator": locator, "projectionLocator": locator, "envelopeLocator": locator,
        "projectionSha256": "0"*64, "artifacts": [], "redactionClass": "public-safe", "retentionClass": "stage-a-contract-evidence",
        "rollback": "marker-manifest-inode-nonce-bound", "canonicalization": "rfc8785-jcs-v1", "payloadSha256": ""
    }
    if row["evidenceSchema"] != "fitness-result-v2": raise ValueError("FITNESS_RESULT_OWNER_VERSION_MISMATCH")
    result["payloadSha256"] = payload_sha256(result)
    return result
