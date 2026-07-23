# Issue #11 Stage A v3 Fresh Independent Plan Validation

## Verdict

**PASS** for plan validation after three bounded plan-only corrections. The corrected Stage A v3
plan is internally consistent, mechanically testable, scaffold-first, and traceable to all seven
PR #27 review findings. It grants no implementation authority. A fresh independent plan-readiness
audit of the exact pushed validation output is the only next phase.

This report does not claim Stage A is ready to cook, does not validate implementation behavior,
and does not authorize Stage B, portal, runner, data, cloud, container, AWS, or Terraform work.
The containing commit SHA is deliberately attested in the Issue #11 validation comment after the
commit is created and pushed; no future or self-referential SHA is placed in this artifact.

## Validation Identity and Runtime

| Item | Exact result |
|---|---|
| Repository | `khanhvg/ai-ready-data-platform` |
| Branch | `plan/issue-11-architecture-curriculum` |
| Independent validation input | `788ea45331a34e34b0d330e568a39ee6c6566e63` |
| Input equality | Local HEAD = upstream tracking ref = fresh live remote ref |
| Input state | Clean nonignored worktree before validator writes; Issue #11 OPEN with `ready for plan validation` |
| Author correction authority | Issue #11 comment `5047513123` |
| Review authority | PR #27 comment `5046838991` |
| Released integration | `fecf6bb8e5dfa7cc69f9766f72ac6f5b9301dad9` |
| Required clean future v3 base | `c07c9a080be7be88447aac497bdf0a2b5fddd020` |
| Runtime | Herdr `0.7.3`; Codex CLI `0.144.1`; `gpt-5.6-sol`; reasoning `xhigh` |
| Plan validator | ClaudeKit `4.5.2`; strict JSON result valid with zero issues; seven phases pending |
| Host feasibility sample | macOS arm64; 16 GiB physical memory; about 38 GiB free disk at validation time |
| Cloud/container actions | None |

The released integration is an ancestor of `c07c9a0…`. The failed v1 head `0f765d3…` and failed
v2 head `482591d…` are not ancestors of that base. The non-plan tree of `c07c9a0…` is identical to
the released integration, and its Issue #11 plan directory is the exact author-correction start
`1c62b681…` before the correction diff is applied. This establishes an unambiguous future input:
clean `c07c9a0…` plus only the eventual validation-and-readiness-passed plan diff.

## Independent Findings

| Severity | Finding | Resolution | Status |
|---|---|---|---|
| High | The four real RED behaviors were described but did not have closed public entrypoint IDs, per-family valid controls, or a closed exact outcome-code contract. A generic nonzero result could therefore masquerade as semantic RED. | Named `I11-EP-CURRICULUM`, `I11-EP-TRACE`, `I11-EP-EXPANSION`, and `I11-EP-HANDOFF`; required metadata-stripped valid controls and mutations; closed 82 unique exact codes across all 22 RED families. | Fixed |
| Medium | The Issue #8 Stage B status was stale and then the live integration ref advanced during validation, invalidating a literal `live == fecf6bb8…` hard stop. | Recorded merged PR #28 object `5644f01b4c0443a81f3af0bcce80f44c847cd986`, its `fecf6bb8…` first parent, absent post-merge release handoff, and exact zero overlap with the 50 future paths, 33 protected identities, and 21 pinned contract paths. The plan now pins the released object while classifying later live deltas. | Fixed |
| Medium | The exact 16 top-level commands did not fully close child-process/tool admission inside the resource controller. | Closed fixed-argv Python, `/bin/ps`, Node archive/hash, npm install flags, LikeC4, and I5-06 adapter/validator children; prohibited shell text and alternate executables. | Fixed |

No Critical or unresolved High/Medium/Low finding remains. Corrections are restricted to the
current Issue #11 plan and validation artifacts. Historical v1/v2 evidence and reports remain
unchanged.

## Scaffold-First TDD Validation

The final tracked scope partitions exactly and without overlap:

| Chronology | Count | Validation result |
|---|---:|---|
| Public semantics-free scaffold | 7 | Real callable parsing, routing, bounded process, evidence, Make, and content I/O entrypoints; no target rules, hardcoded outcomes, fixture IDs, expected-code echo, or fixture-specific branches |
| Complete direct-child tests and invalid fixture catalogue | 5 | Four test paths plus one fixture path; each RED family supplies a parseable valid control and one or more mutations |
| Semantic complement after recorded RED | 38 | Curriculum, templates, content, trace, render, evidence, and final semantics only after RED |
| Final create-only scope | 50 | Unique, absent at released integration, clean v3 base, and validation input |

RED invokes all four named public callables through the scaffold. The harness removes RED IDs,
expected codes, fixture locators, and assertion text before invocation. A valid control must parse
and reach its callable. Each mutation must initially fail because its named semantic rule is absent,
not because of a missing tool/path/import, an unconditional not-implemented return, expected-value
echo, mock, skip, generic behavior-absent guard, or fixture-specific branch. Final invalid-case
success requires the exact stable code; a generic nonzero or wrong code fails.

Evidence binds the plan input, scaffold commit, tests commit, tested tree, callable ID, reached
preconditions, valid-control result, mutation outcome, exact expected code, released dependency
identities, tool identities, and protected 33/33 state. The scaffold/tests/semantic ancestry and
first-semantic-commit relationship are explicit and cannot be substituted by a future SHA.

## Seven Review Findings

| Finding | Precise acceptance and tests | Blocking command/evidence | Rollback |
|---|---|---|---|
| RF-01 genuine scaffold-first RED | 7/5/38 chronology; four exact callable IDs; 22 valid-control/mutation families; exact codes | `architecture_expansion run-focused-tests`; RED reach and ancestry records | Remove only run-owned scaffold/test attempt and return to exact authorized input |
| RF-02 frozen promotion semantics | Decision `insufficient-evidence`; reason `no-common-grain`; independent drift mutations against the released schema constants | `curriculum-check`; promotion fixture outcome, schema identity, and separate evidence-version decision | Reject output; do not infer learner evidence or promotion authority |
| RF-03 complete template bindings | 12 templates; schema/version/compatibility/supersession/removal rules; reciprocal per-instance hashes | Curriculum/template tests and traceability check; template registry and instance hash evidence | Reject affected instance/registry; no partial publication |
| RF-04 critical-flow meaning | 11 distinct critical flows bound to dynamic/deployment topology; eight conceptual-only bridges with divergence and no runtime claim | Trace/flow/topology/bridge tests; `traceability-check`; source/render parity evidence | Reject changed expansion/content; preserve protected six-view base |
| RF-05 bounded controller | Exact 120-second focused-test and 180-second two-install/two-render deadlines; PGID TERM/KILL/reap; RSS/output/file/process controls | Controller resource mutations and process/resource evidence | Kill/reap owned process group, remove owned runtime/evidence bytes, preserve external state |
| RF-06 honest visuals | Vietnamese-first; no double numbering; readable fitted SVG at 1440 and 1024; geometry, text parity, contrast, language, accessibility | Deterministic visual tests plus `verify-expansions`; separate required human inspection record | Reject render set and restore only run-owned renders; never synthesize human approval |
| RF-07 truthful evidence and cleanup | External or app-owned ignored evidence only; privacy/index/hash/ownership controls; nonignored porcelain empty and ignored-inclusive status classified | `clean-handoff`; evidence/index/privacy and cleanup mutations; ignored-inclusive status evidence | Remove only run-owned evidence/runtime; never delete pre-existing ignored or external bytes |

Result: **7/7** review findings map to acceptance criteria, invalid and valid controls, exact command
or controller entrypoints, evidence, and rollback.

## Machine-Testability and Honest Human Gate

The plan closes 82 unique stable semantic outcome codes across exactly 22 RED families. It supplies
valid controls, invalid mutations, protected-identity controls, render mutation controls,
process/resource controls, evidence index/privacy/ownership controls, S3 controls, and rollback
checks. No gate is satisfied by naming a command without defining its observable result.

Automated rendering checks remain blocking for deterministic SVG dimensions, fitted font size,
aspect/canvas bounds, overlap, clipping, WCAG contrast, Vietnamese-first text, duplicate numbering,
accessibility metadata, and source/render text parity at both required widths. Human visual
inspection is separately required and separately evidenced. This validation confirms that the
future gate is explicit; it does not fabricate or replace the future human inspection.

## Scope, Release, Security, and Rollback

| Check | Result |
|---|---|
| Final tracked paths | 50/50 unique create-only paths; exact 7/5/38 partition |
| Top-level command shapes | 16/16 unique; internal children closed separately |
| Protected identities | 33/33 exact Git blob and SHA-256 identities at released integration, clean v3 base, and validation input |
| Released Issue #8 contract set | 21/21 descriptor paths and hashes; 16/16 operation IDs agree with OpenAPI |
| Released Stage A/OpenAPI/Make/golden data | Read-only and protected; no edit authority |
| Future path absence | All 50 absent at `fecf6bb8…`, `c07c9a0…`, and `788ea453…` |
| Issue #8 Stage B change | Merged as `5644f01b…`, but not post-merge release-verified at validation time; non-overlapping, unconsumed, and non-authoritative for Issue #11 |
| Issue #10 / Stage B | Issue #10 remains blocked; Stage B path, command, dependency, and renderer lists are empty |
| Excluded scope | No portal, runner, executable lab, reset, progress, completion, data, cloud, container, AWS, or Terraform authority |
| S3 | 14/14 catalogue rules cover secret-like content, private paths, external URLs, cloud-action tokens, evidence privacy, and bounded negative controls |
| Rollback | PGID-scoped process cleanup; run-owned-path deletion only; protected identities rechecked; external/pre-existing ignored evidence preserved |

Every standalone 40-hex identity in the plan resolves to an existing Git object: 24 commits, 61
blobs, and two trees. No plan artifact invents a future commit SHA or digest. The future validation
output and readiness-derived implementation input remain externally bound values, never predicted
placeholders.

## Resource and Dependency Feasibility

The validation host has 16 GiB physical memory and about 38 GiB free disk. The future plan admits
one controller child at a time, a maximum 1.5 GiB aggregate RSS, and a maximum 2.5 GiB owned runtime
and evidence footprint. Node and Python installs are sequential, all render work stays inside the
single 180-second controller, and focused tests use the separate 120-second controller. The plan
requires no VM, container, browser, cloud service, Terraform provider, or local database.

Python `3.12.3`, Node `22.22.3`, npm `10.9.8`, and `/bin/ps` were present during validation. The
plan pins the Node archive name and SHA-256, protected package/Python lock hashes, LikeC4 version
and subcommands, exact npm flags, executable admissions, timeouts, RSS/output/file/process bounds,
and failure evidence. This is feasible on the sampled 16 GiB Mac without relying on an unbounded
tool download or an unadmitted child process.

## Whole-Plan Strict Sweep

The validator reread `plan.md`, all seven phase files, the Stage A amendment, the five companion
contracts, and this current report. The full-tier matrix checked 15 claims per phase, 105 claims in
total, plus cross-phase catalogue, identity, link, ancestry, scope, security, resource, rollback,
and Git/GitHub state checks. Verified: 105. Failed: 0. Unverified: 0.

- ClaudeKit strict JSON: valid, zero issues, seven phases.
- ClaudeKit status JSON: seven pending phases, zero completed or in progress; this is expected
  because validation does not grant implementation authority.
- Markdown: one H1 per current plan artifact; relative links and anchors resolve; no unresolved
  authoring placeholder.
- Git diff: only current Issue #11 plan/validation artifacts; no protected/product/test/other
  worktree change; `git diff --check` clean.
- Input and dependency state: exact plan branch/input/upstream/live equality; pinned released
  integration and v3 ancestry proven; later live merge classified with zero 50/33/21 overlap; all
  future paths absent; failed v1/v2 evidence unchanged.
- Worktree truth: nonignored input state was clean. Existing ignored Herdr runtime records and one
  Python bytecode cache were identified and ownership-classified; they are not product evidence,
  are not staged, and are not claimed as clean because porcelain omitted them.

## Final Disposition

Plan validation passes after the bounded fixes above. The output commit must be pushed and proven
equal across local HEAD, upstream tracking, and the fresh live remote, then attested in Issue #11.
On that proof, the workflow label moves from `ready for plan validation` to
`ready for plan audit`. The next actor must be a fresh readiness auditor. Stage A implementation
authority remains `none`, and Stage B remains blocked.
