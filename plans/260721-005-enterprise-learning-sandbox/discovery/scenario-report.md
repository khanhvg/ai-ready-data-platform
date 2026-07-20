# Scenario Report: Enterprise Architecture Learning Sandbox

## Method and Bounds

Applied `ck:scenario` to the complete issue #5 proposal in bounded mode with
`--iterations 20`. Exactly one candidate was generated, classified and logged per iteration.
Dimension rotation covered all 12 dimensions before combination, negation, amplification,
persona-shift and temporal-shift variants. All 20 were kept: 12 new situations and 8 meaningful
variants; no duplicates or low-value candidates inflated the matrix.

Priority order: failure, security, scale, persistence, cost, learner UX, local resource budget,
migration and rollback.

## Bounded 20-Iteration Scenario Matrix

| Iteration | Dimension / strategy | Classification | Severity | Concrete trigger and flow | Expected behavior | Verification mapping |
|---:|---|---|---|---|---|---|
| 1 | User types / dimension walk | New | High | A novice starts a lakehouse lesson without prerequisites, then mistakes an intentionally injected dbt warning for a broken solution. | Portal blocks or explains missing prerequisites, labels controlled failures, provides evidence and remediation without revealing the solution early. | Persona E2E: fresh profile, prerequisite guard, warning-state snapshot, remediation path and progress unchanged until verify passes. |
| 2 | Input extremes / dimension walk | New | Critical | A learner submits shell metacharacters, traversal paths, oversized scale values or Terraform-like flags through lab parameters. | Typed schema rejects values before execution; command allow-list uses argument arrays; workspace paths remain contained; no credentials or host files are readable. | Fuzz/property tests, traversal cases, subprocess spy, workspace escape negative test and secret-canary scan. |
| 3 | Timing / dimension walk | New | Critical | Reset runs while Airflow/Iceberg publish or verification is writing, leaving a missing table or mixed evidence. | Per-lab state machine and lock reject or safely queue the conflicting action; publication is atomic/recoverable; evidence identifies the committed run. | Concurrency test with barriers at every write boundary; fault injection between publish steps; post-reset golden checksum and catalog-pointer assertion. |
| 4 | Scale / dimension walk | New | High | Portal, browser, Docker Desktop and a learner accidentally start Airflow, lake and governance on a 16 GiB laptop. | Profile admission prevents incompatible co-run, displays estimated/actual budget, and offers staged alternatives before OOM or host thrash. | Automated profile-matrix test plus measured cold/warm RSS, CPU, disk and start time; forced over-budget denial. |
| 5 | State transitions / dimension walk | New | Critical | ECS tasks and EC2 capacity reach zero, then ClickHouse, Superset or OpenMetadata returns with missing metadata/data/search state. | Every component follows its declared state policy: stateless restart, durable reconnect, or deterministic rebuild; readiness waits for restore/reindex and validates RPO. | Stop-to-zero/start drill, backup restore, object/count/hash comparison, dashboard/catalog login and RTO measurement. |
| 6 | Environment / dimension walk | New | High | Core learner has no AWS credentials, intermittent network, arm64 laptop or missing optional Rill/agent tools. | Credential-free local core still completes; optional steps are clearly skipped; architecture and verification remain available offline where promised. | Clean arm64/amd64 matrix, network-disabled core E2E, absent-tool tests and no-AWS-environment secret scan. |
| 7 | Error cascades / dimension walk | New | Critical | S3/catalog write succeeds but catalog pointer, OpenMetadata ingest or downstream verification times out; retries amplify a partial state. | Workflow records stage outcomes, retries only idempotent operations, never reports success on partial state, and offers bounded resume or rollback. | Network-partition/toxicity test at each seam; replay with same run/idempotency key; catalog and data consistency oracle. |
| 8 | Authorization / dimension walk | New | Critical | One hosted learner guesses another workspace/run/evidence ID or invokes an instructor/reset/solution endpoint. | Object-level authorization denies access without existence leakage; instructor and destructive roles are explicit; audit event contains no sensitive payload. | Cross-user API/E2E matrix, ID enumeration, role downgrade/expired token tests and audit-log redaction assertion. |
| 9 | Data integrity / dimension walk | New | Critical | Generator/dbt refactor preserves row totals but changes seeded bytes, anomaly semantics, mart columns or lineage identifiers. | Versioned golden contract detects drift; intentional migration requires approved mapping, dual-run evidence and rollback. | Double generation, checksums, schema/data contracts, mart snapshot comparison, dbt manifest lineage diff and old/new reader tests. |
| 10 | Integration / dimension walk | New | High | Current Glue Iceberg REST, ClickHouse, OpenMetadata or Superset drivers disagree on Iceberg version/auth/catalog behavior. | Compatibility spike fails before architecture commitment; adapter boundaries surface exact unsupported operations; local path stays intact. | Version matrix contract tests against a disposable catalog/bucket, SigV4/IAM negatives and create/read/evolve/time-travel/delete lifecycle. |
| 11 | Compliance / dimension walk | New | Critical | Synthetic or uploaded lesson data, prompts, citations and OTel traces contain PII/secrets and exceed retention or deletion promises. | Data classification drives redaction, encryption, retention and deletion across source, vector/index, traces, evidence and backups; synthetic data remains default. | Seeded canary/PII detection, deletion propagation, retention clock, backup exception documentation and trace/citation redaction tests. |
| 12 | Business logic / dimension walk | New | High | An AWS/AgentCore lab loops, retries or stays active outside office hours and exceeds the learner/tenant budget. | Per-run quota, model/tool budget, maximum duration and kill switch stop work; residual resources are itemized and alarms notify before ceiling. | Cost-estimator golden cases, forced retry storm, scheduled teardown, quota denial and post-lab resource inventory. |
| 13 | Authorization + state / combination | Variant of 8 | Critical | Two operators run Terraform against the same environment, or a learner can reach apply using a stolen plan/state artifact. | Remote encrypted versioned lock state serializes runs; plan/apply identities are separate; apply requires human approval and the intended environment/SHA. | Concurrent plan lock test, wrong-workspace/role denial, state version recovery, plan redaction and approval-token replay denial. |
| 14 | State transitions / negation | Variant of 5 | High | Learner closes the browser or host crashes during a controlled failure before reset/evidence completes, then resumes hours later. | Durable progress distinguishes lesson, lab and evidence state; resume shows last committed step; reset is safe and repeatable from any interrupted state. | Browser crash/reload, process kill, host restart simulation, repeated reset and progress/evidence state-machine tests. |
| 15 | Timing + business / amplification | Variant of 7 | High | Agent/tool timeout triggers retries while the original side effect later succeeds, producing duplicate tickets/data writes and cost. | Side-effect commands require idempotency keys and approval; uncertain outcomes reconcile before retry; budgets count attempts and results. | Delayed-success test, webhook/tool replay, outbox/inbox dedupe, approval expiry and cost-accounting assertion. |
| 16 | User types / persona shift | Variant of 1 | High | A mid-level learner or instructor skips foundation content, alters solution files, or imports prior evidence to claim completion. | Challenge/diagnostic path may skip instruction but cannot forge verification; evidence binds input SHA, environment, actor and verifier version. | Tampered solution/evidence tests, diagnostic placement flow, signature/hash validation and instructor override audit. |
| 17 | Environment + timing / temporal shift | Variant of 6 | High | Office-hours schedules cross time zones, daylight-saving changes, holidays or deployment downtime, so capacity starts/stops at the wrong local time. | Schedules use explicit IANA zone/UTC semantics, publish next-run time, include override/runbook and never terminate active work without grace/checkpoint. | Clock simulation around DST, holiday/override cases, active-session drain and readiness-SLO assertions. |
| 18 | Error cascades + data / combination | Variant of 7 | Critical | Backup reports success but is corrupt/incomplete; primary metadata/search/ClickHouse state is then lost during scale-down or migration. | Restore verification, not backup exit code, is the acceptance gate; previous known-good copy and migration rollback remain available. | Scheduled restore into empty environment, checksum/logical queries, OpenMetadata reindex, Superset asset check, RTO/RPO and failed-migration rollback. |
| 19 | Environment / persona shift | Variant of 6 | Medium | Keyboard-only, screen-reader or reduced-motion learner cannot follow scroll-linked architecture animation or reach hidden definition/evidence controls. | All content and controls have semantic order, keyboard operation, announced state and static/reduced-motion equivalent; scroll position is not completion. | axe plus manual screen-reader/keyboard audit, 200% zoom, reduced-motion snapshot and no-JS/static content check where supported. |
| 20 | Integration + migration / temporal shift | Variant of 10 | High | PR #4 merges/rebases differently after discovery or another implementation branch changes golden assets before issue #5 work starts. | Implementation refuses stale input; rebase/migration reruns golden and contract suites; unrelated work is preserved; rollback points to immutable SHA/tag. | SHA preflight, three-way diff, clean-checkout golden rerun, migration rehearsal and revert-to-baseline test. |

## Expanded Edge Conditions

The 20 iterations yielded 46 concrete edge checks. Highest-value boundaries include:

- zero/one/max-size datasets and zero-return anomaly cases;
- reset before, during and after each write/commit boundary;
- stale, missing, duplicated and forged evidence;
- task count zero while durable services remain billed;
- catalog data present with pointer absent, and pointer present with object absent;
- clean checkout versus stale `.venv`, cached images, volumes or generated fixtures;
- first cold start, warm restart, interrupted restore and version upgrade;
- local single user versus hosted learner, instructor, automation and agent identities;
- expired approvals/tokens, replayed webhooks/tools and uncertain side-effect outcomes;
- reduced motion, no optional tool, no network and no AWS credential environments.

## Coverage Matrix

| Dimension | Critical | High | Medium | Iterations |
|---|---:|---:|---:|---|
| User types | 0 | 2 | 0 | 1, 16 |
| Input extremes | 1 | 0 | 0 | 2 |
| Timing | 1 | 2 | 0 | 3, 15, 17 |
| Scale | 0 | 1 | 0 | 4 |
| State transitions | 1 | 1 | 0 | 5, 14 |
| Environment | 0 | 2 | 1 | 6, 17, 19 |
| Error cascades | 2 | 1 | 0 | 7, 15, 18 |
| Authorization | 2 | 0 | 0 | 8, 13 |
| Data integrity | 2 | 1 | 0 | 9, 18, 20 |
| Integration | 0 | 2 | 0 | 10, 20 |
| Compliance | 1 | 0 | 0 | 11 |
| Business logic | 0 | 2 | 0 | 12, 15 |

Composite dimension rows count combined scenarios in each applicable dimension; severity totals
below count each scenario exactly once.

## Progress Summaries

### Iteration 5

- Kept: 5 new, 0 variants; discarded: 0.
- Dimensions covered: 5/12.
- Edge checks: 11.
- Severity: 3 Critical, 2 High.
- Gaps: environment, cascades, authorization, integrity, integration, compliance, cost.

### Iteration 10

- Kept: 10 new, 0 variants; discarded: 0.
- Dimensions covered: 10/12.
- Edge checks: 23.
- Severity: 6 Critical, 4 High.
- Gaps: compliance, business/cost, cross-dimension migration and recovery.

### Iteration 15

- Kept: 12 new, 3 variants; discarded: 0.
- Dimensions covered: 12/12.
- Edge checks: 34.
- Severity: 8 Critical, 7 High.
- Gaps: accessibility, schedule-time semantics, corrupt-backup restore and moving baseline.

### Iteration 20

- Kept: 12 new, 8 variants; discarded: 0.
- Dimensions covered: 12/12.
- Edge checks: 46.
- Severity: 9 Critical, 10 High, 1 Medium.
- Remaining gaps are human architecture/product choices, not missing scenario dimensions.

## Severity Summary

- Critical: 9.
- High: 10.
- Medium: 1.
- Low: 0.
- Total: 20 kept scenarios across 12/12 dimensions.

## Composite Score: 1017

```text
scenarios_generated * 10                 = 20 * 10  = 200
edge_cases_found * 15                    = 46 * 15  = 690
dimensions_covered / total * 30          = 12/12*30 = 30
unique_actors_explored * 5               = 8 * 5    = 40
Critical-or-High scenarios found * 3     = 19 * 3   = 57
total                                                = 1017
```

## Saturation

Halted after exactly 20 iterations because bounded mode was requested. This was not a saturation
claim. The complete atomic log is in `scenario-results.tsv`.

## Planner Test Contract

Every Critical/High row must map to at least one automated acceptance test and an owned recovery
procedure. Cloud tests must be credential-gated and default to non-applying validation. Historical
issue #3 evidence may seed assertions but may not replace clean-checkout execution at the accepted
issue #5 base SHA.

## Unresolved Questions

- Which scenarios are required for the first local vertical slice versus later AWS/AI waves?
- Which hosted multi-user risks are deferred if the first release is explicitly single-user and
  localhost-only?
- What RTO/RPO and cost ceilings convert iterations 5, 12 and 18 into pass/fail tests?
