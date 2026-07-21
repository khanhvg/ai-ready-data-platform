#!/usr/bin/env python3
"""Pure non-recursive fixture handoff checks and C1-derived publication."""
from __future__ import annotations
import hashlib, json, pathlib, re
from typing import Iterable,Any
import jsonschema, rfc8785

ROOT=pathlib.Path(__file__).resolve().parents[2]
FOUR_HANDOFF_PATHS=("contracts/data/retail-golden-v1.json","contracts/data/promotion-trust-v1.yaml","tests/fixtures/learning/promotion-trust/evidence-v1.json","tests/fixtures/learning/promotion-trust/manifest.json")
INVALID_PATHS=tuple(f"tests/fixtures/learning/promotion-trust/invalid/canonicalization/{name}.json" for name in ("duplicate-name","nan","positive-infinity","negative-infinity","lone-surrogate","negative-zero-decimal"))
AUTHORIZED_FIXTURE_PATHS=(FOUR_HANDOFF_PATHS[2],FOUR_HANDOFF_PATHS[3],*INVALID_PATHS)
CORE_FILES=("raw.json","projection.json","envelope.json","result.json","run-metadata.json")
PORTABLE_SCHEMA=ROOT/"learning/contracts/promotion-trust-portable-run-attestation-v1.schema.json"
class FixtureError(ValueError): pass
def validate_nonrecursive(value:Any)->None:
    text=json.dumps(value,sort_keys=True)
    if any(term in text for term in ("attestationCommitSha","mergeOrTagSha","manifestSha256","selfSha256")): raise FixtureError("FIXTURE_RECURSIVE_IDENTITY")
def invalidates_issue7(before:dict[str,str],after:dict[str,str])->bool: return before!=after or set(before)!=set(FOUR_HANDOFF_PATHS) or set(after)!=set(FOUR_HANDOFF_PATHS)
def validate_staged_paths(paths:Iterable[str])->None:
    if any(path not in AUTHORIZED_FIXTURE_PATHS for path in paths): raise FixtureError("FIXTURE_PATH_UNAUTHORIZED")
def sha(path:pathlib.Path)->str: return hashlib.sha256(path.read_bytes()).hexdigest()
def verify_fixture(value:dict[str,Any])->None:
    integrity=value.get("integrity",{}); payload={key:child for key,child in value.items() if key!="integrity"}
    if hashlib.sha256(rfc8785.dumps(payload)).hexdigest()!=integrity.get("payloadSha256"): raise FixtureError("FIXTURE_PAYLOAD_HASH_MISMATCH")

def portable_attestation_payload_sha256(value:dict[str,Any])->str:
    payload={key:child for key,child in value.items() if key!="integrity"}
    return hashlib.sha256(rfc8785.dumps(payload)).hexdigest()

def _completion_bytes(run:dict[str,Any])->bytes:
    completion={"schemaVersion":"golden-run-completion-v1","runId":run["runId"],"artifacts":[{"locator":name,"sha256":run["coreSha256"][name]} for name in CORE_FILES]}
    return (json.dumps(completion,sort_keys=True,separators=(",",":"))+"\n").encode()

def verify_portable_attestation(value:dict[str,Any],expected_tested_tree_sha:str)->None:
    try: jsonschema.Draft202012Validator(json.loads(PORTABLE_SCHEMA.read_text())).validate(value)
    except (OSError,json.JSONDecodeError,jsonschema.ValidationError) as exc: raise FixtureError("PORTABLE_ATTESTATION_SCHEMA_INVALID") from exc
    if portable_attestation_payload_sha256(value)!=value["integrity"]["payloadSha256"]: raise FixtureError("PORTABLE_ATTESTATION_INTEGRITY_MISMATCH")
    if value["testedTreeSha"]!=expected_tested_tree_sha or any(run["testedTreeSha"]!=expected_tested_tree_sha for run in value["runs"]): raise FixtureError("PORTABLE_ATTESTATION_TESTED_TREE_MISMATCH")
    first,second=value["runs"]
    if first["runId"]==second["runId"]: raise FixtureError("PORTABLE_ATTESTATION_RUN_IDS_INVALID")
    if first["finishedMonotonicNs"]>second["startedMonotonicNs"]: raise FixtureError("PORTABLE_ATTESTATION_RUN_ORDER_INVALID")
    for run in value["runs"]:
        duration=(run["finishedMonotonicNs"]-run["startedMonotonicNs"])//1_000_000
        if run["finishedMonotonicNs"]<run["startedMonotonicNs"] or run["durationMs"]!=duration or duration>300_000: raise FixtureError("PORTABLE_ATTESTATION_TIMING_INVALID")
        if hashlib.sha256(_completion_bytes(run)).hexdigest()!=run["completionSha256"] or run["projectionSha256"]!=run["coreSha256"]["projection.json"]: raise FixtureError("PORTABLE_ATTESTATION_CORE_IDENTITY_MISMATCH")
    pair_duration=(second["finishedMonotonicNs"]-first["startedMonotonicNs"])//1_000_000
    if value["timing"]["pairDurationMs"]!=pair_duration or pair_duration>600_000: raise FixtureError("PORTABLE_ATTESTATION_TIMING_INVALID")
    if first["projectionSha256"]!=second["projectionSha256"] or first["normalizedRawSha256"]!=second["normalizedRawSha256"]: raise FixtureError("PORTABLE_ATTESTATION_EQUALITY_MISMATCH")

def portable_attestation_document(first:Any,second:Any,tested_tree_sha:str)->dict[str,Any]:
    def run_record(bundle:Any)->dict[str,Any]:
        return {"runId":bundle.run_id,"testedTreeSha":bundle.tested_tree_sha,"startedMonotonicNs":bundle.metadata["startedMonotonicNs"],"finishedMonotonicNs":bundle.metadata["finishedMonotonicNs"],"durationMs":bundle.metadata["durationMs"],"completionSha256":bundle.completion_sha256,"coreSha256":bundle.core_sha256,"projectionSha256":hashlib.sha256(bundle.projection_bytes).hexdigest(),"normalizedRawSha256":hashlib.sha256(bundle.normalized_raw_bytes).hexdigest()}
    first_record,second_record=run_record(first),run_record(second)
    pair_duration=(second_record["finishedMonotonicNs"]-first_record["startedMonotonicNs"])//1_000_000
    value={"schemaVersion":"promotion-trust-portable-run-attestation-v1","testedTreeSha":tested_tree_sha,"sourceBundleVerification":"strict-owner-bound-at-publication","runs":[first_record,second_record],"timing":{"runsSequential":True,"pairDurationMs":pair_duration,"maxRunDurationMs":300_000,"maxPairDurationMs":600_000},"equality":{"projection":"exact","normalizedRaw":"exact"},"integrityScope":"local-artifact-integrity-only","publisherAuthenticity":"externally-attested-not-claimed"}
    value["integrity"]={"canonicalization":"rfc8785-jcs-v1","algorithm":"sha-256","payloadSha256":portable_attestation_payload_sha256(value)}
    verify_portable_attestation(value,tested_tree_sha); return value

def manifest_document(evidence:dict[str,Any],tested_tree_sha:str,portable_attestation:dict[str,Any])->dict[str,Any]:
    verify_fixture(evidence); verify_portable_attestation(portable_attestation,tested_tree_sha)
    payload=(json.dumps(evidence,ensure_ascii=False,sort_keys=True,separators=(",",":"))+"\n").encode()
    artifact_paths=("contracts/data/retail-golden-v1.json","contracts/data/promotion-trust-v1.yaml","learning/contracts/promotion-trust-evidence-v1.schema.json","learning/contracts/promotion-trust-fixture-manifest-v1.schema.json","learning/contracts/promotion-trust-fixture-manifest-v2.schema.json","learning/contracts/promotion-trust-portable-run-attestation-v1.schema.json","learning/contracts/schema-version-registry.json")
    artifacts=[{"locator":path,"byteLength":(ROOT/path).stat().st_size,"sha256":hashlib.sha256((ROOT/path).read_bytes()).hexdigest()} for path in artifact_paths]
    manifest={"schemaVersion":"promotion-trust-fixture-manifest-v2","fixtureId":"promotion-trust-small-42-v1","contractId":"promotion-trust-v1","producerCommand":"make golden-clean PROFILE=small SEED=42","testedTreeSha":tested_tree_sha,"profile":"small","seed":42,"inputWindow":{"start":"2025-07-01","end":"2026-06-30"},"pythonLockSha256":"f41c727b39f99106f95b7937b2811e8d27db89d1d5106e9f1d9effd4403143d2","twoCleanRuns":"equal","portableRunAttestation":portable_attestation,"evidence":{"byteLength":len(payload),"sha256":hashlib.sha256(payload).hexdigest()},"artifacts":artifacts,"canonicalization":"rfc8785-jcs-v1","digestAlgorithm":"sha-256","redactionClass":"sanitized-synthetic-aggregate","publisherAuthenticity":"externally-attested-not-claimed","mergedIdentity":"absent-until-reviewed-remote-merge"}
    validate_nonrecursive(manifest); return manifest

def fixture_documents(projection:dict[str,Any],tested_tree_sha:str,portable_attestation:dict[str,Any])->tuple[dict[str,Any],dict[str,Any]]:
    promotion=projection["promotionTrust"]
    evidence={"schemaVersion":"promotion-trust-evidence-v1","contractId":"promotion-trust-v1","fixtureId":"promotion-trust-small-42-v1","fixtureKind":"tracked-real","dataClassification":"sanitized-synthetic-aggregate","profile":"small","seed":42,"inputWindow":{"start":"2025-07-01","end":"2026-06-30","scope":"generated-input-domain-not-mart-predicate"},"sources":promotion["sources"],"assertions":["PTV1-GRAIN-PROMOTION","PTV1-GRAIN-FULFILLMENT","PTV1-GRAIN-RETURNS","PTV1-GRAIN-DATA-QUALITY","PTV1-HEADLINE-SUFFICIENT","PTV1-NO-CROSS-GRAIN-JOIN","PTV1-NO-ATTRIBUTION","PTV1-DECISION-INSUFFICIENT-EVIDENCE"],"decision":{"value":"insufficient-evidence","reason":"no-common-grain"},"limitations":["four independent grains cannot support cross-source attribution","aggregate synthetic evidence only"]}
    evidence["integrity"]={"canonicalization":"rfc8785-jcs-v1","algorithm":"sha-256","payloadSha256":hashlib.sha256(rfc8785.dumps(evidence)).hexdigest()}
    verify_fixture(evidence)
    validate_nonrecursive(evidence)
    return evidence,manifest_document(evidence,tested_tree_sha,portable_attestation)
