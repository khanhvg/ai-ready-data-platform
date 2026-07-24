# Combined independent plan validation and cook-readiness audit

Date: 2026-07-24 (Asia/Ho_Chi_Minh)

Repository: `khanhvg/ai-ready-data-platform`

Issue: [#38](https://github.com/khanhvg/ai-ready-data-platform/issues/38)

Branch: `plan/issue-38-assessment-package`

Planner/base SHA: `58a9b7f45f5b2d473a39bc2f9eb9258fe92d0b2a`

Immutable audit input SHA: `3d4f9aa40b34ed0db82e5a0309174a80b4616bdb`

Auditor runtime: Codex CLI managed by Herdr; `gpt-5.6-sol`; `model_reasoning_effort="high"`

Context: fresh independent auditor; planner reasoning and self-check treated as assertions, not audit evidence

## Verdict

**PASS — ready to cook**

No Blocker or Important finding remains after the corrections below. This verdict authorizes only the issue's implementation workflow after the verified GitHub state transition. It does not authorize product code in this audit commit, cloud/AWS/Terraform apply, hosted deployment, customer data, additional industry pipelines, learning/lab restoration, or live pipeline control from the web.

## Evidence reviewed

- Verified before editing that local `HEAD`, `origin/plan/issue-38-assessment-package`, and the immutable audit input all equaled `3d4f9aa40b34ed0db82e5a0309174a80b4616bdb`; the tracked worktree was clean.
- Read the full 902-line confirmed advisory, Issue #38 body, both owner comments, and all labels.
- Read all 15 immutable plan artifacts (1,440 lines), including the planner self-check.
- Read the repository README, architecture/storage/transform/demo/OpenMetadata/lake runbooks, version matrix, GH-3 empirical evidence, Makefile, Compose resource limits, ignore/release surfaces, current Python entrypoints, dbt contracts/models relevant to quality/PII, canonical 11-asset inventory, Airflow DAG/callables, and recent cleanup/plan history.
- Independently reconciled current facts: 18 generated/raw tables; 51 dbt models (18 staging, 6 ephemeral intermediate, 7 dimensions, 9 facts, 11 marts); 11 canonical Rill/Iceberg assets; 45 materialized logical OpenMetadata tables/130 lineage edges; current resource limits; and the deliberate removal of the learning portal/labs.

## Findings and corrections

### Important I-01 — Capability anchors were conflated with question scoring anchors

- Evidence: Issue criterion 2 and advisory §§11.2/22 require observable 0–4 anchors for every assessed capability, while the input Phase 1 required only 30 questions/150 anchors and called that capability coverage.
- Affected: `phase-01-rubric-report-prototype-and-calibration.md` Requirements, Architecture, Steps, Success Criteria; `architecture-decisions.md` PD-04/PD-08; `requirements-traceability.md` AC-02/SM-03.
- Required correction: make all 10 domains carry 50 explicit capability anchors in addition to 150 per-question scoring anchors, validate both sets, and expose the selected capability anchor in results.
- Resolution: corrected in all affected artifacts.

### Important I-02 — Readiness/gate semantics and calibration precision were incomplete

- Evidence: the input did not define numeric readiness labels or production-ready threshold, grouped distinct critical controls into four traces, and claimed `118/120` comparable ratings even though one shared `null` is not a maturity rating. Independent recomputation gives 117 within-one-level pairs out of 119 comparable ratings (98.3%); coverage is 119/120 question slots. The single “expected domain maturity” column represented Architect A only: lower-median recomputation produced distinct Architect B domain scores and, for two personas, a one-level difference in final readiness.
- Affected: `architecture-decisions.md` PD-08/PD-10; Phase 1 Architecture/Steps/Success Criteria; Phase 3 Architecture/Steps/Success Criteria; traceability AC-03/SM-04/SM-07.
- Required correction: version labels 0–4, exact one-decimal presentation math, pin the gate bundle/profile, trace quality/security/privacy/governance/ownership/lineage/reproducibility independently, use the real comparable denominator, and record/assert per-rater domain/pre-gate/final expectations rather than one shared result.
- Resolution: corrected; infrastructure strength cannot bypass any critical operand and every triggered/non-triggered rule remains explainable.

### Important I-03 — Dependency ownership and no-network claims were not cookable

- Evidence: Phase 1 used YAML/Jinja/pytest but Phase 2 owned `pyproject.toml`/locks; clean-checkout simultaneously required a fresh environment and no network without vendored wheels/browser. Playwright and the Mermaid renderer had no bounded provisioning contract. The repository currently has only pip requirement files and no assessment package/toolchain.
- Affected: `architecture-decisions.md` PD-02/PD-14 and command contract; Phases 1, 2, 4, 5, and 8; traceability command map.
- Required correction: Phase 1 owns the package/hashed locks; use explicit Python, browser, and diagram bootstrap targets; allow network only for pinned acquisition (or verified caches); block network for all subsequent tests; keep Node/Mermaid build-only; use one Playwright worker/browser.
- Resolution: corrected without adding Node to the application runtime or a frontend build pipeline.

### Important I-04 — Archive/evidence admission did not fully fail closed

- Evidence: the input promised secret/path-safe exports but allowed unspecified evidence files, gave no numeric size limits, did not define the manifest self-digest, destination collision behavior, expanded-size/zip-bomb checks, or cross-runtime ZIP determinism. Opaque PDF/archive content cannot support the claimed secret scan.
- Affected: `architecture-decisions.md` PD-06; Phase 2 Architecture/Steps/Success/Security; Phase 8 hostile-corpus verification; traceability AC-06/SM-09/SM-10.
- Required correction: canonical `ZIP_STORED` export; defined digest coverage; versioned entry/depth/file/total limits; streaming expanded-size/ratio enforcement; reject encryption/unsupported features, archive/pre-existing symlinks and destination collisions; canonicalize/scan only allowlisted text/JSON/CSV/PNG/JPEG evidence and reject opaque types.
- Resolution: corrected with non-mutating preflight and explicit diagnostics.

### Important I-05 — Quarantine did not prove exclusion from a curated acceptance boundary

- Evidence: current `stg_orders` deliberately preserves invalid statuses and the canonical marts expose/summarize quality warnings. The input added `quarantine_orders` but only proved absence from a later AI product, while still calling the existing 11 marts curated; that could not prove the advisory metric that a failing record is blocked from curated.
- Affected: Phase 6 Requirements, Architecture, files, Steps, Success Criteria; traceability SM-13.
- Required correction: use the existing invalid-status injection; create complementary `quarantine_orders` and `accepted_orders`; prove non-empty/disjoint/complete partition and exclusion from accepted/governed outputs; preserve and honestly label the legacy canonical 11 marts.
- Resolution: corrected; no existing mart contract is silently changed.

### Important I-06 — Access-control evidence boundary was under-specified

- Evidence: a “checked policy file plus export entrypoint” could be documentation-only or overstate protection because the local OS user can open DuckDB directly. The compatibility spike had no exact inputs, denials, bypass tests, or stop predicate.
- Affected: `architecture-decisions.md` PD-16/BQ-02; Phase 6 Requirements, Architecture, Steps, Success/Security; traceability SM-14.
- Required correction: define a real application authorization CLI accepting only fixed role/asset IDs/output root, deny raw/staging/unknown assets before query construction, allow only the safe product, accept no SQL/path/table expression, test the real CLI and output schema, state the OS-user limitation, and stop if any property fails.
- Resolution: corrected; documentation or mocks cannot satisfy the gate.

### Important I-07 — Runtime and golden commands could pass without exercising the workflow

- Evidence: `make airflow && make down` starts/stops the UI but does not trigger or poll the DAG; `demo-contract`/`demo-verify` appeared in traceability but not the command/ownership contract. Browser E2E did not require retention and inspection of the real generated report artifact.
- Affected: architecture command contract; Phases 4, 6, and 8; traceability AC-07/AC-08/AC-10 and SM-08/SM-12/SM-16.
- Required correction: add owned `demo-contract`, `demo-verify`, and `demo-airflow-verify` targets; the Airflow target must wait, trigger, poll the exact run, record task states, and tear down. Add an artifact-producing `assessment-runtime-smoke` that drives the real architect journey and verifies standalone report JSON/HTML and digests.
- Resolution: corrected; container startup or unit tests alone cannot close runtime acceptance.

### Important I-08 — Deep-dive recalculation lacked an authoritative state transition

- Evidence: the input said deep dives preserve quick history but may change readiness, without defining which result is active, how conflicts are resolved, or how prior reports remain auditable.
- Affected: Phase 7 Requirements, Architecture, Step 4, Success Criteria.
- Required correction: immutable quick result revisions; separate advisory deep-dive results; explicit architect-reviewed promotion record with source/target digests, capability IDs, rationale, and conflict choices; new result revision/full gate trace; before/after reporting.
- Resolution: corrected; no automatic latest-wins overwrite remains.

### Minor M-01 — JSON Schema and typed-model authority could drift

- Evidence: both were proposed as validators, but neither was named authority and no parity check was planned.
- Affected: `architecture-decisions.md` PD-04; Phase 2 Steps.
- Required correction: make versioned JSON Schema the public authority and require schema/model parity fixtures.
- Resolution: corrected.

### Minor M-02 — Research evidence listed a non-current issue label

- Evidence: immutable input labels were `enhancement`, `ready for plan audit`, `risk:high`, `architecture`, `data-platform`, and `evidence`; the research artifact claimed `triaged`.
- Affected: `research/researcher-01-requirements-advisory.md` Sources and authority.
- Required correction: record the actual immutable-input label set.
- Resolution: corrected.

## Residual cook conditions

These are empirical implementation gates, not unresolved plan findings:

1. Phase 1 must execute calibration; the 117/119 fixture result is a recomputed planned fixture expectation, not a claim that human calibration has already run.
2. Exact Python/browser/Mermaid dependency hashes must be resolved and installed on Python 3.12/macOS arm64; an incompatible lock or unbounded browser run stops the phase rather than weakening the contract.
3. The Phase 6 application authorization spike must satisfy every real-CLI allow/deny/bypass assertion or stop for owner decision BQ-02.
4. OpenMetadata live re-verification requires the documented local token and staged services. Historical GH-3 evidence may be linked, but an unexecuted current stage must remain visibly unexecuted.
5. Cross-path/archive determinism and clean-checkout packaging are acceptance tests to execute during cook; this audit validates their design and exact failure boundaries, not their future runtime result.

## Verification

- Structural scan passed: 16 Markdown artifacts after adding this report, exactly eight linked phase files, required phase H2 order, and 51-line `plan.md`.
- Traceability scan passed: one ordered row each for `AC-01…AC-12` and `SM-01…SM-17`, with corrected step references and discoverable commands.
- Relative-link scan passed across all 16 Markdown artifacts.
- Independent fixture recomputation passed: 117/119 comparable ratings within one level (98.3%), 119/120 comparable slots, and both per-rater domain arrays exactly match the corrected table.
- Repository reconciliation passed: 18 staging sources/models, 6 intermediate models, 7 dimensions, 9 facts, 11 marts, and 11 Rill model/metric/explore plus canonical asset entries.
- Scoped staging contains only 14 changed/new artifacts under `plans/260724-1758-GH-38-ai-ready-assessment-package/`; no product or unrelated plan file is present.
- `git diff --check` and `git diff --cached --check` passed; the complete 14-file staged diff was inspected. Commit/push equality, clean tracked worktree, and GitHub comment/label verification are final publication gates and are reported with the exact output SHA on Issue #38.

## Audit boundary

No product code, application stack, cloud resource, pipeline run, PR, merge, customer data, skill file, or unrelated plan was created or changed by this audit. Only Issue #38 plan artifacts and this report are in scope.
