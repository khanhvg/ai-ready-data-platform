# Technology Decision Inputs for Issue #5

## Decision Posture

This is pre-plan input, not an implementation plan. It narrows viable choices and identifies
proof required before the planner freezes architecture.

**Leading repository strategy:** preserve the issue #3 golden data spine; selectively refactor
execution, state and evidence contracts; build portal and AWS infrastructure as new bounded
surfaces. Rebuild only an individual surface when a measured spike proves replacement cheaper
and safer than adaptation.

## Preserve, Refactor, or Rebuild

| Criterion | Preserve and layer | Incremental refactor | Repository rebuild |
|---|---|---|---|
| Golden behavior risk | Lowest; retains exact generator/dbt/Rill/Iceberg/OpenMetadata evidence | Moderate; safe with characterization and dual-run tests | Highest; must recreate 18-table anomaly semantics, 51-model lineage, 11 marts/explores/assets and integrations |
| First portal slice | Adds a clean new boundary over current commands | Extracts lab/evidence contracts while adding portal | Starts portal cleanly but turns all data assets into migration work |
| AWS track | New Terraform/modules can coexist without disturbing local core | Shared contracts can be extracted after a spike | No benefit: AWS surface is greenfield regardless |
| Local 16 GiB path | Already staged and historically measured | Can improve safety/observability without stack churn | Must re-prove every resource and compatibility claim |
| Rollback | Remove new portal/AWS surface and return to exact SHA | Feature flags/adapters plus golden comparison | Requires full data/config migration rollback |
| Learning value | Learners see evolution from a working platform | Best opportunity to teach seams and fitness functions | Rewrite mechanics risk displacing architecture learning |
| Decision input | Viable now | Viable when a concrete seam reduces complexity | **Rejected by current evidence**; reconsider only if characterization shows the core cannot support lab isolation |

### Surface-Level Posture

| Surface | Preserve | Refactor candidate | Rebuild/new boundary |
|---|---|---|---|
| Generator and DQ scenarios | Output/schema/seed semantics | Split 947-line module only behind golden tests; extract profiles/contracts | No |
| DuckDB/dbt/marts | Local contracts and mart columns | Add contract/fitness assertions and bounded fixtures | No |
| Rill | Default local candidate and Parquet seam | Portal deep links/status adapter | Superset is new AWS BI surface |
| Airflow | TaskFlow graph and callables | Isolate per-lab workspaces, evidence and command runner | AWS orchestration topology remains a decision |
| MinIO/Lakekeeper/Iceberg | Local learning profile and concepts | Atomic/recoverable publish and reset contract | AWS S3/catalog adapter is new |
| OpenMetadata | Logical/physical ingestion intent and validation | Upgrade/reconciliation adapter | AWS deployment dependency topology is new |
| Portal, curriculum, progress | None exists | Not applicable | New modular-monolith portal + privileged lab-runner boundary |
| Terraform/AWS | None exists | Not applicable | New, isolated and non-applying by default |
| Agent labs | None exists | Not applicable | Optional late add-on after admission gate |

## Local Versus AWS Component Matrix

| Capability | Local default/candidate | AWS candidate/requirement | Shared contract | Decision input / gate |
|---|---|---|---|---|
| Learning portal | Static/content-heavy shell plus local API/lab runner | Stateless ECS service behind managed ingress | Lesson schema, progress/evidence API, deep links, accessibility | Web-stack spike; identity evolution from localhost single-user to hosted multi-user |
| Lab execution | Allow-listed local subprocesses in isolated workspaces | ECS tasks/jobs with least-privilege task roles | Start/status/cancel/reset/verify/evidence state machine | Never pass arbitrary commands; bound CPU/memory/time and side effects |
| Retail generation | Existing deterministic Python generator | Same versioned generator in a task/container | Seed/profile/schema/checksum manifest | Clean-checkout double-run; asset/version provenance |
| Analytical store | DuckDB file; single-writer discipline | ClickHouse as serving/warehouse path | Curated table/data-product contracts, query verification | Decide durable authority versus disposable projection |
| Transformation | dbt-duckdb | dbt adapter/target chosen for ClickHouse and/or Iceberg | Model intent, tests, docs, contracts | Cross-engine SQL compatibility spike; do not silently fork semantics |
| BI | Rill candidate over Parquet snapshots | Superset | Metric definitions, dashboard learning objectives, deep links | Keep tools distinct only when learning value justifies it; Superset metadata persists separately |
| Orchestration | Optional Airflow 3 TaskFlow | Unresolved: Airflow on ECS or narrower AWS-native runner | Observable stage DAG, retries, idempotency, evidence | Decide based on curriculum; avoid adding services solely for symmetry |
| Object storage | MinIO | S3 | Bucket/object naming, encryption, retention, checksum | S3 is data storage, not an Iceberg catalog |
| Iceberg catalog | Lakekeeper REST + Postgres | Leading candidate: AWS Glue Iceberg REST/Data Catalog | REST-shaped table lifecycle and schema evolution tests | Validate selected clients, SigV4/IAM/Lake Formation and rollback |
| Governance | OpenMetadata + MySQL + Elasticsearch profile | OpenMetadata ECS server plus durable DB/search dependencies | Asset identity, lineage, owner/tag/test ingestion, reconciliation | Upgrade from 1.6.5; choose managed versus self-hosted dependency cost/recovery |
| Metadata/search persistence | Docker volumes | RDS/Aurora + OpenSearch candidate, or explicitly owned self-hosted equivalents | Backup/restore/reindex verification | Managed choice retains residual cost when ECS/EC2 is zero |
| Secrets/identity | `.env`/localhost dev only; no cloud creds for core | IAM roles, Secrets Manager, hosted learner IdP | Actor/resource/action model; no secret in evidence | Reject placeholder credentials and shared admin identities |
| Observability | Structured evidence plus local OTel collector candidate | CloudWatch/OTel and cost alarms | Trace/run/correlation IDs, redaction, retention | Separate learner evidence from operator telemetry |
| Infrastructure | Compose profiles | Terraform with remote state | Environment manifest and exact SHA | `fmt`/`validate`/static/security/plan only until explicit apply authority |
| Agents | Optional local stubs/evaluations after core | Optional LangGraph/Restate + selected AgentCore modules | Provenance, ACL, eval, approval, idempotency, recovery | Must pass admission gate below |

## Architecture View Inputs

Per the [C4 source](https://c4model.com/diagrams), use the minimum views that answer a concern:

- **Landscape/capability:** business outcomes, actors, value stream and curriculum boundaries.
- **Context:** learner, instructor/operator, portal, external data/identity/AWS services.
- **Containers:** portal, lab runner, progress/evidence store, data platform adapters and optional
  agent runtime.
- **Components:** only for privileged execution, verification/evidence, retrieval/tool approval or
  another high-risk boundary.
- **Deployment:** separate local and AWS views with compute, network and durable state nodes.
- **Dynamic/sequence:** generate-transform-publish, failure-reset-verify, scale-down/restore,
  ingestion/lineage, retrieval/citation, approval/tool/retry/recovery.

Every view needs scope, audience, concern, legend, source version and a validator/render check.

## API and Domain Boundary Inputs

- OpenAPI covers synchronous portal/lab/progress/evidence operations. Include problem/error
  responses, authz, idempotency keys, examples and correlation IDs; validate the contract.
- AsyncAPI applies only if the design introduces real asynchronous channels. It must name
  operations/messages, correlation, retries/dead-letter behavior and security. It is not a reason
  to add Kafka.
- Initial domain candidates: Curriculum, Lab Execution, Progress/Assessment, Evidence,
  Architecture Assets, Data Platform Adapters and optional Agent Runs.
- Initial deployment should remain a modular monolith unless isolation, scaling, release cadence
  or security evidence justifies extracting the privileged lab runner or asynchronous workers.
- “Experience/Process/System/Backend/Technical” is a taxonomy for ownership and consumer intent,
  not a mandate to create five network services.

## AWS State, Persistence, and Scale-to-Zero

AWS documents that an EC2 capacity-provider ASG may have desired capacity zero and that scheduled
ECS service actions can change task counts. It also warns not to modify ECS-managed scaling
policies. Therefore the safe synthesis is to schedule service demand/readiness and let the
capacity provider manage replaceable compute, while durable state lives behind explicit services
or restore/rebuild workflows.

| State | Candidate authority | Can compute go to zero? | Required recovery proof | Residual cost concern |
|---|---|---|---|---|
| Raw/curated lake data and Iceberg metadata files | Versioned/encrypted S3 | Yes | Object/version recovery, checksum and Iceberg snapshot/time-travel query | S3 storage, requests, replication/lifecycle |
| Iceberg current-table pointers/catalog | Glue Data Catalog/Iceberg REST candidate | Yes | Create/commit/evolve/rename/delete and restore/re-register test | Glue/Lake Formation requests/catalog operations |
| ClickHouse tables/metadata | **Decision required:** disposable projection from Iceberg (preferred input) or durable volume/object-storage topology | Tasks/instances yes; data only if external/rebuildable | Empty-start rebuild or backup/restore with query/hash/RTO evidence | Backup/object/EBS/CloudWatch; possible standing node if durable singleton |
| Superset charts/dashboards/users | PostgreSQL-compatible metadata DB | Superset tasks yes | DB backup/restore, migration, dashboard/data-source verification and asset export | Managed DB or self-hosted volume/backup remains |
| Superset cache/async jobs | Redis/message broker only if features require | App tasks yes | Define disposable versus durable queue; prevent duplicate scheduled jobs | Cache/broker service |
| OpenMetadata entities/lineage/policies | MySQL/Postgres | Server tasks yes | DB backup/restore and API entity/count checks | Database remains |
| OpenMetadata search index | OpenSearch/Elasticsearch | Server tasks yes | Rebuild from metadata DB or snapshot restore, then search correctness | Search is often the largest idle-cost item |
| Portal progress/evidence | Durable relational/object store | Portal tasks yes | Actor/run/SHA-bound restore and tamper check | Database/object/log storage |
| Airflow metadata if retained in AWS | Durable database | Scheduler/web tasks yes with caveats | DAG/run state restore and duplicate-run prevention | Database and possibly scheduler availability |
| Terraform state | Separate encrypted/versioned S3 backend with lockfile | Yes | Recover previous state version; lock contention test | Minimal storage/requests/KMS |
| Agent workflow/approval/idempotency | Restate or durable database; not AgentCore session memory | Agent runtime yes | Resume, approval expiry, replay/dedupe and audit | Durable workflow store, AgentCore/CloudWatch/model usage |

### ClickHouse Decision Options

| Option | Advantage | Failure/cost concern | Admission evidence |
|---|---|---|---|
| A. Disposable serving projection rebuilt from Iceberg | Clean fit with replaceable ECS/EC2 and makes S3/Iceberg the durable truth | Cold start and rebuild cost; unavailable until hydration completes | Bounded `demo-large` rebuild time, reconciled row/hash/query outputs, interrupted rebuild resume and readiness SLO |
| B. Single-AZ persistent EBS-backed instance/task | Faster warm start and teaches local database persistence | ASG replacement/AZ/attachment/lifecycle complexity; singleton availability; backup still required | Automated stable attachment, fencing, graceful drain, snapshot/backup restore and replacement-instance drill |
| C. ClickHouse object-storage architecture or managed ClickHouse | Reduces instance-local data risk/operations | Product/version-specific semantics or standing managed cost; beyond current evidence | Official topology spike, failure model, cost and exit/restore tests |

Option A is the leading sandbox input because learners can inspect the durable Iceberg source and
the projection build, but it is not accepted until timing and data-equivalence tests pass.

### Office-Hours Workflow, Not Just a Cron

1. Before opening: raise desired service demand; capacity provider creates EC2; wait for ECS
   registration, durable dependencies, migrations, restores/rebuilds and health checks.
2. Publish **ready** only after portal, data queries, dashboards and catalog checks pass.
3. Before closing: block new labs, drain active work, checkpoint/backup, verify restore artifact,
   stop schedulers/workers and scale service desired counts to zero.
4. Confirm EC2 desired/running zero and inventory residual services/resources/cost tags.
5. Handle DST/holidays/overrides with explicit timezone, next-run display and operator runbook.

## Cost Inputs and STOP Thresholds

The planner must produce region-specific active-hours and compute-zero estimates for:

- ECS EC2/ASG, EBS and snapshots;
- load balancer, public IP, NAT gateway versus endpoints/egress design;
- RDS/Aurora, OpenSearch, Redis/broker if selected;
- S3/Glue/Lake Formation, backups and cross-region/version retention;
- CloudWatch logs/metrics/traces, KMS, Secrets Manager and Terraform state;
- data transfer, container registry and DNS/certificates;
- Bedrock models, AgentCore modules/tools/memory, evaluations and observability.

Required scenarios: zero learners/off-hours, one classroom during office hours, retry/failure
storm, retained backup/log growth and forgotten teardown. STOP until a human sets monthly budget,
region, usage window, retention and acceptable cold-start/RTO.

## Local Resource Budget Inputs

- Core path remains container-free and must run without Rill/AWS/agents.
- Portal + browser + one lesson profile must fit the 16 GiB target with explicit headroom for the
  OS and Docker Desktop; Compose `mem_limit` is not the measurement.
- Retain mutual exclusion for heavy profiles. The guarded lake+governance co-run is an exception
  with measured budget and automatic teardown.
- Add cold/warm RSS, CPU, disk, network and start-time evidence to each profile. Refuse over-budget
  combinations before starting them.
- Bounded fixtures are default for verification; `demo-large` is an explicit scale lab.

## Bedrock AgentCore Admission Gate

AgentCore is required only for an optional AWS add-on, not for the core. AWS documents that
Runtime session state is ephemeral and that modules can be adopted independently. An AgentCore
implementation wave is **not admitted** until all gates pass:

| Gate | Required proof |
|---|---|
| Core independence | First local learning journey passes with no AWS account, model key or network dependency beyond documented installs. |
| Governed products | Versioned data product, owner, classification, contract, quality and OpenMetadata lineage exist for every retrieval source. |
| ACL propagation | Cross-user/role retrieval and citation tests prove deny-by-default at index, retrieval and tool layers. |
| Provenance/citations | Answer evidence binds source/version/chunk/query/run and exposes unsupported claims. |
| Evaluation | Fixed dataset plus retrieval, groundedness, safety and task-success thresholds; regressions block release. |
| Guardrails/policy | Prompt/tool injection tests, allow-listed tools, deterministic policy outside model reasoning and Gateway/non-bypass design where used. |
| Observability/privacy | OTel-compatible traces, run/tool/model correlation, redaction, retention, deletion and cost attribution. |
| Human approval | Side-effect classes and approval expiry/identity/audit defined; read-only and write tools separated. |
| Idempotency/recovery | Durable workflow store, replay/dedupe, uncertain-outcome reconciliation and crash/resume tests; no reliance on ephemeral Runtime session state. |
| Cost/quotas | Per-run token/tool/duration limits, concurrency quotas, alarm and kill switch; region availability confirmed. |
| Portability | LangGraph/Restate responsibilities are explicit and core contracts do not depend on AgentCore-only payloads. |

## Web Stack Options

Use one representative lesson to prototype each serious option. No repository web conventions
exist, so familiarity cannot decide the stack.

| Option | Strengths for this proposal | Risks/constraints | Prototype measurements |
|---|---|---|---|
| Astro + React islands + separate lab API | Content/MDX first; static delivery; hydrate only interactive timeline/diagram/lab controls; natural progressive disclosure | Progress, auth and privileged lab state still need API/runtime; team must own two boundaries; ecosystem choices for complex app state | Static/no-JS content, hydrated bundle per lesson, lab API integration, MDX validation, accessibility and authoring workflow |
| Next.js App Router runtime | Integrated React routing/server/UI, mature data/auth/testing ecosystem, easier hosted multi-user portal | Higher runtime/framework coupling; static export excludes Server Actions and several dynamic features; local privileged runner still needs isolation | Server versus static mode decision, cold start/RSS, bundle, lab streaming/status, authz, MDX and deployment parity |
| React + Vite SPA + FastAPI (or equivalent) lab API | Explicit frontend/backend boundary; simple local dev and ECS containers; strong interactive UI control | More client JavaScript, weaker content/SSR defaults, separate routing/content/SEO decisions, API contract burden | First-load/bundle, offline shell, MDX/content pipeline, OpenAPI generation, accessibility, local process count |
| Documentation framework extended with widgets | Fast curriculum/navigation/search start | Lab/progress/evidence/state may fight the framework; risk of passive documentation dominating | Reject if controlled failure/reset/verify journey requires invasive overrides or cannot meet E2E/a11y goals |

### Web Selection Gate

Score: complete lesson contract, accessibility, MDX/content validation, lab-runner isolation,
OpenAPI contract, clean local startup, cold/warm RSS, JS payload, browser E2E, static/offline value,
deployment/rollback complexity and maintainer skill. Visual similarity to the referenced site is
not a criterion; learning interaction quality is.

## Interaction and Learning Pattern Inputs

Browser observation of `200ms.thenodebook.com` supports these adaptable patterns:

- a single concrete journey rather than a topic index;
- a persistent state/time/progress rail synchronized with the story;
- reversible exploration when moving backward;
- progressive layers: narrative, diagram/code, definition, quantitative evidence, deeper link;
- small consistent visual tokens linking state across acts;
- explicit derivation behind quantitative claims.

For this sandbox, transform those patterns into lab state and evidence: scroll cannot equal
completion; animations require static/reduced-motion equivalents; every claim needs project-owned
content and measurements; do not copy the source page's prose, assets, composition, styles or
implementation.

## Decision Register Inputs for the Planner

| Decision | Leading input | Human approval needed? |
|---|---|---|
| Repository strategy | Preserve + selective refactor + new portal/AWS surfaces | Yes, especially PR #4 disposition |
| Local BI | Preserve Rill unless measured Superset value wins | Yes if changing existing path |
| AWS Iceberg catalog | Glue Iceberg REST leading candidate | Yes after compatibility/cost spike |
| ClickHouse role | Disposable projection leading candidate | Yes; changes RTO and teaching model |
| OpenMetadata/Superset dependencies | Durable managed services leading reliability candidate | Yes; residual cost may be unacceptable |
| First web stack | No winner before prototype | Yes after scorecard |
| AgentCore | Deferred optional modules behind admission gate | Yes before any credentialed/cloud wave |

## Unresolved Questions

- What exact first lesson and actor model should the web-stack prototype implement?
- Is a hosted multi-user portal in the first release, or can the first slice be explicitly
  single-user/localhost while preserving API evolution?
- What are the approved budget, region, RTO/RPO, retention and cold-start thresholds?
- Which AWS orchestration surface serves the curriculum without duplicating Airflow for symmetry?
