# Dependency and Release Gates

## Current Fresh-Live State

Checked on 2026-07-21 after fetching `origin` and reading the live GitHub issue records.

| Dependency | Fresh-live fact | Planning use | Implementation consequence |
|---|---|---|---|
| Issue #6 | CLOSED/`shipped`; verified merge `24be3b34c6b0fcdbd07c5800dcab349054e34713` | Binding data/fixture truth | Read-only baseline for both stages |
| Issue #7 | OPEN/`ready for plan audit`; validated simple-Vite planning head `aa93dfac5cd4a5f4d351ad045b634bbd42254902` | Vite + React is the owner-selected direction | Not a merged Vite handoff; Stage A blocked |
| Issue #8 | OPEN/`ready for plan validation`; planner output `93837667326cb7a298c21921ac04e602ea7313d0` | Confirms candidate Stage A intent only | Not a released contract; Stage A blocked |
| Issue #9 | OPEN/`ready for plan audit`; validated-plan output `4cea857fd4a79dca966f4c6b8d4350b4e5d372a2` | Confirms runner plan exists only | Not a released runner; Stage B blocked |

These heads are provenance facts, not consumable release SHAs. A later head may supersede them.

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

A fresh readiness audit may authorize Stage A independently because it has no runner dependency.
If Stage A is reviewed and merged while Stage B remains blocked, Issue #10 stays OPEN and must
retain the non-completing claim. Stage B starts only from a fresh exact integration head that
contains accepted Stage A and GB-01..GB-05. No rebase, merge, PR, or cook is authorized by this
plan.

## Planning STOP Disposition

No unresolved planning STOP exists at publication: missing #7/#8/#9 releases are deliberately
external implementation gates with a complete fail-closed protocol. Any conflict discovered by
fresh independent validation or readiness changes this disposition to blocked before cook.
