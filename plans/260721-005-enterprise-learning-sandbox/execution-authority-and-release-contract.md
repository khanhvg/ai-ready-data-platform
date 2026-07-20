# Execution, Authority, and Release Contract

## Status and Scope

This companion is normative for every future issue in the implementation graph. It closes
cross-phase execution, authority, handoff, and release ambiguities; it does not authorize issue
creation, implementation, Terraform apply, cloud access, or an AI runtime. If a phase conflicts
with this file, the stricter safety/authority rule here wins and the conflict must be corrected
before that issue starts.

## Earliest Reviewable and Earliest Accepted Outcomes

Two outcomes must not be conflated:

1. **I5-02 reviewable preview:** a static/no-privilege shell may be shown early using an explicitly
   labelled contract fixture. It has no runner, no completion mutation, no decision score, and no
   product/release claim. It exists to obtain novice/accessibility feedback on content order,
   progressive disclosure, reversible navigation, controlled-versus-environmental failure copy,
   hints, reset explanation, evidence explanation, and non-copying review.
2. **I5-05 accepted learner outcome:** only the real runner-backed promotion-trust journey can
   satisfy OWN-02/PH-C08 or claim usable completion. It consumes the merged I5-01 contract and
   content-addressed golden fixture handoff, accepted ADR-005, released I5-03 contracts, and I5-04
   runner.

I5-01 and I5-02 may start in parallel only under a two-stage barrier. Before I5-01 merges, I5-02
may build the unscored preview and common tests. I5-01 publishes the tracked
`contracts/data/retail-golden-v1.json` and sanitized
`tests/fixtures/learning/promotion-trust/{evidence-v1.json,manifest.json}` containing producer
commit, contract hash, fixture hash, tool versions, and retention locator. After that merge, I5-02 must
replay all candidates against exactly that handoff. No measurement, weighted score, framework
ADR, or candidate-specific data-shape workaround produced against the provisional fixture may be
carried into the decision without rerun. The ADR records the exact I5-01 merge SHA and hashes.

### ADR-005 time box and retention

- Total elapsed implementation budget: 14 working hours over at most two implementation days.
- Common contract/harness and early reviewable preview: at most 3 hours.
- Each candidate: at most 3 hours, with the same order-rotated tests and fixture. Kill a candidate
  at 90 minutes if it cannot install, render the static route, and consume the common lesson
  contract; kill at its 3-hour cap if any must-pass remains red. A killed candidate is eliminated,
  not assigned a synthetic score.
- Scorecard, rerun, and ADR: at most 2 hours. If no candidate passes at the total cap, ADR-005 stays
  `Proposed`; I5-05 is blocked and the owner decides whether to narrow requirements or authorize a
  new spike. The tie default is not a bypass.
- Keep source, lockfile, exact commands, fixture hashes, and test/measurement artifacts for all
  candidates until I5-05 merges. Losers are excluded from product builds. A later reviewed cleanup
  may remove loser source only after storing a reproducible source bundle and hash in retained
  release artifacts; scorecard and source/non-copy inventory remain tracked.

## Promotion-Trust Analytical Contract

The existing four marts do not share a campaign/order/time grain:

- promotion: `promo_name, channel`;
- fulfillment: `carrier, region`;
- returns: `reason, category, region`;
- data quality: global scenario/count evidence.

Therefore `promotion-trust-v1` is a **four-mart decision-evidence bundle**, not a causal join or a
campaign-level composite metric. The verifier may prove that a promotion headline is
decision-insufficient and require separately labelled operational/returns/quality context. It
must display each mart's grain, time scope, filters, numerator/denominator, weighted aggregation,
and limitation. It must not attribute a carrier delay, return reason, or global DQ count to a
specific promotion without a common key.

Before I5-02 freezes the real fixture, I5-01 owns a versioned query/assertion manifest with exact
columns, ordering, thresholds/TBCs, expected warning IDs, and failure/remediation IDs. If the
owner later requires causal campaign attribution, I5-07 must propose an additive order/promotion-
grain decision product and ADR while preserving the existing 11 marts, their lineage, warning
semantics, and Rill weighted metrics. A hidden cross-grain join is a release failure.

## Local State, Mutation, and Evidence Authority

| State | Durable authority | Projection/cache | Commit and recovery rule |
|---|---|---|---|
| Lesson/progress | Portal SQLite event/state rows | Browser state | Compare-and-set on released transition version; browser never authors completion |
| Workspace/operation/idempotency | Runner journal keyed by `workspaceId/operationId` | Portal status | Runner is sole writer; retry returns committed result or typed conflict |
| Verification | Runner verifier result keyed by run + verifier hash | Portal display | Only a fresh trusted runner result can request completion |
| Evidence bytes | Immutable filesystem blob keyed by content hash | Portal evidence index | Stage, flush/fsync, atomic rename, then index; never overwrite |
| Completion | Portal SQLite transaction referencing committed runner result and evidence blob | Derived progress view | Unique run/evidence constraints; one transaction writes evidence index + completion event |
| Curated release | `CuratedReleaseManifest` and one atomic `current-release` pointer | Parquet, Iceberg, ClickHouse, Rill, metadata/search | Stage and validate all assets, then move one pointer; consumers pin one release ID |

The runner never writes portal completion directly. If evidence commits but the portal transaction
does not, it is an orphan and cannot grant completion. Startup reconciliation verifies the blob
and runner journal, then either attaches it idempotently through the same transaction or
quarantines it. Process-kill, ENOSPC, duplicate request, and restart tests inject failure before
and after blob flush, rename, result commit, portal transaction, and acknowledgment.

Every mutating entrypoint—including runner commands, direct expert Make targets, and Airflow
callables—must acquire the same lease/fencing token for the affected workspace and
warehouse/export/catalog namespace. Direct expert mode uses a distinct namespace by default and
refuses to mutate a learner namespace while a lease is active. Barrier tests cross runner/Make,
runner/Airflow, reset/publish, and verify/publish; per-API locks alone do not pass.

### Atomic curated release

`CuratedReleaseManifest` contains `releaseId`, `dataRunId`, input Git SHA, golden/data/dbt/semantic
contract hashes, and for all 11 marts: schema hash, row count, content checksum, staged locator,
and engine snapshot/version ID. Publishing stages and verifies the complete set, then atomically
changes one `current-release` pointer. Rill exports, ClickHouse hydration, Iceberg tables,
OpenMetadata/Superset assets, and learner evidence record the same release ID. Failure retains
the previous pointer; a mixed generation is never `ready`. OpenMetadata reconciliation is scoped
by workspace/release namespace and a managed-object marker, preserves unmanaged entities, and
compares exact FQNs, ownership, tags, and lineage edges rather than only counts.

### Honest local evidence guarantee

The canonical unkeyed SHA-256 detects corruption and inconsistent edits; it does **not** prove
authorship against the owner of the same local account, filesystem, SQLite database, and verifier
code. Local completion is trusted only because the running portal accepts a fresh result from the
private runner and rechecks the evidence, artifact, contract, verifier, and release hashes.
Documentation/tests must say “tamper-evident corruption detection within the local single-actor
threat model,” not cryptographic anti-forgery or non-repudiation. Hosted anti-forgery requires an
authority/key outside learner-writable state and remains gated by I5-14.

## Local Execution and Browser Security

Typed argument arrays and `shell=False` are necessary but not an execution sandbox. I5-04 must:

- execute only pinned, hash-verified entrypoints from a read-only base/runtime; an interpreter may
  not import learner-controlled code, plugins, startup hooks, config macros, `PYTHONPATH`, or
  executable files from the workspace;
- use an OS containment boundary with no ambient repository write, home/cloud credentials, or
  outbound network; if the selected host cannot enforce it, the runner stays disabled and the
  static/direct-expert path is the only supported path;
- resolve beneath pre-opened workspace roots, reject symlink/hardlink/device/special-file races,
  and revalidate file identity at use time; path string normalization alone does not pass;
- bound and sanitize child stdout/stderr before persistence or display, redact secret canaries and
  absolute paths, and kill the complete process group on timeout/cancel;
- prove the above with malicious-import, startup-hook, TOCTOU, output-flood, descendant-process,
  environment, network, secret, and base-write tests.

Loopback is a routing property, not browser authentication. The portal and HTTP runner fallback
must use exact `Host`/`Origin` allow-lists, no wildcard CORS, launch-scoped high-entropy secrets,
HttpOnly/SameSite session cookies where a browser session exists, CSRF protection on mutations,
and DNS-rebinding/cross-origin negative tests. Prefer a Unix socket for the runner. A stable port
or URL parameter is not a secret.

## API and Architecture Delivery Contract

Before I5-05, I5-01 owns and renders the minimum local source set:
`C4-L0`, `C4-L1`, `C4-L2-LOCAL`, `C4-L3-RUNNER`, `DEP-LOCAL`, and `DYN-JOURNEY`, with manifest,
structured text alternatives, and stable include seams. I5-06 consumes those sources read-only,
then owns curriculum/AWS expansions and `DYN-PUBLISH`. It may not rewrite an earlier ID without a
shared-core migration. Phase 6 starts only after the merged I5-05 E2E; its stale “parallel after
Phase 3” wording is invalid.

I5-03 owns an operation matrix. Every operation records HTTP path/method, `operationId`, logical
Experience/Process/System/Backend/Technical taxonomy, physical process/module, authority,
authentication/CSRF rule, idempotency, and evidence. The minimum matrix includes lessons,
progress, workspace, operation status, reset, verify, evidence, external-tool status/deep links,
data-product query, and technical liveness/readiness. Adding taxonomy metadata without an
operation is not traceability.

I5-06 must ship at least one executable architecture journey covering the F01→F04→J01/J04/J05
chain: edit a bounded requirement/ADR or view decision, trigger a controlled boundary/resilience
failure, receive a hint, reset, verify an architecture fitness function, retain evidence, and
reflect. Templates/diagrams alone do not satisfy the architecture-first learning outcome.

## Command, Lifecycle, Resource, and Evidence Registry

All commands below are **future targets** unless the immutable input Makefile already contains
them. The owning issue adds each target to tracked `Makefile` help; declaring it here does not make
it available. Every target is non-interactive, uses a unique worktree namespace, emits a
schema-valid `FitnessResult` below `.artifacts/evidence/<fitness-id>/<run-id>/`, and exits non-zero
on required failure. Allowed statuses are `pass`, `fail`, `blocked-tbc`, and
`not-run-optional`; a missing tool for a required gate is `fail`, never skip.

I5-01 adds the only root `Makefile` change: help plus inclusion of `mk/issue-5/*.mk`. Each later
owner writes only `mk/issue-5/i5-<nn>.mk`; any root change requires a serialized shared-core lease.

| Owner | Future targets | Tier / security gate | Required evidence and failure boundary |
|---|---|---|---|
| I5-01 | `help`, `golden-clean`, `data-contracts-check`, `evidence-contracts-check`, `migration-contracts-check`, `architecture-check`, `architecture-render` | core / S3 + preservation | Discoverable registry plus golden/data/evidence/view IDs and exact input SHA; fail on drift, missing tool, dirty base, or unrendered required local view |
| I5-02 | `learn-preview`, `web-spike-scorecard-check` | core / S3 + non-copy | Preview is explicitly unscored; score requires real I5-01 handoff, equal assertions, retained artifacts, and all must-gates |
| I5-03 | `learning-contracts-check`, `lesson-check`, `api-contracts-check`, `evidence-verify` | core / S3 + schema | Contract/API matrix, evidence and generated-type hashes; fail missing operation/authority/migration |
| I5-04 | `runner-test`, `runner-security-test`, `runner-race-test` | core / S3 privileged boundary | Unit, RCE/TOCTOU/browser-boundary, cross-entrypoint barrier, crash and leak evidence |
| I5-05 | `learn`, `learn-status`, `learn-down`, `portal-test`, `portal-a11y`, `portal-e2e`, `lesson-e2e`, `local-journey-e2e`, `portal-visual-review` | core / S3 browser + runner | URL/PIDs/workspace/evidence root, journey and teardown; required browser/manual gates cannot skip |
| I5-06 | `curriculum-check`, `traceability-check`, `architecture-visual-review`, `architecture-lab-e2e` | core / S3 architecture lab | Prerequisite/ID/ADR/view/runnable-lab evidence; fail decorative/unexecutable content |
| I5-07 | `data-labs-e2e`, `lake-contracts-check`, `lake-fault-test`, `metadata-contracts-check`, `metadata-reconcile-test` | optional local profiles / S3 data authority | Release ID, 11-asset atomicity, exact identities/edges, fault/recovery evidence |
| I5-08 | `compose-check`, `compose-security-check`, `profile-budget-check`, `recovery-test` | full-local optional / S3 runtime | Normalized measurements/profile admission/teardown; Docker absence is `not-run-optional` only for Compose-heavy profiles |
| I5-09 | `state-matrix-check`, `cost-model-check`, `aws-decision-check` | AWS non-applying / S3 + owner TBC | Authority/BOM/source freshness/gate state; unresolved gate is `blocked-tbc`, never pass |
| I5-10 | `terraform-check`, `terraform-validate-offline`, `terraform-test-mocked`, `terraform-plan-aws` | AWS non-applying; real plan credential-gated / S3 + Terraform | Offline syntax/policy and explicitly mocked test evidence; only real provider plan may emit a plan claim |
| I5-11 | `aws-adapters-contract`, `engine-equivalence`, `aws-composition-check`, `aws-restore-drill` | AWS adapter; real drill separately authorized / S3 data recovery | Descriptor-to-module composition, real compatibility/restore only in approved validation environment |
| I5-12 | `ai-admission-check`, `ai-evals` | optional AI / S3 + AI admission | Profile-specific admission and evals; credentialed eval is optional until authorized, never N/A for hosted claim |
| I5-13 | `release-evidence` | release / all inherited gates | Clean-checkout aggregate, required/optional registry, rollback, tested-tree provenance |
| I5-14 | `hosted-authz-test`, `hosted-isolation-test` | hosted later / S3 identity | Tenant/object/role denial and learner-ingress authorization |

`make learn LESSON=promotion-trust` and `make local-journey-e2e` must work after dependency install
when Docker is unavailable: host-run portal, isolated runner, DuckDB, and fixture/golden path only.
They must not invoke `docker`, Compose, Rill, Airflow, Iceberg, OpenMetadata, Superset, or AWS.
`make learn-status` reports owned processes, readiness, workspace, and evidence root.
`make learn-down` is idempotent, stops only the recorded process group, retains committed evidence,
removes scoped temporary secrets/workspaces per policy, and proves no owned process remains.
Compose-heavy profiles are optional Phase 8 extensions and cannot redefine core acceptance.

The 16 GiB ceiling is a hardware envelope, not approval of the provisional per-process numbers.
Phase 8 must label all numeric thresholds `candidate` until the product/runtime owner approves them
from repeated measurements. Evidence records OS, architecture, physical/available memory, swap,
Docker/VM settings, pre-existing baseline, process tree and container attribution, deduplication
rules, sample interval/window, cold/warm repetitions, peak RSS/CPU/disk/network, readiness, and
teardown. Unsupported platforms are `not-run-optional`; double-counted or extrapolated results
cannot approve a profile.

Release provenance distinguishes:

- `testedTreeSha`: the immutable commit checked in the clean worktree;
- `attestationCommitSha`: the child commit that adds tracked human-readable evidence, if any;
- `mergeOrTagSha`: recorded externally in the GitHub release/issue attestation after merge.

A tracked file cannot truthfully contain its own commit SHA. Acceptance verifies ancestry and
tree/content hashes; it never recursively rewrites evidence to chase a new SHA.

## AWS Offline, Validation, Apply, Recovery, and Cost Contract

I5-10 owns Terraform for every accepted Phase 9 state row, including selected modules for data
lake/catalog, metadata database, search, portal progress/evidence, secrets/KMS, and backup/recovery
in addition to network/IAM/ECS/office-hours/observability. I5-11 owns adapters and deployment
descriptors but never Terraform. A sequential I5-11 composition gate consumes exact I5-10 outputs
and exact I5-11 descriptor/image hashes and simulates open→hydrate/restore→readiness→drain→backup→
close plus failed-start/retry. Parallel module/adapter work cannot claim AWS readiness by itself.

`terraform-validate-offline` and `terraform-test-mocked` prove syntax, module wiring assertions,
and policy behavior without credentials. Mock-provider values are labelled `mocked`; they do not
prove provider/API compatibility, account reachability, real pricing, deployability, or restore.
`terraform-plan-aws` is the only plan-named target and requires real provider initialization plus
the exact account/region/role gate. An offline check cannot satisfy an apply admission row.

The first real compatibility and empty-restore evidence cannot be a prerequisite to creating the
environment that produces it. Before any production/classroom apply, a separate future owner must
authorize either an exact pre-existing validation environment or one disposable validation-
environment apply with account, region, least-privilege role, no production data, budget cap,
service quotas, TTL, automatic teardown, residual-resource scan, and human security/FinOps
approval. That drill may clear compatibility/restore evidence; it does not authorize a later
production apply. This plan performs neither action.

Every future apply authorization is a single-use envelope bound to saved binary plan hash,
tested Git/config/module/provider-lock/variable hashes, backend bucket/key, state lineage/serial,
account, region, environment, caller role, approver identity, issue/run ID, nonce, creation/expiry,
and consumption status. Apply consumes that exact saved plan without replanning. Approval is
invalid after any bound value changes. Recovery authority is separate from normal apply: state/S3
versions and deletion protection are tested, KMS/application encryption/signing keys and secret
versions have rotation/escrow/deletion owners, and restore validates ciphertext/config
compatibility as well as object checksums.

No learner-reachable AWS ingress exists before I5-14. P10/P11 validation before I5-14 is private
operator-only adapter testing in the authorized validation environment. I5-14 must precede any
hosted learner claim and owns IdP/session, tenant/object authorization, quotas, retention/deletion,
and cross-user evidence. “Localhost” or a security group is not hosted identity.

The cost model is reconciled in both directions with the accepted topology and, when authorized,
Terraform plan JSON plus post-teardown inventory. Every resource/category—NAT/endpoints, ALB/DNS/
TLS, EC2/ECS, RDS/database, OpenSearch/search, EBS/snapshots, S3 versions/requests, KMS/secrets,
logs/traces, Terraform state, backups and residual network/storage—has quantity, unit, currency,
region, price-list offer/SKU/dimension or explicit exclusion reason, source URL/API, effective/as-
of date, retrieval time, freshness TTL, and approval-cycle refresh rule. Current price data is a
gate, not a hard-coded planning fact. Office-hours modeling includes scheduled desired-capacity
changes, actual ECS/ASG scale-from-zero launch behavior and lag, warmup, readiness, drain,
failure/retry storms, and residual cost; a schedule alone is never called scale-to-zero.

`CostGuard` has one durable owner and state machine: admit/deny, warn, block-new-work, drain/cancel,
scale-down/teardown, residual scan, break-glass, and reconciliation. Triggers, actions and protected
state are machine-readable. An alarm without an enforcing authority is evidence of monitoring,
not a kill switch.

## Optional AI Admission Contract

Admission has two profiles:

- `local-single-actor-read-only`: no hosted ACL claim, no AgentCore/AWS requirement, versioned
  governed source/citations, injection/redaction/eval/OTel/cost limits, and no tools with effects.
- `hosted-agentcore`: requires I5-14, real tenant/object ACL propagation, region/service support,
  retention/deletion, priced limits, and every relevant AWS/apply/state gate. No hosted security
  field may be marked not-applicable because the local profile passed.

I5-12 first produces an admission report and responsibility ADR; passing it does not authorize or
automatically create `apps/agent-labs/**` or AgentCore resources. Any runtime implementation is a
separate, human-authorized follow-up after admission. The ADR selects one durable workflow,
approval, and idempotency authority: LangGraph may own explainable agent-graph flow; Restate may
own durable effects/recovery only if admitted; AgentCore session memory is never authoritative.

An approval binds actor, policy/data versions, exact tool ID, canonical arguments, target resource
and environment, expected effect, idempotency key, cost bound, expiry, nonce, and approval digest.
Changing any bound value requires new approval. Delayed/uncertain effects reconcile before retry.
Retrieval/citation evidence binds ACL decision, source/product/version/chunk/content hash, eval
dataset/threshold version, OTel correlation, redaction and cost; unsupported claims remain visible.
