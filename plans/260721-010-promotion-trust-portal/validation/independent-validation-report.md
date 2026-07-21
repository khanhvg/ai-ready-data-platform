---
issue: 10
validation: independent-initial
verdict: PASS_WITH_FIXES
inputSha: ad87c3f6090129dd30cfb626c6f396567f567a42
integrationBaseSha: 24be3b34c6b0fcdbd07c5800dcab349054e34713
branch: plan/issue-10-promotion-portal
readiness: dependency-blocked
stageA: issue-7-merged-vite-and-issue-8-released-stage-a
stageB: issue-9-released-runner-sha
date: 2026-07-22
---

# Independent Validation Report — Issue #10 Promotion-Trust Portal

## Summary

**Verdict: PASS_WITH_FIXES, not readiness.** Eight objective plan defects were corrected and no
plan-validity blocker remains. No implementation, portal/test/config execution, readiness audit,
PR, merge, cloud action, or dependency contract was created.

Implementation remains fail-closed. Issue #7 has no merged Vite handoff, Issue #8 has no released
Stage A contract, and Issue #9 has no released runner. Stage A and Stage B file, command, and
consumable dependency SHA allow-lists are therefore all `[]`. A later amendment must pin real
handoffs and derived allow-lists, then pass fresh independent revalidation and dependency-aware
readiness before cook.

## Frozen Input and Independence

| Check | Result |
|---|---|
| Workspace | Exact requested Issue #10 worktree only; local machine path intentionally not persisted |
| Branch | `plan/issue-10-promotion-portal` |
| Local HEAD | `ad87c3f6090129dd30cfb626c6f396567f567a42` |
| Tracking HEAD at start | `ad87c3f6090129dd30cfb626c6f396567f567a42` |
| Fresh-live branch head at start | `ad87c3f6090129dd30cfb626c6f396567f567a42` |
| Initial tree | clean |
| Issue | #10 OPEN with `ready for plan validation`, `risk:high`, `tdd`, `security:S3`, `frontend`, `accessibility`, `vertical-slice` |
| Planner comment | `5036850618`, exact `PLANNER_ONLY_NOT_VALIDATED` input |
| Owner Vite decision | Comment `5036142177`; direction only, not unmerged-SHA authority |
| Workflow | `ck:plan validate` workflow plus exposed `ck plan validate --strict`; Full-tier verification |

The ten decisions in the validator invocation were treated as explicit owner answers. No
duplicate interview question was needed; zero unresolved business/architecture choices remain.

## Fresh Dependency State

| Dependency | Live state observed | Consumable release | Consequence |
|---|---|---|---|
| Issue #7 | OPEN, `ready to cook` | none | Stage A blocked; audited cook input is not a merge |
| Issue #8 | OPEN, `ready for plan audit` | none | Stage A blocked; no released completion/evidence/browser contract |
| Issue #9 | OPEN, `ready for plan audit` | none | Stage B blocked; no released private runner contract |

No merged PR or owner release record for #7/#8/#9 was accepted as a dependency. Historical or
planning heads are provenance only and are absent from the stage dependency allow-lists.

## Corrected Findings

| ID | Severity | Defect | Correction |
|---|---|---|---|
| IV-01 | Critical | Detailed Stage A/B module and test paths acted as premature file authority | Removed concrete inventories; every phase now declares file authority `[]` until exact-SHA amendment + revalidation + readiness |
| IV-02 | Critical | `fitness-result-v1` was treated as a usable I5-05 runtime fallback although #8 owns the future portal completion/evidence release | Kept the current v1 hash as read-only provenance only; runtime must pin the exact portal-compatible #8 release with no fallback/version invention |
| IV-03 | High | Dependency document carried stale #7/#8 live labels and non-release heads | Rechecked live state on 2026-07-22; recorded state without adding candidate SHAs to authority |
| IV-04 | High | Exact internal routes, module names, runtime mode, generated binding filename, and fixed viewport literals were frozen before #7/#8 releases | Deferred all such literals to a later release-derived amendment |
| IV-05 | High | Empty consumable dependency-SHA authority was implied but not explicit | Added normative Stage A/B dependency SHA allow-lists `[]` and `cookable: false` |
| IV-06 | High | #8/#9 version negotiation, CAS, response-loss, crash/retry, reset, error, unavailable, and evidence-handle semantics were scattered | Added one release-time semantic-closure gate without inventing fields, statuses, routes, or versions |
| IV-07 | High | Immutable issue-body Make acceptance commands could be mistaken for current command authority | Preserved exact commands as acceptance only; current command allow-lists are `[]`; later fragment targets must resolve and fail closed on missing stage dependencies |
| IV-08 | Medium | Planner-only validation state and phase handoff text were stale after corrections | Added validation input/log, phase propagation, whole-plan sweep, and `INDEPENDENT_VALIDATION_PASS_NOT_READINESS` boundary |

## Outcome and Requirements Traceability

| Validator requirement | Plan evidence | Validation disposition |
|---|---|---|
| Outcome/capability/FR/NFR/architecture/threat/test/evidence/operations | `plan.md`; `requirements-and-risk-traceability.md`; `architecture-and-api-boundaries.md`; `threat-model-and-security.md`; `verification-evidence-and-uat.md` | Complete, linked, and internally consistent |
| Runner-independent non-completing Stage A | Plan Stage Claims; Gate A Claim Boundary; phases 1–4 | Static/read-only lesson, navigation, fallback, and honest unavailable state only |
| Stage B-only real journey | Exact Journey Data Flow; phases 5–7 | Controlled failure → four grain-honest marts → exact decision → reset → fresh verified evidence; browser never reaches privilege |
| Simple Vite modular monolith/BFF | Architecture Decision and Performance Shape | One portal/BFF, one private runner later, local/core-only; no service comparison/distributed/cloud addition |
| One #8 completion authority and private #9 runner | State Authority; Release-Time Semantic Closure; Phase 5 | Exact releases required; no local replacement or duplicate progress/evidence truth |
| TDD and practical tests | Tests-Before Matrix and Practical Test Portfolio | Stable RED IDs; focused unit/contract/security/a11y; one Chromium desktop+narrow; axe Critical/Serious; no-JS; recovery; one real journey |
| S3 security | PTP-S3-01..14, HTTP/XSS/storage/evidence/environment sections | Host, Origin, CSRF, CSP, XSS, storage, evidence hash/download/path/injection/secret/PII and no ambient privilege covered |
| Exact Make/cleanup/rollback | Exact Issue Command Contract; Retention/Cleanup; Phase 7 | Root Make unchanged; issue fragment is sole seam; missing dependencies fail closed; only owned runtime removed; evidence retained |
| Empty stage authority until releases | Dependency Gate empty-authority table; all seven Related Code Files sections | Stage A and B file/command/dependency SHA allow-lists all `[]`; no future SHA literal |
| Human and independent gates | Plan Exit; Release Gate; Phase 7 | Fresh exact-head independent review and named human pre-merge approval remain; no CI/cloud expansion |

## Full-Tier Verification

Seven phases require Full tier. Fifteen claims per phase were checked (105 total) using all four
verification roles. Each phase was also required to retain the 15 structural/behavioral sections
and the correct empty stage authority.

| Phase | Fact Checker | Flow Tracer | Scope Auditor | Contract Verifier | Total | Result |
|---|---:|---:|---:|---:|---:|---|
| 1 — Stage A release gate | 4 | 4 | 3 | 4 | 15 | verified |
| 2 — Stage A foundation | 4 | 4 | 3 | 4 | 15 | verified |
| 3 — Stage A static lesson | 4 | 4 | 3 | 4 | 15 | verified |
| 4 — Stage A handoff | 4 | 4 | 3 | 4 | 15 | verified |
| 5 — Stage B runner/BFF gate | 4 | 4 | 3 | 4 | 15 | verified |
| 6 — Stage B real journey | 4 | 4 | 3 | 4 | 15 | verified |
| 7 — Stage B release/rollback | 4 | 4 | 3 | 4 | 15 | verified |
| **Total** | **28** | **28** | **21** | **28** | **105** | **105 verified; 0 failed; 0 unverified** |

Fact checks included source paths, issue labels/comments, root Make include seam, command-owner
registry, Issue #6 hashes/blobs, exact commands, and absent current portal/fragment paths. Flow
traces covered Stage A non-completion and Stage B start/failure/decision/reset/verify/evidence/
completion/recovery. Scope checks covered empty stage authority, exclusive ownership, protected
paths, cleanup, and no cloud/CI/root-Make writes. Contract checks covered exact-release gates,
single #8 authority, private #9 boundary, closed versions/idempotency/CAS/errors, evidence
integrity, and all callers represented by the fixed Make acceptance surface.

## TDD, Security, Evidence, and Operations Gates

- RED IDs cover dependency/contract, component/state, grain honesty, non-completion, history,
  no-JS, unavailable/environment failure, accessibility, S3, private runner, crash/retry,
  idempotency, reset, evidence integrity, real journey, and lifecycle cleanup.
- PTP-S3-01..14 are exact negatives for session, Host/DNS rebinding, Origin/CSRF, browser-direct
  runner, injection, XSS, artifact traversal/type, completion tamper, replay/race, sensitive
  output/PII/private paths, supply chain, cleanup, contract downgrade, and ambient cloud/model
  credentials.
- Issue #6 data hashes and Git blobs were recomputed and match all seven preservation anchors in
  `requirements-and-risk-traceability.md`.
- Four marts remain exactly: promotion 7 rows at `(promo_name, channel)`; fulfillment 25 at
  `(carrier, region_name)`; returns 47 at `(reason, category_name, region_name)`; data quality 10
  at `(scenario)`. The only decision is `insufficient-evidence / no-common-grain`.
- Evidence root remains `.artifacts/evidence/local-journey/{run-id}/`; schema/version is deferred
  to exact released #8. Hashes are local corruption detection, not authenticity/non-repudiation.
- Cleanup/status/down validate owned namespace, PID/start identity/process group and symlink/path
  boundaries, revoke temporary secrets, preserve committed evidence, and never remove foreign or
  repository state.

## Exact Acceptance Commands

The issue-body commands remain byte-for-byte present as the future Stage B acceptance surface:

```bash
make portal-test portal-a11y
make lesson-e2e LESSON=promotion-trust
make local-journey-e2e
make portal-visual-review
make learn-status
make learn-down
```

`make learn LESSON=promotion-trust` remains lifecycle acceptance. The root `Makefile` already
includes `mk/issue-5/*.mk`; only `mk/issue-5/i5-05.mk` may eventually define Issue #10 targets.
Because the implementation command allow-lists are currently empty, none was executed here.

## Strict Checks

| Check/command | Result |
|---|---|
| `ck plan validate plans/260721-010-promotion-trust-portal/plan.md --strict` | PASS; 7 phases, 0 errors, 0 warnings |
| `ck plan status plans/260721-010-promotion-trust-portal/plan.md` | PASS; 7 pending phases, branch exact |
| Full-tier phase structure/authority check | PASS; 105/105 claims, 0 authority failures |
| Cross-plan semantic check | PASS; 15/15 critical claims |
| Local Markdown path/anchor scan | PASS; 54 links, 0 failures |
| SHA-256 + Git-blob recomputation for seven Issue #6 anchors | PASS; 7/7 exact |
| Future dependency SHA/placeholder scan | PASS; none |
| Stale non-release dependency-head scan | PASS; none in authority |
| Exact issue command/order scan | PASS |
| Root Make/include/registry path check | PASS; no root edit |
| Candidate module/route/viewport literal scan | PASS; none retained as implementation authority |
| `git diff --check` | PASS |
| Changed-path scope check | PASS; Issue #10 plan/validation artifacts only |

## Whole-Plan Consistency Sweep

Re-read `plan.md`, all seven phase files, and all five companion contracts after corrections.
Eight decision deltas were checked across overview, dependencies, architecture, phase
requirements, implementation steps, regression gates, success criteria, risks, and validation
log. Thirteen plan files were reconciled. No stale module/route/viewport authority, no runtime
`fitness-result-v1` fallback, no non-release dependency head in an allow-list, and no unresolved
contradiction remains.

## Disposition

- Plan validation: PASS_WITH_FIXES.
- Readiness: not run and still dependency-blocked.
- Stage A dependencies: exact merged Issue #7 Vite handoff plus released Issue #8 Stage A.
- Stage B dependency: exact released Issue #9 runner SHA, compatible with the pinned #8 release.
- Current Stage A/B file, command, and dependency SHA allow-lists: `[]`.
- Next phase: fresh dependency-aware readiness audit, which must remain blocked until a later
  exact-release amendment is independently revalidated.
- Human exact-head pre-merge approval and fresh independent implementation review remain real
  gates. No CI workflow, cloud, AWS, Terraform, PR, merge, implementation, or readiness action was
  performed.
