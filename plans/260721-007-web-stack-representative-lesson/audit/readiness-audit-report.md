---
title: "Fresh Readiness Audit — Issue #7 Gate 0/Gate A"
issue: 7
phase: fresh-readiness-plan-to-cook-audit
status: ready-with-gates
auditInputSha: "0486642528b9a6ba8e96cee18d6eda76c3b5deb9"
plannerSha: "0890c4abab46f81d110be6cbd6de3560e631a735"
discoverySha: "a39251d45a56124322b9143ad16b926b2656073b"
integrationSha: "f9a87d0ebdb72c014a6f8c6eaae865dad4d2188c"
masterReadinessSha: "e440c5855732d5d8f5d634e3cc1359c010cc5ed3"
auditOutputSha: "externally-attested-in-issue-7-publication-comment"
authorizedScope: gate-0-and-gate-a-only
auditedAt: "2026-07-21"
---

# Fresh Readiness Audit — Issue #7 Gate 0/Gate A

## Verdict

`READY_WITH_GATES` for only the bounded first cook defined in
[cook-scope-gate-a.md](./cook-scope-gate-a.md): Gate 0 authority/freeze plus Gate A's
dependency-free common logical tests and retained framework-neutral static `learn-preview`.

This is not full issue readiness. It does not authorize Astro, Next.js, Vite, package or browser
installation, candidate build/test/score, Barrier B, Gate C, Gate D, ADR-005, pre-merge review, PR,
or merge. Issue #7 must remain open after Gate A. A later readiness owner must explicitly open each
deferred boundary.

The audit did not implement code, install/build packages, run browser scoring, change product,
configuration, data, or discovery history, access cloud/runner authority, create a PR, or merge.

## Fresh Phase and Immutable Provenance

The audit began read-only and stopped its edit decision on these checks:

| Check | Observed evidence | Result |
|---|---|---|
| Repository/worktree | Requested issue-7 worktree and repository identity | Pass |
| Branch | `plan/issue-7-web-stack-representative-lesson` | Pass |
| Local input | `HEAD` exactly `0486642528b9a6ba8e96cee18d6eda76c3b5deb9` | Pass |
| Tracking/live remote | Fresh fetch; local, tracking, and live branch all exactly the audit input | Pass |
| Clean input | No staged, unstaged, or untracked paths before audit edits | Pass |
| Planner relation | Audit input's first parent is `0890c4abab46f81d110be6cbd6de3560e631a735` | Pass |
| Required ancestry | Planner, discovery, integration, and master readiness SHAs are ancestors | Pass |
| Discovery immutability | Discovery tree is `ed45ef287be3c0830466ae4a6b60a6bf22b1eb70` at discovery and audit input; no discovery diff | Pass |
| Live issue phase | Issue #7 open with `ready for plan audit` and its risk/security/TDD/frontend/accessibility/decision labels | Pass |
| Stale input | No newer live issue-7 plan-branch commit or contradictory issue comment | Pass |

The containing output commit cannot be written inside itself without a recursive hash claim. The
exact audit output SHA is therefore attested in the issue #7 publication comment and is the only
valid future `IMPLEMENTATION_INPUT_SHA`.

## Current Repository and Blocker Facts

- Issue #6 remains open at `ready for plan validation`; the four required tracked contract/fixture
  files are absent from this tested tree. Barrier B is closed.
- No current `spikes/web/**` product source or `mk/issue-5/i5-02.mk` exists. Gate 0/A is a real
  tests-first implementation, not repair of a hidden implementation.
- No local or remote `feature/issue-5-02-web-spike` branch existed at audit time. The cook must
  create and publish it from the audit output before its first implementation write.
- Node `v22.22.3`, npm `10.9.8`, Python `3.12.3`, and GNU Make `3.81` match the planned host
  assumptions. npm is frozen for later candidates only; the current cook may not invoke it.
- Port `4173` was occupied by an unrelated loopback process at audit time. The audit did not signal
  it. Port `4174` was free at that instant and is the documented verification port, but the cook
  must recheck and stop if it is occupied; it may not scan for or auto-select another port.
- `.artifacts/**` is not ignored. It is generated-only state, must never be staged, and must be
  removed after sanitized Gate A retention. The root `.gitignore` stays protected.

## Readiness Criteria Disposition

| # | Audit criterion | Disposition |
|---:|---|---|
| 1 | Provenance, branch/remote/ancestry, stale input | Pass at immutable input; repeated before cook writes and publication |
| 2 | Exact paths, one product worktree, protected root/shared files | Pass with staged path narrowing and one exact future branch/worktree |
| 3 | Tests-before IDs, order, tests-after, evidence, rollback | Pass after bounded plan corrections; exact IDs are in the cook scope |
| 4 | Issue-local Make + direct fallback lifecycle safety | Pass as an implementation contract; verification is mandatory before Gate A attestation |
| 5 | Ten-act learner journey/state/failures/hints/evidence/reflection | Pass as a testable Gate A contract |
| 6 | Four grain-honest cards/calculation metadata/no causal join | Pass as a testable invariant; expected conclusion remains `insufficient evidence` |
| 7 | Static/no-JS/semantic/reflow/motion/keyboard evidence honesty | Pass with static/logical facets separated from required-pending browser/manual facets |
| 8 | S3 static fixture/no privilege/CSP/network/path/security scans | Pass as a fail-closed Gate A contract |
| 9 | Staged isolation and blocked status schema | Pass after `stage-status.json` and exact target allow-list were added to the plan |
| 10 | Scoped rollback/no orphan/no false completion | Pass after operational rollback was narrowed to owned process/generated state |
| 11 | Validation fixes and actionable links/IDs/commands/dependencies | Pass after staged authorization, direct lifecycle, lock timing, and evidence paths were reconciled |
| 12 | Human gate, #6 merge/digests, browser/manual, 14h/no-winner | Pass as visible non-waivable deferred gates; none is satisfied here |

## Bounded Plan Corrections Applied

Only files inside `plans/260721-007-web-stack-representative-lesson/**` changed. Discovery history
did not change.

1. Candidate phases 3–5 now require a later readiness audit instead of opening automatically at
   Gate A. Their paths and Make targets must be absent from the first cook.
2. Candidate manifests/locks are absent in Gate 0/A. The exact-force-add/clean-install rule is a
   later candidate policy, not a current dependency.
3. `stage-status.json` makes Gate 0/A authority and candidates/Barrier B/Gate C/Gate D/full-issue
   blockers machine-visible.
4. The static host now has an exact route/root/CSP/network boundary and the lifecycle contract has
   a per-port locator with PID-reuse and foreign-process protection.
5. Direct no-build Node lifecycle commands and the limited foreground Python fallback are exact.
6. Gate A accessibility results are limited to source/logical facets. Browser navigation, actual
   keyboard, named screen reader, 200% rendering, reduced-motion rendering, and no-JS manual review
   remain required-pending evidence work.
7. Generated `.artifacts` state is explicitly untracked/transient; only sanitized Gate A evidence
   may be retained under the issue-owned source tree.
8. Rollback preserves tracked source/plans/evidence/protected paths and removes only verified owned
   processes and cook-created transient state.

## Gate Decision

| Stage | Readiness after this audit | Meaning |
|---|---|---|
| Gate 0 | Authorized | Exact input/branch/worktree/remote/path/toolchain/registry freeze and dependency-free tests |
| Gate A | Authorized after Gate 0 | Synthetic, unscored, non-completing static preview and common logical tests |
| Candidate foundations | Deferred, not authorized | No candidate path, package, target, timer, or evidence may exist |
| Barrier B | Blocked | Needs reviewed/merged issue #6 SHA, four exact tracked files/digests, schema and zero issue-7 diff |
| Gate C | Blocked | Needs Barrier B plus fresh current browser and named manual accessibility evidence |
| Gate D | Blocked | Needs complete comparable Gate C evidence; no score/ADR otherwise |
| Full issue/review/PR/merge | Blocked | Needs the full 14-hour protocol, valid winner/no-winner path, retention, and human pre-merge gate |

Gate A output always carries `SYNTHETIC LEARN-PREVIEW — UNSCORED — CANNOT COMPLETE` at entry,
state rail, verify/evidence, and export. It has no completion state, score, winner, runner, mutation,
cloud route, credential, privileged API, release status, or architecture-decision authority.

## Evidence and Publication Gates

The cook must retain a `fitness-result-v1` Gate 0/A subset with exact input/tested-tree/tool and
fixture/test/contract digests, command/result index, failing-before IDs, passing-after IDs,
static-versus-required-pending accessibility facets, protected hashes, changed paths, security/
credential/non-copy scans, process lifecycle results, artifact hashes, redaction result, and
rollback result. Gate A records have null score/disposition and false `decisionGrade`,
`issueComplete`, and `opensBarrierB`.

Before any Gate A publication, the cook must stop its owned preview, sanitize/hash-index retained
evidence, remove transient `.artifacts` created by the cook, prove no candidate/package/ADR path,
prove protected hashes and discovery tree, run `git diff --check`, prove clean local/tracking/live
equality after push, and leave no orphan process. No PR or merge follows.

## Audit Verification Results

The audit ran these planning gates before publication:

- `ck plan status plans/260721-007-web-stack-representative-lesson`: pass; all eight implementation
  phases remain pending (`0/8`), which is correct because this phase performed no cook.
- Structure/frontmatter/DAG/link/anchor/ownership/blocked-stage sweep: pass across 24 Markdown
  files and eight ordered phases.
- Traceability/command sweep: pass for all 68 discovery Critical/High IDs, 19 Gate A `WEB-*` IDs,
  ten Gate 0 failing IDs, twelve exact Make targets, and four direct lifecycle verbs.
- `git diff --check`: pass.
- Changed-path sweep: pass; every audit edit is inside the exact issue-7 plan directory and
  `discovery/**` has no diff.
- Protected hash/tree sweep: pass for root Makefile, `.gitignore`, `release-manifest.json`, and the
  immutable discovery tree.
- Ignore probe: both new audit files are ignored by the repository's `plans/**/*` rule and require
  exact-directory force-add; `.artifacts/**` is visible/unignored as documented.
- Changed-content credential/private-path scan: pass. No new secret, private key, credential value,
  or absolute personal path is present.

Planned implementation commands were audited for syntax, ownership, prerequisites, outputs, and
failure semantics; they were not executed because the implementation files intentionally do not
exist in this phase.

## Non-Waivable Deferred Gates

- Human pre-merge approval remains mandatory and cannot be inferred from automation.
- Issue #6 must be reviewed and merged into the tested ancestry; exact SHA-256 digests for both
  contracts and both tracked learning fixtures must validate.
- Fresh browser evidence and actual manual keyboard, named screen-reader, 200% reflow,
  reduced-motion, and no-JS review remain required.
- The equal `3h common + 3h Astro + 3h Next + 3h Vite + 2h decision = 14h` protocol and its
  90-minute/3-hour kills remain binding if candidates are later authorized.
- Must-pass precedes scoring. Incomplete, stale, mixed, killed, non-comparable, or unsafe evidence
  yields no winner; the Astro within-five-point default cannot waive a missing gate.

## Audit Conclusion

The plan is cookable only at its smallest safe boundary. Gate 0/A can produce a useful retained
learner preview without creating false decision evidence or reaching dependency, runner, cloud, or
shared-product authority. All later work remains visibly and mechanically closed.

`AUDIT_VERDICT=READY_WITH_GATES`

`ISSUE_STATE=ready to cook`

`COOK_SCOPE=gate-0-and-gate-a`
