# Requirements and Discovery Traceability

## Traceability Rules

- A requirement is implementation-ready only when it has an owner, architecture view, ADR,
  implementation issue, test/fitness command, and retained evidence.
- A TBC is a blocker only for the boundary named in its row. AWS budget/RTO TBCs do not block the
  local portal.
- Planned commands become tracked, discoverable Make targets during implementation and emit
  machine-readable results under `.artifacts/evidence/` (ignored runtime output).
- Discovery IDs never disappear. Canonical accepted findings are `PH-C01..PH-C10` and
  `PH-H01..PH-H14`.

## Requirement Catalogue

### Business Outcomes and Capabilities

| ID | Outcome/capability | Measure |
|---|---|---|
| BO-01 | Learner connects architecture to a retail decision | Complete promotion-trust journey with verifier evidence |
| BO-02 | Learner diagnoses and recovers safely | Controlled failure identified; reset/replay preserves golden base |
| BO-03 | Maintainer can evolve local to hosted/AWS without rewriting learning contracts | Same lesson/evidence/data-product contract passes adapter suites |
| BO-04 | Architecture claims are executable | C4/API/data/security/resource/cost/recovery fitness results retained |
| BO-05 | Core learning stays accessible and credential-free | Clean machine/local E2E with no AWS/model credential/network dependency beyond installation |
| CAP-01 | Curriculum and competency management | Acyclic prerequisites, versioned lesson schema, remediation |
| CAP-02 | Lab execution and workspace lifecycle | Typed commands, isolated workspace, state/idempotency/reset |
| CAP-03 | Progress, verification, and evidence | Versioned state, deterministic verifier, integrity and retention |
| CAP-04 | Architecture assets and decisions | C4/dynamic/deployment views, ADRs, traceability |
| CAP-05 | Data platform and governance | Generator→DuckDB→dbt→Rill/Iceberg/OpenMetadata contracts |
| CAP-06 | Local runtime profiles | Admission, health, metrics, teardown |
| CAP-07 | AWS platform | Network/IAM/state/ECS schedule/data/BI/governance; non-applying first |
| CAP-08 | Optional governed AI | Admission, retrieval/evals/approval/recovery/cost |

### FR / NFR / ASR

| ID | Type | Requirement | Acceptance boundary |
|---|---|---|---|
| FR-01 | FR | Render versioned lessons, prerequisites, diagrams, decisions, progress, status and evidence | First journey |
| FR-02 | FR | Run allow-listed prepare/generate/load/dbt/export/configure/verify/reset operations | First journey |
| FR-03 | FR | Generate deterministic retail fixtures and preserve 18-table anomaly/mart/lineage/metric contracts | Shared core |
| FR-04 | FR | Complete failure→diagnose→reset→verify→evidence state flow | First journey |
| FR-05 | FR | Deep-link to Rill/OpenMetadata/Airflow/Superset with consistent status vocabulary | Relevant profile/wave |
| FR-06 | FR | Render/validate local and AWS architecture views and ADR traceability | Architecture waves |
| FR-07 | FR | Validate non-applying Terraform and AWS adapter contracts | AWS waves |
| FR-08 | FR | Admit AI labs only after governed-data and safety gates | Optional AI |
| NFR-01 | NFR | Credential-free, loopback-only first release | Local core |
| NFR-02 | NFR | Fits 16 GiB laptop through measured mutually exclusive profiles | Local release |
| NFR-03 | NFR | WCAG 2.2 AA target; keyboard/screen-reader/200%/reduced-motion/static equivalence | Every portal release |
| NFR-04 | NFR | Deterministic, tamper-detecting exact-SHA evidence | Every completion/release |
| NFR-05 | NFR | No arbitrary shell, traversal, repository write, secret leakage, cross-object trust | Runner/API |
| NFR-06 | NFR | Atomic/recoverable reset/publish/retry with idempotency and race protection | Runner/data |
| NFR-07 | NFR | Local/AWS adapter equivalence where declared; deviations versioned | AWS admission |
| NFR-08 | NFR | Honest active/off-hours/residual cost and bounded retries | AWS/AI |
| NFR-09 | NFR | Backup/restore or deterministic rebuild meets accepted RTO/RPO | AWS apply |
| NFR-10 | NFR | Additive migration preserves unrelated user files and rollback point | Every refactor |
| ASR-01 | ASR | Modular monolith portal + isolated privileged runner | Before Phase 4 merge |
| ASR-02 | ASR | S3/Iceberg is AWS durable analytical truth; ClickHouse role explicitly admitted | Before Phase 11/apply |
| ASR-03 | ASR | Stateful authority and recovery matrix is complete | Before AWS apply |
| ASR-04 | ASR | Terraform state/account/apply trust boundary is separate and least-privilege | Before backend/apply |
| ASR-05 | ASR | AI core independence, ACL, provenance, eval, approval, durability and cost | Before Phase 12 cook |

## Architecture View Catalogue

Planned Structurizr sources live under `architecture/structurizr/`. `make architecture-check`
uses a pinned CLI to validate IDs/relationships/views; `make architecture-render` exports
reviewable SVG/PNG/text equivalents.

| View ID | Minimum view | Audience / concern |
|---|---|---|
| C4-L0 | Landscape/capability | Product owner: business outcomes, actors, capabilities and external tools |
| C4-L1 | System context | Learner/instructor/operator boundaries and local/AWS/identity/data systems |
| C4-L2-LOCAL | Local containers | Portal modular monolith, privileged runner, evidence/progress, data adapters, external UIs |
| C4-L3-RUNNER | Runner components | BFF client, policy chain, command registry, workspace manager, state/evidence writer |
| DEP-LOCAL | Local deployment | Browser/host processes, loopback/Unix socket, workspace, mutually exclusive Compose profiles |
| DYN-JOURNEY | Promotion-trust sequence | Start, controlled failure, diagnose, reset, verify, evidence |
| DYN-PUBLISH | Data publish/retry sequence | dbt/export/Iceberg/catalog commit, fault, resume/rollback |
| C4-L2-AWS | AWS containers | Ingress, portal, runner/jobs, ClickHouse, Superset, OpenMetadata and durable dependencies |
| DEP-AWS | AWS deployment | DNS/TLS/LB, VPC/subnets/routes/SG/endpoints/NAT choice, ECS/ASG, state stores |
| DYN-OFFICE | Office-hours sequence | Open capacity, hydrate/restore, readiness; drain/checkpoint/backup/zero/inventory |
| DYN-RESTORE | Recovery sequence | Empty environment restore/rebuild and equivalence gate |
| C4-L3-AI | Optional AI components | Retrieval ACL, graph/workflow, tools/approval, AgentCore and durable state |
| DYN-AI | Optional agent sequence | Retrieve/cite/evaluate/approve/tool/retry/reconcile |

No code-level C4 view is required. Component views exist only for runner and optional AI high-risk
boundaries.

## Outcome-to-Evidence Matrix

| Outcome/capability | FR/NFR/ASR | View | ADR | Phase / issue | Test or fitness function | Evidence |
|---|---|---|---|---|---|---|
| BO-01, CAP-01 | FR-01, FR-04, NFR-03 | C4-L0, DYN-JOURNEY | ADR-005 | P2/P3/P5; I5-02/I5-03/I5-05 | `make lesson-check LESSON=promotion-trust`; `make lesson-e2e LESSON=promotion-trust` | Lesson schema, axe/manual audit, Playwright trace/screenshots, completion JSON |
| BO-02, CAP-02 | FR-02, FR-04, NFR-05/06 | C4-L3-RUNNER, DYN-JOURNEY | ADR-002/006/007 | P4/P5; I5-04/I5-05 | `make runner-test`; `make runner-race-test` | State-transition log, negative-security JUnit, base-tree hash |
| BO-03, CAP-05 | FR-03, NFR-07/10 | DYN-PUBLISH, DEP-LOCAL/DEP-AWS | ADR-001/004/008/009/010 | P1/P7/P11; I5-01/I5-07/I5-11 | `make golden-clean`; `make data-contracts-check`; `make engine-equivalence` | Golden JSON, dbt manifest diff, query/metric equivalence |
| BO-04, CAP-04 | FR-06, NFR-04 | All scoped views | ADR register | P1/P6/P13; I5-01/I5-06/I5-13 | `make architecture-check`; `make traceability-check` | Render manifest, link/ID report, fitness summary |
| BO-05, CAP-06 | NFR-01/02/03 | DEP-LOCAL | ADR-006/008/009 | P5/P8/P13; I5-05/I5-08/I5-13 | `make local-journey-e2e`; `make profile-budget-check` | Resource JSON, browser evidence, credential/network scan |
| CAP-07 | FR-07, NFR-08/09, ASR-02/03/04 | C4-L2-AWS, DEP-AWS, DYN-OFFICE/RESTORE | ADR-010..016 | P9-P11; I5-09/I5-10/I5-11 | `make terraform-check`; `make aws-adapters-contract`; credential-gated `make terraform-plan-aws` | Static/policy/mock plan, priced BOM, restore/equivalence evidence |
| CAP-08 | FR-08, ASR-05 | C4-L3-AI, DYN-AI | ADR-019/020 | P12; I5-12 | `make ai-admission-check`; optional `make ai-evals` | Admission JSON, eval report, trace/redaction/replay evidence |

## Fitness Function Catalogue

| Domain | Planned exact/discoverable command | Pass condition |
|---|---|---|
| Golden | `make golden-clean PROFILE=small SEED=42` | Fresh venv/cache-independent bounded run twice; schema-valid evidence; stable files/anomalies; expected dbt warning oracle |
| Architecture | `make architecture-check && make architecture-render` | Structurizr valid; required IDs/concerns present; all sources render; text alternatives exist |
| HTTP API | `make api-contracts-check` | OpenAPI lint/examples/problem/auth/idempotency; logical taxonomy complete |
| Async API | Same inventory check | No AsyncAPI unless actual channel; any actual channel has a valid contract |
| Learning contracts | `make learning-contracts-check` | Schemas, refs, prerequisites, patterns/failures, remediation and evidence IDs valid |
| Compose | `make compose-check` | Render valid; ports loopback as declared; profiles/mounts/secrets/resource policies pass |
| Terraform static | `make terraform-check` | fmt/validate/tflint/security/policy and mock `terraform test` pass; no apply target/default |
| Terraform plan | `make terraform-plan-offline`; later `make terraform-plan-aws` | Mock/non-applying plan passes; real plan credential/account/approval gated and redacted |
| Data/dbt | `make data-contracts-check` | Generator, counts/checksums/anomalies, 51-model lineage, mart schemas, warning semantics, curated list pass |
| Iceberg/metadata | `make lake-contracts-check`; `make metadata-contracts-check` | Atomic/fail-loud lifecycle, read-back, rename/delete reconciliation, lineage/entity checks |
| Frontend unit/a11y | `make portal-test`; `make portal-a11y` | Unit/schema/axe pass; keyboard/static/reduced-motion assertions |
| Browser/visual/E2E | `make portal-e2e`; `make portal-visual-review` | Real browser journey and approved screenshots across viewports/states |
| Runner security/race | `make runner-security-test`; `make runner-race-test` | Fuzz/traversal/secret/base-write/authz/replay/barrier/fault tests pass |
| Resource | `make profile-budget-check` | Supported profile matrix within thresholds; invalid combinations refused pre-start |
| Recovery | `make recovery-test` | Reset/publish/evidence recovery and base-tree integrity pass |
| Cost | `make cost-model-check` | Golden BOM cases and retry/retention/residual inventory pass; no claim while TBC |
| AI optional | `make ai-admission-check`; `make ai-evals` | All admission and owner-set eval thresholds pass |
| Full release | `make release-evidence` | Clean checkout aggregate succeeds and produces signed-off manifest of evidence artifacts |

## Accepted Critical Findings

Prediction aliases: C1→PH-C01, C2→PH-C03, C3→PH-C04, C4→PH-C05, C5→PH-C06,
C6→PH-C07, C7→PH-C02, C8→PH-C08.

| ID | Owner / issue | Acceptance criterion | Verification | Mitigation / rollback | Dependency / blocker |
|---|---|---|---|---|---|
| PH-C01 | Shared-core / I5-01 | Every issue pins main `3cd3d41…`; merge tree equals `d027373…`; discovery preserved | `git merge-base --is-ancestor 3cd3d41 HEAD`; tree equality; `make golden-clean` | Stop fan-out on base mismatch; rerun golden; rollback to immutable SHA | Resolved upstream; clean golden still required |
| PH-C02 | Shared-core / I5-01 | One credential-free clean command regenerates ignored fixtures twice and emits valid exact-SHA JSON | `make golden-clean PROFILE=small SEED=42`; JSON Schema; second clean run | Preserve historical evidence; delete only generated workspace; return to input SHA | Phase 1 blocks all refactors |
| PH-C03 | AWS persistence / I5-09/I5-11 | State matrix owns every authority, backup/rebuild, RTO/RPO, zero behavior and cost | `make state-matrix-check`; later `make aws-restore-drill` | Known-good backup/catalog pointer; local track retained | Apply blocked by ADR-010..014 |
| PH-C04 | FinOps/operations / I5-09/I5-10 | Priced active/off-hours/failure BOM; readiness SLO; residual services disclosed | `make cost-model-check`; later office open/close/resource inventory | Budget alarm/quota/kill switch; no scale-to-zero claim; local fallback | Monthly ceiling/retention/cold-start TBC block apply |
| PH-C05 | Runner security / I5-04 | Typed allow-list, isolated workspace, actor-resource-action, least privilege, no apply endpoint | `make runner-security-test`; fuzz/traversal/secret/base-tree negative suite | Disable runner; static lesson and direct expert tools remain | Local identity default accepted; hosted model deferred |
| PH-C06 | Shared-core + runner / I5-03/I5-04 | Versioned state machine, locks/idempotency, atomic reset/publish/evidence | `make runner-race-test`; barrier/fault/replay/crash suite | Journal/resume, atomic workspace pointer, quarantine partial evidence | Evidence contract precedes runner |
| PH-C07 | AI governance / I5-12 | ACL/provenance/evals/guardrails/OTel/approval/idempotency/recovery/cost all admitted; core independent | `make ai-admission-check`; credential-gated `make ai-evals` | AI off; revoke tools/indexes/traces; read-only first | Blocked by governed data, identity, runner and budget |
| PH-C08 | Product/curriculum / I5-02/I5-05 | One accessible promotion-trust journey satisfies every contract field and deterministic completion | `make lesson-e2e LESSON=promotion-trust`; novice/challenge/manual a11y | Static lesson fallback; content version rollback | Stack/contract/runner gates |
| PH-C09 | Terraform / I5-10 | Encrypted/versioned/locked state, environment/SHA binding, plan/apply roles, no apply in default paths | `make terraform-check`; mock locks/wrong-account/replay; later backend restore | Restore prior version; revoke role; separate bootstrap | Account/apply approver TBC; apply blocked |
| PH-C10 | Shared-core/release / I5-01/I5-13 | Versioned data/API/evidence/lesson mappings; additive dual-run; unrelated files preserved | `make migration-contracts-check`; generator/dbt/lineage/OpenAPI/evidence compatibility; `git status` | Adapter/feature flag; old reader/data snapshot; revert to SHA | Phase 1 contracts before migration |

## Accepted High Findings

| ID | Owner / issue | Acceptance criterion | Verification | Mitigation / rollback | Dependency / blocker |
|---|---|---|---|---|---|
| PH-H01 | Local runtime / I5-08 | Portal+browser+admitted profile fits thresholds; invalid combinations fail before start | `make profile-budget-check` cold/warm RSS/CPU/disk/network/readiness | Core/no-container fallback; automatic teardown | Measure supported machines |
| PH-H02 | Shared-core / I5-01 | Environments/images pinned; venv rebuild keyed to requirement/lock hash | Two `make golden-clean` runs; dependency/version report | Last known-good locks/images and migration notes | Phase 1 |
| PH-H03 | Data platform / I5-07 | Iceberg failure cannot report success or expose silent mixed state | `make lake-fault-test` at drop/create/catalog boundaries | Staged/snapshot swap or deterministic rebuild; prior pointer | Catalog/writer capability |
| PH-H04 | Governance / I5-07/I5-11 | Rename/delete reconciliation or per-lab reset verified | `make metadata-reconcile-test` | Catalog reset/manifest reconcile; DB backup/reingest | Version/topology decision |
| PH-H05 | Portal / I5-05/I5-11 | Consistent status/evidence/deep links; portal usable when tools down | Browser E2E for absent/starting/ready/error | Preserve direct tools; graceful portal states | Portal IA and adapters |
| PH-H06 | Portal/accessibility / I5-02/I5-05 | Semantic/static equivalents; no scroll completion | `make portal-a11y`; manual AT/keyboard/zoom/reduced-motion | Disable motion without content loss | Web stack gate |
| PH-H07 | AWS operations / I5-09/I5-10 | Explicit timezone/next-run/drain/checkpoint/override/readiness | Clock/DST/holiday simulation; active-session shutdown; failed-start recovery | Operator override; cancel close if backup fails; local fallback | Hours default; RTO/cold-start TBC |
| PH-H08 | Security/Terraform / I5-08/I5-10 | Local ports bind intentionally; AWS rejects placeholders/static secrets/broad ingress | `make compose-security-check`; `make terraform-check`; reachability/secret negatives | Separate schemas; block plan/deploy; rotate/revoke | Network/IAM design |
| PH-H09 | Data adapters / I5-11 | Declared DuckDB/ClickHouse outputs equivalent; deviations versioned | `make engine-equivalence` with null/timezone/type/metric cases | Keep local golden adapter; reject AWS readiness | ClickHouse/dbt/catalog spike |
| PH-H10 | AI operations / I5-12 | Retry/time/concurrency/spend/idempotency limits visible and enforced | Retry storm/delayed success/duplicate/cost kill-switch evals | Disable add-on; cancel/reconcile | PH-C04/06/07 |
| PH-H11 | Evidence / I5-01/I5-13 | Evidence captures env/tools/commands/SHA/verifier and is CI-retainable/tamper-detecting | `make evidence-contracts-check`; retention/tamper/clean rerun | Preserve raw prior evidence; never overwrite run | PH-C02 |
| PH-H12 | Repository / I5-01 | `release-manifest.json` excluded from product contract and not removed without owner evidence | Consumer/provenance check; tracked-path comparison | Preserve unchanged | Separate cleanup decision |
| PH-H13 | Runner/Airflow / I5-04/I5-07 | Learner jobs cannot write repository/control files; scoped workspace/output only | Negative write attempts; before/after `git status` and tree hash | Read-only base mounts; disable integration | Workspace seam refactor |
| PH-H14 | Portal / I5-02 | Three serious stacks scored with same lesson; winner recorded before portal build | `make web-spike-scorecard-check`; bundle/RSS/start/a11y/E2E artifacts | Discard spike directories/branches; retain contract/evidence fixture | Fixed first narrative |

## Scenario Traceability

| Scenario | Severity | Owning issue | Test/evidence | Recovery |
|---|---|---|---|---|
| SC-01 novice misreads failure | High | I5-05 | prerequisite/warning/remediation Playwright route | progress unchanged; guided reset |
| SC-02 parameter escapes boundary | Critical | I5-04 | property fuzz, traversal, subprocess argv spy, secret canary | reject pre-execution; destroy workspace |
| SC-03 reset races publish | Critical | I5-04/I5-07 | barrier at every write boundary; pointer/base checksum | serialize or rollback journal |
| SC-04 laptop overcommit | High | I5-08 | forced profile matrix and measured cold/warm resource JSON | pre-start denial/teardown |
| SC-05 scale-to-zero loses state | Critical | I5-09/I5-11 | empty-start restore/rebuild, dashboard/catalog/query checks | restore known-good or keep not-ready |
| SC-06 no cloud/optional tools | High | I5-05/I5-13 | network-disabled/no-AWS/absent-tool local E2E | optional skip; local core remains |
| SC-07 partial catalog cascade | Critical | I5-07/I5-11 | seam partitions, replay same key, consistency oracle | bounded resume or previous pointer |
| SC-08 cross-learner access | Critical | Later hosted I5-14 | cross-user/ID enumeration/role-expiry matrix | default deny; revoke session |
| SC-09 golden semantic drift | Critical | I5-01 | bytes/anomalies/schema/marts/lineage/metrics | stop migration; revert SHA |
| SC-10 catalog client mismatch | High | I5-11 | disposable catalog lifecycle + SigV4/IAM negatives | reject adapter; keep local |
| SC-11 PII/secrets in traces | Critical | I5-12 / hosted I5-14 | canary/redaction/deletion/retention tests | delete/reindex/revoke; AI off |
| SC-12 AWS/agent exceeds budget | High | I5-09/I5-12 | golden cost cases, retry storm, quota/teardown | kill switch and residual inventory |
| SC-13 concurrent/stolen apply | Critical | I5-10 | mock/real lock, wrong role/account, approval replay | no apply; restore/revoke |
| SC-14 resume after crash | High | I5-03/I5-04 | browser/process crash/reload, repeated reset | last committed state; recover/reset |
| SC-15 delayed duplicate effect | High | I5-12 | delayed success, replay, approval expiry, accounting | reconcile uncertainty before retry |
| SC-16 forged completion | High | I5-03/I5-05 | edited solution/evidence, SHA/verifier mismatch | reject completion; audit |
| SC-17 schedule timezone/active work | High | I5-10 | clock/holiday/override/drain/readiness simulation | override; cancel close on unsafe state |
| SC-18 corrupt backup | Critical | I5-09/I5-11 | scheduled empty restore, hashes/queries/search/dashboard | previous known-good; rollback migration |
| SC-19 inaccessible motion | Medium retained | I5-02/I5-05 | axe + manual AT/keyboard/zoom/reduced-motion/static | motion disabled, content preserved |
| SC-20 moving baseline | High | I5-01/I5-13 | SHA preflight, three-way diff, clean golden rerun | stop/rebase/rehearse/revert |

SC-08/SC-11 hosted multi-user portions are explicitly deferred, not waived. The first local
release still implements object-shaped IDs, no direct runner access, same-user isolation, and
secret/trace hygiene so hosted evolution does not require a contract break.

## Clean-Checkout Evidence Contract

Future command:

```bash
make golden-clean PROFILE=small SEED=42
```

It must:

1. refuse dirty or wrong-base inputs unless an explicit diagnostic mode is used;
2. build an environment keyed to lock hashes, not an existing `.venv` sentinel;
3. generate two independent ignored fixture directories;
4. compare all 18 CSV bytes, row counts, checksums, and anomaly summaries while allowing only
   `generated_at` to differ;
5. load DuckDB, run `dbt build`, assert the expected warning oracle, generate docs, export all
   11 curated marts, and validate Rill/dbt/curated-list contracts;
6. capture current SHA, golden main SHA, tree status, commands, tool versions, durations,
   resources, assertion IDs and artifact SHA-256 values;
7. validate `evidence.json` against `learning/contracts/evidence.schema.json`;
8. exit non-zero on drift and leave only ignored, deletable runtime artifacts.

Historical `docs/verification/GH-3-full-flow-evidence.md` remains valid historical evidence.
It is not substituted for the new tracked command.
