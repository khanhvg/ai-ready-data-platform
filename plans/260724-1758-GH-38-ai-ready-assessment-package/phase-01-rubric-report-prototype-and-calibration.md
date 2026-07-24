# Phase 1: Rubric/report prototype and synthetic calibration

## Context links

- Parent: [plan.md](./plan.md)
- Decisions: [PD-03, PD-04, PD-08–PD-12](./architecture-decisions.md)
- Traceability: [AC-01–AC-04, AC-08–AC-09; SM-01–SM-08](./requirements-traceability.md)
- Requirements evidence: [researcher-01](./research/researcher-01-requirements-advisory.md)
- Confirmed advisory: `/Users/khanhvg/Documents/work/data-assessment/ai-ready-data-platform-assessment-advisory.md` §§8, 11, 19, 23

## Overview

- Date: 2026-07-24
- Description: First and only initial vertical slice—prove the rubric, gates, findings, report shape, timing, and two-rater consistency with synthetic architect-led customer scenarios.
- Priority: P2
- Implementation status: Pending
- Review status: Requires focused Phase 1 review before Phase 2; this is not the independent combined plan audit.

## Key Insights

- UI and golden-pipeline work cannot compensate for an uncalibrated assessment; this phase uses prototype files and a thin deterministic runner only.
- Capability maturity and confidence are independent. Repository/demo facts never supply customer ratings.
- Four personas keep the minimum-three criterion comfortably bounded and exercise every gate.
- Prototype output becomes a migration fixture; it is not silently treated as final schema.

## Requirements

- Ten capability domains, three quick questions each (30 total), every question with observable anchors 0–4.
- Completion target ≥27/30 and elapsed time ≤60 minutes per scenario.
- Two explicit architect rating fixtures per scenario; ≥85% of paired question ratings differ by no more than one level.
- Prototype gate trace covers low quality, low security/privacy, low governance/ownership, missing critical lineage, and missing reproducibility/versioning.
- Each critical finding contains gap, impact, priority, recommendation, and logical architecture reference.
- A deterministic 12-section `report.json` plus standalone `report.html` prototype.

## Architecture

Prototype files live under `assessment/prototype/0.1.0/` and `assessment/tests/fixtures/scenarios/0.1.0/`; no FastAPI, store, or golden pipeline dependency is introduced. A small `assessment/prototype/run.py` loads YAML/JSON, validates all anchors and references, applies median-of-assessed-answer capability aggregation with explicit configured coverage, emits gate traces/findings, and renders Jinja2 HTML. Phase 2 migrates these fixtures to `1.0.0`; Phase 3 replaces the prototype runner with domain services while preserving golden outputs.

Question order for the explicit arrays below is three questions for each confirmed advisory domain: Strategy, ownership, and operating model (`STR`); Data sources, ingestion, and integration (`ING`); Storage, lifecycle, and data organization (`STO`); Transformation and orchestration (`TRN`); Data quality and reliability (`QUA`); Metadata, catalog, glossary, and lineage (`LIN`); Governance, privacy, and compliance (`GOV`); Security, access control, and policy-as-code (`SEC`); Observability, operations, and cost management (`OPS`); Data products, analytics, and AI readiness (`AID`). `null` means Not assessed and does not count as an answered question.

Framework v1 requires at least two answered questions in every domain and at least 27/30 overall. A domain score is the unweighted lower median (`median_low`) of its answered ratings. The pre-gate readiness level is `floor(mean(all 10 domain scores))`; the labeled 0–100 presentation value is `mean * 25`. No overall/readiness value is emitted if any domain misses coverage. Gates then apply the most restrictive cap. Privacy and ownership gate inputs are explicit critical diagnostic facts within `GOV`/`STR`, not inferred from vendor products.

| Fixture | Architect A ratings (30) | Architect B ratings (30) | Expected domain maturity (STR…AID) | Critical facts and expected outcome |
|---|---|---|---|---|
| `startup-no-governance` | `[2,2,1, 1,1,0, 1,1,1, 2,2,1, 2,1,1, 1,0,1, 1,1,1, 1,1,0, 1,1,0, 2,2,1]` | `[2,1,1, 1,0,0, 1,1,0, 2,1,1, 2,2,1, 1,1,0, 1,1,1, 1,0,0, 1,0,0, 2,1,1]` | `2,1,1,2,1,1,1,1,1,2` | `critical_lineage=false`, `reproducible_versioned=false`; quality and security/privacy cap final readiness at 1. Findings: establish data ownership, quality controls, privacy classification, lineage, reproducibility. |
| `enterprise-lake-weak-quality` | `[3,3,2, 3,3,2, 3,2,3, 3,3,3, 1,1,0, 3,3,2, 3,3,2, 3,3,2, 2,2,1, 2,2,2]` | `[3,2,2, 3,2,2, 3,3,2, 3,3,2, 1,0,0, 3,2,2, 3,2,2, 3,2,2, 2,1,1, 2,1,2]` | `3,3,3,3,1,3,3,3,2,2` | `critical_lineage=true`, `reproducible_versioned=true`; quality cap final readiness at 1 despite platform strength. Finding: quarantine and measurable quality ownership. |
| `manual-governance-missing-lineage` | `[2,2,2, 3,3,3, 2,2,2, 2,2,1, 2,2,1, 1,1,0, 2,2,2, 2,2,1, 2,2,1, 2,2,2]` | `[2,2,1, 3,3,2, 2,1,2, 2,1,1, 2,1,1, 1,0,0, 2,2,1, 2,1,1, 2,2,1, 2,2,1]` | `2,3,2,2,2,1,2,2,2,2` | `critical_lineage=false`, `reproducible_versioned=true`; production-ready is forbidden, final experiment-ready/readiness 2. Findings: automate metadata/lineage and AI operating ownership. |
| `strong-engineering-no-ai-operating-model` | `[3,3,3, 3,3,2, 3,3,3, 4,3,3, 4,3,3, 3,3,3, 3,3,3, 3,3,2, 2,2,null, 1,1,0]` | `[3,1,3, 3,2,2, 3,2,3, 4,3,2, 4,3,2, 3,2,3, 3,2,3, 3,2,2, 2,1,null, 3,1,0]` | `3,3,3,3,3,3,3,3,2,1` | `critical_lineage=true`, `reproducible_versioned=false`; final state limited to experiment-ready/readiness 2. Findings: versioned AI products, AI operating ownership, monitoring, reproducibility. |

Two ratings differing by two in the fourth persona (`STR` and `AID`) intentionally make calibration non-trivial: 118/120 pairs are within one level (98.3%), above the ≥85% target. Each fixture also supplies 30 evidence-status values, architect notes, expected confidence distributions, duration (35/42/48/39 minutes), and actionability review flags. The fourth fixture has 29/30 answered (96.7%) while still answering at least two questions in every domain; the others have 30/30.

## Related code files

- Create: `assessment/prototype/0.1.0/{capabilities.yaml,quick-questions.yaml,gates.yaml,finding-rules.yaml,recommendations.yaml}`
- Create: `assessment/prototype/{run.py,report-template.html.j2,report.css}`
- Create: `assessment/tests/fixtures/scenarios/0.1.0/{startup-no-governance,enterprise-lake-weak-quality,manual-governance-missing-lineage,strong-engineering-no-ai-operating-model}/{architect-a.json,architect-b.json,expected.json}`
- Create: `assessment/tests/scenario/test_prototype_scenarios.py`, `assessment/tests/scenario/test_calibration.py`
- Create generated/ignored: `assessment/.generated/prototype/<scenario>/{report.json,report.html,summary.json}`
- Modify: `Makefile` only to add isolated Phase 1 install/schema/scenario/calibration/report targets; no existing target behavior changes.

## Implementation Steps

1. Define the 10-domain rubric and exactly 30 quick questions with observable, non-vendor anchors 0–4; semantic validation requires every level and capability coverage.
2. Encode the v1 lower-median/coverage/readiness algorithm, confidence precedence, all initial gates, the ordinal finding-priority decision table, recommendations, and architecture placeholders as versioned content.
3. Materialize both-rater fixtures above with explicit evidence statuses, notes, answered count, elapsed minutes, diagnostic facts, expected capabilities/gates/findings, and reviewer actionability flags.
4. Implement the thin offline runner and golden assertions; calculate per-scenario and aggregate within-one-level ratios and reject <85%, <90% completion, >60 minutes, missing gate explanation, or un-actionable critical finding.
5. Define and render the 12 ordered report sections to canonical JSON and standalone HTML with inline/local-only CSS and no external URLs; run twice and compare bytes.
6. Conduct a structured calibration review: ambiguous anchors, largest rating deltas, unreasonable gates, false finding priorities, report usability; change content only with regenerated goldens and recorded rationale.
7. Record the Phase 1 evidence summary and migration fixture freeze. Gate Phase 2 on all success criteria, without claiming independent audit approval.

## Todo list

- [ ] Write 30 fully anchored questions across all 10 domains.
- [ ] Encode all gate and finding prototype content.
- [ ] Add eight rater fixtures and four expected-output fixtures.
- [ ] Prove completion, timing, coverage, calibration, gate, and actionability metrics.
- [ ] Generate deterministic 12-section JSON/HTML for every scenario.
- [ ] Review ambiguous anchors and freeze `0.1.0-prototype` migration inputs.

## Success Criteria

- All 10 domains and 30 questions validate; all 150 anchors exist and are observable.
- Four scenarios finish ≤60 minutes, answer ≥90%, and produce expected capability/gate/finding outcomes.
- At least 85% paired ratings are within one maturity level; planned fixture expectation is 118/120 (98.3%).
- Every capability output has independent confidence; every critical finding has impact, priority, recommendation, and architecture.
- All gate traces explain pre-gate state, applied cap, final state, and inputs.
- `report.json`/`report.html` contain all 12 sections and are byte-stable across two runs.
- No web code, golden-pipeline change, heavy service, customer data, or demo-derived maturity is introduced.

## Risk Assessment

- Anchors may be technically precise but interview-hostile; mitigate with timed two-rater walkthrough and wording review.
- Median aggregation could conceal a critical diagnostic; gates use explicit facts/capability thresholds and traces.
- Golden fixtures can overfit; preserve four contrasting personas and mutation tests for each gate.
- Prototype contracts may drift; freeze inputs and require explicit Phase 2 migration.
- Rollback: remove only the prototype runner/generated outputs and its additive Make targets; preserve the frozen synthetic fixtures as migration evidence. No data-platform or engagement source file is touched.

## Security Considerations

Use synthetic organizations and invented evidence notes only. Reject HTML in authored scenario fields, escape all report content, load no remote assets, and scan generated reports for secrets/absolute paths. The prototype opens no sockets and reads/writes only explicit fixture/output roots.

## Next steps

Request focused Phase 1 review. If every phase gate passes, begin Phase 2 contracts and migration; otherwise revise rubric/content and rerun calibration before any UI or golden work.
