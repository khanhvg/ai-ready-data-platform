---
phase: 6
title: "Architecture source validation and deterministic render"
status: pending
effort: "2.0-3.0 implementation days"
dependsOn: [1, 2, 3, 4, 5]
---

<!-- Updated: Initial validation made npm-lock reproduction/staging and SVG semantic preservation explicit. -->

# Phase 6: Architecture source validation and deterministic render

## Overview

Create exactly six minimum-useful LikeC4 source views and deterministically derive accessible SVG plus semantic text. Use the probed, pinned chain in [architecture-toolchain-decision.md](./architecture-toolchain-decision.md); no Java, Structurizr export claim, browser or native fallback.

## Requirements

- Exact external IDs and internal key mapping; computed view set exactly six.
- C4 abstraction/scope/required elements/relations, audience/concern/owner/legend/traceability enforced by project fitness wrapper.
- Semantic `.txt` generated from computed JSON, not SVG; dynamic step order preserved.
- SVG normalization/accessibility/security and JCS render input freshness.
- Two renders plus a second empty-cache install yield byte equality on the only current support
  lane: native Darwin arm64. Linux tuple hashes are future compatibility inputs only; this cook
  neither claims nor requires Linux execution.
- I5-06 additions-only lease cannot mutate the original six.
- The 119-record npm lock is reproduced twice at SHA-256 `7a56d803…`; because `package-lock.json` is ignored and `.gitignore` is protected, only its exact path may be force-added after verification.

## File inventory

| Action | Planned path | Purpose |
|---|---|---|
| Create | exact `architecture/likec4/**` paths listed in handoff | model and six view sources/manifest |
| Create | exact 12 SVG/TXT files plus `render-manifest.json` | deterministic derived outputs |
| Create | `requirements/architecture/{package.json,package-lock.json}` | Node toolchain lock |
| Create | scoped architecture scripts under `scripts/golden/**` | check/render/text/normalize/fitness |
| Create | `tests/contracts/test_architecture_contract.py` | model/manifest/C4/text/freshness mutations |
| Create | `tests/golden/test_architecture_determinism.py` | empty-cache/two-render/atomicity |

## Dependency map

- Uses phase 3 private staging/process core and phase 4 JCS/envelope.
- Executes after phase 5 in the one-writer cook, even though it has no semantic dependency on the
  promotion fixture candidate.
- Blocks phase 7 public targets and phase 8 completion.
- I5-06 gets a later serialized additions-only lease after merged I5-05.

## Test scenario matrix

| Scenario | Expected |
|---|---|
| malformed/undeclared relation | LikeC4 structured non-zero validation |
| implicit extra index/later AWS/AI/DYN-PUBLISH view | `ARCH_VIEW_SET_MISMATCH` |
| wrong abstraction/missing concern/legend/required element/orphan | `ARCH_C4_FITNESS_FAILED` |
| text scraped from SVG, missing relation/dynamic step | `ARCH_TEXT_ALTERNATIVE_FAILED` |
| script/external URL/foreignObject/private path in SVG | normalization security failure |
| source/tool/normalizer changes without outputs | `ARCH_OUTPUT_STALE` |
| reused DOT directory preserves obsolete file | reject pre-existing staging directory |
| two renders/install roots differ | `ARCH_OUTPUT_NONDETERMINISTIC` |
| missing exact Node/npm/package | typed failure, no skip/fallback |

## Interface checklist

- [ ] `index` maps only to external `C4-L0`; other five mappings exact.
- [ ] Model validation and project C4 fitness are separate required layers.
- [ ] Text contains stable semantic inventory and no layout/private values.
- [ ] Render manifest input hash excludes output hashes.
- [ ] Committed outputs replace atomically only as a complete six-set.

## Tests Before

1. Add manifest schema and exact six/minimum-useful-view expectations.
2. Add malformed references, abstraction/concern/legend/orphan/later-view mutations.
3. Add deterministic text/SVG normalization/security/freshness vectors, including semantic ID/text/style/path/geometry mutations that normalization must preserve.
4. Add missing-tool/version/lock and atomic staging failure cases.
5. Confirm expected failures because sources/locks/renders are absent.

## Implementation

Bootstrap exact Node/npm/lock in a private root; validate/format/export computed JSON and DOT; enforce project fitness; generate text; render using embedded WASM Graphviz; normalize and hash; stage twice; atomically install only the complete set. `architecture-check` privately regenerates and compares without modifying committed output.

## Refactor

Keep source semantics, C4 fitness, text generation, SVG render, normalization and freshness hashing independently testable. Vendor version changes cannot leak behind stable wrappers without manifest/lock migration.

## Tests After

- Two renders in the first install and one render in a second empty-cache install are byte-identical.
- Every source/model/manifest/output/tool mutation fails the named assertion.
- SVG/XML security and text accessibility checks pass all six.
- Original six hashes remain protected in a simulated additions-only lease.

## Regression Gate

- Six sources, six SVGs, six semantic text alternatives and one render manifest are complete/fresh.
- Required missing tools are failures; no unsupported capability claim.
- F-07 and architecture portion of SC-09 pass.

## Failure Evidence, Rollback and STOP

Retain the exact tool fingerprint, computed JSON/DOT, fitness mutation, staged-set inventory and
semantic SVG/text diff. Rollback restores source/manifest/package-lock/rendered outputs as one
reviewed coherent set; never install a partial render set. STOP on an unsupported host, missing or
wrong tool/license/integrity, non-six view set, invalid C4 fitness, semantic-erasing normalization,
stale/nondeterministic output, partial atomic publication or any Java/Structurizr/browser/native/
global/remote-runtime fallback.

## Success criteria

- [ ] Selected pinned chain validates and renders reproducibly.
- [ ] C4 semantics and stakeholder concerns are machine-checked.
- [ ] Accessible text and normalized SVG are deterministic and safe.
- [ ] Rollback restores one coherent source/tool/output set.
