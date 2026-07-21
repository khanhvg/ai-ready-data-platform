---
title: "Issue #13 TDD, Fitness, Evidence, Migration, and Recovery"
status: planned-validated
created: "2026-07-22"
---

# Issue #13 TDD, Fitness, Evidence, Migration, and Recovery

## TDD Order Is Binding

1. Amend exact dependencies/authorities and rerun independent validation/readiness.
2. Characterize current Docker-free commands, Compose render/closure and protected hashes.
3. Write behavior-specific RED tests that exercise real parsers/resolvers/ownership logic.
4. Implement only enough Stage A behavior to make static admission/security/budget tests GREEN.
5. Freeze exact Stage A head.
6. Only then run actual Stage B cold/warm checks and recovery against admitted engine/images/tools.
7. Run dependency/golden blast radius, N-1 readers, rollback and protected-path gates.

No RED test may unconditionally fail, assert a fixture's expected code back to itself, replace the
subject with a mock, or invoke Compose and then claim pre-start denial. A negative test supplies an
invalid real input to the production parser/resolver and asserts typed result, absent Compose
invocation, and absent side effect. Engine-unavailable uses an actually absent/unreachable command
endpoint in a private test environment, not fabricated performance samples.

## Characterization IDs

| ID | Current behavior to freeze before change | Proof |
|---|---|---|
| `LP-CHAR-CORE-001` | `health/dbt/bi` recipe closure contains no Docker/cloud/privilege | Parsed/dry-run argv plus focused existing tests |
| `LP-CHAR-COMPOSE-002` | Three profiles, nine services, exact health/dependency/port/volume/memory render | Canonical Compose inventory and hash |
| `LP-CHAR-GUARDS-003` | Current Make guard/direct start/down/catalog-ingest behavior | Static recipe characterization; no container start |
| `LP-CHAR-PROTECTED-004` | Protected file presence/absence and hashes at amended input | Sorted manifest + SHA-256 |
| `LP-CHAR-SCALE-005` | Dataset `small`/`medium`/`large`/`demo-large` remains separate from service profiles | Generator/schema contract tests |

Characterization assertions protect behavior; they do not bless insecure wildcard ports or missing
limits. Tests for current gaps are RED new-behavior tests.

## Required RED IDs

| ID | Stimulus | Required RED observation before implementation | GREEN behavior |
|---|---|---|---|
| `LP-ADM-INVALID-001` | malformed/composite/option/path/confusable profile request | Current path lacks typed preflight | Reject before Compose argv/process |
| `LP-ADM-MISSING-002` | missing/empty selection or required authority | Current direct path can bypass semantic admission | Typed missing-input denial |
| `LP-ADM-DUPLICATE-003` | same group/service repeated | No canonical duplicate denial | Reject; no dedupe-as-success |
| `LP-ADM-UNKNOWN-004` | unknown group/service/profile | No exact owner allowlist | Reject with known choices, no start |
| `LP-ADM-ALL-THREE-005` | exact three current heavy groups | Direct Compose can select all | Deterministic deny independent of numeric totals |
| `LP-BUDGET-LIMIT-OMISSION-006` | remove/zero/invalid unit/overflow any memory/CPU/PID/disk/log/deadline/owner field | Current config has omissions | Schema/static denial naming service+field |
| `LP-ADM-DEPENDENCY-EXPANSION-007` | hidden/unknown transitive `depends_on` service/profile/port/volume/network | Compose may expand without allowlist comparison | Reject exact closure mismatch |
| `LP-SEC-PORT-COLLISION-008` | duplicate, wildcard, occupied or foreign-owned host port | Current ports wildcard/fixed | Reject before start; foreign listener untouched |
| `LP-SEC-VOLUME-COLLISION-009` | duplicate/external/foreign/mismatched volume/project | Current ownership not immutable | Reject; never adopt/relabel/delete |
| `LP-SEC-LOG-UNBOUNDED-010` | missing/invalid log driver/size/file count | Current logging is unbounded | Static denial |
| `LP-SEC-PID-UNBOUNDED-011` | missing/zero/excess PID cap | Current caps absent | Static denial |
| `LP-READY-TIMEOUT-MISSING-012` | health/one-shot/build/pull/workload/teardown without hard deadline | Current one-shots lack explicit deadline | Static denial |
| `LP-ADM-GUARDED-PAIR-013` | exact pair vs reordered/extra/stale-token/changed-config/workload | Current pair is host recipe only | Admit exact `lake+governance`; Airflow absent; reject variants |
| `LP-EVIDENCE-SCHEMA-014` | missing authority/input/image/config/host/command/raw/summary/recovery/index field/locator | Current I5-08 authority absent | Released-schema-valid complete bundle only |
| `LP-ENGINE-UNAVAILABLE-015` | engine CLI/daemon/allocation unavailable | No typed heavy-profile result | Static can pass; heavy result blocked/non-zero; no samples |
| `LP-RECOVERY-FOREIGN-SENTINEL-016` | foreign project/container/network/volume/port beside failed run | Current broad teardown not manifest-bound | Run state removed; sentinel byte/labels/hash unchanged |
| `LP-SEC-INTERPOLATION-017` | malicious env/Compose interpolation and shell metacharacters | Current env is broad Compose input | Reject/clear; argv arrays only |
| `LP-SUPPLY-IMAGE-018` | tag-only, wrong platform/digest, missing SBOM/signature/provenance, pull drift | Current tags lack authority | Block before start/pull; exact policy result |
| `LP-SEC-HOST-019` | Docker socket, privileged/host namespace/device/capability/RW base/public bind | Current Airflow root is RW and ports public | Static S3 denial; no web/portal engine exposure |
| `LP-SEC-PATH-020` | traversal, symlink, hardlink, FIFO/device/socket, wrong owner/mode | No I5-08 private path boundary | Reject with no read/write/delete outside root |
| `LP-EVIDENCE-INTEGRITY-021` | tamper, truncation, duplicate locator/hash/run ID, stale tree/config/image, replay | No I5-08 bundle exists | Verifier rejects before completion/read |
| `LP-BUDGET-OVER-AGGREGATE-022` | any single/pair closure exceeds its memory/CPU ceiling or host/engine reserve | Current Compose has memory-only limits and no canonical aggregate gate | Typed over-budget denial before Compose argv/process |

### RED Evidence

Record for each ID:

- exact test node/command, tested tree and dependency/contract hashes;
- actual assertion and observed behavior;
- expected new behavior stated independently from fixture content;
- proof no supported Compose startup or foreign mutation occurred;
- result log hash and redaction result.

Do not publish unconditional-fail code or a test that passes only because it compares
`expectedFailureCode` from input to the same returned literal.

## Stage A GREEN Contract

Static GREEN requires:

- exact schema validation and canonical request representation;
- actual Compose service/dependency closure equal to the exact allowlist;
- per-service and aggregate memory/CPU/PID/disk/log/deadline/ownership rules;
- exact per-service start/ready/exit and stop ceilings plus bounded single/pair parent teardown;
- loopback/host-mount/socket/privilege/capability/network/image-policy checks;
- all-three and unauthorized combinations denied before the production Compose runner is called;
- exact guarded-pair plan contains no orchestration service;
- Docker-free core command closure unchanged;
- no dependency, protected hash, shared contract or semantics drift.

Stage A tests may use a recording production runner boundary to prove it was not invoked, but they
must parse/resolve production config and cannot claim live engine acceptance. No image pull/build or
container start belongs in Stage A.

## Fitness Command Contracts

The existing names are reserved but not runnable at the planning input. `mk/issue-5/i5-08.mk`
eventually publishes thin targets only after released command/completion authority is available.

| Command | Primary responsibility | Docker daemon requirement | Final behavior |
|---|---|---|---|
| `make compose-check` | Schema, request grammar, actual Compose/service closure, combination matrix, configured bounds | No | Pass/fail static |
| `make compose-security-check` | S3 static policy, interpolation, image authority, mounts/socket/privilege/caps/networks/ports/paths | No | Pass/fail static |
| `make profile-budget-check` | Static budget first; then require exact Stage B evidence for admitted heavy acceptance | Yes for final live portion | Pass only with all required evidence; typed blocked/non-zero if unavailable |
| `make recovery-test` | Ownership, interruption, residue, retained evidence and actual foreign sentinel | Yes for final integration | Pass only with actual admitted engine sentinel run; typed blocked otherwise |

Stage A-only development may call focused test modules or an explicitly labelled static submode,
but that output cannot be presented as the final default `profile-budget-check`/`recovery-test`
pass. Final verification invokes the four commands in one Make call as requested.

## Evidence Root and Locator Contract

Canonical root:

```text
.artifacts/evidence/local-profiles/<run-id>/
```

Conceptual locator layout (exact filenames/fields must be mapped to the released authority in the
dependency amendment):

```text
authorities.json
inputs/config-hashes.json
inputs/compose-render.json
host/normalization.json
security/image-policy.json
static/admission.json
static/security.json
static/budgets.json
commands/<command-id>/result.json
commands/<command-id>/stdout.txt
commands/<command-id>/stderr.txt
measurements/<scenario>/<cold|warm-1|warm-2>/samples.jsonl
measurements/<scenario>/<cold|warm-1|warm-2>/summary.json
recovery/ownership.json
recovery/teardown.json
recovery/residue.json
rollback/result.json
index.json
<released-completion-locator-written-last>
```

Required semantic content:

- exact input/tested-tree/Stage A/Issue #10 merge/Issue #12 release SHAs;
- lab allowlist and completion/evidence/command authority hashes;
- image index/platform digests, SBOM/signature/provenance results, config/render/tool hashes;
- normalized host/engine allocation and measurement method;
- argv arrays, statuses, typed failures/blocks, timing and bounded logs;
- raw samples and derived summary linked by hashes;
- teardown targets/actions/residue, retained state and foreign sentinel before/after hashes;
- rollback point/action/result and protected-hash result;
- strict repo-relative locators, byte lengths, SHA-256 index and released atomic completion.

No secret values, unredacted home paths, private data, full env dump, synthetic measurement or
unbounded logs enter the bundle.

## Evidence State Machine

```text
allocated(private) -> inputs-frozen -> static-green
  -> live-running -> live-complete -> teardown-complete
  -> rollback/protected-check-complete -> indexed -> completed
```

Any failure before `completed` leaves an incomplete run that cannot be consumed as acceptance.
Recovery may finish teardown and publish a failure/block result only under the released authority;
it cannot turn the run into pass. Completion is written only after residue and retained-evidence
checks.

## Additive Migration and N-1 Readers

- Never mutate current owner-fixed `fitness-result-v1`, schema registry, command registry, golden
  evidence, or release manifest inside I5-08 authority.
- Consume the released completion/evidence contract exactly. If profile measurement needs an
  additive family/version, obtain the serialized shared-contract lease and exact owner amendment
  before implementation; this plan does not grant it.
- New version adds fields; it does not reinterpret old result values or locators.
- Current reader consumes current and N-1. N-1 reader remains available for old evidence during
  migration. Unknown future versions fail closed.
- Test current->current, N-1->current additive read, current with old reader (expected bounded
  refusal where appropriate), duplicate/missing field, tamper, replay and rollback-reader paths.
- No lossy down-conversion. Rollback selects the previous reader/config and preserves newer raw
  evidence for audit without claiming it is old-schema pass evidence.

## Recovery and Teardown Algorithm

1. Open the private immutable ownership manifest with no-follow/regular-file/owner/mode checks.
2. Resolve exact engine objects by both manifest ID and run/project owner labels.
3. Enumerate planned targets and foreign/retained exclusions; hash/record before state.
4. Stop bounded child/workload processes, then only run-owned containers.
5. Remove only run-owned network, explicitly ephemeral volumes, temp bytes, port reservations and
   bounded logs. Never use a broad project/glob/default derived from ambient env.
6. Preserve retained volumes and evidence root.
7. Re-enumerate; fail if run-owned residue remains or any foreign sentinel changed.
8. Record teardown/rollback result, then index and complete evidence.

Interrupted cleanup is idempotent. A missing or mismatched ownership manifest blocks deletion and
returns exact manual locators. Foreign collision during recovery also blocks rather than widening
scope.

## Rollback Boundary

Rollback point is the exact dependency-amended Stage A input SHA/config hash. Rollback may:

- remove I5-08 Compose additions/hardening, profile config, scripts/tests/Make fragment and bounded
  docs from the issue branch through normal version control;
- remove only I5-08 run-owned ephemeral engine/temp state;
- select the previous additive reader/config under its exact compatibility rules.

Rollback must not delete retained evidence, foreign resources, dependency releases, portal/runner
images, admitted labs, golden data, named user volumes, or protected files. No migration or
destructive data conversion is authorized.

## Blast Radius Gate

At the exact final head:

1. Four I5-08 verification commands.
2. Docker-free `health/dbt/bi` and exact released Issue #10 journey.
3. Exact released Issue #12 lab/data/golden commands.
4. Protected golden/shared-contract/migration/command/evidence checks named by amendment.
5. Static diff/hash allowlist and secret/private-path/placeholder scan.
6. Actual foreign sentinel recovery proof and final clean worktree.
7. Human approval naming the exact final head and completed evidence index hash; any later commit
   invalidates approval and requires re-review.

Missing dependency command/tool/image/engine produces fail or typed block under released authority;
it is never changed to `not-run-optional` merely to complete Issue #13.
