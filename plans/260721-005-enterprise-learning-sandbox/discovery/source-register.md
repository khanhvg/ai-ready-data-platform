# Source Register for Issue #5 Discovery

## Scope and Method

Access date for every entry: **2026-07-21**. Primary specifications and vendor/project
documentation were preferred. “Official definition” records what the source itself establishes;
“architectural synthesis” is this discovery phase's derived implication and must not be presented
as vendor guidance.

## Authoritative Sources

| ID | Authoritative URL | Official definition or constraint | Architectural synthesis used here |
|---|---|---|---|
| S01 | [C4 diagrams](https://c4model.com/diagrams) | C4's static core is context, container, component and code; landscape, dynamic and deployment are supporting views. Not every level is required. | Require views only when tied to a stakeholder concern or lab; do not create a decorative diagram inventory. |
| S02 | [C4 dynamic diagrams](https://c4model.com/diagrams/dynamic) | Dynamic views show ordered runtime collaboration for a story/use case and should be used sparingly. | Use them for ingestion, retry, reset, publish, approval and recovery journeys where ordering changes outcomes. |
| S03 | [C4 deployment diagrams](https://c4model.com/diagrams/deployment) | Deployment views map software/container instances to nested deployment and infrastructure nodes in one environment. | Separate local and AWS deployment views and show DNS, load balancing, networks, state stores and scaling boundaries. |
| S04 | [OpenAPI Specification 3.2.0](https://spec.openapis.org/oas/latest.html) | Current OpenAPI normative specification for describing HTTP APIs and their operations, inputs, outputs and security. | Treat learner/lab HTTP boundaries as executable contracts; validate examples, errors and auth, not just render docs. |
| S05 | [AsyncAPI Specification 3.0.0](https://www.asyncapi.com/docs/reference/specification/v3.0.0) | Defines application channels, operations, messages, correlation IDs, bindings, security and reusable components for event-driven APIs. | Add AsyncAPI only when an actual asynchronous contract exists; do not introduce a broker solely to demonstrate the specification. |
| S06 | [AWS Well-Architected pillars](https://docs.aws.amazon.com/wellarchitected/latest/framework/the-pillars-of-the-framework.html) | Six pillars: operational excellence, security, reliability, performance efficiency, cost optimization and sustainability. | Map architecture fitness functions and lab evidence to all six pillars, with business outcomes and trade-offs visible. |
| S07 | [AWS ECS EC2 capacity providers](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/asg-capacity-providers.html) | Capacity providers use Auto Scaling groups; a new empty ASG is recommended, managed scaling can use desired capacity zero, and ECS-managed scaling policies must not be modified. | Scale stateless ECS services to zero through service demand/capacity-provider behavior; keep durable state outside replaceable instances unless a tested attachment design exists. |
| S08 | [Scheduled ECS service scaling](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/service-autoscaling-schedulescaling.html) | Scheduled actions can proactively change ECS task counts and coexist with reactive scaling within scheduled min/max bounds. | Model office hours as explicit task schedules plus startup/readiness and shutdown/checkpoint workflows; a cron expression alone is not the strategy. |
| S09 | [ClickHouse backup and restore](https://clickhouse.com/docs/operations/backup/overview) | ClickHouse provides `BACKUP`/`RESTORE` with configured destinations, including object storage-capable backup paths. | An ECS task/EC2 stop is safe only after a verified backup/restore or if ClickHouse is formally disposable and rebuildable from Iceberg. |
| S10 | [ClickHouse Docker installation](https://clickhouse.com/docs/install/docker) | Official container deployment surface and persistent ClickHouse data/config paths. | Container restart is not persistence. ECS task definition, EC2 replacement, volume attachment, backup and restore must be designed separately. |
| S11 | [Superset production metadata configuration](https://superset.apache.org/admin-docs/configuration/configuring-superset/) | Superset stores charts, dashboards and other application definitions in a metadata database; SQLite is discouraged for production and a managed metadata service/backup strategy is recommended. | Keep Superset tasks stateless and preserve metadata independently. Scale-to-zero does not include deletion or loss of its database. |
| S12 | [Superset Docker Compose guidance](https://superset.apache.org/admin-docs/installation/docker-compose/) | Compose is for development, not production/HA; its PostgreSQL Docker volume is not backed up by default. | Do not lift the local Compose topology into AWS. Require database backup/restore and asset export verification. |
| S13 | [OpenMetadata Docker deployment](https://docs.open-metadata.org/latest/deployment/docker) | Current docs redirect to the v1.13.x deployment family and describe OpenMetadata's container setup with database and search dependencies. | The server may scale separately, but authoritative metadata and search/index recovery require explicit persistent dependencies and version compatibility. |
| S14 | [Apache Iceberg specification: catalog metastore](https://iceberg.apache.org/spec/#catalog-metastore) | A catalog tracks table identifiers and current metadata locations; table data/metadata files live in storage and atomic pointer updates are catalog responsibilities. | “S3-backed Iceberg” is incomplete without a catalog, permissions, commit semantics and disaster recovery. |
| S15 | [AWS Glue Iceberg REST APIs](https://docs.aws.amazon.com/glue/latest/dg/iceberg-rest-apis.html) | AWS Glue exposes Iceberg REST catalog APIs with SigV4 and IAM/Lake Formation authorization options. | Glue REST is the leading AWS catalog candidate because it survives ECS/EC2 scale-to-zero, but client/version and OpenMetadata/ClickHouse interoperability need a spike. |
| S16 | [Connect to Glue Iceberg REST](https://docs.aws.amazon.com/glue/latest/dg/connect-glu-iceberg-rest.html) | Iceberg clients can access tables in Amazon S3 or S3 Tables through the Glue endpoint; v1/v2 tables are supported with v2 default. | Prefer a standards-shaped catalog seam so local Lakekeeper and AWS Glue can share concepts without pretending their auth/operations are identical. |
| S17 | [Terraform S3 backend](https://developer.hashicorp.com/terraform/language/backend/s3) | S3 backend supports opt-in lockfiles; bucket versioning is strongly recommended; credentials and state require scoped access and encryption options. DynamoDB locking is deprecated. | Bootstrap state separately, enable versioning/encryption/lockfile, isolate environments/permissions and forbid local or VCS state. |
| S18 | [Terraform state](https://developer.hashicorp.com/terraform/language/state) | State can contain secrets; remote secure storage and locking are recommended over local/VCS storage. | Redact plan artifacts, run least-privilege CI plans, and test recovery from a previous version before implementation can apply anything. |
| S19 | [Amazon Bedrock AgentCore overview](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/) | AgentCore is modular: Runtime, Memory, Gateway, Identity, Browser, Code Interpreter, Observability/Evaluations and policy capabilities can be adopted independently and support multiple frameworks/models. | Admit only the modules with a learning objective and governance evidence; “AgentCore required” must not mean every service. |
| S20 | [AgentCore Runtime behavior](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-how-it-works.html) | Runtime sessions are isolated; session state is ephemeral and should not be used for long-term durability; IAM/OAuth and managed outbound credentials are supported. | Keep durable workflow/idempotency/approval state in a governed store (or Restate), not in runtime session memory. |
| S21 | [AgentCore pricing](https://aws.amazon.com/bedrock/agentcore/pricing/) | AgentCore and related Bedrock/CloudWatch features are consumption-priced; model, tool, storage and observability charges can be separate. | A credential-gated add-on needs per-lab budgets, quotas, timeouts and teardown evidence; scale-to-zero core compute does not cap model/tool spend. |
| S22 | [Next.js static exports](https://nextjs.org/docs/app/guides/static-exports) | Next.js can emit static assets, but server actions and several dynamic/server features are unavailable in static-export mode. | A Next.js choice must explicitly choose static portal + separate lab API or a maintained server runtime; do not assume both at once. |
| S23 | [Astro islands architecture](https://docs.astro.build/en/concepts/islands/) | Astro can render mostly static HTML and hydrate isolated interactive UI components. | Strong candidate for content-dominant lessons with bounded interactive diagrams, but lab state/API integration still needs a spike. |
| S24 | [200 milliseconds](https://200ms.thenodebook.com/) | Public interactive page observed in a clean browser: scroll-linked acts, persistent time/progress, reversible motion, inline definitions/evidence, staged diagrams/code and deeper links. | Adapt interaction principles only: stateful journey, evidence-on-demand and reversible exploration. Do not copy prose, assets, layout, styling, source or proprietary teaching content. |

## Official Facts Versus Synthesis

- Official sources establish specification semantics, supported service behaviors and documented
  constraints. They do **not** choose this repository's target architecture.
- The preferred synthesis is: durable truth in S3/Iceberg plus durable metadata services;
  replaceable ECS tasks for portal/BI/catalog servers; ClickHouse either demonstrably durable or
  explicitly disposable; scheduled readiness/backup workflows around office hours.
- Cost amounts are intentionally absent. Region, usage window, retention, traffic, NAT/VPC
  design, instance family and service tiers are unresolved; the planner must create a priced bill
  of materials from current AWS calculators before recommending an AWS topology.
- Project version pins in `versions.md` are historical compatibility evidence, not current
  authoritative recommendations.

## Source Gaps Requiring a Planner Spike

- Current ClickHouse release/ECS-specific volume and restore procedure for the chosen topology.
- Exact OpenMetadata v1.13.x AWS deployment matrix, database/search compatibility and upgrade
  path from the repository's 1.6.5 evidence.
- Glue Iceberg REST compatibility with the selected ClickHouse, OpenMetadata and writer clients.
- Region-specific AgentCore service availability, quotas and a measured per-lab cost.
- Comparative measured prototype for Astro+islands, Next.js runtime/static split and React/Vite
  plus a separate lab API.

## Unresolved Questions

- Which sources become version-pinned decision records, and which remain teaching references?
- Is AWS Glue/Lake Formation within the desired curriculum and residual-cost envelope, or should
  the AWS catalog remain a self-hosted REST catalog with greater operations burden?
