# Security, Recovery, Observability, Rollback, and Evidence

## Threat and data model

Protected information includes Terraform state/plan/config, KMS and application key references,
secret versions, durable data/catalog/metadata, budgets and topology decisions, and integrity of
decision/evidence artifacts. Evidence must not contain credentials, AWS account IDs, resource
identifiers tied to an account, customer/learner PII, private filesystem paths, environment
values, or raw sensitive logs.

SHA-256 proves local content integrity only. It does not prove publisher identity,
non-repudiation, release authority, or AWS compatibility. Hosted signing is outside Issue #14.

## S3 threat matrix

| Threat ID | Attack / failure | Required preventive control | Required detection/test | Recovery / residual risk |
|---|---|---|---|---|
| TH-001 | Malicious pricing snapshot changes a rate/formula/quantity | Raw source and canonical projection hashes; formula registry; rates are data, never executable | Mutate each field/hash/formula ID | Reject snapshot; restore prior accepted snapshot |
| TH-002 | Unit confusion (`GB`/`GiB`, hour/month, per-1K/per-request) | Closed dimensioned unit registry and explicit conversions | Cross-dimension and ambiguous-unit fixtures | Deny cost result; no inferred conversion |
| TH-003 | Currency/region/SKU mismatch | USD-only guard contract; product region distinct from API endpoint; exact SKU/dimension | Foreign currency/region/term/rate fixtures | `blocked-tbc`; refresh correct source |
| TH-004 | URL/path injection or source substitution | HTTPS-only allow-listed hosts; canonical URL policy; rooted repo-relative locators | userinfo/redirect/query/fragment/traversal/absolute/private path cases | Reject candidate; retain prior snapshot |
| TH-005 | Duplicate keys, aliases, non-finite or overflow values | Strict duplicate-aware parser; no YAML aliases; bounded Decimal/string/collection/nesting | duplicate, NaN, ±Infinity, exponent/precision/size bombs | Typed failure before arithmetic |
| TH-006 | Shell/command injection through region/schedule/path/ID | Argument-list subprocesses only; closed value grammars; no shell/eval/templates as code | metacharacter/newline/NUL/option-smuggling cases | Deny input; bounded remediation |
| TH-007 | Symlink/hardlink/special-file/TOCTOU source attack | Private rooted workspace; `lstat`/open/fstat identity; regular file; link count one; no following links | symlink swap, hardlink, FIFO/device/socket, pre-existing destination | Refuse file; preserve forensic failure evidence |
| TH-008 | Credentials/account IDs/private paths/PII leak to model/evidence/Git | Structural redaction + canary scans; repository-relative public-safe locators; bounded outputs | AWS key/token/account-ID/home-directory/temp/user/customer canaries | Quarantine/delete only unsafe issue-owned bundle; rotate/revoke externally if real leak |
| TH-009 | Terraform state/lock/backend compromise | S3 versioning/lockfile, TLS, encryption, least privilege, separate roles, exact state path | concurrent lock, wrong identity/state/version, missing encryption/transport cases | No plan/apply; restore prior state version under owner runbook |
| TH-010 | KMS key deletion makes state/data irrecoverable | Separate key admin/use roles; deletion wait/alarms; ciphertext inventory; key/config dependency graph | disabled/pending-deletion/wrong-key/rotation rollback cases | Cancel deletion when possible; otherwise not ready and declared data-loss boundary |
| TH-011 | Broad IAM or public network exposes data/runner | Deny wildcard/broad ingress/static credentials; exact flows and role actions | policy/reachability/placeholder-secret mutations | Reject option/topology; revoke role/security group later under authority |
| TH-012 | Destructive teardown deletes durable truth/evidence/keys | Preserve default; exact resource/owner/mode binding; evidence and keys deny-listed | missing mode, wildcard, foreign resource, active dependency, destroy replay | Refuse action; restore prior state only under separate runbook |
| TH-013 | Backup says success but bytes/semantics are corrupt | Content hashes, consistency-group manifest, empty restore, semantic oracles | truncation, bit flip, wrong key/version, partial group | Retain/use previous known-good; no ready/close claim |
| TH-014 | Catalog/metadata/search restore is inconsistent | Cross-component release/version/watermark binding and dependency-aware readiness | stale search, missing dashboard, wrong catalog pointer, mixed generation | Rebuild/reconcile or roll complete group |
| TH-015 | Evidence tamper/replay/substitution | Canonical immutable manifest, exact command/input/tested-tree hashes, run ID and parent-free hash index | mutate, duplicate artifact, foreign run, replay/expiry, recursive self-hash | Reject/quarantine; regenerate from exact clean input |
| TH-016 | CostGuard bypass via rounding/negative/duplicate top line | Unrounded exact comparison; non-negative finite values; unique IDs; stable sorting | near-cent budget, negative line, duplicate ID, overflow | Deny; no fallback budget |
| TH-017 | Schedule replay/out-of-order transition duplicates effects | Durable state machine, idempotency/fencing, transition preconditions, reconciliation | duplicate/missed/out-of-order events and crash barriers | Reconcile to prior safe or stopped-not-ready |
| TH-018 | Optional agent state/trace retains sensitive data or becomes authority | AI off by default; classification/ACL/retention/deletion; runtime memory never durable authority | disabled-core, ACL, prompt/tool injection, retention/delete/replay tests | Disable/revoke/delete admitted state; preserve governed source |
| TH-019 | Live refresh or current time makes offline release irreproducible | Checked-in accepted snapshot; clock injected/frozen; network denied for core | run with no network/credentials and altered host time | Fail live-only gate; use accepted snapshot |
| TH-020 | Resource/BOM row is unpriced or maps to invented Terraform path | Exact bidirectional mapping and released concern IDs | orphan/duplicate/wildcard/stale mapping fixtures | Reject selected topology/estimate |

No Critical/High threat may remain unresolved for implementation readiness. This planner does not
perform that readiness determination.

## Security control requirements

### Terraform backend, lock, IAM, and KMS

- Separate backend bootstrap/recovery, plan, apply, workload, backup/restore, key-administration,
  and evidence roles as selected; no ambient/static credentials.
- S3 Block Public Access, bucket-owner-enforced ownership, TLS-only access, encryption, versioning,
  S3 lockfile and exact-prefix actions are future acceptance requirements; exact KMS topology is
  still `TBC`.
- State/plan/config/log output is sensitive even if Terraform marks values sensitive. Evidence
  records hashes and safe projections, never full state/plan or account/resource identifiers.
- Wrong account/region/environment/workspace/input SHA/role/plan/config/lock/snapshot identity
  fails before any cloud action. This issue itself never evaluates a real account.
- Key deletion, backup deletion, object lifecycle expiration, catalog drop, DB/search deletion,
  and destroy require independent named authority and cannot be triggered by default test targets.

### Parser and filesystem boundary

- Input format has one canonical encoding and strict duplicate-name parsing before object mapping.
- Accept only finite bounded canonical decimal strings; reject float coercion and scientific
  values outside the accepted precision/exponent contract.
- Validate syntax, size, count, depth, unit, currency, region, URL and ID before use.
- Read accepted snapshot/evidence files from an issue-owned private workspace using descriptor
  identity checks; reject links, non-regular files, multiple links, ownership/mode mismatch, and
  post-open mutation.
- Write atomically to new run-scoped paths with restrictive permissions. Never overwrite prior
  evidence or follow caller-controlled output paths.
- Subprocesses receive fixed executable plus validated argument list, closed stdin, clean env,
  bounded time/output, process-group termination, and no `shell=True`.

## Recovery contract

### Backup consistency

Each backup has a consistency-group manifest containing component IDs, source generation,
schema/config/key versions, start/end/checkpoint time, RPO observation, object/content hashes,
writer-fence evidence, backup result, and restore-oracle version. A successful API/job status
without a complete manifest and restore proof is `backup-unverified`, never pass.

Write fencing and consistency technique are option-specific: quiesce/drain, application snapshot,
database-native backup, immutable manifest/pointer, or rebuildable projection. The ADR must state
what writes can occur during backup and what the recovery point means.

### Restore test protocol

1. Select an accepted recovery point without modifying the source or prior known-good point.
2. Prove required keys/config/schema/tool versions are available.
3. Restore into a new isolated target; never overwrite by default.
4. Rebuild derived projections/indexes only from declared authorities.
5. Run structural and semantic oracles: object/hash/set, catalog pointer/table operations,
   ClickHouse schema/row/query/metric equivalence, OpenMetadata entities/lineage/search freshness,
   Superset dashboards/datasources/session/key behavior, scheduler/CostGuard reconciliation.
6. Measure observed RPO/RTO separately from owner objectives; fail if either is missing or missed.
7. Delete only the exact restore-test resources after validation and verify residual cost/inventory;
   evidence persists.

Real AWS restore tests remain separately authorized. Offline fixtures prove model behavior, not
service compatibility or achieved RTO.

### Failure dispositions

| Failure | Required disposition |
|---|---|
| Key unavailable/deleted | Not ready; block teardown/migration; recover key reference/material only under accepted runbook or declare unrecoverable loss |
| Latest backup corrupt | Quarantine; restore prior known-good; investigate consistency/fence; retain hashes |
| AZ failure | Follow selected single-/multi-AZ design and state loss boundary; never upgrade claim after incident |
| Region failure | `deferred` or selected cross-region runbook with separately costed replication; no implicit failover |
| Catalog loss | Reconstruct/reconcile from durable manifests/objects if proved, otherwise restore prior complete catalog state |
| Metadata DB loss | Restore consistent DB then migrations and semantic asset checks |
| Search loss | Rebuild from DB/catalog source or restore accepted snapshot; remain not-ready until freshness/oracles pass |
| ClickHouse loss | Rehydrate disposable projection or restore durable data per ADR; equivalence before ready |
| Schedule failure | Reconcile durable transition/idempotency state; no blind retry of destructive steps |
| CostGuard failure | Deny new opening/plan/apply transition; existing-safe shutdown follows DR/ops policy, not abrupt data loss |

## Teardown and break-glass

Two explicit modes only:

- `preserve`: stop/drain replaceable compute, retain declared durable state/keys/backups/evidence,
  inventory residual costs, and verify restart/restore prerequisites. This is the default.
- `destroy`: separately authorized exact environment/resource set after backup/restore evidence,
  retention/legal/security checks, key/ciphertext dependency checks, CostGuard reconciliation,
  and human confirmation. Evidence and unrelated/foreign resources are always preserved.

Break-glass is not a wildcard. It binds actor, reason, incident, exact action/resource/state,
expected loss, cost bound, expiry, nonce, approval digest, and reconciliation. Replay, scope
change, expired approval, wrong actor/environment/SHA, missing backup, or unknown dependent state
denies the action.

## Observability contract

Decision/runtime evidence must expose without sensitive identifiers:

| Domain | Required signals |
|---|---|
| Cost | scenario subtotal, contingency, guard total/status, price age, top driver IDs, residual inventory count/cost, budget headroom |
| Schedule | requested/current state, transition age, next run, calendar/timezone version, retries/DLQ, override state, active work/drain count |
| Readiness | dependency health, restore/hydration/migration progress, query/catalog/search/dashboard/evidence oracle status |
| Backup/restore | consistency group, recovery point age, backup/restore result, observed RPO/RTO, validation and cleanup status |
| State/security | lock contention, wrong-authority denial, key state/rotation age, secret/config version, public/IAM policy denial counts |
| Data | release/snapshot/checkpoint IDs, ClickHouse equivalence, catalog pointer consistency, metadata/search watermark |
| Evidence | tested-tree/input/snapshot/topology/state hashes, artifact count/bytes, redaction class, verifier result, rollback result |

Metrics, logs, traces, alarms, backup evaluations, scheduler retries, and evidence storage are cost
dimensions when selected. Retention and cardinality are bounded. No raw Terraform state, plan,
secret, account/resource ID, user query, PII, or private path appears in telemetry/evidence.

## Evidence layout

Future runs use:

```text
.artifacts/evidence/aws-decisions/<run-id>/
  result.json
  manifest.json
  authority-projection.json
  state-matrix-result.json
  option-decision-result.json
  bom-reconciliation-result.json
  cost-result.json
  costguard-result.json
  pricing-provenance.json
  schedule-recovery-result.json
  security-result.json
  rollback-result.json
```

`manifest.json` lists every other artifact by repository-relative run path, media type, byte size,
SHA-256, schema version, producer step, redaction class, and verification status. It does not hash
itself or contain a future attestation commit. `result.json` uses the released compatible
`fitness-result-v1` contract only after the exact dependency amendment maps it.

Required statuses: `pass`, `fail`, `blocked-tbc`, and `not-run-optional`. Missing required tools,
snapshot, evidence, or fields are `fail` or `blocked-tbc` as specified, never skip. Optional live
source refresh is `not-run-optional` only for refresh; accepted offline snapshot tests remain
required.

## Evidence replay and provenance

- Bind input SHA, tested-tree SHA, dependency release SHAs, schema/model/formula/unit registry
  hashes, state/BOM/topology hashes, pricing raw/projection hashes, exact command/args and tool
  versions.
- Bind caller region/schedule/budget/contingency only as safe normalized values; never bind or
  emit account ID or account-specific resource data.
- Preserve raw public pricing source only when license/size/policy allows; otherwise store exact
  public URL/API identifiers and source hash with a reviewable normalized projection.
- Offline verification rejects foreign tested tree, stale snapshot, missing artifact, duplicate
  path, hash mismatch, unexpected artifact, non-canonical document, or replayed/expired authority.
- Git commit ancestry and GitHub human comments supply external workflow provenance; local hashes
  do not claim human identity.

## Rollback contract

Implementation rollback is additions-only and removes/reverts only exact Issue #14-owned files
after preserving failure evidence. It must restore the prior command-registry behavior (the I5-09
entries stay `future-owner` if implementation is withdrawn), leave root Make/shared contracts/
views/golden semantics untouched, retain the previous accepted pricing snapshot and ADR versions,
and invalidate dependent CostGuard/BOM decisions when a selected ADR is reopened.

Cloud rollback is outside current authority. A later environment-specific runbook must restore
the last complete state/catalog/metadata/key/config generation, disable unsafe schedules/roles,
inventory residual resources/cost, and retain evidence. “Destroy everything” is not rollback.
