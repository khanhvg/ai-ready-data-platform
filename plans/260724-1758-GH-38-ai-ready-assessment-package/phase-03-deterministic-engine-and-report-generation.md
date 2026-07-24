# Phase 3: Deterministic engine and report generation

## Context links

- Parent: [plan.md](./plan.md)
- Dependencies: [Phase 1](./phase-01-rubric-report-prototype-and-calibration.md), [Phase 2](./phase-02-versioned-contracts-local-store-and-portability.md)
- Decisions: [PD-08–PD-12](./architecture-decisions.md)
- Traceability: [AC-02–AC-04, AC-08; SM-05–SM-08](./requirements-traceability.md)

## Overview

- Date: 2026-07-24
- Description: Build deterministic maturity, confidence, readiness-gate, finding/recommendation, and canonical report services over final v1 contracts.
- Priority: P2
- Implementation status: Completed
- Review status: Initial edge-case scout findings corrected; fresh exact-head review remains
  pending publication.

## Key Insights

- Maturity aggregation, confidence summarization, readiness labels, and gating are distinct typed operations.
- Every output must be reconstructable from pinned content plus engagement source state.
- Findings are traceable rules with architect review state; they are not opaque generated prose.
- HTML is a presentation of canonical report JSON and must require no manual edit.

## Requirements

- Deterministic outputs for missing/partial answers, coverage thresholds, ties, and conflicting evidence.
- Capability results with score 0–4, capability anchor/label, presentation score, coverage, confidence distribution/status, and source question IDs.
- Full explainable rule traces for all gates.
- Findings/recommendations with stable content references and architect accept/defer/edit-note review; edits do not rewrite engine truth.
- Exactly 12 ordered report sections and standalone accessible HTML.
- No demo evidence can affect maturity, confidence, priority, or readiness.

## Architecture

Pure services accept immutable typed snapshots and loaded version bundles:

```text
answers -> maturity -> confidence ----+
diagnostic facts -> gates ------------+-> assessment result
capability gaps -> findings -> recommendations
assessment result + catalog/demo references + reviews -> report.json -> report.html
```

Maturity uses the versioned aggregation, capability anchors, readiness labels, exact decimal presentation formula, and coverage rules fixed in calibration. Confidence summarizes status counts and chooses the most conservative status by configured precedence. The pinned assessment profile selects the exact seven-rule gate bundle; gates evaluate without short-circuiting so every triggered/non-triggered rule has an operand-level trace and the most restrictive cap wins. Findings are sorted deterministically by priority, capability order, and finding ID. Canonical JSON uses stable key/list order, one-decimal presentation-score strings, and an explicit source-state digest; generated wall-clock time is excluded or injected from engagement metadata.

## Implemented code files

- `assessment/src/assessment/engine/`: maturity, confidence, gate, finding, priority,
  recommendation, input, and evaluator services.
- `assessment/src/assessment/reporting/`: canonical report models, generation, and rendering.
- `assessment/src/assessment/framework_assets/1.0.0/`: pinned bundle, HTML template, and CSS.
- `assessment/src/assessment/frameworks.py`: packaged framework loading and integrity checks.
- `assessment/tests/unit/test_{maturity,confidence,gates,findings,recommendations,priority}.py`.
- `assessment/tests/contract/test_report_contract.py`.
- `assessment/tests/scenario/test_v1_scenario_goldens.py` and migrated v1 scenario expectations.

## Implementation Steps

1. Implement maturity results with configured coverage, not-assessed handling, deterministic median/rounding, capability ordering, and labeled 0–100 presentation score.
2. Implement independent confidence distributions and conservative summary; preserve conflicting evidence and produce evidence-next-action language without changing maturity.
3. Implement all seven versioned gate rules and evaluation traces. Prove quality, security, and privacy independently cap 1; governance and ownership independently cap 2; critical-lineage absence caps 2/forbids production-ready; reproducibility absence caps 2/limits experiment-ready; combined triggers select the minimum cap while retaining every explanation.
4. Implement finding, priority, recommendation, and review-state services; validate complete links and deterministic ordering, and prove demo-reference mutation leaves engine results unchanged.
5. Build canonical report model with the 12 required ordered sections and evidence provenance (`customer answer`, `customer evidence`, `architect judgment`, `demo illustration`).
6. Resolve the report template/CSS from the engagement-pinned framework version, then render standalone semantic HTML with embedded CSS/SVG, escaped content, print styles, table alternatives for diagrams, no remote resources, and no manual-edit step.
7. Migrate Phase 1 goldens and compare intended v0.1→v1 deltas; add property/boundary tests and two-run byte comparisons.
8. Expose CLI commands `evaluate` and `report` with explicit engagement/output roots, machine-readable errors, nonzero failure codes, and no network/service startup.

## Todo list

- [x] Implement and boundary-test maturity and coverage.
- [x] Implement separate confidence summaries.
- [x] Emit complete gate traces for triggered and untriggered rules.
- [x] Generate linked findings/recommendations with review states.
- [x] Produce canonical 12-section report JSON.
- [x] Render accessible self-contained HTML.
- [x] Prove scenario goldens and deterministic bytes.
- [x] Prove demo evidence cannot influence scoring.

## Success Criteria

- All unit/contract/scenario tests pass via `make assessment-test assessment-scenarios assessment-report`.
- The four Phase 1 capability/gate/finding expectations remain satisfied after migration.
- Every result shows coverage and confidence independently; no score is emitted below required coverage.
- All seven triggered/non-triggered gate traces are visible with operand provenance; the strongest cap and readiness label are deterministic.
- Every critical finding has gap, impact, priority, recommendation, architecture; unresolved reference is a contract error.
- Both report files contain all 12 sections; standalone HTML renders headlessly with network disabled and is byte-stable.
- Changing demo artifact availability/checksums cannot change maturity/readiness/findings priority.

## Risk Assessment

- Rule ordering could alter outcomes; evaluate all rules and choose explicit minimum cap.
- Sparse answers may appear precise; enforce coverage and surface Not assessed rather than impute.
- Architect edits could destroy provenance; store review notes/overrides separately and report both generated and reviewed state.
- HTML determinism can break on nondeterministic SVG/metadata; normalize assets and omit generated timestamps.
- Rollback: revert the additive pure engine/report modules and restore the prior framework pointer; source answers/evidence remain untouched and generated reports may be safely regenerated or removed.

## Security Considerations

Escape all customer-authored fields, sanitize Markdown, ban template auto-safe bypasses, enforce output-root containment, and use no browser execution for report generation. CSP-compatible standalone output contains no script, forms, remote fonts, telemetry, or clickable credential URIs.

## Next steps

Publish and independently verify an immutable Phase 3 head. Phase 4 may then expose only these
stable services through the loopback web workflow; Phases 4–8 remain pending.
