# Phase 1 implementation evidence

Status: implementation, focused reviews, and independent post-cook verification complete

## Provenance and boundary

- GitHub issue: #38.
- Implementation input and audited-plan SHA:
  `0b5335d907397bb8fd4f7a8c794ff2e930b6fe6b`.
- Branch: `feature/issue-38-phase-1-rubric-calibration`.
- Base: `integration/issue-5-local-learning`.
- Scope: the bounded `0.1.0-prototype` rubric, runner, synthetic calibration,
  local reports, tests, bootstrap, and documentation only.
- Excluded: all Phase 2+ persistence, migration service, import/export, web,
  catalog, golden-pipeline, demo-manifest, S3, cloud, deployment, customer-data,
  learning-portal, and lab work.

The frozen migration manifest covers 18 versioned YAML/JSON inputs and has
aggregate SHA-256
`302011ab87f8e38294eef7ae0e3a7514edf05bc9e24b3a0eee5c1b1afb5f113b`.

## Calibration review

- Content inventory: 10 confirmed domains, 50 observable domain anchors, 30
  questions, and 150 question-specific anchors.
- Comparable-rating denominator: 119 of 120 slots. The one Not-assessed slot is
  coverage, not a disagreement.
- Agreement: 117 of 119 comparable ratings are within one level (`98.3%`).
- Largest deltas: `Q-STR-02` and `Q-AID-01` in
  `strong-engineering-no-ai-operating-model`, both delta 2.
- Paired result checks: 40 domain results and 4 final-readiness results; every
  paired delta is at most one.
- Anchor review: all anchors describe observable states and retain distinct
  0–4 progression. The two largest-delta anchors were reviewed against the
  architect notes; their disagreement represents deliberately different
  interpretation of operating ownership and AI-data controls, so wording was
  retained and the calibration result remains above the 85% threshold.
- Gate reasonableness: all seven gates are independently traced. Quality,
  security, and privacy cap at 1. Governance, ownership, lineage, and
  reproducibility cap at 2 and are explicitly tested from pre-gate level 3.
- Priority reasonableness: a versioned decision table assigns triggered gates
  as Critical blockers and ungated/cross-domain AI operating gaps as foundation
  work. Confidence remains separate from maturity and adds an evidence
  validation action to each finding.
- Report usability: all four personas and both raters complete in 35–48 minutes
  with 29–30 answers. Reports expose the readiness calculation, seven gate
  explanations, confidence, blockers, findings, target state, architecture
  placeholders, roadmap, technology options, and evidence appendix in the
  canonical 12-section order.

## Audited-plan discrepancy

Enterprise Architect B's audited domain array is
`[2,2,3,3,0,2,2,2,1,2]`. It sums to 19, so the authoritative formula produces
`floor(19 / 10) = 1` and final readiness 1. The plan sentence claiming both
enterprise raters have pre-gate level 2 is arithmetically inconsistent. The
source ratings, formula, recomputed fixture expectation, and tests therefore
retain `1/1`; no output was hard-coded to match the prose.

## Verification record

The following Phase 1 commands were run with exit code 0. All commands except
dependency acquisition execute through `assessment/tools/run-offline.sh`,
which uses the macOS sandbox to deny outbound network access.

| Command | Result |
|---|---|
| `make assessment-install` | Hash-locked environment installed |
| `make assessment-schema` | 10 domains, 50 domain anchors, 30 questions, 150 question anchors |
| `make assessment-contract` | 48 expected-result assertions across 8 raters |
| `make assessment-scenarios` | 8 raters complete; 29–30 answers; 35–48 minutes |
| `make assessment-calibration` | 117/119, 98.3%; 1 Not-assessed slot separate |
| `make assessment-report` | 36 artifacts; two-run byte stability true |
| `make assessment-test` | 33 passed, including inherited-`PYTHONPATH` isolation regression |
| `make assessment-lint` | Ruff clean |
| `make assessment-typecheck` | strict mypy clean, 2 source files |
| `make assessment-build` | wheel and sdist built; all 8 required packaged assets verified |

### Independent post-cook completion gate

A fresh clean-install rerun after the cook worker exited exposed one environment-isolation defect: `assessment-build` inherited Hermes' `PYTHONPATH`, so Python resolved `setuptools 79.0.1` from the host agent environment instead of the hash-locked `setuptools 80.9.0` inside `.assessment-venv`. The shared offline wrapper now removes inherited `PYTHONPATH` before invoking `sandbox-exec`. A real subprocess regression starts the wrapper with a deliberately contaminated path and proves the child cannot observe it. The regression was verified RED before the fix and GREEN afterward. The full Phase 1 suite, build, Docker Compose configuration, and 12 actual Python entrypoint compile checks then passed again.

Generated local-only artifacts are under
`assessment/.generated/prototype/<scenario>/`, with a canonical
`report.json`, standalone `report.html`, and `summary.json` for each persona
and separate Architect A/B report sets. Build artifacts are under
`assessment/dist/`. Both locations are ignored and regenerated rather than
manually edited.

Representative Architect A report JSON SHA-256 values:

- startup:
  `fd7272a43378196bfa571d711e2eaea8745bc1eb0c3d4421712392539b0d8176`
- enterprise:
  `ed1faa2c63056155849a82ae70676ed486612a9982321ca96d8c980d56615f98`
- manual governance:
  `5b287e6d82dbb3f56fb9a02b43c027e4b8a023ada0e14c698db94ddfd1feae9a`
- strong engineering:
  `3630473523a4372f06db8bacb7f843898685355da9428e78afb842a2b694efe1`

Safety assertions reject missing/duplicate IDs, missing 0–4 anchors, incorrect
counts, incomplete coverage, malformed diagnostic facts, missing or altered
gate semantics/explanations, malformed finding conditions, unsafe authored
text, external URLs, secrets, and POSIX/Windows absolute paths. Report checks
also reject active elements, linked assets, and event handlers.

## Runtime and review

- Python 3.12.3; pip 25.1.1.
- Runtime: Jinja2 3.1.6, MarkupSafe 3.0.3, PyYAML 6.0.2.
- Development: pytest 8.4.1, Ruff 0.12.4, mypy 1.16.1,
  types-PyYAML 6.0.12.20260724, build 1.2.2.post1, setuptools 80.9.0,
  wheel 0.45.1, pip-tools 7.5.0.
- Initial spec review: 0 Critical, 5 Important. All five were corrected.
- Final spec-compliance review: PASS, 0 Critical, 0 Important.
- Initial code-quality review: 0 Critical, 2 Important, with one additional
  question/domain binding case found on re-review. Exact framework semantics,
  binding mutations, and complete standalone HTML evidence were corrected.
- Final code-quality review: PASS, 0 Critical, 0 Important.
- Exact pushed/tested PR-head SHA and CI state: recorded in the PR and Issue
  #38 publication evidence after the final commit is pushed.

## Residual conditions and rollback

- Offline enforcement uses `sandbox-exec` and is intentionally bounded to the
  audited macOS runtime. Dependency acquisition remains the only networked
  Phase 1 target.
- Reports and build outputs are disposable local artifacts.
- Rollback is removal/reversion of the additive `assessment/` package,
  assessment Make targets, ignore entries, and bounded documentation updates;
  no data or service migration is involved.
