---
type: independent-plan-validation
issue: 9
date: "2026-07-22"
inputSha: "5cea5ce248b49ff8741af1b1e65f8ac2eb64698f"
releasedStageASha: "fecf6bb8e5dfa7cc69f9766f72ac6f5b9301dad9"
verdict: PASS
readiness: READY_FOR_DEPENDENCY_AUDIT
cloudAction: none
---

# Independent Validation of the Issue #9 Release Amendment

## Verdict

`PASS`. The amended six-phase plan is structurally valid, internally consistent, dependency-bound,
TDD-first, and closed to Issue #9 ownership. The former unreleased-dependency facts are replaced by
the exact released Stage A identities. No implementation, source/config/data, shared contract,
runtime artifact, PR/merge, credential, AWS/Terraform, container, or cloud action was performed.

The requested `$ck:plan-to-cook` convenience skill was not exposed. The validation used the
workflow-equivalent CK plan skill, Full-tier Fact Checker / Flow Tracer / Scope Auditor / Contract
Verifier review, strict CK CLI validation/status, and deterministic closure scans.

## Immutable Inputs and Release Proof

| Check | Result |
|---|---|
| Required worktree / branch | exact Issue #9 worktree; `plan/issue-9-privileged-local-runner` |
| Clean starting local/upstream/live plan head | `5cea5ce248b49ff8741af1b1e65f8ac2eb64698f` |
| Fresh integration ref | `fecf6bb8e5dfa7cc69f9766f72ac6f5b9301dad9` |
| Release tree | `27fc3667ef37892dad5c3fbfd76769f65a0760be` |
| PR #23 merge ancestry | `5c2244c2c860234d0df49cf0a42ad950c6495717` is release parent/ancestor |
| PR #25 second parent | `734cf637a20ae186597e23d96a194ed4e30220ea` |
| Stage A release evidence | [Issue #8 release comment](https://github.com/khanhvg/ai-ready-data-platform/issues/8#issuecomment-5043195549) |
| Released checks | `56/56`; `65/65`; 16 operations; `4/4`; inherited `19/19 + 1/1 + 13/13` |

All authoritative release reads and SHA-256 recomputation used exact Git-object bytes from
`fecf6bb8e5dfa7cc69f9766f72ac6f5b9301dad9`. The feature worktree and ignored artifacts were not
used as contract authority.

## Objective Corrections and Propagation

1. Replaced the historical absent-release blocker with the exact release SHA/tree/parents,
   handoff, verification counts, and current integration identity.
2. Expanded Phase 2 to an exact 38-path read-only SHA-256 pin set covering the contract set,
   version and command-owner registries, activation, operation/OpenAPI/problem, lab/lesson/
   manifest, completion/state/progress/evidence, canonicalization, Make input, released readers,
   checker, and Make fragment. All pins reproduce.
3. Recorded that Stage A has no type-generation command or output authority. Direct released
   readers are mandatory; generated bindings are denied.
4. Resolved the runner-owned activation path as
   `apps/lab-runner/config/command-owner-activation-i5-04-v1.json` and the private pre-parse body
   limit as exactly 16,384 bytes. Future file/head hashes are measured after bytes exist, never
   guessed.
5. Reconciled the public OpenAPI profile with the stricter private runner IPC boundary: the runner
   is not a browser-facing OpenAPI server; Issue #10's BFF owns later public mapping.
6. Moved real Make-target/gate scaffolding into Phase 3 so every RED assertion is contemporaneous,
   reaches a named fixture marker through a public runner Make target, and is committed before any
   Phase 4/5 production behavior.
7. Reconciled Phase ownership language: Phase 5 extends race tests created RED in Phase 3; Phase 6
   extends the Phase 3 gate/Make scaffolding and Phase 5 evidence module.

## Full-Tier Validation Matrix

| Role | Evidence checked | Result |
|---|---|---|
| Fact Checker | README/docs, Issue #9 and #8 records, released Git ancestry/tree/bytes, host tuple, Make/Airflow/data seams | PASS |
| Contract Verifier | 21-entry contract-set closure, 38 pinned interfaces, exact readable/current matrix, 16 operations, 8 commands, completion/state/evidence readers | PASS |
| Flow Tracer | Six ordered phases, public RED-before-behavior, GREEN, fencing/release, S3/evidence/rollback/review handoff | PASS |
| Scope Auditor | 66 exact absent future creates, 50 present read-only inputs, one narrow present modify seam, denied shared/root/portal/cloud paths | PASS |

Catalog closure is exact: 20 `RUN-*` requirements, 15 `THR-*` threats, 44 stable `RED-*`
assertions, and 9 required `S3-*` scan rows. No active amendment file contains an unresolved
planning marker, synthesized SHA, or generated-binding admission.

## Lease and Ownership Validation

The latest Issue #8 Stage B handoff is [blocked with no output or amended path](https://github.com/khanhvg/ai-ready-data-platform/issues/8#issuecomment-5043335319).
Issue #9 reads released Stage A bytes and has no shared-contract write. Therefore there is no real
write overlap. A future actual overlap remains an immediate STOP. The exact write boundary stays:

- `apps/lab-runner/**`;
- `mk/issue-5/i5-04.mk`; and
- only the characterized pre-`_run` Airflow learner-namespace refusal if Phase 1 still proves it
  necessary.

Root Make, portal, shared contracts, golden core, data semantics, other issue plans/fragments,
cloud/Terraform, and container paths are denied.

## Structural and Deterministic Checks

- `ck plan validate ... --strict`: PASS, 0 errors, 0 warnings, 6 phases.
- `ck plan status ...`: PASS, plan pending, 0/6 complete as expected before cook.
- Released contract-set embedded SHA closure: PASS, 21/21 plus registry pointer.
- Phase 2 release-pin closure: PASS, 38/38 unique exact paths/hashes.
- Exact path classification: PASS, 66 future creates absent, 50 read-only inputs present, one
  existing modify seam present.
- Requirement/threat/RED/S3 catalog uniqueness and counts: PASS (`20/15/44/9`).
- Local Markdown paths/anchors, placeholder/future-SHA, private-path/credential, S3 boundary,
  protected scope, diff, and whole-plan stale-term scans: PASS.
- Current amended artifact SHA-256 closure is recorded separately in
  `release-readiness-sha256.txt`; the historical `artifact-sha256.txt` remains bound to its
  historical Git input.

## Validation Decision

The plan is eligible for a dependency-aware readiness decision. This validation does not prove
future containment, process cleanup, RED/GREEN behavior, gate results, or release approval; those
remain exact phase and pre-merge gates.
