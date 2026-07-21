# Verification, Evidence, and UAT

## TDD Rule

Each implementation phase begins with a retained failing test/evidence ID at the exact
implementation input and dependency SHAs. Make the smallest in-scope implementation, keep the
test green through refactor, then run the phase regression gate. Do not write portal behavior
before the corresponding RED assertion exists. Do not weaken a test, schema, fixture, S3 control,
or accessibility expectation to obtain green.

## Tests-Before Matrix

| ID | First failing assertion | Stage |
|---|---|---|
| PTP-RED-A-001 | Missing/wrong #7/#8 release, version, digest, ancestry, or lock fails Gate A | A |
| PTP-RED-A-002 | Issue #6 fixture/contract/protected hash drift fails | A |
| PTP-RED-A-010 | Business question and four independent grains absent from shell | A |
| PTP-RED-A-011 | Any cross-grain attribution or non-canonical decision renders | A/B |
| PTP-RED-A-012 | Stage A offers mutation/completion or labels baseline fixture as fresh | A |
| PTP-RED-A-013 | Back/forward/reload replays mutation or changes canonical progress | A/B |
| PTP-RED-A-014 | JavaScript-disabled route lacks grains, limitations, decision, and unavailable state | A |
| PTP-RED-A-015 | Runner unavailable/offline/environment failure is confused with controlled failure | A/B |
| PTP-RED-A-016 | Focus, semantic name, narrow overflow, reduced motion, or live region fails | A/B |
| PTP-RED-S3-001..014 | Negative rows in the S3 matrix fail for expected reason | A/B |
| PTP-RED-B-001 | Missing/wrong #9 API/registry/evidence release fails Gate B | B |
| PTP-RED-B-010 | Browser can observe/call runner transport or submit arbitrary input | B |
| PTP-RED-B-011 | Duplicate/crash/reload produces more than one operation/result | B |
| PTP-RED-B-012 | Reset deletes prior evidence or leaves non-ready workspace | B |
| PTP-RED-B-013 | Completion occurs without fresh committed verifier result and valid evidence | B |
| PTP-RED-B-014 | Artifact size/media/digest/handle disagreement still downloads/completes | B |
| PTP-RED-B-015 | Exact journey does not execute controlled failure → decision → reset → verify | B |
| PTP-RED-B-016 | `learn-down` stops/deletes foreign state or leaves owned process running | B |

Tests load the exact tracked Issue #6 fixture and released #8 manifests read-only. No copied,
synthetic, ignored, or framework-specific promotion data fixture is allowed. Real runner E2E uses
the exact released #9 conformance path; if absent, Gate B fails.

## Practical Test Portfolio

| Layer | Scope | Bound |
|---|---|---|
| Unit/component | route reducer, safe view model, status/error/live regions, controls, evidence metadata | focused files; no snapshot wall |
| Contract | #6 hashes; #8 schema/types/operation/completion; #9 API/registry/problem/idempotency/evidence | exact releases only |
| Security | PTP-S3-01..14 plus package/bundle/private-path scans | closed negative matrix |
| Accessibility | semantic roles/names, keyboard, focus, live regions, reduced motion, overflow; axe | zero Critical/Serious |
| Browser | real Chromium only; exact journey; desktop and one narrow viewport | one smoke suite |
| Static/no-JS | real JavaScript-disabled Chromium plus deterministic static parser/equivalence | one lesson |
| Recovery | runner unavailable/crash/retry, response loss, duplicate, reset/verify conflict, learn-down | exact #9 fault seams |
| Visual/UAT | fixed screenshots and bounded checklist | no native OS automation |

No Firefox/WebKit parity matrix, timer/scorecard, sample performance contest, native macOS
automation, exhaustive device grid, or automated conformance claim belongs to I5-05.

## Exact Issue Command Contract

The final Stage B exact head must run the Issue #10 Verify block unchanged:

```bash
make portal-test portal-a11y
make lesson-e2e LESSON=promotion-trust
make local-journey-e2e
make portal-visual-review
make learn-status
make learn-down
```

Also exercise the accepted lifecycle entry:

```bash
make learn LESSON=promotion-trust
```

`mk/issue-5/i5-05.mk` owns these exact I5-05 targets and delegates to locked scripts under
`apps/learning-portal/**`. It does not edit root Make or invoke Docker/Compose/Rill/Airflow/
Iceberg/OpenMetadata/AWS/Terraform.

The exact commands above are the immutable acceptance surface, not current implementation
authority. The existing root Make include seam and command-owner registry reserve them for
`mk/issue-5/i5-05.mk`. Today both stage command allow-lists are `[]`. After a later exact-SHA
amendment and readiness authorize the fragment, every target must remain resolvable and return a
typed non-zero dependency-unavailable result until its own stage gate is satisfied. Stage A may
then run only the explicitly authorized runner-independent subsets; it cannot claim the Issue
Verify block because `lesson-e2e` and `local-journey-e2e` require Stage B.

## Command Acceptance

| Command | Required result/evidence |
|---|---|
| `make portal-test portal-a11y` | unit/state/released-contract/S3 tests, build/typecheck, axe zero Critical/Serious, no hidden completion |
| `make lesson-e2e LESSON=promotion-trust` | one Chromium journey for the exact released lesson; desktop+narrow; no-JS/static equivalence |
| `make local-journey-e2e` | clean namespaced real runner/core journey, controlled failure, canonical decision, reset, fresh verify, completion, evidence download/digest, cleanup |
| `make portal-visual-review` | deterministic bounded screenshots/trace/manifest/UAT checklist; no automatic human approval |
| `make learn-status` | schema-valid owned PID/start identity, portal/runner readiness, workspace and evidence root; unavailable typed honestly |
| `make learn-down` | idempotent owned process-group stop, secret revocation, scoped workspace cleanup, evidence retained, foreign state untouched |
| `make learn LESSON=promotion-trust` | loopback portal/private runner/core only; useful URL/status/teardown; unsafe prerequisite fails before mutation |

Each required target emits only the exact portal-compatible result/evidence schema released by #8
and pinned in the later amendment under `.artifacts/evidence/local-journey/{run-id}/`, with
command, tool versions, input/output/tested-tree SHAs, dependency merge/release SHAs,
contract/fixture/lock hashes, assertions, result, artifact hashes, redaction/retention class, and
rollback result. The current `fitness-result-v1` registry row is not a runtime fallback. Missing
required tool/evidence is `fail`.

## Chromium Smoke

Use the exact Chromium revision and one desktop plus one narrow viewport locked by the merged
Issue #7 handoff and pinned in the later amendment. This plan does not invent viewport literals
before that handoff.

Fix locale `en-US`, timezone `UTC`, color scheme, reduced-motion mode, animation/transition
suppression for capture, seeded data, route, and released dependency hashes. Assertions cover:

- visible focus and logical keyboard order;
- no horizontal document overflow at both viewports;
- business question, four grain names/limitations, controlled/environment failure distinction;
- exact canonical decision;
- reset/retry state and prior-evidence retention;
- verified evidence metadata/download at Stage B;
- no console/page/unhandled errors or CSP violations.

The same suite invokes axe once per required state set, with zero Critical/Serious violations.
Automated checks are necessary but do not claim full WCAG 2.2 AA or screen-reader conformance.

## No-JavaScript and Static Fallback

A real Chromium context with JavaScript disabled loads the exact released interactive entry and
follows its static path. A separate parser test reads the built static HTML. Both must prove the same stable
released facts: stakeholder question, four mart IDs/grains, each limitation, expected controlled
failure, `insufficient-evidence`, `no-common-grain`, reset explanation, baseline fixture label,
and runner-unavailable/non-completion notice. No fact/control may exist only behind animation,
hover, client JavaScript, or scroll position.

## Runner Failure and Idempotency Cases

Run against the released #9 fault/conformance seams:

1. runner absent/not-ready before start: no mutation; static lesson remains available;
2. runner crashes before commit: environmental failure; retry/recover/reset offered; no progress;
3. result commits but response is lost: same idempotency key returns committed result;
4. evidence commits before completion transaction: reconcile through the one #8 transaction or
   quarantine; no early completion;
5. duplicate click/request: one operation ID and one committed result;
6. reset versus verify conflict: released typed conflict; never two successful mutations;
7. portal restart: reload canonical runner/completion state; no POST replay;
8. corrupted/missing artifact or wrong digest: evidence/download/completion fail;
9. `learn-down` during active operation: released cancellation/reconciliation, full owned process
   group stopped, prior evidence retained.

## Deterministic Portal Visual Review

`make portal-visual-review` is a bounded artifact generator, not native OS automation. It:

1. runs the locked Chromium at the one desktop and one narrow viewport pinned from #7;
2. captures a fixed state list: entry/question, four-grain context, controlled failure,
   canonical decision, runner unavailable, reset/retry, verified evidence, and static fallback;
3. records full-page and focused-control screenshots, trace, console/CSP result, viewport,
   locale/timezone, dependency/input/tested-tree SHAs, and artifact SHA-256;
4. emits a deterministic manifest and `uat-checklist.md` beneath the current evidence root;
5. exits non-zero on missing state/artifact, overflow, focus invisibility, console/CSP error,
   mismatch, or unbounded capture count.

The checklist asks one human to review information hierarchy, focus visibility, error/live-region
copy, grain honesty, narrow readability, static equivalence, reduced-motion result, evidence
integrity wording, and absence of a false completion claim. Reviewer identity, exact head, date,
result, and residual notes are added outside the deterministic artifact hash. The command never
clicks VoiceOver/System Settings/native browser menus and never fabricates approval.

## Retention and Cleanup Evidence

Retain:

- RED results and assertion IDs;
- Gate A/B dependency identity manifests;
- unit/contract/S3/a11y/axe reports;
- Chromium trace/screenshots/static HTML digest;
- real journey operation/state transition log;
- evidence manifest/download digest;
- learn status/down and rollback results;
- exact-head human UAT/pre-merge approval.

Cleanup removes only marker-verified I5-05 temporary state and runner-owned workspace through the
released API. It preserves committed evidence, the completion record for its retention period,
the Issue #6 fixture, unrelated ignored files, other worktrees, and other process groups. A
rollback first disables Stage B and proves Stage A fallback, then restores the exact reviewed Git
point without deleting evidence.

## Release Gate

Before any Stage A or Stage B merge:

- fresh independent plan validation and stage-specific readiness are published at exact heads;
- required tests and S3 scans pass with zero unresolved Critical/High findings;
- changed paths match exclusive ownership; protected/shared hashes match;
- dependency releases and human review bind the exact PR head;
- the branch is clean and local = tracking = fresh-live;
- no cloud/AWS/Terraform/destructive action occurred;
- human exact-head pre-merge approval is recorded.

Planning/static checks performed on this plan do not satisfy any item above.
