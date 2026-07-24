# Requirements Evidence: GitHub Issue #38 and Confirmed Advisory

Researched: 2026-07-24 (Asia/Ho_Chi_Minh)
Scope: read-only extraction of the binding delivery contract; no implementation recommendation beyond resolving requirements.

## Sources and authority

- Primary delivery contract: [GitHub Issue #38](https://github.com/khanhvg/ai-ready-data-platform/issues/38), especially `Outcome`, `Acceptance criteria`, `Initial delivery order`, `Constraints and public contracts`, `Out of scope`, `Verification intent`, and `Rollback and recovery`.
- Authorization/status evidence: [owner comment](https://github.com/khanhvg/ai-ready-data-platform/issues/38#issuecomment-5069080056); issue labels include `triaged`, `risk:high`, `architecture`, `data-platform`, and `evidence`.
- Confirmed product source: `/Users/khanhvg/Documents/work/data-assessment/ai-ready-data-platform-assessment-advisory.md` (2026-07-24), sections 2–6, 8–12, and 15–23.
- Current runtime context: repository `README.md`, sections `Core stack`, `Optional profiles`, and `Startup order and resource trade-offs`.

## Every issue acceptance criterion

1. Quick assessment covers all 10 confirmed capability domains, uses approximately 30 diagnostic questions, and is designed to finish within 60 minutes.
2. Every assessed capability has observable maturity anchors 0–4 plus a separate confidence/evidence status.
3. Executive AI-readiness applies versioned, explainable gates; strengths cannot hide critical quality, governance, privacy, security, lineage, or reproducibility gaps.
4. Findings connect gap, impact, priority, recommendation, logical architecture, technology options, and demo evidence; demo artifacts are never customer maturity evidence.
5. Framework content is versioned and not hard-coded in UI logic.
6. Each engagement uses a portable folder with relative paths, schema/framework versions, import/export, and no secrets or absolute machine paths in exports.
7. Local workflow supports create engagement → quick assessment → findings review → deep-dive selection → report → export → import.
8. Report contains executive summary, readiness, heatmap, gates, confidence, blockers, findings, target state, reference diagrams, roadmap, technology options, and evidence appendix.
9. Rubric and report are prototyped/tested against at least three synthetic customer scenarios before major UI or golden-pipeline investment.
10. A separate reproducible golden e-commerce evidence layer covers ingestion, quality/quarantine, transformation, metadata/lineage, governance, policy-based access, serving, and AI-ready publication.
11. A future domain recipe can be added without changing the assessment engine or core schema.
12. The implementation plan provides requirement→step→verification traceability, affected modules/contracts, dependency order, exact or discoverable test commands, runtime smoke criteria, compatibility/rollback, and documentation impact.

Source: Issue #38 `Acceptance criteria`.

## Material advisory success metrics

The plan must preserve all measurable targets from advisory §23:

1. Quick assessment: ≤60 minutes and ≥90% questions answered.
2. Coverage: 100% of defined capability domains.
3. Anchoring: every question has clear anchors for all levels 0–4.
4. Inter-rater consistency: two Architects differ by no more than one maturity level on ≥85% of questions for the same scenario.
5. Confidence: 100% of capability scores show independent confidence/evidence status.
6. Critical findings: 100% include impact, recommendation, priority, and reference architecture.
7. AI-ready score: gating rules are always applied and explained.
8. Report: generated as HTML or PDF without manual editing.
9. Portability: copied folder imports/reopens on another machine/path without data loss.
10. Export hygiene: zero credentials, tokens, or absolute machine paths.
11. Golden pipeline: reproducible from the guide with ≥95% of steps automated.
12. Stage proof: ingestion, quality, quarantine, transformation, lineage, governance, access control, serving, and AI-ready publication are all demonstrated.
13. Quality proof: ≥1 failing record/rule is detected and blocked from curated.
14. Privacy proof: ≥1 PII field is classified and masked or access-controlled.
15. Lineage proof: source-to-published-data-product path is visible.
16. Web proof: artifacts for every golden-pipeline stage display without web pipeline control.
17. Extensibility proof: adding one domain recipe changes neither assessment engine nor core schema.

Advisory §5 adds qualitative outcomes: gaps and priorities are clear; customers understand AI readiness as foundation/trust/control; important findings have recommendations and architectures; the pipeline reproduces on another machine or AWS account; industry expansion avoids platform duplication.

## Binding product decisions

- Primary users: Solution Architect and Enterprise Architect; use cases are discovery, technical workshop, and executive reporting (advisory §§2.1, 3).
- Capability scores are the source of truth; normalized 0–100 is presentation-only and cannot bypass gates (advisory §§2.2, 11.4–11.6; Issue `Constraints`).
- Vendor-neutral capability/rubric; AWS is the first implementation mapping, never a maturity criterion (advisory §§2.3, 13–14; Issue `Constraints`).
- Two modes: interview-only is explicitly `Self-reported`; evidence-led records separate confidence/evidence state. Allowed statuses: Self-reported, Partially evidenced, Evidenced, Conflicting evidence, Not assessed (advisory §§2.4, 11.3).
- Two engagement depths: quick scan (~30 questions/10 domains/60 minutes) and domain deep dives (about 15–30 questions/domain) (advisory §§2.5, 11.1).
- Local-first, portable, engagement folder authoritative; SQLite may only cache/index; storage must have schema/framework versioning, migration strategy, relative paths, and a future S3 adapter boundary (advisory §§2.6, 9–10).
- Three independent but linked cores: assessment engine, knowledge/architecture catalog, demo evidence. Demo never determines customer maturity (advisory §§3, 7, 15).
- Web displays guides/manifests/artifacts but never runs the pipeline; Demo Guide does not score (advisory §§2.7–2.8, 8.5, 16).
- Content is versioned outside UI: capabilities, questions, anchors/models, recommendations, architecture patterns, technology mappings, report templates, demo manifests (advisory §9).
- Initial gates: quality ≤1 or security/privacy ≤1 caps AI readiness at 1; governance/ownership ≤1 caps it at 2; missing critical lineage forbids `production AI-ready`; missing reproducibility/versioning allows only `experiment-ready`. Gates are versioned, explainable, visible, and profile-configurable (advisory §11.6).
- No learning portal or interactive labs: Issue `Constraints` explicitly preserves post-cleanup data-only scope.

## Dependency order (binding)

1. Prove rubric, question bank, report template, timing, consistency, gates, and recommendations with synthetic scenarios.
2. Define versioned framework/content and portable engagement schemas, migrations, compatibility tests.
3. Build the local create/assess/review/deep-dive/report/export/import path.
4. Build the capability/architecture library, first quality, governance/metadata/lineage, then security/policy.
5. Build/verify the separate reproducible golden pipeline and stage artifact manifest.
6. Link finding → capability → logical architecture → implementation mapping → demo artifact → action.
7. Add deep dives/domain recipes only after MVP stability; hosted/S3/multi-user expansion remains later and separately authorized.

Sources: Issue `Initial delivery order`; advisory §17. Starting UI or demo before rubric validation violates advisory §§7, 17.1, 18, 19.1.

## Synthetic scenario and demo requirements

- Assessment prototypes: use at least three; advisory §19.1 supplies four reversible personas: startup without governance; enterprise lake with weak quality; manual-governance organization; technically strong platform without AI operating model.
- Measure duration/completion, score consistency/inter-rater variance, gate explanations/reasonableness, and recommendation actionability (Issue `Verification intent`; advisory §§19.1, 23).
- Golden data: deterministic, reproducible, synthetic e-commerce/retail only; no customer data. Advisory §12.1 names customers, products, orders, payments, support tickets and requires deliberate duplicate/null/invalid-reference/late-arrival/business-rule failures.
- Golden outputs must include a quarantine failure, classified/masked PII, source-to-product lineage, and a versioned AI-ready dataset manifest with owner, contract/schema, quality/freshness SLA, access classification, lineage, and reproduction instructions (Issue `Verification intent`; advisory §§12.4–12.11, 16, 22–23).

## Reporting, portability, and runtime verification

- Report contract is the 12-part list in advisory §8.6 plus criterion 8; output HTML or PDF without manual edits.
- Contract/unit tests cover content/schema validation and migration; maturity, confidence, gates, findings, priority, reporting, and import/export deterministically (Issue `Verification intent`).
- End-to-end smoke: create → assess → review → select deep dives → report → export → import; then copy to a different path and reopen without loss.
- Scan exports for credentials, tokens, and absolute paths. Cleanup may remove generated runtime data but must preserve engagement source/evidence (Issue `Rollback and recovery`).
- Existing README establishes a resource-aware local runtime: deterministic retail generator, DuckDB/dbt/Rill core, opt-in Airflow/lake/governance profiles, and only one guarded lake+governance co-run. Golden work must preserve this runtime and its heavy-profile sequencing unless a later accepted plan changes it.

## Non-goals and prohibitions

- No automated customer-system scanning; customer data/credentials; cloud apply, Terraform apply/destroy, hosted deployment, or automatic S3 upload.
- No SaaS, multi-tenancy, login, online collaboration, cloud portfolio dashboard, or live web pipeline control.
- No multiple industry pipelines in MVP; no complex model training solely to claim readiness.
- No product-adoption checklist, vendor lock-in, or maturity based on AWS/tool presence.
- No multiple same-role tools merely to prove neutrality; no screenshot-only evidence; no single unexplained 0–100 score; no vector DB/feature store/MLOps requirement absent a real use case.
- No reintroduction of the removed learning portal or interactive lab product.

Sources: Issue `Constraints`/`Out of scope`; advisory §§6, 11.5, 18.

## Genuine blockers vs reversible defaults

**Genuine blockers**

- Implementation is not authorized until an independent combined plan-readiness audit completes and the issue reaches `ready to cook`; current issue is open/triaged and the owner comment states this gate explicitly.
- Any need for credentials, customer data, AWS/Terraform apply, hosted deployment, or GitHub mutation requires new authority.
- A plan that omits traceability, migration/backward-compatibility, rollback, exact/discoverable tests, or runtime smoke criteria fails criterion 12.

**Reversible defaults (do not block planning)**

- Use the advisory's four personas while satisfying the minimum-three requirement; scenario names/content can change without altering contracts.
- HTML or PDF is acceptable; choose the smallest existing report path and test it.
- Advisory §13 tool choices (S3/Glue/Athena/Lake Formation/dbt/Soda-or-GX/OpenMetadata/Superset-or-Metabase/Terraform) are an AWS reference profile, not authorization or mandatory MVP runtime replacement.
- Choose one tool per role; alternative products remain content mappings.
- S3 adapter, auth, collaboration, hosted deployment, portfolio reporting, and additional recipes are deferred extension points.

## Discrepancies and planning resolution

- Advisory §23 requires at least three scenarios; §19.1 lists four. No conflict: execute ≥3, preferably all four if effort remains bounded.
- Advisory §5 says reproducible on another machine **or AWS account**; Issue forbids AWS apply and prioritizes local portability. Verify another local path/machine now; leave AWS reproduction as a future reference-profile contract.
- Advisory proposes an AWS-first golden stack, while README documents an established local DuckDB/dbt/Rill/Airflow/lake/governance runtime. Issue explicitly says preserve that runtime. Plan should extend/reuse or separately map it, not replace it by inference.
- Advisory §17.8 describes future hosted/S3 expansion; Issue places cloud creation and automatic S3 upload out of scope. Treat §17.8 as roadmap-only.
- Advisory §12.1 names five e-commerce entities, while the existing deterministic retail generator has 18 tables. The acceptance contract is capability/evidence coverage, not an exact table count; plan must map existing tables and add only genuinely missing synthetic evidence (for example support-ticket semantics) after inspection.

## Unresolved questions

None. Repository research confirmed there is no existing assessment report generator/schema owner and no proven PII classification/masking, explicit quarantine dataset, or AI-ready dataset manifest; the plan treats all four as Issue #38 gaps.
