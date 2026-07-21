---
title: "Fresh Readiness / Plan-to-Cook Audit — Issue #6 I5-01"
issue: 6
phase: fresh-readiness-plan-to-cook-audit
status: ready-with-gates
auditInputSha: "c27d5fdadbf5bcf4f635de14241250d5ac238e45"
plannerSha: "cec9f6b02cb3bf9f2aa7e2cf26af32692008aacd"
discoverySha: "7a65da010abf0e3730731b6d744b532156c48fdc"
integrationSha: "f9a87d0ebdb72c014a6f8c6eaae865dad4d2188c"
masterReadinessSha: "e440c5855732d5d8f5d634e3cc1359c010cc5ed3"
auditOutputSha: "externally-attested-in-issue-6-publication-comment"
authorizedScope: full-eight-phase
auditedAt: "2026-07-21"
---

# Fresh Readiness / Plan-to-Cook Audit — Issue #6 I5-01

## Verdict

`READY_WITH_GATES` for the full eight-phase serialized cook defined in
[cook-scope.md](./cook-scope.md).

The corrected plan is executable by one future implementation actor in exactly one new branch
and one new worktree. No Critical or unresolved High readiness ambiguity remains. The remaining
gates—RED evidence, exact lock/tool publication, formal two-run evidence, C1/C2 attestation,
post-implementation review, human pre-merge approval and later remote merge—are honest future
implementation/release gates, not permission to weaken or skip work.

This audit performed no `$ck:cook`, implementation, product/config/data edit, dependency/tool
installation, fixture publication, architecture-source generation, cloud action, destructive
migration, PR or merge.

## Fresh Phase and Immutable Provenance

| Check | Observed result |
|---|---|
| Worktree/branch | exact requested issue #6 worktree on `plan/issue-6-freeze-golden-baseline-contracts` |
| Immutable input | local HEAD, upstream and freshly observed live remote all `c27d5fdadbf5bcf4f635de14241250d5ac238e45` before edits |
| Clean input | no staged, unstaged or untracked path before audit edits |
| Planner relation | audit input descends directly from planner `cec9f6b02cb3bf9f2aa7e2cf26af32692008aacd` |
| Required ancestry | discovery, integration and master-readiness SHAs all verified ancestors |
| Input issue state | issue #6 open with `ready for plan audit`, `risk:high`, `tdd`, `security:S3`, `shared-core`, `data-integrity` |
| Requested runtime identity | user requested Codex `gpt-5.6-sol`, `model_reasoning_effort="xhigh"`; no shell API exposes an independent runtime attestation |

The audit output SHA cannot appear literally in its containing tracked files without recursion.
The exact containing commit is published in the issue #6 readiness comment and becomes the only
valid future `IMPLEMENTATION_INPUT_SHA`.

## Sources Read

The audit read:

- issue #6 body and all seven comments, including the exact fixture authority clarification;
- all issue #6 discovery, plan, decision, phase, handoff, traceability and validation artifacts;
- master issue #5 body/comments and binding I5-01/P1, execution/authority/release,
  architecture-view, S3 runner/security, implementation-graph, traceability and readiness-audit
  artifacts at the supplied SHAs;
- issue #7 body/comments, its current readiness report, Gate 0/A cook scope and issue #6 fixture
  handoff at `e8ca5f3ee9e8976a4b92915fd7d7dc687609f7a9`;
- README, system/storage/transformation/historical evidence/lake/governance documentation and the
  current Make, generator, loader, dbt, Rill, Airflow, export, curated, Iceberg and OpenMetadata
  source surfaces.

The requested `$ck:plan-to-cook` skill was not installed or present in the local skill catalog.
The audit therefore applied the repository's existing readiness-report/cook-scope pattern and the
user's 14 criteria directly. `ck:git` publication safety was used subject to the session's
no-delegation constraint. No `ck:cook` workflow was invoked.

## Read-Only Repository and Dependency Probes

No package/tool install or product implementation command ran.

| Probe | Result |
|---|---|
| `ck plan status` | pending, 0/8, correct plan branch and tags |
| Future issue #6 feature branch | absent locally and remotely |
| Future issue #6 implementation worktree path | absent |
| Host tools | CPython 3.12.3/pip 26.1.1; Node 22.22.3/npm 10.9.8; GNU Make 3.81 |
| Existing Make | exactly 15 targets; all seven issue #6 targets absent; `make -n golden-clean` fails as expected |
| Static sources | all relevant Python files parse; dbt has 51 SQL models; Rill has 11 metrics and 11 explores; curated registry has exact 11 assets |
| Protected baseline | release manifest, `.gitignore`, Airflow DAG, data/dbt/Rill/lake/governance/discovery identities and absence markers recorded in the cook scope |
| Compiler lock candidate | retained disposable validation bytes re-hashed read-only: exact repository-relative 40 lines and `ece1d206…`; literal is now embedded to break bootstrap circularity |
| Issue #7 Gate A | feature branch/worktree exists at exact audit output and currently has untracked `mk/`/`spikes/` work only; four issue #6 handoff files remain absent |

Issue #7's Gate A work is disjoint and may continue independently. Barrier B remains closed. It
cannot consume the issue #6 cook branch, C1, C2 or local fixture output; it waits for reviewed
remote M plus four exact digests.

## Readiness Findings and Bounded Fixes

All fixes are planning-only and inside
`plans/260721-006-freeze-golden-baseline/**`. Discovery history is unchanged.

| ID | Severity | Input ambiguity | Bounded resolution |
|---|---|---|---|
| RA6-01 | High | No exact future branch/worktree/absence/reuse/no-rebase lease existed | Froze branch `feature/issue-6-golden-baseline-contracts`, one sibling implementation worktree, external input-SHA rule, absence/equality checks, one writer and no reuse/rebase/merge/force/reset |
| RA6-02 | High | Phase 5/6 parallel wording and prose-only tests-before left writer/order and RED proof interpretable | Serialized all eight phases, defined exact task IDs, named RED IDs/commands/evidence, phase-1/2 bootstrap ordering and no bulk generation before RED |
| RA6-03 | High | The compiler tool lock was required to install the compiler that would create that same lock | Embedded the exact reviewed 40-line compiler lock source and hash; bundled pip may install only after byte verification, then generates the 840-line/56-distribution application lock |
| RA6-04 | High | Architecture provenance relied on an ambient Node version and contradictory Linux-required wording | Required the official Darwin-arm64 Node archive/hash, safe private extraction, two lock installs, offline render after bootstrap; Linux/Windows are explicit future lanes |
| RA6-05 | High | Formal execution mixed Git-less archives with Git-root verification and called visible `.artifacts` ignored/private | Formal runs now use one read-only C1 worktree plus two disjoint sequential state roots; `.artifacts` is explicitly visible/untracked/never staged with relative safe locators and marker-only cleanup |
| RA6-06 | High | Root Make/help and Airflow exception were bounded conceptually but not exact enough for a medium-reasoning cook | Froze the two-line ordered include, help ownership, 15/54/7 tests and exact Airflow import/parse/default/explicit-path/DAG regression boundary |
| RA6-07 | Medium | Private permissions, free-space/disk bounds and retry ownership were not numeric/executable | Added Darwin POSIX mode checks, 6 GiB preflight, per-root/evidence caps, sequential cleanup, one identical owner-approved network retry and retained first failure |
| RA6-08 | High | Traceability named rollback/STOP globally, but phase-local exit behavior remained implicit enough that a cook could continue after a failed gate | Added a phase-specific failure-evidence, rollback and STOP section to every phase; no failed phase can advance, generate a later artifact or publish C2 |
| RA6-09 | High | Lease command blocks used prose placeholders that Bash would treat as redirection or literal brace paths | Replaced them with executable issue-comment SHA resolution, exact repository/worktree variables, local/tracking/live equality, clean-state, ancestry and label assertions |

No fix expands issue authority, changes a product decision, edits a protected file or reverses a
validated decision.

## Fourteen-Criterion Disposition

| # | Criterion | Disposition |
|---:|---|---|
| 1 | Exact implementation lease | Pass after RA6-01; exact external input SHA, new branch/worktree, equality, absence, one writer and no destructive Git behavior are mandatory |
| 2 | Authority/protected state | Pass; exact issue/comment paths, hashes/absence/tree IDs, unrelated/untracked preservation, conditional Make/Airflow exceptions and later-path denial are frozen |
| 3 | Tests-first execution | Pass after RA6-02; each phase has named RED IDs, exact sequential task boundary, evidence, green/refactor/blast radius and refusal rollback |
| 4 | Dependency lock | Pass after RA6-03; direct RFC 8785 root, exact 840/56 app lock, exact compiler lock, two empty installs, imports/checks/runs, unsupported tuple/sdist/resolver failures |
| 5 | Architecture toolchain | Pass after RA6-04; exact Node/npm/LikeC4/hpcc locks/integrities/licenses/commands, six IDs, C4 fitness, semantic text, controlled SVG normalization and no false fallback |
| 6 | Golden characterization | Pass; 18/6,812, 51/141/18, 179/7/0/186, nine-vs-seven, 11 marts, Rill/Airflow/curated/catalog anchors and anomaly-layer mutations agree |
| 7 | Contracts/canonicalization/provenance | Pass; Schema 2020-12, RFC 8785/I-JSON vectors, registry/migrations, raw/projection/envelope, five pointers, atomic writes and non-recursive C1/C2/M semantics are explicit |
| 8 | Workspace security:S3 | Pass after RA6-05/07; private modes, lexical/realpath/parent/link/foreign/TOCTOU/concurrency/process/env/output/time/disk/atomic/refusal/scan defenses are executable; generalized runner remains deferred |
| 9 | Curated release/promotion trust | Pass; schema/pointer only, exact 11 common-generation assets, four-grain 89-row safe candidate/invalids, `insufficient-evidence` and deny-list are exact |
| 10 | Make/Airflow/shared leases | Pass after RA6-06; current 15, master 54, issue seven, safe missing fragments, import/parse/default/explicit Airflow behavior and additions-only view lease are exact |
| 11 | Operational feasibility/time | Pass with future evidence gate; 300/600 core guards, separate architecture/lock timing, output/disk bounds, identical retry and marker-only cleanup are frozen |
| 12 | Evidence/release | Pass; safe relative `fitness-result-v1`, explicit equality layers, zero staged/tracked `.artifacts`, rollback before C2, external merge/tag and human gate are mandatory |
| 13 | Dependency handoff | Pass; issue #7 waits for reviewed M plus exact four digest/blob checks; its current Gate A remains synthetic/disjoint and cannot open scoring |
| 14 | Whole-plan/risk | Pass after bounded fixes; validation corrections, F-01..F-12, SC-01..SC-15 and binding PH/authority items retain owner/path/test/evidence/rollback/dependency/STOP traceability; DAG/IDs/versions/hashes agree |

## Authorized Cook and Evidence Spine

The authorized cook is `full-eight-phase`, not a staged subset. It executes the exact serialized
tasks in [cook-scope.md](./cook-scope.md), ending at external C1/C2/four-digest attestation.

Required public commands are:

```bash
make help
make golden-clean PROFILE=small SEED=42
make data-contracts-check
make evidence-contracts-check
make migration-contracts-check
make architecture-check
make architecture-render
git diff --check "$IMPLEMENTATION_INPUT_SHA"...HEAD
```

All required missing tools/evidence fail typed and non-zero. The two formal C1 runs are sequential,
state-independent, ≤300 seconds each and ≤600 seconds combined. Rollback rehearsal precedes C2.
Transient `.artifacts` is never staged. C2 contains only authorized promotion fixture/manifest/
raw-parser invalid bytes and cannot recursively contain itself or M.

## Remaining Non-Waivable Gates

- Every phase RED capture and all future implementation evidence.
- Exact tracked Python and architecture locks/sources/rendered outputs.
- Two formal clean C1 runs and third-reader C2 verification.
- Independent post-implementation review/security validation.
- Human pre-merge approval.
- PR/merge/tag and external M; none is authorized by this audit.
- Issue #7 Barrier B/current-browser/manual-accessibility/scoring/ADR gates.
- Publisher, generalized runner, signing, later architecture views, portal, cloud/AWS/Terraform and
  AI work remain with their later owners.

## Proof of No Implementation

The audit changed only Markdown files under the exact issue #6 plan directory. It did not create
the feature branch/worktree, product tests/code/contracts/locks/fixtures/views, `.artifacts`,
dependencies, tools, cloud state, migrations, PR or merge. Root Make, Airflow, release manifest,
`.gitignore`, repository sources, discovery and user state remain untouched.

`AUDIT_VERDICT=READY_WITH_GATES`

`ISSUE_STATE=ready to cook`

`COOK_SCOPE=full-eight-phase`
