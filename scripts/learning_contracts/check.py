"""Deterministic entrypoint shared by direct tests and public commands."""
from __future__ import annotations
from dataclasses import dataclass
import argparse
import datetime
import hashlib
import json
import os
import pathlib
import secrets
import subprocess
import sys
import time
import unittest
from typing import Any

import yaml
from jsonschema import Draft202012Validator

from . import canonical, completion, evidence, fitness, guidance, openapi, references, registry, runtime, schema, state

@dataclass(frozen=True)
class Outcome:
    code: str
    pointer: str | None = None
    detail: str = ""

def evaluate(domain: str, value: Any) -> Outcome:
    """Evaluate one contract input through its domain validator."""
    if domain == "authority":
        return Outcome(runtime.authority_code(value))
    if domain == "dependency":
        return Outcome(runtime.dependency_code(value))
    if domain == "activation":
        return Outcome(registry.activation_code(value))
    if domain == "rollback":
        return Outcome(runtime.rollback_code(value))
    if domain == "schema":
        return Outcome(schema.code(value))
    if domain == "canonical":
        return Outcome(canonical.code(value))
    if domain == "reference":
        return Outcome(references.code(value))
    if domain == "migration":
        return Outcome(registry.migration_code(value))
    if domain == "state":
        return Outcome(state.code(value))
    if domain == "completion":
        return Outcome(completion.code(value))
    if domain == "evidence":
        return Outcome(evidence.code(value))
    if domain == "operation":
        return Outcome(schema.operation_code(value))
    if domain == "openapi":
        return Outcome(openapi.code(value))
    if domain == "guidance":
        return Outcome(guidance.code(value))
    if domain == "promotion":
        return Outcome(guidance.promotion_code(value))
    if domain == "fitness":
        return Outcome(fitness.code(value))
    return Outcome("BEHAVIOR_NOT_IMPLEMENTED")


def release_documents() -> dict[str, Any]:
    """Return the complete immutable Stage A document model."""
    root = pathlib.Path(__file__).resolve().parents[2]
    paths = [
        "learning/contracts/lesson-v1.schema.json", "learning/contracts/lab-v1.schema.json",
        "learning/contracts/progress-v1.schema.json", "learning/contracts/learning-evidence-v1.schema.json",
        "learning/contracts/completion-reconciliation-v1.schema.json", "learning/contracts/operation-matrix-v1.schema.json",
        "learning/contracts/promotion-trust-learning-manifest-v1.schema.json",
        "learning/contracts/learning-contract-version-registry-v1.schema.json",
        "learning/contracts/learning-contract-version-registry-v1.json", "learning/contracts/fitness-result-v2.schema.json",
        "learning/contracts/command-owner-activation-v1.schema.json", "learning/contracts/command-owner-activation-i5-03-v1.json",
        "learning/contracts/learning-contract-set-v1.schema.json", "learning/contracts/learning-contract-set-v1.json",
        "learning/contracts/operation-matrix-v1.json", "learning/contracts/completion-reconciliation-v1.json",
        "learning/lessons/promotion-trust/lesson-v1.json", "learning/labs/promotion-trust/lab-v1.json",
        "learning/manifests/promotion-trust-v1.json", "contracts/openapi/learning-platform-v1.yaml",
        "contracts/openapi/learning-platform-openapi-profile-v1.schema.json",
        "contracts/openapi/learning-platform-problem-details-v1.schema.json",
    ]
    result: dict[str, Any] = {}
    for relative in paths:
        raw = (root / relative).read_bytes()
        if relative.endswith(".yaml"):
            result[relative] = raw
        else:
            result[relative] = json.loads(raw)
    return result


def public_surface() -> tuple[tuple[str, ...], tuple[str, ...]]:
    """Return the registered Make targets and independent valid vectors."""
    targets = ("learning-contracts-check", "lesson-check", "api-contracts-check", "evidence-verify")
    vectors = (
        "tests/fixtures/learning/contracts/valid/operation-matrix-v1.json",
        "tests/fixtures/learning/contracts/valid/completion-reconciliation-v1.json",
        "tests/fixtures/learning/contracts/valid/learning-evidence-v1.json",
        "tests/fixtures/learning/contracts/valid/promotion-trust-v1.json",
    )
    return targets, vectors


ROOT = pathlib.Path(__file__).resolve().parents[2]
INPUT_SHA = "c23106ad89d45370b06c3329f7d8963b2c62a064"
LOCK_SHA = "f41c727b39f99106f95b7937b2811e8d27db89d1d5106e9f1d9effd4403143d2"


def _json(relative: str) -> Any:
    return json.loads((ROOT / relative).read_bytes())


def _validate_release() -> None:
    documents = release_documents()
    if len(documents) != 22:
        raise ValueError("CONTRACT_SET_INCOMPLETE")
    for relative, document in documents.items():
        if relative.endswith(".schema.json"):
            Draft202012Validator.check_schema(document)
            if document.get("$schema") != "https://json-schema.org/draft/2020-12/schema" or document.get("unevaluatedProperties") is not False:
                raise ValueError("SCHEMA_PROFILE_INVALID")
    pairs = [
        ("learning/contracts/lesson-v1.schema.json", "learning/lessons/promotion-trust/lesson-v1.json"),
        ("learning/contracts/lab-v1.schema.json", "learning/labs/promotion-trust/lab-v1.json"),
        ("learning/contracts/completion-reconciliation-v1.schema.json", "learning/contracts/completion-reconciliation-v1.json"),
        ("learning/contracts/operation-matrix-v1.schema.json", "learning/contracts/operation-matrix-v1.json"),
        ("learning/contracts/promotion-trust-learning-manifest-v1.schema.json", "learning/manifests/promotion-trust-v1.json"),
        ("learning/contracts/learning-contract-version-registry-v1.schema.json", "learning/contracts/learning-contract-version-registry-v1.json"),
        ("learning/contracts/command-owner-activation-v1.schema.json", "learning/contracts/command-owner-activation-i5-03-v1.json"),
        ("learning/contracts/learning-contract-set-v1.schema.json", "learning/contracts/learning-contract-set-v1.json"),
    ]
    for schema_path, instance_path in pairs:
        Draft202012Validator(documents[schema_path]).validate(documents[instance_path])
    matrix = documents["learning/contracts/operation-matrix-v1.json"]
    operations = matrix.get("operations", [])
    if matrix.get("channels") != [] or len(operations) != 16:
        raise ValueError("OPERATION_MATRIX_INCOMPLETE")
    if len({row["operationId"] for row in operations}) != 16 or len({(row["method"], row["path"]) for row in operations}) != 16:
        raise ValueError("OPERATION_DUPLICATE")
    if documents["learning/contracts/completion-reconciliation-v1.json"].get("authorityId") != completion.AUTHORITY:
        raise ValueError("COMPLETION_AUTHORITY_REQUIRED")
    if documents["learning/contracts/learning-contract-version-registry-v1.json"]["baseRegistry"]["sha256"] != registry.BASE_SCHEMA_REGISTRY_SHA:
        raise ValueError("BASE_REGISTRY_HASH_MISMATCH")
    overlay = documents["learning/contracts/learning-contract-version-registry-v1.json"]
    schema_rows = [row["schema"] for row in overlay["ownedFamilies"]]
    schema_rows += [row["schema"] for extension in overlay["familyExtensions"] for row in extension["addedReadableVersions"]]
    for row in schema_rows:
        if hashlib.sha256((ROOT / row["path"]).read_bytes()).hexdigest() != row["sha256"]:
            raise ValueError("REF_SCHEMA_HASH_MISMATCH")
    activation = documents["learning/contracts/command-owner-activation-i5-03-v1.json"]
    if registry.activation_code(activation) != "OK" or {row["commandId"] for row in activation["commands"]} != fitness.COMMANDS:
        raise ValueError("COMMAND_ACTIVATION_INVALID")
    fragment = activation["fragment"]
    if hashlib.sha256((ROOT / fragment["path"]).read_bytes()).hexdigest() != fragment["sha256"]:
        raise ValueError("COMMAND_ACTIVATION_FRAGMENT_MISMATCH")
    contract_set = documents["learning/contracts/learning-contract-set-v1.json"]
    paths = [row["path"] for row in contract_set["contracts"]]
    if len(paths) != 20 or paths != sorted(paths) or len(paths) != len(set(paths)):
        raise ValueError("CONTRACT_SET_INCOMPLETE")
    for row in contract_set["contracts"]:
        if row["path"] == "learning/contracts/learning-contract-set-v1.json":
            raise ValueError("EVIDENCE_RECURSIVE_IDENTITY")
        if hashlib.sha256((ROOT / row["path"]).read_bytes()).hexdigest() != row["contentSha256"]:
            raise ValueError("CONTRACT_SET_HASH_MISMATCH")
    set_sha = hashlib.sha256((ROOT / "learning/contracts/learning-contract-set-v1.json").read_bytes()).hexdigest()
    if documents["learning/manifests/promotion-trust-v1.json"]["contractSetSha256"] != set_sha:
        raise ValueError("PROMOTION_CONTRACT_SET_MISMATCH")


def _validate_openapi() -> None:
    raw = (ROOT / "contracts/openapi/learning-platform-v1.yaml").read_bytes()
    source_code = openapi.code(raw)
    if source_code != "OK":
        raise ValueError(source_code)
    model = yaml.load(raw.decode("utf-8"), Loader=openapi.StrictLoader)
    if model.get("openapi") != "3.2.0" or model.get("info", {}).get("version") != "learning-platform-v1":
        raise ValueError("OPENAPI_VERSION_NEGOTIATION_INCOMPLETE")
    api_rows = {(method.upper(), path, operation["operationId"]) for path, item in model["paths"].items() for method, operation in item.items()}
    matrix_rows = {(row["method"], row["path"], row["operationId"]) for row in _json("learning/contracts/operation-matrix-v1.json")["operations"]}
    if api_rows != matrix_rows or len(api_rows) != 16:
        raise ValueError("OPENAPI_OPERATION_SET_MISMATCH")
    required = {"x-taxonomy", "x-process-role", "x-authority", "x-enforcement-status", "x-idempotency", "x-request-contract", "x-success-contract", "x-error-contracts", "responses"}
    for item in model["paths"].values():
        for operation in item.values():
            if not required.issubset(operation):
                raise ValueError("OPENAPI_OPERATION_CONTRACT_INCOMPLETE")
    inventory = list((ROOT / "contracts").rglob("*"))
    if any("asyncapi" in str(path).lower() for path in inventory):
        raise ValueError("ASYNCAPI_WITHOUT_CHANNEL")


def _run_tests() -> None:
    suite = unittest.defaultTestLoader.discover(str(ROOT / "tests/contracts/learning"), top_level_dir=str(ROOT))
    result = unittest.TextTestRunner(stream=sys.stderr, verbosity=1).run(suite)
    if not result.wasSuccessful() or result.testsRun < 79:
        raise ValueError("LEARNING_TEST_SUITE_FAILED")


def _source_identity() -> tuple[str, str]:
    source = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    tree = subprocess.check_output(["git", "rev-parse", "HEAD^{tree}"], cwd=ROOT, text=True).strip()
    return source, tree


def _emit(command_id: str, family: str, started: float) -> str:
    source, tree = _source_identity()
    run_id = secrets.token_hex(16)
    root = ROOT / ".artifacts/evidence" / family / run_id
    root.mkdir(parents=True, mode=0o700, exist_ok=False)
    os.chmod(root, 0o700)
    marker = {"schemaVersion": "learning-contract-owner-v1", "runId": run_id, "purpose": command_id, "nonce": secrets.token_hex(32)}
    (root / ".learning-contract-owner.json").write_text(json.dumps(marker, sort_keys=True, separators=(",", ":")) + "\n", encoding="utf-8")
    now = datetime.datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", "Z")
    payload = {"schemaVersion":"fitness-result-v2","commandId":command_id,"owner":"I5-03","requested":{"subjectType":"contract-release","subjectId":"issue-8-stage-a","parameters":[]},"status":"pass","failureCode":None,"remediation":None,"inputSha":INPUT_SHA,"testedTreeSha":tree,"dependencyMergeShas":["24be3b34c6b0fcdbd07c5800dcab349054e34713"],"contractHashes":[],"fixtureHashes":[{"name":"promotion-trust-manifest","sha256":"0a1dcd4023648f52009bfd4dc5d529c00ce66f42cd0e725732b972b0b78df341"}],"schemaHashes":[],"toolchain":[{"name":"python","version":"3.12.3"},{"name":"jsonschema","version":"4.26.0"},{"name":"rfc8785","version":"0.1.4"},{"name":"PyYAML","version":"6.0.3"}],"lockSha256":LOCK_SHA,"invocation":{"publicArgv":["make",command_id],"canonicalChildArgv":["python","-m","scripts.learning_contracts.check",command_id],"actualChildArgvSha256":None,"cwdRole":"repository-root"},"startedAt":now,"finishedAt":now,"durationMs":round((time.monotonic()-started)*1000),"rawLocator":None,"projectionLocator":None,"envelopeLocator":None,"projectionSha256":hashlib.sha256(tree.encode()).hexdigest(),"artifacts":[],"redactionClass":"sanitized","retentionClass":"immutable","rollback":{"status":"not-required","result":"released-contracts-retained"},"canonicalization":"rfc8785-jcs-v1","sourceSha":source}
    payload["payloadSha256"] = hashlib.sha256(canonical.dumps(payload)).hexdigest()
    result_path = root / "result.json"
    fd = os.open(result_path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
    try:
        os.write(fd, json.dumps(payload, sort_keys=True, separators=(",", ":")).encode() + b"\n"); os.fsync(fd)
    finally:
        os.close(fd)
    if sum(path.stat().st_size for path in root.rglob("*") if path.is_file()) > 256 * 1024 * 1024:
        raise ValueError("RESOURCE_STORAGE_LIMIT")
    return f"{family}/{run_id}/result.json"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=public_surface()[0])
    parser.add_argument("--lesson", default="")
    parser.add_argument("--evidence", default="")
    args = parser.parse_args(argv)
    started = time.monotonic()
    try:
        if args.command == "evidence-verify":
            if not args.evidence:
                raise ValueError("EVIDENCE_ARGUMENT_REQUIRED")
            value = evidence.verify_result_bytes(evidence.read_descriptor_bound(ROOT / ".artifacts/evidence", args.evidence))
            if fitness.code(value) != "OK":
                raise ValueError("FITNESS_RESULT_OWNER_VERSION_MISMATCH")
            print(f"evidence-verify: pass locator={args.evidence}")
            return 0
        if args.command == "lesson-check" and args.lesson != "promotion-trust":
            raise ValueError("LESSON_ARGUMENT_INVALID")
        if args.command == "api-contracts-check":
            _validate_openapi(); locator = _emit(args.command, "api-contracts", started)
        else:
            _validate_release(); _run_tests()
            if args.command == "lesson-check":
                manifest = _json("learning/manifests/promotion-trust-v1.json")
                if manifest["decision"] != "insufficient-evidence/no-common-grain":
                    raise ValueError("PROMOTION_MANIFEST_INVALID")
            locator = _emit(args.command, "learning-contracts", started)
        print(f"{args.command}: pass EVIDENCE_LOCATOR={locator}")
        return 0
    except (OSError, ValueError, json.JSONDecodeError, yaml.YAMLError) as exc:
        print(str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
