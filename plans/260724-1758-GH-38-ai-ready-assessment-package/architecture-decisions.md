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
- **PD-02 — Dependency isolation and reproducible bootstrap.** Phase 1 owns `assessment/pyproject.toml`, direct runtime/dev input files, hash-locked transitive requirement files, and `.assessment-venv/`; later phases extend those same files rather than creating a second package boundary. A pinned lock compiler command regenerates locks only intentionally; normal installation uses `python3.12 -m venv` and `pip install --require-hashes -r ...`. Dependency/bootstrap targets may access the package index and the separate pinned Playwright Chromium download; after bootstrap, schema/unit/scenario/report/browser/runtime tests run with outbound network blocked. An offline install is supported only when a documented, checksum-verified wheel/browser cache is supplied—clean checkout must not claim a cache-free offline install. Never mix assessment dependencies into `.venv/`. Record Python, lock-compiler, application, test, and browser versions in `versions.md`; run Playwright with one worker and one browser instance on the 16GB Mac profile.
- **PD-03 — Three independent cores.** Keep assessment engine, knowledge/architecture catalog, and golden demo evidence as separate namespaces joined by typed references. Only architect-entered assessment answers/evidence feed maturity.
- **PD-04 — Versioned content, no UI business logic.** Store safe YAML/Markdown beneath version directories and validate it with JSON Schema plus semantic cross-reference checks. Versioned JSON Schemas are the public contract authority; Pydantic/domain models are consumers and must pass schema/model parity fixtures so they cannot silently narrow, widen, or rename the contract. UI/engine resolve IDs and versions; questions, domain/question anchors, readiness labels, gate operands/rules, recommendations, mappings, report sections, and demo stages are not hard-coded in routes/templates.
- **PD-05 — Authoritative folder store.** Engagement folder is authority; `LocalEngagementStore` implements a narrow `EngagementStore` protocol. JSON is canonical machine state, Markdown is safe authored content, all paths are relative, and writes use temp-file + fsync + atomic replace. SQLite is deferred to a disposable index/cache only.
- **PD-06 — Portable archive and evidence admission.** Export deterministic ZIP entries sorted by normalized NFC POSIX path, using `ZIP_STORED`, the fixed ZIP epoch, normalized modes, canonical JSON, and a manifest of SHA-256/size/schema versions. The manifest's overall digest is defined over the canonical entry records excluding the manifest entry/digest field, avoiding a self-referential checksum. V1 limits are versioned and tested: at most 1,024 entries, path depth 16, 32 MiB per file, 128 MiB total expanded bytes, and 100:1 maximum expanded-to-compressed ratio; imports also reject encrypted/unsupported ZIP features and enforce expanded-byte/ratio limits while streaming rather than trusting central-directory sizes. Evidence exported in v1 is limited to normalized UTF-8 text/JSON/CSV and re-encoded PNG/JPEG with metadata removed; PDF, nested archives, executables, and other opaque formats remain referenced as unavailable/excluded until a safe canonicalizer exists. Text and canonicalized image bytes receive secret/path scanning; any unscannable or suspicious attachment fails export with a field/path diagnostic rather than being silently omitted. Import validates fully before a staged same-filesystem atomic move and rejects traversal, absolute/drive/UNC paths, NUL/backslash ambiguity, archive or pre-existing symlinks, non-regular entries, duplicate/Unicode/case-fold collisions, destination collision/overwrite, size/count/depth/ratio limits, checksum mismatch, secrets, and unsupported versions. Export never follows evidence symlinks.
- **PD-07 — Version compatibility.** Phase 1 fixtures use `0.1.0-prototype`; Phase 2 provides a pure, idempotent `0.1.0-prototype → 1.0.0` migration. Known older versions migrate through a registry; unknown newer versions fail closed without mutating the source.
- **PD-08 — Deterministic maturity and readiness semantics.** Ratings are integer 0–4 or not assessed. Each of the 10 assessed domains has its own observable 0–4 capability anchors, and each of the 30 questions has separate 0–4 scoring guidance. Framework v1 requires at least two of three quick answers in every domain and at least 27 of 30 overall. Each domain score is the unweighted lower median (`median_low`) of its answered ratings. The pre-gate readiness level is `floor(sum(all 10 domain scores) / 10)`. Versioned labels are `0 Not ready`, `1 Foundation blocked`, `2 Experiment-ready only`, `3 Production-ready`, and `4 Optimized production-ready`; production-ready therefore means level ≥3. The presentation-only 0–100 value is the exact decimal `sum(domain scores) * 2.5`, serialized with one decimal place, and is never substituted for the readiness level. No readiness/overall value is emitted if any domain misses coverage. These algorithms, anchors, labels, domain order, and future version changes remain explicit versioned framework content; domain scores are the source of truth.
- **PD-09 — Independent confidence.** Every answer records one of Self-reported, Partially evidenced, Evidenced, Conflicting evidence, Not assessed. Capability confidence reports the full distribution and the least-assured assessed status using `Conflicting evidence → Self-reported → Partially evidenced → Evidenced`; Not assessed is reported as coverage rather than silently ranked. Confidence changes claim language/evidence actions, never maturity.
- **PD-10 — Explainable readiness gates.** Seven independently traced v1 rules emit rule ID/version, exact operand ID/value/source question or diagnostic fact, pre-gate state, cap, final state, and explanation: quality domain ≤1 caps 1; security domain ≤1 caps 1; the explicit privacy critical fact ≤1 caps 1; governance domain ≤1 caps 2; the explicit ownership critical fact ≤1 caps 2; missing critical-dataset lineage caps 2 (not production-ready); and missing reproducibility/versioning caps 2 (experiment-ready only). Privacy, ownership, lineage, and reproducibility are required versioned diagnostic facts answered by the architect and never inferred from products or demo artifacts. All rules evaluate, the minimum cap wins, and the selected assessment profile pins the gate bundle/version in `engagement.json`; unknown profile/rule versions fail validation.
- **PD-11 — Deterministic findings/recommendations.** Rule/content IDs connect gap → impact → priority → recommendation → logical architecture → vendor-neutral technology options → optional AWS mapping → demo evidence → action. V1 priority is ordinal: a gate-to-level-1 or production-readiness blocker is `Critical blocker`; an ungated domain ≤1 or cross-domain dependency blocker is `High-priority foundation`; domain 2 is `Near-term improvement`; domain 3 with an accepted level-4 target is `Strategic enhancement`; level 4 has no gap finding unless an explicit risk rule fires. Confidence adds an evidence-validation action but never changes maturity or priority. Demo references explain a pattern and never alter score, priority, gate, or confidence.
- **PD-12 — Report output.** Canonical `report.json` and one self-contained `report.html` are required. The 12 ordered sections are executive summary, readiness, capability heatmap, gates, confidence, blockers, findings, target state, reference diagrams, roadmap, technology options, evidence appendix. The Jinja template and CSS are versioned framework content selected by the engagement's framework version, while Python only validates and renders the report model. Defer a PDF renderer; browser print-to-PDF is guidance only.
- **PD-13 — Web boundary.** FastAPI/Jinja2 supplies create → quick assess → review → deep-dive select → report → export → import on loopback. Pages use progressive enhancement, CSRF protection, restrictive headers, no CDN/telemetry, bounded upload, escaped Markdown, and no pipeline-control endpoint.
- **PD-14 — Diagrams by audience and bounded renderer.** Maintain Mermaid source plus reviewed SVG for executive readiness, logical platform context, engagement lifecycle, scoring/gates, security/access, metadata/lineage, and demo evidence mapping. A build-only `assessment/diagram-tools/package.json`/lock pins the Mermaid CLI and tested Node major; `make assessment-diagram-install` may fetch only that locked toolchain. `make assessment-diagrams-update` is the explicit maintainer mutation that renders one file at a time with remote fetches disabled, normalizes SVG metadata, and writes the source/tool/output digest manifest. The verification target `make assessment-diagrams` renders to a temporary directory and compares committed SVG/manifest parity without modifying the worktree. The Python application, browser UI, and report runtime never require Node or Mermaid. Do not collapse the views into one poster.
- **PD-15 — Golden evidence reuse.** Extend existing retail pipeline only for missing quarantine, PII classification/masking/access policy, AI-ready manifest, Demo Guide, and stage manifests. Web reads validated artifacts; it never invokes `make`, subprocesses, Docker, Airflow, or pipeline scripts.
- **PD-16 — Bounded access-policy proof.** Compatibility-spike one explicit application authorization boundary: a versioned checked YAML policy maps a fixed demo role and logical asset IDs to allow/deny decisions; a Python export entrypoint accepts only role ID, asset ID, and fixed output root, opens DuckDB internally, permits the masked governed product, rejects raw/staging/customer-PII asset IDs before query construction, accepts no SQL/path/table expression, and exits nonzero on denial. Tests invoke the real CLI, prove raw denial, safe allowance, output-column constraints, unknown-role/asset denial, and absence of a web route. Label this an application-level local demonstration control; the local OS user can still open DuckDB directly, so it is not database IAM or production enforcement. If the pinned Python/DuckDB stack cannot enforce this boundary exactly, or any bypass is found, stop Phase 6 for BQ-02—do not substitute a policy document or test-only mock.
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
make assessment-browser-install
make assessment-diagram-install
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
make assessment-diagrams
make assessment-diagrams-update
make assessment-web
make assessment-e2e
make assessment-runtime-smoke
make assessment-portability
make assessment-security-scan
make assessment-clean-checkout
make assessment-clean
make demo-contract
make demo-verify
make demo-airflow-verify
```

`assessment-install` provisions the locked Python environment and may fetch packages; `assessment-browser-install` separately provisions the pinned Chromium build and may fetch it; `assessment-diagram-install` provisions the locked build-only Mermaid/Node dependencies. Every verification target after those bootstrap targets blocks outbound network. `assessment-web` is the only intentionally long-running target and prints the loopback URL; browser/runtime tests launch and tear it down themselves. `assessment-build` builds a wheel/sdist and validates installed CLI/content inclusion. `assessment-diagrams-update` is an explicit maintainer mutation; `assessment-diagrams` is its non-mutating render/parity gate. Neither is a frontend build or application runtime step. `demo-contract` validates schemas/manifests without services; `demo-verify` validates the lightweight core, quarantine/accepted partition, policy, manifests, and reuse links; `demo-airflow-verify` starts Airflow alone, waits healthy, triggers the default generate→load→transform→serve DAG, polls the exact run to terminal success, captures task states, and tears Airflow down on success/failure. Existing regression remains `make seed SCALE=small SEED=42 && make load && make health && make dbt && make bi`.

## Genuine blocking questions

1. **BQ-01 — Implementation authorization:** has the owner-required independent combined plan-readiness audit completed and has the issue received the corresponding implementation authorization? Until yes, this package is plan-only.
2. **BQ-02 — Access-control feasibility only if spike fails:** if the Phase 6 bounded safe-export control cannot prove allow/deny behavior on the pinned local stack, should scope add a compatible enforcement dependency or explicitly defer stage-level access-control acceptance? Do not choose silently or mislabel policy documentation as enforcement.

No other question blocks planning; dependency pins, exact UI wording, diagram styling, and sample recipe label are reversible implementation details.
