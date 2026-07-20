# Implementation Issue Graph

## Authorization Boundary

This is a proposed follow-up graph, not authorization to create/cook the issues. Independent plan
validation and readiness audit must approve the master plan first. No issue may apply Terraform
or create cloud resources unless a later owner explicitly authorizes that separate action.

Every implementation issue must record:

- immutable main input `3cd3d41f71582774e8d9656a51d1044035f4503c`;
- reviewed tree head `d0273731a5077cc17c2f4398057623b83a50bb65`;
- discovery SHA `d3ce0c5832cca4f1b68299cbba111e7cc6c7a430`;
- immutable planner input `8ec96f92245c679d019ac3648c5c2d77a49f0429`, independent validation
  output SHA, and later readiness-audit output SHA;
- files it exclusively owns, public contracts it consumes, and exact evidence command.

Every implementation issue inherits `risk:high`, `tdd`, and `security:S3` from the epic even when
its additional labels express a narrower specialty. `security:S3` requires a written disposition
of the epic S3/data-security threat model; it does not imply every issue touches AWS. Every merge
also requires the owner-mandated human pre-merge approval. An issue body may not weaken these
inherited gates.

## Shared-Core Owner

**I5-01 owner is the shared-core owner through the first local release.** Exclusive contracts:

- `learning/contracts/**`
- `contracts/openapi/**` and any future `contracts/asyncapi/**`
- `contracts/data/**`
- architecture workspace/manifest schema, required IDs and include interfaces
- evidence schema/canonicalization/version registry
- golden baseline command/evidence envelope
- mappings for generator anomalies, dbt/marts/lineage/Rill metrics, and
  `lake/curated_assets.json`

I5-03 is a sequential write lease held by the same shared-core owner in the same long-lived
shared-core worktree after I5-01 merges. It is not a second concurrent owner or worktree. Other
issues consume released versions and must not edit the same contract in parallel. Contract
changes use additive-first versioning, compatibility tests, a migration note, and a new exact
contract release SHA before downstream work resumes.

## Dependency Graph

```text
Validation + readiness audit
        +--> I5-01 Golden/shared core --------+
        +--> I5-02 Representative web spike --+--> I5-03 Lesson/lab/evidence contracts
                                                      |
                                                      +--> I5-04 Privileged runner
I5-02 + I5-03 + I5-04 -------------------------------> I5-05 Portal slice
                                                           |
                                                           +--> I5-06 Curriculum/C4
                                                           +--> I5-07 Data guided labs
I5-05 + I5-07 ---------------------------------------> I5-08 Local profiles
I5-05 + I5-06 + I5-07 + I5-08 ----------------------> I5-13 Local release

I5-01 + I5-06 --> I5-09 AWS decisions --> I5-10 Terraform (no apply)
                                      \--> I5-11 AWS adapters (no apply)

I5-07 + I5-09 + I5-11 + I5-14(hosted identity, later) --> I5-12 Optional AI
```

AWS decision work does not block I5-02 through I5-08. AWS apply remains blocked regardless of
whether I5-09 through I5-11 merge.

## Wave and Parallelization Strategy

| Wave | Issues | Parallelism | Merge rule |
|---|---|---|---|
| 0 | I5-01, I5-02 | Start in parallel with disjoint ownership; I5-02 uses historical/contract fixture until I5-01 emits real golden fixture | I5-02 decision ADR cannot merge before real fixture check from I5-01 |
| 1 | I5-03, I5-04, I5-05 | Sequential contract→runner→portal integration; portal-only shell work may start after I5-02, but no product expansion merges before the runner-backed journey | Wave exits only when `make local-journey-e2e` passes the real promotion-trust journey |
| 2 | I5-06, I5-07 | Parallel only after I5-05 E2E; distinct architecture/curriculum vs data-lab ownership | Shared contract changes routed sequentially through the I5-01 owner |
| 3 | I5-08, I5-13 local gates | I5-08 measures profiles; I5-13 begins release harness after I5-05 | Local release requires I5-01..I5-08 |
| AWS | I5-09 then I5-10/I5-11 | I5-10 and I5-11 parallel after decision matrix freezes interfaces | Non-applying only; no false cost/readiness claim |
| Later | I5-14 then optional I5-12 | Hosted identity before multi-user/AI authorization | Separate approval and worktrees |

The first implementation wave is explicitly optimized for a runnable learning web vertical slice,
not a complete curriculum or cloud topology.

## Branch and Worktree Strategy

After validation and a separate readiness audit both pass, create the integration branch from the
exact readiness-audit output commit. That commit must descend from this immutable planner input
and contain the discovery, planner, independent-validation, and audit artifacts:

```text
integration/issue-5-local-learning
```

Each bounded issue uses:

```text
feature/issue-5-01-golden-contract
feature/issue-5-02-web-spike
feature/issue-5-03-learning-contracts  # sequential reuse of shared-core worktree/owner
feature/issue-5-04-lab-runner
feature/issue-5-05-portal-vertical-slice
...
```

Use one sibling worktree per branch, for example
`{workspace-parent}/ai-ready-data-platform-issue-5-04-lab-runner`. Never share `.venv`,
`node_modules`, generated data, Docker project names, ports, evidence directories, or Terraform
working/state directories between worktrees. Each issue derives a unique Compose project name and
port range.

Merge policy:

1. Issue start evidence records integration input SHA, upstream merged dependency SHAs, contract
   versions, branch, and worktree. Any mismatch stops work.
2. Rebase/merge current integration branch before final verification and record the new input SHA.
3. Re-run the issue's golden/contract blast-radius commands and record issue output SHA.
4. A dependent issue starts only from the upstream issue's merged integration SHA, never its
   unmerged feature SHA.
5. Merge only through a reviewed PR with the inherited `risk:high`/TDD/security:S3/human gate.
6. Delete no old contract until dual-read/rollback acceptance passes.
7. Never force-push shared integration/main.

## Exact Dependency Matrix

| Issue | blockedBy | blocks |
|---|---|---|
| I5-01 | validation PASS, readiness-audit PASS | I5-03, I5-04, I5-07, I5-09, all refactors |
| I5-02 | validation PASS; real I5-01 fixture before ADR merge | I5-03, I5-05 |
| I5-03 | I5-01 merged, I5-02 ADR merged | I5-04, I5-05 |
| I5-04 | I5-01 and I5-03 merged | I5-05, runner-backed I5-07 |
| I5-05 | I5-02, I5-03, I5-04 merged | I5-06, I5-07, I5-08, I5-13 |
| I5-06 | I5-03 and I5-05 merged | I5-09, I5-13 |
| I5-07 | I5-01, I5-03, I5-04, I5-05 merged | I5-08, I5-11, I5-12, I5-13 |
| I5-08 | I5-05 and I5-07 merged | I5-13 |
| I5-09 | I5-01 and I5-06 merged | I5-10, I5-11; AWS apply remains separately blocked |
| I5-10 | I5-09 interface release | optional non-applying release evidence only |
| I5-11 | I5-07 and I5-09 merged; I5-10 outputs optional/read-only | I5-12; AWS readiness claim |
| I5-12 | I5-07, I5-09, I5-11 and I5-14 when multi-user is claimed | optional AI release only |
| I5-13 | I5-01..I5-08 merged | local release/owner merge decision |
| I5-14 | I5-13 and separate hosted-product decision | multi-user I5-12 claim |

## File Ownership Matrix

| Owner issue | Exclusive paths | Consumes read-only/shared |
|---|---|---|
| I5-01 | `scripts/golden/**`, `contracts/data/**`, base `learning/contracts/**`, evidence core, architecture workspace/manifest schema and required IDs, dependency locks | Current data spine |
| I5-02 | `spikes/web/**`, scorecard report, ADR-005 proposal | Golden evidence fixture + draft lesson |
| I5-03 | Sequential shared-core lease for lesson/lab/progress schemas and first manifests; same owner/worktree as I5-01, never concurrent | I5-01 evidence core, I5-02 score |
| I5-04 | `apps/lab-runner/**`, runner tests, workspace runtime config | Released contracts; existing pipeline entrypoints |
| I5-05 | Winning `apps/learning-portal/**`, portal tests | Released lesson/OpenAPI/evidence contracts; runner API |
| I5-06 | `learning/curriculum/**`, Structurizr models/views/rendered outputs, implementation ADR templates | Shared-core architecture IDs/include interfaces; portal renderer |
| I5-07 | `learning/labs/data-platform/**`, data lab verifiers; narrowly approved pipeline seams | Golden data contracts; runner registry |
| I5-08 | Compose/profile admission/resource scripts and tests | Portal/runner images; existing profiles |
| I5-09 | `docs/decisions/aws/**`, cost/state models and tests | Architecture/deployment model |
| I5-10 | `infra/aws/terraform/**`, Terraform tests/policies | Accepted I5-09 interfaces |
| I5-11 | `platform/adapters/aws/**`, `platform/images/**`, AWS adapter deployment-descriptor inputs and contract tests; never `infra/aws/terraform/**` | Data contracts + I5-09 state decisions + read-only Terraform output schema |
| I5-12 | `apps/agent-labs/**`, AI evals/policies after admission | Governed data/identity/evidence interfaces |
| I5-13 | Release evidence orchestration and tracked runbook/docs | All merged outputs; does not change their contracts |
| I5-14 | Hosted identity/tenant adapters and authz tests | Local object-shaped contracts |

## Proposed Follow-up Issues

### I5-01 — Freeze golden baseline and shared architecture contracts

- Labels: `risk:high`, `security:S3`, `tdd`, `shared-core`, `data-integrity`.
- Depends on: independent plan validation + readiness audit.
- Phase: 1.
- TDD:
  1. Write characterization tests for current generator bytes/anomalies, 18 raw tables,
     dbt warnings/51-model lineage/11 marts, Rill weighted metrics, Airflow graph,
     curated assets and historical evidence parsing.
  2. Add lock-hash environment setup, workspace path seams, `make golden-clean`, evidence
     schema/canonicalization, and architecture skeleton.
  3. Re-run current and new contract suites twice from clean generated state.
- Acceptance:
  - exact main/discovery/reviewed-tree inputs recorded;
  - `release-manifest.json` and unrelated files unchanged;
  - `docs/code-standards.md` hash-preserved if present at issue input, otherwise preservation
    manifest records `absent`; the issue never creates/overwrites/deletes it;
  - future command regenerates ignored fixtures and evidence without pre-existing venv/data;
  - preservation/migration mapping and rollback manifest committed.
- Verify:

```bash
make golden-clean PROFILE=small SEED=42
make data-contracts-check
make evidence-contracts-check
make architecture-check
git diff --check
```

### I5-02 — Select web stack with one representative lesson

- Labels: `risk:high`, `security:S3`, `tdd`, `frontend`, `accessibility`, `decision-gate`.
- Depends on: validated plan; may start with I5-01, merge waits for its real evidence fixture.
- Phase: 2.
- Candidates: Astro+React islands, Next.js App Router, React/Vite+typed API.
- TDD: shared interaction/a11y/E2E test first; implement same lesson in time-boxed spikes; capture
  bundle/start/RSS/JS/a11y evidence; accept ADR-005.
- Acceptance: all must-pass criteria; weighted score; tie rule; no copied proprietary content;
  spike directories removable with no contract loss.
- Verify: `make web-spike-scorecard-check`, candidate unit/a11y/Playwright commands recorded in
  the scorecard.

### I5-03 — Version lesson, lab, progress and evidence contracts

- Labels: `risk:high`, `security:S3`, `tdd`, `shared-core`, `api`.
- Depends on: I5-01, ADR-005 evidence from I5-02.
- Phase: 3.
- TDD: failing schema/ref/state/tamper/migration fixtures first; implement JSON Schemas, OpenAPI,
  state machine and evidence canonicalization; add backward-reader tests.
- Acceptance: complete contract from `lesson-lab-contract.md`; logical API taxonomy; no AsyncAPI
  without a channel; promotion-trust manifest validates.
- Verify: `make learning-contracts-check api-contracts-check evidence-contracts-check`.

### I5-04 — Build isolated privileged local runner

- Labels: `risk:high`, `security:S3`, `tdd`, `backend`.
- Depends on: I5-01, I5-03.
- Phase: 4.
- TDD: argv/path/env/quota/base-write/race/crash/idempotency negatives first; implement runner;
  new behavior tests; full data-contract regression.
- Acceptance: loopback/private transport, no direct browser credential, `shell=false`, typed
  commands, read-only base, atomic workspace, no Terraform apply command, auditable state.
- Verify:

```bash
make runner-test
make runner-security-test
make runner-race-test
make data-contracts-check
```

### I5-05 — Deliver runnable promotion-trust portal slice

- Labels: `risk:high`, `security:S3`, `tdd`, `frontend`, `accessibility`, `vertical-slice`.
- Depends on: I5-02, I5-03, I5-04.
- Phase: 5.
- TDD: component/state/a11y/real-browser journey tests first; implement portal modular monolith and
  BFF; integrate actual runner/data products; run manual AT/visual review.
- Acceptance: business question→raw/model/DQ→decision→reset→verified product→evidence; no cloud
  credential; static/reduced-motion path; external-tool unavailable states.
- Verify:

```bash
make portal-test portal-a11y
make lesson-e2e LESSON=promotion-trust
make local-journey-e2e
make portal-visual-review
```

### I5-06 — Publish architecture curriculum, templates and fitness functions

- Labels: `risk:high`, `security:S3`, `tdd`, `architecture`, `curriculum`.
- Depends on: I5-03 and passing, merged I5-05 real journey; no portal-source overlap.
- Phase: 6.
- TDD: broken-reference/prerequisite/view/ADR/pattern-without-failure fixtures first.
- Acceptance: foundation→mid competency graph, templates, minimum useful C4 sources, render/text
  equivalents, requirement/ADR/test traceability, pattern admission rules.
- Verify: `make curriculum-check architecture-check architecture-render traceability-check`.

### I5-07 — Add data-pipeline guided labs without changing golden semantics

- Labels: `risk:high`, `security:S3`, `tdd`, `data-platform`, `recovery`.
- Depends on: I5-01, I5-03, I5-04 and passing, merged I5-05 real journey.
- Phase: 7.
- TDD: current warning/mart/lineage/publish/catalog behavior first; add labs and fail-loud seams;
  regression/equivalence after.
- Acceptance: labs for deterministic ingest/model/quality, orchestration, metric weighting,
  Iceberg commit/recovery, OpenMetadata reconciliation; every service/pattern has a failure.
- Verify: `make data-labs-e2e lake-fault-test metadata-reconcile-test data-contracts-check`.

### I5-08 — Enforce local profiles and resource budgets

- Labels: `risk:high`, `security:S3`, `tdd`, `performance`, `compose`.
- Depends on: I5-05, I5-07.
- Phase: 8.
- TDD: invalid profile combinations and measurement schema first; implement admission/telemetry;
  cold/warm profile matrix.
- Acceptance: core+portal and each admitted heavy profile fit approved thresholds; all-three
  denied; guarded co-run measured; ports/mounts/credentials local-only; teardown clean.
- Verify: `make compose-check compose-security-check profile-budget-check recovery-test`.

### I5-09 — Decide AWS state, cost, persistence and readiness

- Labels: `risk:high`, `security:S3`, `tdd`, `decision-gate`, `aws`, `finops`, `recovery`.
- Depends on: I5-01, I5-06. Does not block local issues.
- Phase: 9.
- TDD: incomplete state/cost/TBC matrices fail schema tests; cost golden cases first.
- Acceptance: state authority matrix; ClickHouse alternatives; catalog/metadata/search options;
  active/off-hours/failure BOM; apply TBCs explicit; no false zero-cost claim.
- Verify: `make state-matrix-check cost-model-check aws-decision-check`.

### I5-10 — Build non-applying Terraform platform modules

- Labels: `risk:high`, `security:S3`, `tdd`, `terraform`, `no-apply`.
- Depends on: I5-09 accepted design interfaces.
- Phase: 10.
- TDD: policy/mock tests for network/IAM/state/schedule/wrong-account first; build modules; run
  static/mock/non-applying plan checks.
- Acceptance: networking, IAM, state backend contract, ECS EC2 capacity, office workflow,
  observability/budget/teardown outputs; no default/apply path.
- Verify: `make terraform-check terraform-plan-offline`; real `make terraform-plan-aws` remains
  credential and owner gated.

### I5-11 — Prove AWS ClickHouse/Superset/OpenMetadata/S3-Iceberg adapters

- Labels: `risk:high`, `security:S3`, `tdd`, `aws`, `data-platform`, `persistence`, `no-apply`.
- Depends on: I5-07 and I5-09; consumes an I5-10 output schema read-only when present; spikes may
  run locally/disposable only and never edit Terraform-owned paths.
- Phase: 11.
- TDD: local contract fixtures and incompatibility cases first; adapter lifecycle/equivalence;
  recovery readiness tests.
- Acceptance: validated catalog choice; ClickHouse role evidence; Superset/OpenMetadata state and
  restore contract; versioned divergences; no cloud resource created by default.
- Verify: `make aws-adapters-contract engine-equivalence metadata-contracts-check`; credential
  gated restore drills later.

### I5-12 — Optional governed AI admission and learning add-on

- Labels: `risk:high`, `security:S3`, `tdd`, `ai`, `optional`, `cost`.
- Depends on: I5-07, I5-09, I5-11, hosted identity I5-14 where multi-user ACL is claimed.
- Phase: 12.
- TDD: ACL/prompt-tool injection/citation/redaction/approval/replay/crash/cost evals first.
- Acceptance: admission JSON all green; explicit LangGraph/Restate/AgentCore responsibilities;
  local core unchanged; read-only first use case.
- Verify: `make ai-admission-check`; optional credential-gated `make ai-evals`.

### I5-13 — Produce clean-checkout release, recovery and rollback evidence

- Labels: `risk:high`, `security:S3`, `tdd`, `release`, `evidence`.
- Depends on: I5-01..I5-08 for local release; includes merged non-applying AWS checks when present.
- Phase: 13.
- TDD: release manifest schema and stale/forged evidence failures first; aggregate checks; run from
  clean checkout twice; review docs/rollback.
- Acceptance: all gates pass, exact SHAs captured, browser/manual evidence retained, rollback
  rehearsed, runtime artifacts ignored, no product contract drift.
- Verify: `make release-evidence`, `git diff --check`, clean status, plan-defined evidence
  manifest.

### I5-14 — Hosted multi-user identity and tenant evolution (later)

- Labels: `risk:high`, `security:S3`, `tdd`, `identity`, `hosted`.
- Depends on: local release I5-13 and separate product decision.
- Not required for first local release. Owns IdP/session/tenant/object authorization, per-lab
  workspace quotas, instructor/operator roles, deletion/retention, and cross-user tests.
- Verify: `make hosted-authz-test hosted-isolation-test`.

## Per-Issue Acceptance Template

Every follow-up issue body must include:

1. Expected files/behavior and explicit out-of-scope.
2. Tests-before characterization and failure fixture.
3. Implementation/refactor steps with exclusive ownership.
4. Tests-after plus blast-radius regression commands.
5. Security/resource/accessibility/recovery evidence as applicable.
6. Migration and rollback from exact input SHA.
7. Machine-readable evidence path and schema version.
8. STOP/TBC conditions and who may clear them.
9. Confirmation that product code, cloud apply, merge, and issue-state transitions remain outside
   the issue unless explicitly authorized.
