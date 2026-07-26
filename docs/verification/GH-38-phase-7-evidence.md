# GH-38 Phase 7 verification

## Overview

Phase 7 implements deterministic finding-to-action mappings, the initial three
deep dives, explicit reviewed promotion revisions, report/web presentation, and
one inert manufacturing-maintenance recipe fixture. It starts from integration
merge `b24fc56546f3f70a2057c0b9dde3f35874a0f5ab`. Phase 8 release and
clean-checkout finalization remain out of scope.

The implementation is local-only. It performs no cloud action, remote mapping
fetch, upload, pipeline control, arbitrary command execution, or SQL execution.
Demo evidence remains optional and never contributes to scoring, gates, or
priority.

## Contract evidence

- Eight of eight critical finding families resolve a typed chain from generated
  gap and impact through priority, recommendation, logical architecture,
  vendor-neutral technology options, optional demo leaf, and accountable
  roadmap action.
- Provenance distinguishes generated assessment facts, architect judgment,
  catalog references, and demo illustration. Technology profile references are
  content-only and non-executable.
- Deep-dive content contains exactly 20 data-quality, 24
  governance/metadata/lineage, and 20 security/privacy/policy questions. Every
  question has complete 0–4 anchors, evidence guidance, duration,
  confidence/evidence semantics, and recommendation links.
- Quick, deep-dive, and promoted result documents are separate. Promotion is
  explicit, architect-reviewed, digest-bound, conflict-complete, and produces a
  new result revision with seven fresh gate traces while retaining the prior
  reportable revision.
- Archive preflight recomputes and validates the complete advisory, answer,
  result, promotion, and active-pointer graph. It replays recorded promotion
  semantics and rejects stale digests, broken links, duplicate conflict choices,
  and consistently rehashed answer tampering before export or import.
- Report JSON, standalone HTML, and loopback pages display active/prior
  revisions, mappings, roadmap actions, technology choices, evidence appendix,
  and demo present/absent/unavailable states. Corrupt demo content fails closed
  at the demo boundary while the assessment source remains recoverable.

## Test-first provenance

Initial RED was retained contemporaneously: the Phase 7 mapping, deep-dive, and
recipe modules did not exist. Review corrections also began with reproducible
failures for stale promotion targets, unusable prior report selection, mixed
`Not assessed` promotion, broken archive graphs, consistently rehashed
promotion tampering, and contradictory duplicate conflict choices. Each
correction has a focused regression.

The final exact-tree verification includes:

| Command | Result |
|---|---|
| `make assessment-contract assessment-test assessment-scenarios assessment-report assessment-e2e` | Pass: 48 contract checks; 225 tests passed with one unchanged object-store boundary skip and two E2E deselections in the non-E2E target; 6 scenario goldens; 8 report-contract tests; 2 real Chromium E2E tests |
| `make assessment-runtime-smoke` | Pass: Chromium via Playwright 149, 30 quick answers, 20-question deep dive, reviewed promotion, seven gate traces, active/prior revision display, report/export/import, demo absent/unavailable/corrupt handling, narrow/wide/200% layout, local-only traffic, and clean teardown |
| `make assessment-lint assessment-typecheck` | Pass: Ruff clean and strict mypy clean over 53 source files |
| `make assessment-build` plus isolated wheel/sdist loads | Pass: inventory explicitly checks 121 packaged files; isolated installs each load deep-dive counts `[20, 24, 20]` and eight mapping chains |
| `make assessment-diagrams` | Pass: five adversarial renderer tests and seven deterministic reviewed diagram pairs |
| `make assessment-store assessment-migration assessment-import-export assessment-security-scan assessment-engine` | Pass: 10 store, 10 migration, 30 archive with one unchanged skip, 29 security subset with the same skip, and 28 engine tests |
| `make demo-contract demo-verify` | Pass: nine stages, 30/30 automation, canonical 11 marts, seven denied/one allowed policy cases, 990 safe rows, and 41 demo/catalog contract tests |
| `docker compose config --quiet` | Pass |
| tracked Python compilation and `git diff --check` | Pass |

The current retail regression also regenerated 6,812 deterministic source rows,
completed dbt with `PASS=205`, `WARN=7`, `ERROR=0`, retained exactly 11
canonical marts, and preserved the nine-stage demo manifest truth. Heavy
optional profiles were not started.

## Inert recipe proof

The fixture is confined to
`assessment/tests/fixtures/recipes/manufacturing-maintenance-0.1.0`, labels
itself inert and non-production, declares demo status absent, exposes no
pipeline route, and loads only through the additive recipe loader.

Adding and removing a copied fixture produces no delta:

| Surface | SHA-256 |
|---|---|
| Engine source tree | `dbeeb85792d5a92222ae9e8b9ee1b95f932f9ff1c8d2e46b2abb169980dce3be` |
| Core schema tree | `2821c1fa13627eb8f671ed899dc032773317f9ed7b1efa08243e212bbf31df81` |
| Scenario report set | `dc3487bda18a6947eeae7398261331fc9c2f27a08db8c527d6c1b4bd31d068ed` |

The four individual scenario report hashes are recorded in the fixture's
tracked `inertness-proof.json` and are asserted before and after fixture
addition/removal.

## Review, limitations, and rollback

Producer specification and code-quality review passed with zero Critical, zero
Important, and zero Minor findings after all corrections and invalidated tests
were rerun. Publication records the tested commit and remote/PR equality. A
completely fresh detached exact-head verifier remains mandatory and
controller-managed; the producing worker does not merge or enable auto-merge.

The one unchanged object-store boundary test remains skipped because object
storage is intentionally outside the local filesystem implementation. Rollback
removes the additive mapping/deep-dive content and inert fixture and restores
the prior content pointers; it never deletes engagement history, named volumes,
or cloud resources.
