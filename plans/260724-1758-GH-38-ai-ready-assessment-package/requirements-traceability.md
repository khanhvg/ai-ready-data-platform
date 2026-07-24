# Requirements traceability

IDs in this document are planning shorthand only. Do not use `AC-*`/`SM-*` in code comments, test names, migration names, or commits; implementation names must describe behavior.

## Issue acceptance criteria

| ID | Requirement | Implementation step(s) | Verification |
|---|---|---|---|
| AC-01 | Quick assessment covers 10 domains, ~30 anchored questions, ≤60 min | P1.2–P1.5; P5.1 | `make assessment-schema assessment-scenarios`; scenario timing record shows 30 questions, all 10 domains, each run ≤60 min |
| AC-02 | Every capability has maturity anchors 0–4 and separate confidence/evidence | P1.2–P1.4; P3.1–P3.2 | `make assessment-contract assessment-test`; semantic validator rejects any of 50 domain anchors, 150 question anchors, or statuses |
| AC-03 | Versioned explainable gates prevent critical gaps being hidden | P1.3–P1.5; P3.3 | `make assessment-scenarios assessment-test`; golden traces prove all seven independent gate rules and combined minimum-cap behavior |
| AC-04 | Findings link gap through action, architecture, options, demo; demo never scores | P1.3; P3.4; P5.2–P5.4; P7.1 | `make assessment-contract assessment-test`; mutation test changes demo manifest with identical maturity/readiness output |
| AC-05 | Framework content versioned outside UI logic | P2.1–P2.2; P4.1 | `make assessment-contract`; route/template grep plus content-version isolation test |
| AC-06 | Portable relative-path folder, versions, import/export, no secrets/absolute paths | P2.3–P2.7; P8.2–P8.3 | `make assessment-import-export assessment-portability assessment-security-scan` |
| AC-07 | Local create→assess→review→select→report→export→import path | P4.1–P4.9 | `make assessment-e2e assessment-runtime-smoke`; reopened imported engagement matches source state and the runtime smoke retains report/transcript digests |
| AC-08 | Report contains all 12 required sections | P1.6; P3.5–P3.6 | `make assessment-report assessment-schema assessment-runtime-smoke`; JSON order/content and real standalone HTML checks |
| AC-09 | Prototype/calibrate ≥3 synthetic scenarios before major UI/golden work | P1.1–P1.8 phase gate | `make assessment-scenarios assessment-calibration`; P2 cannot start without recorded P1 pass |
| AC-10 | Separate reproducible golden evidence covers all required stages | P6.1–P6.11 | `make demo-contract demo-verify demo-airflow-verify`; staged lake/catalog commands per P6 plus manifest checksum and current-vs-historical evidence status |
| AC-11 | Future recipe added without engine/core-schema change | P7.6–P7.8 | `make assessment-contract assessment-test`; tree/hash proof shows only recipe fixture/content changes |
| AC-12 | Plan has traceability, modules, order, commands, smoke, rollback, docs | All phases; architecture decisions; this matrix | `reports/combined-plan-readiness-audit.md` structural/link/traceability checks plus verified Issue #38 `ready to cook` transition |

## Advisory success metrics

| ID | Metric | Implementation step(s) | Verification |
|---|---|---|---|
| SM-01 | Quick assessment ≤60 min and ≥90% answered | P1.4–P1.5 | Scenario summary: elapsed minutes and answered/30 ≥27 |
| SM-02 | 100% of 10 domains covered | P1.2; P2.2 | Semantic coverage assertion via `make assessment-contract` |
| SM-03 | Every domain and question anchored 0–4 | P1.2; P2.2 | Schema + semantic completeness test for 50 domain and 150 question anchors |
| SM-04 | Two architects within one level on ≥85% comparable ratings | P1.4–P1.5 | `make assessment-calibration`; explicit per-rater expectations, Not-assessed exclusion, comparable denominator/ratio, and ≤1 paired domain/final-readiness deltas |
| SM-05 | 100% capability scores show confidence/evidence | P3.2; P3.5 | Unit/report contract tests reject missing confidence |
| SM-06 | 100% critical findings include impact, recommendation, priority, architecture | P3.4; P5.2 | Contract/semantic tests over generated critical findings |
| SM-07 | AI-ready gates always applied and explained | P3.3 | Unit/property tests and scenario golden traces |
| SM-08 | HTML report needs no manual editing | P1.6; P3.5–P3.6; P4.8 | Byte-stable two-run generation plus artifact-producing headless runtime render |
| SM-09 | Copied folder reopens elsewhere without loss | P2.3–P2.7; P8.2 | `make assessment-portability` compares canonical source and regenerated report data |
| SM-10 | Zero credentials/tokens/absolute paths in exports | P2.6–P2.7; P8.3 | `make assessment-security-scan` covers secret, URI credential, opaque evidence, and POSIX/macOS/Windows paths |
| SM-11 | Golden pipeline ≥95% executable guide steps automated | P6.7–P6.10 | Demo Guide emits every executable step, eligibility rationale, numerator, and denominator; talk-track/browse items are listed separately |
| SM-12 | All nine golden stages demonstrated | P6.2–P6.10 | `make demo-contract demo-verify demo-airflow-verify` plus staged lake/catalog evidence; validator distinguishes current execution from historical proof |
| SM-13 | ≥1 failing record/rule detected and blocked from curated | P6.2 | invalid-status quarantine/accepted partition proves non-empty, disjoint, complete, and absent from accepted/governed outputs |
| SM-14 | ≥1 PII field classified and masked or access-controlled | P6.1, P6.3–P6.4 | classification contract, masked-output assertion, and real raw/staging-deny/safe-allow policy CLI test |
| SM-15 | Source-to-published-product lineage visible | P6.5; P7.1 | dbt/OpenMetadata manifest references and reviewed lineage SVG |
| SM-16 | Web displays every stage artifact without pipeline control | P4.6; P6.6; P7.5 | bounded Playwright stage-page test; route/subprocess deny-list inspection |
| SM-17 | One recipe changes neither engine nor core schema | P7.6–P7.8 | pre/post hashes and full contract/engine tests |

## Cross-cutting verification map

| Surface | Discoverable command | Starts heavy services? |
|---|---|---|
| Install | `make assessment-install` | No |
| Browser bootstrap | `make assessment-browser-install` | No containers; may fetch the pinned browser |
| Diagram-tool bootstrap | `make assessment-diagram-install` | No containers; build-only locked Node/Mermaid tools |
| Unit | `make assessment-test` | No |
| JSON Schema | `make assessment-schema` | No |
| Semantic contracts | `make assessment-contract` | No |
| Scenarios/calibration | `make assessment-scenarios assessment-calibration` | No |
| Import/export | `make assessment-import-export` | No |
| Report | `make assessment-report` | No |
| Lint/typecheck/build | `make assessment-lint assessment-typecheck assessment-build` | No |
| Diagram update/render parity | `make assessment-diagrams-update` (explicit mutation); `make assessment-diagrams` (non-mutating verification) | No; one build-only render at a time |
| Browser smoke | `make assessment-e2e` | No containers; loopback process is torn down |
| Architect runtime/report smoke | `make assessment-runtime-smoke` | No containers; loopback/browser are torn down |
| Portability/hygiene | `make assessment-portability assessment-security-scan` | No |
| Clean checkout | `make assessment-clean-checkout` | No for assessment slice |
| Existing core regression | `make seed SCALE=small SEED=42 && make load && make health && make dbt && make bi` | No |
| Demo contracts/core proof | `make demo-contract demo-verify` | No |
| Airflow execution proof | `make demo-airflow-verify` | Yes; Airflow alone, exact DAG triggered/polled/teardown |
| Heavy golden proof | `make lake-up && make lake-publish && make down`; guarded `make catalog-ingest && make down`, staged per P6/P8 | Yes, explicitly staged |
| Cleanup | `make assessment-clean`; existing `make down`; existing `make clean` only with engagement preservation check | No new services |
