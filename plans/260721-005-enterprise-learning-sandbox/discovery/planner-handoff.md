# Planner Handoff for Issue #5

## Handoff Contract

- Discovery input SHA: `9bcacd7a44a33d298388dca2a8d2b398c6bb22a8`.
- Git base: `origin/main` at `45daa70b20414c5dee76a18592ab905c11443d3b`.
- Discovery verdict: **STOP for implementation**.
- Issue #5 must remain `triaged`; discovery does not authorize implementation, merge, Terraform
  apply, cloud resources, destructive migration or repository rewrite.
- The next planner runs in a fresh phase and must read every artifact in this directory plus the
  complete issue/PR sources. It must not assume PR #4 has merged.

Supporting discovery:

- `repository-inventory.md`
- `prediction-report.md`
- `scenario-report.md` and `scenario-results.tsv`
- `technology-decision-inputs.md`
- `source-register.md`

## Accepted Critical Findings

“Accepted” here means discovery found sufficient evidence to require the gate. It does not mean a
human has selected the architecture trade-off.

| ID | Finding | Required acceptance criteria | Required tests/evidence | Mitigation and rollback | Dependencies | Unresolved human decision |
|---|---|---|---|---|---|---|
| PH-C01 | PR #4 is the actual golden base but is open/unmerged with no CI | Every implementation issue declares immutable base SHA; accepted PR #4 disposition recorded; unrelated work preserved | Clean clone/checkout at accepted SHA; one golden command; compare branch graph and all preserved asset contracts | Tag/pin before fan-out; if base changes, stop, rebase, rerun golden/contract suite; rollback to immutable SHA | Maintainer PR #4 decision; issue #3 evidence | Merge unchanged, rebase, or retain explicit dependency? |
| PH-C02 | No executable clean-checkout golden baseline | Credential-free bounded command regenerates fixtures and machine-readable evidence from no prior `.venv`, data, volume or cache; exact SHA captured | Two independent runs; 18-table counts/checksums/anomalies; dbt contracts; snapshot/curated drift; syntax/Compose; no generated tracked files | Keep historical evidence; add new evidence schema alongside it; rollback deletes generated state and returns to input SHA | PH-C01; dependency locking | Maximum runtime and whether optional heavy profiles belong in the default golden command |
| PH-C03 | AWS state ownership and ClickHouse role are undefined | State matrix names authority, persistence, backup, restore/rebuild, RTO/RPO, scale-to-zero and owner for all stateful components | Stop-to-zero/start; empty-environment restore; corrupt-backup failure; ClickHouse data/query equivalence; Superset dashboard and OpenMetadata lineage/search checks | Prefer durable S3/Iceberg truth and replaceable tasks; retain previous backups/snapshots/catalog pointers; rollback target documented | Catalog choice; DB/search topology; cost ceiling | Durable ClickHouse or disposable serving projection? Managed or self-hosted metadata/search? |
| PH-C04 | “Scale to zero” can hide residual cost and unusable cold start | Region-specific active/off-hours bill of materials and readiness SLO; residual services itemized; budget alarms and teardown evidence | Cost-estimator golden cases; office open/close drill; EC2/task zero check; residual resource inventory; failure/retry spend test | Budget/quota/kill switch; staged rollout; retain local path; destroy only explicitly disposable test resources | PH-C03; region, hours, retention | Monthly ceiling, region, hours, cold-start target and retained-service budget |
| PH-C05 | Portal-triggered lab/Terraform/tool execution creates privileged RCE/authz boundary | Actor-resource-action matrix, per-lab workspace isolation, typed inputs, allow-listed commands, least privilege, localhost/cloud separation and audited destructive actions | Injection/traversal/fuzz; cross-user access; expired/downgraded roles; workspace escape; secret canary; apply endpoint denial; tamper tests | Default deny; no shell strings; separate plan/apply identity; destroy workspace on reset; rollback disables privileged runner while content remains | Learner identity model; web/API boundary; Terraform state | First release single-user localhost or hosted multi-user? Which actions require instructor/operator approval? |
| PH-C06 | Reset/publish/retry concurrency can silently corrupt or duplicate state | Versioned lab state machine, locks/idempotency, atomic/recoverable publish, evidence bound to committed run and deterministic reset from every state | Barrier-based race tests; failure at each write boundary; duplicate webhook/tool/retry; crash/reload/resume; post-reset golden oracle | Resume/rollback journal; snapshot/pointer rollback; idempotency ledger; quarantine partial evidence | PH-C02, PH-C03, lab runner design | Required concurrency level and whether single-user mode may defer multi-learner contention only (not same-user races) |
| PH-C07 | RAG/agents can leak ACL data/PII or cause unapproved side effects | AgentCore admission gate passes; ACL propagated end-to-end; provenance/citations/evals/guardrails/OTel/approval/idempotency/recovery/cost defined; core remains credential-free | Cross-role retrieval denial; prompt/tool injection; unsupported-claim/citation checks; PII/secret trace redaction; approval replay/expiry; crash/resume; eval thresholds | Agent wave off by default; read-only tools first; durable workflow state outside Runtime; revoke gateway/tool; delete indexes/traces per policy | Governed data products; identity; PH-C05/06; cloud budget | Which agent use case delivers enough learning value, and which AgentCore modules are admitted? |
| PH-C08 | Curriculum breadth lacks a smallest invariant learning journey | First vertical slice is one business outcome with prerequisites, FR/NFR, C4 views, decision/trade-off, starter, controlled failure, reset, verify, solution, evidence and reflection; accessibility included | Fresh novice E2E; advanced diagnostic route; keyboard/screen-reader/reduced-motion; failure/remediation; deterministic completion/evidence | Feature flags and content versioning; preserve static lesson when runner unavailable; rollback to last lesson contract/version | Human narrative/personas; PH-C02/05; web-stack spike | First narrative, foundation/mid-level persona boundaries and completion threshold |
| PH-C09 | Terraform state/plan compromise can expose secrets or alter wrong environment | Remote encrypted/versioned S3 backend with lockfile and least privilege; environment/SHA binding; plan/apply role separation; no apply in planning/default tests | Concurrent lock; wrong workspace/account/role denial; previous-version recovery; secret scan/redaction; approval-token replay | Restore state version; revoke role/session; keep bootstrap state separate; destroy only explicitly approved test environment | PH-C04/05; AWS account strategy | Account/environment layout and who may approve apply in later implementation issues |
| PH-C10 | Migration/refactor can preserve counts while changing semantics | Versioned data/API/evidence/lesson contracts and explicit migration mapping; dual-read/run period; rollback acceptance | Generator bytes/anomaly summary, mart schema/query snapshots, dbt lineage diff, OpenAPI compatibility, old/new evidence reader and rename/delete catalog tests | Additive-first migration; preserve old adapter/data snapshot; rollback to old contract and SHA without deleting user work | PH-C01/02; catalog reconciliation | Allowed intentional schema/metric changes and deprecation window |

## Accepted High Findings

| ID | Finding | Required acceptance criteria | Verification | Mitigation/rollback | Dependencies / decision |
|---|---|---|---|---|---|
| PH-H01 | Local profile budget is unmeasured end-to-end | Portal/browser plus any admitted lesson profile fits an approved 16 GiB headroom; invalid combinations fail before start | Cold/warm RSS, CPU, disk, network and readiness matrix; forced over-budget denial | Preserve core/no-container fallback; automatic teardown | Choose thresholds and supported machines |
| PH-H02 | `.venv` and component pins can drift | Rebuild keyed to lock/requirements hashes; current compatibility/security matrix recorded | Clean environment install twice; dependency diff; current OpenMetadata/Lakekeeper/Airflow/dbt/Rill/Superset spikes | Keep last known-good lock/images and migration notes | Package/container lock strategy |
| PH-H03 | Local Iceberg publish is non-atomic | Failure never produces silent success; learner sees committed/current snapshot or explicit recoverable absence | Inject failure between drop/create and catalog commit; verify rollback/read-back | Snapshot/staging swap where supported or guaranteed rebuild from source | Selected Iceberg writer/catalog capabilities |
| PH-H04 | OpenMetadata ingest accumulates stale renamed/deleted assets | Reconciliation or reset semantics documented and verified | Rename/delete model, reingest, API/search/lineage assertions | Per-lab catalog reset or reconciliation manifest; DB backup | Upgrade/topology decision |
| PH-H05 | Superset/OpenMetadata external UIs fragment learning | Portal provides consistent status/evidence/deep links and explains logical/physical state without cloning tools | Browser E2E for unavailable/starting/ready/error deep links; terminology test | Portal remains usable with tools down; preserve direct expert access | Information architecture and web stack |
| PH-H06 | Scroll-linked visual learning can exclude users | Semantic/static equivalents; keyboard, screen reader, zoom and reduced motion; scroll is not completion | axe, manual assistive-tech audit, reduced-motion visual test and logical focus order | Disable motion without content loss | Design system choice |
| PH-H07 | Office schedule ignores timezone, active work and readiness | Explicit timezone/next-run, drain/grace/checkpoint, override and ready/not-ready status | DST/holiday clock simulation, active-session shutdown and failed-start recovery | Operator override; keep core local; cancel close when backup fails | Hours/timezone and RTO decisions |
| PH-H08 | Local development credentials/ports could reach AWS/public network | AWS validation rejects placeholders, broad ingress and static secrets; local services bind only as intended | Terraform policy/static scan, network reachability, secret scan and placeholder-negative tests | Separate config schemas; revoke/rotate; block deployment | Network/IAM design |
| PH-H09 | Cross-engine dbt/metric semantics may fork | Shared contract states which outputs must be equivalent and which are platform-specific | DuckDB/ClickHouse query fixtures, type/timezone/null edge cases and metric comparison | Keep local golden adapter; version platform-specific deviations | ClickHouse/dbt adapter choice |
| PH-H10 | Scheduled or retried agents/workflows amplify cost/actions | Per-run time/concurrency/spend and idempotency limits are enforced and visible | Retry storm, delayed success, duplicate message, cost quota and kill-switch tests | Disable add-on; cancel work; reconcile uncertain effects | PH-C04/06/07 |
| PH-H11 | Historical evidence is host-specific and manually captured | New evidence includes environment/tool versions, commands, SHA and verifier schema and is CI-retainable | Validate JSON/schema, tamper detection, artifact retention and clean rerun | Preserve raw evidence; never overwrite prior run | PH-C02 and CI design |
| PH-H12 | Root `release-manifest.json` has unclear product ownership | Planner classifies, relocates/removes only with evidence, or explicitly excludes it from product contracts | Compare listed 1,558 paths to actual tracked repository and upstream provenance | Preserve file until owner/consumer is proven; no deletion in first wave | Maintainer decision if cleanup is in scope |
| PH-H13 | Airflow root mount is read-write | Learner jobs run in scoped generated workspace and cannot edit repository/control files | Write-attempt negative tests and post-run `git status`/hash check | Read-only mounts plus dedicated output volume/workspace | Lab runner/Airflow integration design |
| PH-H14 | Web stack could bias architecture before lesson contract | Three serious options are scored with the same representative lesson and no proprietary copying | Bundle/RSS/cold start, MDX validation, lab API, accessibility and E2E scorecard | Discard prototype branch; retain content schema and test fixtures | Human first lesson and hosting model |

## Required Acceptance-Criteria Envelope

The planner must ensure its final acceptance criteria collectively cover:

1. Immutable input SHA and clean-checkout golden baseline.
2. Preserve/refactor/rebuild decision matrix with migration and rollback evidence.
3. One runnable, accessible local learning vertical slice with deterministic reset/verify/evidence.
4. Local resource budgets and mutually exclusive profiles.
5. Local/AWS C4 and critical sequence views tied to stakeholder concerns.
6. OpenAPI and only-needed AsyncAPI contracts plus validators.
7. AWS state matrix, ClickHouse role, S3/Iceberg catalog, backup/restore and RTO/RPO.
8. ECS EC2 office-hours readiness/drain flow and honest residual cost model.
9. Terraform remote state, least privilege, plan/security checks and credential-gated tests; no
   default apply.
10. Superset and OpenMetadata metadata/search persistence and recovery.
11. Learner identity, privileged execution isolation, authorization and evidence integrity.
12. AgentCore admission gate and credential-free core.
13. Curriculum prerequisite/competency graph and standard lesson/lab contract.
14. Migration, rollback and preservation of unrelated user work.

## Required Verification Layers

| Layer | Minimum gate |
|---|---|
| Static | Markdown links/structure; Python/TypeScript syntax; JSON/YAML; C4/diagram render; OpenAPI/AsyncAPI lint; Terraform fmt/validate/security/policy; Compose render |
| Unit/contract | Lesson schema, lab state machine, command allow-list, evidence hash/schema, cost model, generator/data/dbt/metric contracts |
| Integration | Bounded generate-load-dbt-snapshot; Rill/Superset adapter; Iceberg catalog lifecycle; OpenMetadata ingest/reconcile; portal lab API |
| Failure/recovery | Reset/publish races, network partitions, corrupt backup, scale-to-zero restore, stale dependency/cache, migration rollback |
| Security | Object authz, traversal/injection, secrets/PII, network exposure, Terraform role/state, agent prompt/tool/approval/replay |
| Learner UX | Fresh novice, advanced diagnostic, prerequisites, controlled failure, reset, evidence, external-tool down/starting/ready states |
| Accessibility/browser | Unit/a11y, real browser E2E/visual review, keyboard, screen reader, 200% zoom, reduced motion |
| Cost/operations | Active/off-hours inventory, budget alarms, schedule/DST, readiness, drain, teardown and retained-state checks |

## Dependency and Ownership Boundaries

The planner should preserve single ownership at shared seams:

- one golden-baseline/data-contract owner;
- one lesson/lab/evidence contract owner;
- one portal shell/design-system owner;
- one privileged lab-runner/security owner;
- one local profile/resource owner;
- one AWS networking/IAM/Terraform-state owner;
- one AWS persistence/catalog/backup owner;
- one optional agent governance owner after admission.

Parallel implementation must not edit the same shared contract, migration sequence, generated
artifact or Terraform state backend. PR #4/base integration and contract ownership precede fan-out.

## Human Decision Queue Before Implementation Authorization

1. PR #4 disposition and immutable base.
2. First business narrative, personas and completion threshold.
3. Single-user local first versus hosted multi-user first.
4. Monthly AWS ceiling, region, office hours, RTO/RPO and cold-start readiness target.
5. ClickHouse durable versus disposable projection.
6. Glue versus another Iceberg catalog after compatibility/cost spike.
7. Managed versus self-hosted Superset/OpenMetadata metadata/search dependencies.
8. AWS orchestration scope.
9. Web-stack winner after a representative-lesson scorecard.
10. First agent use case and admitted AgentCore modules, if any.

## Planner Exit Constraint

The planner may translate these findings into phases and implementation issues only after making
every Critical/High item traceable to an owner, acceptance criterion, test and rollback. It must
leave unresolved human choices visible and must not “resolve” them by silently changing issue
scope. Independent validation/readiness gates occur in later fresh phases, not in this discovery
phase.
