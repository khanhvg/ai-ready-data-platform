# Dependency and Release Gates

## Current Fresh-Live State

Rechecked on 2026-07-22 from the exact validation input after comparing local, tracking, and
fresh-live refs and reading the live GitHub issue records.

| Dependency | Fresh-live fact | Planning use | Implementation consequence |
|---|---|---|---|
| Issue #6 | CLOSED/`shipped`; verified merge `24be3b34c6b0fcdbd07c5800dcab349054e34713` | Binding data/fixture truth | Read-only baseline for both stages |
| Issue #7 | OPEN/`ready to cook`; no merged Vite handoff | Vite + React is the owner-selected direction | An audited implementation input is not a merge/release; Stage A blocked |
| Issue #8 | OPEN/`ready for plan audit`; no released Stage A contract | Confirms validated planning intent only | No consumable completion/evidence/browser contract; Stage A blocked |
| Issue #9 | OPEN/`ready for plan audit`; no released runner | Confirms validated runner planning intent only | No consumable private runner contract; Stage B blocked |

These live records are provenance facts, not consumable release SHAs. A later record may
supersede them.

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

## Gate A — Static Portal Authority

Stage A stays disabled until one fresh readiness phase proves all rows:

| ID | Required exact handoff | Fail-closed proof |
|---|---|---|
| GA-01 | Issue #7 is merged into the authorized integration lineage | Remotely observed merge SHA, reviewed Vite head, ancestry/blob equality, exact package manager/Node/npm requirements, product-source promotion map, package/lock digests, minimal Chromium/axe/no-JS/build/S3 results, rollback notes |
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
