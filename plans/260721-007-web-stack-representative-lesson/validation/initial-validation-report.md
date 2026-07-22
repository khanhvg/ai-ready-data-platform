# Independent Initial Plan Validation — Issue #7

## Verdict

**PASS** after bounded planning-only corrections. The eight-phase plan is internally consistent,
implementable within its declared authority, and fail-closed around issue #6, browsers, manual
accessibility, scoring, and the 14-hour cap. This verdict validates the plan, not any future
implementation, browser result, fixture, candidate, score, ADR decision, PR, or merge.

## Immutable Inputs and Phase Identity

| Input | Immutable SHA / observed state | Validation result |
|---|---|---|
| Fresh planner output and validator input | `0890c4abab46f81d110be6cbd6de3560e631a735` | Local HEAD, tracking ref, and live remote were exact before edits |
| Discovery | `a39251d45a56124322b9143ad16b926b2656073b` | Commit resolves; `discovery/**` retained at tree `ed45ef287be3c0830466ae4a6b60a6bf22b1eb70` |
| Audit integration | `f9a87d0ebdb72c014a6f8c6eaae865dad4d2188c` | Commit resolves and is in required ancestry |
| Master readiness report | `e440c5855732d5d8f5d634e3cc1359c010cc5ed3` | Commit resolves and is in required ancestry |
| Repository / branch | `khanhvg/ai-ready-data-platform`; `plan/issue-7-web-stack-representative-lesson` | Exact requested worktree and branch |
| Validator phase | Independent initial plan validation; 2026-07-21 Asia/Ho_Chi_Minh | No discovery/planner role reuse; no subagent/team |
| Issue #7 live state at entry | Open; `ready for plan validation`, `risk:high`, `tdd`, `security:S3`, `frontend`, `accessibility`, `decision-gate` | Body and all four comments read |
| Issue #6 live state | Open; no merged fixture output; comment clarifies exact fixture ownership | Dependency/path authority verified only; no unmerged output consumed |

Requested validator profile was Codex `gpt-5.6-sol` with `model_reasoning_effort="xhigh"`.
Validation used the Full `ck:plan validate` workflow and four independent lenses per phase:
implementation feasibility (`IF`), architecture/learning (`AL`), frontend/accessibility (`FA`),
and security/QA (`SQ`). No red-team, readiness/plan-to-cook audit, cook, implementation, package
install/build, product/config/data edit, browser scoring, cloud action, PR, or merge occurred.

## Status Vocabulary

- `VF` — verified fact from Git, live issue state, repository source, master contract, or read-only
  package metadata.
- `PC` — internally consistent and testable plan contract; future behavior is not claimed to exist.
- `FIX` — correctable plan gap found and corrected under the exact issue #7 plan directory.
- `GATE` — honest external or future execution condition that remains unverified/closed.

## Validation Questions and Answers

No user decision question was necessary. The issue body/comments and binding master artifacts
already fix the authority, candidates, modes, weights, clocks, fixture barrier, evidence rules,
and no-winner behavior, while the request explicitly permits bounded plan fixes. Asking the user
to re-select those decisions would have contradicted source authority.

| Check | Answer and source |
|---|---|
| What owns the implementation paths? | Issue #7 body owns only `spikes/web/**`, the three exact ADR/scorecard paths, and `mk/issue-5/i5-02.mk`; plan-state sync is planning-only. |
| Can root integration be required? | No. Root `Makefile`, `.gitignore`, shared contracts/schemas, portal, runner, and protected product/data paths remain forbidden. Issue-local `make -f` and direct fallbacks are the executable interfaces. |
| What is the first runnable result? | Gate A's retained semantic synthetic preview, independent of issue #6 and every candidate outcome. It is permanently unscored and non-completing. |
| May pre-#6 evidence score? | No. Foundation scope is only `PROVISIONAL_UNSCORED` or `ELIMINATED`; decision-scope browser/manual/real-fixture work remains mandatory Gate C input. |
| Is a browser absence optional? | No. Early static/parser work may proceed, but browser/manual commands fail closed at Gate C and block all score/winner publication. |
| Can issue #7 copy issue #6 data? | No. Barrier B accepts only an actual merged SHA plus exact four-file/schema digests; files stay read-only and any fixture drift invalidates all candidate evidence. |
| Can weighting rescue a hard failure? | No. The 12 must-passes precede scoring; eliminated/incomplete candidates have null scores. |
| Can Astro preference create a winner? | No. It applies only within five points among complete passing candidates with valid evidence; every no-winner condition and cap dominates it. |
| Does S3 authorize privilege? | No. It requires negative boundaries and future Host/Origin/session/CSRF/DNS-rebinding/BFF compatibility without implementing auth, mutation, runner access, or privilege. |
| What is the future implementation base? | A later readiness handoff must name one exact full `IMPLEMENTATION_INPUT_SHA`; Gate 0 proves initial local/tracking/live-remote equality and retains it as ancestry/changed-path authority. |

## High-Risk Sample — 120 Claims

Fifteen independent repository/contract/testability claims were sampled for each of eight phases
(120 total; required minimum 96). `PC` means the plan makes the claim testable, not that the future
artifact exists.

### Phase 1 — Gate 0 Authority and Freeze (15)

| # | Lens | Status | Claim and sampled evidence |
|---:|---|---|---|
| 1.01 | SQ | VF | Pre-edit HEAD, tracking, and live remote were all `0890c4a…`; the SHA-drift stop gate passed. |
| 1.02 | IF | VF | Planner, discovery, integration, and readiness SHAs all resolve as commits; Git ancestry can be tested locally. |
| 1.03 | AL | VF | Live issue #7 grants only the narrow spike/ADR/Make-fragment paths used by the plan. |
| 1.04 | SQ | VF | Root `Makefile` hash is `6b75a7…f52f54`; it exposes no issue #7/root preview alias today. |
| 1.05 | SQ | VF | `.gitignore` hash is `aa93e4…971316`; it ignores both `plans/` and `package-lock.json`. |
| 1.06 | SQ | VF | `release-manifest.json` hash is `f9037b…f9539`; the plan protects it read-only. |
| 1.07 | IF | VF | `docs/code-standards.md`, portal, runner, and the issue #6 handoff files are absent at validator input. |
| 1.08 | IF | VF | Runtime Node `v22.22.3` and npm `10.9.8` exactly match the freeze and satisfy the declared framework engines. |
| 1.09 | SQ | VF | Read-only npm metadata resolves Astro 7.1.3, Next 16.2.10, Vite 8.1.5, Playwright 1.61.1, and React 19.2.7 with integrity values. |
| 1.10 | AL | PC | Astro static/island, Next standalone App Router, and Vite prerendered/MPA modes are singular and reject metric-friendly substitution. |
| 1.11 | FA | PC | The common WEB-ID registry is frozen before candidates; missing/duplicate/renamed assertions fail the gate. |
| 1.12 | SQ | FIX | Replaced the impossible discovery-SHA-as-future-HEAD rule with exact later implementation-input equality, required ancestry, and drift checks. |
| 1.13 | IF | FIX | Added exact-path tracked-state proof for the three candidate locks ignored by repository policy; broad force-add stays forbidden. |
| 1.14 | AL | FIX | Added a complete pre-observation 0..5 anchor registry/digest gate before any candidate action. |
| 1.15 | SQ | GATE | The future readiness-authorized `IMPLEMENTATION_INPUT_SHA` does not exist yet and correctly blocks Phase 1 execution, not plan validation. |

### Phase 2 — Gate A Common Contract and Static Preview (15)

| # | Lens | Status | Claim and sampled evidence |
|---:|---|---|---|
| 2.01 | IF | PC | Gate A depends only on Gate 0 and dependency-free Node/static files; issue #6, a package install, runner, portal, browser, and cloud are not hidden prerequisites. |
| 2.02 | AL | PC | The common boundary contains logical manifest/mart/state/client/evidence/failure shapes and test semantics, not rendering/router/component APIs. |
| 2.03 | AL | PC | `preview-journey-contract.md` specifies exactly ten acts from frame through reflection. |
| 2.04 | FA | PC | Three novice probes and `orient`/`connect`/`explain` hints are distinct, reversible, and non-completing. |
| 2.05 | AL | VF | Repository SQL/Rill sources support four distinct grains: promotion/channel, carrier/region, return reason/category/region, and global scenario/count. |
| 2.06 | AL | PC | Every card discloses filters, numerator, denominator, aggregation/weighting, time scope, limitations, and evidence reference. |
| 2.07 | SQ | PC | Contract/schema/DOM/copy/diagram scans forbid causal cross-mart relationships and require exactly `insufficient evidence`. |
| 2.08 | FA | PC | Exact label `SYNTHETIC LEARN-PREVIEW — UNSCORED — CANNOT COMPLETE` appears on entry, rail, verify/evidence, and export. |
| 2.09 | FA | PC | `completed` is forbidden from schema, DOM, URL, storage, events, evidence, and export. |
| 2.10 | FA | PC | Explicit controls alone commit; scroll, hover, motion, time, card visits, reflection, and JavaScript alone remain transient/non-authoritative. |
| 2.11 | FA | PC | Back/forward/reload preserve committed state while digest change or tampering resets safely; browser truth cannot author verification. |
| 2.12 | SQ | PC | Controlled, environmental, unexpected, and future-auth compatibility failures have separate codes, copy, recovery, progression, and implementation authority. |
| 2.13 | FA | PC | Native semantics, named-AT/manual keyboard, logical focus/status/errors, 200% reflow, reduced motion, and no-JS/static evidence are hard gates, never weighted trade-offs. |
| 2.14 | IF | FIX | Added deterministic loopback port behavior, explicit override validation, occupied-port failure, 10-second readiness timeout, owned-process cleanup, and honest foreground fallback semantics. |
| 2.15 | SQ | FIX | Added `learn-preview-reset-check` to prove duplicate reducer reset, baseline digest, visible count, history replacement, and idempotency without claiming it mutates an open browser. |

### Phase 3 — Astro React Islands Foundation (15)

| # | Lens | Status | Claim and sampled evidence |
|---:|---|---|---|
| 3.01 | IF | VF | `astro@7.1.3` exists and its Node engine `>=22.12.0` accepts the frozen Node version. |
| 3.02 | AL | PC | Astro mode is frozen to static output with the common production-like static host, never its dev server for evidence. |
| 3.03 | FA | PC | Full semantic lesson HTML precedes hydration; only reversible lab controls enter the React island. |
| 3.04 | SQ | PC | Fixture strings remain data; only trusted project build-time content is compiled, with schema validation. |
| 3.05 | AL | PC | Importing the entire lesson/content tree into the island is an explicit kill condition, keeping the comparison meaningful. |
| 3.06 | IF | PC | The 90-minute gate requires clean install, static build, semantic route, and common consumption. |
| 3.07 | SQ | PC | The three-hour gate eliminates on any executable foundation-scope failure; no time extension exists. |
| 3.08 | IF | FIX | The independently generated Astro lock must be exact-path force-added and proven tracked despite `.gitignore`. |
| 3.09 | AL | PC | Adapter use cannot add candidate-only fields/transitions or modify common/#6 contracts. |
| 3.10 | FA | PC | No-JS facts, acts, cards, limitations, label, and fallback navigation remain complete. |
| 3.11 | SQ | PC | Client graph, CSP, source maps, browser types, network inventory, and hostile content are explicit failure surfaces. |
| 3.12 | SQ | PC | Lifecycle scripts, advisories, licenses, provenance, lock hash, and build manifest enter retained evidence. |
| 3.13 | FA | FIX | Foundation evidence no longer ambiguously requires unavailable browser targets; it lists them as mandatory pending decision scope. |
| 3.14 | SQ | PC | Pre-B result is only `PROVISIONAL_UNSCORED` or `ELIMINATED`, with `numericScore: null`. |
| 3.15 | IF | GATE | Astro is not installed/built/tested here; the future timer and all foundation assertions remain execution gates. |

### Phase 4 — Next App Router Foundation (15)

| # | Lens | Status | Claim and sampled evidence |
|---:|---|---|---|
| 4.01 | IF | VF | `next@16.2.10` exists and its Node engine `>=20.9.0` accepts the frozen Node version. |
| 4.02 | AL | PC | One honest topology is frozen: self-hosted standalone App Router, not static export/dev/edge substitution. |
| 4.03 | AL | PC | Semantic content stays server/prerendered where supported; the `use client` boundary contains only explicit reversible state. |
| 4.04 | SQ | PC | The Route Handler is read-only fixture replay/readiness; Server Actions, mutation, runner URLs, credentials, and cloud paths fail. |
| 4.05 | SQ | PC | Trusted MDX/frontmatter receives an explicit schema; `@next/mdx` alone cannot count as validation. |
| 4.06 | FA | PC | The initial response must be semantic and usable without JavaScript, with the same common facts and state invariants. |
| 4.07 | IF | PC | The 90-minute foundation requires clean install, standalone build, semantic route, and common consumption. |
| 4.08 | IF | PC | The three-hour cap covers executable foundation tests, lifecycle, CSP, bundle, and supply-chain evidence. |
| 4.09 | IF | FIX | The independent Next lock is explicitly tracked by exact force-add; root/common workspaces remain prohibited. |
| 4.10 | SQ | PC | CSP/render-mode tests reject wildcard origin, `unsafe-eval`, remote script, and hidden dynamic-mode switches. |
| 4.11 | AL | PC | Server/client graph, integrated process-tree/RSS hooks, cache behavior, and static facts are retained rather than normalized to Astro/Vite topology. |
| 4.12 | FA | FIX | Browser E2E/a11y are mandatory Gate C decision-scope commands, not a pre-B provisional pass or optional skip. |
| 4.13 | SQ | PC | A pre-Gate-C evidence target rejects numeric score/winner and missing pending-decision inventory. |
| 4.14 | AL | PC | Future BFF evolution is only an OpenAPI-compatible read-only seam; no privilege is implemented to improve Next's score. |
| 4.15 | IF | GATE | No Next install/build/process evidence exists yet; all candidate feasibility measurements remain future gates. |

### Phase 5 — React/Vite Typed API Foundation (15)

| # | Lens | Status | Claim and sampled evidence |
|---:|---|---|---|
| 5.01 | IF | VF | `vite@8.1.5` exists and its Node engine `^20.19.0 || >=22.12.0` accepts the frozen Node version. |
| 5.02 | AL | PC | Vite mode is a real prerendered/MPA semantic artifact with progressive React, not an empty SPA shell. |
| 5.03 | AL | PC | Evidence is served by the common production-like static host; `vite preview` is diagnosis-only and prohibited in decision evidence. |
| 5.04 | SQ | PC | The typed adapter is read-only; public `VITE_*` values reject secret-shaped/private/runner URLs. |
| 5.05 | SQ | PC | Trusted project content is build-time/schema-validated; runtime MDX/eval/fixture JSX is forbidden. |
| 5.06 | FA | PC | Complete facts and linear navigation exist in emitted HTML before enhancement. |
| 5.07 | IF | PC | The 90-minute gate requires clean install, successful static build, semantic route, and common consumption. |
| 5.08 | IF | PC | The three-hour cap includes unit/schema/static/env/lifecycle evidence and permits no custom SSR-framework escape. |
| 5.09 | IF | FIX | The independent Vite lock is explicitly force-added by exact path and must be tracked. |
| 5.10 | SQ | PC | Asset manifest, compressed/raw JS, lazy chunks, CSP, maps, lifecycle, advisories, licenses, and provenance are retained. |
| 5.11 | AL | PC | Candidate-native authoring/API seams remain measurable; common rendering primitives are not introduced. |
| 5.12 | FA | FIX | Browser a11y/E2E remain required decision-scope Gate C work without contaminating foundation disposition semantics. |
| 5.13 | SQ | PC | Empty/non-semantic HTML, unsafe public env, dev-server substitution, mode/fixture drift, and missing pending gates are non-zero failures. |
| 5.14 | AL | PC | Killed Vite remains retained and cannot be resurrected/scored without a separately authorized spike. |
| 5.15 | IF | GATE | No Vite build or true prerender feasibility result exists yet; implementation must prove it inside equal clocks. |

### Phase 6 — Barrier B Issue #6 Fixture Handoff (15)

| # | Lens | Status | Claim and sampled evidence |
|---:|---|---|---|
| 6.01 | SQ | VF | Live issue #6 is open; no merge SHA or product output may be assumed. |
| 6.02 | AL | VF | Issue #6 comments clarify its write authority to the two tracked fixture files plus invalid fixtures; issue #7 remains read-only. |
| 6.03 | IF | VF | All four required handoff files are absent at validator input, so Barrier B is honestly closed. |
| 6.04 | SQ | PC | Barrier B requires a full SHA that is an actual merged ancestor of the tested tree, not a branch/ref/comment claim. |
| 6.05 | SQ | PC | Exact SHA-256 digests are required for promotion-trust evidence JSON, manifest JSON, lesson manifest schema, and lab evidence schema. |
| 6.06 | AL | PC | The two contract files are read as canonical schemas; issue #7 may not fork, copy, or patch around them. |
| 6.07 | SQ | PC | Dependency files must have zero issue #7 diff, and mixed/dirty/untracked substitutes fail. |
| 6.08 | AL | PC | Every mart declaration requires source, grain, time, filters, numerator, denominator, weighting, limitations, and evidence reference. |
| 6.09 | AL | PC | Cross-grain relationship/causality fields are rejected; fixture schema cannot manufacture a common promotion/fulfillment/return grain. |
| 6.10 | SQ | PC | Secret, raw-row, absolute-path, private URL, framework score, ADR decision, and recursive-SHA fields are forbidden. |
| 6.11 | FA | PC | A fixture digest change invalidates all candidate/browser/manual/persisted-state evidence, not just one candidate. |
| 6.12 | IF | PC | Absent/unmerged/mixed/tampered/schema-invalid cases are tests-before inputs and cause a non-zero barrier command. |
| 6.13 | SQ | PC | Stale provisional evidence cannot enter Gate C or ADR-005 after a fixture change. |
| 6.14 | AL | PC | Gate A preview remains runnable on its synthetic fixture while Barrier B is closed, with no score path. |
| 6.15 | IF | GATE | The exact issue #6 merge SHA and four observed digests are intentionally unknown until a reviewed merge exists. |

### Phase 7 — Gate C Real Fixture Rerun and Score (15)

| # | Lens | Status | Claim and sampled evidence |
|---:|---|---|---|
| 7.01 | SQ | GATE | No browser scoring was run; fresh Playwright/current-browser evidence remains a hard entry gate. |
| 7.02 | IF | VF | `@playwright/test@1.61.1` exists and accepts the frozen Node engine; browser binaries/channels were not installed or probed. |
| 7.03 | FA | PC | Gate C requires stable Chrome plus one additional engine, exact versions, fresh screenshots/traces, and normalized projects. |
| 7.04 | FA | GATE | Named screen-reader/browser/OS, keyboard, 200% zoom/reflow, reduced-motion, and no-JS manual evidence must still be performed. |
| 7.05 | AL | PC | Twelve binary must-passes cover common shape, static/a11y/state/failure/trust/security/content/BFF/lifecycle/supply chain before weights. |
| 7.06 | AL | FIX | All seven 0..5 anchor levels/predicates now freeze before candidates; post-observation edits/digest drift invalidate scoring. |
| 7.07 | IF | PC | Three complete rotated rounds produce three cold and three warm samples per survivor, with no selective retry. |
| 7.08 | IF | PC | Cold/warm readiness, process-tree RSS, client/build sizes, browser transfer, and authoring task have distinct declared measurements. |
| 7.09 | AL | PC | Static host RSS for Astro/Vite and integrated Next server RSS are labelled honestly; topology is not normalized away. |
| 7.10 | SQ | PC | Raw environment includes OS/CPU/memory/tool/browser/font/locale/viewport/port/background/order/digests/command hashes. |
| 7.11 | FA | PC | Entry/failure/four-card/reset/verify/reflection screenshots and first-failure traces cover the representative journey. |
| 7.12 | SQ | PC | Any red/missing manual/browser/security/non-copy/retention input eliminates or forces no-winner; no partial score exists. |
| 7.13 | AL | PC | Weights sum to 100 and points are `weight * anchor / 5`; scoring receives only complete passing candidates. |
| 7.14 | AL | PC | Astro tie preference is subordinate to complete pass, valid inputs, five-point threshold, no-winner conditions, and cap. |
| 7.15 | IF | PC | Gate C and D share the final two hours; inability to complete fair reruns/evidence within 14 total hours produces no winner. |

### Phase 8 — Gate D ADR Retention and Handoff (15)

| # | Lens | Status | Claim and sampled evidence |
|---:|---|---|---|
| 8.01 | AL | VF | Issue #7 body authorizes exactly ADR `docs/decisions/0005-web-stack.md` and two scorecard evidence paths. |
| 8.02 | AL | PC | ADR status is always `Proposed`; automation cannot write `Accepted` or imply merge/release authority. |
| 8.03 | SQ | PC | Machine JSON is derived from verified Gate C indexes and is authoritative for consistency with Markdown/ADR prose. |
| 8.04 | SQ | PC | Eliminated/incomplete candidates have no numeric score; explicit no-winner contains no hidden default. |
| 8.05 | IF | PC | Winner reproduction uses exact candidate path, mode, lock, build/start/test commands, and input digests. |
| 8.06 | IF | PC | All three source trees and locks remain through I5-05; only transient install/build/runtime state may be safely removed. |
| 8.07 | AL | PC | Losing builds are excluded from default/product entrypoints while explicit issue-local reproduction remains. |
| 8.08 | SQ | PC | Retention indexes source/locks/commands/raw/browser/manual/non-copy hashes and separates tested-tree from containing-commit attestation. |
| 8.09 | SQ | PC | Recursive/self SHA claims, illegal status, mismatched outcome/digest, premature removal, and root alias are negative tests. |
| 8.10 | IF | PC | A no-winner scorecard can pass schema while `web-winner-reproduce` correctly refuses non-zero and points to the neutral preview. |
| 8.11 | SQ | PC | Local rollback removes selection/scores, restores Proposed/no-winner, stops scoped state, and preserves source/evidence/protected files. |
| 8.12 | AL | PC | Root alias, shared contracts, portal/runner integration, cloud deploy, PR, merge, and later cleanup remain separate owners/actions. |
| 8.13 | FA | PC | The neutral semantic preview/common tests survive winner, no-winner, elimination, and rollback outcomes. |
| 8.14 | AL | FIX | Removed the stale implication that independent validation/readiness occurs after Phase 8; it correctly precedes Phase 1. |
| 8.15 | IF | GATE | No ADR/scorecard/retention artifact exists yet; human pre-merge review and downstream I5-03/I5-05 remain future gates. |

## Findings by Severity and Exact Fixes

### Critical

None remaining. No plan condition permits issue #6 substitution, hidden privilege, scoring before
must-pass, an accessibility trade-off, an unbounded timer, or unauthorized shared/root work.

### High — corrected

1. **Future SHA authority conflated discovery with implementation input.** Phase 1 previously used
   discovery SHA `a39251d…` as `HEAD`/changed-path base even though validation/readiness descendants
   must precede implementation. Corrected `plan.md`, Phase 1, candidate protocol, and implementation
   handoff to require a later exact `IMPLEMENTATION_INPUT_SHA`, initial local/tracking/live-remote
   equality, immutable ancestor checks, later ancestry, and remote-drift failure.
2. **Pre-B browser status was internally ambiguous.** Candidate phases listed required browser
   commands inside the three-hour foundation gate while also allowing a provisional result when
   browsers were pending. Corrected the protocol, matrix, phases 3–5, and handoff with explicit
   `foundation` versus mandatory Gate C `decision` scope. No browser/manual result is optional or
   treated as passed.
3. **Independent locks could be silently untracked.** Root `.gitignore` ignores
   `package-lock.json`. Corrected Phase 1, phases 3–5, protocol, matrix, plan acceptance, and handoff
   to force-add only the three exact candidate locks and fail when they are untracked or broadly
   force-added. The dependency-free common harness no longer claims a lock.
4. **Score anchors were named but not frozen against hindsight.** Corrected Phase 1, protocol,
   matrix, Gate C, plan acceptance, and handoff to require a complete seven-category 0..5
   machine-checkable predicate registry, digest-frozen before any candidate action, with rejection
   of post-observation edits or free-form interpolation.

### Medium — corrected

5. **Gate A lifecycle lacked exact reset/timeout/port evidence.** Corrected Phase 2, protocol, and
   handoff with default/override port rules, occupied-port failure, 10-second readiness timeout,
   owned-process termination, clear status/down semantics, honest Python fallback, and an
   idempotent reducer reset-check target.
6. **Phase 8 next step repeated pre-implementation gates after implementation.** Corrected its
   handoff language so validation/readiness precede Phase 1 and downstream review follows Phase 8.

### Low / informational

- Gate C plus ADR publication is deliberately tight at two active hours. This is binding master
  authority; the safe outcome is no-winner, not a timer bypass.
- The plan may retain an early runnable preview before browser availability, but cannot claim full
  preview accessibility acceptance or decision evidence until required browser/manual records pass.

## Remaining Honest Blockers and Unverified Gates

1. Issue #6 is open and its four required tracked handoff files are absent. Barrier B is closed.
2. No exact merged issue #6 SHA or four observed file digests exist yet.
3. Fresh current-Chrome/additional-engine Playwright evidence has not been produced.
4. Manual keyboard, named screen-reader/browser/OS, 200% reflow, reduced-motion, and no-JS evidence
   has not been produced.
5. A later readiness handoff has not assigned `IMPLEMENTATION_INPUT_SHA`.
6. All Make/direct commands are explicitly future. No spike code, candidate package, fixture,
   browser binary, score, ADR decision, or evidence run was asserted present.

These conditions block their execution gates and any winner, not the correctness of this plan.

## Whole-Plan Consistency and Traceability

- Structure is eight phases with valid frontmatter and one acyclic dependency chain:
  `1 → 2 → {3,4,5} → 6 → 7 → 8`.
- Timing is identical everywhere: `3h Gate A + 3h Astro + 3h Next + 3h Vite + 2h Gate C/D = 14h`;
  each candidate has the same 90-minute foundation kill and three-hour cap.
- Authority terminology now consistently separates planner output, discovery/integration/readiness
  ancestry, later implementation input, issue #6 merge input, and tested-tree/containing-commit
  evidence.
- Gate vocabulary is consistent: Gate 0 authority/freeze; Gate A retained preview; Barrier B #6
  merge/digests; Gate C fresh decision rerun; Gate D Proposed ADR/retention.
- Every discovery Critical/High aggregate and all `WD-*`, `PR-*`, `SC-*`, and `PH-*` identifiers map
  in `acceptance-and-test-matrix.md` to owner paths, tests/evidence, rollback, dependencies, and
  preview/ADR/portal boundaries. All shared `WEB-*` IDs map to a path/assertion, evidence, rollback,
  dependency, and the same three boundaries.
- Repository mart SQL/metric sources support the four declared grains and calculation limitations;
  no plan path introduces a cross-mart causal join.
- S3 security disposition explicitly covers credential/private-path canaries, runner/private URL,
  privileged routes, wildcard CORS, remote/runtime content, CSP, lock/lifecycle/advisory/license,
  evidence sanitation, Host/Origin/DNS-rebinding compatibility, future session/CSRF/BFF rules, and
  the prohibition on implementing privilege for score.
- All phases retain tests-before, bounded implementation/refactor, tests-after/blast-radius,
  future commands with non-zero behavior, evidence/rollback, and explicit dependencies.
- Discovery history is unchanged; only bounded planning artifacts and this validation report were
  modified.

## Verification Commands and Publication Checks

The validator ran or will re-run before publication:

```text
git rev-parse HEAD; git rev-parse @{u}; git ls-remote origin refs/heads/plan/issue-7-web-stack-representative-lesson
gh issue view 7 --comments; gh issue view 6 --comments
git cat-file -e <each immutable SHA>^{commit}
ck plan status plans/260721-007-web-stack-representative-lesson
frontmatter / dependency-DAG / relative-link / anchor / WEB-ID / discovery-ID sweeps
future-command registry / ownership / traceability / terminology sweeps
git check-ignore -v --no-index <exact issue #7 plan paths>
git diff --check
changed-path allow-list / protected-hash / discovery-tree checks
high-confidence credential and private-path scans
```

Read-only toolchain/package metadata probes were permitted validation evidence; no install, build,
candidate command, browser run, scoring, or product execution occurred. Final command results and
the output commit SHA are published in the issue #7 validation comment.

Observed pre-commit results:

| Sweep | Result |
|---|---|
| SHA drift / ancestry | PASS — exact planner HEAD/tracking/live remote at entry; all four immutable commits resolve; discovery/integration/readiness are ancestors |
| `ck plan status` | PASS — issue #7, `pending`, 0/8 complete, requested branch and tags |
| Frontmatter / DAG | PASS — 9 YAML frontmatters parse; phases 1..8 unique; no missing, forward, or unknown dependency |
| Links / anchors | PASS — 22 Markdown files; 0 missing relative links; 0 bad anchors |
| Traceability IDs | PASS — 19 WEB IDs + 68 discovery Critical/High IDs expected; 0 missing |
| Command ownership | PASS — 38 issue-local Make targets used; all 38 represented in the canonical registry |
| Validation sampling | PASS — 15 claims in each of 8 phases (120 total) |
| Ignore probe | PASS — `plans/**/*` and `package-lock.json` ignores confirmed; only the exact issue #7 plan directory was force-added for publication |
| Scope / protected state | PASS — staged paths stay under the exact plan directory; raw discovery diff empty; protected hashes and absence markers unchanged |
| Whitespace / secrets / private paths | PASS — `git diff --check`; 8 broad policy-word hits reviewed; 0 high-confidence credential, key, token, credentialed-URI, private absolute-path, or sensitive-file hit |

## Final Decision

The corrected plan satisfies authority/provenance, earliest runnable outcome, promotion-trust
correctness, state/accessibility, candidate fairness, Barrier B, browser/measurement gates,
Security:S3, TDD/commands/evidence, and whole-plan traceability requirements. Remaining unknowns
are explicitly fail-closed execution gates.

**VALIDATION_VERDICT=PASS**
