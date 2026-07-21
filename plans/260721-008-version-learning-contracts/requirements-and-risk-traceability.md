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
| Issue #8 body | `https://github.com/khanhvg/ai-ready-data-platform/issues/8` observed OPEN with `triaged`, `risk:high`, `tdd`, `security:S3`, `shared-core`, `api` | Exclusive paths, tests-first order, three primary checks, evidence root, S3, migration/rollback, STOP rules |
| Owner parallelization decision | `https://github.com/khanhvg/ai-ready-data-platform/issues/5#issuecomment-5036142770` | Plan downstream lanes now; only fresh readiness may authorize a genuinely independent Stage A; single shared-contract writer |
| Planning input | `24be3b34c6b0fcdbd07c5800dcab349054e34713` | Shipped Issue #6 integration/handoff and exact read-only contract/fixture bytes |
| Master discovery | `plans/260721-005-enterprise-learning-sandbox/discovery/` at the input | PH-C02, PH-C05, PH-C06, PH-H06, PH-H11 and SC-01/02/03/06/14/16/19/20 |
| Normative lesson/lab contract | `plans/260721-005-enterprise-learning-sandbox/lesson-lab-contract.md` | Required lesson/lab fields, state machine, API operations, evidence, accessibility, remediation |
| Master Phase 3 | `plans/260721-005-enterprise-learning-sandbox/phase-03-shared-lesson-lab-and-evidence-contract.md` | TDD order, operation matrix, one completion authority, probes/hints, backward readers, no AsyncAPI without channel |
| Master implementation graph | `plans/260721-005-enterprise-learning-sandbox/implementation-issue-graph.md` | I5-03 dependencies/ownership, downstream blockers, exact target names, serialized release SHA |
| Master readiness | `e440c5855732d5d8f5d634e3cc1359c010cc5ed3` | Per-issue plan→independent validation→fresh audit, no master cook, mandatory human pre-merge approval |
| Issue #6 handoff | `plans/260721-006-freeze-golden-baseline/implementation-handoff.md` and shipped input tree | Strict I-JSON/JCS, schema registry/readers, fitness evidence, protected paths, additive migration |
| Issue #7 state | OPEN/unmerged at planning time; owner selected Vite in Issue #7 comment `5036142177` | Direction only. No accepted ADR or merged handoff SHA exists; Stage B stays blocked |

## Requirement Matrix

| ID | Requirement | Stage / phase | Planned verification | Evidence |
|---|---|---|---|---|
| LC-001 | Start only from a fresh readiness-authorized exact head with one active shared-contract lease | A/1, B/6 | local = tracking = fresh-live; ancestry; clean and lease checks | authority result + remote refs |
| LC-002 | Write failing schema/ref/state/tamper/migration fixtures before behavior | A/1 | named RED assertions fail for intended missing behavior while read-only characterizers pass | `.artifacts/evidence/learning-contracts/<run-id>/tdd/red/` |
| LC-003 | Version lesson, lab, progress, and learner-evidence families with closed Draft 2020-12 schemas | A/2 | valid, missing, wrong-type, unknown-field, bounds and mutation fixtures | schema suite result and schema hashes |
| LC-004 | Reuse Issue #6 strict I-JSON/RFC 8785/SHA-256 profile without changing its bytes | A/2 | duplicate-name/non-finite/surrogate/BOM/JCS cross-reader vectors | canonical vector index and exact I5-01 hashes |
| LC-005 | Resolve competency/view/ADR/lab/verifier/failure/remediation references and reject cycles/ambiguity | A/2-3 | broken ref, duplicate ID, missing target and prerequisite-cycle negatives | reference graph projection |
| LC-006 | Preserve the normative state machine and typed conflicts/idempotency | A/3 | all legal/illegal transition pairs; duplicate/conflicting key properties | transition matrix result |
| LC-007 | Establish one completion authority and crash/orphan reconciliation protocol | A/3 | failure injection around runner result, evidence rename, progress commit and acknowledgment | reconciliation journal projection |
| LC-008 | Required probes are non-mutating; optional probe absence cannot forge pass | A/3 | mutation spy, missing tool, retry and required/optional matrix | probe result index |
| LC-009 | Hints are ordered evidence events and never change verifier/completion | A/3 | out-of-order, unauthorized reveal and completion-mutation negatives | hint event projection |
| LC-010 | Operation matrix covers every claimed Experience/Process/System/Backend/Technical operation | A/3-4 | two-way OpenAPI/matrix set equality and required metadata checks | matrix hash and coverage table |
| LC-011 | OpenAPI covers lesson/progress/workspace/operation/reset/verify/evidence/tool/query/health boundaries | A/4 | profile/schema/ref/example/problem/idempotency/correlation checks | OpenAPI hash and operation report |
| LC-012 | No AsyncAPI without a real channel | A/4 | repository inventory fails any AsyncAPI artifact while channel registry is empty; no artifact is created | contract inventory |
| LC-013 | Learner evidence includes exact provenance, redaction, retention, artifacts and canonical integrity | A/4 | tamper, stale hash, absolute path, secret/PII, recursive identity and missing provenance negatives | learner-evidence verification result |
| LC-014 | Promotion-trust manifest preserves four independent grains and `insufficient-evidence / no-common-grain` | A/4 | fixture digest, grain/order/limitation and forbidden attribution mutations | manifest and fixture hash report |
| LC-015 | Existing Issue #6 contracts and tracked fixtures remain byte-for-byte read-only/readable | A/1-5, B/6 | pre/post hash allow-list plus existing data/evidence/migration suites | protected-path report |
| LC-016 | New v1 families have identity readers; future migration engine is additive, reversible, cycle-free and closed | A/2,5 | private v0↔v1 vector; unknown/lossy/cycle/collision negatives; no fictional release | migration report |
| LC-017 | Public targets live only in `mk/issue-5/i5-03.mk`; do not duplicate I5-01 target ownership | A/5 | command registry ownership and Make recipe inventory | command/owner projection |
| LC-018 | Stage A consumes no selected-framework/ADR bytes | A/1,5 | source/import/ref scan, dependency-absent execution, decoy-tree invariance, changed/read path allow-list | stage-boundary result |
| LC-019 | Vite binding consumes exact merged Issue #7 handoff and cannot redefine Stage A | B/6 | merge/ADR/lock hash checks plus generated ID/hash equality | Vite handoff result |
| LC-020 | Contract release identities are exact external merge SHAs with human exact-head approval | A/5, B/6 | reviewed head = approved head = remotely observed merge parent/head per repository flow | external issue/PR attestation |
| LC-021 | All checks stay local, 16 GiB-safe and post-install offline | A/1-5, B/6 | no-network/no-cloud-credential run; no Docker/heavy profile; bounded time/output | environment/tool/resource fields |
| LC-022 | No cloud/AWS/Terraform action or destructive migration exists in the command graph | All | command/source scan and subprocess spy | S3 negative-test result |

## S3 Threat and Negative-Test Matrix

| Threat | Trust boundary | Required negative tests | Fail-safe behavior |
|---|---|---|---|
| Malformed or ambiguous JSON | Contract reader | duplicate names after escape decoding, BOM, lone surrogate, NaN/Infinity, negative-zero vector, oversized arrays/strings | reject before mapping/canonicalization |
| Unknown security-sensitive field | All closed schemas | secret/env/path/raw-command/SQL fields and namespaced-extension abuse | schema error; no field dropping/coercion |
| Reference substitution | Authoring/registry | duplicate IDs, wrong family/version, traversal/remote `$ref`, schema-hash mismatch, cycle | reject complete document set |
| Forged completion | Browser/Vite/progress | browser-completed flag, stale/edited runner result, mismatched verifier/evidence/contract hash | no completion event; typed failure |
| Dual mutable truth | Progress/runner/evidence | runner writes completion, evidence presence implies completion, divergent browser cache | only progress-store compare-and-set transaction can commit |
| Crash/partial commit | Evidence/progress | kill/ENOSPC before and after stage, fsync/rename/index/transaction/ack | prior state remains authoritative; orphan attach through same transaction or quarantine |
| Replay/idempotency collision | HTTP/state | same key/same payload, same key/different payload, stale expected version, reset/verify race | return same committed result or typed conflict; no second effect |
| Evidence tamper/leak | Evidence boundary | payload/artifact/verifier/fixture hash edits, absolute path, credential/private-key/PII canary, recursive SHA | reject/quarantine; redact bounded diagnostics |
| Cross-grain misattribution | Promotion-trust manifest | hidden join/common-grain assertion, omitted limitation, changed ordering/threshold | manifest validation fails; completion unavailable |
| Operation/auth drift | OpenAPI/matrix | undocumented operation, missing taxonomy/owner/auth/CSRF/idempotency/evidence, raw SQL endpoint | API contract check fails |
| Framework contract fork | Vite binding | copied schema with changed field/default, operation rename, alternate completion rule/canonicalizer | Stage B fails; Stage A remains unchanged |
| Supply-chain/runtime drift | Validator execution | wrong Python/platform/freeze/lock hash, unadmitted dependency, install-script request | fail with typed remediation; no dependency mutation |
| Cloud/destructive escape | Command graph | AWS credential canary, `terraform`, cloud SDK, Docker/heavy-profile, shell string, broad delete invocation | command graph rejected before execution |

## Risk Register

| ID | Risk | Severity | Mitigation / rollback | Clearing evidence |
|---|---|---:|---|---|
| RK-01 | Stage A silently reads provisional Issue #7 contracts | Critical | explicit read/import/path allow-list; run with dependency absent and decoy bytes; readiness independently decides | LC-018 evidence |
| RK-02 | New registry competes with Issue #6 registry | Critical | scoped new-family registry; reject family overlap; compose read-only at dispatch; never edit I5-01 registry | registry collision suite |
| RK-03 | JSON Schema appears closed but semantic refs/state remain open | Critical | separate closed semantic validator and exhaustive mutation/reference matrices | LC-003/005/006 |
| RK-04 | Evidence hash is mistaken for authenticity | High | exact local-corruption-only wording; require fresh private-runner result later; hosted signing remains I5-14 | claim/text and tamper tests |
| RK-05 | Evidence and progress become dual truth | Critical | one transaction references immutable evidence + committed runner result; orphan cannot complete itself | LC-007 suite |
| RK-06 | Reset/verify/reconcile race fabricates state | Critical | expected-version CAS, one mutation lease, idempotency and fault injection | state/reconciliation suite |
| RK-07 | Promotion manifest introduces causal attribution across four grains | Critical | encode independent grains/limitations and forbid common-grain claim | LC-014 mutations |
| RK-08 | Generic API taxonomy becomes physical microservices | High | matrix metadata maps to portal+BFF/runner modules; no service is created by taxonomy | operation matrix review/check |
| RK-09 | AsyncAPI is added for polling/SSE without a channel | High | polling-only v1; channel inventory empty; orphan AsyncAPI check | LC-012 inventory |
| RK-10 | New validator/runtime breaks offline or 16 GiB target | High | existing locked Python only; no new distribution; bounded output/time and post-install no-network run | runtime/freeze/resource evidence |
| RK-11 | Backward migration silently drops information | Critical | lossless round-trip property; lossy edge is STOP/new version decision; old readers retained | migration report |
| RK-12 | Stage B uses owner direction instead of accepted merged handoff | Critical | require exact merged SHA/ADR/lock/hashes; current unmerged Issue #7 bytes are non-authority | Phase 6 entry result |
| RK-13 | Vite binding becomes a second schema/canonicalizer | Critical | generated IDs/hashes only; no copied schema/default/state logic; byte equality gates | Stage B drift suite |
| RK-14 | Root Make or I5-01 target is overwritten | High | one issue fragment; command registry check; root/fragment hashes protected | changed-path report |
| RK-15 | Contract release file recursively claims its own commit | High | tracked set contains content hashes only; release/merge SHA recorded externally | provenance check |
| RK-16 | Staged Stage A merge is treated as planner authorization | Critical | explicit candidate-only wording; fresh validation/readiness and human exact-head approval remain mandatory | external gate attestations |

## Command and Evidence Matrix

| Command | Owner | Required scope | Evidence root / principal assertion |
|---|---|---|---|
| `make learning-contracts-check` | I5-03 | Stage A and final Stage B | `.artifacts/evidence/learning-contracts/<run-id>/`; schemas, refs, state, completion, probes, hints, migration, binding when present |
| `make lesson-check LESSON=promotion-trust` | I5-03 | Stage A and final | same family; promotion manifest + fixture hash + grain integrity |
| `make api-contracts-check` | I5-03 | Stage A and final | `.artifacts/evidence/api-contracts/<run-id>/`; OpenAPI/profile/refs/examples/matrix equality/no AsyncAPI |
| `make evidence-verify` | I5-03 | Stage A and final | validates one emitted learner or fitness evidence locator without mutation |
| `make evidence-contracts-check` | I5-01 read-only | blast radius | proves base evidence/JCS/fitness contracts unchanged |
| `make data-contracts-check migration-contracts-check` | I5-01 read-only | blast radius | proves Issue #6 data/fixture/readers and migration dispatch unchanged |
| `make help` | I5-01 root registry | blast radius | exactly one owner/recipe per public command; I5-03 target discovery |

## STOP Conditions

- Dirty/wrong/divergent implementation base or missing exact remote ancestry.
- No exclusive shared-contract lease, conflicting writer, or path need outside the phase allow-list.
- Stage A reads an Issue #7/framework/ADR byte or needs a selected-stack dependency.
- Issue #6 contract/fixture/lock/Make bytes change or a protected path changes.
- Missing required tool/lock, unadmitted runtime dependency, schema/ref/operation/migration drift,
  failed S3 negative, secret/private path in evidence, or inability to roll back safely.
- Any Stage B attempt before the exact Issue #7 Vite ADR/handoff is merged and externally attested.
- Any exact-head human approval mismatch, failed required check, or unresolved contract-release SHA.

Planning-time Issue #7 dependency is the only expected unresolved gate. It blocks Stage B, not
fresh independent validation of this full staged plan.
