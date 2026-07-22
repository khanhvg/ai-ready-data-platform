# Decision, State, BOM, and Cost Contracts

## Decision model

Each ADR and machine-readable option row must contain:

```yaml
decisionId: stable-kebab-id
scope: bounded component or concern
status: selected | rejected | deferred | blocked-tbc
forces: []
releasedConcernIds: []
nfrIds: []
options:
  - optionId: stable-kebab-id
    advantages: []
    disadvantages: []
    failureModes: []
    costDimensions: []
    stateRows: []
    securityControls: []
    compatibilityEvidence: []
    recoveryEvidence: []
    exitAndMigration: []
decisionOwnerEvidence: null
effectiveAt: null
supersedes: null
```

Rules:

- `selected` requires non-empty forces, released concern IDs, test evidence, state rows, cost
  dimensions, recovery/exit plan, and owner evidence. It does not authorize apply.
- `rejected` identifies the exact violated force/test; preference language is insufficient.
- `deferred` names the event/evidence that would reopen it and contributes no BOM/resource.
- `blocked-tbc` names every missing field and blocks dependent selections.
- One scope may have at most one selected authority. Duplicate authority is a hard failure.
- An ADR narrative cannot override the machine-readable row. Contradiction fails.

## Required option analysis

| Decision scope | Options that must be evaluated | Admission / rejection forces | Current outcome |
|---|---|---|---|
| ECS on EC2 topology | replaceable ECS tasks on new empty ASG capacity provider; alternate compute only if released concern demands comparison | ECS/EC2 learning need, segmentation, drain/readiness, capacity-to-zero behavior, cost, operational complexity | `blocked-tbc` |
| Network segmentation | private app/data subnets; controlled public egress; NAT; gateway/interface endpoints; ingress/load balancer candidates | exact ingress/egress flows, least privilege, availability, fixed/hourly and transfer charges, learner exposure prohibition | `blocked-tbc` |
| ClickHouse persistence | disposable S3/Iceberg-derived projection; fenced EBS authority; supported object-storage/managed alternative | hydration/equivalence/readiness, failure/recovery, writer fencing, cost, exit | `blocked-tbc` |
| Iceberg storage/catalog | S3 objects plus Glue Iceberg REST; alternate compatible REST catalog only with evidence | exact client/version operation matrix, IAM/Lake Formation needs, pointer/metadata recovery, portability, cost | `blocked-tbc` |
| OpenMetadata persistence | replaceable server + durable DB + rebuildable/restoreable search; self-hosted vs managed DB/search | exact version support, backup/restore, reindex, Multi-AZ requirement, fixed cost | `blocked-tbc` |
| Superset persistence | replaceable server + metadata DB; built-in DB cache vs dedicated cache/coordination only for selected features | dashboards/datasources/session/secret recovery, async feature needs, failure mode, cost | `blocked-tbc` |
| Search/index | rebuild from relational/catalog truth; snapshots; managed or self-hosted only if required | rebuild source/time, query readiness, storage, fixed cost, version support | `blocked-tbc` |
| Agent state/evidence | no AI; read-only optional AI; evidence-gated AgentCore modules | governed data/ACL/citations/evals/durability/cost, exact concern, no runtime-memory authority | `deferred` |
| Scheduling orchestration | smallest construct satisfying idempotent open/close/readiness/retry/reconciliation; managed workflow only if justified | observable state, failure injection, operations burden, fixed/request cost | `blocked-tbc` |

Globally rejected regardless of later topology: hidden public ingress, static credentials,
instance-local-only durable truth without accepted loss, multiple unfenced writers, a backup with no
restore oracle, hardcoded owner budget/region/account, stopped-equals-zero claims, destructive
teardown default, and AgentCore/module adoption for architecture pattern symmetry.

## State/key/config authority schema

Each row is a single authority. `logicalWriter` and `logicalReaders` name stable workload roles;
future AWS IAM principals remain empty until the account/environment design is approved.

```yaml
stateId: stable-id
stateClass: data | metadata | index | config | secret | key | control | evidence
system: logical component
authority: selected durable authority or TBC
logicalWriter: one role
logicalReaders: [one-or-more roles]
physicalWriterIdentity: null
physicalReaderIdentities: []
durability: TBC
availabilityScope: TBC
encryptionAtRest: TBC
encryptionInTransit: TBC
keyAuthorityStateId: TBC
configSchemaAndVersion: TBC
backupConsistencyGroup: TBC
backupMethod: TBC
restoreOrRebuildMethod: TBC
restoreOracleIds: []
rpo: TBC
rto: TBC
retention: TBC
deletionMode: preserve-by-default | separately-authorized-destroy
deletionOwner: TBC
migrationOwner: TBC
migrationOrder: []
zeroOrStoppedBehavior: TBC
residualCostLineIds: []
terraformBindingIds: []
releasedConcernIds: []
evidenceIds: []
status: blocked-tbc
```

Validation rejects missing fields, duplicate `stateId`, duplicate authorities for one semantic
state, one writer owning incompatible transitions without fencing, cyclic key/config/restore
dependencies, missing cost lines, impossible RPO/RTO units, `TBC` hidden in prose, or a selected
row with any required `TBC`.

## Minimum state authority matrix

This table names required logical writers/readers. Every other field remains `TBC` until the
future implementation and owners decide it; blank cells are forbidden in the implemented model.

| Required state row | Logical writer | Logical readers | Authority/durability/key | Backup/restore/RPO/RTO/retention | Deletion/migration owner | Current status |
|---|---|---|---|---|---|---|
| Terraform state object | exact Terraform plan/apply role | exact Terraform plan/apply/recovery roles | `TBC`; separate backend/KMS authority | version restore and recovery drill `TBC` | cloud state owner `TBC` | `blocked-tbc` |
| Terraform S3 lockfile | exact Terraform invocation role | concurrent Terraform invocations/recovery role | S3 lock object; encryption/IAM `TBC` | stale-lock adjudication; not a data backup | state/recovery owner `TBC` | `blocked-tbc` |
| Backend config and saved-plan approval envelope | plan-authority workflow | apply preflight/reviewer | immutable exact-input binding `TBC` | retained for audit/expiry; replay denied | security/apply owner `TBC` | `blocked-tbc` |
| Application config schema/version | configuration publisher | ECS tasks/jobs/readiness verifier | versioned source `TBC`; no secrets | previous known-good; config compatibility | app owner `TBC` | `blocked-tbc` |
| Application secrets and secret versions | secret-rotation authority | exact workload roles | secret/KMS authority `TBC` | rotation/escrow/revoke oracle | security owner `TBC` | `blocked-tbc` |
| KMS and application encryption/signing keys | key-administration authority | encrypt/decrypt/sign/verify roles | key policy/rotation `TBC` | key-loss prevention and prior ciphertext access | security owner `TBC` | `blocked-tbc` |
| S3/Iceberg data objects | admitted publication writer | ClickHouse hydrator/query/catalog/governance roles | durable object authority `TBC` | object/version/manifest restore `TBC` | data publisher `TBC` | `blocked-tbc` |
| Iceberg metadata/manifests/snapshots | admitted Iceberg commit writer | catalog/read engines/governance | metadata authority `TBC` | prior complete snapshot/pointer oracle | data/catalog owner `TBC` | `blocked-tbc` |
| Catalog namespaces/tables/pointers | catalog mutation role | ClickHouse/OpenMetadata/query/readiness roles | Glue/alternate `TBC`; key/auth `TBC` | export/reconcile/rebuild/restore `TBC` | catalog owner `TBC` | `blocked-tbc` |
| ClickHouse data/projection | hydration/ingestion role; direct writers otherwise denied | query/BI/readiness roles | disposable or durable `TBC` | rehydrate/backup/equivalence `TBC` | analytics owner `TBC` | `blocked-tbc` |
| ClickHouse hydration checkpoint/fence | hydrator coordinator | hydrator/readiness/recovery | durable control state `TBC` | idempotent resume/reconcile `TBC` | analytics/ops `TBC` | `blocked-tbc` |
| OpenMetadata relational metadata | OpenMetadata server/migration role | server/backup/restore verifier | durable DB `TBC`; KMS `TBC` | consistent DB backup/empty restore `TBC` | governance owner `TBC` | `blocked-tbc` |
| OpenMetadata search index/snapshot/rebuild journal | index publisher/reindex role | server/search/readiness | rebuildable/restoreable authority `TBC` | DB-to-index rebuild and/or snapshot `TBC` | governance/search owner `TBC` | `blocked-tbc` |
| Superset metadata/dashboards/datasources | Superset app/migration/import role | app/backup/restore/readiness | durable DB `TBC`; secret key dependency | DB backup + semantic asset verification `TBC` | BI owner `TBC` | `blocked-tbc` |
| Superset cache/coordination | Superset web/worker roles if admitted | Superset roles/readiness | none, DB-backed, or dedicated `TBC` | expiry/rebuild; durable classification explicit | BI owner `TBC` | `blocked-tbc` |
| Superset sessions/cookie signing state | Superset auth/session role | Superset request handlers | selected session authority + secret key `TBC` | expiry/rotation/logout behavior `TBC` | BI/security `TBC` | `blocked-tbc` |
| Scheduler/open-close workflow state | scheduler/workflow transition role | ops/readiness/CostGuard roles | durable idempotency/reconciliation `TBC` | replay/resume/manual override `TBC` | operations owner `TBC` | `blocked-tbc` |
| CostGuard inputs/decision/enforcement state | authorized caller + CostGuard transition role | plan/apply/readiness/audit roles | immutable budget/snapshot/topology binding `TBC` | replay/expiry/reconcile `TBC` | FinOps/ops `TBC` | `blocked-tbc` |
| Portal/progress state, if a released concern requires it | released portal application role | portal/evidence/readiness roles | external issue authority `TBC` | no selection in Issue #14 | external owner `TBC` | `blocked-tbc` |
| Agent workflow/approval/idempotency state, if admitted | deterministic policy/workflow role | agent/policy/audit/recovery roles | durable authority separate from runtime memory `TBC` | checkpoint/replay/recovery `TBC` | AI/security owner `TBC` | `deferred` |
| Agent memory/index/trace, if admitted | admitted memory/index/trace roles | policy/retrieval/eval/audit roles | classification/retention/key `TBC` | deletion/rebuild/export `TBC` | AI/data/security `TBC` | `deferred` |
| Decision/evidence bundle and price snapshot | decision/evidence finalizer only | offline verifier/human reviewer | checked-in source + immutable run bundle; signing not implied | content hash/index + retained prior bundle | release/evidence owner `TBC` | `blocked-tbc` |

## Backup consistency and restore ordering

The implemented matrix must define named consistency groups rather than independent “backup
success” booleans. Candidate groups to resolve after topology selection:

1. backend state + lock adjudication metadata + backend config/key version;
2. Iceberg objects + metadata/manifests + catalog pointer/namespace export;
3. OpenMetadata DB + search snapshot/rebuild watermark + exact server/schema version;
4. Superset metadata DB + exported dashboards/datasources + secret/config versions;
5. ClickHouse durable data or disposable hydration checkpoint + source release ID;
6. scheduler/CostGuard/approval/idempotency state + exact topology/price/input hashes;
7. agent workflow/memory/index/trace only if admitted, with independent retention classes.

Restore order is derived from dependencies and must detect cycles. The default shape is keys and
config -> durable truth/DB -> catalog -> search/index/projection -> application tasks -> semantic
oracles -> ready. Actual services and order remain `TBC`.

## BOM and Terraform reconciliation schema

No actual row is populated before the Issue #11 release. Future rows must follow:

```yaml
bomId: stable-logical-id
decisionId: selected-decision-id
stateIds: []
releasedConcernIds: []
terraformBindings:
  - bindingId: stable-id
    bindingType: resource | data-source | module-variable | module-output
    exactAddressOrSchemaField: exact future value
costLineIds: []
excludedCostDimensions: []
quantityDrivers: []
lifecycle: create | active | stopped | backup | restore | preserve | destroy
owner: TBC
```

Invariants:

- every selected BOM row has at least one selected decision and released concern;
- every state row maps to a BOM/Terraform binding or explicitly remains external and read-only;
- each Terraform resource/data source and cost-bearing variable/output maps back to BOM;
- every cost-bearing BOM lifecycle dimension is priced or explicitly excluded with owner,
  reason, source, expiry, and acceptance evidence;
- no duplicate binding, orphan row, wildcard address, guessed module path, or stale concern ID;
- data sources are costed when their queries/requests can incur cost, not assumed free;
- actual future paths/resources remain empty until the exact amendment.

Current values:

```yaml
bomRows: []
terraformBindings: []
releasedConcernIds: []
```

## Pricing snapshot schema

```yaml
snapshotId: content-addressed-id
schemaVersion: TBC
currency: USD
productRegion: caller-supplied
retrievedAt: exact RFC3339 UTC
freshnessTtl: owner-approved duration
rawSourceSha256: 64-hex
canonicalProjectionSha256: 64-hex
extractorVersion: exact
testedTreeSha: exact
prices:
  - priceId: stable-id
    sourceType: aws-price-list-bulk | aws-price-list-query | service-page
    sourceUrl: https-only allow-listed host
    apiOperation: exact or null
    serviceCode: exact
    productFamily: exact
    sku: exact or explicitly unavailable for service-page-only dimension
    offerTermCode: exact or explicitly unavailable
    rateCode: exact or explicitly unavailable
    dimensionCode: exact
    description: normalized
    productRegion: exact
    apiEndpointRegion: exact or not-applicable
    currency: USD
    sourceUnit: exact
    normalizedUnit: exact closed-registry unit
    rateDecimal: finite non-negative decimal string
    effectiveAt: exact RFC3339 UTC
```

Reject redirects to non-allow-listed hosts, query/userinfo/fragments not admitted by policy,
duplicate JSON/YAML keys, aliases/anchors if YAML is used, NaN/Infinity, exponent/precision
overflow, negative rates/quantities, unknown units, ambiguous GB/GiB, currency mismatch, region
mismatch, stale timestamps, unbounded collections/strings/nesting, traversal/absolute/private
paths, symlinks/hardlinks/special files, or raw source/hash disagreement.

## Cost input and line-item schema

Required caller inputs:

```yaml
monthlyBudgetUsd: finite positive decimal string
region: explicit AWS product region
schedule:
  timezone: IANA name
  activeWindows: explicit intervals
  holidays: explicit calendar/list version
  manualOverridePolicyId: exact accepted policy
contingencyRate: finite non-negative decimal string
scenario: baseline-730h | scheduled-demo
```

No default budget, region, schedule, holiday policy, or contingency is allowed. `TBC`, empty,
zero/negative budget, invalid timezone, overlapping/contradictory windows, and non-finite or
overflow inputs fail closed.

Each cost line contains:

```yaml
costLineId: stable-id
bomId: exact selected BOM row
priceId: exact snapshot row
scenarioId: exact
quantity: finite non-negative decimal
quantityUnit: closed-registry unit
usage: finite non-negative decimal
usageUnit: closed-registry unit
hoursClass: active | retained-730h | event-derived | not-hourly
formulaId: closed-registry formula
rawAmountUsd: recomputed, never trusted input
displayAmountUsd: recomputed presentation value
assumptions: []
exclusions: []
```

Mandatory dimensions when selected: compute instance hours; EBS GB-month/IOPS/throughput and
snapshots; EFS GB/storage class/read/write/tiering/backup; S3 GB-month/objects/GET/PUT/LIST/
lifecycle/replication/transfer; RDS instance/storage/IOPS/backup/transfer/public IPv4; OpenSearch
instance or OCU/storage/IOPS/transfer; NAT hours/GB; endpoint hours/GB; public IPv4/EIP hours; ELB
hours/LCU/NLCU/processed bytes; CloudWatch metrics/log ingestion/archive/query; AWS Backup
storage/copy/restore/evaluation; KMS key/rotation/request; catalog/request; cross-AZ/region/internet
transfer; DNS/cert/queue/workflow/request dimensions; AgentCore/model dimensions only if admitted.

Support plans, taxes/duties, commitments/reservations, Marketplace/software licensing, free-tier
credits, private discounts, and foreign exchange are exclusions unless the owner explicitly
adds current authoritative sources and model rules. Exclusion is disclosure, never zero pricing.

## Formula and rounding contract

Use base-10 arbitrary-precision Decimal. Never use binary float or `eval`.

```text
rawLineUsd = normalizedQuantity × normalizedUsage × rateUsdPerNormalizedUnit
subtotalRawUsd = exact sum(rawLineUsd)
contingencyRawUsd = subtotalRawUsd × contingencyRate
guardTotalRawUsd = subtotalRawUsd + contingencyRawUsd
budgetDecision = allow only when guardTotalRawUsd <= monthlyBudgetUsd
display amounts = ROUND_HALF_UP(raw amount, 2 decimal places)
```

The guard compares unrounded values so rounding cannot bypass budget. Displayed line sums may
differ from displayed total by rounding; evidence exposes raw canonical decimal strings and the
rounding rule. Unit conversions are explicit formula-registry entries with dimension checks.

## Scenario semantics

- `baseline-730h`: 730 hours for every selected always-on or retained hourly dimension; event and
  storage/request/transfer quantities come from explicit scenario inputs.
- `scheduled-demo`: compute-active hours are derived from the caller schedule; startup,
  hydration, drain, backup, retry, and manual-override hours/requests are added; retained/fixed
  dimensions still use their actual retained billing duration, commonly 730 hours.
- No scenario uses “scale to zero” as a cost line. It names exactly what stops and retains a
  residual inventory of everything still billable.
- Storage/request/log/backup/transfer growth uses explicit starting quantity, growth per period,
  compaction/deletion/retention behavior, and scenario duration.

## CostGuard contract

CostGuard is a deterministic admission decision, not an alarm-only claim.

```yaml
guardInputBinding:
  topologyHash: exact
  stateMatrixHash: exact
  pricingSnapshotHash: exact
  region: caller value
  scheduleHash: exact
  budgetUsd: caller value
  contingencyRate: caller value
  testedTreeSha: exact
decision:
  subtotalRawUsd: exact
  contingencyRawUsd: exact
  guardTotalRawUsd: exact
  status: allow | deny | blocked-tbc
  topDriverCostLineIds: stable descending amount, then ID
  alternativeDecisionIds: pre-authored and evidence-backed only
  reasonCodes: []
```

Missing/invalid/TBC/stale/unreconciled input returns `blocked-tbc`. Over budget returns `deny` and
must block dependent plan/apply/readiness transitions. Top drivers never contain free-form model
advice. Alternatives reference option IDs whose security/state/recovery trade-offs are visible.

Runtime alarms/budgets may complement CostGuard only if a later selected design defines an
enforcing actor, action, durable state, retry/reconciliation, break-glass owner, and evidence.
An alarm without enforcement cannot satisfy FR-013.

## Scheduled start/stop contract

Candidate state machine:

```text
STOPPED -> OPEN_REQUESTED -> DEPENDENCIES_STARTING -> RESTORING_OR_HYDRATING
        -> VERIFYING -> READY
READY -> DRAIN_REQUESTED -> DRAINING -> CHECKPOINTING -> BACKING_UP
      -> VERIFYING_BACKUP -> STOPPING -> RESIDUAL_INVENTORY_VERIFIED -> STOPPED
Any state -> DEGRADED/FAILED -> reconcile to prior safe state or STOPPED_NOT_READY
```

Open order derives from the state dependency graph: keys/config and authority checks; durable
stores/catalog/DB/search; projection hydration/migrations; app tasks; query/dashboard/catalog/
search/evidence oracles; ready. Close order blocks new work, drains active work, checkpoints,
creates and verifies consistent backups, stops replaceable services/compute, and inventories
retained resources. A failed backup cancels unsafe close unless a separately authorized
break-glass decision explicitly accepts bounded loss.

Every transition includes idempotency key, previous/current state, trigger, schedule/calendar
version, actor, attempt, deadline, dependency results, cost delta, rollback target, and evidence
hash. Duplicate/out-of-order/missed events reconcile rather than repeat destructive effects.

The selected schedule records IANA timezone, calendar/holiday version, next run, grace/drain
window, manual override reason/expiry/owner, missed-event policy, retry/DLQ policy, and audit.
No default timezone/hours is inferred from the planner host.

## Stoppable versus retained decision table

| Component class | Candidate stop behavior | Residual/fixed disclosure |
|---|---|---|
| ECS services/tasks/EC2 ASG | May scale to zero only after drain/checkpoint and selected capacity behavior | Startup/hydration and any retained capacity/warm pool still counted |
| ClickHouse task/instance | May stop if selected authority survives or projection is reproducibly disposable | EBS/EFS/S3/snapshots/checkpoints remain billable as selected |
| RDS | Temporary stop is option-dependent and cannot be called indefinite zero | Storage, IOPS, backups/snapshots and public IPv4 can remain; restart/readiness counted |
| OpenSearch managed/search alternative | No stop assumption; actual selected lifecycle required | Instance/OCU/storage and transfer remain until exact lifecycle changes |
| NAT gateway/endpoints/ALB/EIP | Not stopped merely because tasks stop | Hourly/data/public IPv4 dimensions persist while provisioned/associated |
| S3/EBS/EFS/backups/logs/KMS | Retained by design unless separately deleted | Storage, request, transfer, backup, log and key/request dimensions persist |
| Glue/catalog/control state | Retention and request behavior explicit | Requests/storage/control dimensions priced when applicable |
| AgentCore/AI | Deferred unless separately admitted | Runtime, memory, index, trace and model dimensions never hidden |

No destructive delete/recreate operation is smuggled into “stop.” Preserve/destroy are separate
teardown decisions and authority envelopes.
