# Phase 7: End-to-end mappings, deep dives, and recipe extension

## Context links

- Parent: [plan.md](./plan.md)
- Dependencies: [Phase 5](./phase-05-capability-architecture-and-demo-catalog.md), [Phase 6](./phase-06-golden-retail-evidence-and-manifests.md)
- Decisions: [PD-03, PD-04, PD-11, PD-17](./architecture-decisions.md)
- Traceability: [AC-04, AC-07, AC-11; SM-06, SM-15–SM-17](./requirements-traceability.md)

## Overview

- Date: 2026-07-24
- Description: Complete the finding-to-action mapping chain, add initial high-value deep dives, and prove a future domain recipe is inert content rather than an engine/schema fork.
- Priority: P2
- Implementation status: Pending
- Review status: Pending golden evidence review.

## Key Insights

- Links across independent cores need typed semantics and provenance; a shared string ID is insufficient without validation.
- Deep dives refine one capability and evidence plan; they do not change quick-assessment history or introduce a second scoring engine.
- Quality, governance/metadata/lineage, and security/policy are the first deep dives because they exercise critical gates and map to available golden evidence.
- Extensibility is proved by content-only loading and hash/diff evidence, not by building another industry pipeline.

## Requirements

- Every critical finding follows: gap → business/AI impact → priority → recommendation → logical architecture → technology options → optional demo artifact → accountable action/roadmap.
- Mapping provenance identifies generated assessment fact, architect judgment, catalog reference, and demo illustration.
- Initial deep dives contain 15–30 anchored questions per selected domain, reuse evidence statuses, and preserve quick/deep results separately.
- Deep-dive outputs may refine findings/recommendations with explicit provenance; readiness changes only through the same versioned engine/gates and transparent recalculation.
- Add one sample future recipe conforming to extension schema without changing engine or core engagement schema.
- Web/report display missing/unavailable demo evidence honestly and remain fully useful without it.

## Architecture

`MappingResolver` consumes validated result/catalog/demo registries and produces a typed `FindingActionChain`. It cannot write assessment inputs or call the engine. Demo links are optional leaf references. `DeepDiveService` uses the existing answer, maturity, confidence, gate, finding, store, and report contracts with a `scope=deep-dive` discriminator and capability ID.

Initial deep dives:

| Content file | Size | Coverage |
|---|---:|---|
| `deep-dives/data-quality.yaml` | 20 questions | profiling, contracts, rule ownership, quarantine, observability, remediation |
| `deep-dives/governance-metadata-lineage.yaml` | 24 questions | ownership, glossary, metadata, technical/business lineage, change impact, reproducibility |
| `deep-dives/security-privacy-policy.yaml` | 20 questions | classification, minimization, masking, access policy, audit, retention, AI use |

Each question has 0–4 anchors and evidence guidance. Quick and deep-dive documents remain separate; the report labels source and assessment depth.

The extension fixture `assessment/tests/fixtures/recipes/manufacturing-maintenance-0.1.0/` contains only a recipe manifest, domain vocabulary, question extension, mapping, and absent-demo declaration. A pre/post tree hash excludes that fixture and generated caches; engine source and core schemas must be byte-identical. It is an inert proof fixture, not a supported second recipe or pipeline.

## Related code files

- Create: `assessment/src/assessment/catalog/mapping.py`
- Create: `assessment/src/assessment/domain/deep_dives.py`
- Create: `assessment/content/frameworks/1.0.0/deep-dives/{data-quality,governance-metadata-lineage,security-privacy-policy}.yaml`
- Create: `assessment/content/catalog/1.0.0/mappings/finding-action-chains.yaml`
- Create: `assessment/tests/contract/test_mapping_chain.py`
- Create: `assessment/tests/integration/test_deep_dive_recalculation.py`
- Create: `assessment/tests/fixtures/recipes/manufacturing-maintenance-0.1.0/{recipe.yaml,vocabulary.yaml,questions.yaml,mappings.yaml}`
- Create: `assessment/tests/contract/test_recipe_extension_is_inert.py`
- Modify: report/web review, deep-dive, roadmap, technology-options, and evidence-appendix views
- Modify: content schema only through the additive recipe extension point already defined in Phase 2

## Implementation Steps

1. Define the typed mapping-chain contract, provenance enums, optional demo leaf, accountable action fields, deterministic resolution/sort rules, and semantic validation.
2. Populate every Phase 1/v1 critical finding family with complete chain links and validate 100% coverage; include vendor-neutral options before optional local/AWS mappings.
3. Author and calibrate the three initial deep dives above (64 total questions) with anchors 0–4, evidence guidance, expected duration, and linked recommendations.
4. Implement deep-dive persistence/evaluation using existing services; preserve quick answers/results, label recalculation provenance, and show before/after gate explanations when new architect-entered evidence changes state.
5. Wire chain and deep-dive results into review/report/web, including unavailable-demo behavior and action/roadmap ownership.
6. Add the inert future recipe fixture through the public content extension loader only; do not add a pipeline, routes, engine branch, core field, vendor rule, or production content claim.
7. Capture pre/post hashes for `assessment/src/assessment/engine/` and core schema files; prove adding/removing the recipe fixture changes neither hash nor existing scenario/report results.
8. Run semantic, unit, scenario, report, and bounded browser tests with demo manifests present, absent, and corrupt; corrupt content fails validation while assessment source remains recoverable.

## Todo list

- [ ] Define and validate the full mapping-chain contract.
- [ ] Map 100% of critical finding families through accountable action.
- [ ] Author/calibrate quality, governance-lineage, and security-policy deep dives.
- [ ] Preserve quick/deep provenance and transparent recalculation.
- [ ] Display mapping/deep-dive outputs in review/report/web.
- [ ] Add inert future recipe fixture only.
- [ ] Prove engine/core schema hashes and existing outputs are unchanged.
- [ ] Test demo-present/absent/corrupt behavior.

## Success Criteria

- Every critical finding has a complete, resolved, provenance-labeled gap-to-action chain.
- All three deep dives contain 15–30 fully anchored questions and use the same confidence/evidence statuses.
- Quick assessment history is unchanged; any readiness recalculation names deep-dive inputs and emits a fresh full gate trace.
- Demo artifacts are optional leaves and never feed score/gate/priority; assessment/report remain usable with no demo outputs.
- Adding/removing the recipe fixture leaves engine source, core schemas, existing scenario outputs, and report JSON hashes unchanged.
- `make assessment-contract assessment-test assessment-scenarios assessment-report assessment-e2e` passes without heavy services.

## Risk Assessment

- Cross-reference graphs can form cycles; validate allowed edge types and reject cycles where traversal requires a DAG.
- Deep dives may silently overwrite quick results; separate documents/scopes and immutable prior result digests.
- More questions may exceed workshop time; deep dives are selected after review and have independent duration guidance.
- A sample recipe can be mistaken for supported product scope; keep it under tests/fixtures and label it non-production/inert.
- Rollback: remove the inert recipe fixture and restore the prior mapping/deep-dive content pointer. Quick assessment documents and earlier result digests remain authoritative and are never deleted.

## Security Considerations

Deep-dive content and architect notes follow the same safe YAML/Markdown, escaping, and export hygiene rules. Security/privacy evidence must be synthetic or redacted; the tool does not request secrets, raw customer records, credentials, or system access. Mapping URLs cannot fetch remotely during build/runtime.

## Next steps

Review P6–P7 as a slice. Then run Phase 8's clean-checkout, portability, security, resource, regression, docs, and release gates across the entire implementation.
