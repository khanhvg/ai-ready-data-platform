# Requirements traceability

IDs in this document are planning shorthand only. Do not use `AC-*`/`SM-*` in code comments, test names, migration names, or commits; implementation names must describe behavior.

## Issue acceptance criteria

| ID | Requirement | Implementation step(s) | Verification |
|---|---|---|---|
| AC-01 | Quick assessment covers 10 domains, ~30 anchored questions, ≤60 min | P1.1–P1.4; P5.1 | `make assessment-schema assessment-scenarios`; scenario timing record shows 30 questions, all 10 domains, each run ≤60 min |
| AC-02 | Every capability has maturity anchors 0–4 and separate confidence/evidence | P1.1–P1.3; P3.1–P3.2 | `make assessment-contract assessment-test`; semantic validator rejects missing anchors/status |
| AC-03 | Versioned explainable gates prevent critical gaps being hidden | P1.2–P1.4; P3.3 | `make assessment-scenarios assessment-test`; golden traces prove all four gate rules |
| AC-04 | Findings link gap through action, architecture, options, demo; demo never scores | P1.2; P3.4; P5.2–P5.4; P7.1 | `make assessment-contract assessment-test`; mutation test changes demo manifest with identical maturity/readiness output |
| AC-05 | Framework content versioned outside UI logic | P2.1–P2.2; P4.1 | `make assessment-contract`; route/template grep plus content-version isolation test |
| AC-06 | Portable relative-path folder, versions, import/export, no secrets/absolute paths | P2.3–P2.7; P8.1–P8.3 | `make assessment-import-export assessment-portability assessment-security-scan` |
| AC-07 | Local create→assess→review→select→report→export→import path | P4.1–P4.7 | `make assessment-e2e`; reopened imported engagement matches source state |
| AC-08 | Report contains all 12 required sections | P1.5; P3.5–P3.6 | `make assessment-report assessment-schema`; JSON order/content and standalone HTML checks |
| AC-09 | Prototype/calibrate ≥3 synthetic scenarios before major UI/golden work | P1.1–P1.7 phase gate | `make assessment-scenarios assessment-calibration`; P2 cannot start without recorded P1 pass |
| AC-10 | Separate reproducible golden evidence covers all required stages | P6.1–P6.8 | `make demo-contract demo-verify`; staged existing commands per P6 and manifest checksum validation |
| AC-11 | Future recipe added without engine/core-schema change | P7.3–P7.5 | `make assessment-contract assessment-test`; tree/hash proof shows only recipe fixture/content changes |
| AC-12 | Plan has traceability, modules, order, commands, smoke, rollback, docs | All phases; architecture decisions; this matrix | Planner structural check now; independent audit remains required before implementation |

## Advisory success metrics

| ID | Metric | Implementation step(s) | Verification |
|---|---|---|---|
| SM-01 | Quick assessment ≤60 min and ≥90% answered | P1.3–P1.4 | Scenario summary: elapsed minutes and answered/30 ≥27 |
| SM-02 | 100% of 10 domains covered | P1.1; P2.1 | Semantic coverage assertion via `make assessment-contract` |
| SM-03 | Every question anchored 0–4 | P1.1; P2.1 | Schema + semantic completeness test |
| SM-04 | Two architects within one level on ≥85% questions | P1.3–P1.4 | `make assessment-calibration`; explicit paired fixtures and aggregate ratio |
| SM-05 | 100% capability scores show confidence/evidence | P3.2; P3.5 | Unit/report contract tests reject missing confidence |
| SM-06 | 100% critical findings include impact, recommendation, priority, architecture | P3.4; P5.2 | Contract/semantic tests over generated critical findings |
| SM-07 | AI-ready gates always applied and explained | P3.3 | Unit/property tests and scenario golden traces |
| SM-08 | HTML report needs no manual editing | P1.5; P3.5–P3.6 | Byte-stable two-run generation and headless standalone render |
| SM-09 | Copied folder reopens elsewhere without loss | P2.3–P2.7; P8.1 | `make assessment-portability` compares canonical source and regenerated report data |
| SM-10 | Zero credentials/tokens/absolute paths in exports | P2.6–P2.7; P8.2 | `make assessment-security-scan` covers secret, URI credential, POSIX/macOS/Windows paths |
| SM-11 | Golden pipeline ≥95% guide steps automated | P6.7–P6.8 | Demo Guide step manifest calculates automated/total; manual browse/talk steps excluded and labeled |
| SM-12 | All nine golden stages demonstrated | P6.2–P6.8 | Stage manifest validator requires ingestion, quality, quarantine, transformation, lineage, governance, access, serving, publication |
| SM-13 | ≥1 failing record/rule detected and blocked from curated | P6.2 | dbt quarantine assertion plus curated anti-join verification |
| SM-14 | ≥1 PII field classified and masked or access-controlled | P6.3–P6.4 | classification contract, masked-output assertion, raw-deny/safe-allow policy test |
| SM-15 | Source-to-published-product lineage visible | P6.5; P7.1 | dbt/OpenMetadata manifest references and reviewed lineage SVG |
| SM-16 | Web displays every stage artifact without pipeline control | P4.6; P6.6; P7.2 | bounded Playwright stage-page test; route/subprocess deny-list inspection |
| SM-17 | One recipe changes neither engine nor core schema | P7.3–P7.5 | pre/post hashes and full contract/engine tests |

## Cross-cutting verification map

| Surface | Discoverable command | Starts heavy services? |
|---|---|---|
| Install | `make assessment-install` | No |
| Unit | `make assessment-test` | No |
| JSON Schema | `make assessment-schema` | No |
| Semantic contracts | `make assessment-contract` | No |
| Scenarios/calibration | `make assessment-scenarios assessment-calibration` | No |
| Import/export | `make assessment-import-export` | No |
| Report | `make assessment-report` | No |
| Lint/typecheck/build | `make assessment-lint assessment-typecheck assessment-build` | No |
| Browser smoke | `make assessment-e2e` | No containers; loopback process is torn down |
| Portability/hygiene | `make assessment-portability assessment-security-scan` | No |
| Clean checkout | `make assessment-clean-checkout` | No for assessment slice |
| Existing core regression | `make seed SCALE=small SEED=42 && make load && make health && make dbt && make bi` | No |
| Heavy golden proof | Existing `make airflow`, `make lake-up && make lake-publish`, `make catalog-ingest`, staged per P6/P8 | Yes, explicitly staged |
| Cleanup | `make assessment-clean`; existing `make down`; existing `make clean` only with engagement preservation check | No new services |
