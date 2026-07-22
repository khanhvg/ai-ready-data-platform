---
title: "Issue #8 Stage B requirements and risk traceability"
status: pending
priority: P1
issue: 8
created: "2026-07-22"
---

# Issue #8 Stage B Requirements and Risk Traceability

## Accepted Sources

| Source | Exact authority | Stage B consequence |
|---|---|---|
| Issue #8 body/comments | Current issue plus Stage A evidence `5043195549` and conflict report `5043335319` | I5-03 owns the serialized first-manifest/shared-contract seam and tests-first/S3/release duties |
| Release integration | `fecf6bb8e5dfa7cc69f9766f72ac6f5b9301dad9` | sole Stage B implementation input |
| Stage A release | PR #23 merge `5c2244c2c860234d0df49cf0a42ad950c6495717`; 21-entry set hash in plan | immutable contract core; must not be rewritten |
| Issue #7 release | PR #22 merge `1806b6d515f2f7a2ace2be7077af84a745ff221f`; Accepted ADR and exact Vite package/lock/source hashes in plan | exact read-only browser identifier authority |
| Issue #6 evidence | `evidence-v1.json` SHA-256 `2f4d90228fa2ea8859a8db630ff587b6cebdc10a0bf6b7db25e46c3dc27181d5` | exact physical grain-key/order authority |
| Master graph/contract | `plans/260721-005-enterprise-learning-sandbox/implementation-issue-graph.md` and `lesson-lab-contract.md` at input | I5-03 shared contracts; I5-04 runner; I5-05 portal; one contract truth |
| Issue #9/#10 | Current bodies/comments | consumers are read-only at the shared seam; portal/runner behavior is downstream-owned |

## Requirements Matrix

| ID | Requirement | Phase | Verification | Evidence |
|---|---|---:|---|---|
| BND-001 | Start from exact clean input/live ref with PR #22/#23 ancestry and sole I5-03 lease | 1 | local=tracking=fresh-live, ancestry, state, lease checks | authority result |
| BND-002 | Preserve all Stage A/Issue #6/Issue #7 protected bytes | 1-3 | exact SHA-256 plus Git diff/opened-path inventory | protected result |
| BND-003 | Freeze real source mismatch before behavior | 1 | manifest/evidence/Vite extraction equality to exact expected rows | RED result |
| BND-004 | Publish one closed bounded binding schema/document | 2 | meta-schema + instance + unknown-field/bounds negatives | schema hashes/results |
| BND-005 | Bind every dependency by exact path/hash/merge SHA | 2-3 | regular-file ref/hash verification and wrong-hash fixtures | dependency projection |
| BND-006 | Map exactly four grains, two unique field-alias rules applied in three row positions, and one grain-ID alias | 2 | exact ordered set equality; missing/extra/rename negatives | alias projection |
| BND-007 | Mapping is total, ordered, bijective, and value-preserving | 2 | source/target order, unique target, record-key existence, no transform | mapping result |
| BND-008 | Browser binding remains projection-only | 1-3 | authority-field mutation and forbidden-key/source scans | trust-boundary result |
| BND-009 | Server Stage A validation/OpenAPI and completion authority remain unchanged | 2-3 | protected hashes, API/matrix/completion checks | primary/blast results |
| BND-010 | No generated TypeScript/UI/runner/data/Make/registry/manifest/OpenAPI output | 1-3 | exact changed-path/import/source inventories | boundary result |
| BND-011 | Existing I5-03 public command validates binding and emits fitness v2 provenance | 2-3 | public Make result and evidence verification | binding hashes/evidence |
| BND-012 | Stage A 65-invalid/16-operation/final-4 and inherited 19/1/13 results remain | 3 | existing exact commands/result counts | blast report |
| BND-013 | No new dependency, install, network, browser, cloud, or destructive command | 1-3 | lock/import/subprocess/offline/S3 scans | S3 result |
| BND-014 | v1 reader is retained; rollback deselects without deleting released history | 2-3 | dual-read and marker-owned rollback rehearsal | rollback result |
| BND-015 | Final release uses observed hashes/SHAs and exact-head independent/human gates | 3 | tested=reviewed=approved head; fresh remote merge observation | external handoff |

## Exact Binding Field and Semantic Contract

Every object is closed with `additionalProperties: false` or equivalent. Required fields are never
made optional by defaults.

| Field | Exact semantics |
|---|---|
| `schemaVersion` | const `promotion-trust-vite-binding-v1` |
| `bindingId` | const `promotion-trust-vite-binding-v1` |
| `mode` | const `lossless-identifier-alias-v1` |
| `stageA` | `releaseSha`; exact `{path,sha256}` for contract set and promotion manifest |
| `issue7` | `mergeSha`; exact `{path,sha256}` for Accepted ADR, package, lock, and lesson contract |
| `fixture` | exact `{path,sha256}` for evidence and fixture manifest; const use `build-time-validation-only` |
| `grainBindings[]` | closed `stageAGrain,viteGrain,stageAKeys,viteKeys,aliases`; exactly four ordered unique rows |
| `aliases[]` | closed `from,to,kind`; `kind` is `identity` or `identifier-alias`; no transform/default/value |
| `decision` | const `insufficient-evidence/no-common-grain` |
| `trustBoundary` | projection-only browser, Stage A server validation, `learning-progress-authority-v1`, and false authority flags |

Semantic validation order:

1. descriptor-bound bounded read, strict UTF-8/I-JSON and closed schema;
2. exact dependency SHA/path/merge identity;
3. Stage A manifest source/grain/key extraction;
4. Issue #6 evidence grain/order/record-key extraction;
5. Issue #7 Vite grain/value extraction as confirmed by the existing Node suite;
6. exact four-row order and total source/target coverage;
7. alias source/target uniqueness, positional equality, and zero transformation;
8. decision/no-common-grain and trust-boundary invariants;
9. canonical binding hash/evidence projection.

First failure wins with a stable bounded code. No field stripping, coercion, default insertion,
case conversion, value rewrite, inferred alias, or fallback is allowed.

## Stable Real-Path RED Catalog

| RED ID | Real input/fixture | Expected failure |
|---|---|---|
| `I8B-AUTH-001` | wrong local/live input, ancestry, dirty tree, or lease | `STAGE_B_AUTHORITY_INVALID` |
| `I8B-PROTECTED-002` | any protected input hash/path drift | `STAGE_B_PROTECTED_DRIFT` |
| `I8B-MISMATCH-010` | real Stage A + Issue #6 + Issue #7 paths | characterizer passes only with the exact three absent aliases |
| `I8B-BINDING-ABSENT-011` | absent binding/schema/reader before GREEN | `VITE_BINDING_REQUIRED` |
| `I8B-ALIAS-020` | `contract-key-drift.json` | `BINDING_STAGE_A_KEY_MISMATCH` |
| `I8B-ALIAS-021` | `fixture-key-drift.json` | `BINDING_FIXTURE_KEY_MISMATCH` |
| `I8B-ALIAS-022` | `duplicate-target-key.json` | `BINDING_ALIAS_NOT_BIJECTIVE` |
| `I8B-ALIAS-023` | `grain-id-drift.json` | `BINDING_GRAIN_MISMATCH` |
| `I8B-HASH-024` | `dependency-hash-drift.json` | `BINDING_DEPENDENCY_HASH_MISMATCH` |
| `I8B-BOUNDARY-025` | `completion-authority-override.json` | `BINDING_AUTHORITY_FORBIDDEN` |
| `I8B-PATH-026` | `absolute-path.json` | `BINDING_REFERENCE_FORBIDDEN` |
| `I8B-BOUNDARY-027` | `raw-record-leak.json` | `BINDING_DATA_PAYLOAD_FORBIDDEN` |
| `I8B-NO-COPY-030` | in-memory schema/default/value/operation/auth mutation | `BINDING_CONTRACT_FORK_FORBIDDEN` |
| `I8B-NO-GENERATED-TYPES-031` | changed-path inventory | `BINDING_DOWNSTREAM_PATH_FORBIDDEN` |
| `I8B-INVENTORY-032` | missing/extra invalid fixture | `BINDING_FIXTURE_INDEX_INCOMPLETE` |
| `I8B-ROLLBACK-040` | missing binding selection / unowned cleanup candidate | `BINDING_NOT_SELECTED` / `ROLLBACK_SCOPE_UNOWNED` with Stage A intact |

Fixtures contain only inputs/cases, never their expected code. The test owns the exact path→ID→code
table so fixture bytes cannot select their result.

## S3 Threat and Negative-Test Matrix

| Threat | Boundary | Negative test | Fail-safe behavior |
|---|---|---|---|
| Hash/ref substitution | Stage A/Issue #6/Issue #7 reads | wrong SHA/path, traversal, remote ref, symlink/hardlink/special file, race | refuse before parsing/use |
| Non-bijective alias | Binding semantics | missing/extra/duplicate/reordered source or target | no binding projection |
| Value/data transformation | Binding/browser | raw records, transform/default/template/expression/value field | closed schema/boundary rejection |
| Second contract truth | Binding/portal | copied schema fields/defaults/operations/canonicalizer | fail changed-path/source scan |
| Forged authority | Browser/server | authorize/validate/mutate/complete/evidence flags or fields | `BINDING_AUTHORITY_FORBIDDEN`; no state effect |
| Raw fixture leakage | Browser bundle | record arrays/values/private evidence locator | `BINDING_DATA_PAYLOAD_FORBIDDEN` |
| Secret/private path | Document/evidence/logs | credential, private-key, PII, and machine-private-locator canaries | fail and quarantine bounded evidence |
| Supply-chain drift | Python/Node checks | new import/distribution/lock/package/install/npx/network | fail; no mutation/fetch |
| Resource exhaustion | Reader/check/evidence | oversized doc/array/log/time/RSS/disk | bounded failure with remediation |
| Cloud/destructive escape | Command graph | AWS/Terraform/cloud/Docker/browser/server/broad delete | reject command graph before execution |
| Unsafe rollback | Cleanup/consumer selection | foreign marker/device/inode/nonce, symlink/hardlink/special file | refuse deletion; retain Stage A/binding/evidence |

## Risk Register

| ID | Risk | Severity | Mitigation / clearing evidence |
|---|---|---:|---|
| BR-01 | Treat source mismatch as harmless display prose | Critical | exact fixture/Vite keys drive real lookup; RED proves absent alias and Issue #10 read-only boundary |
| BR-02 | Rewrite released Stage A | Critical | 21-entry set and protected hashes; zero Stage A allow-list |
| BR-03 | Binding becomes a new domain schema | Critical | aliases/IDs/hashes only; no values/defaults/operations/state/auth/completion |
| BR-04 | Positional alias maps wrong meaning | Critical | stable grain ID + source order + target order + Vite label + record-key existence; one-to-one only |
| BR-05 | Nullable category is coerced/defaulted | High | key existence is separate from value; null remains untouched |
| BR-06 | Vite spike becomes portal implementation | High | Issue #7 paths read-only; no UI/type/build output; Issue #10 retains ownership |
| BR-07 | New family lacks backward/rollback story | High | new v1 reader retained; no predecessor; deselection not deletion; future versions explicit |
| BR-08 | Existing check silently skips binding | Critical | absence is RED/fail; public check result/evidence must include binding hashes |
| BR-09 | Contract set/registry falsely updated | High | two-component handoff; Stage A set/registry protected and unchanged |
| BR-10 | Planning/implementation head is mistaken for merge SHA | Critical | output/merge identity only externally recorded after existence/remote observation |
| BR-11 | Shared lease released before downstream-consumable release | Critical | keep active through merge/handoff; external lease-release assertion last |
| BR-12 | S3 evidence leaks local or fixture data | Critical | no raw values/records/private locators; bounded scans and quarantine |

## Command and Evidence Matrix

| Command | Owner / tool | Exact purpose | Evidence |
|---|---|---|---|
| `python3 -m unittest tests.contracts.learning.test_vite_consumer_binding` | I5-03 / admitted Python | exact Stage B RED/GREEN, binding semantics and boundary | test names/codes, paths/hashes, duration/resource |
| `node --test spikes/web/candidates/vite/tests/promotion-trust-contract.test.mjs` | I5-02 read-only / Node v22.22.3 | five exact Vite/fixture contract assertions | TAP 5/5 and protected hashes |
| `make learning-contracts-check api-contracts-check evidence-contracts-check` | I5-03 + I5-01 | Stage A + binding primary gate, API/base evidence | fitness v2 plus inherited evidence |
| `make lesson-check LESSON=promotion-trust` | I5-03 | promotion manifest + binding/fixture identity | lesson fitness result |
| `make data-contracts-check migration-contracts-check` | I5-01 read-only | base data/readers/migration | inherited 19/19 + 1/1 |
| `make help` | root/base registry read-only | command ownership/composition unchanged | target/owner inventory |
| `make evidence-verify EVIDENCE="$EVIDENCE_LOCATOR"` | I5-03 | verify emitted binding-aware evidence | verification result |
| `git diff --check` | Git | whitespace hygiene | exit 0 |

No other implementation command is admitted. Final release additionally runs declarative
hash/path/S3/resource/rollback scans described in Phase 3.

## STOP Conditions

- wrong/dirty/divergent input, live ref, ancestry, or active conflicting shared writer;
- any hash/path/version differs from the pinned input or a protected/unlisted tracked path changes;
- mapping requires a fourth alias, value/default transform, record copy, registry/manifest/OpenAPI/
  Make change, generated type, portal, runner, data pipeline, or new dependency;
- browser can validate/authorize/mutate/complete/emit or server/completion authority drifts;
- missing required tool/result/evidence, test weakening, nondeterminism, resource breach, S3 hit,
  unsafe cleanup, or rollback cannot retain Stage A/binding/readers/evidence;
- exact-head independent review, repository check, human approval, or observed remote release
  identity is missing/mismatched.
