---
phase: 1
title: "Gate 0 Authority and Freeze"
status: pending
priority: P1
dependencies: []
effort: "preflight; active spike timer not started"
barrier: authorized-by-fresh-readiness-audit-for-gate-0-only
---

# Phase 1: Gate 0 Authority and Freeze

## Context Links

- [Plan authority](./plan.md#authority-and-current-blockers)
- [Implementation handoff](./implementation-handoff.md)
- [Security S3 disposition](./security-s3-disposition.md)
- [Discovery planner handoff](./discovery/planner-handoff.md)

## Overview

Create the fail-closed issue-local authority/toolchain/mode registry before any preview or
candidate work. Gate 0 performs no candidate install/build and does not start the 14-hour active
spike timer. A mismatch is a hard STOP, not a prompt to rebase, patch shared files, or continue on
mixed provenance.

## Requirements

- Accept only a full 40-hex `IMPLEMENTATION_INPUT_SHA` named by the later readiness handoff. Before
  the first implementation write, require local HEAD, its tracking ref, and a freshly fetched live
  remote ref to equal it. Require planner output `0890c4abab46f81d110be6cbd6de3560e631a735`,
  discovery `a39251d45a56124322b9143ad16b926b2656073b`, integration
  `f9a87d0ebdb72c014a6f8c6eaae865dad4d2188c`, and readiness report
  `e440c5855732d5d8f5d634e3cc1359c010cc5ed3` as ancestors. After issue-owned writes, retain the
  recorded implementation input as the changed-path base and require it to remain an ancestor of
  the tested tree with no tracking/live-remote drift.
- Freeze Node `v22.22.3`, npm `10.9.8`, lockfile version 3, and exact top-level candidate pins:
  Astro `7.1.3`, Next `16.2.10`, Vite `8.1.5`, React/React DOM `19.2.7`, and Playwright
  `1.61.1`. Exact transitive trees come only from the three independent candidate lockfiles; the
  common harness is dependency-free and has no package manifest or lock.
- For the currently authorized Gate 0/Gate A cook, candidate directories, manifests, lockfiles,
  installs, builds, tests, and targets must be absent. Gate 0 freezes their future policy only; the
  tracked-lock proof is activated solely by a later readiness audit that authorizes candidates.
- Reject semver ranges for frozen top-level dependencies. A version/mode change invalidates that
  candidate's evidence and does not extend its cap.
- Freeze candidate modes:
  - Astro: static output, trusted build-time content, smallest React state island, common static
    measurement host; typed future BFF seam only.
  - Next: self-hosted standalone App Router, prerenderable semantic lesson page, narrow Client
    Component, read-only Route Handler replay; no Server Action shortcut.
  - React/Vite: static MPA/prerendered semantic HTML with progressive React enhancement and typed
    adapter; common static measurement host; never `vite preview` for evidence.
- Freeze the common test-ID manifest from `acceptance-and-test-matrix.md`; candidates may map
  adapters/selectors but may not rename, weaken, or fork assertions.
- Before any candidate action, create a complete seven-category `score-anchors.json`. Every
  category must define integer anchors 0 through 5 as pre-observation, machine-checkable numeric
  thresholds and/or a fixed reviewer predicate checklist; weights are exactly `20/20/20/15/10/10/5`.
  Reject missing levels, free-form interpolation, post-candidate edits, or a digest mismatch.
- Because `.gitignore` ignores `package-lock.json`, a later candidate cook must require exact-path
  force-add and tracked-state proof for `spikes/web/candidates/{astro,next,vite}/package-lock.json`;
  broad force-add is forbidden. In Gate 0/Gate A, the same paths must be absent.
- Treat `security:S3` as applicable to browser/content/dependency/evidence boundaries even though
  issue #7 implements no privilege.

## Architecture

A dependency-free Node checker reads small JSON registries and Git/file metadata, then every
issue-local Make target delegates to it before work. Registries are data, not a generalized build
system. No network, package install, candidate renderer, or shared contract is involved.

## Protected Baseline

| Path/state at discovery SHA | Required baseline |
|---|---|
| `Makefile` | SHA-256 `6b75a7a1f8e516e8967d317edb9de35378c02eddd645d2731dcf5cfc9bf52f54` |
| `.gitignore` | SHA-256 `aa93e47707e95286126f47b3d70fe7fc6c047b49c861184533e38b3c5a971316` |
| `release-manifest.json` | SHA-256 `f9037b5d946d14f7b1b9c020939f1a44961011f2ad933db9f2b69054abbf9539` |
| `docs/code-standards.md` | `ABSENT`; issue #7 must not create it |
| Issue #7 discovery tree | Git tree `ed45ef287be3c0830466ae4a6b60a6bf22b1eb70`; every discovery file immutable |
| Four issue #6 handoff files | `ABSENT`; presence alone never opens Barrier B without a merged SHA/digest record |
| `apps/learning-portal`, `apps/lab-runner` | `ABSENT`; issue #7 must not create them |

## File Inventory

| Action | Planned path | Purpose | Test impact |
|---|---|---|---|
| Create | `spikes/web/harness/authority.json` | Immutable SHAs, protected hashes, allow/deny paths | Negative drift/path tests |
| Create | `spikes/web/harness/toolchain.json` | Exact Node/npm/top-level pins and lock format | Exact equality test |
| Create | `spikes/web/harness/candidate-modes.json` | One declared runtime/build mode per candidate | Mode drift invalidation |
| Create | `spikes/web/harness/test-ids.json` | Canonical shared WEB IDs and semantics | No candidate fork |
| Create | `spikes/web/harness/score-anchors.json` | Complete pre-observation 0-5 predicates and fixed weights | No post-hoc scoring |
| Create | `spikes/web/harness/stage-status.json` | Machine-visible authorization/blocker schema | Deferred targets cannot open |
| Create | `spikes/web/harness/scripts/authority-check.mjs` | Direct fail-closed preflight | All later targets depend on it |
| Create | `spikes/web/harness/tests/authority.test.mjs` | Wrong SHA/hash/path/toolchain/mode fixtures | Tests before behavior |
| Create | `mk/issue-5/i5-02.mk` | Issue-local targets only | Root Make remains unchanged |

No existing product/config/data file is modified or deleted.

## Related Code Files

- Create only the Gate 0 paths in the inventory above.
- Read repository/Git metadata and protected files without modifying them.
- Delete nothing.

## Dependency Map

```text
immutable planner/discovery/integration/readiness + later implementation input + issue #7 body
  -> authority/toolchain/mode/test-ID/score-anchor freeze
  -> Gate A and all candidate targets
```

Issue #6 is not needed to close Gate 0; it is checked only as absent/unmerged and remains Barrier B.

## Interface Checklist

- [ ] `authority.json` distinguishes allowed, read-only dependency, protected, and absent paths.
- [ ] Toolchain check compares exact values, not major ranges.
- [ ] Candidate mode check hashes the declaration into every later evidence record.
- [ ] Test-ID manifest contains all shared `WEB-*` IDs exactly once.
- [ ] Score anchors contain all seven categories and levels 0..5, are frozen before candidate work,
      and are digest-bound into later evidence.
- [ ] Changed-path check accepts only the issue allow-list and rejects discovery edits.
- [ ] Stage status says Gate 0 authorized, Gate A authorized only after Gate 0, candidates deferred,
      Barrier B/C/D blocked, and full issue incomplete.
- [ ] Candidate directories/locks are absent in this cook; later candidate authorization must
      explicitly activate exact tracked-lock proof and must never broad-force-add.
- [ ] Root Make alias is documented as future integration-owner work, not acceptance.

## Test Scenario Matrix

| Priority | Scenario | Expected assertion |
|---|---|---|
| Critical | Initial local/tracking/live-remote input mismatch or later input ancestry/remote drift | Non-zero before work continues; evidence says `fail` |
| Critical | Protected hash or absence marker changes | Non-zero and exact path reported |
| Critical | Shared/portal/runner/root path appears in changed set | Non-zero; no automatic cleanup or reset |
| High | Node/npm or candidate mode differs | Non-zero; existing evidence invalidated |
| High | WEB ID missing/duplicated | Non-zero; candidate timers cannot start |
| High | Score anchor category/level/predicate missing or changed after freeze | Non-zero; candidate timers cannot start or evidence is invalidated |
| High | Candidate path/target/manifest/lock appears during this cook | Non-zero; deferred work cannot begin |
| High | Stage status is missing or makes a deferred/blocked stage runnable | Non-zero before work continues |
| High | Issue #6 files absent | Gate 0 passes with Barrier B still `closed`; no score path opens |

## Implementation Steps

1. Author failure fixtures/tests and capture `G0-AUTH-001`, `G0-REMOTE-001`,
   `G0-ANCESTRY-001`, `G0-PROTECTED-001`, `G0-PATH-001`, `G0-TOOLCHAIN-001`,
   `G0-REGISTRY-001`, `G0-ANCHOR-001`, `G0-STAGE-001`, and `G0-DEFERRED-001`.
2. Create immutable authority/toolchain/mode/test-ID/score-anchor registries.
3. Implement the direct checker and thin issue-local targets.
4. Run clean/negative cases and retain Gate 0 evidence.

## Tests Before

1. Write `authority.test.mjs` fixtures for wrong initial local/tracking/live-remote input, missing
   ancestry, later remote drift, protected hash drift,
   changed forbidden path, edited discovery file, wrong Node/npm, semver range, mode drift, and
   missing/duplicate WEB ID, incomplete/late anchor edits, illegal candidate paths/targets/locks,
   and a stage registry that makes a deferred/blocked stage runnable.
2. Run the direct test command and record the intended failures before creating the checker or
   Make targets.

## Refactor

Implement only the small data registry/checker and issue-local Make fragment. Do not add a root
include, dependency, package manifest, candidate source, ADR score, or fixture workaround.
The Make fragment exposes only the twelve Gate 0/Gate A targets named in the readiness scope and
uses an explicit unknown-target failure; no wildcard, pattern, recursive root-Make, or candidate
target is allowed.

## Tests After

- Re-run every negative fixture and the clean real worktree case.
- Capture exact command, tested tree, tool versions, protected hashes, and changed paths below
  `.artifacts/evidence/web-spike/<run-id>/gate-0/authority.json`.
- Confirm the output identifies Barrier B as closed rather than silently treating absent fixtures
  as optional.

## Regression Gate

Planned future commands (they do not exist in this planning commit):

```bash
node --test spikes/web/harness/tests/authority.test.mjs
node spikes/web/harness/scripts/authority-check.mjs --implementation-input <full-40-hex-authorized-sha>
make -f mk/issue-5/i5-02.mk i5-02-authority-check IMPLEMENTATION_INPUT_SHA=<full-40-hex-authorized-sha>
make -f mk/issue-5/i5-02.mk i5-02-protected-hash-check IMPLEMENTATION_INPUT_SHA=<full-40-hex-authorized-sha>
make -f mk/issue-5/i5-02.mk i5-02-toolchain-check IMPLEMENTATION_INPUT_SHA=<full-40-hex-authorized-sha>
make -f mk/issue-5/i5-02.mk i5-02-changed-path-check IMPLEMENTATION_INPUT_SHA=<full-40-hex-authorized-sha>
```

Each target emits `fitness-result-v1` evidence and exits non-zero for a mismatch, required missing
tool, forbidden changed path, or incomplete record. A clean Gate 0 result is `pass`; it is not a
candidate score or implementation authorization.

## Success Criteria

- [ ] Exact authority, protected baselines, toolchain, candidate modes, WEB IDs, score anchors, and path rules are machine-readable.
- [ ] Every later issue-local target depends on the authority check.
- [ ] Issue #6 remains visibly closed without blocking the retained preview path.
- [ ] Root/shared/protected/discovery paths are unchanged.

## Risk, Security, and Rollback

Risk is false authority caused by drift or a broad allow-list. Fail before writes. Operational
rollback stops owned processes and removes only generated runtime/raw evidence after safe
retention; it preserves tracked Gate 0/Gate A source, plans, retained evidence, and protected
files. If failure occurs before a commit, stop with the scoped worktree intact for review. A source
revert needs separate review; do not automate destructive Git reset/checkout or broad deletion.

## Next Steps

Proceed to Gate A only after Gate 0 passes at the implementation input authorized by the separate
validation/readiness phases.
