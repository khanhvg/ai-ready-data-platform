# Requirements, Concern, and Risk Traceability

## Traceability rule

Every future model/ADR/test/evidence row carries stable IDs from this file plus exact released
Issue #11 concern IDs after the dependency amendment. The Issue #5 `PH-*` and `SC-*` labels below
are provenance aliases only. They cannot satisfy the future `deploymentConcernIds` field.

## Functional requirements

| ID | Requirement | Owner role | Planned verification | Failure / rollback | Dependency |
|---|---|---|---|---|---|
| FR-001 | Publish one authority ledger that fails closed when file, command, dependency, pricing, BOM, region/account, budget, or apply authority is empty or contradictory | Architecture + Security | Authority/TBC schema negatives | `blocked-tbc`; no implementation/apply | Released Issue #11 + exact amendment |
| FR-002 | Model every minimum state/key/config component with named logical writer/reader, authority, durability, encryption/key authority, backup/restore, RPO/RTO, retention, deletion, migration, and teardown ownership | Data + App + Ops | Missing/duplicate/contradictory row fixtures | Reject matrix; preserve current state | FR-001 |
| FR-003 | Record option outcomes as `selected`, `rejected`, `deferred`, or `blocked-tbc`, with forces, trade-offs, admission evidence, exit cost, and rejected alternatives | Architecture | Option completeness and no-pattern-theater tests | Reopen ADR; selected BOM invalid | Exact concern/NFR mapping |
| FR-004 | Compare ECS on EC2 topology and network segmentation without silently selecting public ingress, NAT, endpoints, ALB/NLB, EIP, EFS, RDS, OpenSearch, or extra orchestration | Architecture + Security + FinOps | Option/concern/BOM reconciliation | Defer/reject unrequired service | Released deployment concerns |
| FR-005 | Decide ClickHouse durable vs disposable projection only from hydration, equivalence, RPO/RTO, readiness, failure, and cost evidence | Data + Ops | Empty-start, interrupt, equivalence, corrupt-state cases | Keep durable truth/local path; no ready claim | Data contract + released concerns |
| FR-006 | Decide S3/Iceberg and catalog authority, lifecycle, pointer/commit, restore, auth, compatibility, and deletion ownership | Data + Security | Catalog capability/failure/recovery matrix | Retain previous catalog/pointer; reject candidate | Exact client/version evidence |
| FR-007 | Decide OpenMetadata DB/search and Superset metadata/cache/session authority; server tasks remain replaceable only if durable dependencies and restores prove it | App + Data + Ops | DB restore, search rebuild/snapshot, dashboard/datasource/session checks | Prior known-good; no ready claim | Exact versions/features |
| FR-008 | Keep AgentCore/AI optional and evidence-gated; separate runtime/session/memory/index/workflow/evidence authorities | AI + Security + FinOps | Disabled-core and state-ownership tests | `deferred` or disable/revoke/delete by policy | AI admission + exact concerns |
| FR-009 | Build a BOM contract where every future cost/state row maps to exact Terraform resource/data source/module variable/output and released concern ID; every mapping is priced or explicitly excluded | Architecture + FinOps + I5-10 | Bidirectional orphan/duplicate/stale mapping tests | Reject topology/BOM | Issue #11 release; later I5-10 schema |
| FR-010 | Store a current-source pricing snapshot with full provenance and no fabricated rates | FinOps | Provenance, freshness, URL, region, SKU, unit, currency, content-hash tests | `blocked-tbc`; refresh candidate only | Exact region + source approval |
| FR-011 | Calculate transparent 730-hour baseline and schedule-derived demo scenarios with quantities, rates, hours, storage, requests, transfer, backups, logs, and explicit support/tax exclusions | FinOps | Deterministic golden cases | No estimate/approval claim | FR-009/010 |
| FR-012 | Include persistent/fixed charges during stopped compute, including each selected EBS/EFS/S3/RDS/OpenSearch/NAT/EIP/ALB/log/backup/transfer/KMS dimension | FinOps + Ops | Stopped-but-not-zero and residual inventory cases | Fail false-zero claim | Selected BOM only |
| FR-013 | Enforce caller-supplied finite positive `monthlyBudgetUsd`, region, schedule, and contingency; compare total plus contingency, deny over budget, report stable top drivers and authored alternatives | FinOps | Missing/invalid/TBC/over-budget/rounding/overflow cases | Deny; no fallback budget | Owner inputs |
| FR-014 | Define scheduled open/readiness/drain/backup/stop workflows, timezone/holidays, dependency order, readiness, manual override, retries, rollback, and residual billing | Ops + App + Data | Clock, holiday, active work, partial-start, failed-backup, replay tests | Cancel close/open; return to prior safe state | Selected topology + RPO/RTO |
| FR-015 | Define consistent backups and restore oracles for key loss, corruption, AZ/region failure, catalog/metadata/search rebuild, and prior-version rollback | Ops + Security + Data | Empty-environment restore and fault matrix | Previous known-good/local fallback | Owner RPO/RTO/retention |
| FR-016 | Separate teardown `preserve` and `destroy` modes; default to preserve; require exact authorization for destructive scope | Ops + Security | Wrong-mode, active-dependency, foreign-resource and retained-evidence tests | Refuse destructive action | Named authority |
| FR-017 | Emit compact hash-indexed evidence at `.artifacts/evidence/aws-decisions/<run-id>/` with price provenance, decision/trace results, rollback, and no sensitive/account-specific content | Security + Release | Schema/hash/redaction/tamper/replay tests | Quarantine bundle; fail gate | Released evidence compatibility |
| FR-018 | Expose only the three future targets named by the command registry through `mk/issue-5/i5-09.mk`; root Make remains untouched | Issue #14 implementer | Registry ownership, help, path and recipe tests | Remove fragment/revert issue-owned files | Exact command amendment |
| FR-019 | Run deterministic core tests without network/AWS; optional live source refresh cannot satisfy release alone | Test + FinOps | Network-denied suite and offline replay | Reject live-only evidence | Checked-in snapshot |
| FR-020 | Require human exact-head review before merge and separate explicit named authorization before any AWS/Terraform apply | Human reviewer + apply approver | GitHub exact-SHA read-back and authority envelope check | No merge/apply | All prior gates |

## Non-functional requirements

| ID | Requirement | Planned proof | STOP condition |
|---|---|---|---|
| NFR-001 | Deterministic: Decimal/rational arithmetic, stable sorting, explicit timezone, no ambient clock/network/account | Repeated offline golden outputs hash-equal | Byte or semantic drift |
| NFR-002 | Fail closed: missing/TBC/invalid/contradictory authority cannot become zero, default, selection, pass, or readiness | Mutation suite for each required field | Any permissive fallback |
| NFR-003 | Transparent: each total is reconstructable from quantity × unit-normalized rate × usage, plus explicit contingency and rounding | Line-item formula replay | Unexplained subtotal or hidden fee |
| NFR-004 | Secure S3: strict untrusted parsing, bounded regular-file reads, path containment, no shell evaluation, secret/account/private/PII redaction | Threat matrix and negative fixtures | Critical/High residual defect |
| NFR-005 | Current-source: effective/retrieved dates, source hashes, region/unit/currency and freshness are explicit | Snapshot freshness/provenance test | Stale/unattributed rate |
| NFR-006 | Recoverable: readiness depends on tested restore/rebuild and key/config availability, not backup-job success | Empty restore and corruption oracles | Restore cannot meet accepted objectives |
| NFR-007 | Least authority: exact writers/readers, IAM/KMS/backend ownership, deletion and break-glass roles | State/role conflict tests | Shared/unowned destructive authority |
| NFR-008 | No false zero: residual/fixed resources remain visible for the full billing period they are retained | Stopped scenario invariant | Total becomes zero with retained selected service |
| NFR-009 | Bounded growth: storage/request/log/backup/transfer and failure/retry sensitivity is explicit | Growth and overflow golden cases | Unbounded/implicit dimension |
| NFR-010 | Plan/repository isolation: exact allow-list only, protected hash/absence preservation, no broad force-add | Changed-path and protected baseline check | Any outside-plan planner change or later outside-lease change |
| NFR-011 | Auditable but private: compact content-addressed evidence, repository-relative locators, no account-specific data | Redaction/path/hash index tests | Sensitive or private locator in evidence |
| NFR-012 | Honest claims: offline/mocked/static/live/owner-approved states remain distinct | Evidence status vocabulary tests | Mock/live or planner/readiness conflation |
| NFR-013 | Maintainable: one canonical unit registry, formula engine, state row schema, option schema, and evidence index | Duplicate-contract/stale-field checks | Divergent embedded schemas |
| NFR-014 | Additive/rollback-safe: old readers/contracts remain until compatible migration and rollback proof | N-1/current reader and rollback tests | In-place destructive migration |

## Concern crosswalk status

| Provenance alias | Historical force from Issue #5 | Issue #14 FR/NFR | Released Issue #11 ID |
|---|---|---|---|
| PH-C03 | State/persistence authority and ClickHouse role | FR-002, FR-005..008, FR-015; NFR-006/007 | `TBC: []` |
| PH-C04 | FinOps, residual cost, readiness, CostGuard | FR-010..014; NFR-003/005/008/009 | `TBC: []` |
| PH-C09 | Terraform backend/lock/wrong-environment protection | FR-002, FR-009, FR-016; NFR-004/007 | `TBC: []` |
| PH-H07 | Timezone, readiness, drain and override | FR-014; NFR-001/006 | `TBC: []` |
| PH-H08 | Static secret, IAM, ingress and network safety | FR-004, FR-017; NFR-004/007 | `TBC: []` |
| PH-H09 | DuckDB/ClickHouse semantic divergence | FR-005; NFR-006/012 | `TBC: []` |
| SC-05 | Compute stop loses state / incomplete restore | FR-002, FR-005, FR-015 | `TBC: []` |
| SC-12 | Budget/retry/retention overrun | FR-011..013; NFR-008/009 | `TBC: []` |
| SC-13 | Lock/replay/wrong apply authority | FR-001/002/009/020; NFR-004/007 | `TBC: []` |
| SC-17 | Schedule/timezone/active-work failure | FR-014; NFR-001/006 | `TBC: []` |
| SC-18 | Corrupt backup accepted | FR-015/017; NFR-006/011 | `TBC: []` |

The amendment must not merely copy aliases. It must prove exact semantic correspondence or mark a
new requirement unmatched and `blocked-tbc`.

## State row coverage map

| State class | Minimum rows | Primary requirements | Required failure cases |
|---|---|---|---|
| Terraform control | backend state object, S3 lockfile, backend config, saved-plan/approval envelope | FR-001/002/009/020 | concurrent lock, wrong state, version loss, replay, secret in state/plan |
| App config/key | config schema/version, secret versions, KMS/application signing/encryption keys | FR-002/015/016 | missing version, key disabled/deleted, rotation rollback, secret leak |
| Data lake | S3 objects, Iceberg metadata/manifests/snapshots/current catalog pointers | FR-002/006/015 | mixed generation, orphan object, corrupt metadata, unauthorized delete |
| Analytics | ClickHouse local data/projection/checkpoints | FR-002/005/014/015 | empty start, partial hydration, duplicate load, semantic drift |
| Governance | OpenMetadata relational DB, search index/snapshot/rebuild journal | FR-002/007/015 | DB restored/search stale, reindex failure, corrupt snapshot |
| BI | Superset metadata, dashboards/datasources, cache, session/secret state | FR-002/007/015 | DB restore without assets, cache/session loss misclassified as durable loss |
| Platform search | Any separately selected search/index store | FR-002/003/015 | no rebuild source, fixed cost hidden, stale index ready |
| AI | workflow/checkpoints, approvals/idempotency, memory/index, trace | FR-002/008/013/015 | runtime ephemeral state used as authority, replay, retained PII |
| Operations | schedule/override/drain/readiness/CostGuard/reconciliation | FR-002/013/014 | duplicate event, partial stop/start, alarm without enforcement |
| Evidence | immutable run bundle, price snapshot/provenance, hash index, rollback result | FR-017/019/020 | tamper, replay, recursive SHA, private path, account ID |

## Cost scenario coverage

| Scenario ID | Required dimensions | Expected invariant |
|---|---|---|
| COST-730 | 730 active-hour baseline for selected always-on and compute resources | Reconstructable total; no free-tier/discount assumption unless snapshot explicitly models it |
| COST-DEMO | Caller schedule-derived active compute hours plus 730-hour retained dimensions | Lower compute may not erase fixed/residual items |
| COST-STOPPED | Tasks/instances at zero with selected retained state/network/control plane | Total remains non-zero whenever billable resources remain |
| COST-GROWTH | Storage, object/request, log, backup, snapshot and transfer growth | Growth is monotonic for positive rate/quantity |
| COST-NETWORK | NAT vs endpoints vs controlled public-egress candidates | Compare only admitted, security-equivalent alternatives; no hidden IPv4/transfer |
| COST-FAILURE | Retry storm, failed open/close, orphan restore test, forgotten teardown | All retries/hours/storage/cleanup lag are counted |
| COST-CONTINGENCY | Required caller contingency and presentation rounding | Guard compares unrounded subtotal + contingency |
| COST-OVER | Budget one smallest supported unit below guard total | Denied with stable top drivers and authored alternatives |

## Recovery scenario coverage

| Scenario ID | Injection | Required result |
|---|---|---|
| DR-KEY-LOSS | Disable/schedule deletion/wrong key reference | Not ready; prevent teardown; restore key reference or roll to decryptable generation |
| DR-BACKUP-CORRUPT | Truncate/mutate backup or hash/index | Restore oracle fails; prior known-good retained |
| DR-AZ | Lose selected AZ-local compute/storage path | Outcome follows accepted topology; no unsupported multi-AZ claim |
| DR-REGION | Region unavailable | Explicit selected/deferred strategy; no implicit cross-region recovery |
| DR-CATALOG | Catalog pointer/metadata missing or inconsistent | Reconcile from durable truth or roll pointer; no mixed ready state |
| DR-METADATA | OpenMetadata/Superset DB lost | Restore DB and verify semantic assets before ready |
| DR-SEARCH | Search index missing/stale | Rebuild or restore per selected authority; compare index freshness/content |
| DR-CLICKHOUSE | Compute/local projection empty or corrupt | Hydrate/rebuild from accepted truth, then equivalence and readiness |
| DR-SCHEDULE | Duplicate/missed/out-of-order open/close event | Idempotent state transition and reconciliation |
| DR-TEARDOWN | Preserve/destroy confusion or foreign resource | Fail before mutation; preserve evidence/state/keys by default |

## Apply-blocking TBC register

Every row is required and currently unresolved:

| TBC ID | Required value / evidence | Owner role | Blocks |
|---|---|---|---|
| TBC-001 | Exact released Issue #11 concern IDs and release SHA | Architecture owner | Any implementation allow-list |
| TBC-002 | Exact implementation file and command allow-lists at amended SHA | Issue owner + validator/auditor | Cook |
| TBC-003 | Exact BOM/topology and service/version compatibility | Architecture/data/app owners | Cost approval and apply |
| TBC-004 | Caller region and product-region mappings | Cloud/apply owner | Snapshot/model/apply |
| TBC-005 | Caller schedule/timezone/holiday/manual override policy | Operations owner | Demo scenario/apply |
| TBC-006 | Finite positive monthly budget and finite non-negative contingency | FinOps owner | CostGuard/apply |
| TBC-007 | Retention/deletion policy by data/evidence/config/key class | Data/security owners | State acceptance/apply |
| TBC-008 | RPO/RTO and readiness/cold-start objectives by component | Operations/data/app owners | Option selection/apply |
| TBC-009 | Current checked-in pricing snapshot and freshness policy | FinOps owner | Numeric cost claim/apply |
| TBC-010 | Account/environment layout and identity model | Security/cloud owner | Any real plan/apply |
| TBC-011 | Exact named human reviewer and later named cloud/apply approver evidence | Human owners | Merge/apply respectively |
| TBC-012 | Real current compatibility/restore evidence where selected options require it | Architecture/data/ops | Production/readiness/apply |

No TBC blocks this planner artifact. All apply-blocking TBCs block AWS readiness and apply.
