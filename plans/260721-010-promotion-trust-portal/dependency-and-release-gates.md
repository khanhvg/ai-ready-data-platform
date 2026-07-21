# Dependency and Release Gates

## Current Fresh-Live State

Rechecked on 2026-07-22 from readiness input
`e2bba33deff76985eb3bdae361d494d162c854f8` after proving local, tracking, and fresh-live Issue
#10 refs equal and reading the live GitHub issue and PR records.

| Dependency | Fresh-live fact | Planning use | Implementation consequence |
|---|---|---|---|
| Issue #6 | CLOSED/`shipped`; verified merge `24be3b34c6b0fcdbd07c5800dcab349054e34713` | Binding data/fixture truth | Read-only baseline for both stages |
| Issue #7 | OPEN/`ready for human review`; PR #22 is OPEN and mergeable at head `b219ba2d3843934c3bce2fbbec2a844b48b2dfa9` onto base `24be3b34c6b0fcdbd07c5800dcab349054e34713`, with no review or merge commit | Vite + React is the owner-selected direction; the PR head is provenance only | No human exact-head approval and no merge/release; Stage A blocked |
| Issue #8 | OPEN/`ready to cook`; serialized six-High real-path repair is active; no released Stage A contract or shared-contract lease release | Confirms owner-directed repair only | No consumable completion/evidence/browser contract; Stage A blocked |
| Issue #9 | OPEN/`ready for plan audit`; readiness audit published at `5cea5ce248b49ff8741af1b1e65f8ac2eb64698f` with `BLOCKED` and `COOK_SCOPE=none` | Blocked audit is durable planning evidence only | No released private runner contract; Stage B blocked |

These live records are provenance facts, not consumable release SHAs. A later record may
supersede them.

## Issue #7 Scope Reconciliation

Gate A consumes only the final simple Vite + React release handoff. Its binding admission evidence
is limited to the frozen-lock build, focused Node contract tests, one Chromium smoke at one desktop
and one narrow viewport, one axe Critical/Serious scan, no-JavaScript/static fallback,
fixture/hash identity, `npm audit` High/Critical disposition, S3 scans, cleanup/rollback, two fresh
exact-head reviews, and human exact-head pre-merge approval.

VoiceOver/System Settings/native Chrome-menu automation, a Firefox/WebKit or multi-browser
scorecard, performance sampling, timers, and Gate-D comparison work are preserved only as history
and are not Gate A blockers. They must not be resumed or promoted into Issue #10 scope.

## Empty Implementation Authority at Validation

Missing dependencies are implementation blockers, not values to fill with provisional heads.
Both stages therefore have empty authority until real releases exist:

| Stage | File allow-list | Command allow-list | Dependency SHA allow-list | Cookable |
|---|---|---|---|---|
| A | `[]` | `[]` | `[]` | `false` |
| B | `[]` | `[]` | `[]` | `false` |

The owner-selected Vite direction does not authorize an unmerged Issue #7 implementation SHA.
A later amendment must pin real dependency SHAs and derived file/command allow-lists, then pass
fresh independent revalidation and dependency-aware readiness before either stage may cook.

## Ownership and Writer-Overlap Decision

- Issue #7 owns its open spike/PR lineage; Issue #10 cannot copy from or treat that branch as a
  release before human approval and merge.
- Issue #8 is the active serialized writer for shared learning contracts. Issue #10 has no shared-
  contract lease and cannot inspect, edit, borrow, or pin its in-flight checkpoint.
- Issue #9 owns runner source and has no released runner authority. Issue #10 may consume only a
  later exact released server-client/API handoff.
- Root Make, shared contracts, dependency worktrees, and portal integration remain single-writer
  surfaces. I5-05 future writes stay inside a released-dependency-derived subset of
  `apps/learning-portal/**` plus `mk/issue-5/i5-05.mk`.

No concurrent writer may touch shared contracts, root Make, or portal integration. An active lease,
overlapping changed path, or missing lease release is a hard STOP.

## Gate A — Static Portal Authority

Stage A stays disabled until one fresh readiness phase proves all rows:

| ID | Required exact handoff | Fail-closed proof |
|---|---|---|
| GA-01 | Issue #7 has human exact-head approval and is merged into the authorized integration lineage | Remotely observed approval and merge SHA, reviewed Vite head, ancestry/blob equality, exact package manager/Node/npm requirements, product-source promotion map, package/lock digests, frozen-lock build, focused Node contracts, one Chromium desktop+narrow smoke, one axe Critical/Serious scan, no-JS/static fallback, fixture/hash identity, npm audit High/Critical, S3 scans, cleanup/rollback, and two exact-head review records |
| GA-02 | Issue #8 Stage A is released into the authorized integration lineage | Remotely observed release SHA plus exact version matrix, schema registry activation, lesson/lab/progress/evidence schemas, promotion-trust lesson manifest/content, generated type/validator consumption path, OpenAPI and operation matrix, completion/reconciliation authority, migration/rollback matrix, artifact digests |
| GA-03 | Fresh I5-05 implementation input contains GA-01 and GA-02 | Local HEAD = tracking ref = fresh live implementation ref; both release SHAs are ancestors; tree clean; no conflicting portal/shared-contract lease |
| GA-04 | Issue #6 truth is unchanged | Four handoff paths match the SHA-256 and Git blob identities in `requirements-and-risk-traceability.md`; protected `release-manifest.json` hash unchanged |
| GA-05 | Scope is still exclusive | Planned diff allow-list is only `apps/learning-portal/**` and `mk/issue-5/i5-05.mk` |

If Issue #8 does not publish a directly consumable validator/type/operation-matrix interface, stop
and return to the Issue #8 owner. I5-05 must not copy, reinterpret, or locally fork the contract.

### Gate A Claim Boundary

Allowed:

- Vite/React shell promoted from the exact Issue #7 handoff.
- Canonical Issue #8 lesson content rendered read-only.
- Browser history, static/no-JavaScript fallback, accessibility, responsive layout.
- Explicit `runner-unavailable`, offline, and environmental failure states.
- Baseline Issue #6 fixture displayed only as labelled retained reference evidence.

Forbidden:

- Import or call an Issue #9 candidate API.
- Create a runner-compatible placeholder, fake runner, or invented command registry.
- Persist or synthesize completion.
- Relabel Issue #6 fixture evidence as a fresh learner run.
- Claim that failure/reset/verify actually executed.

## Gate B — Real Journey Authority

Stage B stays disabled until one fresh readiness phase proves all rows:

| ID | Required exact handoff | Fail-closed proof |
|---|---|---|
| GB-01 | Stage A exact head is accepted | Stage A commands/evidence pass; static non-completion wording retained; exact head reviewed |
| GB-02 | Issue #9 runner is released into the authorized integration lineage | Remotely observed release SHA; API/OpenAPI/client consumption path; private transport/launch-secret rules; exact registry and command IDs; state/idempotency/problem contracts; artifact/evidence API; readiness/status semantics; conformance harness; security/race/crash evidence and digests |
| GB-03 | Fresh I5-05 Stage B input contains the Issue #9 release | Local = tracking = fresh live; runner release ancestor; exact API/registry/evidence digests match; no conflicting runner/shared-contract lease |
| GB-04 | Cross-release compatibility is explicit | Issue #9 release names the exact Issue #8 release it consumes; Issue #8 schema/version registry still recognizes all required versions; no local adapter guess |
| GB-05 | Runner is actually containable on the host | Released readiness probe passes. If containment is unavailable, runner remains disabled and Stage A fallback remains the only supported mode |

If Issue #9 lacks an immutable verified-artifact handle/download operation, exact idempotent reset
semantics, or a conformance harness, Stage B stops. I5-05 cannot add those capabilities to runner
source or infer them from draft plans.

## Vite Runtime Admission at Future Gate A

The later amendment must bind the exact merged #7 Node/npm/package-manager/tool versions,
committed package and lock paths/digests, promotion map, and install/build/test commands. From a
fresh clean checkout, the exact released install contract must use the frozen lock. After the
declared dependency acquisition/cache step, build, focused tests, static/no-JavaScript output, and
the admitted Chromium/axe smoke must not require undeclared network access. Missing cache/tool,
lock drift, lifecycle-script drift, or outbound access is `fail`, never an online fallback.

Stage A contains no runner import or runner-compatible placeholder. Stage B server-only runner and
optional-tool modules must be loaded only after their released capability/readiness gate and must
never enter the browser bundle or make the static path fail at startup. The portal consumes the
released #8 validators/view model instead of copying contract truth. No alternate framework,
runtime, package manager, schema, fixture, or hand-written static contract may be introduced when
the #7/#8 handoff is absent or incompatible.

## Gate Recording

The future gate command records a closed manifest under the I5-05 evidence root with:

- implementation input and tested tree SHA;
- dependency issue, reviewed head, merge/release SHA, and ancestry result;
- every consumed path/package/module, byte length, Git blob ID, and SHA-256;
- Node/npm/lock/tool versions from the released handoff;
- exact schema, registry, OpenAPI, operation matrix, completion, runner API, command registry, and
  evidence versions that actually exist;
- active lease check, changed-path allow-list, protected hashes, and decision;
- `pass` or a stable failure code. Absence or mismatch is `fail`, never skip.

The manifest is evidence of dependency identity, not publisher authenticity and not human
approval.

## Stage/Branch Strategy

A later exact-SHA amendment plus fresh readiness audit may authorize Stage A independently
because it has no runner dependency.
If Stage A is reviewed and merged while Stage B remains blocked, Issue #10 stays OPEN and must
retain the non-completing claim. Stage B starts only from a fresh exact integration head that
contains accepted Stage A and GB-01..GB-05. No rebase, merge, PR, or cook is authorized by this
plan.

## Planning STOP Disposition

No unresolved plan-validity STOP remains after independent validation fixes. Missing #7/#8/#9
releases remain deliberate external implementation STOPs; current file, command, and dependency
SHA allow-lists are empty. Readiness must remain dependency-blocked until a later amendment pins
real handoffs and is revalidated. Any mismatch remains `fail`, never a provisional adapter.
