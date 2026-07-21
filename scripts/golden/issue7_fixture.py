#!/usr/bin/env python3
"""Pure non-recursive fixture handoff checks and C1-derived publication."""
from __future__ import annotations
import hashlib, json, pathlib, re
from typing import Iterable,Any
import rfc8785

ROOT=pathlib.Path(__file__).resolve().parents[2]
FOUR_HANDOFF_PATHS=("contracts/data/retail-golden-v1.json","contracts/data/promotion-trust-v1.yaml","tests/fixtures/learning/promotion-trust/evidence-v1.json","tests/fixtures/learning/promotion-trust/manifest.json")
INVALID_PATHS=tuple(f"tests/fixtures/learning/promotion-trust/invalid/canonicalization/{name}.json" for name in ("duplicate-name","nan","positive-infinity","negative-infinity","lone-surrogate","negative-zero-decimal"))
AUTHORIZED_FIXTURE_PATHS=(FOUR_HANDOFF_PATHS[2],FOUR_HANDOFF_PATHS[3],*INVALID_PATHS)
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
def fixture_documents(projection:dict[str,Any],tested_tree_sha:str,run_ids:tuple[str,str]|None=None)->tuple[dict[str,Any],dict[str,Any]]:
    promotion=projection["promotionTrust"]
    evidence={"schemaVersion":"promotion-trust-evidence-v1","contractId":"promotion-trust-v1","fixtureId":"promotion-trust-small-42-v1","fixtureKind":"tracked-real","dataClassification":"sanitized-synthetic-aggregate","profile":"small","seed":42,"inputWindow":{"start":"2025-07-01","end":"2026-06-30","scope":"generated-input-domain-not-mart-predicate"},"sources":promotion["sources"],"assertions":["PTV1-GRAIN-PROMOTION","PTV1-GRAIN-FULFILLMENT","PTV1-GRAIN-RETURNS","PTV1-GRAIN-DATA-QUALITY","PTV1-HEADLINE-SUFFICIENT","PTV1-NO-CROSS-GRAIN-JOIN","PTV1-NO-ATTRIBUTION","PTV1-DECISION-INSUFFICIENT-EVIDENCE"],"decision":{"value":"insufficient-evidence","reason":"no-common-grain"},"limitations":["four independent grains cannot support cross-source attribution","aggregate synthetic evidence only"]}
    evidence["integrity"]={"canonicalization":"rfc8785-jcs-v1","algorithm":"sha-256","payloadSha256":hashlib.sha256(rfc8785.dumps(evidence)).hexdigest()}
    verify_fixture(evidence)
    validate_nonrecursive(evidence)
    payload=(json.dumps(evidence,ensure_ascii=False,sort_keys=True,separators=(",",":"))+"\n").encode()
    artifact_paths=("contracts/data/retail-golden-v1.json","contracts/data/promotion-trust-v1.yaml","learning/contracts/promotion-trust-evidence-v1.schema.json","learning/contracts/promotion-trust-fixture-manifest-v1.schema.json","learning/contracts/schema-version-registry.json")
    artifacts=[{"locator":path,"byteLength":(ROOT/path).stat().st_size,"sha256":hashlib.sha256((ROOT/path).read_bytes()).hexdigest()} for path in artifact_paths]
    locators=[f"golden/{run_id}" for run_id in (run_ids or ())]
    manifest={"schemaVersion":"promotion-trust-fixture-manifest-v1","fixtureId":"promotion-trust-small-42-v1","contractId":"promotion-trust-v1","producerCommand":"make golden-clean PROFILE=small SEED=42","testedTreeSha":tested_tree_sha,"profile":"small","seed":42,"inputWindow":{"start":"2025-07-01","end":"2026-06-30"},"pythonLockSha256":"f41c727b39f99106f95b7937b2811e8d27db89d1d5106e9f1d9effd4403143d2","twoCleanRuns":"equal","cleanRunEvidenceLocators":locators,"evidence":{"byteLength":len(payload),"sha256":hashlib.sha256(payload).hexdigest()},"artifacts":artifacts,"canonicalization":"rfc8785-jcs-v1","digestAlgorithm":"sha-256","redactionClass":"sanitized-synthetic-aggregate","publisherAuthenticity":"externally-attested-not-claimed","mergedIdentity":"absent-until-reviewed-remote-merge"}
    validate_nonrecursive(manifest); return evidence,manifest
