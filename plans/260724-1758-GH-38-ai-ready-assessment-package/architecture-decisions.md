# Architecture decisions and implementation contract

## Authority and current-state split

Planning baseline is commit `58a9b7f45f5b2d473a39bc2f9eb9258fe92d0b2a`. Repository facts already proven and reusable:

- `data-generator/generate.py` emits 18 deterministic retail CSVs and `data/raw/manifest.json`.
- `ingestion/load_raw.py` lands 18 `raw.*` DuckDB tables; `make health` validates read-only opening.
- `transform/dbt/` contains 51 models: 18 staging, 6 ephemeral intermediate, 7 dimensions, 9 facts, 11 marts; `make dbt` runs models and tests.
- `lake/curated_assets.json` is the canonical 11-mart inventory used by Parquet/Rill/Iceberg paths.
- `orchestration/airflow/dags/retail_batch_pipeline.py` uses Airflow 3 `airflow.sdk` TaskFlow.
- `governance/openmetadata/` proves 45 materialized logical tables/130 lineage edges and 11 physical Iceberg assets.
- `docker-compose.yml` limits Airflow 4g; MinIO 1g/init 256m; Lakekeeper DB/migration 512m each/server 1g; OpenMetadata DB 1g/search **1g**/server **2g**.

Not proven and therefore Issue #38 work: architect-led assessment contracts/content/store/engine/report/web/catalog; explicit quarantine; PII classification plus masking/access-policy evidence; AI-ready dataset manifest; demo-stage manifests. Existing sandbox proof is demo evidence only and cannot become customer maturity evidence.

## Plan decisions

- **PD-01 — Minimal application stack.** Use Python 3.12, Pydantic/domain models, FastAPI, Jinja2, local CSS, minimal vanilla JS, pytest, and bounded Playwright. Bind to `127.0.0.1` only. Reason: one application runtime, offline operation, accessible server-rendered workflow, small attack surface. Defer a SPA, Node application runtime, and frontend build pipeline; PD-14 permits only a pinned build-time Mermaid renderer for reviewed SVG assets.
- **PD-02 — Dependency isolation.** Add `assessment/pyproject.toml`, locked runtime/dev requirement files, and `.assessment-venv/`; never mix web/test dependencies into `.venv/`. Record verified versions in `versions.md`.
- **PD-03 — Three independent cores.** Keep assessment engine, knowledge/architecture catalog, and golden demo evidence as separate namespaces joined by typed references. Only architect-entered assessment answers/evidence feed maturity.
- **PD-04 — Versioned content, no UI business logic.** Store safe YAML/Markdown beneath version directories and validate it with JSON Schema plus semantic cross-reference checks. UI/engine resolve IDs and versions; questions, anchors, gates, recommendations, mappings, report sections, and demo stages are not hard-coded in routes/templates.
- **PD-05 — Authoritative folder store.** Engagement folder is authority; `LocalEngagementStore` implements a narrow `EngagementStore` protocol. JSON is canonical machine state, Markdown is safe authored content, all paths are relative, and writes use temp-file + fsync + atomic replace. SQLite is deferred to a disposable index/cache only.
- **PD-06 — Portable archive.** Export deterministic ZIP entries sorted lexically with normalized timestamps/modes and a canonical manifest of SHA-256/size/schema versions. Import validates fully before a staged atomic move and rejects traversal, absolute paths, symlinks, duplicates/case-fold collisions, oversize/count/depth limits, checksum mismatch, secrets, and unsupported versions.
- **PD-07 — Version compatibility.** Phase 1 fixtures use `0.1.0-prototype`; Phase 2 provides a pure, idempotent `0.1.0-prototype → 1.0.0` migration. Known older versions migrate through a registry; unknown newer versions fail closed without mutating the source.
- **PD-08 — Deterministic maturity.** Ratings are integer 0–4 or not assessed. Framework v1 requires at least two of three quick answers in every domain and at least 27 of 30 overall. Each domain score is the unweighted lower median (`median_low`) of its answered ratings. The pre-gate readiness level is `floor(mean(all 10 domain scores))`; the presentation-only 0–100 value is `mean * 25`. No readiness/overall value is emitted if any domain misses coverage. These algorithms, domain order, and future version changes remain explicit versioned framework content; domain scores are the source of truth.
- **PD-09 — Independent confidence.** Every answer records one of Self-reported, Partially evidenced, Evidenced, Conflicting evidence, Not assessed. Capability confidence reports the full distribution and the least-assured assessed status using `Conflicting evidence → Self-reported → Partially evidenced → Evidenced`; Not assessed is reported as coverage rather than silently ranked. Confidence changes claim language/evidence actions, never maturity.
- **PD-10 — Explainable readiness gates.** Versioned rules emit rule ID, inputs, pre-gate state, cap, final state, and explanation. Quality ≤1 or security/privacy ≤1 caps readiness at 1; governance/ownership ≤1 caps 2; missing critical lineage blocks production-ready; missing reproducibility/versioning limits experiment-ready.
- **PD-11 — Deterministic findings/recommendations.** Rule/content IDs connect gap → impact → priority → recommendation → logical architecture → vendor-neutral technology options → optional AWS mapping → demo evidence → action. V1 priority is ordinal: a gate-to-level-1 or production-readiness blocker is `Critical blocker`; an ungated domain ≤1 or cross-domain dependency blocker is `High-priority foundation`; domain 2 is `Near-term improvement`; domain 3 with an accepted level-4 target is `Strategic enhancement`; level 4 has no gap finding unless an explicit risk rule fires. Confidence adds an evidence-validation action but never changes maturity or priority. Demo references explain a pattern and never alter score, priority, gate, or confidence.
- **PD-12 — Report output.** Canonical `report.json` and one self-contained `report.html` are required. The 12 ordered sections are executive summary, readiness, capability heatmap, gates, confidence, blockers, findings, target state, reference diagrams, roadmap, technology options, evidence appendix. The Jinja template and CSS are versioned framework content selected by the engagement's framework version, while Python only validates and renders the report model. Defer a PDF renderer; browser print-to-PDF is guidance only.
- **PD-13 — Web boundary.** FastAPI/Jinja2 supplies create → quick assess → review → deep-dive select → report → export → import on loopback. Pages use progressive enhancement, CSRF protection, restrictive headers, no CDN/telemetry, bounded upload, escaped Markdown, and no pipeline-control endpoint.
- **PD-14 — Diagrams by audience.** Maintain Mermaid source plus reviewed SVG for executive readiness, logical platform context, engagement lifecycle, scoring/gates, security/access, metadata/lineage, and demo evidence mapping. Do not collapse them into one poster.
- **PD-15 — Golden evidence reuse.** Extend existing retail pipeline only for missing quarantine, PII classification/masking/access policy, AI-ready manifest, Demo Guide, and stage manifests. Web reads validated artifacts; it never invokes `make`, subprocesses, Docker, Airflow, or pipeline scripts.
- **PD-16 — Bounded access-policy proof.** Compatibility-spike a local policy-enforced safe export. Default implementation is a checked policy file plus an export entrypoint that allows the masked customer projection and denies raw PII. Label it local demonstration control, not production IAM. If the spike disproves feasibility, stop Phase 6 for owner review rather than claiming enforcement.
- **PD-17 — Extension boundary.** A recipe is inert versioned content conforming to the same framework extension schema. Loading a sample future recipe must not change engine/core engagement schemas; no second industry pipeline is built.
- **PD-18 — Resource and cleanup policy.** Assessment commands are process-local and start no containers. Golden verification runs core, then Airflow/lake/governance one at a time; only `make catalog-ingest` may use the existing guarded lake+governance window and it stops Airflow. `make assessment-clean` removes generated reports/cache/tmp/browser artifacts but preserves engagement sources and evidence.
- **PD-19 — Cloud and persistence alternatives.** Define a future `ObjectEngagementStore` interface contract only. Defer S3 implementation/upload, cloud resources, Terraform, hosted service, auth, collaboration, portfolio dashboards, database authority, and multi-tenancy.
- **PD-20 — Compatibility/rollback.** Changes are additive. Existing public commands and data contracts remain; new schemas are versioned. Roll back by removing assessment targets/package and golden additions, then regenerate existing ignored artifacts. Never delete engagement folders in cleanup.
- **PD-21 — First implementation profile.** The catalog's first named implementation profile is AWS, while all maturity criteria remain vendor-neutral. V1 maps one tool per role: S3 object storage; Glue Data Catalog; Athena query; Lake Formation access governance (IAM supplies identities/policies rather than a competing access product); dbt Core with the Athena adapter for transformation; Soda Core for quality; OpenMetadata for metadata/lineage; Apache Superset for analytics; Terraform as reviewed infrastructure source only; and the existing deterministic generator for synthetic data. This issue authors/validates mapping content only—no SDK calls, credentials, Terraform/AWS apply, or deployment. The existing DuckDB/dbt/Rill/Airflow/Lakekeeper/OpenMetadata stack is a separate local demo-evidence profile, not the maturity model or a second tool choice inside the AWS profile; alternatives are catalog content.

## Proposed implementation surface

```text
assessment/
  pyproject.toml
  requirements.lock
  requirements-dev.lock
  contracts/{framework,engagement,answer,report,recipe}-v1.schema.json
  content/frameworks/1.0.0/{framework.yaml,gates.yaml,finding-rules.yaml,recommendations.yaml}
  content/frameworks/1.0.0/{capabilities,questions,deep-dives}/*.yaml
  content/frameworks/1.0.0/report-templates/{report.html.j2,report.css}
  content/catalog/1.0.0/{architectures,technology-mappings,diagrams}/*
  content/demo/1.0.0/{stages.yaml,evidence-links.yaml}
  src/assessment/{__main__.py,cli.py,config.py}
  src/assessment/domain/{models.py,versions.py}
  src/assessment/content/{loader.py,schemas.py,semantics.py,markdown.py}
  src/assessment/storage/{protocol.py,local.py,migrations.py,archive.py,hygiene.py}
  src/assessment/engine/{maturity.py,confidence.py,gates.py,findings.py,recommendations.py}
  src/assessment/reporting/{models.py,generator.py,renderer.py}
  src/assessment/catalog/{models.py,loader.py}
  src/assessment/web/{app.py,csrf.py,routes.py,templates/,static/}
  tests/{unit,contract,scenario,integration,e2e,fixtures}/
demo/
  contracts/{demo-stage-manifest,ai-ready-dataset-manifest}-v1.schema.json
  manifests/
```

Golden additions are scoped to `transform/dbt/models/quarantine/`, a masked safe mart, `governance/policy/`, `demo/contracts/`, `demo/manifests/`, and `docs/demo-guide.md`; exact files are in Phase 6.

## Engagement folder protocol

```text
<engagement>/
  engagement.json
  assessment/quick.json
  assessment/deep-dives/<capability-id>.json
  evidence/index.json
  evidence/files/<sanitized-name>
  selections/deep-dives.json
  findings/review.json
  reports/report.json
  reports/report.html
  metadata/checksums.json
```

`engagement.json` pins engagement schema, framework, catalog, and demo-content versions. Evidence records source, status, relative file reference, digest, and architect notes. Generated reports may be replaced; answer/evidence/review source files may not be removed by cleanup.

## Commands contract

Implementation adds exact Make targets delegating to `.assessment-venv/bin/python -m assessment`:

```text
make assessment-install
make assessment-test
make assessment-schema
make assessment-contract
make assessment-scenarios
make assessment-calibration
make assessment-import-export
make assessment-report
make assessment-lint
make assessment-typecheck
make assessment-build
make assessment-web
make assessment-e2e
make assessment-portability
make assessment-security-scan
make assessment-clean-checkout
make assessment-clean
```

`assessment-web` is the only long-running target and prints the loopback URL; browser tests launch/tear it down themselves. `assessment-build` builds a wheel/sdist and validates installed CLI/content inclusion. Existing regression remains `make seed SCALE=small SEED=42 && make load && make health && make dbt && make bi`.

## Genuine blocking questions

1. **BQ-01 — Implementation authorization:** has the owner-required independent combined plan-readiness audit completed and has the issue received the corresponding implementation authorization? Until yes, this package is plan-only.
2. **BQ-02 — Access-control feasibility only if spike fails:** if the Phase 6 bounded safe-export control cannot prove allow/deny behavior on the pinned local stack, should scope add a compatible enforcement dependency or explicitly defer stage-level access-control acceptance? Do not choose silently or mislabel policy documentation as enforcement.

No other question blocks planning; dependency pins, exact UI wording, diagram styling, and sample recipe label are reversible implementation details.
