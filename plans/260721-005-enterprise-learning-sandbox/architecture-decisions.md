# Architecture Decisions and ADR Backlog

## Decision Policy

This register separates decisions needed before the first local cook from decisions that block
AWS apply or optional AI only. A leading hypothesis is not an approval. Every TBC remains visible
until its named owner records evidence and accepts an ADR.

Statuses:

- **Accepted default:** owner supplied or already proven; implementation may plan against it.
- **Decision gate:** implementation issue must produce evidence and an accepted ADR before
  dependent code merges.
- **Apply gate:** non-applying code may be built and checked; no cloud apply until accepted.
- **Admission gate:** entire optional wave stays off.

## Decision Summary

| ADR | Decision | Status | Needed before | Owner | Evidence / acceptance |
|---|---|---|---|---|---|
| ADR-001 | Preserve golden data spine; selectively refactor shared seams; add portal/AWS contexts | Accepted default | Phase 1 | Shared-core owner | Characterization suite preserves generator anomalies, marts, lineage, metrics, Airflow graph, curated list |
| ADR-002 | Portal starts as content-capable modular monolith plus isolated privileged runner | Accepted default | Phase 4 | Portal + runner owners | Two-process deployment, typed boundary, no arbitrary shell; extraction criteria documented |
| ADR-003 | Experience/Process/System/Backend/Technical are logical API ownership layers, not services | Accepted default | Contract design | Shared-core owner | OpenAPI tags/extensions map every operation; container diagram shows actual processes |
| ADR-004 | Local and AWS share lesson/data/evidence contracts, not identical engines/topology | Accepted default | Phase 3 | Shared-core architecture owner | `retail-golden-v1.json`, `local-aws-data-product-equivalence-v1.yaml`, `iceberg-lifecycle-v1.yaml`, `openmetadata-asset-identity-v1.yaml`, lesson and evidence schemas run against local adapters; AWS admission reuses the same versions and records deviations |
| ADR-005 | Web framework selected by representative-lesson scorecard | Decision gate | Phase 5 | Portal owner | Phase 2 scorecard; all must-pass criteria; winning ADR committed |
| ADR-006 | Local single-user localhost first; hosted multi-user later | Accepted default | Phase 4 | Product/security owner | Loopback-only, isolated workspace, same-user race tests; hosted identity model left as future ADR |
| ADR-007 | Progress/evidence are versioned state, separate from generated lab workspace | Accepted default | Phase 3 | Shared-core owner | State-machine tests, canonical hash, reset preservation rules, tamper test |
| ADR-008 | DuckDB and Rill remain local defaults | Accepted default | Local waves | Data-platform owner | Any replacement requires better lesson score, lower/equal RSS/start time, and preserved metric contract |
| ADR-009 | Local Iceberg remains MinIO/Lakekeeper; OpenMetadata remains | Accepted default | Phase 7 | Data-platform owner | Current contracts preserved; atomic publish and reconciliation failures become explicit labs/gates |
| ADR-010 | S3/Iceberg is AWS durable analytical truth; ClickHouse is initially a disposable projection hypothesis | Decision/apply gate | Phase 11 / any apply | AWS persistence owner | Empty-start rebuild, interrupted resume, query/row/hash equivalence, readiness within approved SLO |
| ADR-011 | AWS Iceberg catalog leading candidate is Glue Iceberg REST | Decision/apply gate | Phase 11 / any apply | AWS persistence owner | Current writer, ClickHouse, OpenMetadata compatibility; IAM/SigV4; create/evolve/time-travel/rename/delete/restore; priced residual |
| ADR-012 | Superset and OpenMetadata servers are replaceable; their metadata authorities persist separately | Apply gate | Any apply | AWS persistence owner | State matrix, backup/restore into empty environment, dashboard/catalog/search correctness, approved RTO/RPO/cost |
| ADR-013 | Office-hours default is weekdays 08:00-18:00 Asia/Ho_Chi_Minh in configurable ap-southeast-1 | Accepted planning default; apply gate | Phase 10 / any apply | AWS operations owner | Next-run display, readiness workflow, drain/checkpoint, override; cold-start target still TBC |
| ADR-014 | AWS monthly ceiling, retention, cold-start/readiness SLO, production RTO/RPO, account/environment and named apply approver | TBC apply gate | Any apply or cost/readiness claim | Product + FinOps + operations + security | Signed decision record, priced active/off-hours/failure-storm BOM, exact account/environment/plan SHA and approver identity |
| ADR-015 | Terraform state uses encrypted/versioned S3 lockfile with plan/apply role separation | Accepted design; apply gate | Backend bootstrap/apply | Terraform owner | Mock tests plus later real lock, wrong-account denial, previous-version restore; never store state/plan secrets in VCS |
| ADR-016 | AWS orchestration exists only when a curriculum/runtime requirement survives Phase 9 | Decision gate | Phase 10/11 | Architecture owner | Compare Airflow-on-ECS versus narrow readiness/hydration workflows; no symmetry-only service |
| ADR-017 | AsyncAPI is absent until a real asynchronous channel is introduced | Accepted default | Contract design | Shared-core owner | Contract inventory check fails orphan AsyncAPI or undocumented actual channel |
| ADR-018 | Evidence integrity uses canonical payload hash locally; hosted signing/key identity is later | Accepted default | Phase 3 | Evidence owner | Canonicalization, verifier hash, artifact hashes, tamper detection; no secret payload |
| ADR-019 | AI/AgentCore is optional and off until admission | Admission gate | Phase 12 | AI governance owner | Every gate in Phase 12 passes; core journey still succeeds network/cloud-credential free |
| ADR-020 | LangGraph and Restate are admitted by responsibility, not bundled by default | Decision/admission gate | AI implementation | AI governance owner | LangGraph only for explainable agent graph; Restate only for durable side-effect/recovery need |
| ADR-021 | Root release-manifest.json remains untouched legacy/tooling provenance | Accepted default | Cleanup work | Repository owner | Consumer/provenance investigation required before relocate/delete; excluded from product golden contract |

## ADR-001 Preserve / Refactor / Rebuild Matrix

| Surface | Preserve | Selective refactor | Rebuild/new | Rollback |
|---|---|---|---|---|
| Generator | Seed/profile/schema/anomaly/checksum semantics | Parameterize output/workspace; split only behind characterization | No | Golden double-run and restore exact module |
| DuckDB/dbt | Raw schema, 51-model graph, warning semantics, mart columns | Add workspace paths and contract/fitness tests | ClickHouse adapter is AWS-new | Dual-run local golden; switch adapter off |
| Rill | 11 models/metrics/explores and weighted metrics from reviewed tree | Portal status/deep-link adapter | Superset is AWS-new | Disable adapter; direct Rill remains |
| Airflow | TaskFlow DAG/callables/task order | Read-only base + scoped workspace and evidence hooks | AWS orchestration remains undecided | Disable runner integration; use existing host commands |
| Iceberg | Curated allow-list; local MinIO/Lakekeeper concepts | Atomic/recoverable publish, reset and evidence | S3/catalog AWS adapter | Restore snapshot/catalog pointer or deterministic rebuild |
| OpenMetadata | Logical/physical identity and lineage intent | Upgrade/reconcile/reset adapters | AWS deployment topology is new | Restore DB; reingest known manifest |
| Portal/learning | None | N/A | New bounded context | Feature flag/static lesson; delete new context without touching data spine |
| Terraform/AWS | None | N/A | New isolated non-applying context | Remove modules/state bootstrap plan; no resources existed |
| AI | None | N/A | Optional later context | Disable wave; revoke tools/indexes/traces per policy |
| User-owned standards | `docs/code-standards.md` hash if present; explicit absent record otherwise | None without separate owner decision | No | Preservation check fails and work stops; restore exact input bytes |

Whole-repository rebuild is rejected unless a later measured gate proves characterization,
workspace isolation, or contract evolution cannot be achieved incrementally. That gate must show
lower total migration risk and include a dual-run/revert rehearsal.

## ADR-002 Portal and Runner Boundary

Initial physical deployment:

1. **Learning portal modular monolith:** lesson rendering, information architecture, progress,
   evidence presentation, BFF endpoints, and local state repository.
2. **Privileged runner:** loopback/Unix-socket process with private service token, typed command
   descriptors, isolated workspaces, sanitized environment, resource/time limits, and audit.

Browser traffic never calls the runner directly. The portal BFF maps logical API operations to
allow-listed runner commands. Initial extraction criteria for more services:

- runner security isolation needs a different host/container boundary;
- independently measured CPU/memory scaling;
- separate release cadence or failure containment;
- hosted multi-user object authorization and queueing;
- an actual asynchronous channel requiring a worker.

Curriculum taxonomy does not satisfy any extraction criterion by itself.

## ADR-005 Web Stack Scorecard

Candidates: Astro + React islands, Next.js App Router, React/Vite + typed API. All render the same
project-owned representative lesson using a real golden evidence fixture.

Must-pass:

- complete reversible journey: question→progressive disclosure→controlled failure→diagnose→
  reset→verify→evidence→reflection, with committed progress correct after back/reload;
- explicit controlled/environmental failure distinction, typed remediation, idempotent reset, and
  no completion before a valid verifier/evidence record;
- semantic HTML, keyboard, screen-reader, 200% zoom, reduced-motion/static equivalent;
- no-scroll-only completion action and no fact/control hidden behind animation, hover, or JS-only
  disclosure;
- typed BFF/runner boundary and OpenAPI compatibility;
- content/schema validation and deterministic browser E2E;
- local startup without AWS/model credentials;
- a project-owned source inventory confirming no copied prose/assets/layout/style/code from the
  inspiration site.

Weighted score:

| Criterion | Weight |
|---|---:|
| Lesson authoring/schema/MDX safety | 20 |
| Accessibility and static/reduced-motion behavior | 20 |
| Lab status/evidence interaction and API boundary | 20 |
| Cold/warm start, RSS, JS payload | 15 |
| Unit/E2E/visual testability | 10 |
| Hosted evolution without rewriting contracts | 10 |
| Maintenance/dependency surface | 5 |

Time box: two implementation days total. A candidate failing a must-pass is eliminated. Highest
score wins. Tie within five points defaults to Astro + React islands because the product is
content-heavy and progressive hydration is the smaller initial runtime; the scorecard may
override that default with evidence.

Exact decision evidence is
`plans/260721-005-enterprise-learning-sandbox/reports/web-stack-scorecard.md` plus
`plans/260721-005-enterprise-learning-sandbox/reports/web-stack-scorecard.json`. The JSON records
candidate commands, lock/tool versions, normalized environment, must-gate booleans, measurements,
artifact hashes and reason. `make web-spike-scorecard-check` exits non-zero if a candidate lacks
evidence, scores eliminated candidates, uses different lesson assertions, omits the non-copy
inventory, or declares a winner without all must-gates. On failure ADR-005 remains `Proposed` and
I5-05 is blocked; no fallback framework is selected by preference alone.

## ADR-010 ClickHouse Admission

Disposable-projection admission requires:

- S3/Iceberg remains the durable authority and current catalog pointers are recoverable;
- `demo-large` rebuild into an empty ClickHouse meets the owner-approved cold-start/readiness SLO;
- row counts, schema, null/timezone/type edge cases, business queries, and metrics are equivalent
  to the versioned local contract;
- interrupted hydration resumes or restarts idempotently without reporting ready;
- queries and Superset remain unavailable until readiness is true;
- rebuild compute/request cost is included in the budget model.

If it fails, compare:

- fenced single-AZ EBS attachment + verified backup/restore;
- officially supported object-storage/managed ClickHouse topology;
- adjusted office-hours availability.

No alternative is accepted without state ownership, failure model, cost, exit path, and restore
evidence.

## ADR-011/012 AWS State Ownership Gate

Before apply, the decision record must name authority, persistence, backup, restore/rebuild,
RTO/RPO, scale-to-zero behavior, residual cost, and accountable owner for:

- S3 raw/curated objects and Iceberg metadata;
- Iceberg catalog pointers;
- ClickHouse projection or durable data;
- Superset metadata and any cache/job queue;
- OpenMetadata metadata DB and search index;
- portal identity/progress/evidence;
- orchestration state if retained;
- Terraform state;
- AI workflow/approval/idempotency state if admitted.

## Local Versus AWS Contract

The versioned source files are owned by I5-01/I5-03 and consumed read-only downstream:

- `contracts/data/retail-golden-v1.json` — protected generator/dbt/mart/metric/lineage truth;
- `contracts/data/local-aws-data-product-equivalence-v1.yaml` — engine-neutral query, type,
  null/timezone, row/schema and metric assertions plus versioned allowed deviations;
- `contracts/data/iceberg-lifecycle-v1.yaml` — create/read/evolve/time-travel/rename/delete,
  staged commit/current pointer, idempotent retry and restore/rebuild failure behavior;
- `contracts/data/openmetadata-asset-identity-v1.yaml` — 11 physical Iceberg assets, 45 logical
  dbt assets at the input baseline, owner/tag/lineage identity and rename/delete reconciliation;
- `learning/contracts/evidence.schema.json` and the lesson/lab schemas — common completion and
  evidence semantics.

Local MinIO/Lakekeeper and local OpenMetadata must prove these contracts first. AWS Glue/S3 and
AWS OpenMetadata reuse the same contract IDs; topology, auth, scale and persistence differences
are explicit adapter metadata, never silent contract forks.

| Concern | Local | AWS | Shared invariant |
|---|---|---|---|
| Identity | Single local actor | Hosted IdP/roles TBC | Actor/resource/action model; no object-ID trust |
| Analytics | DuckDB | ClickHouse | Curated data-product and query equivalence contracts |
| BI | Rill | Superset | Metric definitions, learning outcome, portal status/deep links |
| Object store/catalog | MinIO/Lakekeeper | S3/validated catalog | Iceberg lifecycle, asset identity, checksums |
| Governance | OpenMetadata local profile | OpenMetadata + durable dependencies | Entity/owner/tag/lineage/reconciliation contracts |
| Execution | Local allow-listed runner | ECS tasks/workflows | State machine, idempotency, evidence, cancellation |
| Progress/evidence | Local durable store | Hosted durable store TBC | Versioned schema, integrity, retention/deletion policy |

## Open Decisions by Boundary

### Required before the Phase 5 local vertical-slice cook

- ADR-005 web-stack winner.
- Concrete lesson completion threshold and remediation wording, within the fixed narrative.
- Final runner command allow-list, workspace limits, and local service-token transport.
- Evidence schema/version and state transition rules.

Phases 2-4 are the bounded decision-enabling implementation issues that resolve these gates.
They do not depend on AWS budget/RTO decisions. No Phase 5 portal-slice implementation begins
until their outputs are accepted.

### Required before AWS apply only

- Monthly ceiling and residual-service ceiling.
- Retention for S3 versions, backups, logs, traces, evidence, and Terraform plans.
- Cold-start/readiness SLO.
- Production RTO/RPO.
- Managed versus self-hosted metadata/search/database topology.
- ClickHouse role acceptance, catalog acceptance, account/environment layout, and apply approver.

Every future S3/Terraform backend or analytical bucket also requires public-access block,
`BucketOwnerEnforced`, an `aws:SecureTransport=false` deny, SSE-KMS, versioning, Terraform S3
backend `use_lockfile = true` (no new DynamoDB lock dependency), least-privilege prefix/action
policies, no static credentials, lifecycle and
retention/deletion rules, restore/version recovery, access logging/monitoring, and exact
account/region/plan-SHA binding. Security approves the S3/IAM controls; Product/FinOps/operations
set numeric gates; the named apply approver approves one exact non-stale plan. None is authorized
in this plan.

### Required before optional AI

- First AI learning use case and data classification.
- Admitted AgentCore modules and region availability.
- Retrieval/groundedness/safety thresholds.
- LangGraph/Restate responsibility boundary.
- Trace/index retention, deletion, and per-run spend.
