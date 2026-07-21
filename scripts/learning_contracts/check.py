#!/usr/bin/env python3
"""Public Stage A command scaffold."""

from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import os
import pathlib
import re
import subprocess
import sys
import time
from collections.abc import Sequence
from typing import Any

import jsonschema

from .canonical import canonical_bytes, parse_json
from .schema import LearningContractError, read_document, validate_document


ROOT = pathlib.Path(__file__).resolve().parents[2]
FIXTURE_ROOT = ROOT / "tests/fixtures/learning/contracts"
BASE_REGISTRY_SHA256 = "8e18588f63b5d99c0b60a229758575e8badf0f055bfcb4f89908f9fa2684a57e"
PROMOTION_FIXTURE_SHA256 = "0a1dcd4023648f52009bfd4dc5d529c00ce66f42cd0e725732b972b0b78df341"
MUTATION_VECTOR_SCHEMA = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "object",
    "minProperties": 1,
    "maxProperties": 12,
    "propertyNames": {"pattern": "^[A-Za-z$][A-Za-z0-9$]*$"},
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


def _cycle(edges: object) -> bool:
    if not isinstance(edges, list):
        return False
    graph: dict[str, list[str]] = {}
    for edge in edges:
        if isinstance(edge, list) and len(edge) == 2 and all(isinstance(item, str) for item in edge):
            graph.setdefault(edge[0], []).append(edge[1])
    visiting: set[str] = set()
    visited: set[str] = set()
    def visit(node: str) -> bool:
        if node in visiting:
            return True
        if node in visited:
            return False
        visiting.add(node)
        found = any(visit(child) for child in graph.get(node, []))
        visiting.remove(node)
        visited.add(node)
        return found
    return any(visit(node) for node in graph)


def _semantic_code(target: str, value: dict[str, Any]) -> str | None:
    if target == "activation":
        if value.get("baseRegistrySha256") != hashlib.sha256((ROOT / "learning/contracts/command-owner-registry-v1.json").read_bytes()).hexdigest():
            return "COMMAND_ACTIVATION_BASE_MISMATCH"
    elif target == "completion":
        source = value.get("completionSource")
        if source == "browser":
            return "COMPLETION_AUTHORITY_REQUIRED"
        if source in {"evidence-presence", "operation-result"}:
            return "COMPLETION_DUAL_TRUTH"
        if value.get("orphan") and value.get("attemptsCompletion"):
            return "RECONCILIATION_ORPHAN_CANNOT_COMPLETE"
        if value.get("orphan") and value.get("declaredSha256") != value.get("actualSha256"):
            return "RECONCILIATION_HASH_MISMATCH"
    elif target == "evidence":
        if "rawSql" in value:
            return "CONTRACT_INJECTION_FIELD_FORBIDDEN"
        locator = value.get("locator")
        if isinstance(locator, str) and (locator.startswith("/") or ".." in pathlib.PurePosixPath(locator).parts):
            return "EVIDENCE_LOCATOR_INVALID"
        if value.get("dependencyMergeShas") == []:
            return "EVIDENCE_PROVENANCE_INCOMPLETE"
        if value.get("testedTreeSha") == "self-containing-identity":
            return "EVIDENCE_RECURSIVE_IDENTITY"
        if "indexedPayloadSha256" in value and value.get("indexedPayloadSha256") != value.get("payloadSha256"):
            return "EVIDENCE_REPLAY_CONFLICT"
        if "payload" in value and value.get("payloadSha256") != hashlib.sha256(canonical_bytes(value["payload"])).hexdigest():
            return "EVIDENCE_PAYLOAD_HASH_MISMATCH"
        artifact = value.get("artifact")
        if isinstance(artifact, dict) and artifact.get("sha256") != value.get("actualSha256"):
            return "EVIDENCE_ARTIFACT_HASH_MISMATCH"
        if "verifierSha256" in value and value.get("verifierSha256") != value.get("actualVerifierSha256"):
            return "EVIDENCE_VERIFIER_HASH_MISMATCH"
    elif target == "guidance":
        if value.get("completionMutation"):
            return "HINT_COMPLETION_FORBIDDEN"
        if isinstance(value.get("command"), str) and re.search(r"(?:touch|rm|mv|cp|>|curl|wget)", value["command"]):
            return "PROBE_MUTATION_FORBIDDEN"
        if value.get("status") == "unavailable" and value.get("result") == "pass":
            return "PROBE_REQUIRED_UNAVAILABLE" if value.get("required") else "PROBE_OPTIONAL_FALSE_PASS"
        hints = value.get("hints")
        if isinstance(hints, list) and [item.get("order") for item in hints] != sorted(item.get("order") for item in hints):
            return "HINT_ORDER_INVALID"
        if value.get("revealed") and not value.get("revealAuthorized"):
            return "HINT_REVEAL_FORBIDDEN"
    elif target == "migration":
        base = value.get("baseRegistry")
        if isinstance(base, dict) and base.get("sha256") != BASE_REGISTRY_SHA256:
            return "BASE_REGISTRY_HASH_MISMATCH"
        if _cycle(value.get("edges")):
            return "MIGRATION_CYCLE"
        if set(value.get("ownedFamilies", [])) & set(value.get("baseFamilies", [])):
            return "SCHEMA_FAMILY_COLLISION"
        if value.get("lossless") is False:
            return "MIGRATION_LOSSY_FORBIDDEN"
        if value.get("family") == "lesson" and value.get("version") != "lesson-v1":
            return "SCHEMA_VERSION_UNREADABLE"
    elif target == "openapi":
        if value.get("errors") == ["500 INTERNAL_CONTRACT_ERROR"]:
            return "OPENAPI_ERROR_CONTRACT_MISMATCH"
        if "authority" in value and value.get("authority") is None:
            return "OPERATION_AUTHORITY_MISSING"
        if "idempotency" in value and value.get("idempotency") is None:
            return "OPERATION_IDEMPOTENCY_MISSING"
        if value.get("responseHeaders") == []:
            return "OPENAPI_VERSION_NEGOTIATION_INCOMPLETE"
        if value.get("channels") == [] and value.get("asyncapiArtifacts"):
            return "ASYNCAPI_WITHOUT_CHANNEL"
        if value.get("matrixOperationIds") != value.get("openapiOperationIds"):
            return "OPENAPI_OPERATION_SET_MISMATCH"
        if "rawSql" in value.get("requestFields", []):
            return "OPENAPI_RAW_QUERY_FORBIDDEN"
        reference = value.get("$ref")
        if isinstance(reference, str) and "://" in reference:
            return "OPENAPI_REF_FORBIDDEN"
        if value.get("schema", "").endswith("Request-v1") and set(value.get("required", [])) != {"schemaVersion", "requestId"}:
            return "OPENAPI_REQUEST_CONTRACT_MISMATCH"
        if value.get("schema") == "Workspace" and set(value.get("required", [])) != {"schemaVersion", "workspaceId", "state"}:
            return "OPENAPI_RESPONSE_CONTRACT_MISMATCH"
    elif target == "operation":
        operations = value.get("operations")
        if isinstance(operations, list):
            pairs = [(item.get("method"), item.get("path")) for item in operations]
            if len(pairs) != len(set(pairs)):
                return "OPERATION_DUPLICATE"
        if "authorization" in value and value.get("authorization") is None:
            return "OPERATION_AUTHORIZATION_INCOMPLETE"
        if "evidence" in value and value.get("evidence") is None:
            return "OPERATION_EVIDENCE_INCOMPLETE"
        if "operationId" in value and not any(key in value for key in ("taxonomy", "processRole", "authorization", "evidence")):
            return "OPERATION_TAXONOMY_INCOMPLETE"
        if isinstance(value.get("processRole"), str) and any(token in value["processRole"] for token in ("portal", "sqlite", ".")):
            return "OPERATION_ROLE_NOT_NEUTRAL"
    elif target == "promotion":
        if value.get("fixtureSha256") != PROMOTION_FIXTURE_SHA256 and "fixtureSha256" in value:
            return "PROMOTION_FIXTURE_HASH_MISMATCH"
        if value.get("commonGrain") is not None:
            return "PROMOTION_COMMON_GRAIN_FORBIDDEN"
        if value.get("limitations") == []:
            return "PROMOTION_LIMITATION_REQUIRED"
    elif target == "reference":
        reference = value.get("reference")
        if reference == "verifier:missing":
            return "REF_TARGET_MISSING"
        if _cycle(value.get("edges")):
            return "REF_CYCLE"
        if isinstance(reference, str) and ".." in pathlib.PurePosixPath(reference).parts:
            return "REF_TRAVERSAL_FORBIDDEN"
        if isinstance(reference, str) and "://" in reference:
            return "REF_REMOTE_FORBIDDEN"
        if isinstance(reference, str) and "sha256" in value:
            candidate = ROOT / reference
            if not candidate.is_file() or hashlib.sha256(candidate.read_bytes()).hexdigest() != value["sha256"]:
                return "REF_SCHEMA_HASH_MISMATCH"
    elif target == "state":
        if value.get("effectCount", 0) > 1:
            return "IDEMPOTENCY_DUPLICATE_EFFECT"
        if "storedRequestSha256" in value and value.get("storedRequestSha256") != value.get("requestSha256"):
            return "IDEMPOTENCY_KEY_REUSE"
        if value.get("from") == "not_started" and value.get("to") == "completed":
            return "STATE_TRANSITION_FORBIDDEN"
        if "expectedRevision" in value and value.get("expectedRevision") != value.get("actualRevision"):
            return "PROGRESS_VERSION_CONFLICT"
    return None


def validate_invalid_fixture(path: pathlib.Path, target: str) -> None:
    try:
        value = read_document(path)
    except LearningContractError as exc:
        if target == "openapi" and exc.code == "YAML_DUPLICATE_NAME":
            raise LearningContractError("OPENAPI_YAML_DUPLICATE_KEY") from exc
        raise
    if target == "canonical":
        if "encodedHex" in value:
            parse_json(bytes.fromhex(value["encodedHex"]))
        elif "encodedJson" in value:
            parse_json(value["encodedJson"].encode("utf-8"))
        raise LearningContractError("FIXTURE_UNEXPECTEDLY_VALID")
    if target == "schema":
        lesson_schema = read_document(ROOT / "learning/contracts/lesson-v1.schema.json")
        errors = list(jsonschema.Draft202012Validator(lesson_schema).iter_errors(value))
        if errors:
            priority = {"type": 0, "additionalProperties": 1, "required": 2}
            selected = min(errors, key=lambda item: priority.get(item.validator, 3))
            codes = {"required": "SCHEMA_REQUIRED_PROPERTY", "additionalProperties": "SCHEMA_UNKNOWN_PROPERTY", "type": "SCHEMA_TYPE_MISMATCH"}
            raise LearningContractError(codes.get(selected.validator, "SCHEMA_INVALID")) from selected
        raise LearningContractError("FIXTURE_UNEXPECTEDLY_VALID")
    try:
        jsonschema.Draft202012Validator.check_schema(MUTATION_VECTOR_SCHEMA)
        jsonschema.Draft202012Validator(MUTATION_VECTOR_SCHEMA).validate(value)
    except jsonschema.ValidationError as exc:
        raise LearningContractError("FIXTURE_VECTOR_SCHEMA_INVALID") from exc
    code = _semantic_code(target, value)
    if code is None:
        raise LearningContractError("FIXTURE_UNEXPECTEDLY_VALID")
    raise LearningContractError(code)


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
    except jsonschema.exceptions.JsonSchemaException as exc:
        raise LearningContractError(f"SHIPPED_SCHEMA_INVALID:{schema_path.name}") from exc


def validate_valid_corpus() -> None:
    pairs = [
        ("lesson-v1.schema.json", ROOT / "learning/lessons/promotion-trust/lesson-v1.json"),
        ("lab-v1.schema.json", ROOT / "learning/labs/promotion-trust/lab-v1.json"),
        ("completion-reconciliation-v1.schema.json", FIXTURE_ROOT / "valid/completion-reconciliation-v1.json"),
        ("operation-matrix-v1.schema.json", FIXTURE_ROOT / "valid/operation-matrix-v1.json"),
        ("learning-evidence-v1.schema.json", FIXTURE_ROOT / "valid/learning-evidence-v1.json"),
        ("promotion-trust-learning-manifest-v1.schema.json", FIXTURE_ROOT / "valid/promotion-trust-v1.json"),
    ]
    for schema_name, instance_path in pairs:
        _validate_schema_instance(ROOT / "learning/contracts" / schema_name, instance_path)
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
    return invalid_rows


def _git_value(*arguments: str) -> str:
    return subprocess.check_output(["git", *arguments], cwd=ROOT, text=True).strip()


def _emit_fitness(command_id: str, subject_type: str, subject_id: str, started: float) -> pathlib.Path:
    from scripts.golden.workspace import allocate_family, atomic_write
    from .fitness import verify_fitness
    workspace = allocate_family(("evidence", "learning-contracts"), command_id)
    try:
        result_raw = b'{"result":"pass"}\n'
        atomic_write(workspace.run_fd, "result.json", result_raw)
        source_sha = _git_value("rev-parse", "HEAD")
        tested_tree = _git_value("rev-parse", "HEAD^{tree}")
        now = datetime.datetime.now(datetime.UTC)
        argv = [sys.executable, "-m", "scripts.learning_contracts.check", command_id]
        contract_hashes = [
            {"name": path.name.replace(".schema.json", "").replace(".json", ""), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
            for path in sorted((ROOT / "learning/contracts").glob("*.schema.json"))
        ]
        fixture_hashes = [
            {"name": path.stem, "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
            for path in sorted((FIXTURE_ROOT / "valid").glob("*"))
        ]
        value: dict[str, Any] = {
            "schemaVersion": "fitness-result-v2",
            "commandId": command_id,
            "owner": "I5-03",
            "requested": {"subjectType": subject_type, "subjectId": subject_id, "parameters": []},
            "status": "pass", "failureCode": None, "remediation": None,
            "inputSha": source_sha, "testedTreeSha": tested_tree,
            "dependencyMergeShas": ["24be3b34c6b0fcdbd07c5800dcab349054e34713"],
            "contractHashes": contract_hashes,
            "fixtureHashes": fixture_hashes,
            "schemaHashes": contract_hashes,
            "toolchain": [{"name": "python", "version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"}],
            "lockSha256": hashlib.sha256((ROOT / "requirements/golden-py312-macos-arm64.lock").read_bytes()).hexdigest(),
            "invocation": {"publicArgv": ["make", command_id], "canonicalChildArgv": ["python", "-m", "scripts.learning_contracts.check", command_id], "actualChildArgvSha256": hashlib.sha256(canonical_bytes(argv)).hexdigest(), "cwdRole": "repository-root"},
            "startedAt": datetime.datetime.fromtimestamp(started, datetime.UTC).isoformat().replace("+00:00", "Z"),
            "finishedAt": now.isoformat().replace("+00:00", "Z"),
            "durationMs": max(0, int((time.time() - started) * 1000)),
            "rawLocator": "result.json", "projectionLocator": None, "envelopeLocator": None, "projectionSha256": None,
            "artifacts": [{"locator": "result.json", "mediaType": "application/json", "size": len(result_raw), "sha256": hashlib.sha256(result_raw).hexdigest()}],
            "redactionClass": "public-contract-evidence", "retentionClass": "review-bundle",
            "rollback": {"supported": True, "preserveEvidence": True},
            "canonicalization": "RFC8785",
        }
        value["payloadSha256"] = hashlib.sha256(canonical_bytes(value)).hexdigest()
        verify_fitness(value, root=workspace.path)
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
        evidence_path = _emit_fitness("learning-contracts-check", "contract-set", "issue-8-stage-a-v1", started)
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
        evidence_path = _emit_fitness("lesson-check", "lesson", lesson, started)
        print(json.dumps({"result": "pass", "lesson": lesson, "evidence": evidence_path.relative_to(ROOT).as_posix()}, sort_keys=True))
    elif command == "evidence":
        locator = arguments.evidence or os.environ.get("EVIDENCE", "")
        validate_public_value("EVIDENCE", locator)
        path = ROOT / locator
        value = read_document(path)
        if value.get("schemaVersion") == "fitness-result-v2":
            from .fitness import verify_fitness
            verify_fitness(value, root=path.parent)
        elif value.get("schemaVersion") == "learning-evidence-v1":
            from .evidence import verify_evidence
            verify_evidence(value, root=path.parent, seen_run_ids=set())
        else:
            raise LearningContractError("EVIDENCE_VERSION_UNSUPPORTED")
        evidence_path = _emit_fitness("evidence-verify", "evidence", path.name, started)
        print(json.dumps({"result": "pass", "verified": locator, "evidence": evidence_path.relative_to(ROOT).as_posix()}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
