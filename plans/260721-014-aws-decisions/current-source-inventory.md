# Current Source and Authority Inventory

## Purpose

Freeze what the planner and independent validator actually observed, with the observation phase
named on every time-sensitive row. This is not a pricing snapshot, compatibility proof, release
manifest, AWS inventory, or account record. Planner retrieval time for web/GitHub inspection:
`2026-07-22T00:32:50Z` (`2026-07-22T07:32:50+07:00`). Independent-validation retrieval time:
`2026-07-22T01:04:11Z` (`2026-07-22T08:04:11+07:00`).

## Repository and GitHub authority

| Source | Observed state | Authority use |
|---|---|---|
| Local branch | `plan/issue-14-aws-decisions` | Required planner branch |
| Clean input | `24be3b34c6b0fcdbd07c5800dcab349054e34713` | Exact immutable plan input |
| GitHub repository | `khanhvg/ai-ready-data-platform` | Issue/comment and publication source |
| Issue #14 at planner retrieval | OPEN; exact labels `triaged`, `risk:high`, `tdd`, `security:S3`, `decision-gate`, `recovery`, `aws`, `finops` | Historical planner input; not the post-publication workflow state |
| Issue #14 body/comment at planner retrieval | Audited Phase 9 scope; only the 2026-07-20 audited integration handoff comment existed | Historical source of the owned scope, tests, evidence, and no-cloud boundary |
| Issue #14 at independent-validation input | OPEN; exact labels `ready for plan validation`, `risk:high`, `tdd`, `security:S3`, `decision-gate`, `recovery`, `aws`, `finops`; planner authority comment `5040589180`; local/tracking/fresh-live SHA `51a45b54633e3c34ff39876ed9ddb8b9e675b3d1` | Exact validation workflow and byte input; no readiness or implementation authority |
| Issue #6 | CLOSED and `shipped`; merge verification names `24be3b34c6b0fcdbd07c5800dcab349054e34713` | Released read-only golden baseline |
| Issue #11 | OPEN at `ready for plan audit`; blocked audit output `ab653f6edec73e5ef875723945d2e3cd7814b4e6` with `IMPLEMENTATION_AUTHORITY=none` | Dependency state only; not a released concern-ID authority |
| Issue #11 planner/validation SHAs | `7620d168...` / `1287fe35...` | Historical current-branch provenance only; never consumed as release |
| Planner upstream before publish | `origin/integration/issue-5-local-learning` | Historical planner state; not assumed to be the Issue #14 publication target |

Issue URLs:

- `https://github.com/khanhvg/ai-ready-data-platform/issues/14`
- `https://github.com/khanhvg/ai-ready-data-platform/issues/11`
- `https://github.com/khanhvg/ai-ready-data-platform/issues/6`

## Byte-grounded repository sources

The following identities were recomputed from actual Git bytes. Git blob IDs and SHA-256 values
are complementary byte identities; neither upgrades a planning or dependency artifact into release
authority.

### Released Issue #6 authority

All rows are read from exact released commit
`24be3b34c6b0fcdbd07c5800dcab349054e34713`.

| Source path | Git blob | SHA-256 | Authority use |
|---|---|---|---|
| `README.md` | `a600847c8f2685b4d65b9c3be0c1aa80a226ae34` | `c9c0e9fb8a85b9f63b47f3e0a1717715d2e74af54a5f6db3edcfde070783c171` | Released local behavior inventory |
| `docs/system-architecture.md` | `1fa5e72974c60e007a78db17855138988fb1901e` | `dcb26c853e9f8f58d40a6f472cd1f72617b6a807ac907157e88397638322e8e1` | Released logical/physical architecture distinction |
| `plans/260721-005-enterprise-learning-sandbox/phase-09-aws-state-cost-and-persistence-decisions.md` | `62c5c9283c8f5b8369215a33cb62f1fcb20e8d0a` | `fc8ec4e849e63444294d4c60d3168767d6b473a10332f7316f0408839a47b4c4` | Historical Issue #14 planning provenance only |
| `plans/260721-005-enterprise-learning-sandbox/execution-authority-and-release-contract.md` | `b2ed27959dad6ee4c163e9e73911e88964fbb541` | `0050199985cac7b5f9cd78b9fb691afec20f7705b20dd29d33b8fb1f44787d95` | Released workflow/ownership boundary |
| `learning/contracts/command-owner-registry-v1.json` | `18d05a010da0d462c4e146954a18560c6b826af4` | `a94ac86bda0b70643edef9f144a59d8753d91f963b83d22cd510adbc31970e80` | Released future-name declarations only |
| `learning/contracts/fitness-result-v1.schema.json` | `0212ca96614aea02dbb60434d67a0cbb379a8213` | `a104ad6330bcfc22bda0fb661fef96f067c09153da7dc2f306103e5f93a4ab6d` | Released read-only evidence contract candidate |
| `Makefile` | `e1a4332a9645ccbd37bec4be1f70372241e16b7b` | `12926b16a797fded79b0b11b00147887258721f145c79e66472f44c5f0228458` | Released wildcard fragment seam; protected |
| `mk/issue-5/i5-01.mk` | `ba8646eda060f7b609b2e7a054a3f552e48e2ee5` | `d38dfb497161aa20761de7fcef7ae0fb09015adfdee885331ee1fba9403f9028` | Read-only fragment convention |

### Issue #11 discovery input, never release authority

These rows are read from blocked plan/audit head
`ab653f6edec73e5ef875723945d2e3cd7814b4e6` only to prove the dependency remains unresolved.

| Source path | Git blob | SHA-256 | Allowed use |
|---|---|---|---|
| `plans/260721-011-architecture-curriculum/plan.md` | `ddd0fa360b92b8aac6e65c4c826ba6023bb923f0` | `180a77fd58391b2c07e99be132d15bbfa2fd00e43482e3ea85cf37304bc80086` | Discover explicit empty implementation/dependency authority |
| `plans/260721-011-architecture-curriculum/dependency-and-release-gates.md` | `b2755ecb812d6f55df2bd0eb1b63b720e6b66708` | `bf39bab233717d10c7f99a7787fa3e7d3cba0a91b0984427adeb3fb7bdc7c088` | Discover unresolved dependency gates only |
| `plans/260721-011-architecture-curriculum/audit/readiness-audit-report.md` | `4ebc6b64a95287e7ce861647a54f1d76c81faa68` | `845ca39081551e0bc45b5c140c617e9424a1fddcf381668679d1602de13f4773` | Discover `IMPLEMENTATION_AUTHORITY=none` and blocked audit only |

The 14 current Issue #14 Markdown artifacts are bound to validation input
`51a45b54633e3c34ff39876ed9ddb8b9e675b3d1`. They are future-plan contracts, not current
implementation files. All future Issue #14-owned model/test/ADR/Make paths remain absent or
non-exact candidate families until the dependency-release amendment.

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
