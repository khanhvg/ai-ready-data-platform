# Requirements and Risk Traceability

## Current Stage B Inputs

| Input | Exact identity | Use |
|---|---|---|
| Readiness input | `8c77957ad3be84dc97e4633cdafd898ea9e431fa` | Exact clean plan-only amendment input |
| Portal Stage A PR #31 merge | `041d4ca866e927a331e159fdf8216838b481a595` | Shipped portal and passing post-merge browser smoke |
| Portal Stage A reviewed head | `473f54c2e0879d3037cbed25b2e7a3f0626d558d` | Focused review Critical/Important = 0 |
| Runner PR #32 merge / implementation base | `671201f78024786a9f2eba5e9e5fce7c78b4443d` | Shipped runner and exact Stage B cook base |
| Runner reviewed head | `86a6c259ad384591777cf1d46f2f6c9ea6327361` | 66/66, eight operations, dbt multiprocessing, clean-checkout smoke |
| Lane | Issue #10 comment `5056144073` | Standard lean; focused review + functional safety tests |

Current Stage B requirements are Phase 6's fixed journey, 18-path write set, 15 commands, eight
released operations, authenticated loopback request contract, immutable evidence, truthful reset,
sole progress/completion authority, browser/a11y/no-JS/lifecycle tests, and Critical/Important=0
review. Historical Stage A rows below retain their release-time meaning and do not re-block Stage B.

## Historical Stage A Inputs

| Input | Exact identity | Use |
|---|---|---|
| V3 correction input | `2f278eb25aaff9e050314b01d1be155b76793f11` | Exact clean local/upstream/live post-review plan input |
| Issue #6 integration merge | `24be3b34c6b0fcdbd07c5800dcab349054e34713` | Read-only protected data truth |
| Issue #7 approved feature head | `b219ba2d3843934c3bce2fbbec2a844b48b2dfa9` | Human-approved Vite release content |
| Issue #7 PR #22 merge | `1806b6d515f2f7a2ace2be7077af84a745ff221f` | Released Vite/React authority |
| Issue #8 Stage A PR #23 merge | `5c2244c2c860234d0df49cf0a42ad950c6495717` | Released learning-contract authority |
| Embedded Stage A / final release parent 1 | `fecf6bb8e5dfa7cc69f9766f72ac6f5b9301dad9` | Shared binding's exact `stageA.releaseSha`; ancestry only, no longer cook base |
| Issue #8 final integration release | `5644f01b4c0443a81f3af0bcce80f44c847cd986` | Pristine Stage A cook base; Issue #8 CLOSED/`shipped` |
| Released integration tree | `a38594d420fe7df2b30265a8a72bb5fad1698012` | Exact 921-entry tree authority |
| Shared Vite binding | `promotion-trust-vite-binding-v1`; SHA-256 `03d2aa6bd9fa178e6075865364a8ae8b83ce548c42b450d1858b451b45d0d1d0` | Exact read-only alias authority; schema SHA-256 `74035baee08b378e46421466333d6933d1bad820337acd1b80a633d236173a43` |
| Issue #8 release evidence | https://github.com/khanhvg/ai-ready-data-platform/issues/10#issuecomment-5047964988 | Final merge/topology/binding/pristine evidence handoff |
| Master readiness report | `e440c5855732d5d8f5d634e3cc1359c010cc5ed3` | Issue fan-out authority only |
| Prior independent validation | `e2bba33deff76985eb3bdae361d494d162c854f8` | Immutable historical validation output |
| Failed implementation review | PR #29 comment `5050218543`; 3 Medium findings | Invalidates prior Stage A readiness; immutable negative history |
| Fresh recovery authorization | Issue #10 comment `5050239390` | V3 plan correction only; no cook/runner/cloud authority |
| Live Issue #10 before correction publication | OPEN with `ready for review`, `risk:high`, `tdd`, `security:S3`, `frontend`, `accessibility`, `vertical-slice` | Must move to `ready for plan validation`, not readiness |
| Live Issue #9 at the Stage A audit | OPEN and unreleased | Historical Stage A blocker; superseded by PR #32 |

The [Stage A release amendment](./stage-a-release-amendment.md) is the normative byte/path/command
closure. The prior validation and blocked audit remain historical evidence; they do not override
the later released dependency facts.

## Protected Data and Contract Truth

These identities were recomputed from pristine integration
`5644f01b4c0443a81f3af0bcce80f44c847cd986` and remain read-only:

| Path | Contract/version | Bytes | SHA-256 | Git blob |
|---|---|---:|---|---|
| `contracts/data/retail-golden-v1.json` | `retail-golden-v1` | 3031 | `f303282e3b524e1273e702c9b8b24b500aaa01afdd3c3b623ac997afba8840cc` | `2bdd653ced3ce3f69652d2b873f21699e1e1fc81` |
| `contracts/data/promotion-trust-v1.yaml` | `promotion-trust-v1` | 1682 | `c30e1938aae6eeffa2adf0c0b3bdee15f7f877d769cce09e171d43dc2f153cfe` | `876789d549276b44a6e64cc4c9a471886fd2752b` |
| `tests/fixtures/learning/promotion-trust/evidence-v1.json` | `promotion-trust-evidence-v1` / `promotion-trust-small-42-v1` | 16252 | `2f4d90228fa2ea8859a8db630ff587b6cebdc10a0bf6b7db25e46c3dc27181d5` | `6b5d8a01a59856cdb93a674a0cce5c2bcc9527e0` |
| `tests/fixtures/learning/promotion-trust/manifest.json` | `promotion-trust-fixture-manifest-v2` | 4364 | `0a1dcd4023648f52009bfd4dc5d529c00ce66f42cd0e725732b972b0b78df341` | `a4b32032962f5f787d733f7de8cf657491944e37` |
| `learning/contracts/fitness-result-v1.schema.json` | `fitness-result-v1` | 1375 | `a104ad6330bcfc22bda0fb661fef96f067c09153da7dc2f306103e5f93a4ab6d` | `0212ca96614aea02dbb60434d67a0cbb379a8213` |
| `learning/contracts/schema-version-registry.json` | `schema-version-registry-v1` | 5816 | `8e18588f63b5d99c0b60a229758575e8badf0f055bfcb4f89908f9fa2684a57e` | `c63a41853c49fb16f381950f74339e14017fc355` |
| `release-manifest.json` | protected legacy provenance | 366321 | `f9037b5d946d14f7b1b9c020939f1a44961011f2ad933db9f2b69054abbf9539` | `b27d231c5ee6d48fd7932b06807ef6a9a2220e21` |

The fixture contains 89 sanitized aggregate rows at four independent grains:

1. `mart_promotion_effectiveness` — `(promo_name, channel)` — 7 rows.
2. `mart_fulfillment_performance` — `(carrier, region_name)` — 25 rows.
3. `mart_returns_analysis` — `(reason, category_name, region_name)` — 47 rows.
4. `mart_data_quality` — `(scenario)` — 10 rows.

The only valid outcome is `insufficient-evidence` with reason `no-common-grain`; the released
controlled-failure code is `PROMOTION_HEADLINE_INSUFFICIENT`. Stage A may explain these facts but
may not imply a causal join, execute the failure, or relabel retained fixture evidence as fresh.

## Requirement Catalogue

| ID | Requirement | Stage | Verification |
|---|---|---|---|
| PTP-FR-01 | Vietnamese-first catalog/module/lesson/step shell renders the released stakeholder question | A | render/adapter/no-JS/Chromium |
| PTP-FR-02 | Present all four independent grain scopes, calculations, and limitations honestly | A/B | contract assertions + Chromium |
| PTP-FR-03 | Promotion-trust is one vertical slice, not the whole course | A | catalog/copy assertions |
| PTP-FR-04 | Explain controlled failure separately from runner/environment unavailability | A explanation; B execution | state/negative tests |
| PTP-FR-05 | Show only `insufficient-evidence / no-common-grain` for released v1 evidence | A read-only; B deferred mutation | released validator + view tests |
| PTP-FR-06 | Read-only navigation, back/forward/reload, and no-JS pages never mutate or progress | A | router + browser/network/storage tests |
| PTP-FR-07 | Runner is explicitly unavailable; run/reset/verify are explanatory and completion impossible | A | DOM/bundle/import/request negatives |
| PTP-FR-08 | Later released #11/#12 content enters only through hash-bound released registry/binding entries without content-ID code switches | A seam only | current released descriptor + branded test-only metamorphic pure-function tests + production rejection/absence |
| PTP-FR-09 | Execute/reset/fresh-verify/evidence/completion journey only through released #9 | B | Phase 6 fixed real-runner journey |
| PTP-FR-10 | Start/status/down control only the Stage A static process and preserve review artifacts | A | lifecycle/PID/path/cleanup tests |
| PTP-NFR-01 | Exact #7 Vite/React lock and exact #8 validators/contracts/shared binding; no duplicated truth | A | shared binding + released-adapter mutation tests |
| PTP-NFR-02 | One loopback GET/HEAD static process plus private authenticated child-control listener; no product API/BFF/database/runner/service worker | A | closed request inventory + no-PID-signal lifecycle tests |
| PTP-NFR-03 | No cloud/model credentials, AWS/Terraform/Docker/optional-profile action | A/B | call/environment/bundle scans |
| PTP-NFR-04 | Semantic keyboard path, focus, 1280x800/360x800 reflow, reduced motion, axe zero Critical/Serious | A | one Chromium suite + unit checks |
| PTP-NFR-05 | CSP/Host/path/XSS/storage/output/artifact/cleanup boundaries fail closed | A | S3 catalogue |
| PTP-NFR-06 | Static and React modes share one safe view model and equivalent stable facts | A | parser/render/no-JS comparison |
| PTP-NFR-07 | One process/worker, exact same-run Playwright/Chrome identity, and exact time/file/byte/artifact/current-generation/trace ceilings | A | browser-admission/lifecycle/build/evidence/trace/output-limit tests |
| PTP-NFR-09 | Scaffold/tests/RED/first-semantic/final commits and trees are contemporaneously bound | A | Git ancestry + raw/sanitized log manifests |
| PTP-NFR-10 | One atomic current generation verifies all non-self hashes and classifies stale/interrupted generations as negative history | A | closure/interruption/ignored-inclusive tests |
| PTP-NFR-08 | Lane S requires focused exact-head review with Critical/Important=0; no separate human/security/red-team ceremony | Release | focused review + functional safety tests |

## Source-to-Plan Trace

| Accepted source | Current requirements | Phases |
|---|---|---|
| Issue #10 body/comments and I5-05 master plan | PTP-FR-01..10 | 1..7 |
| Released #7 ADR/toolchain/lock | PTP-NFR-01/04/07 | 1..4 |
| Released #8 registry/lesson/lab/OpenAPI/evidence/completion | PTP-FR-01/02/04/05/09, PTP-NFR-01/06 | 1..7 |
| Issue #6 protected fixture/data | PTP-FR-02/05 | 1, 3, 4, 6 |
| Issue #11/#12 ownership contracts | PTP-FR-03/08 | 2, 3 |
| S3/readiness rules | PTP-NFR-02/03/05/07/08 | 1..7 |

## Risk Register

| ID | Risk | Impact | Mitigation / rollback |
|---|---|---|---|
| PTP-R-01 | Feature/worktree or pre-composition bytes mistaken for release | Contract/tool drift | Bind remote merges plus pristine composed tree and every consumed byte |
| PTP-R-02 | Issue #7 spike becomes portal architecture | Brittle duplicate product | Promote exact toolchain/lock only; purpose-built catalog/provider/router/render seams |
| PTP-R-03 | Static fixture looks like a fresh completed run | False learner trust | retained-baseline label; no action/completion/evidence control |
| PTP-R-04 | Cross-grain display implies causality | Wrong business decision | adjacent independent-grain limitations and exact decision tests |
| PTP-R-05 | Browser or BFF grows a generic privileged surface | command execution/XSS/state forgery | fixed action map, session/CSRF, exact Host/Origin/body/method limits, no browser runner authority |
| PTP-R-06 | Static/React/router route truth diverges | Inconsistent no-JS experience | one released registry, catalog and route derivation, stable fact IDs |
| PTP-R-07 | #11/#12 require hard-coded switches | Curriculum growth stalls | family-driven released registry plus test-only metamorphic proof; no invented release |
| PTP-R-08 | Dependency or contract downgrade | Unsafe/incorrect render | exact paths/hashes/versions/validators; unknowns fail before build |
| PTP-R-09 | Mutable lifecycle state targets foreign process/path | Irrecoverable state loss | child-held capability/self-shutdown, no PID signal, containment/sentinel negatives |
| PTP-R-10 | Visual/a11y scope becomes ceremony or overclaim | delay/false conformance | one Chromium desktop+narrow, keyboard, axe Critical/Serious, no-JS; no separate ceremony |
| PTP-R-11 | Package lock or supply chain drifts | unreproducible/unsafe build | exact transitive lock, frozen install, no scripts, audit gate |
| PTP-R-12 | Stage A is mistaken for completed Issue #10 | Premature closure | Issue stays open until Stage B merges and post-merge smoke passes |
| PTP-R-13 | RED is reconstructed after semantics | False TDD provenance | exact scaffold/tests commit ancestry and contemporaneous raw/sanitized logs |
| PTP-R-14 | Stale or partial evidence is selected | False exact-head proof | selector-written-last atomic publication, non-self closure, negative history |

## Hard STOP Conditions

- Stage B cook does not start from clean exact `671201f78024786a9f2eba5e9e5fce7c78b4443d`, or local,
  upstream, and fresh integration disagree.
- Any release ancestry/tree/path/blob/byte/hash/version/registry/operation/lock/protected identity
  differs from the amendment.
- Any Stage B change falls outside the exact 18 Phase 6 paths, changes package-lock/dependencies,
  modifies runner/shared/root-Make/golden truth, deletes a path, or overlaps an active owner.
- Scaffold chronology is not exact 22 paths then eight tests; RED is retrospective, missing a real
  Chromium/public path, or fails for setup/forced/mock/skip/fallback reasons.
- A portal-local binding, alias/mapping table, copied binding schema, generated binding type,
  duplicate default catalog/step routes, promotion switch, test descriptor in production, or
  invented module/identifier/release truth appears.
- Browser input reaches a runner credential/transport or selects operation/command/argv/env/path/
  URL/SQL/image/package/plugin/Docker/cloud authority.
- Lifecycle signals a mutable recorded PID; blocked Stage B output fails released
  `fitness-result-v2`; build/request inventory is open; runtime/lock/env admission drifts.
- Any current evidence entry/hash/privacy/count/size/aggregate/binding fails; trace is missing,
  duplicated, source-bearing, oversized, stale-head, or unindexed; partial publication is current.
- RED/GREEN browser identities differ, browser admission falls back from exact Chromium/Chrome
  channel, differs from Chrome `150.0.7871.181` / executable SHA-256
  `b724a4c5603cfc8b9d9f27a5153c8a39e7133e53666ced7f2a8b03bf49484f85`, or author-generated
  evidence is mislabeled as independent/human-approved.
- A required test/tool/measurement is absent; focused review has Critical/Important; axe has
  Critical/Serious;
  S3, cleanup, protected hash, private-locator/PII/raw-record/source-map/remote-import scan, or
  exact-head review fails.
- Controlled and environmental failure are conflated; four-grain/canonical-decision semantics or
  vertical-slice/course wording drifts.
- Stage A claims run, reset, fresh evidence, progress, completion, full course, full WCAG, cloud,
  hosted, or human approval.

## Unresolved Questions

None. Exact released dependencies, implementation base, paths, commands, operations, adapter,
journey, acceptance, and rollback are specified. If the pinned local runtime cannot import the
released progress/completion/evidence functions, cook must report that narrow dependency rather
than clone or modify shared authority.
