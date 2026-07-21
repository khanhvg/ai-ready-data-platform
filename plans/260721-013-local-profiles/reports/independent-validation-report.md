---
title: "Issue #13 Fresh Independent Plan Validation"
status: pass-with-fixes
issue: 13
branch: "plan/issue-13-local-profiles"
inputSha: "a23a0b77ac06dd6635f3b6a250432783cb9e2e04"
shippedBaselineSha: "24be3b34c6b0fcdbd07c5800dcab349054e34713"
date: "2026-07-22"
scope: "plan-validation-only"
---

# Issue #13 Fresh Independent Plan Validation

## Summary

Verdict: `PASS_WITH_FIXES`. Seven objective plan defects were corrected inside
`plans/260721-013-local-profiles/**`; no product, Compose, root Make, shared contract, portal,
runner, lab, golden, cloud or other worktree path was changed. This is not a readiness audit and
does not authorize implementation, container operations, a PR or a merge.

Stage A remains blocked on a passing merged Issue #10 journey and released/admitted Issue #12
labs plus exact image/lab/command/completion/allowlist authorities. Stage B remains blocked on the
exact Stage A head and admitted engine/images/toolchain. Every current authority-ledger value
remains `EMPTY`.

## Input and Live-State Proof

| Check | Result |
|---|---|
| Worktree | Exact requested Issue #13 worktree only |
| Branch | `plan/issue-13-local-profiles` |
| Clean local/tracking/fresh remote before validation | All `a23a0b77ac06dd6635f3b6a250432783cb9e2e04` |
| Shipped baseline | Parent `24be3b34c6b0fcdbd07c5800dcab349054e34713` |
| Planner comment | `PLANNER_ONLY_NOT_VALIDATED`, exact referenced comment observed |
| Issue #13 | Open; `ready for plan validation`; required risk/TDD/S3/performance/compose labels present |
| Issue #10 | Open; `ready for plan audit`; no passing merged journey authority |
| Issue #12 | Open; `ready for plan audit`; no released/admitted lab authority |

## Verification Results

- Tier: Full, five phases, 92 claim assertions checked.
- Roles: Fact Checker, Flow Tracer, Scope Auditor and Contract Verifier.
- Before correction: Verified 85 | Failed 7 | Unverified 0.
- After correction: Verified 92 | Failed 0 | Unverified 0.
- Questions asked: 0. The user's validation directive supplied the decisions that the normal
  validation interview would otherwise confirm.

The per-phase sampling met the Full-tier minimum:

| Phase | Claims checked | Principal verified contracts |
|---:|---:|---|
| 1 | 20 | exact ancestry; open dependencies; three profiles/nine services; exact images, ports, volumes, health/dependency closure; core and scale characterization; hashes and empty authorities |
| 2 | 18 | behavior-specific RED structure; invalid/missing/duplicate/unknown/all-three/over-budget/closure/collision/limit/security/evidence/engine/foreign-sentinel cases; pre-runner denial |
| 3 | 18 | single policy source; Compose-policy equality; exact singles/pair/all-three rules; reserve math; supported Make boundary; protected root/shared/golden paths; Stage A no-start boundary |
| 4 | 18 | exact Stage A/engine/image/tool entry; four actual scenarios; one cold/two warm; normalized layered metrics; no-pull acceptance; capped raw/summary evidence; honest engine block |
| 5 | 18 | ownership manifest/labels/nonce; idempotent foreign-safe teardown; current/N-1/tamper/replay; four future commands and exact dependency/golden blast radius; rollback; exact-head human approval |

## Static Checks

| Gate | Result |
|---|---|
| `ck plan validate ... --strict` | PASS; five phases, zero errors/warnings |
| Compose v5.1.2 static render | PASS; no engine lifecycle call |
| Profiles/services | PASS; `orchestration`, `lake`, `governance`; exactly nine actual services |
| Closure | PASS; singles, exact `lake+governance` union, and all-three render match inventory |
| Config inventory | PASS; exact current images/build, five volumes, published ports, healthchecks, dependencies and memory limits |
| Docker-free Make dry-run | PASS; `health dbt bi` closure contains no Docker/cloud/socket/sudo/privilege command |
| Future command authority | Correctly absent; dry-run stops at missing `compose-check`, consistent with `future-owner/not-runnable` registry rows |
| Local links/phase dependencies | PASS |
| Protected named hashes | PASS |
| Protected 307-file aggregate | PASS; `bf5ac7969dc039d19051cff5c3d8bad84102887451eb9409082b8ecaa65ae5b4` reproduced from baseline blobs and checkout bytes |
| Placeholder/stale authority | PASS; no unclassified placeholder or guessed authority; schema locator variables are explicit; all 12 implementation authorities remain `EMPTY` |
| Threshold arithmetic | PASS; singles `4/4`, `3.25/2.5`, `4/3.5` GiB/CPU; pair `7.25/6`; denied all-three `11.25/10`; host reserve formulas complete |
| Per-service bounds | PASS; memory/CPU/PID/disk/log/start/stop plus single/pair parent teardown ceilings are deterministic |
| Traceability | PASS; 5 characterization IDs + 22 stable RED IDs, including explicit over-budget, port, volume, engine and foreign-sentinel mappings |
| Scope/diff | PASS; Issue #13 plan/validation paths only |

## Objective Findings and Fixes

1. The protected 307-file aggregate did not reproduce from its documented algorithm. Replaced it
   with the reproducible value and made the byte/order algorithm explicit.
2. Several exact image strings were abbreviated in the inventory. Recorded the rendered image
   strings verbatim while retaining their non-authoritative tag-only classification.
3. Per-service start/readiness existed, but per-service stop and parent teardown ceilings were not
   explicit. Added deterministic service, single-group and guarded-pair ceilings.
4. Engine lower bounds existed, but engine allocation itself was not bounded to preserve the
   4 GiB/2 CPU host reserve. Added exact upper-bound formulas and kept engine overhead observed,
   never invented.
5. Evidence streams were described as bounded but had no practical deterministic bundle/sample
   caps. Added sample, raw stream, derived document, command stream and 512 MiB total caps.
6. Over-budget behavior lacked its own stable RED ID and exact traceability. Added
   `LP-BUDGET-OVER-AGGREGATE-022` and mapped collision IDs explicitly.
7. Human approval was mandatory but not bound strongly enough to the exact final head/evidence.
   Bound approval to the exact clean head and completed evidence index hash; later commits require
   renewed review.

## Acceptance-Criteria Disposition

| # | Disposition |
|---:|---|
| 1 | PASS — inventory derives from actual Compose/config bytes; no invented service/image/profile; core and scale contracts protected |
| 2 | PASS — static configured limits primary; aggregate, host reserve, service and lifecycle ceilings consistent |
| 3 | PASS — one cold plus two warm sequential runs, normalized layered metrics, no flaky score/matrix |
| 4 | PASS — Docker-free core independent; missing engine blocks required heavy acceptance; optional status cannot release |
| 5 | PASS — fail-closed grammar/closure/budget/collision/ownership checks; exact guarded pair only |
| 6 | PASS — exact Stage A/B dependency split, amendment/revalidation/readiness gates, no implementation authority |
| 7 | PASS — characterization-first genuine TDD with stable behavior IDs and required engine/foreign sentinels |
| 8 | PASS — S3 interpolation, shell, supply chain, secrets/PII, host, path/resource, evidence and teardown threats covered |
| 9 | PASS — released evidence authority deferred; strict capped raw/summary/index/rollback and owner-only cleanup contracts |
| 10 | PASS — four future commands plus exact #10/#12/golden blast radius; protected root/shared/portal/runner/lab/cloud boundaries |
| 11 | PASS — human approval is mandatory at the exact final clean head and evidence index |

## Whole-Plan Consistency Sweep

- Files reread: `plan.md`; all five phases; `inventory.md`;
  `requirements-and-traceability.md`; `resource-model.md`; `threat-model.md`;
  `tdd-fitness-evidence-recovery.md`.
- Decision deltas checked: 7 defect classes.
- Reconciled stale references: all affected phase, requirement, TDD, resource, threat, inventory
  and validation-status references.
- Unresolved contradictions: 0.

## Recommendation

Transition Issue #13 from `ready for plan validation` to `ready for plan audit` after the
validation-only commit is pushed and local/tracking/fresh-live heads are equal and clean. The next
phase is a fresh dependency-aware readiness audit, not implementation.
