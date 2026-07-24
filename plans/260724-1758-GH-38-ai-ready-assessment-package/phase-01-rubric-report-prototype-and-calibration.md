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

- Ten capability domains, each with observable maturity anchors 0–4, plus three quick questions per domain (30 total), each with separate observable scoring guidance 0–4.
- Completion target ≥27/30 and elapsed time ≤60 minutes per scenario.
- Two explicit architect rating fixtures per scenario; ≥85% of comparable paired ratings differ by no more than one level, while Not-assessed coverage is reported separately.
- Prototype gate trace covers low quality, low security/privacy, low governance/ownership, missing critical lineage, and missing reproducibility/versioning.
- Each critical finding contains gap, impact, priority, recommendation, and logical architecture reference.
- A deterministic 12-section `report.json` plus standalone `report.html` prototype.

## Architecture

Prototype files live under `assessment/prototype/0.1.0/` and `assessment/tests/fixtures/scenarios/0.1.0/`; no FastAPI, store, or golden pipeline dependency is introduced. A small `assessment/prototype/run.py` loads YAML/JSON, validates all anchors and references, applies median-of-assessed-answer capability aggregation with explicit configured coverage, emits gate traces/findings, and renders Jinja2 HTML. Phase 2 migrates these fixtures to `1.0.0`; Phase 3 replaces the prototype runner with domain services while preserving golden outputs.

Question order for the explicit arrays below is three questions for each confirmed advisory domain: Strategy, ownership, and operating model (`STR`); Data sources, ingestion, and integration (`ING`); Storage, lifecycle, and data organization (`STO`); Transformation and orchestration (`TRN`); Data quality and reliability (`QUA`); Metadata, catalog, glossary, and lineage (`LIN`); Governance, privacy, and compliance (`GOV`); Security, access control, and policy-as-code (`SEC`); Observability, operations, and cost management (`OPS`); Data products, analytics, and AI readiness (`AID`). `null` means Not assessed and does not count as an answered question.

Framework v1 requires at least two answered questions in every domain and at least 27/30 overall. A domain score is the unweighted lower median (`median_low`) of its answered ratings. The pre-gate readiness level is `floor(sum(all 10 domain scores) / 10)` with versioned labels `0 Not ready`, `1 Foundation blocked`, `2 Experiment-ready only`, `3 Production-ready`, and `4 Optimized production-ready`. The labeled 0–100 presentation value is exact `sum(domain scores) * 2.5`, rendered with one decimal place. No overall/readiness value is emitted if any domain misses coverage. Seven separate rules then evaluate quality, security, privacy, governance, ownership, critical lineage, and reproducibility/versioning; every rule emits a trace and the most restrictive cap wins. Privacy, ownership, lineage, and reproducibility gate inputs are explicit versioned diagnostic facts within `GOV`/`STR`/`LIN`/`AID`, not inferred from vendor products or demo artifacts.

| Fixture | Architect A ratings (30) | Architect B ratings (30) | Expected A domain maturity (STR…AID) | Expected B domain maturity (STR…AID) | Critical facts and expected outcome |
|---|---|---|---|---|---|
| `startup-no-governance` | `[2,2,1, 1,1,0, 1,1,1, 2,2,1, 2,1,1, 1,0,1, 1,1,1, 1,1,0, 1,1,0, 2,2,1]` | `[2,1,1, 1,0,0, 1,1,0, 2,1,1, 2,2,1, 1,1,0, 1,1,1, 1,0,0, 1,0,0, 2,1,1]` | `2,1,1,2,1,1,1,1,1,2` | `1,0,1,1,2,1,1,0,0,1` | `critical_lineage=false`, `reproducible_versioned=false`; A pre/final readiness is `1/1`, B is `0/0`; critical gates never raise a lower pre-gate result. Findings include ownership, quality, privacy, lineage, and reproducibility. |
| `enterprise-lake-weak-quality` | `[3,3,2, 3,3,2, 3,2,3, 3,3,3, 1,1,0, 3,3,2, 3,3,2, 3,3,2, 2,2,1, 2,2,2]` | `[3,2,2, 3,2,2, 3,3,2, 3,3,2, 1,0,0, 3,2,2, 3,2,2, 3,2,2, 2,1,1, 2,1,2]` | `3,3,3,3,1,3,3,3,2,2` | `2,2,3,3,0,2,2,2,1,2` | `critical_lineage=true`, `reproducible_versioned=true`; both pre-gate levels are 2 and quality caps both final results at 1 despite platform strength. Finding: quarantine and measurable quality ownership. |
| `manual-governance-missing-lineage` | `[2,2,2, 3,3,3, 2,2,2, 2,2,1, 2,2,1, 1,1,0, 2,2,2, 2,2,1, 2,2,1, 2,2,2]` | `[2,2,1, 3,3,2, 2,1,2, 2,1,1, 2,1,1, 1,0,0, 2,2,1, 2,1,1, 2,2,1, 2,2,1]` | `2,3,2,2,2,1,2,2,2,2` | `2,3,2,1,1,0,2,1,2,2` | `critical_lineage=false`, `reproducible_versioned=true`; production-ready is forbidden; A pre/final readiness is `2/2`, B is `1/1`. Findings include metadata/lineage and AI operating ownership. |
| `strong-engineering-no-ai-operating-model` | `[3,3,3, 3,3,2, 3,3,3, 4,3,3, 4,3,3, 3,3,3, 3,3,3, 3,3,2, 2,2,null, 1,1,0]` | `[3,1,3, 3,2,2, 3,2,3, 4,3,2, 4,3,2, 3,2,3, 3,2,3, 3,2,2, 2,1,null, 3,1,0]` | `3,3,3,3,3,3,3,3,2,1` | `3,2,3,3,3,3,3,2,1,1` | `critical_lineage=true`, `reproducible_versioned=false`; both pre/final results are `2/2`, limited to experiment-ready. Findings: versioned AI products, AI operating ownership, monitoring, reproducibility. |

Two comparable ratings differ by two in the fourth persona (`STR` and `AID`), intentionally making calibration non-trivial. The shared Not-assessed item is excluded from the rating denominator, so 117/119 comparable rating pairs are within one level (98.3%), above the ≥85% target; coverage is reported separately as 119 comparable pairs out of 120 question slots. The table records each rater's distinct expected domain scores and pre/final readiness; every paired domain score and final readiness differs by at most one level. Each fixture also supplies 30 evidence-status values, architect notes, expected confidence distributions, duration (35/42/48/39 minutes), and actionability review flags. The fourth fixture has 29/30 answered (96.7%) while still answering at least two questions in every domain; the others have 30/30.

## Related code files

- Create: `assessment/pyproject.toml`, `assessment/requirements{,-dev}.in`, `assessment/requirements{,-dev}.lock`, `assessment/tools/compile-locks.sh`
- Create: `assessment/prototype/0.1.0/{capabilities.yaml,quick-questions.yaml,readiness-levels.yaml,gates.yaml,finding-rules.yaml,recommendations.yaml}`
- Create: `assessment/prototype/{run.py,report-template.html.j2,report.css}`
- Create: `assessment/tests/fixtures/scenarios/0.1.0/{startup-no-governance,enterprise-lake-weak-quality,manual-governance-missing-lineage,strong-engineering-no-ai-operating-model}/{architect-a.json,architect-b.json,expected.json}`
- Create: `assessment/tests/scenario/test_prototype_scenarios.py`, `assessment/tests/scenario/test_calibration.py`
- Create generated/ignored: `assessment/.generated/prototype/<scenario>/{report.json,report.html,summary.json}`
- Modify: `Makefile` only to add isolated Phase 1 install/schema/scenario/calibration/report targets; no existing target behavior changes.

## Implementation Steps

1. Create the bounded Python 3.12 package/bootstrap skeleton, pin the lock compiler, generate hash-locked runtime/dev requirements, and prove `make assessment-install` in a fresh `.assessment-venv`; bootstrap may use the package index, while all Phase 1 verification runs with outbound network blocked.
2. Define the 10-domain rubric with 50 observable non-vendor domain anchors and exactly 30 quick questions with 150 separate scoring anchors; semantic validation requires every level, stable ID, and domain coverage.
3. Encode the v1 lower-median/coverage/readiness labels and decimal presentation algorithm, confidence precedence, seven independently traced gates, the ordinal finding-priority decision table, recommendations, and architecture placeholders as versioned content.
4. Materialize both-rater fixtures above with explicit evidence statuses, notes, answered count, elapsed minutes, diagnostic facts, per-rater expected capabilities/pre-gate/final readiness/gates/findings, and reviewer actionability flags.
5. Implement the thin offline runner and golden assertions; calculate per-scenario comparable-pair denominators and aggregate within-one-level ratios, assert each paired domain/final readiness differs by at most one level, and reject <85%, <90% completion, >60 minutes, missing gate explanation, or un-actionable critical finding.
6. Define and render the 12 ordered report sections to canonical JSON and standalone HTML with inline/local-only CSS and no external URLs; run twice and compare bytes.
7. Conduct a structured calibration review: ambiguous anchors, largest rating deltas, unreasonable gates, false finding priorities, report usability; change content only with regenerated goldens and recorded rationale.
8. Record the Phase 1 evidence summary and migration fixture freeze. Gate Phase 2 on all success criteria, without claiming independent audit approval.

## Todo list

- [ ] Bootstrap the isolated, hash-locked Python 3.12 prototype environment.
- [ ] Write 50 capability anchors and 30 questions/150 scoring anchors across all 10 domains.
- [ ] Encode all gate and finding prototype content.
- [ ] Add eight rater fixtures and four expected-output fixtures.
- [ ] Prove completion, timing, coverage, calibration, gate, and actionability metrics.
- [ ] Generate deterministic 12-section JSON/HTML for every scenario.
- [ ] Review ambiguous anchors and freeze `0.1.0-prototype` migration inputs.

## Success Criteria

- All 10 domains and 30 questions validate; all 50 domain anchors and 150 question scoring anchors exist and are observable.
- Four scenarios finish ≤60 minutes, answer ≥90%, and produce expected capability/gate/finding outcomes.
- At least 85% comparable paired ratings are within one maturity level; the fixture expectation is 117/119 (98.3%), with Not-assessed coverage reported separately; paired domain and final-readiness deltas are each ≤1.
- Every capability output has independent confidence; every critical finding has impact, priority, recommendation, and architecture.
- All seven gate traces explain operand source/value, pre-gate state, applied cap, and final state, including non-triggered rules.
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
