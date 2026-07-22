#!/usr/bin/env python3
"""Public Stage A command scaffold."""

from __future__ import annotations

import argparse
import copy
import datetime
import hashlib
import json
import os
import pathlib
import platform
import re
import resource
import subprocess
import sys
import tempfile
import time
from collections.abc import Sequence
from typing import Any

import jsonschema

from .canonical import canonical_bytes, parse_json
from .schema import LearningContractError, read_document, validate_document
from .references import resolve_reference
from .vite_binding import (
    validate_shipped_vite_binding,
    validate_vite_binding_document,
    validate_vite_binding_path,
)


ROOT = pathlib.Path(__file__).resolve().parents[2]
FIXTURE_ROOT = ROOT / "tests/fixtures/learning/contracts"
BASE_REGISTRY_SHA256 = "8e18588f63b5d99c0b60a229758575e8badf0f055bfcb4f89908f9fa2684a57e"
PROMOTION_FIXTURE_SHA256 = "0a1dcd4023648f52009bfd4dc5d529c00ce66f42cd0e725732b972b0b78df341"
FIXTURE_METADATA_SCHEMA = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "object",
    "additionalProperties": False,
    "required": ["family", "case"],
    "properties": {
        "family": {"enum": ["activation", "completion", "evidence", "guidance", "migration", "openapi", "operation", "promotion", "reference", "schema", "state"]},
        "case": {"type": "string", "pattern": "^[a-z0-9]+(?:-[a-z0-9]+)*$", "maxLength": 80},
    },
}


def validate_public_value(name: str, value: str) -> str:
    if not isinstance(value, str) or not value or len(value) > 256 or "\x00" in value:
        raise LearningContractError("PUBLIC_ARGUMENT_INVALID")
    if name == "LESSON":
        if re.fullmatch(r"[a-z0-9][a-z0-9-]{0,63}", value) is None:
            raise LearningContractError("PUBLIC_ARGUMENT_INVALID")
        return value
    if name == "EVIDENCE":
        candidate = pathlib.PurePosixPath(value)
        secret = re.search(r"(?:AKIA[0-9A-Z]{16}|[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,})", value)
        if (
            candidate.is_absolute()
            or any(part in {"", ".", ".."} for part in candidate.parts)
            or "\\" in value
            or secret
            or re.search(r"[;&|`$<>(){}!\n\r]", value)
        ):
            raise LearningContractError("PUBLIC_ARGUMENT_INVALID")
        return value
    raise LearningContractError("PUBLIC_ARGUMENT_INVALID")


_CASE_INPUTS: dict[tuple[str, str], dict[str, Any]] = {
    ("completion", "evidence-presence-completes"): {"completionSource": "evidence-presence", "completed": True},
    ("completion", "forged-browser-completion"): {"completionSource": "browser", "completed": True},
    ("completion", "operation-result-direct-write"): {"completionSource": "operation-result", "completed": True},
    ("completion", "orphan-hash-mismatch"): {"orphan": True, "declaredSha256": "a" * 64, "actualSha256": "b" * 64},
    ("completion", "orphan-self-completion"): {"orphan": True, "attemptsCompletion": True},
    ("evidence", "artifact-hash"): {"artifact": {"sha256": "0" * 64}, "actualSha256": "f" * 64},
    ("evidence", "evidence-payload"): {"payload": {"id": "changed"}, "payloadSha256": "0" * 64},
    ("evidence", "locator-traversal"): {"locator": "../secret"},
    ("evidence", "missing-dependency-sha"): {"dependencyMergeShas": []},
    ("evidence", "recursive-identity"): {"testedTreeSha": "self-containing-identity"},
    ("evidence", "replayed-run-identity"): {"indexedPayloadSha256": "a" * 64, "payloadSha256": "b" * 64},
    ("evidence", "stale-verifier-hash"): {"verifierSha256": "0" * 64, "actualVerifierSha256": "f" * 64},
    ("evidence", "injection-field"): {"rawSql": "select * from secrets"},
    ("guidance", "hint-completes"): {"completionMutation": True},
    ("guidance", "mutating-probe"): {"command": "touch file"},
    ("guidance", "optional-unavailable-passes"): {"required": False, "status": "unavailable", "result": "pass"},
    ("guidance", "required-unavailable-passes"): {"required": True, "status": "unavailable", "result": "pass"},
    ("guidance", "unauthorized-reveal"): {"revealed": True, "revealAuthorized": False},
    ("migration", "base-registry-hash-mismatch"): {"baseRegistry": {"sha256": "0" * 64}},
    ("migration", "cycle"): {"edges": [["v0", "v1"], ["v1", "v0"]]},
    ("migration", "family-collision"): {"ownedFamilies": ["data-contract", "lesson"], "baseFamilies": ["data-contract"]},
    ("migration", "lossy-edge"): {"lossless": False},
    ("migration", "unknown-version"): {"family": "lesson", "version": "v9"},
    ("openapi", "error-set-drift"): {"errors": ["500 INTERNAL_CONTRACT_ERROR"]},
    ("openapi", "missing-authority"): {"authority": None},
    ("openapi", "missing-idempotency"): {"idempotency": None},
    ("openapi", "missing-version-response"): {"responseHeaders": []},
    ("openapi", "orphan-asyncapi"): {"channels": [], "asyncapiArtifacts": ["contracts/asyncapi/orphan.yaml"]},
    ("openapi", "orphan-operation"): {"matrixOperationIds": ["listLessons"], "openapiOperationIds": ["listLessons", "orphan"]},
    ("openapi", "raw-sql-query"): {"requestFields": ["rawSql"]},
    ("openapi", "remote-ref"): {"$ref": "https://example.invalid/schema.json"},
    ("openapi", "request-shape-drift"): {"schema": "CreateWorkspaceRequest-v1", "required": ["schemaVersion"]},
    ("openapi", "response-shape-drift"): {"schema": "Workspace", "required": ["schemaVersion"]},
    ("operation", "duplicate-method-path"): {"operations": [{"method": "GET", "path": "/v1/a"}, {"method": "GET", "path": "/v1/a"}]},
    ("operation", "missing-authorization"): {"authorization": None},
    ("operation", "missing-evidence-rule"): {"evidence": None},
    ("operation", "missing-taxonomy"): {"operationId": "a", "method": "GET", "path": "/v1/a"},
    ("operation", "physical-module-role"): {"processRole": "portal.sqlite.writer"},
    ("promotion", "fixture-hash-drift"): {"fixtureSha256": "0" * 64},
    ("promotion", "hidden-common-grain"): {"commonGrain": "campaign"},
    ("promotion", "missing-limitation"): {"limitations": []},
    ("reference", "missing-verifier"): {"reference": "verifier:missing"},
    ("reference", "path-traversal"): {"reference": "../private.json"},
    ("reference", "prerequisite-cycle"): {"edges": [["a", "b"], ["b", "a"]]},
    ("reference", "remote-ref"): {"reference": "https://example.invalid/schema.json"},
    ("reference", "schema-hash-mismatch"): {"reference": "learning/contracts/lesson-v1.schema.json", "sha256": "0" * 64},
    ("state", "duplicate-effect"): {"effectCount": 2},
    ("state", "idempotency-payload-conflict"): {"storedRequestSha256": "a" * 64, "requestSha256": "b" * 64},
    ("state", "illegal-transition"): {"from": "not_started", "to": "completed"},
    ("state", "stale-version"): {"expectedRevision": 4, "actualRevision": 5},
}


def validate_invalid_fixture(path: pathlib.Path, target: str) -> None:
    try:
        value = read_document(path)
    except LearningContractError as exc:
        if target == "openapi" and exc.code == "YAML_DUPLICATE_NAME":
            raise LearningContractError("OPENAPI_YAML_DUPLICATE_KEY") from exc
        raise
    if isinstance(value, dict) and any(
        key in value for key in ("expected", "expectedCode", "actual", "actualCode")
    ):
        # Outcomes belong only to the independently maintained corpus index.
        # Fixture bytes may describe an input/case, but cannot select the result
        # that the real validator or operation is expected to produce.
        raise LearningContractError("FIXTURE_METADATA_INVALID")
    if target == "canonical":
        if "encodedHex" in value:
            parse_json(bytes.fromhex(value["encodedHex"]))
        elif "encodedJson" in value:
            parse_json(value["encodedJson"].encode("utf-8"))
        raise LearningContractError("FIXTURE_UNEXPECTEDLY_VALID")
    try:
        jsonschema.Draft202012Validator.check_schema(FIXTURE_METADATA_SCHEMA)
        jsonschema.Draft202012Validator(FIXTURE_METADATA_SCHEMA).validate(value)
    except jsonschema.ValidationError as exc:
        raise LearningContractError("FIXTURE_METADATA_INVALID") from exc
    family, case = value["family"], value["case"]
    if family != target:
        raise LearningContractError("FIXTURE_METADATA_INVALID")

    lesson = read_document(ROOT / "learning/lessons/promotion-trust/lesson-v1.json", family="lesson")
    lab = read_document(ROOT / "learning/labs/promotion-trust/lab-v1.json", family="lab")
    if lesson["lab"]["id"] != lab["id"] or lesson["lab"]["version"] != lab["version"]:
        raise LearningContractError("FIXTURE_CONTEXT_INVALID")

    if family == "schema":
        mutated = copy.deepcopy(lesson)
        if case == "missing-required":
            mutated.pop("title")
        elif case == "unknown-field":
            mutated["unexpectedSecurityField"] = "x"
        elif case == "wrong-type":
            mutated["id"] = 42
        else:
            raise LearningContractError("FIXTURE_CASE_UNKNOWN")
        lesson_schema = read_document(ROOT / "learning/contracts/lesson-v1.schema.json")
        errors = list(jsonschema.Draft202012Validator(lesson_schema).iter_errors(mutated))
        if errors:
            priority = {"type": 0, "additionalProperties": 1, "required": 2}
            selected = min(errors, key=lambda item: priority.get(item.validator, 3))
            codes = {"required": "SCHEMA_REQUIRED_PROPERTY", "additionalProperties": "SCHEMA_UNKNOWN_PROPERTY", "type": "SCHEMA_TYPE_MISMATCH"}
            raise LearningContractError(codes.get(selected.validator, "SCHEMA_INVALID")) from selected
        raise LearningContractError("FIXTURE_UNEXPECTEDLY_VALID")
    mutation = _CASE_INPUTS.get((family, case))
    if mutation is None and not (family == "activation" or (family == "guidance" and case == "out-of-order-hint")):
        raise LearningContractError("FIXTURE_CASE_UNKNOWN")
    if family == "activation":
        from .schema import validate_activation_semantics
        activation = read_document(ROOT / "learning/contracts/command-owner-activation-i5-03-v1.json", family="command-activation")
        resolve_reference(ROOT, activation["baseRegistryPath"], activation["baseRegistrySha256"])
        validate_activation_semantics(activation)
        activation = copy.deepcopy(activation)
        activation["baseRegistrySha256"] = "0" * 64
        validate_activation_semantics(activation)
    elif family == "completion":
        from .completion import complete, validate_completion_contract, validate_completion_semantics
        validate_completion_contract(read_document(
            ROOT / "learning/contracts/completion-reconciliation-v1.json",
            family="completion-reconciliation",
        ))
        complete({"state": "verified", "revision": 1, "effects": [], "idempotency": {}}, {"expectedRevision": 1, "idempotencyKey": "fixture-context", "evidenceId": "evidence-context"})
        validate_completion_semantics(mutation)
    elif family == "evidence":
        from .evidence import validate_evidence_semantics, verify_evidence
        actual_evidence = read_document(FIXTURE_ROOT / "valid/learning-evidence-v1.json", family="learning-evidence")
        with tempfile.TemporaryDirectory() as temporary:
            artifact_raw = b'{"result":"pass"}\n'
            artifact_path = pathlib.Path(temporary) / "result.json"
            artifact_path.write_bytes(artifact_raw)
            actual_evidence["artifacts"][0].update({"locator": "result.json", "size": len(artifact_raw), "sha256": hashlib.sha256(artifact_raw).hexdigest()})
            actual_evidence["integrity"]["payloadSha256"] = hashlib.sha256(canonical_bytes({key: child for key, child in actual_evidence.items() if key != "integrity"})).hexdigest()
            verify_evidence(actual_evidence, root=pathlib.Path(temporary), seen_run_ids=set())
        validate_evidence_semantics(mutation)
    elif family == "guidance":
        from .guidance import evaluate_guidance, validate_guidance_semantics, validate_hints
        valid_hints = [{"hintId": item["id"], "order": item["order"], "revealAfter": item["revealAfter"], "evidenceEvent": item["evidenceEvent"]} for item in lesson["hints"]]
        validate_hints(valid_hints)
        evaluate_guidance({"satisfiedPrerequisites": []}, {"action": "hint", "prerequisites": []})
        if case == "out-of-order-hint":
            hints = list(reversed(valid_hints))
            validate_hints(hints)
        else:
            validate_guidance_semantics(mutation)
    elif family == "migration":
        from .registry import migrate_persisted_document, validate_registry_semantics
        read_document(ROOT / "learning/contracts/learning-contract-version-registry-v1.json", family="version-registry")
        migrate_persisted_document(FIXTURE_ROOT / "valid/private-migration-v0.json", "private-migration-v1")
        validate_registry_semantics(mutation, expected_base_sha256=BASE_REGISTRY_SHA256)
    elif family == "openapi":
        from .openapi import LearningPlatform, validate_openapi_semantics, validate_shipped_openapi
        validate_shipped_openapi()
        LearningPlatform().dispatch({"method": "GET", "path": "/health/live", "headers": {}, "query": {}})
        validate_openapi_semantics(mutation)
    elif family == "operation":
        from .openapi import validate_operation_matrix, validate_operation_semantics
        matrix = read_document(ROOT / "learning/contracts/operation-matrix-v1.json", family="operation-matrix")
        validate_operation_matrix(matrix)
        validate_operation_semantics(mutation)
    elif family == "promotion":
        from .fitness import evaluate_promotion_document, validate_promotion_semantics
        manifest = read_document(ROOT / "learning/manifests/promotion-trust-v1.json", family="promotion-manifest")
        resolve_reference(ROOT, manifest["fixture"]["path"], manifest["fixture"]["sha256"])
        evaluate_promotion_document(manifest, root=ROOT)
        validate_promotion_semantics(mutation, expected_fixture_sha256=PROMOTION_FIXTURE_SHA256)
    elif family == "reference":
        from .references import validate_contract_reference
        manifest = read_document(ROOT / "learning/manifests/promotion-trust-v1.json", family="promotion-manifest")
        resolve_reference(ROOT, manifest["fixture"]["path"], manifest["fixture"]["sha256"])
        validate_contract_reference(mutation, root=ROOT)
    elif family == "state":
        from .state import execute_operation, validate_state_semantics
        progress = {
            "schemaVersion": "progress-v1", "progressId": "progress-fixture",
            "actor": {"subjectId": "fixture-actor", "authContextSha256": "0" * 64},
            "lessonId": lesson["id"], "lessonVersion": lesson["version"],
            "labId": lab["id"], "labVersion": lab["version"],
            "contractSetSha256": "0" * 64, "revision": 0, "state": "not-started",
            "events": [], "completion": None,
        }
        with tempfile.TemporaryDirectory() as temporary:
            persisted = pathlib.Path(temporary) / "progress.json"
            persisted.write_bytes(canonical_bytes(progress) + b"\n")
            read_document(persisted, family="progress")
        execute_operation({"state": "not-started", "revision": 0, "effects": []}, {"action": "start", "expectedRevision": 0, "prerequisitesSatisfied": True})
        validate_state_semantics(mutation)
    raise LearningContractError("FIXTURE_UNEXPECTEDLY_VALID")


def validate_invalid_corpus() -> list[dict[str, str]]:
    index = read_document(FIXTURE_ROOT / "fixture-index-v1.json")
    rows = index.get("fixtures") if isinstance(index, dict) else None
    if not isinstance(rows, list) or len(rows) != 65:
        raise LearningContractError("FIXTURE_INDEX_COUNT")
    declared = {row.get("path") for row in rows if isinstance(row, dict)}
    actual = {
        path.relative_to(FIXTURE_ROOT).as_posix()
        for path in (FIXTURE_ROOT / "invalid").rglob("*")
        if path.is_file()
    }
    if declared != actual or len(declared) != 65:
        raise LearningContractError("FIXTURE_INDEX_INCOMPLETE")
    results: list[dict[str, str]] = []
    for row in rows:
        actual_code = "OK"
        try:
            validate_invalid_fixture(FIXTURE_ROOT / row["path"], row["target"])
        except LearningContractError as exc:
            actual_code = exc.code
        result = {"rowId": row["rowId"], "expected": row["expectedCode"], "actual": actual_code}
        results.append(result)
        if actual_code != row["expectedCode"]:
            raise LearningContractError(f"FIXTURE_RESULT_MISMATCH:{row['rowId']}:{row['expectedCode']}:{actual_code}")
    return results


def _validate_schema_instance(schema_path: pathlib.Path, instance_path: pathlib.Path) -> None:
    schema_value = read_document(schema_path)
    instance = read_document(instance_path)
    try:
        jsonschema.Draft202012Validator.check_schema(schema_value)
        jsonschema.Draft202012Validator(schema_value).validate(instance)
    except (jsonschema.exceptions.SchemaError, jsonschema.exceptions.ValidationError) as exc:
        raise LearningContractError(f"SHIPPED_SCHEMA_INVALID:{schema_path.name}") from exc


def validate_valid_corpus() -> None:
    pairs = [
        ("lesson-v1.schema.json", ROOT / "learning/lessons/promotion-trust/lesson-v1.json"),
        ("lab-v1.schema.json", ROOT / "learning/labs/promotion-trust/lab-v1.json"),
        ("completion-reconciliation-v1.schema.json", FIXTURE_ROOT / "valid/completion-reconciliation-v1.json"),
        ("operation-matrix-v1.schema.json", FIXTURE_ROOT / "valid/operation-matrix-v1.json"),
        ("learning-evidence-v1.schema.json", FIXTURE_ROOT / "valid/learning-evidence-v1.json"),
        ("promotion-trust-learning-manifest-v1.schema.json", FIXTURE_ROOT / "valid/promotion-trust-v1.json"),
        ("promotion-trust-learning-manifest-v1.schema.json", ROOT / "learning/manifests/promotion-trust-v1.json"),
    ]
    for schema_name, instance_path in pairs:
        _validate_schema_instance(ROOT / "learning/contracts" / schema_name, instance_path)
    promotion = read_document(ROOT / "learning/manifests/promotion-trust-v1.json")
    resolve_reference(ROOT, promotion["fixture"]["path"], promotion["fixture"]["sha256"])
    if promotion["fixture"]["sha256"] != promotion["fixtureSha256"]:
        raise LearningContractError("PROMOTION_FIXTURE_HASH_MISMATCH")
    expected_contract_set_schema = hashlib.sha256(
        (ROOT / "learning/contracts/learning-contract-set-v1.schema.json").read_bytes()
    ).hexdigest()
    if promotion["contractSetSha256"] != expected_contract_set_schema:
        raise LearningContractError("PROMOTION_CONTRACT_SET_HASH_MISMATCH")
    private = read_document(FIXTURE_ROOT / "valid/private-migration-v0.json")
    from .registry import migrate_document
    if migrate_document(migrate_document(private, "private-migration-v1"), "private-migration-v0") != private:
        raise LearningContractError("MIGRATION_ROUND_TRIP_LOSSY")


def _verify_release_hashes() -> None:
    registry = read_document(ROOT / "learning/contracts/learning-contract-version-registry-v1.json")
    base = registry.get("baseRegistry", {})
    if base.get("sha256") != hashlib.sha256((ROOT / base.get("path", "")).read_bytes()).hexdigest():
        raise LearningContractError("BASE_REGISTRY_HASH_MISMATCH")
    schema_rows = [family["schema"] for family in registry["ownedFamilies"]]
    schema_rows.extend(
        item["schema"]
        for extension in registry["familyExtensions"]
        for item in extension["addedReadableVersions"]
    )
    for row in schema_rows:
        if hashlib.sha256((ROOT / row["path"]).read_bytes()).hexdigest() != row["sha256"]:
            raise LearningContractError(f"REGISTRY_SCHEMA_HASH_MISMATCH:{row['path']}")
    activation = read_document(ROOT / "learning/contracts/command-owner-activation-i5-03-v1.json")
    if activation["baseRegistrySha256"] != hashlib.sha256((ROOT / activation["baseRegistryPath"]).read_bytes()).hexdigest():
        raise LearningContractError("COMMAND_ACTIVATION_BASE_MISMATCH")
    fragment = activation["fragment"]
    if hashlib.sha256((ROOT / fragment["path"]).read_bytes()).hexdigest() != fragment["sha256"]:
        raise LearningContractError("COMMAND_FRAGMENT_HASH_MISMATCH")
    base_commands = {
        row["command"]: row
        for row in read_document(ROOT / activation["baseRegistryPath"])["commands"]
        if row.get("owner") == activation["owner"]
    }
    activated_commands = {row["commandId"]: row for row in activation["commands"]}
    if set(base_commands) != set(activated_commands):
        raise LearningContractError("COMMAND_ACTIVATION_SET_MISMATCH")
    for command_id, activated in activated_commands.items():
        retained = base_commands[command_id]
        if (
            retained["fragment"] != fragment["path"]
            or retained["security"] != "S3"
            or retained["availability"] != "future-owner"
            or activated != {
                "commandId": command_id,
                "availability": "implemented",
                "evidenceVersion": "fitness-result-v2",
            }
        ):
            raise LearningContractError("COMMAND_ACTIVATION_ROW_MISMATCH")
    contract_set = read_document(ROOT / "learning/contracts/learning-contract-set-v1.json")
    paths = [item["path"] for item in contract_set["contracts"]]
    if paths != sorted(paths) or len(paths) != len(set(paths)):
        raise LearningContractError("CONTRACT_SET_ORDER_INVALID")
    for item in contract_set["contracts"]:
        actual = hashlib.sha256((ROOT / item["path"]).read_bytes()).hexdigest()
        if item["contentSha256"] != actual:
            raise LearningContractError(f"CONTRACT_SET_HASH_MISMATCH:{item['path']}")


def validate_all_contracts() -> list[dict[str, str]]:
    from .openapi import validate_shipped_openapi
    validate_valid_corpus()
    invalid_rows = validate_invalid_corpus()
    validate_shipped_openapi()
    _verify_release_hashes()
    validate_shipped_vite_binding()
    return invalid_rows


def _git_value(*arguments: str) -> str:
    return subprocess.check_output(["git", *arguments], cwd=ROOT, text=True).strip()


def _fitness_provenance() -> dict[str, Any]:
    schema_hashes = [
        {"name": path.name.replace(".schema.json", "").replace(".json", ""), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
        for path in sorted((ROOT / "learning/contracts").glob("*.schema.json"))
    ]
    contract_hashes = list(schema_hashes)
    contract_hashes.extend(
        {"name": name, "sha256": hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()}
        for name, relative in (
            ("promotion-trust-vite-binding-document-v1", "learning/bindings/vite/promotion-trust-v1.json"),
            ("stage-a-contract-set-v1", "learning/contracts/learning-contract-set-v1.json"),
            ("stage-a-promotion-manifest-v1", "learning/manifests/promotion-trust-v1.json"),
            ("stage-a-completion-authority-v1", "learning/contracts/completion-reconciliation-v1.json"),
            ("issue-7-vite-adr", "docs/decisions/0005-web-stack.md"),
            ("issue-7-vite-package", "spikes/web/candidates/vite/package.json"),
            ("issue-7-vite-lock", "spikes/web/candidates/vite/package-lock.json"),
            ("issue-7-vite-lesson-contract", "spikes/web/candidates/vite/src/lesson-contract.mjs"),
        )
    )
    contract_hashes.sort(key=lambda item: (item["name"], item["sha256"]))
    fixture_hashes = [
        {
            "name": path.relative_to(FIXTURE_ROOT).as_posix().replace("/", "."),
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        }
        for path in sorted(FIXTURE_ROOT.rglob("*")) if path.is_file()
    ]
    fixture_hashes.extend(
        {"name": name, "sha256": hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()}
        for name, relative in (
            ("promotion-trust-evidence-v1", "tests/fixtures/learning/promotion-trust/evidence-v1.json"),
            ("promotion-trust-fixture-manifest-v2", "tests/fixtures/learning/promotion-trust/manifest.json"),
        )
    )
    fixture_hashes.sort(key=lambda item: (item["name"], item["sha256"]))
    return {
        "inputSha": _git_value("rev-parse", "HEAD"),
        "testedTreeSha": _git_value("rev-parse", "HEAD^{tree}"),
        "dependencyMergeShas": [
            "24be3b34c6b0fcdbd07c5800dcab349054e34713",
            "1806b6d515f2f7a2ace2be7077af84a745ff221f",
            "5c2244c2c860234d0df49cf0a42ad950c6495717",
            "fecf6bb8e5dfa7cc69f9766f72ac6f5b9301dad9",
        ],
        "contractHashes": contract_hashes,
        "fixtureHashes": fixture_hashes,
        "schemaHashes": schema_hashes,
        "lockSha256": hashlib.sha256((ROOT / "requirements/golden-py312-macos-arm64.lock").read_bytes()).hexdigest(),
    }


def _emit_fitness(
    command_id: str,
    subject_type: str,
    subject_id: str,
    started: float,
    *,
    invalid_rows: list[dict[str, str]] | None = None,
) -> pathlib.Path:
    from scripts.golden.workspace import allocate_family, atomic_write
    from .fitness import verify_fitness
    workspace = allocate_family(("evidence", "learning-contracts"), command_id)
    try:
        result_raw = b'{"result":"pass"}\n'
        atomic_write(workspace.run_fd, "result.json", result_raw)
        invalid_raw = json.dumps(invalid_rows or [], sort_keys=True, separators=(",", ":")).encode() + b"\n"
        atomic_write(workspace.run_fd, "invalid-fixture-results.json", invalid_raw)
        provenance = _fitness_provenance()
        now = datetime.datetime.now(datetime.UTC)
        argv = [sys.executable, "-m", "scripts.learning_contracts.check", command_id]
        value: dict[str, Any] = {
            "schemaVersion": "fitness-result-v2",
            "commandId": command_id,
            "owner": "I5-03",
            "requested": {"subjectType": subject_type, "subjectId": subject_id, "parameters": []},
            "status": "pass", "failureCode": None, "remediation": None,
            "inputSha": provenance["inputSha"], "testedTreeSha": provenance["testedTreeSha"],
            "dependencyMergeShas": provenance["dependencyMergeShas"],
            "contractHashes": provenance["contractHashes"],
            "fixtureHashes": provenance["fixtureHashes"],
            "schemaHashes": provenance["schemaHashes"],
            "toolchain": [{"name": "python", "version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"}],
            "lockSha256": provenance["lockSha256"],
            "invocation": {"publicArgv": ["make", command_id], "canonicalChildArgv": ["python", "-m", "scripts.learning_contracts.check", command_id], "actualChildArgvSha256": hashlib.sha256(canonical_bytes(argv)).hexdigest(), "cwdRole": "repository-root"},
            "startedAt": datetime.datetime.fromtimestamp(started, datetime.UTC).isoformat().replace("+00:00", "Z"),
            "finishedAt": now.isoformat().replace("+00:00", "Z"),
            "durationMs": max(0, int((time.time() - started) * 1000)),
            "rawLocator": "result.json", "projectionLocator": None, "envelopeLocator": None, "projectionSha256": None,
            "artifacts": [
                {"locator": "result.json", "mediaType": "application/json", "size": len(result_raw), "sha256": hashlib.sha256(result_raw).hexdigest()},
                {"locator": "invalid-fixture-results.json", "mediaType": "application/json", "size": len(invalid_raw), "sha256": hashlib.sha256(invalid_raw).hexdigest()},
            ],
            "redactionClass": "public-contract-evidence", "retentionClass": "review-bundle",
            "rollback": {"supported": True, "preserveEvidence": True},
            "canonicalization": "RFC8785",
        }
        value["payloadSha256"] = hashlib.sha256(canonical_bytes(value)).hexdigest()
        peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        peak_bytes = int(peak if platform.system() == "Darwin" else peak * 1024)
        if value["durationMs"] > 120000 or peak_bytes > 512 * 1024 * 1024 or len(result_raw) + len(invalid_raw) > 10 * 1024 * 1024:
            raise LearningContractError("RESOURCE_CEILING_EXCEEDED")
        activation = read_document(ROOT / "learning/contracts/command-owner-activation-i5-03-v1.json")
        verify_fitness(value, root=workspace.path, activation=activation, expected_provenance=provenance)
        atomic_write(workspace.run_fd, "fitness-result-v2.json", json.dumps(value, sort_keys=True, separators=(",", ":")).encode() + b"\n")
        return workspace.path / "fitness-result-v2.json"
    finally:
        workspace.close()


def main(argv: Sequence[str] | None = None) -> int:
    started = time.time()
    parser = argparse.ArgumentParser(prog="learning-contracts")
    parser.add_argument("command", nargs="?", choices=("check", "lesson", "api", "evidence"))
    parser.add_argument("--lesson")
    parser.add_argument("--evidence")
    arguments = parser.parse_args(argv)
    if arguments.lesson is not None:
        validate_public_value("LESSON", arguments.lesson)
    if arguments.evidence is not None:
        validate_public_value("EVIDENCE", arguments.evidence)
    command = arguments.command or "check"
    if command == "check":
        rows = validate_all_contracts()
        evidence_path = _emit_fitness("learning-contracts-check", "contract-set", "issue-8-stage-a-v1", started, invalid_rows=rows)
        print(json.dumps({"result": "pass", "invalidFixtures": len(rows), "evidence": evidence_path.relative_to(ROOT).as_posix()}, sort_keys=True))
    elif command == "api":
        from .openapi import validate_shipped_openapi
        validate_shipped_openapi()
        evidence_path = _emit_fitness("api-contracts-check", "contract-set", "learning-platform-v1", started)
        print(json.dumps({"result": "pass", "operations": 16, "evidence": evidence_path.relative_to(ROOT).as_posix()}, sort_keys=True))
    elif command == "lesson":
        lesson = arguments.lesson or os.environ.get("LESSON", "")
        validate_public_value("LESSON", lesson)
        if lesson != "promotion-trust":
            raise LearningContractError("LESSON_UNKNOWN")
        validate_valid_corpus()
        validate_shipped_vite_binding()
        evidence_path = _emit_fitness("lesson-check", "lesson", lesson, started)
        print(json.dumps({"result": "pass", "lesson": lesson, "evidence": evidence_path.relative_to(ROOT).as_posix()}, sort_keys=True))
    elif command == "evidence":
        locator = arguments.evidence or os.environ.get("EVIDENCE", "")
        validate_public_value("EVIDENCE", locator)
        path = ROOT / locator
        value = read_document(path)
        if value.get("schemaVersion") == "fitness-result-v2":
            from .fitness import verify_fitness
            activation = read_document(ROOT / "learning/contracts/command-owner-activation-i5-03-v1.json")
            verify_fitness(value, root=path.parent, activation=activation, expected_provenance=_fitness_provenance())
        elif value.get("schemaVersion") == "learning-evidence-v1":
            from .evidence import verify_evidence
            verify_evidence(
                value,
                root=path.parent,
                authoritative_root=ROOT,
                replay_root=ROOT / ".artifacts/evidence/learning-replay",
            )
        else:
            raise LearningContractError("EVIDENCE_VERSION_UNSUPPORTED")
        evidence_path = _emit_fitness("evidence-verify", "evidence", path.name, started)
        print(json.dumps({"result": "pass", "verified": locator, "evidence": evidence_path.relative_to(ROOT).as_posix()}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
