---
title: "Issue #8 Requirements and Risk Traceability"
status: pending
priority: P1
issue: 8
created: "2026-07-21"
---

# Issue #8 Requirements and Risk Traceability

## Accepted Sources

| Source | Immutable identity / locator | Contract carried forward |
|---|---|---|
| Issue #8 body/state | `https://github.com/khanhvg/ai-ready-data-platform/issues/8` observed OPEN at validation input with `ready for plan validation`, `risk:high`, `tdd`, `security:S3`, `shared-core`, `api` | Exclusive paths, tests-first order, three primary checks, evidence root, S3, migration/rollback, STOP rules |
| Owner parallelization decision | `https://github.com/khanhvg/ai-ready-data-platform/issues/5#issuecomment-5036142770` | Plan downstream lanes now; only fresh readiness may authorize a genuinely independent Stage A; single shared-contract writer |
| Planning input | `24be3b34c6b0fcdbd07c5800dcab349054e34713` | Shipped Issue #6 integration/handoff and exact read-only contract/fixture bytes |
| Master discovery | `plans/260721-005-enterprise-learning-sandbox/discovery/` at the input | PH-C02, PH-C05, PH-C06, PH-H06, PH-H11 and SC-01/02/03/06/14/16/19/20 |
| Normative lesson/lab contract | `plans/260721-005-enterprise-learning-sandbox/lesson-lab-contract.md` | Required lesson/lab fields, state machine, API operations, evidence, accessibility, remediation |
| Master Phase 3 | `plans/260721-005-enterprise-learning-sandbox/phase-03-shared-lesson-lab-and-evidence-contract.md` | TDD order, operation matrix, one completion authority, probes/hints, backward readers, no AsyncAPI without channel |
| Master implementation graph | `plans/260721-005-enterprise-learning-sandbox/implementation-issue-graph.md` | I5-03 dependencies/ownership, downstream blockers, exact target names, serialized release SHA |
| Master readiness | `e440c5855732d5d8f5d634e3cc1359c010cc5ed3` | Per-issue plan→independent validation→fresh audit, no master cook, mandatory human pre-merge approval |
| Issue #6 handoff | `plans/260721-006-freeze-golden-baseline/implementation-handoff.md` and shipped input tree | Strict I-JSON/JCS, schema registry/readers, fitness evidence, protected paths, additive migration |
| Issue #7 state | OPEN/unmerged at planning time; owner selected Vite in Issue #7 comment `5036142177` | Direction only. No accepted ADR or merged handoff SHA exists; Stage B stays blocked |
| OpenAPI authority | `https://spec.openapis.org/oas/v3.2.0.html` (published 2025-09-19) | OpenAPI 3.2.0 is real; the project profile validates only the exact offline subset used and does not claim to be a universal validator |

## End-to-End Traceability Coverage

| Layer | IDs / authority | Planned artifact | RED / contract proof | GREEN command and evidence |
|---|---|---|---|---|
| Outcome | Issue #8 acceptance; LC-001..025 | versioned learning contracts plus staged Vite binding | authority/stage-boundary RED | three-command primary gate; external release attestation |
| Capability | CAP-01 author/validate; CAP-02 progress/complete; CAP-03 prove evidence; CAP-04 expose HTTP; CAP-05 publish promotion-trust; CAP-06 evolve/rollback | schemas, pure validators, operation/completion documents, OpenAPI, manifests, registry/release set | I8-SCHEMA/STATE/COMPLETION/TAMPER/OPENAPI/PROMO/MIGRATION suites | learning/API/evidence results under bounded evidence roots |
| Functional requirements | FR-01..FR-12 mapped by LC-002..020 and LC-023..024 | exact files in the Stage A allow-list | stable test/fixture IDs below | exact primary and blast-radius commands |
| Non-functional requirements | NFR-01 closed/fail-safe; NFR-02 deterministic; NFR-03 offline; NFR-04 16 GiB; NFR-05 no new dependency; NFR-06 additive/backward; NFR-07 bounded/redacted; NFR-08 no cloud/heavy profile; NFR-09 framework-neutral; NFR-10 authority-gated | canonical profile, runtime/import manifest, protected hashes, rollback protocol | I8-CANON/DEPS/SECRET/ROLLBACK/STAGEA suites | lock/import scan, offline rerun, resource record, protected-path result |
| Architecture | ADR-003/007/017/018; execution-authority contract | logical taxonomy, one progress authority, synchronous polling, local-corruption-only evidence claim | matrix/dual-truth/no-channel/tamper RED | operation-set equality and reconciliation result |
| Contracts | lesson, lab, progress, learning-evidence, completion, operation matrix, promotion manifest, OpenAPI, fitness v2, registries, release set | closed Draft 2020-12/OpenAPI 3.2.0 documents | exact field/validator and fixture tables below | schema/ref/API/evidence/migration reports |
| Operations | 16 method/path/operationId rows from the normative lesson/lab contract | `operation-matrix-v1.json` + OpenAPI paths | missing/extra/auth/idempotency/version negatives | bidirectional set equality and per-row request/response coverage |
| Tests | TDD, property/mutation, fault injection, compatibility, dependency, rollback | tests/fixtures exact allow-list | Phase 1 captures all RED before behavior | focused suites then exact make blast radius |
| Evidence/operations | `fitness-result-v2` for I5-03; retained v1 for I5-01 | command results, learner evidence, contract set, external SHA attestations | owner/version mismatch and locator/hash negatives | one exact tested head, bounded locators/hashes, rollback and external review gates |

## Closed Contract Field Sets

All executable JSON objects use `required` plus `unevaluatedProperties: false` at every object
boundary; optionality is expressed by an explicitly named property, never by accepting unknown
fields. Array item objects are equally closed and have explicit size/uniqueness bounds.

| Family | Exact required top-level fields | Semantic invariants beyond JSON Schema |
|---|---|---|
| `lesson-v1` | `schemaVersion,id,version,title,summary,level,competencies,outcome,stakeholder,prerequisites,prerequisiteChecks,fr,nfr,asr,architectureViews,decision,patterns,narrativeSteps,lab,evidence,reflection,accessibility,remediation,hints` | stable/unique IDs; existing competency/view/ADR/lab/verifier/failure/remediation refs; prerequisite DAG; hint order; evidence threshold; no reflection/scroll completion |
| `lab-v1` | `schemaVersion,id,version,lessonId,risk,profile,inputs,workspace,commands,starter,controlledFailure,stateMachine,reset,verify,solution,evidence,accessibility,remediation` | typed bounded inputs; registered command IDs only; relative workspace locators; exact legal state graph; reset oracle; every failure remediated |
| `progress-v1` | `schemaVersion,progressId,actor,lessonId,lessonVersion,labId,labVersion,contractSetSha256,revision,state,events,completion` | monotonic integer revision; ordered unique events; state derived from legal transitions; `completion` is null or one authority-committed evidence/result reference, never browser/evidence presence |
| `learning-evidence-v1` | `schemaVersion,evidenceId,lesson,lab,actor,workspaceId,runId,operationId,inputGitSha,officialGoldenMainSha,dependencyMergeShas,contractHashes,fixtureHashes,verifier,environment,parameters,transitions,commands,assertions,artifacts,timing,redactionClass,retentionClass,rollback,integrity` | strict provenance; relative descriptor-bound locators; artifact size/hash; last committed verified run only; payload-only JCS digest; no recursive/self/merge identity or authenticity claim |
| `completion-reconciliation-v1` | `schemaVersion,authorityId,authorityVersion,idempotencyScope,commitPreconditions,commitOrder,uniqueConstraints,faultPoints,reconciliation,resets,conflicts` | `authorityId=learning-progress-authority-v1`; one CAS commit; deterministic attach/quarantine; no last-write-wins; no other writer emits completion |
| `operation-matrix-v1` | `schemaVersion,apiVersion,channels,operations` | `channels` is exactly `[]`; exactly the 16 normative method/path/operationId rows; unique IDs/pairs; complete taxonomy, process role, authn/authz/CSRF, idempotency, request, response, error and evidence metadata |
| `learning-contract-version-registry-v1` | `schemaVersion,baseRegistry,ownedFamilies,familyExtensions` | `baseRegistry={path:"learning/contracts/schema-version-registry.json",sha256:"8e18588f63b5d99c0b60a229758575e8badf0f055bfcb4f89908f9fa2684a57e"}`; disjoint owned families; exactly one extension `{family,baseReaderId,addedReadableVersions,migrations}` for `fitness-result`; v2 read/identity edge; v1 remains base-current/readable; no base-current, base-reader or emission-fallback mutation |
| `fitness-result-v2` | `schemaVersion,commandId,owner,requested,status,failureCode,remediation,inputSha,testedTreeSha,dependencyMergeShas,contractHashes,fixtureHashes,schemaHashes,toolchain,lockSha256,invocation,startedAt,finishedAt,durationMs,rawLocator,projectionLocator,envelopeLocator,projectionSha256,artifacts,redactionClass,retentionClass,rollback,canonicalization,payloadSha256` | `owner` and `commandId` must match one active hash-bound command row whose evidence version is v2; requested is closed `{subjectType,subjectId,parameters}` where parameters is a sorted unique bounded array of closed `{name,valueType,value}` scalar entries; invocation is closed `{publicArgv,canonicalChildArgv,actualChildArgvSha256,cwdRole}` and never persists a private absolute argv; toolchain and hash inventories are sorted arrays of closed name/hash or name/version entries; artifacts are closed `{locator,mediaType,size,sha256}`; locators are nullable or descriptor-safe relative; status/failure/rollback consistency; JCS payload digest excludes `payloadSha256` |
| `command-owner-activation-v1` | `schemaVersion,baseRegistryPath,baseRegistrySha256,owner,fragment,commands` | generic closed activation schema; every command must exactly match a reserved `future-owner` base row for the same owner/fragment and name one readable evidence version. The I5-03 instance contains exactly its four rows with `fitness-result-v2`; a later owner may add only an issue-owned activation instance, never edit this schema/base registry |
| `learning-contract-set-v1` | `schemaVersion,setId,registry,contracts` | exact sorted Stage A contract paths/family/version/schema/content hashes; no own byte hash, tested/merge SHA or mutable evidence locator |
| `promotion-trust-learning-manifest-v1` | `schemaVersion,manifestId,lesson,lab,evidenceSchema,dataContract,fixture,sources,decision,limitations,contractSetSha256` | four ordered independent grains; exact hashes; `insufficient-evidence/no-common-grain`; no cross-grain attribution |

## Ordered Validation and Canonicalization Contract

Validation order is normative and first failure wins: (1) descriptor-bound regular-file/size check;
(2) UTF-8, no BOM, one JSON document and no trailing data; (3) duplicate-name detection before map
creation; (4) I-JSON strings/numbers including no lone surrogate/non-finite/unsafe integer; (5)
Draft 2020-12 schema/meta-schema and closed-field validation; (6) local `$ref` containment/hash;
(7) semantic uniqueness/graph/state/operation/authority checks; (8) RFC 8785 canonical payload
bytes; (9) SHA-256 comparison. No coercion, default insertion, Unicode normalization, float/decimal
conversion, field stripping or YAML conversion is permitted for domain/evidence documents.

The OpenAPI YAML loader is the only YAML reader. It uses the locked `PyYAML 6.0.3` with a custom
safe loader that rejects duplicate keys, aliases/anchors/merge keys, tags, multiple documents,
non-JSON scalar resolution, BOM, trailing content and unsafe numbers before profile validation.
The normalized parsed OpenAPI model is hashed with the same JCS implementation; this digest is not
a substitute for validating the original YAML/profile semantics.

## Exact Stage A Implementation Allow-List

No unlisted tracked path may change. Every path is Issue #8-owned and every `Create` path must be
absent at the authorized input. There is no Stage A modification to a shipped Issue #6 path. The
Issue #8 registry overlay binds the immutable base-registry hash and carries the v2 extension.

| Action | Exact tracked paths |
|---|---|
| Create — schemas/registries | `learning/contracts/lesson-v1.schema.json`; `learning/contracts/lab-v1.schema.json`; `learning/contracts/progress-v1.schema.json`; `learning/contracts/learning-evidence-v1.schema.json`; `learning/contracts/completion-reconciliation-v1.schema.json`; `learning/contracts/operation-matrix-v1.schema.json`; `learning/contracts/promotion-trust-learning-manifest-v1.schema.json`; `learning/contracts/learning-contract-version-registry-v1.schema.json`; `learning/contracts/learning-contract-version-registry-v1.json`; `learning/contracts/fitness-result-v2.schema.json`; `learning/contracts/command-owner-activation-v1.schema.json`; `learning/contracts/command-owner-activation-i5-03-v1.json`; `learning/contracts/learning-contract-set-v1.schema.json`; `learning/contracts/learning-contract-set-v1.json` |
| Create — contract instances/content | `learning/contracts/operation-matrix-v1.json`; `learning/contracts/completion-reconciliation-v1.json`; `learning/lessons/promotion-trust/lesson-v1.json`; `learning/labs/promotion-trust/lab-v1.json`; `learning/manifests/promotion-trust-v1.json`; `contracts/openapi/learning-platform-v1.yaml`; `contracts/openapi/learning-platform-openapi-profile-v1.schema.json`; `contracts/openapi/learning-platform-problem-details-v1.schema.json` |
| Create — implementation | `scripts/learning_contracts/__init__.py`; `scripts/learning_contracts/canonical.py`; `scripts/learning_contracts/registry.py`; `scripts/learning_contracts/schema.py`; `scripts/learning_contracts/references.py`; `scripts/learning_contracts/state.py`; `scripts/learning_contracts/completion.py`; `scripts/learning_contracts/guidance.py`; `scripts/learning_contracts/openapi.py`; `scripts/learning_contracts/evidence.py`; `scripts/learning_contracts/runtime.py`; `scripts/learning_contracts/fitness.py`; `scripts/learning_contracts/check.py`; `mk/issue-5/i5-03.mk` |
| Create — tests | `tests/contracts/learning/__init__.py`; `tests/contracts/learning/test_authority_and_stage_boundary.py`; `tests/contracts/learning/test_runtime_dependencies.py`; `tests/contracts/learning/test_schema_contracts.py`; `tests/contracts/learning/test_reference_integrity.py`; `tests/contracts/learning/test_state_and_completion.py`; `tests/contracts/learning/test_operation_matrix.py`; `tests/contracts/learning/test_prerequisite_and_hints.py`; `tests/contracts/learning/test_evidence_tamper.py`; `tests/contracts/learning/test_evidence_provenance.py`; `tests/contracts/learning/test_version_migrations.py`; `tests/contracts/learning/test_openapi_contract.py`; `tests/contracts/learning/test_promotion_trust_manifest.py`; `tests/contracts/learning/test_command_and_release.py` |
| Create — valid fixtures | `tests/fixtures/learning/contracts/fixture-index-v1.json`; `tests/fixtures/learning/contracts/valid/private-migration-v0.json`; `tests/fixtures/learning/contracts/valid/operation-matrix-v1.json`; `tests/fixtures/learning/contracts/valid/completion-reconciliation-v1.json`; `tests/fixtures/learning/contracts/valid/learning-evidence-v1.json`; `tests/fixtures/learning/contracts/valid/promotion-trust-v1.json` |
| Create — invalid fixtures | Every exact repository path in the TDD RED table below; secret, PII, absolute-private-path and credential-like canaries are generated only in a marker-owned private test root and are never tracked |

Stage A planning may read only these master files:
`plans/260721-005-enterprise-learning-sandbox/lesson-lab-contract.md`,
`plans/260721-005-enterprise-learning-sandbox/phase-03-shared-lesson-lab-and-evidence-contract.md`,
`plans/260721-005-enterprise-learning-sandbox/execution-authority-and-release-contract.md`, and
`plans/260721-005-enterprise-learning-sandbox/implementation-issue-graph.md`; runtime checks
do not read plans. Stage A implementation may read only Issue #6 paths named in its shipped handoff,
`Makefile`, `mk/issue-5/i5-01.mk`, the frozen golden requirements/metadata, and standard Git metadata
needed for exact-head/ancestry checks. Runtime repository imports are limited to these public names,
whose definitions/signatures exist at the exact input: `scripts.golden.canonical` —
`CanonicalizationError`, `parse_json`, `dumps`; `scripts.golden.dependency_lock` — `LockError`,
`platform_preflight`, `verify_lock`; `scripts.golden.runtime` — `RuntimeErrorTyped`,
`require_platform`, `clean_env`, `run`; `scripts.golden.source_state` — `SourceStateError`,
`identity`, `assert_unchanged`; `scripts.golden.workspace` — `WorkspaceError`, `OwnedWorkspace`,
`validate_relative_path`, `allocate_family`, `atomic_write`. Issue #8 modules may import one another.
The Issue #6 `fitness` module is deliberately not admitted because its result owner is I5-01.
`jsonschema==4.26.0`, `rfc8785==0.1.4`, and `PyYAML==6.0.3` are already in the exact Issue #6 lock;
standard library modules require no package. Any other import, package, manifest/lock edit, install
action, Issue #7/framework path read, portal/runner source read, or network fetch is
`DEPENDENCY_IMPORT_UNADMITTED` and STOP.

The deny-list is exact by category: all tracked paths not listed above; all Issue #7/Vite/React/
ADR source/lock/evidence; portal/runner/data-platform implementation; `scripts/golden/**` except the
exact read-only public imports admitted above;
`tests/contracts/**` outside the new `tests/contracts/learning/**`; `tests/golden/**`;
`tests/fixtures/learning/promotion-trust/**`; `requirements/**`; root `Makefile`;
`mk/issue-5/i5-01.mk` and every issue fragment except new `i5-03.mk`; `release-manifest.json`;
`docs/code-standards.md`; `.gitignore`; other plans/discovery/audit; `.github/**`; Docker/Compose;
cloud/AWS/Terraform; ignored runtime fixtures; `.artifacts/**` as tracked/staged content; unrelated
user work. Read-only characterization does not grant mutation authority.

### Serialized Cook and Execution Ceilings

- One actor owns `feature/issue-5-03-learning-contracts` from the exact readiness output. Phases 1
  through 5 run in order in one issue-owned worktree; there is no phase fan-out, parallel Make flag,
  second shared-core writer or partial Stage A release.
- Before Phase 1 tracked writes, the same worktree must contain a manifest-admitted Issue #6 golden
  runtime with Python 3.12.3, lock SHA-256
  `f41c727b39f99106f95b7937b2811e8d27db89d1d5106e9f1d9effd4403143d2`, freeze SHA-256
  `cdb87ed71e0996f90041371cc25138afa02d78b134cbdc4afe9c25baa6649bba`, passing `pip check`, and
  exact `jsonschema==4.26.0`, `rfc8785==0.1.4`, `PyYAML==6.0.3`. If absent, stop before RED. The
  existing I5-01 `make golden-clean PROFILE=small SEED=42` may establish this generated runtime as
  an explicit pre-cook dependency step; its lock-verified wheel download is not Stage A behavior.
  All Stage A RED/GREEN/public checks then run with network and cloud credentials absent.
- Every focused RED/GREEN subprocess has a 60-second monotonic deadline, 2 MiB stdout and 2 MiB
  stderr live limits, and at most 16 MiB retained aggregate output. Public ceilings are 120 seconds
  for `learning-contracts-check`, 60 seconds for `api-contracts-check` and `lesson-check`, 30 seconds
  for `evidence-verify`, and the shipped 60 seconds for each I5-01 contract check. The exact
  three-target primary invocation has a 300-second aggregate ceiling; the complete ordered Stage A
  primary/blast/rollback sequence has a 600-second aggregate ceiling.
- Stage A mutable workspace plus retained evidence is capped at 256 MiB per run and 2 GiB peak RSS.
  A timeout, output/disk/RSS ceiling, missing runtime, missing tool or incomplete cleanup is a typed
  failure. These are local admission ceilings, not product SLOs; any increase requires retained
  measurement and a reviewed plan amendment.
- The 121-path scope is fixture-heavy by design: 65 invalid fixtures plus 6 valid/index fixtures,
  14 test modules, 13 implementation modules, 22 contract/content/OpenAPI files and one Make
  fragment. All 121 paths form one coherent Stage A release; no subset is independently published.

### Downstream Direct-Consumption Seam

The release set exposes the exact version registry, generic activation schema, operation matrix,
OpenAPI IDs, completion authority and evidence schemas/hashes. I5-04 can consume those JSON
artifacts directly and publish an I5-04-owned activation instance for its already reserved base
rows. Its commands then emit `fitness-result-v2` only when `owner`, `commandId`, fragment and
evidence version match that activation. No `learning/contracts/**` edit, copied schema, guessed
adapter or alternate canonicalizer is required; optional language bindings remain downstream
generated artifacts and never become a public contract.

## Stable TDD RED Fixture and Failure Matrix

Every row is created/indexed in Phase 1 and fails before the corresponding production file exists.
The fixture index records `testId`, exact path or `generated-private`, target contract, expected
code, expected JSON Pointer (or null), and `redReason=missing-behavior`; a syntax/import/fixture-index
failure never satisfies RED.

| Test ID | Exact fixture/path | Exact expected failure |
|---|---|---|
| `I8-AUTH-BASE-001` | `generated-private` wrong local/tracking/fresh-live identity | `AUTHORITY_HEAD_MISMATCH` before any write |
| `I8-AUTH-LEASE-002` | `generated-private` missing/conflicting shared-contract lease | `AUTHORITY_LEASE_REQUIRED` before any write |
| `I8-AUTH-PROTECTED-003` | `generated-private` changed shipped Issue #6 byte | `PROTECTED_PATH_CHANGED` before behavior execution |
| `I8-I6-FIXTURE-PIN-004` | `generated-private` base-registry mutation in a disposable copy | shipped verifier fails `FIXTURE_MANIFEST_ARTIFACT_MISMATCH`, proving overlay-only registration is required |
| `I8-STAGEA-NO-I7-010` | `generated-private` forbidden Issue #7/framework/portal/runner read or decoy influence | `STAGE_A_FRAMEWORK_DEPENDENCY` |
| `I8-SCHEMA-CLOSED-100` | `tests/fixtures/learning/contracts/invalid/schema/unknown-field.json` | `SCHEMA_UNKNOWN_PROPERTY` at the inserted property pointer |
| `I8-SCHEMA-MISSING-101` | `tests/fixtures/learning/contracts/invalid/schema/missing-required.json` | `SCHEMA_REQUIRED_PROPERTY` at the parent pointer |
| `I8-SCHEMA-TYPE-102` | `tests/fixtures/learning/contracts/invalid/schema/wrong-type.json` | `SCHEMA_TYPE_MISMATCH` at the mutated pointer |
| `I8-CANON-DUPLICATE-103` | `tests/fixtures/learning/contracts/invalid/canonicalization/duplicate-name.json` | `JSON_DUPLICATE_NAME`, before mapping |
| `I8-CANON-NUMBER-104` | `tests/fixtures/learning/contracts/invalid/canonicalization/nan.json`; `tests/fixtures/learning/contracts/invalid/canonicalization/positive-infinity.json`; `tests/fixtures/learning/contracts/invalid/canonicalization/negative-infinity.json` | `JSON_NON_IJSON_NUMBER` for each token |
| `I8-CANON-SURROGATE-105` | `tests/fixtures/learning/contracts/invalid/canonicalization/lone-surrogate.json` | `JSON_LONE_SURROGATE` |
| `I8-CANON-RANGE-106` | `tests/fixtures/learning/contracts/invalid/canonicalization/unsafe-integer.json` | `JSON_INTEGER_UNSAFE` |
| `I8-CANON-UTF8-107` | `tests/fixtures/learning/contracts/invalid/canonicalization/invalid-utf8.json` | `JSON_UTF8_INVALID` before parsing |
| `I8-CANON-BOM-108` | `tests/fixtures/learning/contracts/invalid/canonicalization/bom.json` | `JSON_BOM_FORBIDDEN` before parsing |
| `I8-CANON-TRAILING-109` | `tests/fixtures/learning/contracts/invalid/canonicalization/trailing-document.json` | `JSON_TRAILING_CONTENT` |
| `I8-REF-MISSING-110` | `tests/fixtures/learning/contracts/invalid/ref/missing-verifier.json` | `REF_TARGET_MISSING` |
| `I8-REF-CYCLE-111` | `tests/fixtures/learning/contracts/invalid/ref/prerequisite-cycle.json` | `REF_CYCLE` |
| `I8-REF-TRAVERSAL-112` | `tests/fixtures/learning/contracts/invalid/ref/path-traversal.json` | `REF_TRAVERSAL_FORBIDDEN` |
| `I8-REF-REMOTE-113` | `tests/fixtures/learning/contracts/invalid/ref/remote-ref.json` | `REF_REMOTE_FORBIDDEN` |
| `I8-REF-HASH-114` | `tests/fixtures/learning/contracts/invalid/ref/schema-hash-mismatch.json` | `REF_SCHEMA_HASH_MISMATCH` before semantic use |
| `I8-REGISTRY-BASE-115` | `tests/fixtures/learning/contracts/invalid/migration/base-registry-hash-mismatch.json` | `BASE_REGISTRY_HASH_MISMATCH` before extension composition |
| `I8-STATE-ILLEGAL-120` | `tests/fixtures/learning/contracts/invalid/state/illegal-transition.json` | `STATE_TRANSITION_FORBIDDEN` |
| `I8-STATE-STALE-121` | `tests/fixtures/learning/contracts/invalid/state/stale-version.json` | `PROGRESS_VERSION_CONFLICT` |
| `I8-IDEMPOTENCY-CONFLICT-122` | `tests/fixtures/learning/contracts/invalid/state/idempotency-payload-conflict.json` | `IDEMPOTENCY_KEY_REUSE` with no mutation |
| `I8-IDEMPOTENCY-DUPLICATE-123` | `tests/fixtures/learning/contracts/invalid/state/duplicate-effect.json` | `IDEMPOTENCY_DUPLICATE_EFFECT` until the same committed result is returned with exactly one effect |
| `I8-COMPLETION-FORGE-130` | `tests/fixtures/learning/contracts/invalid/completion/forged-browser-completion.json` | `COMPLETION_AUTHORITY_REQUIRED` |
| `I8-COMPLETION-DUAL-131` | `tests/fixtures/learning/contracts/invalid/completion/operation-result-direct-write.json` | `COMPLETION_DUAL_TRUTH` |
| `I8-COMPLETION-PRESENCE-134` | `tests/fixtures/learning/contracts/invalid/completion/evidence-presence-completes.json` | `COMPLETION_DUAL_TRUTH` |
| `I8-RECONCILE-ORPHAN-132` | `tests/fixtures/learning/contracts/invalid/completion/orphan-self-completion.json` | `RECONCILIATION_ORPHAN_CANNOT_COMPLETE` |
| `I8-RECONCILE-TAMPER-133` | `tests/fixtures/learning/contracts/invalid/completion/orphan-hash-mismatch.json` | `RECONCILIATION_HASH_MISMATCH` and quarantine |
| `I8-TAMPER-PAYLOAD-140` | `tests/fixtures/learning/contracts/invalid/evidence/evidence-payload.json` | `EVIDENCE_PAYLOAD_HASH_MISMATCH` |
| `I8-TAMPER-ARTIFACT-141` | `tests/fixtures/learning/contracts/invalid/evidence/artifact-hash.json` | `EVIDENCE_ARTIFACT_HASH_MISMATCH` |
| `I8-LOCATOR-TRAVERSAL-142` | `tests/fixtures/learning/contracts/invalid/evidence/locator-traversal.json` | `EVIDENCE_LOCATOR_INVALID` before open |
| `I8-LOCATOR-PRIVATE-147` | `generated-private` absolute/home/symlink/hardlink/device locators | `EVIDENCE_LOCATOR_INVALID` before content trust |
| `I8-TAMPER-VERIFIER-148` | `tests/fixtures/learning/contracts/invalid/evidence/stale-verifier-hash.json` | `EVIDENCE_VERIFIER_HASH_MISMATCH` |
| `I8-EVIDENCE-REPLAY-149` | `tests/fixtures/learning/contracts/invalid/evidence/replayed-run-identity.json` | `EVIDENCE_REPLAY_CONFLICT` with no index/progress mutation |
| `I8-EVIDENCE-PROVENANCE-143` | `tests/fixtures/learning/contracts/invalid/evidence/missing-dependency-sha.json` | `EVIDENCE_PROVENANCE_INCOMPLETE` |
| `I8-EVIDENCE-RECURSIVE-144` | `tests/fixtures/learning/contracts/invalid/evidence/recursive-identity.json` | `EVIDENCE_RECURSIVE_IDENTITY` |
| `I8-SECRET-145` | `generated-private` | `EVIDENCE_SENSITIVE_CONTENT`; canary absent from retained bytes |
| `I8-INJECTION-146` | `tests/fixtures/learning/contracts/invalid/security/injection-field.json` | `CONTRACT_INJECTION_FIELD_FORBIDDEN` |
| `I8-MIGRATION-UNKNOWN-150` | `tests/fixtures/learning/contracts/invalid/migration/unknown-version.json` | `SCHEMA_VERSION_UNREADABLE` |
| `I8-MIGRATION-LOSS-151` | `tests/fixtures/learning/contracts/invalid/migration/lossy-edge.json` | `MIGRATION_LOSSY_FORBIDDEN` |
| `I8-MIGRATION-CYCLE-152` | `tests/fixtures/learning/contracts/invalid/migration/cycle.json` | `MIGRATION_CYCLE` |
| `I8-MIGRATION-COLLISION-153` | `tests/fixtures/learning/contracts/invalid/migration/family-collision.json` | `SCHEMA_FAMILY_COLLISION` |
| `I8-OPERATION-DUPLICATE-154` | `tests/fixtures/learning/contracts/invalid/operation/duplicate-method-path.json` | `OPERATION_DUPLICATE` |
| `I8-OPERATION-TAXONOMY-155` | `tests/fixtures/learning/contracts/invalid/operation/missing-taxonomy.json` | `OPERATION_TAXONOMY_INCOMPLETE` |
| `I8-OPERATION-ROLE-156` | `tests/fixtures/learning/contracts/invalid/operation/physical-module-role.json` | `OPERATION_ROLE_NOT_NEUTRAL` |
| `I8-OPERATION-AUTHZ-157` | `tests/fixtures/learning/contracts/invalid/operation/missing-authorization.json` | `OPERATION_AUTHORIZATION_INCOMPLETE` |
| `I8-OPERATION-EVIDENCE-158` | `tests/fixtures/learning/contracts/invalid/operation/missing-evidence-rule.json` | `OPERATION_EVIDENCE_INCOMPLETE` |
| `I8-MIGRATION-BACKWARD-159` | `generated-private` v1 registry entry without its old reader | `SCHEMA_VERSION_UNREADABLE` before current-version selection |
| `I8-OPENAPI-MATRIX-160` | `tests/fixtures/learning/contracts/invalid/openapi/orphan-operation.json` | `OPENAPI_OPERATION_SET_MISMATCH` |
| `I8-OPENAPI-AUTH-161` | `tests/fixtures/learning/contracts/invalid/openapi/missing-authority.json` | `OPERATION_AUTHORITY_MISSING` |
| `I8-OPENAPI-IDEMPOTENCY-162` | `tests/fixtures/learning/contracts/invalid/openapi/missing-idempotency.json` | `OPERATION_IDEMPOTENCY_MISSING` |
| `I8-OPENAPI-RAW-163` | `tests/fixtures/learning/contracts/invalid/openapi/raw-sql-query.json` | `OPENAPI_RAW_QUERY_FORBIDDEN` |
| `I8-OPENAPI-REF-164` | `tests/fixtures/learning/contracts/invalid/openapi/remote-ref.json` | `OPENAPI_REF_FORBIDDEN` |
| `I8-OPENAPI-VERSION-165` | `tests/fixtures/learning/contracts/invalid/openapi/missing-version-response.json` | `OPENAPI_VERSION_NEGOTIATION_INCOMPLETE` |
| `I8-ASYNCAPI-166` | `tests/fixtures/learning/contracts/invalid/openapi/orphan-asyncapi.json` | `ASYNCAPI_WITHOUT_CHANNEL` |
| `I8-PROBE-MUTATION-167` | `tests/fixtures/learning/contracts/invalid/guidance/mutating-probe.json` | `PROBE_MUTATION_FORBIDDEN` |
| `I8-HINT-ORDER-168` | `tests/fixtures/learning/contracts/invalid/guidance/out-of-order-hint.json` | `HINT_ORDER_INVALID` |
| `I8-HINT-COMPLETION-169` | `tests/fixtures/learning/contracts/invalid/guidance/hint-completes.json` | `HINT_COMPLETION_FORBIDDEN` |
| `I8-PROMO-GRAIN-170` | `tests/fixtures/learning/contracts/invalid/promotion-trust/hidden-common-grain.json` | `PROMOTION_COMMON_GRAIN_FORBIDDEN` |
| `I8-PROMO-LIMIT-171` | `tests/fixtures/learning/contracts/invalid/promotion-trust/missing-limitation.json` | `PROMOTION_LIMITATION_REQUIRED` |
| `I8-PROMO-HASH-172` | `tests/fixtures/learning/contracts/invalid/promotion-trust/fixture-hash-drift.json` | `PROMOTION_FIXTURE_HASH_MISMATCH` |
| `I8-OPENAPI-REQUEST-173` | `tests/fixtures/learning/contracts/invalid/openapi/request-shape-drift.json` | `OPENAPI_REQUEST_CONTRACT_MISMATCH` |
| `I8-OPENAPI-RESPONSE-174` | `tests/fixtures/learning/contracts/invalid/openapi/response-shape-drift.json` | `OPENAPI_RESPONSE_CONTRACT_MISMATCH` |
| `I8-OPENAPI-ERROR-175` | `tests/fixtures/learning/contracts/invalid/openapi/error-set-drift.json` | `OPENAPI_ERROR_CONTRACT_MISMATCH` |
| `I8-PROBE-REQUIRED-176` | `tests/fixtures/learning/contracts/invalid/guidance/required-unavailable-passes.json` | `PROBE_REQUIRED_UNAVAILABLE` with no mutation |
| `I8-PROBE-OPTIONAL-177` | `tests/fixtures/learning/contracts/invalid/guidance/optional-unavailable-passes.json` | `PROBE_OPTIONAL_FALSE_PASS` |
| `I8-HINT-REVEAL-178` | `tests/fixtures/learning/contracts/invalid/guidance/unauthorized-reveal.json` | `HINT_REVEAL_FORBIDDEN` |
| `I8-OPENAPI-YAML-179` | `tests/fixtures/learning/contracts/invalid/openapi/duplicate-key.yaml` | `OPENAPI_YAML_DUPLICATE_KEY` before profile validation |
| `I8-FITNESS-OWNER-180` | `generated-private` v1 result with `owner=I5-03`, plus v2 owner/command/activation mismatches | `FITNESS_RESULT_OWNER_VERSION_MISMATCH`; resolved only by v2 whose owner, command and evidence version match the active row |
| `I8-DEPS-IMPORT-181` | `generated-private` forbidden import/package/lock delta | `DEPENDENCY_IMPORT_UNADMITTED` |
| `I8-DEPS-MANIFEST-182` | `generated-private` freeze/lock/manifest hash drift | `DEPENDENCY_MANIFEST_DRIFT` |
| `I8-DEPS-ADVISORY-183` | `generated-private` missing/unreviewed inherited advisory disposition | `DEPENDENCY_ADVISORY_UNRESOLVED` |
| `I8-COMMAND-ACTIVATION-184` | `tests/fixtures/learning/contracts/invalid/command/base-command-registry-hash-mismatch.json` | `COMMAND_ACTIVATION_BASE_MISMATCH` before recipe dispatch |
| `I8-ROLLBACK-SCOPE-190` | `generated-private` unowned marker/path | `ROLLBACK_SCOPE_UNOWNED`; no deletion |

## Requirement Matrix

| ID | Requirement | Stage / phase | Planned verification | Evidence |
|---|---|---|---|---|
| LC-001 | Start only from a fresh readiness-authorized exact head with one active shared-contract lease | A/1, B/6 | local = tracking = fresh-live; ancestry; clean and lease checks | authority result + remote refs |
| LC-002 | Write every schema/ref/state/tamper/canonicalization/migration/operation/completion/reconciliation/probe/hint/release negative before behavior | A/1 | exact stable matrix above; named RED assertions fail for intended missing behavior while read-only characterizers pass | `.artifacts/evidence/learning-contracts/<run-id>/tdd/red/` |
| LC-003 | Version lesson, lab, progress, and learner-evidence families with closed Draft 2020-12 schemas | A/2 | valid, missing, wrong-type, unknown-field, bounds and mutation fixtures | schema suite result and schema hashes |
| LC-004 | Reuse Issue #6 strict I-JSON/RFC 8785/SHA-256 profile without changing its bytes | A/2 | duplicate-name/non-finite/surrogate/BOM/JCS cross-reader vectors | canonical vector index and exact I5-01 hashes |
| LC-005 | Resolve competency/view/ADR/lab/verifier/failure/remediation references and reject cycles/ambiguity | A/2-3 | broken ref, duplicate ID, missing target and prerequisite-cycle negatives | reference graph projection |
| LC-006 | Preserve the normative state machine and typed conflicts/idempotency | A/3 | all legal/illegal transition pairs; duplicate/conflicting key properties | transition matrix result |
| LC-007 | Establish one completion authority and crash/orphan reconciliation protocol | A/3 | failure injection around operation result, evidence rename, progress commit and acknowledgment | reconciliation journal projection |
| LC-008 | Required probes are non-mutating; optional probe absence cannot forge pass | A/3 | mutation spy, missing tool, retry and required/optional matrix | probe result index |
| LC-009 | Hints are ordered evidence events and never change verifier/completion | A/3 | out-of-order, unauthorized reveal and completion-mutation negatives | hint event projection |
| LC-010 | Operation matrix covers every claimed Experience/Process/System/Backend/Technical operation | A/3-4 | two-way OpenAPI/matrix set equality and required metadata checks | matrix hash and coverage table |
| LC-011 | OpenAPI covers lesson/progress/workspace/operation/reset/verify/evidence/tool/query/health boundaries | A/4 | profile/schema/ref/example/problem/idempotency/correlation checks | OpenAPI hash and operation report |
| LC-012 | No AsyncAPI without a real channel | A/4 | repository inventory fails any AsyncAPI artifact while channel registry is empty; no artifact is created | contract inventory |
| LC-013 | Learner evidence includes exact provenance, redaction, retention, artifacts and canonical integrity | A/4 | tamper, stale hash, absolute path, secret/PII, recursive identity and missing provenance negatives | learner-evidence verification result |
| LC-014 | Promotion-trust manifest preserves four independent grains and `insufficient-evidence / no-common-grain` | A/4 | fixture digest, grain/order/limitation and forbidden attribution mutations | manifest and fixture hash report |
| LC-015 | Existing Issue #6 contracts, registry, readers and tracked fixtures remain byte-for-byte read-only/readable | A/1-5, B/6 | protected hashes + base-registry hash binding + existing data/evidence/migration suites | protected-path/registry compatibility report |
| LC-016 | New v1 families have identity readers; fitness v1 remains readable beside v2; migration engine is additive, reversible where representable, cycle-free and closed | A/2,5 | v1 reader vectors, private v0↔v1 vector, v2 owner vector; unknown/lossy/cycle/collision negatives | migration report |
| LC-017 | Public targets live only in `mk/issue-5/i5-03.mk`; do not duplicate I5-01 target ownership | A/5 | command registry ownership and Make recipe inventory | command/owner projection |
| LC-018 | Stage A consumes no selected-framework or Issue #7 ADR bytes | A/1,5 | source/import/ref scan, dependency-absent execution, decoy-tree invariance, changed/read path allow-list | stage-boundary result |
| LC-019 | Vite binding consumes exact merged Issue #7 handoff and cannot redefine Stage A | B/6 | merge/ADR/lock hash checks plus generated ID/hash equality | Vite handoff result |
| LC-020 | Contract release identities are exact external merge SHAs with independent exact-head review and human exact-head approval | A/5, B/6 | tested head = independently reviewed head = human-approved head; remotely observed merge identity/blob equality per repository flow | external issue/PR attestation |
| LC-021 | All checks stay local, 16 GiB-safe and post-install offline | A/1-5, B/6 | no-network/no-cloud-credential run; no Docker/heavy profile; bounded time/output | environment/tool/resource fields |
| LC-022 | No cloud/AWS/Terraform action or destructive migration exists in the command graph | All | command/source scan and subprocess spy | S3 negative-test result |
| LC-023 | I5-03 fitness evidence is truthful and later registered command owners can consume v2 without another shared-contract write | A/1,2,5 | v1 owner mismatch RED; v2 owner/command/activation mismatches; generic activation schema plus I5-03 instance; v1 reader/hash regression | fitness-version and downstream-consumption compatibility report |
| LC-024 | OpenAPI wire semantics and compatibility are exact | A/3-4 | per-operation request/success/error/auth/idempotency table; `/v1` and body schema-version negatives | API compatibility report |
| LC-025 | Dependency/advisory surface is bounded without inventing a tool | A/1-5 | exact lock/freeze/import/manifests unchanged; `pip check`; zero new distribution/import; inherited advisory disposition recorded | dependency inventory/advisory disposition |

## S3 Threat and Negative-Test Matrix

| Threat | Trust boundary | Required negative tests | Fail-safe behavior |
|---|---|---|---|
| Malformed or ambiguous JSON | Contract reader | duplicate names after escape decoding, BOM, lone surrogate, NaN/Infinity, negative-zero vector, oversized arrays/strings | reject before mapping/canonicalization |
| Unknown security-sensitive field | All closed schemas | secret/env/path/raw-command/SQL fields and namespaced-extension abuse | schema error; no field dropping/coercion |
| Reference substitution | Authoring/registry | duplicate IDs, wrong family/version, traversal/remote `$ref`, schema-hash mismatch, cycle | reject complete document set |
| Forged completion | Browser/Vite/progress | browser-completed flag, stale/edited operation result, mismatched verifier/evidence/contract hash | no completion event; typed failure |
| Dual mutable truth | Progress/operation-result/evidence | operation-result writer completes progress, evidence presence implies completion, divergent browser cache | only the `learning-progress-authority-v1` compare-and-set transaction can commit |
| Crash/partial commit | Evidence/progress | kill/ENOSPC before and after stage, fsync/rename/index/transaction/ack | prior state remains authoritative; orphan attach through same transaction or quarantine |
| Replay/idempotency collision | HTTP/state | same key/same payload, same key/different payload, stale expected version, reset/verify race | return same committed result or typed conflict; no second effect |
| Evidence tamper/leak | Evidence boundary | payload/artifact/verifier/fixture hash edits, traversal/absolute/symlink/hardlink/device locator, credential/private-key/PII canary, recursive SHA | reject/quarantine before trust; descriptor-bound read; redact bounded diagnostics |
| Cross-grain misattribution | Promotion-trust manifest | hidden join/common-grain assertion, omitted limitation, changed ordering/threshold | manifest validation fails; completion unavailable |
| Operation/auth/injection drift | OpenAPI/matrix | undocumented operation, missing taxonomy/role/auth/CSRF/idempotency/evidence/version, raw SQL/command/path/URL/template injection field | API contract check fails before dispatch |
| Framework contract fork | Vite binding | copied schema with changed field/default, operation rename, alternate completion rule/canonicalizer | Stage B fails; Stage A remains unchanged |
| Supply-chain/runtime drift | Validator execution | wrong Python/platform/freeze/lock hash, unadmitted dependency, install-script request | fail with typed remediation; no dependency mutation |
| Known/advisory drift | Dependency boundary | changed lock/freeze/manifests, newly imported distribution, missing `pip check`, unreviewed inherited advisory | fail; only a pre-authorized recorded inherited-advisory disposition can satisfy the gate; never fetch/fix/waive inside the check |
| Cloud/destructive escape | Command graph | AWS credential canary, `terraform`, cloud SDK, Docker/heavy-profile, shell string, broad delete invocation | command graph rejected before execution |

## Risk Register

| ID | Risk | Severity | Mitigation / rollback | Clearing evidence |
|---|---|---:|---|---|
| RK-01 | Stage A silently reads provisional Issue #7 contracts | Critical | explicit read/import/path allow-list; run with dependency absent and decoy bytes; readiness independently decides | LC-018 evidence |
| RK-02 | New registry competes with Issue #6 registry | Critical | hash-bound overlay; reject family overlap except the declared fitness extension; never edit the base registry or its fixture-pinned hash | registry collision/base-hash suite |
| RK-03 | JSON Schema appears closed but semantic refs/state remain open | Critical | separate closed semantic validator and exhaustive mutation/reference matrices | LC-003/005/006 |
| RK-04 | Evidence hash is mistaken for authenticity | High | exact local-corruption-only wording; require a fresh trusted verifier result later; hosted signing remains I5-14 | claim/text and tamper tests |
| RK-05 | Evidence and progress become dual truth | Critical | one transaction references immutable evidence + committed operation result; orphan cannot complete itself | LC-007 suite |
| RK-06 | Reset/verify/reconcile race fabricates state | Critical | expected-version CAS, one mutation lease, idempotency and fault injection | state/reconciliation suite |
| RK-07 | Promotion manifest introduces causal attribution across four grains | Critical | encode independent grains/limitations and forbid common-grain claim | LC-014 mutations |
| RK-08 | Generic API taxonomy becomes physical microservices | High | matrix uses abstract process roles and `downstream-required` enforcement only; no portal/runner module mapping or service is created | operation matrix review/check |
| RK-09 | AsyncAPI is added for polling/SSE without a channel | High | polling-only v1; channel inventory empty; orphan AsyncAPI check | LC-012 inventory |
| RK-10 | New validator/runtime breaks offline or 16 GiB target | High | existing locked Python only; no new distribution; bounded output/time and post-install no-network run | runtime/freeze/resource evidence |
| RK-11 | Backward migration silently drops information | Critical | lossless round-trip property; lossy edge is STOP/new version decision; old readers retained | migration report |
| RK-12 | Stage B uses owner direction instead of accepted merged handoff | Critical | require exact merged SHA/ADR/lock/hashes; current unmerged Issue #7 bytes are non-authority | Phase 6 entry result |
| RK-13 | Vite consumer representation becomes a second schema/canonicalizer | Critical | any amended representation is limited to IDs/hashes; no copied schema/default/state logic; byte equality gates | Stage B drift suite |
| RK-14 | Root Make or I5-01 target is overwritten | High | one issue fragment; command registry check; root/fragment hashes protected | changed-path report |
| RK-15 | Contract release file recursively claims its own commit | High | tracked set contains content hashes only; release/merge SHA recorded externally | provenance check |
| RK-16 | Readiness-authorized Stage A cook is mistaken for PR/merge authority or full Issue #8 completion | Critical | implementation-only wording; final independent exact-head review, repository checks, human approval and external merge identity remain mandatory; Stage B stays closed | external gate attestations |
| RK-17 | I5-03 emits invalid v1 evidence or v2 owner becomes another hard-coded shared bottleneck | Critical | RED v1 and v2 owner/command mismatches; v2 owner is activation-bound; retain v1/readers; future owners add only issue-owned activation instances | LC-023 report |
| RK-18 | Reserved I5-03 commands remain labelled `future-owner` in the immutable command registry | High | retain base registry; use the generic activation schema and I5-03-owned hash-bound instance; `make help` keeps the immutable snapshot view while the I5-03 validator composes activation | command/activation report |
| RK-19 | YAML 1.1 coercion/duplicate keys make OpenAPI ambiguous | Critical | custom locked safe loader rejects non-JSON YAML features/duplicates and hashes normalized model | OpenAPI parser vectors |

## Command and Evidence Matrix

| Command | Owner | Required scope | Evidence root / principal assertion |
|---|---|---|---|
| `make learning-contracts-check` | I5-03 / `fitness-result-v2` | Stage A and final Stage B | `.artifacts/evidence/learning-contracts/<run-id>/`; Stage A schemas, refs, state, completion, probes, hints and migration; any Stage B addition requires the amended plan |
| `make lesson-check LESSON=promotion-trust` | I5-03 / `fitness-result-v2` | Stage A and final | same family; promotion manifest + fixture hash + grain integrity |
| `make api-contracts-check` | I5-03 / `fitness-result-v2` | Stage A and final | `.artifacts/evidence/api-contracts/<run-id>/`; OpenAPI/profile/refs/examples/matrix equality/no AsyncAPI |
| `make evidence-verify` | I5-03 / `fitness-result-v2` | Stage A and final | validates one emitted learner or fitness evidence locator without mutation |
| `make evidence-contracts-check` | I5-01 read-only | blast radius | proves base evidence/JCS/fitness contracts unchanged |
| `make data-contracts-check migration-contracts-check` | I5-01 read-only | blast radius | proves Issue #6 data/fixture/readers and migration dispatch unchanged |
| `make help` | I5-01 root registry | blast radius | base registry remains green and reserved I5-03 names/owners remain discoverable; activation/recipe exactness is proven by I5-03 tests |

## STOP Conditions

- Dirty/wrong/divergent implementation base or missing exact remote ancestry.
- No exclusive shared-contract lease, conflicting writer, or path need outside the phase allow-list.
- Stage A reads an Issue #7/framework/ADR byte or needs a selected-stack dependency.
- Any Issue #6 contract/registry/fixture/reader/lock/Make byte or another protected path changes.
- Missing required tool/lock, unadmitted runtime dependency, schema/ref/operation/migration drift,
  failed S3 negative, secret/private path in evidence, or inability to roll back safely.
- Any Stage B attempt before the exact Issue #7 Vite ADR/handoff is merged and externally attested.
- Any exact-head human approval mismatch, failed required check, or unresolved contract-release SHA.
- Any missing independent exact-head review, ambiguous request/version/conflict semantics,
  unreviewed dependency/advisory delta, or evidence locator that is not descriptor-bound.

Planning-time Issue #7 dependency is the only expected unresolved gate. It blocks Stage B, not
fresh independent validation of this full staged plan.
