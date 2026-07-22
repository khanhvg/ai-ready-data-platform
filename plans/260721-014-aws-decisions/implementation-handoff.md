# Implementation Amendment and Execution Handoff

## Current disposition

```yaml
planStatus: planner-only-not-validated
implementationAuthority: none
implementationFileAllowlist: []
commandAllowlist: []
dependencyReleaseShas: []
releasedIssue11ConcernIds: []
pricingSnapshot: []
bom: []
terraformBindings: []
region: []
accountEnvironment: []
budgetAndContingency: []
applyApproval: []
cloudAction: none
```

The three named Make targets are future command-contract declarations, not current runnable
authority. This file is not a cook instruction until the amendment/revalidation/readiness chain
below is complete.

## Mandatory gate sequence

1. Issue #11 publishes an immutable released architecture/curriculum concern handoff with exact
   release SHA, stable concern IDs, source paths/hashes, and acceptance semantics.
2. Start from a fresh clean exact SHA containing Issue #6 and the released Issue #11 handoff.
3. Amend only this plan directory to populate exact dependency/current-authority fields, concern
   crosswalk, candidate option constraints, current official-source inventory, exact implementation
   file/command allow-lists, protected baseline, and future verification matrix.
4. Publish that amendment and run a fresh independent plan revalidation at its exact head.
5. Run a separate fresh dependency-aware readiness audit. It must name a non-empty cook scope;
   branch/candidate/validation alone is not readiness.
6. Only then run one tests-first implementation session inside the exact allow-list. No AWS call,
   Terraform plan/apply/destroy, credential/account read, or resource action is implied.
7. Run independent exact-head code/security review, required offline tests and blast radius,
   obtain mandatory human exact-head pre-merge approval, then use the repository merge workflow.
8. Any later real AWS/Terraform plan or apply is another separately authorized operation with a
   named owner, exact account/environment/region/saved plan/expiry and current budget evidence.

If any step changes the exact head, repeat the downstream exact-head gates.

## Amendment contents

The amendment must convert each empty field into an exact, reviewable value or keep it
`blocked-tbc`. It must not invent future resources merely to make fields non-empty.

| Field | Required amendment evidence |
|---|---|
| Dependency release | Issue #11 release SHA, GitHub release/merge comment, ancestry, source/hash read-back |
| Concern mapping | Stable released IDs mapped to FR/NFR/state/option/BOM/test/evidence rows |
| File allow-list | Every exact repo-relative regular file, action, owner, schema, max size, test and rollback; no wildcard except the already authorized ownership envelope in prose |
| Command allow-list | Exact three targets, direct script/test entrypoints, args/env, timeout/output bounds, evidence IDs and failure codes |
| Protected baseline | Exact Issue #6/#11 file/tree hashes, absences, semantic invariants, and changed-path checker |
| Pricing authority | Exact candidate snapshot path/schema, allowed source hosts/APIs, extractor version, freshness policy, currency/unit registry |
| BOM contract | Exact schema fields and released concern linkage; actual service/resource rows only after option evidence |
| Owner TBCs | Named role/value/evidence/expiry without account IDs or secrets in tracked files |

## Candidate ownership envelope, not an allow-list

Issue #14 may eventually write only:

```text
docs/decisions/aws/**
cost/state decision models and their tests
mk/issue-5/i5-09.mk
```

This envelope does not authorize exact files today. The amendment must choose existing-pattern
locations without editing shared contract/architecture/portal/runner/lab/root files. If the
implementation needs a shared schema, command registry edit, architecture view, Terraform module,
adapter, root Make change, or other path, STOP and request the serialized owner lease/new issue.

## Tests-first sequence

### RED-A — authority and schema completeness

Write failing fixtures first for empty/duplicate/contradictory authority, state, option, BOM,
price, cost, TBC, schedule, teardown, and evidence rows. Record stable assertion IDs and prove
each failure occurs before production/model code exists.

### RED-B — cost and CostGuard golden cases

Write offline golden fixtures for:

- 730-hour baseline and schedule-derived demo hours;
- compute stopped with every selected persistent/fixed dimension retained;
- storage/object/request/log/backup/transfer growth;
- NAT versus endpoint versus controlled-egress alternatives only where admitted;
- startup/hydration/drain/backup/retry/orphan-cleanup hours and requests;
- contingency, unrounded comparison, half-up display rounding and near-cent budget edges;
- missing/invalid/TBC budget, region, schedule, contingency and snapshot;
- stale source, wrong region/currency/unit/SKU/dimension and unsupported conversions;
- non-finite, negative, duplicate, precision/exponent/collection/size overflow;
- over-budget denial, stable top drivers, and pre-authored alternative IDs.

### RED-C — state, teardown and recovery

Write failing cases for missing writer/reader/authority/key/config/backup/restore/RPO/RTO/
retention/deletion/migration fields; duplicate writers/authorities; cyclic restore/key dependencies;
backend lock/version/replay; preserve/destroy confusion; empty start; interrupted hydration;
corrupt backup; key loss; catalog/metadata/search inconsistency; schedule replay; and readiness
before oracles.

### RED-D — BOM/topology/provenance reconciliation

Write failing cases for orphan/duplicate/wildcard/stale Terraform binding, unpriced resource/data
source, price without BOM, state without binding, missing released concern, incompatible option,
stale snapshot, and live-refresh-only evidence.

### RED-E — S3 adversarial boundary

Write the complete TH-001..TH-020 fixtures before accepting parser/filesystem/process/evidence
behavior. Include duplicate names, NaN/Infinity, malicious formula/unit/currency/URL/path,
credentials/account/private-path/PII canaries, symlink/hardlink/FIFO/device/socket, command/option
injection, TOCTOU swap, key/backend/IAM misuse, destructive teardown, backup tamper, and evidence
replay/substitution.

### GREEN and refactor

Implement the smallest canonical schemas/readers/evaluator/evidence finalizer and ADR documents
inside the exact allow-list. Do not create Terraform/resources/adapters. Keep one unit registry,
one formula registry, one decision/state/BOM model, and one evidence manifest implementation.
Refactor only after each RED class passes for the intended reason.

## Future command behavior

### `make state-matrix-check`

Validates authority ledger, state/key/config rows, writer/reader fencing, backup/restore/RPO/RTO,
retention/deletion/migration, dependency DAG, stopped behavior, teardown modes, and state-to-BOM/
cost/evidence links. It can return `blocked-tbc` before selection, but cannot return pass with an
incomplete required row.

### `make cost-model-check`

Runs strict pricing parser/provenance/freshness/unit/currency/region tests, deterministic golden
scenarios, formula/rounding, residual-cost invariants, CostGuard allow/deny/blocked cases,
sensitivity/overflow, and offline replay. It emits no current price claim unless the accepted
snapshot and caller inputs are complete.

### `make aws-decision-check`

Aggregates authority, option/ADR, traceability, BOM/Terraform/concern reconciliation, schedule,
recovery/security, evidence/redaction/rollback and protected-path checks. Any apply-blocking TBC
returns `blocked-tbc`, never pass. It performs no AWS/Terraform action.

Each target is non-interactive, network-denied by default, input-SHA bound, time/output bounded,
and emits one `fitness-result-v1`-compatible bundle after the exact released schema mapping.

## Required future verification

At minimum after implementation:

```text
make state-matrix-check cost-model-check aws-decision-check
```

Then run the exact Issue #6 and released Issue #11 blast-radius commands and protected hashes named
by the amended allow-list. Do not guess those Issue #11 commands now. Required missing tools are
fail. Optional live source refresh is `not-run-optional`; it cannot replace offline accepted
snapshot tests.

No default command may call AWS, `terraform plan`, `terraform apply`, `terraform destroy`, read
credentials/account state, create/delete resources, or prompt for destructive confirmation.

## Evidence and output contract

Evidence root:

```text
.artifacts/evidence/aws-decisions/<run-id>/
```

The bundle is private during the run, compact, content-hash-indexed, and retains safe failure
evidence. It records exact input/tested-tree/dependency/model/snapshot hashes, command/args/tool
versions, statuses, decision IDs, TBCs, protected result, redaction class, and rollback result.
It contains no account ID, resource ARN/name, credentials, environment values, private paths,
customer/learner data, or raw sensitive plan/state/logs.

## Review and human gates

- Independent validation, readiness audit, implementation, and exact-head review are separate
  sessions. No session validates its own phase.
- Planner/validator/auditor exit 0 is insufficient; each publishes explicit verdict, exact input/
  output SHA, artifact path, GitHub comment, label state, fresh remote read-back, and clean tree.
- Human exact-head pre-merge review is mandatory. Standing approval applies only under its stated
  exact-head/review/test/security/dependency conditions and never authorizes cloud action.
- A later apply approval is distinct from merge approval and binds an exact saved plan and all
  inputs. Any replan/input/head/account/region/role/expiry change invalidates it.

## Rollback and STOP

Rollback may remove/revert only exact Issue #14-owned implementation files and generated private
workspaces after preserving failure evidence. It must not mutate retained evidence, prior pricing
snapshots/ADRs, shared contracts/views, root Make/release manifest, golden semantics, or unrelated
state.

STOP on wrong/dirty base, missing/changed dependency, empty authority required for the step,
protected diff, invented path/resource/rate/SHA/owner, parser/filesystem/security regression,
unrestorable state, stale/unreconciled cost, unresolved Critical/High finding, missing human gate,
or any attempt to expand into AWS/Terraform/cloud action.
