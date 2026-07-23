---
title: "Issue #10 Stage A v3 independent plan validation"
reportDate: "2026-07-23"
inputSha: "a9e5ee26eacaec1b07ce9a25ac4b86da15f0b9a1"
integrationReleaseSha: "5644f01b4c0443a81f3af0bcce80f44c847cd986"
branch: "plan/issue-10-promotion-portal"
verdict: PASS
reviewFindings: "3/3"
stageB: blocked-on-issue9
cloudAction: none
---

# Issue #10 Stage A V3 Independent Plan Validation

## Summary

**Verdict: PASS, not readiness.** The corrected Stage A plan independently resolves all three
failed-PR findings and is implementable with scaffold-first TDD, one released production registry,
and a closed current evidence generation. Three bounded plan-validation findings were fixed without
changing product scope, commands, released inputs, or Stage B authority.

This report does not authorize cook, implementation, a feature worktree, PR #29 changes, evidence
reuse, approval, merge, runner/container activity, cloud/AWS/Terraform action, or a full-product
claim. The next legal gate is a fresh independent plan-readiness audit.

## Frozen Input and Independence

| Check | Result |
|---|---|
| Workspace | Exact requested Issue #10 plan worktree only |
| Branch | `plan/issue-10-promotion-portal` |
| Local HEAD at start | `a9e5ee26eacaec1b07ce9a25ac4b86da15f0b9a1` |
| Configured upstream at start | exact input |
| Fresh live branch at start | exact input |
| Initial tracked/index/untracked state | clean |
| Issue state at start | OPEN with `ready for plan validation` plus the required risk/TDD/S3/frontend/accessibility/vertical-slice labels |
| Herdr session | `validate-issue10-portal-stage-a-v3`; Codex `gpt-5.6-sol`; reasoning `xhigh` |
| Write authority used | Issue #10 plan/validation artifacts only |

The correction commit parent is `2f278eb25aaff9e050314b01d1be155b76793f11`. Its delta to the
input is exactly 16 paths beneath `plans/260721-010-promotion-trust-portal/**`: 15 modifications and
one correction-report create, with zero product/test path. Failed PR #29 remains open at rejected
head `28a71ccc9028c61084a0aaed7fb1b426a62b6ba8`; this validation did not modify its branch or
evidence. No command targeted another worktree for write.

The output commit cannot contain its own SHA without recursion. Git, the Issue #10 validation
comment, and post-push local/upstream/fresh-live equality bind that identity after publication.

## Authority Reviewed

- [Failed PR #29 independent review](https://github.com/khanhvg/ai-ready-data-platform/pull/29#issuecomment-5050218543)
- [Stage A v3 correction handoff](https://github.com/khanhvg/ai-ready-data-platform/issues/10#issuecomment-5050628420)
- Exact integration release `5644f01b4c0443a81f3af0bcce80f44c847cd986`, tree
  `a38594d420fe7df2b30265a8a72bb5fad1698012`
- [Normative Stage A amendment](../stage-a-release-amendment.md)

## Independent Findings and Bounded Fixes

| ID | Severity | Finding | Plan-only correction |
|---|---|---|---|
| V3-IV-01 | Medium | Browser identity was retained but exact admission and RED/GREEN equality were implicit | Required Playwright 1.61.1 + Chromium/Chrome channel, one worker/zero retries, one measured Chrome product/version/executable digest across RED/GREEN, and no fallback/download/public path |
| V3-IV-02 | Medium | Privacy and provenance gates did not explicitly name PII/raw-record/remote-import scans or distinguish author-generated evidence from later independent review | Added explicit scan classes and a role-boundary record; independent/human records remain external and cannot rewrite author evidence |
| V3-IV-03 | Low | A blocked Stage B paragraph retained mutable PID/process-group validation wording, while two old reports were not self-labeled as superseded | Restored child-authenticated self-shutdown and added historical banners; PID/start/process-group data are informational only and runner lifecycle remains #9-owned |

No new path, command, dependency, route, product semantic, fixture, or implementation authority was
added. After the fixes, unresolved validation findings are zero.

## Exact Stage A Closure

The amendment was parsed rather than counted from prose:

| Catalogue | Result |
|---|---|
| Final tracked scope | 33 unique create-only paths; 0 modify; 0 delete |
| Scaffold class | 22 unique paths |
| Complete tests class | 8 unique paths |
| Later-create class | 3 unique paths |
| Class relation | pairwise disjoint; exact 33-path union; no unclassified or third class |
| Integration absence | 33/33 absent from exact integration |
| Commands | 18/18 unique exact shapes |
| Released inputs | 85/85 unique; every Git blob, byte count, and SHA-256 matches integration |

The integration has 921 tracked entries and tree-listing SHA-256
`a6681b3e7ee932fbd29728bc3f649017e57e6980871a3de9def9cb3ac318d9fe`. Root Make retains the
sorted `mk/issue-5/*.mk` seam, and the released owner registry has exactly nine I5-05 reservations
for `mk/issue-5/i5-05.mk`. The package lock remains a tracked Stage A create despite the broad
ignore rule; root Make and `.gitignore` remain denied.

## Scaffold-First TDD Validation

- Commit 1 is exactly the 22 semantics-free callable adapter/provider/catalog/router/render/static-
  route/server/lifecycle/evidence/build/Make seams. It can serve one bounded neutral document and
  contains no target lesson, step, route list, outcome, fixture ID, expected-value branch, forced
  failure, mock, skip, or duplicate truth.
- Commit 2 creates all eight complete tests and changes no scaffold byte. All 18 commands, every
  public Make delegate, and real Chrome reach the scaffold. Setup controls may pass; behavior RED
  must fail at named absent semantics, never missing imports/tools/paths, expected echo,
  unconditional failure, mock/skip/focus, copied predicate, fallback fixture, or retrospective log.
- The 14 unique `PTP-RED-A` IDs map to ten unique named classifications. Valid controls are exact
  released inputs or private run-owned state; mutations change one field or filesystem property.
- RED raw/sanitized logs bind the scaffold and tests commits/trees before first semantics. First
  semantic, ordered later semantic, final commit/tree, and all raw/sanitized GREEN identities are
  separately bound. A changed test requires a new tests-only commit and fresh RED.
- The three later creates are exact; all later semantic edits stay inside the original 22 scaffold
  paths. No Stage A modify/delete class or Stage B path exists.

`SCAFFOLD_FIRST_TDD=pass`.

## Generic Authority Validation

`learning/contracts/learning-contract-set-v1.json` at exact released SHA-256
`92aaf9a573f5d23b5bf5d8d7db1e68150d4b0944f0e6ab6e651b1a3d34408638` is the sole production
descriptor-registry root. Released validators plus the exact promotion manifest/lesson/lab and
shared Vite binding construct one immutable `ReleasedPortalDescriptorRegistry`. Catalog, router,
steps, static documents, React rendering, and routes derive from that object.

Production forbids a local default catalog, step/route truth, alias map, copied schema, generated
binding type, content-ID switch, and test descriptor. Branded `test-only-structure` values enter
only pure functions, are production-rejected, and must be absent from build/runtime/evidence. The
metamorphic portfolio proves generic mechanics without claiming a second or future release. Current
release admission remains exact and fail-closed.

`GENERIC_AUTHORITY=pass`.

## Evidence, Trace, and Roles

One owner-private pending generation becomes current only after a second verifier proves every
payload entry, non-self inventory/index/selector hash, mode/type/link/media/privacy/size/count/
aggregate bound, source/tree/input/dependency/tool binding, and required artifact. Interrupted
publication exposes a prior verified generation or none. Prior/stale/failed generations are
verified outer negative history and cannot satisfy current evidence.

Current records include raw/sanitized RED and GREEN for all 18 commands, resource and all-14-S3
results, lifecycle, both blocked results, interruption/cleanup/rollback, browser/axe/no-JS/
console/CSP/request/storage data, bounded screenshots, and exactly one real Chromium trace.
Playwright tracing is on only for the journey, with sources disabled; the visual project omits
trace capture and no test asserts trace absence. Trace archive paths, count, compressed/
uncompressed size, sources, privacy, and SHA-256 are verified.

The role record labels current evidence as author/cook-produced with independent review and human
approval false. Later independent reviews bind the exact head/tree and generation index in
separate immutable records. Cleanup uses child-authenticated self-shutdown, runs twice, preserves
selected/negative-history evidence, and cannot act on a mutable recorded PID or foreign state.

`CHROMIUM_TRACE=pass`; `EVIDENCE_CLOSURE=pass`.

## Defensive, Product, and Admission Validation

All seven defensive requirements have real machine gates: authenticated child self-shutdown;
schema-valid blocked `fitness-result-v2`; closed build/request inventory; exact runtime/lock/env;
generic registry seam; bounded artifacts; and full RED/S3 controls. PTP-S3-01..14 are unique and
require valid control plus exact mutation/absence proof without skips.

Released product truth is ten ordered narrative steps and four independent aggregate grains with
89 sanitized rows: 7 promotion, 25 fulfillment, 47 returns, and 10 data-quality. The only outcome
is `insufficient-evidence/no-common-grain`; controlled failure remains distinct from environment/
runner unavailability. The product contract is Vietnamese-first, desktop/narrow, keyboard/focus/
overflow/reduced-motion, axe Critical/Serious zero, and no-JavaScript equivalent. Runner,
execution, reset, fresh evidence, progress, completion, course maturity, and full-product claims
remain unavailable or prohibited.

Admission binds Node 22.22.3, npm 10.9.8, lockfile v3, exact released package graph, CPython 3.12.3
and hashed freeze, Playwright 1.61.1, exact Chromium/Chrome-channel same-run identity, one worker,
zero retries, and explicit time/process/file/byte ceilings. The validation host exposes the exact
Node/npm versions, Chrome 150.0.7871.181, 16 GiB RAM, and sufficient free disk for the bounded plan;
no package, browser, build, portal, or product test was run.

Private locator, secret/private-key, PII, raw-record, source-map, remote-import, cloud/runner,
package-lock, root-Make/direct-fragment, rollback, ignored-inclusive, protected-path, and clean-
status gates are explicit. Stage B file, command, dependency, transport, action, evidence, reset,
progress, and completion authorities remain `[]` because Issue #9 is OPEN/`ready to cook` but has
no published feature branch or reviewed/merged/pristine release.

`S3=pass`; `RESOURCE_FEASIBILITY=pass`; `STAGE_B=blocked-on-issue9`.

## Full-Tier Verification and Machine Checks

Seven phases require Full tier. For each phase, 15 claims were checked across the Fact Checker,
Flow Tracer, Scope Auditor, and Contract Verifier roles: 105/105 verified, 0 failed, 0 unverified.
The checks covered paths and release objects, scaffold-to-public/browser flow, state/lifecycle/
evidence lifetime, and every command/registry/phase consumer.

| Check | Result |
|---|---|
| CK 4.5.2 strict JSON validation | valid; 7 phases; 0 issues |
| CK JSON status | 7 pending; 0 complete/in-progress; 0% implementation progress |
| Local Markdown links and anchors | pass |
| Placeholder/current-authority scan | pass |
| Scope/class/absence/overlap | 33 = 22 + 8 + 3; exact and disjoint |
| Released catalogue | 85/85 blob/byte/SHA-256 exact |
| Commands/RED/S3 | 18/18 commands; 14/14 RED IDs; 10 classifications; 14/14 S3 IDs |
| Protected identities and released truth | pass; 7/7 protected; ten steps; four grains/89 rows; canonical decision |
| Trace/evidence/roles/privacy contract | pass |
| Root Make/owner registry/package lock | pass; sorted seam; 9/9 reservations; direct fragment denied |
| Stage B and cross-issue overlap | blocked/empty; no Stage A path overlap found |
| Diff/secret/private-path/whole-plan | plan-only; whitespace clean; zero unresolved contradictions |

## Whole-Plan Consistency Sweep

The sweep reread `plan.md`, all seven phases, the current companion contracts, historical reports,
the correction report, and this validation report. It propagated three validation deltas: exact
browser admission, explicit evidence role/privacy classes, and immutable child-authenticated
lifecycle wording. Counts remain 33/22/8/3/18/85 everywhere current; historical 34-path or empty-
authority statements remain clearly superseded. Unresolved contradictions: zero.

## Disposition

- Plan validation: PASS.
- PR #29 findings: 3/3 resolved at plan level.
- Readiness: not run; next gate is a fresh independent readiness audit.
- Cook scope: none.
- Issue state after successful publication: `ready for plan audit`.
- Stage B: blocked on unreleased Issue #9.
- Cloud action: none.
