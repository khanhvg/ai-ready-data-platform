# GitHub Issue #38 Phase 3 verification evidence

Status: Phase 3 implementation and bounded pre-publication checks are complete. Publication,
immutable tested implementation SHA, pull request, CI/check state, and fresh exact-head review
remain pending and are not claimed here.

## Scope

This evidence covers package `0.3.0`: deterministic maturity/coverage and confidence services,
all-rule evaluation for the pinned seven-gate bundle, linked findings/recommendations with
separate architect review state, canonical source-state digests, exactly 12 ordered report
sections, standalone HTML rendering, and `evaluate`/`report` CLI commands with explicit
engagement and output roots.

The implementation remains offline after dependency installation. It starts no service or
container, performs no cloud action, does not scan customer systems or the retail demo, and does
not let demo illustrations influence maturity, confidence, priority, gates, or readiness.
Phases 4–8 remain pending.

## Immutable input and RED proof

- Phase 3 started from immutable Phase 2 commit
  `b6659e1b1e4f4b2a050e9a106a6a10946e0ec3ad`.
- The initial focused collection failed RED with six `ModuleNotFoundError` collection errors and
  pytest exit `2`, proving the new engine modules were absent before implementation.

## Pre-publication verification

Completed local checks:

- focused specification re-review: `75 passed`;
- full assessment suite: `141 passed, 1 skipped`;
- public schema/contract/store/migration/import-export/portability/security targets:
  7 schemas, 25/10/10/29/1/28 tests passed, with the same intentional skip;
- engine/scenario/report targets: `28`, `6`, and `7` tests passed; all 36 prototype
  artifacts were byte-stable and calibration remained 117/119 (`98.3%`);
- Ruff: passed;
- strict mypy: passed over 37 files;
- package build: passed with 50 required packaged files;
- 51 tracked or pending Python sources compiled in memory;
- `docker compose config --quiet` and `git diff --check`: passed;
- initial edge-case scout: `1 Critical / 7 Important`;
- every initial scout finding was corrected in the pending diff.

The one skip is the existing future `ObjectEngagementStore`/S3 contract placeholder. Phase 3
does not implement cloud/object storage. The completed checks ran through the assessment
network-denying wrapper where defined by the Makefile.

The principal verification commands all exited `0`:

```text
make assessment-schema assessment-contract assessment-store assessment-migration assessment-import-export assessment-portability assessment-security-scan
make assessment-scenarios assessment-calibration assessment-report assessment-test
make assessment-engine
make assessment-lint assessment-typecheck assessment-build
.assessment-venv/bin/python -m pytest -q assessment/tests
docker compose config --quiet
git diff --check
```

The implementation exercises:

- missing and partial coverage, deterministic maturity aggregation, exact presentation scoring,
  and explicit `Not assessed` results;
- independent confidence distributions and conservative summaries;
- triggered and untriggered operand-level traces for all seven gates, including combined-cap
  selection;
- deterministic finding priority, recommendations, stable references, and architect
  accept/defer/edit-note review without rewriting engine truth;
- canonical `assessment-result.json` and `report.json`, a source-state digest that excludes
  generated reports, and two-run byte stability;
- exactly 12 ordered report sections and escaped, semantic standalone HTML with embedded CSS,
  no active content, and no remote resources;
- CLI rejection of missing roots, source/output aliasing, and symlinked output paths; source
  documents and their snapshot are read under the engagement writer lock through
  descriptor-bound storage operations.

An independent synthetic engagement was migrated beneath a canonical `/private/tmp` root.
Two `evaluate` and two `report` runs exited `0`, left engagement source bytes unchanged, and
produced byte-identical artifacts:

| Artifact | SHA-256 |
|---|---|
| `assessment-result.json` | `6731307002a5211dae3fa777ee9168d7e34befd198401af66d3e2ffd80851e45` |
| `report.json` | `279317d1215f07eadd7715f0f892f6c91d663fbacdb96c1d97960b21b7499e6b` |
| `report.html` | `726c5b28d0ea86b103a38cb957b68d6a3b92361bd2fe8abca62e0e48e6405137` |
| `report-manifest.json` | `8e728d3029e9d7be2f8c688c68574c7325839f35c2800ccba1ee4b8c1ae8a06d` |
| source-state digest | `e0842264521fa1bbf416c57f824cf2ca6580077233207e4937ce7b02e6377b0d` |

The structural HTML scan found one `main`, exactly 12 JSON-matching sections, embedded SVG,
the diagram table alternative, and print CSS. It found no active tags, remote resources/fonts,
`src`/`href`/event attributes, telemetry, or credential URI. Separate source scans found no
cloud/network/service imports, unsafe rendering/execution bypass, or credential markers.

Package artifacts were:

| Artifact | SHA-256 |
|---|---|
| wheel | `3050482c8734eb0b55527a28faf0cfec5b9e4c0ddeeb61390757d4a99f950655` |
| sdist | `4ba83fa6f10aae54716ebb5c338c51e15895a68364f876833d5048a555f0f357` |

## Publication and independent review

The implementation is not yet published. Therefore these fields are intentionally pending:

- Tested implementation SHA: **pending publication**
- Remote branch SHA: **pending publication**
- Pull request: **pending publication**
- CI/checks: **pending publication**
- Pending-diff specification review: **passed, 0 Critical / 0 Important / 0 Minor**
- Pending-diff code-quality review: **passed, 0 Critical / 0 Important / 0 Minor**

Both pending-diff review stages pass. A fresh independent detached exact-head verifier remains
the controller's required post-publication transition and is not represented by these reviews.

## Rollback and residual boundary

Rollback may remove the additive Phase 3 engine, framework assets, reporting services, CLI
commands, tests, and generated outputs without changing source engagement folders. Generated
outputs must remain outside the engagement root and may be regenerated from the pinned framework
and coherent source snapshot.

No Phase 4 web workflow, Phase 5 catalog, Phase 6 golden-pipeline evidence integration, Phase 7
mapping/deep-dive workflow, or Phase 8 release work is claimed.
