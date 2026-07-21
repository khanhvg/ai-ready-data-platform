---
title: "Issue #13 Requirements and Traceability"
status: planned-validated
issue: 13
created: "2026-07-22"
---

# Issue #13 Requirements and Traceability

## Functional Requirements

| ID | Requirement | Acceptance |
|---|---|---|
| FR-01 | Preserve Docker-free core | `make health`, `make dbt`, `make bi` or exact released equivalents run without Docker, cloud, socket, sudo, or privileged services |
| FR-02 | Admit only inventoried service groups | Current groups are exactly `orchestration`, `lake`, `governance`; future additions require exact released service/image amendment |
| FR-03 | Validate request grammar before startup | Empty, missing, duplicate, unknown, malformed, unauthorized pair, all-three, and over-budget selections deny before supported Compose invocation |
| FR-04 | Validate dependency closure | Recursively expanded services/profiles/ports/volumes/networks equal the exact allowlist; no silent dependency activation |
| FR-05 | Require configured bounds | Every service has memory, CPU, PID, disk, log, start/ready/exit and stop deadlines, port and volume/project ownership |
| FR-06 | Enforce aggregate baseline | Single group `<=6 GiB/4 CPUs`; exact `lake+governance` pair `<=10 GiB/6 CPUs`; host reserve `>=4 GiB/2 CPUs`; all three always denied |
| FR-07 | Measure practical cold/warm evidence | One cold plus two warm sequential repetitions per admitted actual scenario after readiness; no large matrix or fake workload |
| FR-08 | Report engine unavailability honestly | Docker-free core/static checks remain independent; required heavy acceptance is blocked/non-zero without admitted engine/images/tools |
| FR-09 | Teardown by ownership | Delete only exact run-owned project/container/network/ephemeral volume/temp/process/port/log state; preserve evidence, retained state and foreign sentinels |
| FR-10 | Publish strict evidence | `.artifacts/evidence/local-profiles/<run-id>/` contains exact authorities, normalized host/engine/image/config/tool inputs, commands/results, capped raw+summary measurements, rollback/teardown, strict locators/hash index/completion within the 512 MiB run cap |
| FR-11 | Use released completion/evidence authority | Do not reuse owner-fixed current schema or invent fields/SHAs; exact authority recorded in dependency amendment |
| FR-12 | Preserve compatibility and rollback | Additive schema/config evolution, N-1 readers, exact rollback point, no lossy conversion or protected-contract edit |
| FR-13 | Require exact-head human approval | Human approval names the exact final clean head and completed evidence index hash; any later commit requires re-review |

## Non-Functional Requirements

| ID | Requirement | Gate |
|---|---|---|
| NFR-01 | 16 GiB Mac friendly | Static aggregate/host reserve gates plus normalized Stage B evidence |
| NFR-02 | Deterministic/fail-closed | Canonical request/closure/config hash; missing/ambiguous input denies |
| NFR-03 | Non-flaky performance | Static hard bounds primary; raw repeated evidence corroborates; no single timing/RSS equality oracle |
| NFR-04 | Security S3 | Full threat model, negative tests, digest/SBOM/signature policy, protected hashes, no portal Docker socket |
| NFR-05 | Portable and honest | Record architecture/engine allocation/tool versions; unsupported arm64/amd64 or accounting is blocked with remediation |
| NFR-06 | Bounded execution | Per-service start/stop deadlines, parent teardown deadlines, PID/disk/log/sample/evidence caps and zero acceptance restarts |
| NFR-07 | Maintainability | One declarative profile source; thin scripts; root Make remains protected; no speculative abstraction/service |
| NFR-08 | Evidence integrity | Private atomic publication, raw retained, canonical summary/index, tamper/replay detection |
| NFR-09 | Recovery isolation | Idempotent owner-scoped cleanup and actual foreign sentinel preservation |
| NFR-10 | No cloud expansion | No AWS/Terraform/cloud/credential action or claim |

## Stage Gates

| Gate | Required exact inputs | Allowed work | Exit |
|---|---|---|---|
| Plan validation | Exact planner output SHA only | Plan/static/link/dependency/hash/placeholder/threshold/traceability checks; validation-only commit/push and issue transition | Independent validation passes; ready for fresh plan audit |
| Stage A entry | Passing merged #10; released/admitted #12; actual portal/runner/lab/image/command/completion/allowlist authorities; clean descendant input; amendment validated/audited | Characterization, RED tests, static admission/config/Compose/scripts/Make fragment only | All static gates GREEN at exact Stage A head; no container needed/started |
| Stage B entry | Exact Stage A head; admitted engine allocation, images, SBOM/signature/provenance, tools, real workloads | Sequential cold/warm runs and ownership-scoped teardown | Complete raw+summary+recovery evidence or typed block |
| Release handoff | Stage A/B evidence, dependency and golden blast radius, exact-head human review | Bounded docs and Issue #5 Phase 13 handoff | No protected drift; exact rollback; exact head/index approved; ready for separate release process |

## Requirement-to-Test/Evidence Traceability

| Requirement | RED/characterization IDs | Phase | Fitness/verification | Evidence locator class |
|---|---|---:|---|---|
| FR-01 | `LP-CHAR-CORE-001` | 1, 5 | `make health dbt bi`; exact #10/#12/golden blast radius | `commands/core-*` |
| FR-02/03 | `LP-ADM-INVALID-001`, `LP-ADM-MISSING-002`, `LP-ADM-DUPLICATE-003`, `LP-ADM-UNKNOWN-004`, `LP-ADM-ALL-THREE-005` | 2, 3 | `make compose-check profile-budget-check` | `static/admission-*` |
| FR-04 | `LP-ADM-DEPENDENCY-EXPANSION-007` | 2, 3 | `make compose-check` | `static/closure.json` |
| FR-05/06 | `LP-BUDGET-LIMIT-OMISSION-006`, `LP-BUDGET-OVER-AGGREGATE-022`, `LP-SEC-LOG-UNBOUNDED-010`, `LP-SEC-PID-UNBOUNDED-011`, `LP-READY-TIMEOUT-MISSING-012`, `LP-ADM-GUARDED-PAIR-013` | 2, 3 | `make compose-security-check profile-budget-check` | `static/budgets.json`, `static/security.json` |
| FR-07 | `LP-EVIDENCE-SCHEMA-014` plus Stage B actual repetitions | 2, 4 | `make profile-budget-check` | `measurements/<scenario>/<rep>/{samples,summary}` |
| FR-08 | `LP-ENGINE-UNAVAILABLE-015` | 2, 4 | `make profile-budget-check recovery-test` | typed command result; no samples |
| FR-09 | `LP-SEC-PORT-COLLISION-008`, `LP-SEC-VOLUME-COLLISION-009`, `LP-RECOVERY-FOREIGN-SENTINEL-016` | 2, 5 | `make recovery-test` | `recovery/{ownership,teardown,residue,rollback}` |
| FR-10/11 | `LP-EVIDENCE-SCHEMA-014`, `LP-EVIDENCE-INTEGRITY-021` | 2, 4, 5 | released evidence verifier plus four issue commands | `authorities.json`, `index.json`, completion |
| FR-12 | N-1/migration/tamper cases | 5 | exact released migration/evidence check | `migration/n-1.json`, `rollback/result.json` |
| NFR-04 | `LP-SEC-INTERPOLATION-017`, `LP-SUPPLY-IMAGE-018`, `LP-SEC-HOST-019`, `LP-SEC-PATH-020` | 2, 3, 5 | `make compose-security-check` | `security/*` |
| NFR-09 | collision/sentinel/interrupted teardown cases | 2, 5 | `make recovery-test` | `recovery/*` |
| FR-13 | exact-head/index approval assertion | 5 | human review record checked by release handoff | released approval locator recorded by the dependency amendment |

## Exact Future Verification Contract

After release authority exists and Stage B is available:

```bash
make compose-check compose-security-check profile-budget-check recovery-test
```

Also run exact dependency-amended blast radius:

- passing merged Issue #10 Docker-free real journey commands;
- released Issue #12 lab/data-contract/golden commands;
- current `make health dbt bi` unless exact released equivalents supersede them;
- protected golden/shared-contract/migration checks named by the exact dependency release.

The dependency amendment must list commands verbatim with owner and SHA. No future command is
invented here. Missing required commands/tools are blocked/fail, not optional pass.

## Acceptance Traceability to User Decisions

| User acceptance decision | Plan contract |
|---|---|
| Docker-free core primary | FR-01; Phase 1/5 regression; no engine dependency |
| Static limits primary | Resource model decision hierarchy; Phases 2/3 before Phase 4 |
| 4 GiB/2 CPU reserve and aggregate ceilings | FR-06; exact current group mapping |
| One cold + two warm, normalized | FR-07; minimal four-scenario matrix |
| Engine absent blocks heavy only | FR-08; no sample fallback |
| No silent dependencies/invalid requests | FR-03/04; explicit RED matrix |
| Ownership-safe teardown | FR-09; actual foreign sentinel required |
| S3 full boundary | NFR-04; threat model TM-01..TM-20 |
| Released evidence authority | FR-10/11; current owner-fixed schema not reused |
| Additive/N-1/rollback | FR-12; Phase 5 |
| Human exact-head review/approval | FR-13; Phase 5; any later commit invalidates approval |

## Out of Scope

- Implementing this plan or performing readiness in the planner/validation sessions.
- Starting/building/pulling containers or probing engine state during planning.
- Creating portal, runner, lab, shared contract, architecture, migration, release, or golden code.
- Changing root Make, code standards, root release manifest, dataset/mart/lineage/Rill/Airflow/lake
  semantics, or unrelated Compose.
- AWS, Terraform, cloud, hosted, AI, production cost/readiness, PR, merge, or release action.
