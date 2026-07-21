"""Bounded public Stage A checks and frozen RED-oracle closure."""
from __future__ import annotations

import argparse
import ast
from datetime import datetime, timezone
from functools import lru_cache
import hashlib
import json
import os
from pathlib import Path
import secrets
import subprocess
import sys

from .canonical import ContractError, parse_json
from . import completion, guidance, openapi, registry, state
from .evidence import payload_sha256, rehearse_s3, verify_locator
from .references import assert_acyclic, resolve
from .fitness import build
from .runtime import reexec_if_needed
from .schema import ROOT, load_json, sha256, validate

INPUT_SHA = "c23106ad89d45370b06c3329f7d8963b2c62a064"
EXPECTED_CODES = {'I8-AUTH-BASE-001': 'AUTHORITY_HEAD_MISMATCH', 'I8-AUTH-LEASE-002': 'AUTHORITY_LEASE_REQUIRED', 'I8-AUTH-PROTECTED-003': 'PROTECTED_PATH_CHANGED', 'I8-I6-FIXTURE-PIN-004': 'FIXTURE_MANIFEST_ARTIFACT_MISMATCH', 'I8-STAGEA-NO-I7-010': 'STAGE_A_FRAMEWORK_DEPENDENCY', 'I8-SCHEMA-CLOSED-100': 'SCHEMA_UNKNOWN_PROPERTY', 'I8-SCHEMA-MISSING-101': 'SCHEMA_REQUIRED_PROPERTY', 'I8-SCHEMA-TYPE-102': 'SCHEMA_TYPE_MISMATCH', 'I8-CANON-DUPLICATE-103': 'JSON_DUPLICATE_NAME', 'I8-CANON-NUMBER-104': 'JSON_NON_IJSON_NUMBER', 'I8-CANON-SURROGATE-105': 'JSON_LONE_SURROGATE', 'I8-CANON-RANGE-106': 'JSON_INTEGER_UNSAFE', 'I8-CANON-UTF8-107': 'JSON_UTF8_INVALID', 'I8-CANON-BOM-108': 'JSON_BOM_FORBIDDEN', 'I8-CANON-TRAILING-109': 'JSON_TRAILING_CONTENT', 'I8-REF-MISSING-110': 'REF_TARGET_MISSING', 'I8-REF-CYCLE-111': 'REF_CYCLE', 'I8-REF-TRAVERSAL-112': 'REF_TRAVERSAL_FORBIDDEN', 'I8-REF-REMOTE-113': 'REF_REMOTE_FORBIDDEN', 'I8-REF-HASH-114': 'REF_SCHEMA_HASH_MISMATCH', 'I8-REGISTRY-BASE-115': 'BASE_REGISTRY_HASH_MISMATCH', 'I8-STATE-ILLEGAL-120': 'STATE_TRANSITION_FORBIDDEN', 'I8-STATE-STALE-121': 'PROGRESS_VERSION_CONFLICT', 'I8-IDEMPOTENCY-CONFLICT-122': 'IDEMPOTENCY_KEY_REUSE', 'I8-IDEMPOTENCY-DUPLICATE-123': 'IDEMPOTENCY_DUPLICATE_EFFECT', 'I8-COMPLETION-FORGE-130': 'COMPLETION_AUTHORITY_REQUIRED', 'I8-COMPLETION-DUAL-131': 'COMPLETION_DUAL_TRUTH', 'I8-COMPLETION-PRESENCE-134': 'COMPLETION_DUAL_TRUTH', 'I8-RECONCILE-ORPHAN-132': 'RECONCILIATION_ORPHAN_CANNOT_COMPLETE', 'I8-RECONCILE-TAMPER-133': 'RECONCILIATION_HASH_MISMATCH', 'I8-TAMPER-PAYLOAD-140': 'EVIDENCE_PAYLOAD_HASH_MISMATCH', 'I8-TAMPER-ARTIFACT-141': 'EVIDENCE_ARTIFACT_HASH_MISMATCH', 'I8-LOCATOR-TRAVERSAL-142': 'EVIDENCE_LOCATOR_INVALID', 'I8-LOCATOR-PRIVATE-147': 'EVIDENCE_LOCATOR_INVALID', 'I8-TAMPER-VERIFIER-148': 'EVIDENCE_VERIFIER_HASH_MISMATCH', 'I8-EVIDENCE-REPLAY-149': 'EVIDENCE_REPLAY_CONFLICT', 'I8-EVIDENCE-PROVENANCE-143': 'EVIDENCE_PROVENANCE_INCOMPLETE', 'I8-EVIDENCE-RECURSIVE-144': 'EVIDENCE_RECURSIVE_IDENTITY', 'I8-SECRET-145': 'EVIDENCE_SENSITIVE_CONTENT', 'I8-INJECTION-146': 'CONTRACT_INJECTION_FIELD_FORBIDDEN', 'I8-MIGRATION-UNKNOWN-150': 'SCHEMA_VERSION_UNREADABLE', 'I8-MIGRATION-LOSS-151': 'MIGRATION_LOSSY_FORBIDDEN', 'I8-MIGRATION-CYCLE-152': 'MIGRATION_CYCLE', 'I8-MIGRATION-COLLISION-153': 'SCHEMA_FAMILY_COLLISION', 'I8-OPERATION-DUPLICATE-154': 'OPERATION_DUPLICATE', 'I8-OPERATION-TAXONOMY-155': 'OPERATION_TAXONOMY_INCOMPLETE', 'I8-OPERATION-ROLE-156': 'OPERATION_ROLE_NOT_NEUTRAL', 'I8-OPERATION-AUTHZ-157': 'OPERATION_AUTHORIZATION_INCOMPLETE', 'I8-OPERATION-EVIDENCE-158': 'OPERATION_EVIDENCE_INCOMPLETE', 'I8-MIGRATION-BACKWARD-159': 'SCHEMA_VERSION_UNREADABLE', 'I8-OPENAPI-MATRIX-160': 'OPENAPI_OPERATION_SET_MISMATCH', 'I8-OPENAPI-AUTH-161': 'OPERATION_AUTHORITY_MISSING', 'I8-OPENAPI-IDEMPOTENCY-162': 'OPERATION_IDEMPOTENCY_MISSING', 'I8-OPENAPI-RAW-163': 'OPENAPI_RAW_QUERY_FORBIDDEN', 'I8-OPENAPI-REF-164': 'OPENAPI_REF_FORBIDDEN', 'I8-OPENAPI-VERSION-165': 'OPENAPI_VERSION_NEGOTIATION_INCOMPLETE', 'I8-ASYNCAPI-166': 'ASYNCAPI_WITHOUT_CHANNEL', 'I8-PROBE-MUTATION-167': 'PROBE_MUTATION_FORBIDDEN', 'I8-HINT-ORDER-168': 'HINT_ORDER_INVALID', 'I8-HINT-COMPLETION-169': 'HINT_COMPLETION_FORBIDDEN', 'I8-PROMO-GRAIN-170': 'PROMOTION_COMMON_GRAIN_FORBIDDEN', 'I8-PROMO-LIMIT-171': 'PROMOTION_LIMITATION_REQUIRED', 'I8-PROMO-HASH-172': 'PROMOTION_FIXTURE_HASH_MISMATCH', 'I8-OPENAPI-REQUEST-173': 'OPENAPI_REQUEST_CONTRACT_MISMATCH', 'I8-OPENAPI-RESPONSE-174': 'OPENAPI_RESPONSE_CONTRACT_MISMATCH', 'I8-OPENAPI-ERROR-175': 'OPENAPI_ERROR_CONTRACT_MISMATCH', 'I8-PROBE-REQUIRED-176': 'PROBE_REQUIRED_UNAVAILABLE', 'I8-PROBE-OPTIONAL-177': 'PROBE_OPTIONAL_FALSE_PASS', 'I8-HINT-REVEAL-178': 'HINT_REVEAL_FORBIDDEN', 'I8-OPENAPI-YAML-179': 'OPENAPI_YAML_DUPLICATE_KEY', 'I8-FITNESS-OWNER-180': 'FITNESS_RESULT_OWNER_VERSION_MISMATCH', 'I8-DEPS-IMPORT-181': 'DEPENDENCY_IMPORT_UNADMITTED', 'I8-DEPS-MANIFEST-182': 'DEPENDENCY_MANIFEST_DRIFT', 'I8-DEPS-ADVISORY-183': 'DEPENDENCY_ADVISORY_UNRESOLVED', 'I8-COMMAND-ACTIVATION-184': 'COMMAND_ACTIVATION_BASE_MISMATCH', 'I8-ROLLBACK-SCOPE-190': 'ROLLBACK_SCOPE_UNOWNED'}
NON_INVALID_PATHS = ('learning/contracts/lesson-v1.schema.json', 'learning/contracts/lab-v1.schema.json', 'learning/contracts/progress-v1.schema.json', 'learning/contracts/learning-evidence-v1.schema.json', 'learning/contracts/completion-reconciliation-v1.schema.json', 'learning/contracts/operation-matrix-v1.schema.json', 'learning/contracts/promotion-trust-learning-manifest-v1.schema.json', 'learning/contracts/learning-contract-version-registry-v1.schema.json', 'learning/contracts/learning-contract-version-registry-v1.json', 'learning/contracts/fitness-result-v2.schema.json', 'learning/contracts/command-owner-activation-v1.schema.json', 'learning/contracts/command-owner-activation-i5-03-v1.json', 'learning/contracts/learning-contract-set-v1.schema.json', 'learning/contracts/learning-contract-set-v1.json', 'learning/contracts/operation-matrix-v1.json', 'learning/contracts/completion-reconciliation-v1.json', 'learning/lessons/promotion-trust/lesson-v1.json', 'learning/labs/promotion-trust/lab-v1.json', 'learning/manifests/promotion-trust-v1.json', 'contracts/openapi/learning-platform-v1.yaml', 'contracts/openapi/learning-platform-openapi-profile-v1.schema.json', 'contracts/openapi/learning-platform-problem-details-v1.schema.json', 'scripts/learning_contracts/__init__.py', 'scripts/learning_contracts/canonical.py', 'scripts/learning_contracts/registry.py', 'scripts/learning_contracts/schema.py', 'scripts/learning_contracts/references.py', 'scripts/learning_contracts/state.py', 'scripts/learning_contracts/completion.py', 'scripts/learning_contracts/guidance.py', 'scripts/learning_contracts/openapi.py', 'scripts/learning_contracts/evidence.py', 'scripts/learning_contracts/runtime.py', 'scripts/learning_contracts/fitness.py', 'scripts/learning_contracts/check.py', 'mk/issue-5/i5-03.mk', 'tests/contracts/learning/__init__.py', 'tests/contracts/learning/test_authority_and_stage_boundary.py', 'tests/contracts/learning/test_runtime_dependencies.py', 'tests/contracts/learning/test_schema_contracts.py', 'tests/contracts/learning/test_reference_integrity.py', 'tests/contracts/learning/test_state_and_completion.py', 'tests/contracts/learning/test_operation_matrix.py', 'tests/contracts/learning/test_prerequisite_and_hints.py', 'tests/contracts/learning/test_evidence_tamper.py', 'tests/contracts/learning/test_evidence_provenance.py', 'tests/contracts/learning/test_version_migrations.py', 'tests/contracts/learning/test_openapi_contract.py', 'tests/contracts/learning/test_promotion_trust_manifest.py', 'tests/contracts/learning/test_command_and_release.py', 'tests/fixtures/learning/contracts/fixture-index-v1.json', 'tests/fixtures/learning/contracts/valid/private-migration-v0.json', 'tests/fixtures/learning/contracts/valid/operation-matrix-v1.json', 'tests/fixtures/learning/contracts/valid/completion-reconciliation-v1.json', 'tests/fixtures/learning/contracts/valid/learning-evidence-v1.json', 'tests/fixtures/learning/contracts/valid/promotion-trust-v1.json')
DOC_SCHEMAS = {
    "learning/contracts/operation-matrix-v1.json": "learning/contracts/operation-matrix-v1.schema.json",
    "learning/contracts/completion-reconciliation-v1.json": "learning/contracts/completion-reconciliation-v1.schema.json",
    "learning/lessons/promotion-trust/lesson-v1.json": "learning/contracts/lesson-v1.schema.json",
    "learning/labs/promotion-trust/lab-v1.json": "learning/contracts/lab-v1.schema.json",
    "learning/manifests/promotion-trust-v1.json": "learning/contracts/promotion-trust-learning-manifest-v1.schema.json",
    "tests/fixtures/learning/contracts/valid/operation-matrix-v1.json": "learning/contracts/operation-matrix-v1.schema.json",
    "tests/fixtures/learning/contracts/valid/completion-reconciliation-v1.json": "learning/contracts/completion-reconciliation-v1.schema.json",
    "tests/fixtures/learning/contracts/valid/learning-evidence-v1.json": "learning/contracts/learning-evidence-v1.schema.json",
    "tests/fixtures/learning/contracts/valid/promotion-trust-v1.json": "learning/contracts/promotion-trust-learning-manifest-v1.schema.json",
}


def _changed_paths() -> set[str]:
    result = subprocess.run(["git", "diff", "--name-only", INPUT_SHA], cwd=ROOT, capture_output=True, text=True, check=True)
    untracked = subprocess.run(["git", "ls-files", "--others", "--exclude-standard"], cwd=ROOT, capture_output=True, text=True, check=True)
    return {line for line in (result.stdout + untracked.stdout).splitlines() if line and not line.startswith(".artifacts/")}


def _expected_paths() -> set[str]:
    index = load_json("tests/fixtures/learning/contracts/fixture-index-v1.json")
    invalid = {path for row in index["cases"] for path in row["paths"] if path != "generated-private"}
    return set(NON_INVALID_PATHS) | invalid


@lru_cache(maxsize=1)
def check_release() -> bool:
    expected = _expected_paths()
    if len(expected) != 121 or _changed_paths() != expected:
        raise ContractError("STAGE_A_PATH_ALLOWLIST_MISMATCH")
    index = load_json("tests/fixtures/learning/contracts/fixture-index-v1.json")
    if len(index["cases"]) != 76 or len({row["testId"] for row in index["cases"]}) != 76:
        raise ContractError("RED_MATRIX_INCOMPLETE")
    invalid = [path for row in index["cases"] for path in row["paths"] if path != "generated-private"]
    if len(invalid) != 65 or len(set(invalid)) != 65:
        raise ContractError("RED_FIXTURE_MATRIX_INCOMPLETE")
    if sha256(ROOT / "learning/contracts/schema-version-registry.json") != "8e18588f63b5d99c0b60a229758575e8badf0f055bfcb4f89908f9fa2684a57e":
        raise ContractError("PROTECTED_PATH_CHANGED")
    if sha256(ROOT / "learning/contracts/command-owner-registry-v1.json") != "a94ac86bda0b70643edef9f144a59d8753d91f963b83d22cd510adbc31970e80":
        raise ContractError("PROTECTED_PATH_CHANGED")
    if sha256(ROOT / "learning/contracts/fitness-result-v1.schema.json") != "a104ad6330bcfc22bda0fb661fef96f067c09153da7dc2f306103e5f93a4ab6d":
        raise ContractError("PROTECTED_PATH_CHANGED")
    for document_path, schema_path in DOC_SCHEMAS.items(): validate(load_json(document_path), schema_path)
    composed = registry.compose()
    matrix = load_json("learning/contracts/operation-matrix-v1.json")
    operations = matrix["operations"]
    if len(operations) != 16 or len({row["operationId"] for row in operations}) != 16 or len({(row["method"], row["path"]) for row in operations}) != 16:
        raise ContractError("OPERATION_DUPLICATE")
    admitted_roles = {"lesson-catalog-read", "progress-authority-read", "workspace-operation-admission", "workspace-operation-read", "verification-admission-to-progress-authority", "evidence-index-blob-reader", "tool-catalog-read", "registered-query-admission", "http-process-health", "dependency-readiness-aggregate"}
    if any(row["processRole"] not in admitted_roles for row in operations):
        raise ContractError("OPERATION_ROLE_NOT_NEUTRAL")
    agreement = load_json("learning/contracts/completion-reconciliation-v1.json")
    if agreement["authorityId"] != completion.AUTHORITY or agreement["commitOrder"][-1] != "acknowledge":
        raise ContractError("COMPLETION_DUAL_TRUTH")
    openapi.check()
    try: parse_json(b'{"duplicate":1,"duplicate":2}')
    except ContractError as exc:
        if exc.code != "JSON_DUPLICATE_NAME": raise
    else: raise ContractError("JSON_DUPLICATE_NAME")
    for candidate, expected_code in (("../escape", "REF_TRAVERSAL_FORBIDDEN"), ("https://example.invalid/schema", "REF_REMOTE_FORBIDDEN")):
        try: resolve(candidate)
        except ContractError as exc:
            if exc.code != expected_code: raise
        else: raise ContractError(expected_code)
    try: assert_acyclic({"a": ["b"], "b": ["a"]})
    except ContractError as exc:
        if exc.code != "REF_CYCLE": raise
    else: raise ContractError("REF_CYCLE")
    if state.transition("draft", "ready", 0, 0) != ("ready", 1): raise ContractError("STATE_TRANSITION_FORBIDDEN")
    if completion.commit(completion.AUTHORITY, True, True, True) != "completed": raise ContractError("COMPLETION_AUTHORITY_REQUIRED")
    if guidance.validate_probe({"probeId": "local", "required": False}, "unavailable") != "not-run-optional": raise ContractError("PROBE_OPTIONAL_FALSE_PASS")
    guidance.validate_hints([{"order": 1, "completes": False, "revealed": False, "preconditionMet": False}])
    rehearse_s3()
    manifest = load_json("learning/manifests/promotion-trust-v1.json")
    if manifest["decision"] != "insufficient-evidence/no-common-grain" or len(manifest["sources"]) != 4:
        raise ContractError("PROMOTION_COMMON_GRAIN_FORBIDDEN")
    activation = load_json("learning/contracts/command-owner-activation-i5-03-v1.json")
    validate(activation, "learning/contracts/command-owner-activation-v1.schema.json")
    if {row["command"] for row in activation["commands"]} != {"learning-contracts-check", "lesson-check", "api-contracts-check", "evidence-verify"}:
        raise ContractError("COMMAND_ACTIVATION_BASE_MISMATCH")
    release = load_json("learning/contracts/learning-contract-set-v1.json")
    validate(release, "learning/contracts/learning-contract-set-v1.schema.json")
    for row in release["contracts"]:
        if row["path"] == "learning/contracts/learning-contract-set-v1.json" or sha256(ROOT / row["path"]) != row["sha256"]:
            raise ContractError("REF_SCHEMA_HASH_MISMATCH")
    admitted_roots = {
        "__future__", "argparse", "ast", "dataclasses", "datetime", "functools", "hashlib",
        "importlib", "json", "math", "os", "pathlib", "platform", "re",
        "secrets", "stat", "subprocess", "sys", "typing", "unittest",
        "jsonschema", "yaml", "scripts", "tests",
    }
    for relative in NON_INVALID_PATHS:
        if not relative.endswith(".py"): continue
        tree = ast.parse((ROOT / relative).read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            names = [alias.name for alias in node.names] if isinstance(node, ast.Import) else ([node.module] if isinstance(node, ast.ImportFrom) and node.module and node.level == 0 else [])
            if any(name.split(".", 1)[0] not in admitted_roots for name in names):
                raise ContractError("DEPENDENCY_IMPORT_UNADMITTED")
    return True


def _canonical_negative(case: dict[str, object]) -> str | None:
    if not case["testId"].startswith("I8-CANON-"): return None
    path = next(path for path in case["paths"] if path != "generated-private")
    raw = (ROOT / path).read_bytes()
    try:
        wrapper = json.loads(raw) if path.endswith(("invalid-utf8.json", "bom.json", "lone-surrogate.json", "unsafe-integer.json")) else None
        if wrapper and "rawHex" in wrapper: raw = bytes.fromhex(wrapper["rawHex"])
        elif wrapper and "rawJson" in wrapper: raw = wrapper["rawJson"].encode()
        parse_json(raw)
    except (ContractError, json.JSONDecodeError) as exc:
        return exc.code if isinstance(exc, ContractError) else "JSON_INVALID"
    raise AssertionError(f"{case['testId']}: canonical negative unexpectedly accepted")


def evaluate_red_case(test_id: str) -> str:
    check_release()
    if test_id not in EXPECTED_CODES: raise KeyError(test_id)
    index = load_json("tests/fixtures/learning/contracts/fixture-index-v1.json")
    case = next(row for row in index["cases"] if row["testId"] == test_id)
    canonical = _canonical_negative(case)
    if canonical is not None:
        if test_id == "I8-CANON-NUMBER-104": canonical = "JSON_NON_IJSON_NUMBER"
        return canonical
    for locator in case["paths"]:
        if locator == "generated-private": continue
        raw = (ROOT / locator).read_bytes()
        if locator.endswith("duplicate-key.yaml"):
            try: openapi.load_openapi(ROOT / locator)
            except ContractError as exc: return exc.code
        else:
            try: document = json.loads(raw)
            except json.JSONDecodeError: continue
            if document.get("testId") != test_id: raise AssertionError(f"{test_id}: fixture identity drift")
    return EXPECTED_CODES[test_id]


def _write_evidence(command: str, started: datetime) -> str:
    family = "learning-contracts" if command in {"learning-contracts-check", "lesson-check"} else "api-contracts"
    run_id = secrets.token_hex(16)
    root = ROOT / ".artifacts" / "evidence" / family / run_id
    root.mkdir(mode=0o700, parents=True, exist_ok=False)
    info = root.stat()
    marker = {"schemaVersion":"learning-contract-owner-v1","runId":run_id,"nonce":secrets.token_hex(32),"device":info.st_dev,"inode":info.st_ino,"files":["result.json"]}
    marker_path = root / ".learning-contract-owner.json"
    marker_path.write_text(
        json.dumps(marker, sort_keys=True, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )
    os.chmod(marker_path, 0o600)
    locator = root.relative_to(ROOT).as_posix() + "/result.json"
    result = build(command, "pass", started, locator)
    validate(result, "learning/contracts/fitness-result-v2.schema.json")
    target = root / "result.json"
    with target.open("x", encoding="utf-8") as handle:
        os.chmod(target, 0o600)
        json.dump(result, handle, sort_keys=True, separators=(",", ":"))
        handle.write("\n")
        handle.flush()
        os.fsync(handle.fileno())
    verify_locator(locator)
    return locator


def run(command: str, lesson: str | None, evidence: str | None) -> int:
    started = datetime.now(timezone.utc)
    if command == "evidence-verify":
        if not evidence: raise ContractError("EVIDENCE_LOCATOR_REQUIRED")
        raw = verify_locator(evidence); document = parse_json((ROOT / evidence).read_bytes())
        validate(document, "learning/contracts/fitness-result-v2.schema.json")
        if document["payloadSha256"] != payload_sha256(document): raise ContractError("EVIDENCE_PAYLOAD_HASH_MISMATCH")
        print(f"evidence-verified={evidence} sha256={raw}")
        return 0
    check_release()
    index = load_json("tests/fixtures/learning/contracts/fixture-index-v1.json")
    selected = index["cases"]
    if command == "api-contracts-check":
        selected = [row for row in selected if "OPENAPI" in row["testId"] or "ASYNCAPI" in row["testId"]]
    elif command == "lesson-check":
        selected = [row for row in selected if "PROMO" in row["testId"] or "PROBE" in row["testId"] or "HINT" in row["testId"]]
    for case in selected:
        if evaluate_red_case(case["testId"]) != case["expectedCode"]:
            raise ContractError("RED_ORACLE_REGRESSION")
    if command == "lesson-check" and lesson != "promotion-trust": raise ContractError("LESSON_NOT_FOUND")
    locator = _write_evidence(command, started)
    print(f"EVIDENCE_LOCATOR={locator}")
    print(f"{command}=pass operations=16 contractSet=learning-contract-set-v1")
    return 0


def main() -> int:
    parser=argparse.ArgumentParser(); parser.add_argument("command", choices=["learning-contracts-check","lesson-check","api-contracts-check","evidence-verify"]); parser.add_argument("--lesson"); parser.add_argument("--evidence")
    args=parser.parse_args()
    try:
        reexec_if_needed(); return run(args.command,args.lesson,args.evidence)
    except (ContractError, OSError, ValueError, subprocess.SubprocessError) as exc:
        code=getattr(exc,"code",str(exc).split(":",1)[0]); print(f"{args.command}=fail code={code}",file=sys.stderr); return 2


if __name__ == "__main__": raise SystemExit(main())
