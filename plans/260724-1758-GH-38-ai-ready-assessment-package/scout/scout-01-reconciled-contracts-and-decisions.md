# Reconciled planner handoff

Date: 2026-07-24
Baseline: `58a9b7f45f5b2d473a39bc2f9eb9258fe92d0b2a`

## Corrections to research summaries

- The assessment product records architect-led customer engagements. It is not a repository-readiness scanner and must not infer customer maturity from this sandbox.
- Current Compose limits are Airflow `4g`; MinIO `1g`; MinIO init `256m`; Lakekeeper DB `512m`; Lakekeeper migration `512m`; Lakekeeper `1g`; OpenMetadata DB `1g`; OpenMetadata search `1g`; OpenMetadata server `2g`.
- Current dbt proof is 51 models total: 18 staging, 6 ephemeral intermediate, 7 dimensions, 9 facts, 11 marts. OpenMetadata shows 45 materialized logical tables because the 6 intermediate models are ephemeral.
- Existing quality tests surface controlled failures and staging deduplicates selected inputs, but there is no explicit quarantine dataset/zone contract.
- Existing customer email is synthetic PII-like data, but there is no proven classification plus masking/access-policy path.
- There is no versioned AI-ready dataset manifest, demo-stage artifact manifest, assessment framework, engagement schema, assessment engine, report generator, catalog UI, or application test harness.
- Commit `656322d` deliberately removed the learning portal, lab runner, learning contracts, broad architecture curriculum, and their tests. Do not copy or restore those product surfaces.

## Plan decisions for independent audit

These are evidence-backed and reversible; they are not new product authority.

1. **Application stack:** Python 3.12, a self-contained `assessment/` package, FastAPI loopback-only server, Jinja2 server-rendered pages, locally shipped CSS and minimal vanilla JavaScript, Pydantic/domain models, JSON Schema validation, pytest, and Playwright only for the bounded browser smoke. No SPA, Node runtime, database server, authentication, or container is required.
2. **Dependency isolation:** create `.assessment-venv/` and assessment-specific lock/install targets rather than adding web dependencies to the data-pipeline `.venv`; record tested versions in `versions.md`.
3. **Content format:** human-authored versioned YAML/Markdown plus JSON Schemas and semantic cross-reference checks. UI and engine resolve stable IDs and framework version; they contain no question, anchor, gate, finding, recommendation, mapping, report-section, or demo-stage business content.
4. **Storage:** engagement folder is authoritative. JSON documents and relative artifact paths are written atomically. A `LocalEngagementStore` implements a narrow store protocol; SQLite and S3 implementations are deferred. Export is a deterministic ZIP with manifest/checksums; import rejects traversal, symlinks, duplicate names, unsupported versions, oversize files, secrets, and absolute paths.
5. **Migration:** Phase 1 emits explicit `0.1.0-prototype` scenario engagements; Phase 2 supplies the supported migration to engagement schema `1.0.0`, plus unknown-newer rejection and non-mutating import validation.
6. **Scoring:** question answers are 0–4 or not assessed; maturity never includes confidence. A capability result requires configured coverage and is derived deterministically from its question ratings. The exact aggregation and tie/round rules live in versioned framework content and are golden-tested. The 0–100 executive value is a labeled presentation average only; readiness status is separately capped by versioned gates.
7. **Confidence:** preserve per-answer evidence status; capability/report summaries show the distribution plus a conservative status. Confidence changes assertion language/evidence actions, not the maturity value.
8. **Gates:** implement advisory v1 rules with stable rule IDs and an evaluation trace containing version, inputs, pre-gate result, cap, final result, and explanation. Missing lineage and reproducibility use explicit diagnostic facts, not product-presence inference.
9. **Reports:** canonical deterministic `report.json` plus standalone local `report.html`; HTML satisfies the advisory's HTML-or-PDF metric. PDF remains print-to-PDF guidance unless a later requirement justifies a renderer.
10. **Diagrams:** several small audience views with versioned Mermaid source and reviewed/rendered SVG: executive capability/readiness view, logical platform context, engagement lifecycle, scoring/gates flow, security/access flow, metadata/lineage flow, and demo evidence mapping. Do not create one poster.
11. **Golden evidence:** reuse the existing deterministic retail substrate and canonical files. Add only missing quarantine, PII classification/masking/access-policy evidence, AI-ready dataset manifest, and stage artifact manifests. Keep these demo facts in a separate evidence namespace and never use them as engagement maturity inputs.
12. **Technology profiles:** AWS is the first named implementation mapping with one selected tool per role, while the local evidence profile uses the current DuckDB/dbt/Rill/Airflow/Lakekeeper/OpenMetadata components plus one bounded access-policy mechanism selected in the compatibility spike. Both are content/evidence only in this issue; no Terraform/AWS apply. Alternatives stay in technology mappings.
13. **Heavy services:** assessment unit/schema/scenario/report/web tests start no heavy profile. Golden verification runs core first, then one heavy profile at a time; only the existing guarded lake+governance ingestion window may co-run and it stops Airflow.
14. **First delivery slice:** rubric + approximately 30 anchored questions + v1 gates/findings/recommendations + standalone report prototype + at least three synthetic scenarios and two-rater calibration. No web, golden-pipeline change, or cloud work in the first implementation review.

## Required phase order

1. Rubric/report prototype and synthetic calibration.
2. Versioned content/engagement/demo contracts, local store, migration/import/export boundary.
3. Deterministic engine, gates/findings, and report service.
4. Local web user path.
5. Capability/architecture/Demo Guide catalog.
6. Existing golden pipeline gap completion and demo manifests.
7. Mapping integration, initial deep dives, and one inert recipe-extension proof.
8. Full portability/security/resource/regression/docs/release verification.

## Required verification surfaces

- Unit: maturity, confidence, coverage, executive presentation, gates, findings, priority, mappings.
- Contract: schema validation, semantic references, manifest hashes, content version isolation, migration registry.
- Scenarios: at least startup/no governance; mature lake/weak quality; manual governance/missing lineage; preferably strong engineering/no AI operating model.
- Calibration: two rater fixtures per scenario; at least 85% question ratings within one maturity level.
- Portability: create through UI, report, export, copy ZIP/folder to a new absolute path, import/reopen, regenerate identical canonical report data.
- Hygiene: secret patterns, entropy-sensitive keys, URI credentials, symlinks/traversal, and absolute POSIX/macOS/Windows paths absent from exports.
- Regression: existing `make seed SCALE=small SEED=42`, `make load`, `make health`, `make dbt`, `make bi`; heavy proof only in its staged phase.
- Clean checkout: clone/worktree at implementation commit, build isolated venvs, run content/schema/unit/scenario/report/browser smoke, and separately run the core data-platform regression.

## Unresolved questions

None block planning. The local access-policy tool and exact compatible dependency versions require an early, bounded implementation compatibility spike; failure must fall back to an explicitly documented non-enforcing demo artifact and cannot be misrepresented as proven policy enforcement.
