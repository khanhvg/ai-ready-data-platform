---
title: "Authorized Cook Scope — Issue #7 Gate 0 and Gate A Only"
issue: 7
status: authorized-with-gates
authorization: gate-0-and-gate-a-only
auditInputSha: "0486642528b9a6ba8e96cee18d6eda76c3b5deb9"
implementationInputSha: "exact-audit-output-sha-attested-in-issue-7-publication-comment"
futureBranch: "feature/issue-5-02-web-spike"
futureWorktreeName: "ai-ready-data-platform-issue-5-02-web-spike"
activeBudget: "3 hours for Gate A; Gate 0 preflight excluded"
---

# Authorized Cook Scope — Gate 0 and Gate A Only

> `READY_WITH_GATES` is not ADR/winner/full-issue readiness. Stop after the retained synthetic
> preview attestation. Do not implement a framework candidate and do not open a PR.

## Exact Authority

The only valid `IMPLEMENTATION_INPUT_SHA` is the exact audit output commit published in the issue
#7 readiness comment. It must be the commit containing this file. A literal SHA cannot be embedded
inside its own containing commit without a recursive hash claim; no predecessor, placeholder,
branch name, or `HEAD` substitution is valid.

The cook must create exactly one product worktree named
`{workspace-parent}/ai-ready-data-platform-issue-5-02-web-spike` on exactly branch
`feature/issue-5-02-web-spike`, starting at the published implementation input. Before the first
write, push the unchanged branch with upstream tracking, fetch, and prove:

```text
local HEAD == tracking ref == freshly fetched live remote == IMPLEMENTATION_INPUT_SHA
```

Resolve `{workspace-parent}` as the parent directory of the primary repository; do not treat it as
a literal directory. After proving the branch is still absent locally and remotely, the intended
sequence is:

```bash
git fetch --prune origin
git worktree add -b feature/issue-5-02-web-spike {workspace-parent}/ai-ready-data-platform-issue-5-02-web-spike <IMPLEMENTATION_INPUT_SHA>
git -C {workspace-parent}/ai-ready-data-platform-issue-5-02-web-spike push -u origin HEAD:refs/heads/feature/issue-5-02-web-spike
git -C {workspace-parent}/ai-ready-data-platform-issue-5-02-web-spike fetch origin refs/heads/feature/issue-5-02-web-spike
```

Then compare `git rev-parse HEAD`, `git rev-parse @{upstream}`, and the exact SHA returned by
`git ls-remote --heads origin refs/heads/feature/issue-5-02-web-spike`. Any pre-existing branch,
additional product worktree, mismatch, or command failure is a STOP for owner review, not an
instruction to reset, force-push, reuse, or delete it.

The input must contain planner `0890c4abab46f81d110be6cbd6de3560e631a735`, discovery
`a39251d45a56124322b9143ad16b926b2656073b`, integration
`f9a87d0ebdb72c014a6f8c6eaae865dad4d2188c`, master readiness
`e440c5855732d5d8f5d634e3cc1359c010cc5ed3`, validation/audit input
`0486642528b9a6ba8e96cee18d6eda76c3b5deb9`, and this audit output in ancestry.

After issue-owned commits, keep the input as the changed-path base. Tracking/live may equal the
input before a push or an authorized descendant after a push, but must never be divergent or
unknown. Fetch and require exact local/tracking/live equality before final Gate A publication.

## Authorized Task IDs

Only these tasks may execute, in order:

| ID | Authorized work | Exit condition |
|---|---|---|
| `G0-01` | Create/publish exact branch and one worktree; input/remote/ancestry/clean/protected preflight before first write | All immutable checks pass |
| `G0-02` | Write authority failure fixtures/tests first | All ten `G0-*` cases fail for the intended missing behavior |
| `G0-03` | Add authority/toolchain/mode/WEB-ID/score-anchor/stage-status registries | Registries parse and deferred stages remain closed |
| `G0-04` | Add dependency-free authority checker and issue-local Make fragment with only authorized targets | Clean and negative authority cases behave deterministically |
| `G0-05` | Retain Gate 0 evidence and recheck clean/protected/path/deferred state | Gate 0 `pass`; no candidate or later target exists |
| `GA-01` | Write Gate A logical/static/security/lifecycle tests and invalid fixtures first | Applicable `WEB-*`/lifecycle tests fail for intended missing behavior |
| `GA-02` | Add safe synthetic fixture, logical contracts, vectors, and pure state reducer | Contract/state/failure/trust tests pass |
| `GA-03` | Add semantic ten-act no-JS HTML with four grain-honest cards and permanent labels | Static parser/content tests pass |
| `GA-04` | Add focus/reflow/reduced-motion CSS | Static CSS/a11y facets pass; human/browser facets pending |
| `GA-05` | Add smallest optional JS for explicit previous/next, history/reload, reset, verify/evidence/export | State/navigation/reset tests pass without granting authority |
| `GA-06` | Add exact-route static host, owned lifecycle controller, and thin Make wrappers | Start/status/reset/down/direct fallback contracts pass |
| `GA-07` | Run full Gate 0/A blast radius, security/CSP/network/source/credential/non-copy/path/hash scans and rollback drill | All authorized checks pass; all deferred checks stay closed |
| `GA-08` | Commit source, rerun against exact tested tree, sanitize/retain evidence, remove transient state, attest/push | Clean tree, no process, remote equality; issue stays open |

No task ID may be renamed, merged with a deferred phase, or treated as permission for adjacent
work. A contract correction discovered after `GA-08` needs a new reviewed descendant and a fresh
clean evidence run.

## Allowed Tracked Paths

The Gate 0/A cook may create or modify only:

```text
mk/issue-5/i5-02.mk
spikes/web/common/contracts/lesson-manifest-view.schema.json
spikes/web/common/contracts/mart-evidence-view.schema.json
spikes/web/common/contracts/journey-state-view.schema.json
spikes/web/common/contracts/lab-client-view.schema.json
spikes/web/common/contracts/evidence-index-view.schema.json
spikes/web/common/contracts/candidate-evidence-record.schema.json
spikes/web/common/contracts/failure-codes.json
spikes/web/common/fixtures/synthetic-promotion-trust-v1.json
spikes/web/common/state/preview-state.mjs
spikes/web/common/state/preview-state-vectors.json
spikes/web/common/tests/fixtures/invalid-completed-state.json
spikes/web/common/tests/fixtures/invalid-cross-grain-attribution.json
spikes/web/common/tests/fixtures/invalid-executable-content.json
spikes/web/common/tests/fixtures/invalid-secret-canary.json
spikes/web/common/tests/fixtures/invalid-stale-digest.json
spikes/web/common/tests/fixtures/invalid-unknown-field.json
spikes/web/common/tests/contract-schema.test.mjs
spikes/web/common/tests/four-grain.test.mjs
spikes/web/common/tests/preview-label.test.mjs
spikes/web/common/tests/preview-authority.test.mjs
spikes/web/common/tests/state-navigation.test.mjs
spikes/web/common/tests/state-reset.test.mjs
spikes/web/common/tests/failure-taxonomy.test.mjs
spikes/web/common/tests/static-facts.test.mjs
spikes/web/common/tests/journey-contract.test.mjs
spikes/web/common/tests/browser-authority.test.mjs
spikes/web/common/tests/non-copy.test.mjs
spikes/web/preview/index.html
spikes/web/preview/preview.css
spikes/web/preview/preview.mjs
spikes/web/harness/authority.json
spikes/web/harness/toolchain.json
spikes/web/harness/candidate-modes.json
spikes/web/harness/test-ids.json
spikes/web/harness/score-anchors.json
spikes/web/harness/stage-status.json
spikes/web/harness/scripts/authority-check.mjs
spikes/web/harness/scripts/static-host.mjs
spikes/web/harness/scripts/preview-control.mjs
spikes/web/harness/tests/authority.test.mjs
spikes/web/harness/tests/preview-control.test.mjs
spikes/web/non-copy-inventory.md
spikes/web/evidence/retained/gate-a/<run-id>/**
```

No other tracked path below the named directories is implicit. Invalid test fixtures are inert
JSON data and must be schema-rejected or safely rendered as text. No package manifest, lockfile,
vendored dependency, generated build, browser artifact, source map, remote MDX, or real issue-6
fixture may appear.

Generated state may exist temporarily only at:

```text
.artifacts/evidence/web-spike/<run-id>/gate-0/**
.artifacts/evidence/web-spike/<run-id>/gate-a/**
.artifacts/runtime/i5-02/learn-preview/<port>.json
```

`.artifacts` is not ignored. Never stage it. Sanitize/hash-index the approved subset into the
retained Gate A path, then remove all transient state created by this cook.

## Protected Paths and States

Any change/presence violation is an immediate STOP:

- root `Makefile`, `.gitignore`, `release-manifest.json`, `docs/code-standards.md`;
- `contracts/**`, `schemas/**`, `tests/fixtures/learning/**`;
- `apps/learning-portal/**`, `apps/lab-runner/**`;
- existing dbt, Rill, Airflow, Iceberg, OpenMetadata, data, product, runtime, or config files;
- `plans/260721-007-web-stack-representative-lesson/**` during implementation;
- all `spikes/web/candidates/**`, candidate manifests/locks, fixture handoff, decision evidence,
  and ADR-005 paths;
- cloud, Docker, runner, credential, private API, mutation, package-install, browser-install, PR,
  review, and merge state.

Required protected baselines:

| State | Required value |
|---|---|
| `Makefile` SHA-256 | `6b75a7a1f8e516e8967d317edb9de35378c02eddd645d2731dcf5cfc9bf52f54` |
| `.gitignore` SHA-256 | `aa93e47707e95286126f47b3d70fe7fc6c047b49c861184533e38b3c5a971316` |
| `release-manifest.json` SHA-256 | `f9037b5d946d14f7b1b9c020939f1a44961011f2ad933db9f2b69054abbf9539` |
| Issue-7 discovery tree | `ed45ef287be3c0830466ae4a6b60a6bf22b1eb70` |
| `docs/code-standards.md`, portal, runner | Absent |
| Four issue-6 handoff files | Absent in this input; presence alone never opens Barrier B |

## Exact Make Surface

`mk/issue-5/i5-02.mk` may expose exactly these twelve targets:

```text
i5-02-authority-check
i5-02-protected-hash-check
i5-02-toolchain-check
i5-02-changed-path-check
i5-02-security-check
i5-02-credential-check
i5-02-non-copy-check
web-common-test
learn-preview
learn-preview-status
learn-preview-reset-check
learn-preview-down
```

Each target invokes the same authority source of truth. The fragment may not include or recurse to
the root Makefile and may not use wildcard/pattern dispatch. It must reject unknown targets. Names
containing `astro`, `next`, `vite`, `candidate`, `install`, `build`, `browser`, `a11y`, `e2e`,
`barrier`, `score`, `adr`, `winner`, `retention`, or `rollback` must not be defined or dispatched.

## Tests Before

Run and retain the intentional pre-implementation failures before adding their behavior.

Gate 0 IDs:

```text
G0-AUTH-001       wrong/missing input SHA
G0-REMOTE-001     initial mismatch or later divergence/unknown remote
G0-ANCESTRY-001   missing required immutable ancestor
G0-PROTECTED-001  hash/absence/discovery-tree drift
G0-PATH-001       path outside exact staged allow-list
G0-TOOLCHAIN-001  wrong Node/npm or non-exact frozen policy
G0-REGISTRY-001   malformed/missing WEB/mode/authority registry
G0-ANCHOR-001     incomplete/late score anchors
G0-STAGE-001      false stage/full-issue readiness
G0-DEFERRED-001   candidate/later target or path exists
```

Gate A IDs, each with explicit `staticLogical` and, where applicable, `browserDecision` or
`manualDecision` facets:

```text
WEB-CONTRACT-001  WEB-CONTRACT-002  WEB-CONTRACT-003
WEB-PREVIEW-001   WEB-PREVIEW-002
WEB-STATE-001     WEB-STATE-002
WEB-FAIL-001
WEB-TRUST-001     WEB-TRUST-002
WEB-A11Y-001      WEB-A11Y-002      WEB-A11Y-003      WEB-A11Y-004
WEB-STATIC-001    WEB-NOSCROLL-001  WEB-API-001
WEB-E2E-001       WEB-NONCOPY-001
```

Also write failing lifecycle cases for invalid/occupied port, 10-second timeout, stale/reused PID,
wrong start fingerprint/command/cwd/root/run ID/input, unsafe route/path/symlink/traversal, wrong
lesson/digest, double reset, down-without-locator, foreign listener, and an owned process that
survives shutdown.

The failure record includes exact input SHA, working-tree digest, command, test ID, expected
failure reason, actual failure reason, and no false pass. It contains no secret, absolute personal
path, score, completion, or decision field.

## Implementation and Refactor Order

1. Make Gate 0 tests fail; add registries; add authority checker; add only Gate 0 Make wrappers;
   make all Gate 0 negatives and the clean case pass.
2. Make all applicable Gate A tests fail against the missing preview.
3. Add the safe synthetic projection and plain logical contracts.
4. Add the pure dependency-free state reducer and vectors; no DOM or framework dependency.
5. Add semantic HTML containing all ten acts, prerequisite probes, deterministic hints, failure
   classes, verify/evidence/export/reflection, four separate cards, and all facts/limitations.
6. Add CSS for visible focus, in-flow layout, narrow/200% rules, and reduced motion.
7. Add the smallest progressive JavaScript for explicit previous/next, committed-versus-transient
   state, back/forward/reload, reset, fixture-only verify, evidence, and export.
8. Add the exact-route static host, then process controller, then thin Gate A Make wrappers.
9. Refactor only after green tests; do not generalize toward a candidate framework or portal.
10. Run the complete blast radius and rollback drill, commit source, rerun against that tested tree,
    retain sanitized evidence in a separate attestation commit, push, and stop.

## Learner and Data Invariants

- Exactly ten visible acts with explicit previous/next review and a useful linear no-JS path.
- Three unscored prerequisite probes and deterministic orient → connect → explain hints.
- Explicit committed/transient state; scroll, hover, motion, time, visitation, reflection, and JS
  presence never commit or verify.
- Back/forward/reload restore the committed state. Reset is idempotent for resettable lesson state,
  replaces history state, produces the same baseline digest on repeat, and advances a separate
  visible audit counter exactly once per explicit invocation.
- Controlled, environmental, and unexpected failures have distinct code/copy/recovery/progression/
  evidence behavior.
- Verify examines only the synthetic fixture. Evidence/export is sanitized. Reflection cannot
  complete anything.
- The exact notice `SYNTHETIC LEARN-PREVIEW — UNSCORED — CANNOT COMPLETE` appears at entry, state
  rail, verify/evidence, and inside every export. The state vocabulary has no `completed` value.
- Exactly four separate cards: promotion (`promo_name, channel`), fulfillment (`carrier, region`),
  returns (`reason, category, region`), and global DQ (`scenario/count`). Each card discloses grain,
  time/filter scope, numerator, denominator, weighting, and limitations.
- There is no cross-mart join, composite, visual edge, causal wording, or promotion attribution of
  fulfillment/return/DQ facts. The only expected conclusion is `insufficient evidence`.

## Static Host and Process Contract

- Hardcode real root `spikes/web/preview`; do not accept a caller-supplied directory.
- Bind only `127.0.0.1`; no `0.0.0.0`, IPv6 wildcard, remote fetch/import, service worker, CORS,
  runner/cloud route, credential, mutation, proxy, or directory listing.
- Serve only `/`, `/index.html`, `/preview.css`, `/preview.mjs`, `/__i5_02_ready`. Resolve and
  verify every file remains below the real root; reject dotfiles, symlinks, traversal, encoding
  tricks, query-driven paths, and unknown routes.
- Use CSP at least:
  `default-src 'none'; base-uri 'none'; form-action 'none'; frame-ancestors 'none'; script-src 'self'; style-src 'self'; img-src 'self'; font-src 'none'; connect-src 'none'; object-src 'none'; worker-src 'none'; manifest-src 'none'`.
- Preflight a fixed explicit port. Never scan or auto-select. Readiness must match the requested run
  ID within 10 seconds. On timeout, stop only the process group created by that start attempt.
- Store locator `.artifacts/runtime/i5-02/learn-preview/<port>.json` with PID, process group,
  process-start fingerprint, command hash, cwd, real root, host, port, run ID, fixture digest, and
  implementation input.
- `status`/`down` act only if all locator/process fields and readiness run ID match. A mismatch is
  non-zero and signals nothing. `down` with no locator is idempotent; it is non-zero if a verified
  owned process survives.

Direct lifecycle, with no package install/build:

```bash
node spikes/web/harness/scripts/preview-control.mjs start --lesson promotion-trust --port 4174 --implementation-input <IMPLEMENTATION_INPUT_SHA>
node spikes/web/harness/scripts/preview-control.mjs status --port 4174 --implementation-input <IMPLEMENTATION_INPUT_SHA>
node spikes/web/harness/scripts/preview-control.mjs reset-check --lesson promotion-trust --implementation-input <IMPLEMENTATION_INPUT_SHA>
node spikes/web/harness/scripts/preview-control.mjs down --port 4174 --implementation-input <IMPLEMENTATION_INPUT_SHA>
```

Foreground review fallback only:

```bash
python3 -m http.server 4174 --bind 127.0.0.1 --directory spikes/web/preview
```

Stop the fallback with Ctrl-C. It provides no managed PID, readiness, CSP, security, fitness, or
evidence claim. Gate A verification uses the Node host.

## Tests After and Blast Radius

Execute from the product worktree with the published full SHA substituted literally:

```bash
node --test spikes/web/harness/tests/authority.test.mjs
node --test spikes/web/harness/tests/preview-control.test.mjs
node --test spikes/web/common/tests/*.test.mjs
node spikes/web/harness/scripts/authority-check.mjs --implementation-input <IMPLEMENTATION_INPUT_SHA>
make -f mk/issue-5/i5-02.mk i5-02-authority-check IMPLEMENTATION_INPUT_SHA=<IMPLEMENTATION_INPUT_SHA>
make -f mk/issue-5/i5-02.mk i5-02-protected-hash-check IMPLEMENTATION_INPUT_SHA=<IMPLEMENTATION_INPUT_SHA>
make -f mk/issue-5/i5-02.mk i5-02-toolchain-check IMPLEMENTATION_INPUT_SHA=<IMPLEMENTATION_INPUT_SHA>
make -f mk/issue-5/i5-02.mk i5-02-changed-path-check IMPLEMENTATION_INPUT_SHA=<IMPLEMENTATION_INPUT_SHA>
make -f mk/issue-5/i5-02.mk i5-02-security-check IMPLEMENTATION_INPUT_SHA=<IMPLEMENTATION_INPUT_SHA>
make -f mk/issue-5/i5-02.mk i5-02-credential-check IMPLEMENTATION_INPUT_SHA=<IMPLEMENTATION_INPUT_SHA>
make -f mk/issue-5/i5-02.mk i5-02-non-copy-check IMPLEMENTATION_INPUT_SHA=<IMPLEMENTATION_INPUT_SHA>
make -f mk/issue-5/i5-02.mk web-common-test IMPLEMENTATION_INPUT_SHA=<IMPLEMENTATION_INPUT_SHA>
make -f mk/issue-5/i5-02.mk learn-preview LESSON=promotion-trust PREVIEW_PORT=4174 IMPLEMENTATION_INPUT_SHA=<IMPLEMENTATION_INPUT_SHA>
make -f mk/issue-5/i5-02.mk learn-preview-status PREVIEW_PORT=4174 IMPLEMENTATION_INPUT_SHA=<IMPLEMENTATION_INPUT_SHA>
make -f mk/issue-5/i5-02.mk learn-preview-reset-check LESSON=promotion-trust IMPLEMENTATION_INPUT_SHA=<IMPLEMENTATION_INPUT_SHA>
make -f mk/issue-5/i5-02.mk learn-preview-down PREVIEW_PORT=4174 IMPLEMENTATION_INPUT_SHA=<IMPLEMENTATION_INPUT_SHA>
make -f mk/issue-5/i5-02.mk learn-preview-down PREVIEW_PORT=4174 IMPLEMENTATION_INPUT_SHA=<IMPLEMENTATION_INPUT_SHA>
git diff --check <IMPLEMENTATION_INPUT_SHA>...HEAD
```

In addition:

1. Start a test-owned listener on a fixed test port; prove `learn-preview` fails without signalling
   it. If audit-observed port `4173` is still foreign-occupied, it may be an additional read-only
   collision proof, never a process to stop.
2. Inspect exact headers/body/routes over loopback and reject every unsafe/unknown path and method.
3. Prove no runtime network authority, CORS, secret/token/private URL/path, service worker,
   executable fixture content, source map, package manifest/lock, candidate/ADR path, or
   `completed` state exists.
4. Prove all four protected hashes/states, the discovery tree, changed path allow-list, exact Make
   target set, stage-status blockers, and no `.artifacts` staging.
5. Source/static checks may pass the Gate A facets of semantics, no-JS content, native controls,
   CSS reflow, and reduced-motion rules. Record actual browser/keyboard/named-screen-reader/200%/
   reduced-motion/no-JS-manual facets as `required-pending`, not pass or skip.
6. After the source commit, rerun the full suite at its exact `testedTreeSha`; create sanitized
   retained evidence and its hash index; then create a distinct attestation commit. Record that
   attestation commit externally because it cannot self-reference.
7. Stop all owned processes, remove transient cook-created `.artifacts`, fetch, push, fetch again,
   and prove clean local/tracking/live equality. Do not open a PR.

## Evidence Contract

Retain under `spikes/web/evidence/retained/gate-a/<run-id>/**` using
`fitness-result-v1`. Each record contains only allow-listed fields including:

```text
issue=7
gate=gate-0|gate-a
candidate=common|preview
fixtureKind=synthetic-preview
notice=SYNTHETIC LEARN-PREVIEW — UNSCORED — CANNOT COMPLETE
resultStatus=pass|fail
candidateDisposition=null
numericScore=null
decisionGrade=false
issueComplete=false
opensBarrierB=false
implementationInputSha=<published audit output>
testedTreeSha=<source commit tested>
```

Also record safe run ID, relative artifact locators, exact commands/tool versions, contract/
fixture/test/mode/anchor digests, failing-before and passing-after IDs, accessibility facet status,
protected hashes, changed paths, CSP/route/network/security/credential/non-copy results, lifecycle/
rollback result, artifact hashes, and redaction result. Reject absolute paths, full environment
dumps, headers/cookies/tokens, PII, raw hostile content, score/winner/completion fields, and any
self-referential commit claim.

This evidence is synthetic preview engineering evidence only. It is not release, candidate,
Barrier B, Gate C, Gate D, decision, ADR, or issue-completion evidence.

## STOP Conditions

Stop without expanding scope if any of these occurs:

- input/branch/worktree/tracking/live/ancestry mismatch, divergent remote, dirty base, or lease;
- any protected hash/state/discovery/path violation;
- required host tool mismatch or any need for npm, package/browser install, Docker, cloud, model or
  AWS credentials, runner, portal, mutation, privileged API, remote content, or root Make change;
- candidate/later target/path/manifest/lock or ADR/score/winner field appears;
- issue #6 bytes are copied, synthesized, or treated as merged;
- occupied/invalid port, readiness over 10 seconds, uncertain PID ownership, reused PID,
  mismatched run ID/process fingerprint, surviving owned process, or orphan process;
- route/path/CSP/CORS/network/secret/private-path/hostile-content/non-copy scan fails;
- any label surface is missing, any `completed` state exists, or export can imply completion/score;
- cards merge grains, omit calculation metadata/limitations, make causal attribution, or yield a
  conclusion other than `insufficient evidence`;
- a static/logical accessibility check is represented as actual browser/manual evidence;
- the common contract cannot stabilize within Gate A's three active hours;
- evidence cannot be sanitized/retained without staging transient `.artifacts` or exposing private
  data; or
- any request arises for pre-merge review, PR, merge, full issue completion, or a deferred phase.

A STOP preserves the scoped worktree for review. Do not weaken a test, substitute fake evidence,
silently skip, rebase/reset around drift, edit a protected/shared file, or auto-open a later gate.

## Operational Rollback

1. Read the exact per-port locator and verify PID, process group, process-start fingerprint,
   command, cwd, real preview root, run ID, fixture digest, and implementation input.
2. If every value matches, request graceful shutdown, then apply the bounded owned-process timeout;
   fail if the owned process survives. If anything mismatches, signal nothing and report the
   foreign/stale locator.
3. Once required sanitized evidence and hashes exist, remove only cook-created transient files
   under `.artifacts/runtime/i5-02/**` and `.artifacts/evidence/web-spike/<run-id>/**`.
4. Re-run down/status, port, changed-path, protected-hash, credential, and clean-tree checks.
5. Preserve all tracked Gate 0/A source, this plan/audit package, retained evidence, discovery,
   protected/shared files, and unrelated state. A source revert/delete needs separate review.

Never use broad recursive deletion, destructive Git reset/checkout, foreign-process signals,
shared contract edits, migrations, cloud actions, or removal of issue #6/user data as rollback.

## Explicitly Deferred

- phases 3–5 and all Astro/Next/Vite source, package install/build/test/evidence and timers;
- phase 6 Barrier B until reviewed issue #6 is merged and its exact SHA/four file digests/schema/
  zero issue-7 diff are verified;
- phase 7 current-browser, E2E, screenshots/traces, actual keyboard, named screen reader, 200%
  reflow, reduced-motion, no-JS manual review, real-fixture rerun, measurements, must-pass, score;
- phase 8 winner/no-winner ADR-005, final retention/reproduction/selection/rollback;
- the equal 14-hour candidate protocol and every 90-minute/3-hour kill;
- portal/runner/BFF/completion, root Make integration, release, human pre-merge gate, review, PR,
  merge, cloud, deployment, migration, or destructive cleanup.

After `GA-08`, stop. Issue #7 remains open even if every Gate 0/A check passes. A future owner must
perform a fresh readiness decision before any deferred work.
