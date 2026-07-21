---
title: "Issue #8: Version lesson, lab, progress, and evidence contracts"
description: "TDD plan for a framework-neutral learning-contract release followed by an exact-SHA-gated Vite binding, with an Issue #8-owned additive version overlay and no second completion authority."
status: pending
priority: P1
issue: 8
branch: "plan/issue-8-version-learning-contracts"
tags: [feature, api, shared-core, contracts, tdd, security-s3, migration]
blockedBy: []
blocks: []
created: "2026-07-21"
createdBy: "ck:plan"
source: skill
planningMode: "issue-pipeline-staged-tdd-planner-only"
inputSha: "24be3b34c6b0fcdbd07c5800dcab349054e34713"
plannerBoundary: "PLANNER_ONLY_NOT_VALIDATED"
validationInputSha: "93837667326cb7a298c21921ac04e602ea7313d0"
validationBoundary: "INDEPENDENT_VALIDATION_PASS_NOT_READINESS"
validationReport: "validation/independent-validation-report.md"
---

# Issue #8: Version lesson, lab, progress, and evidence contracts

## Outcome

Plan the full I5-03 contract release from the shipped Issue #6 integration input. Stage A creates
the framework-neutral JSON Schema, validation, state, evidence, OpenAPI, migration, first-manifest,
and Make surfaces. It also adds the minimum Issue #8-owned `fitness-result-v2` extension required
because shipped `fitness-result-v1` is closed to `owner: I5-01`; the shipped registry, fixture and
reader bytes remain unchanged.
Stage B binds immutable Stage A outputs to the owner-selected web stack only after Issue #7
publishes an accepted Vite ADR/handoff at an exact merged SHA.

This directory is a planning artifact only. It does not validate or audit itself and authorizes no
implementation, contract/config change, cook, PR, merge, label beyond the requested planning-state
transition, cloud action, Terraform action, destructive migration, or synthetic human approval.

## Stage Decision

| Stage | Scope | Dependency | Planner assessment |
|---|---|---|---|
| A — framework-neutral contract core | Phases 1-5 | Shipped Issue #6 input only | **Validated framework-neutral candidate, not readiness.** Independent validation confirms the corrected plan has no selected-framework, Issue #7 ADR-byte, portal/runner-internal, or future-SHA input. Only a fresh readiness audit may authorize a bounded cook/merge scope; implementation evidence, independent exact-head review, repository checks, and human exact-head approval still follow. |
| B — selected-web-stack binding/handoff | Phase 6 | Exact merged Issue #7 Vite ADR/handoff SHA plus accepted Stage A contract release SHA | **Hard blocked and non-cookable.** Issue #7 is OPEN and unmerged at validation time. The owner’s Vite direction is not a merge SHA or accepted ADR. No placeholder adapter, guessed dependency path/hash/command, or future SHA is recorded. |

Stage A merging, if later authorized, would not complete Issue #8 or automatically unblock any
downstream issue. This validator decides plan correctness only. A fresh readiness audit is the next
and only gate allowed to propose a bounded Stage A cook/merge scope; dependency owners separately
decide downstream consumption.

## Phases

| Phase | Name | Status |
|-------|------|--------|
| 1 | [Authority freeze and Stage A TDD RED](./phase-01-authority-freeze-and-stage-a-tdd-red.md) | Pending |
| 2 | [Stage A schemas validators and canonicalization](./phase-02-stage-a-schemas-validators-and-canonicalization.md) | Pending |
| 3 | [Stage A operations completion and guidance](./phase-03-stage-a-operations-completion-and-guidance.md) | Pending |
| 4 | [Stage A OpenAPI evidence and promotion manifest](./phase-04-stage-a-openapi-evidence-and-promotion-manifest.md) | Pending |
| 5 | [Stage A compatibility release and staged handoff](./phase-05-stage-a-compatibility-release-and-staged-handoff.md) | Pending |
| 6 | [Stage B Vite binding and final handoff](./phase-06-stage-b-vite-binding-and-final-handoff.md) | **Blocked — non-cookable until exact merged Issue #7 handoff SHA** |

## Dependencies and Authority

- Immutable planning input: `24be3b34c6b0fcdbd07c5800dcab349054e34713`, the remotely
  observed `origin/integration/issue-5-local-learning` Issue #6 handoff merge.
- Immutable independent-validation input: `93837667326cb7a298c21921ac04e602ea7313d0`,
  proven equal to local HEAD, tracking and fresh live remote before validation edits.
- Issue #6 contract files, registry, readers, locks, Make fragment, and tracked promotion-trust
  fixtures are read-only inputs. Their exact bytes are captured in Phase 1 and must be unchanged by
  every stage.
- Owner parallelization authority:
  `https://github.com/khanhvg/ai-ready-data-platform/issues/5#issuecomment-5036142770`.
  It permits dependency-aware planning and later bounded staged scopes; it does not authorize this
  planner to cook or merge Stage A.
- Stage B requires a freshly fetched, exact merged Issue #7 commit whose accepted handoff names
  Vite, the ADR/lock/tool paths, commands, hashes, and residual risks. An owner comment, unmerged
  branch head, proposed ADR, or guessed hash cannot clear the gate.
- The repository contains no same-scope Issue #7 plan directory at this input. Therefore no
  unresolved local `blockedBy` reference is added. The external Stage B gate is normative in this
  plan and in Phase 6.
- Master issue #5 and historical issue #3 plans remain accepted/read-only inputs. Their `pending`
  metadata does not authorize cross-plan edits from this issue worktree.

## Public Contract Boundary

- JSON Schema Draft 2020-12 is authoritative for executable learning documents.
- OpenAPI 3.2.0 describes only the synchronous HTTP admission/read boundary. V1 uses `202` plus
  bounded `GET` polling for long operations. No channel or broker exists, so no AsyncAPI artifact
  is created.
- The one mutable completion authority is the framework-neutral `learning-progress-authority-v1`
  compare-and-set transaction. Browser state, operation-result journals, evidence blobs, and Vite
  bindings are projections/references and cannot independently mark completion.
- Learner evidence and command fitness evidence are distinct versioned records. Both use strict
  I-JSON plus the existing RFC 8785/SHA-256 profile, but neither claims same-host authenticity or
  non-repudiation.
- Stage B may generate a Vite-facing hash/ID binding only. It cannot change Stage A schemas,
  operation semantics, completion authority, evidence canonical bytes, or migration rules.

## Verification Contract

Primary required commands at the future implementation head, exactly as one make invocation:

```bash
make learning-contracts-check api-contracts-check evidence-contracts-check
```

Blast-radius gates:

```bash
make lesson-check LESSON=promotion-trust
make data-contracts-check migration-contracts-check
make help
git diff --check
```

`make evidence-verify` runs against the evidence locator emitted by the preceding contract check;
the evidence path is discovered from the result rather than hard-coded. Required missing tools,
schemas, refs, commands, hashes, or evidence are `fail`, never an optional skip. Commands run
locally, use the existing manifest-admitted Python 3.12 lock, and remain safe for a 16 GiB laptop.
After dependencies are available, the contract checks must pass with network and cloud credentials
absent. No Docker, AWS, Terraform, browser, or heavy profile is part of Stage A.

## Ownership and Protected Surfaces

- Future issue-owned writes are limited to the exact Stage A files in
  [the implementation allow-list](./requirements-and-risk-traceability.md#exact-stage-a-implementation-allow-list),
  not directory-wide globs. Every new path is I5-03-owned.
- Existing Issue #6 files under `learning/contracts/**`, `scripts/golden/**`,
  `tests/contracts/**`, `tests/golden/**`, `tests/fixtures/learning/promotion-trust/**`,
  `requirements/golden-*`, and `mk/issue-5/i5-01.mk` remain byte-for-byte read-only.
- There is no protected-file exception. `learning-contract-version-registry-v1.json` is an
  Issue #8-owned additive overlay bound to shipped registry SHA-256
  `8e18588f63b5d99c0b60a229758575e8badf0f055bfcb4f89908f9fa2684a57e`. It adds a fitness-v2
  readable entry/current-for-I5-03/fallback-v1 policy for the Issue #8 dispatcher without changing
  the shipped registry, global current version, Issue #6 schema/reader/fixture/command registry,
  lock, Make file or canonicalization byte.
- Root `Makefile` already includes `mk/issue-5/*.mk`; Issue #8 must not edit it or duplicate the
  I5-01-owned `evidence-contracts-check` target.
- Protected deny-list: `release-manifest.json`, `docs/code-standards.md`, `.gitignore`, raw
  discovery/audit history, Issue #7 `spikes/web/**` and ADR files, portal/runner/data-platform
  implementation, other issue fragments, ignored runtime fixtures, cloud/AWS/Terraform paths,
  and unrelated user work.

## Release, Migration, and Rollback

- New families start at v1. Do not publish a fictional predecessor. The reader/migration engine is
  exercised with private reversible vectors; every future released version must retain old readers
  and explicit additive migration edges.
- The existing `fitness-result` family is the one deliberate non-new family: v2 is required for
  truthful `owner: I5-03` evidence because v1 fixes `owner: I5-01`. V1 stays readable and unchanged;
  rollback disables I5-03 emission while retaining both v1/v2 schemas, readability and evidence.
- A lossy migration, field drop, registry-family collision, canonical-byte change, or need to edit
  an Issue #6 contract is a STOP requiring a new version and authority decision.
- `STAGE_A_CONTRACT_RELEASE_SHA` and the final contract release SHA are externally recorded remote
  merge identities after the applicable exact-head human approval. A tracked artifact never embeds
  its own containing commit.
- Rollback reselects the prior readable version/binding and removes only marker-verified Issue #8
  generated workspace state. It never rewrites retained evidence, deletes old schemas/readers, or
  mutates Issue #6 fixtures.

## Traceability and Open Questions

- Detailed requirements, threats, risks, commands, and source links:
  [Requirements and risk traceability](./requirements-and-risk-traceability.md).
- Open product or architecture questions: none for Stage A. Stage B’s exact input identity and
  accepted handoff contents are unresolved by design and are a hard dependency gate, not a planner
  choice.

## Validation Log

### Session 1 — 2026-07-21

- Trigger: fresh independent Issue #8 validation of exact input
  `93837667326cb7a298c21921ac04e602ea7313d0`.
- Questions asked: 0; the user supplied the exact stage, security, compatibility, testing and
  authority decisions. Objective defects were corrected without reopening product choices.
- Verification tier: Full (6 phases; fact checker, flow tracer, scope auditor and contract verifier).
- Result: PASS_WITH_FIXES; detailed evidence is in
  [the independent validation report](./validation/independent-validation-report.md).
- Phase propagation: all six phase files plus traceability were reconciled.

### Whole-Plan Consistency Sweep

- Files reread: `plan.md`, all six `phase-*.md` files, and
  `requirements-and-risk-traceability.md`.
- Decision deltas checked: Stage A independence, TDD RED order, fitness evidence version,
  completion authority, OpenAPI wire contract, Stage B placeholder removal, review/authority gates.
- Reconciled stale references: recorded in the validation report.
- Unresolved contradictions: 0.

## Next Gate

Fresh staged readiness audit only. Validation establishes a corrected framework-neutral candidate;
it grants no cook, PR, merge, release or downstream authority. Stage B remains non-cookable until a
real merged Issue #7 Vite ADR/handoff SHA exists and this plan is amended/revalidated against it.
