# Current Source and Authority Inventory

## Purpose

Freeze what this planner actually observed. This is not a pricing snapshot, compatibility proof,
release manifest, AWS inventory, or account record. Retrieval time for web/GitHub inspection:
`2026-07-22T00:32:50Z` (`2026-07-22T07:32:50+07:00`).

## Repository and GitHub authority

| Source | Observed state | Authority use |
|---|---|---|
| Local branch | `plan/issue-14-aws-decisions` | Required planner branch |
| Clean input | `24be3b34c6b0fcdbd07c5800dcab349054e34713` | Exact immutable plan input |
| GitHub repository | `khanhvg/ai-ready-data-platform` | Issue/comment and publication source |
| Issue #14 | OPEN; exact labels `triaged`, `risk:high`, `tdd`, `security:S3`, `decision-gate`, `recovery`, `aws`, `finops` | Current issue scope and workflow authority |
| Issue #14 body/comment | Audited Phase 9 scope; only the 2026-07-20 audited integration handoff comment existed at retrieval | Source of truth for owned scope, tests, evidence, and no-cloud boundary |
| Issue #6 | CLOSED and `shipped`; merge verification names `24be3b34c6b0fcdbd07c5800dcab349054e34713` | Released read-only golden baseline |
| Issue #11 | OPEN at `ready for plan audit`; blocked audit output `ab653f6edec73e5ef875723945d2e3cd7814b4e6` with `IMPLEMENTATION_AUTHORITY=none` | Dependency state only; not a released concern-ID authority |
| Issue #11 planner/validation SHAs | `7620d168...` / `1287fe35...` | Historical current-branch provenance only; never consumed as release |
| Current upstream before publish | `origin/integration/issue-5-local-learning` | Not assumed to be the Issue #14 publication target |

Issue URLs:

- `https://github.com/khanhvg/ai-ready-data-platform/issues/14`
- `https://github.com/khanhvg/ai-ready-data-platform/issues/11`
- `https://github.com/khanhvg/ai-ready-data-platform/issues/6`

## Local source inventory

| Source | Observed fact | Use / restriction |
|---|---|---|
| `README.md` | Local-first DuckDB/dbt/Rill flow; optional MinIO/Lakekeeper/OpenMetadata; named volumes persist across ordinary down | Preserve local semantics; no AWS equivalence inferred |
| `docs/system-architecture.md` | Logical DuckDB/dbt view is distinct from physical Iceberg view; no fabricated lineage edge | Future AWS design must preserve the distinction |
| `plans/260721-005-enterprise-learning-sandbox/phase-09-*.md` | Historical state/cost decision plan and legacy concern references | Non-authoritative planning provenance |
| Issue #5 execution authority contract | I5-09 target names are future, S3, non-applying, and TBC-aware | Command declarations only; not runnable authority |
| `learning/contracts/command-owner-registry-v1.json` | I5-09 has `state-matrix-check`, `cost-model-check`, `aws-decision-check`; all `future-owner` / `not-runnable` | Preserve registry; later implementation owns only its Make fragment |
| `Makefile` | Additions-only wildcard include already released | Root file protected; no root edit required |
| `mk/issue-5/i5-01.mk` | Existing fragment pattern | Read-only convention source |
| `learning/contracts/fitness-result-v1.schema.json` | Released evidence envelope exists | Read-only consumed contract after exact compatibility mapping |
| Issue #6 architecture and golden assets | Six exact views and golden semantics exist | Protected read-only blast radius |
| `docs/code-standards.md` | Absent | Must remain absent in this issue |
| `docs/decisions/aws/**`, `infra/aws`, `scripts/aws`, `tests/aws`, `mk/issue-5/i5-09.mk` | Absent at input | No implementation exists by implication |
| `apps`, `learning/portal`, `learning/runner`, `learning/labs` | Absent at input | Protected absence; this issue cannot create them |

## Legacy concern provenance, not current authority

The Issue #5 master plan names the following Phase 9/10/11 references:

```text
PH-C03 PH-C04 PH-C09 PH-H07 PH-H08 PH-H09
SC-05 SC-12 SC-13 SC-17 SC-18
```

They explain why the epic opened Issue #14, but they are not substituted for exact released
Issue #11 concern IDs. The later amendment must record a crosswalk with source path, release SHA,
stable concern ID, title, acceptance, owner, and deployment/BOM relevance. Until then:

```yaml
releasedIssue11ConcernIds: []
deploymentConcernIds: []
```

## Official behavior-source candidates

These mutable official pages are source candidates for a later compatibility/source snapshot.
They establish topics to re-check; they do not select a service or current version.

| Topic | Official source URL | Planned use |
|---|---|---|
| Terraform S3 backend/lockfile | `https://developer.hashicorp.com/terraform/language/backend/s3` | Verify S3 backend, `use_lockfile`, version recovery, permissions, and sensitive config behavior |
| ECS EC2 capacity providers | `https://docs.aws.amazon.com/AmazonECS/latest/developerguide/asg-capacity-providers.html` | Capacity/readiness/drain forces; no zero-cost inference |
| ECS scheduled service scaling | `https://docs.aws.amazon.com/AmazonECS/latest/developerguide/service-autoscaling-schedulescaling.html` | Candidate compute scheduling mechanism |
| EventBridge schedule semantics | `https://docs.aws.amazon.com/scheduler/latest/UserGuide/schedule-types.html` | Timezone/DST/holiday test inputs |
| EventBridge retry/DLQ | `https://docs.aws.amazon.com/scheduler/latest/UserGuide/managing-schedule.html` | Delivery failure and replay handling |
| RDS temporary stop | `https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_StopInstance.html` | Residual storage/backup/public IPv4 cost and restart/readiness caveats |
| Glue Iceberg REST endpoint | `https://docs.aws.amazon.com/glue/latest/dg/connect-glu-iceberg-rest.html` | Candidate catalog capabilities; requires exact client/version proof later |
| Glue Iceberg REST APIs | `https://docs.aws.amazon.com/glue/latest/dg/iceberg-rest-apis.html` | Operation/auth/limitation matrix |
| Superset configuration | `https://superset.apache.org/docs/configuration/configuring-superset/` | Metadata DB, secret-key rotation, sessions, and supported DB evidence |
| Superset cache | `https://superset.apache.org/docs/configuration/cache/` | Decide if dedicated cache/coordination is actually required |
| OpenMetadata deployment | `https://docs.open-metadata.org/v1.13.x-SNAPSHOT/deployment/kubernetes/on-prem` | Candidate DB/search compatibility only; snapshot docs are not a version pin |
| OpenMetadata docs index | `https://docs.open-metadata.org/llms.txt` | Later exact-version documentation discovery |
| ClickHouse documentation | `https://clickhouse.com/docs` | Later exact persistence/backup/object-storage compatibility evidence |
| AgentCore overview | `https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/` | Optional/deferred module inventory only |
| AgentCore runtime state | `https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-how-it-works.html` | Prevent ephemeral runtime state from becoming durable authority |
| KMS destructive key deletion | `https://docs.aws.amazon.com/kms/latest/developerguide/deleting-keys.html` | Key-loss and deletion safety tests |
| S3 Block Public Access | `https://docs.aws.amazon.com/AmazonS3/latest/userguide/access-control-block-public-access.html` | Backend/data/evidence access control |
| S3 security practices | `https://docs.aws.amazon.com/AmazonS3/latest/userguide/security-best-practices.html` | TLS, least privilege, audit and access controls |
| AWS Backup restore testing | `https://docs.aws.amazon.com/aws-backup/latest/devguide/restore-testing.html` | Candidate restore-test behavior and cleanup risk; no automatic acceptance |
| AWS Backup restore behavior | `https://docs.aws.amazon.com/aws-backup/latest/devguide/restoring-a-backup.html` | Restore metadata, new-resource behavior, and RTO non-guarantee |

## Official pricing-source candidates

No rate was copied from these pages. Search-result examples and marketing examples are explicitly
excluded from the future checked-in snapshot.

| Candidate product/dimension | Official source URL/API entry | Snapshot status |
|---|---|---|
| AWS Price List Query/Bulk APIs | `https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/price-changes.html` | Empty; future optional refresh only |
| Bulk price list retrieval | `https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/using-the-aws-price-list-bulk-api.html` | Empty |
| EC2 compute/data transfer | `https://aws.amazon.com/ec2/pricing/` | Empty |
| EBS volume/IOPS/snapshot | `https://aws.amazon.com/ebs/pricing/` | Empty |
| EFS storage/throughput/backup | `https://aws.amazon.com/efs/pricing/` | Empty |
| S3 storage/request/transfer/lifecycle | `https://aws.amazon.com/s3/pricing/` | Empty |
| RDS compute/storage/IOPS/backup/transfer | `https://aws.amazon.com/rds/pricing/` | Empty |
| OpenSearch instance/OCU/storage/transfer | `https://aws.amazon.com/opensearch-service/pricing/` | Empty |
| VPC NAT/endpoints/public IPv4 | `https://aws.amazon.com/vpc/pricing/` | Empty |
| Elastic Load Balancing hours/LCUs/transfer | `https://aws.amazon.com/elasticloadbalancing/pricing/` | Empty |
| CloudWatch metrics/log ingestion/storage/query | `https://aws.amazon.com/cloudwatch/pricing/` | Empty |
| AWS Backup storage/copy/restore/evaluation | `https://aws.amazon.com/backup/pricing/` | Empty |
| KMS keys/rotation/requests | `https://aws.amazon.com/kms/pricing/` | Empty |
| AgentCore, only if admitted | `https://aws.amazon.com/bedrock/agentcore/pricing/` | Deferred; not in BOM |
| Support and taxes | AWS support plan and service-pricing terms at retrieval time | Explicitly excluded unless owner later includes them |

## Future pricing snapshot admission

A snapshot becomes admissible only when a separately authorized implementation records, per
price dimension:

```text
source URL or exact API operation
AWS service/product code, SKU, offer term, rate code and dimension
product region and API endpoint region as distinct fields
currency and normalized unit
effective timestamp and retrieval timestamp
raw source content SHA-256 and canonical projection SHA-256
source license/terms note and freshness TTL
extractor/tool version and exact tested-tree SHA
```

The snapshot must be checked in, human-reviewable, and consumed offline. Live refresh output is a
candidate requiring diff review; it cannot overwrite the accepted snapshot or make release pass.
Malformed, stale, foreign-region, wrong-currency, ambiguous-unit, duplicate, non-finite, or
unattributed prices fail closed.

## Current empty authorities

```yaml
implementationFileAllowlist: []
commandAllowlist: []
dependencyReleaseShas: []
releasedIssue11ConcernIds: []
currentPricingSnapshot: []
currentBomRows: []
currentTerraformBindings: []
currentRegion: []
currentAccountOrEnvironment: []
currentOwnerBudgetUsd: []
currentApplyApproval: []
```
