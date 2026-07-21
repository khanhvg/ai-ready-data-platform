# Requirements and Risk Traceability

## Immutable and Live Inputs

| Input | Exact identity | Use |
|---|---|---|
| I5-05 planner input / Issue #6 integration merge | `24be3b34c6b0fcdbd07c5800dcab349054e34713` | Exact clean repository baseline |
| Golden main | `3cd3d41f71582774e8d9656a51d1044035f4503c` | Historical golden anchor |
| Reviewed golden tree | `d0273731a5077cc17c2f4398057623b83a50bb65` | Preserved Issue #3 data spine |
| Master discovery | `d3ce0c5832cca4f1b68299cbba111e7cc6c7a430` | Accepted discovery |
| Master planner | `8ec96f92245c679d019ac3648c5c2d77a49f0429` | Accepted master plan |
| Master validation | `5962316b8113ece592a26fe6211a97ae77eb70fb` | Accepted initial validation |
| Master red-team/readiness input | `bf740edb87452fe766591d0eeefd0bd5151220fa` | Accepted risk input |
| Master readiness report | `e440c5855732d5d8f5d634e3cc1359c010cc5ed3` | Issue fan-out authority only |
| Audited mapping/integration handoff | `f9a87d0ebdb72c014a6f8c6eaae865dad4d2188c` | Ownership/dependency graph |
| Live Issue #10 | OPEN with `ready for plan validation`, `risk:high`, `tdd`, `security:S3`, `frontend`, `accessibility`, `vertical-slice` at validation input | Fresh issue scope and commands |
| Owner fan-out decision | https://github.com/khanhvg/ai-ready-data-platform/issues/5#issuecomment-5036142770 | Planning may run in parallel; dependencies remain binding |
| Owner Vite decision | https://github.com/khanhvg/ai-ready-data-platform/issues/7#issuecomment-5036142177 | Vite + React direction; no merge/release claim |

Primary repository sources:

- [Master plan](../260721-005-enterprise-learning-sandbox/plan.md)
- [Phase 5](../260721-005-enterprise-learning-sandbox/phase-05-runnable-portal-vertical-slice.md)
- [Lesson/lab contract](../260721-005-enterprise-learning-sandbox/lesson-lab-contract.md)
- [Execution authority](../260721-005-enterprise-learning-sandbox/execution-authority-and-release-contract.md)
- [Requirements traceability](../260721-005-enterprise-learning-sandbox/requirements-traceability.md)
- [Implementation graph](../260721-005-enterprise-learning-sandbox/implementation-issue-graph.md)
- [Readiness audit](../260721-005-enterprise-learning-sandbox/audit/readiness-audit-report.md)
- [Issue #6 fixture handoff](../260721-006-freeze-golden-baseline/issue-7-fixture-and-merge-handoff.md)
- [Issue #6 evidence contract](../260721-006-freeze-golden-baseline/evidence-canonicalization-and-provenance-contract.md)

## Issue #6 Data Truth

These exact input identities are read-only preservation anchors:

| Path | Contract/version | SHA-256 | Git blob |
|---|---|---|---|
| `contracts/data/retail-golden-v1.json` | `retail-golden-v1` | `f303282e3b524e1273e702c9b8b24b500aaa01afdd3c3b623ac997afba8840cc` | `2bdd653ced3ce3f69652d2b873f21699e1e1fc81` |
| `contracts/data/promotion-trust-v1.yaml` | `promotion-trust-v1` | `c30e1938aae6eeffa2adf0c0b3bdee15f7f877d769cce09e171d43dc2f153cfe` | `876789d549276b44a6e64cc4c9a471886fd2752b` |
| `tests/fixtures/learning/promotion-trust/evidence-v1.json` | `promotion-trust-evidence-v1` / `promotion-trust-small-42-v1` | `2f4d90228fa2ea8859a8db630ff587b6cebdc10a0bf6b7db25e46c3dc27181d5` | `6b5d8a01a59856cdb93a674a0cce5c2bcc9527e0` |
| `tests/fixtures/learning/promotion-trust/manifest.json` | `promotion-trust-fixture-manifest-v2` | `0a1dcd4023648f52009bfd4dc5d529c00ce66f42cd0e725732b972b0b78df341` | `a4b32032962f5f787d733f7de8cf657491944e37` |
| `learning/contracts/fitness-result-v1.schema.json` | `fitness-result-v1` | `a104ad6330bcfc22bda0fb661fef96f067c09153da7dc2f306103e5f93a4ab6d` | `0212ca96614aea02dbb60434d67a0cbb379a8213` |
| `learning/contracts/schema-version-registry.json` | `schema-version-registry-v1` | `8e18588f63b5d99c0b60a229758575e8badf0f055bfcb4f89908f9fa2684a57e` | `c63a41853c49fb16f381950f74339e14017fc355` |
| `release-manifest.json` | protected legacy provenance | `f9037b5d946d14f7b1b9c020939f1a44961011f2ad933db9f2b69054abbf9539` | `b27d231c5ee6d48fd7932b06807ef6a9a2220e21` |

The fixture contains 89 sanitized aggregate rows at four independent grains:

1. `mart_promotion_effectiveness` — `(promo_name, channel)` — 7 rows.
2. `mart_fulfillment_performance` — `(carrier, region_name)` — 25 rows.
3. `mart_returns_analysis` — `(reason, category_name, region_name)` — 47 rows.
4. `mart_data_quality` — `(scenario)` — 10 rows.

The only valid outcome is `insufficient-evidence` with reason `no-common-grain`. The expected
controlled failure is `PROMOTION_HEADLINE_INSUFFICIENT`. No campaign-level causal join,
fulfillment/return/DQ attribution, fake row, ignored fixture, or locally rewritten threshold may
satisfy a portal assertion.

## Requirement Catalogue

| ID | Requirement | Stage | Verification |
|---|---|---|---|
| PTP-FR-01 | Render the business question and stakeholder concern from the released Issue #8 lesson | A | Component/contract/no-JS tests |
| PTP-FR-02 | Present all four mart grains, filters, calculations, scopes, and limitations honestly | A/B | Contract assertions + Chromium |
| PTP-FR-03 | Show controlled failure separately from runner/environment failure | A explanation; B execution | State/unit + real journey |
| PTP-FR-04 | Record only `insufficient-evidence / no-common-grain` for the v1 evidence | A read-only; B canonical mutation | Released validator + E2E |
| PTP-FR-05 | Reset through the released Issue #9 operation, preserve prior immutable evidence, and prove a fresh ready state | B | Crash/retry/idempotency E2E |
| PTP-FR-06 | Verify a fresh run and expose evidence metadata/download integrity | B | Real runner + byte/digest test |
| PTP-FR-07 | Use the one Issue #8 completion authority; browser/reflection/navigation never completes | B | Transaction/reconciliation negatives |
| PTP-FR-08 | Provide read-only navigation/static fallback and explicit runner-unavailable state without completion | A | No-JS/offline/unavailable tests |
| PTP-FR-09 | Back/forward/reload never replay POST, duplicate operation, or corrupt canonical state | A/B | Router + browser history tests |
| PTP-FR-10 | `learn-status` and `learn-down` report/stop only issue-owned processes and preserve evidence | B | Lifecycle tests |
| PTP-NFR-01 | Vite/React modular monolith + same-origin BFF; private runner; no distributed framework | A/B | Process/boundary inspection |
| PTP-NFR-02 | Docker-free, no cloud/model credentials, no AWS/Terraform action | A/B | Environment/call/credential scans |
| PTP-NFR-03 | Practical accessibility: semantic keyboard path, visible focus, narrow reflow, reduced motion, live regions, axe zero Critical/Serious | A/B | Focused tests + one Chromium |
| PTP-NFR-04 | 16 GiB-friendly: one portal process, one released runner process, core DuckDB path; no heavy optional profile | B | Process inventory; no numeric release claim |
| PTP-NFR-05 | Same-origin/Host/Origin/CSRF/CSP/XSS/storage protections fail closed | A/B | S3 negative suite |
| PTP-NFR-06 | Evidence uses registered schema/canonicalization/artifact hashes and honest local-integrity language | B | Contract/download/tamper tests |
| PTP-NFR-07 | Offline/runner crash/unavailable/retry states are recoverable and never masquerade as controlled lesson failure | A/B | State + real crash/retry tests |
| PTP-NFR-08 | Manual AT/visual checks remain residual production UAT, not an automated conformance claim | Release | Bounded artifact/checklist + human gate |

## Source-to-Plan Trace

| Accepted source IDs | I5-05 requirements | Plan phases |
|---|---|---|
| OWN-02, BO-01, BO-02, FR-01, FR-04 | PTP-FR-01..07 | 2, 3, 6, 7 |
| OWN-04, BO-05, NFR-01, NFR-02 | PTP-NFR-01/02/04 | 1, 4, 5, 7 |
| OWN-09, NFR-10 | exact-head, TDD, S3, rollback, approval | 1..7 |
| ASR-01, ADR-002/003/006 | modular monolith/private runner/logical layers | 2, 5, 6 |
| ADR-007/018, NFR-04/06 | one completion transaction, integrity limits, recovery | 5, 6, 7 |
| PH-C08, PH-H05/06/14 | real runner journey, external-tool state, accessibility, Vite handoff | 1..7 |
| Issue #10 exact Verify block | all product acceptance | 4, 7 |

## Risk Register

| ID | Risk | Impact | Mitigation / rollback | Owner/gate |
|---|---|---|---|---|
| PTP-R-01 | Draft #7/#8/#9 output mistaken for release | Contract/API drift; unsafe cook | Empty stage authorities; later-amendment GA/GB exact remote merge/release checks; no future SHA in source | Readiness |
| PTP-R-02 | Static fixture looks like a fresh completed run | False learner trust | Stage A banner, no completion mutation/control, baseline-evidence label | Portal |
| PTP-R-03 | UI derives completion from local state/reflection | Forged completion | Issue #8 authority only; server transaction; negative tests | Portal + #8 |
| PTP-R-04 | Browser reaches privileged runner | RCE/base mutation | same-origin BFF only; private transport secret server-only; no CORS | Portal + #9 |
| PTP-R-05 | Cross-grain presentation implies causality | Wrong business decision | fixed four-grain table/limitations and exact v1 decision assertion | Content |
| PTP-R-06 | Crash/reset retry duplicates mutation or loses evidence | Corrupt state | #9 idempotency/reconciliation; stable client key; fault injection | Runner/BFF |
| PTP-R-07 | Evidence bytes/digest/index disagree | False verification | verified immutable handle; schema/JCS/hash; fail download/completion | BFF |
| PTP-R-08 | XSS from lesson/evidence/error content | session/operation abuse | released validation; React escaping; no raw HTML; CSP; attachment downloads | Portal |
| PTP-R-09 | Browser storage leaks token/evidence/state | replay/disclosure | no privileged token or canonical evidence in Web Storage/IndexedDB | Portal |
| PTP-R-10 | Accessibility matrix becomes expensive or overclaims conformance | Delay/false claim | one Chromium desktop+narrow; axe Critical/Serious; residual human UAT | Portal |
| PTP-R-11 | Optional tools/Docker/cloud become hidden dependencies | 16 GiB and credential failure | core-only commands; status adapters optional; explicit unavailable states | Lifecycle |
| PTP-R-12 | Cleanup deletes evidence or unrelated state | Irrecoverable audit loss | marker/namespace checks; stop process group; preserve committed evidence | Lifecycle |
| PTP-R-13 | Visual command relies on native OS automation | flaky/non-portable gate | fixed Chromium capture + bounded checklist only | Test |
| PTP-R-14 | Package lock is ignored or dependency supply chain drifts | unreproducible/unsafe build | exact #7 handoff; `npm ci`; force-add exact app lock only; high/critical audit gate | Portal |

## Hard STOP Conditions

- Dirty/wrong base; local/tracking/fresh-live mismatch; missing required ancestry.
- Unmerged/unreleased dependency, digest/version/operation/registry mismatch, or active conflicting
  lease.
- Any write outside I5-05 ownership; any protected/shared contract or Issue #6 fixture drift.
- Required test/tool missing; Critical/High S3 finding; axe Critical/Serious violation.
- Browser-direct runner path, wildcard CORS, ambient credentials, repository write, arbitrary
  command/path/SQL, or unbounded evidence/log content.
- Controlled and environmental failure conflated; v1 decision/grain semantics changed.
- Completion without fresh committed runner result plus valid immutable evidence.
- Cleanup/rollback cannot preserve prior evidence and unrelated state.
- Missing fresh independent validation/readiness or human exact-head pre-merge approval.

## Unresolved Questions

None for planning. Exact dependency SHAs, versions, method/path pairs, registry commands, and
client modules are intentionally absent until their owning issues publish releases; their absence
blocks implementation through GA/GB, not completion of this plan.
