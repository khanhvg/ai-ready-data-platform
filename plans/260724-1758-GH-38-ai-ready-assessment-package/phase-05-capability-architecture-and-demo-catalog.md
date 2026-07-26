# Phase 5: Capability, architecture, mapping, and Demo Guide catalog

## Context links

- Parent: [plan.md](./plan.md)
- Dependencies: [Phase 3](./phase-03-deterministic-engine-and-report-generation.md), [Phase 4](./phase-04-loopback-web-assessment-workflow.md)
- Decisions: [PD-03, PD-04, PD-11, PD-14, PD-21](./architecture-decisions.md)
- Traceability: [AC-01, AC-04–AC-05, AC-08; SM-02, SM-06, SM-15–SM-16](./requirements-traceability.md)
- Architecture baseline: repository `docs/system-architecture.md`

## Overview

- Date: 2026-07-24
- Description: Populate the versioned capability, logical architecture, vendor-neutral technology mapping, Demo Guide, and multi-audience diagram catalog.
- Priority: P2
- Implementation status: Completed
- Review status: Completed through merged Phase 5 verification evidence.

## Key Insights

- The catalog explains options and patterns; technology presence is never a maturity criterion.
- AWS is the first optional implementation mapping, not the logical architecture or an authorization to provision cloud resources.
- Different conversations require different diagrams; one dense poster is explicitly rejected.
- Demo Guide entries explain how an existing artifact illustrates a pattern and remain read-only/non-scoring.

## Requirements

- Complete the advisory's exact 10-domain capability catalog: strategy/ownership/operating model; sources/ingestion/integration; storage/lifecycle/organization; transformation/orchestration; quality/reliability; metadata/catalog/glossary/lineage; governance/privacy/compliance; security/access/policy-as-code; observability/operations/cost; data products/analytics/AI readiness.
- Logical architectures for quality, governance/ownership, metadata/lineage, security/privacy/policy, platform/integration, operations, and AI-ready data products.
- Vendor-neutral option sets with AWS as the first named implementation profile and the current sandbox as a separate local demo-evidence mapping; exactly one selected tool per role in the AWS profile and no vendor scoring.
- Multiple audience-appropriate Mermaid+SVG diagrams with textual/table alternatives.
- Demo Guide and stage catalog versioned independently from assessment framework.
- Semantic validation of every capability→architecture→technology→demo reference.

## Architecture

Catalog content lives in `assessment/content/catalog/1.0.0/`; it is loaded through the same safe content registry but never imported by maturity/gate modules. Architecture entries contain problem, forces, logical components, controls, data flows, trade-offs, evidence expectations, and mappings. Technology entries identify role/capability fit, constraints, and alternatives—not weighted product rankings. The AWS v1 profile selects S3, Glue Data Catalog, Athena, Lake Formation, dbt Core with dbt-athena, Soda Core, OpenMetadata, Apache Superset, Terraform source, and the deterministic synthetic generator for their distinct roles. The local evidence profile describes the already-proven sandbox separately. Neither profile is executable from the assessment web.

Required audience diagrams:

| Source/rendered file | Primary audience | Purpose |
|---|---|---|
| `diagrams/executive-ai-readiness.{mmd,svg}` | Executive sponsor | Capabilities, gates, readiness, roadmap relationship |
| `diagrams/logical-platform-context.{mmd,svg}` | Enterprise Architect | Vendor-neutral target-state boundaries |
| `diagrams/engagement-lifecycle.{mmd,svg}` | Solution Architect | Create→assess→review→deep dive→report→portable archive |
| `diagrams/scoring-and-gates.{mmd,svg}` | Architect/reviewer | Maturity, confidence, gates, findings separation |
| `diagrams/security-and-access.{mmd,svg}` | Security/data governance | Classification, policy decision, masked product, evidence |
| `diagrams/metadata-and-lineage.{mmd,svg}` | Data/platform architect | Source→transform→product metadata/lineage proof |
| `diagrams/demo-evidence-mapping.{mmd,svg}` | Demo presenter | Read-only stage artifacts mapped to catalog patterns |

SVG rendering is deterministic through a build-only locked `assessment/diagram-tools/package.json`/lock, tested Node major, and pinned Mermaid CLI. `make assessment-diagram-install` is the only network-permitted provisioning step; `make assessment-diagrams-update` explicitly updates normalized reviewed SVG and the source/tool/output digest manifest, while `make assessment-diagrams` renders into a temporary directory and verifies parity without modifying the worktree. It is not part of the Python application runtime or a frontend application build. Shipped web/report paths use committed reviewed SVG and text alternatives, not a browser Mermaid runtime.

## Related code files

- Create: `assessment/content/catalog/1.0.0/catalog.yaml`
- Create: `assessment/content/catalog/1.0.0/capabilities/*.yaml`
- Create: `assessment/content/catalog/1.0.0/architectures/{quality,governance-metadata-lineage,security-policy,platform-integration,operations,ai-data-products}.yaml`
- Create: `assessment/content/catalog/1.0.0/technology-mappings/{aws-first-profile,local-demo-evidence,alternatives}.yaml`
- Create: `assessment/content/catalog/1.0.0/diagrams/*.{mmd,svg}`
- Create: `assessment/content/catalog/1.0.0/diagrams/render-manifest.json`, `assessment/diagram-tools/{package.json,package-lock.json,render.mjs}`
- Create: `assessment/content/demo/1.0.0/{stages.yaml,demo-guide.yaml,evidence-links.yaml}`
- Create: `assessment/src/assessment/catalog/{models.py,loader.py,renderer.py}`
- Create: `assessment/tests/contract/test_catalog_semantics.py`, `assessment/tests/contract/test_diagram_assets.py`
- Modify: report/catalog/demo templates to consume catalog services only
- Modify: `Makefile` for `assessment-diagram-install`, `assessment-diagrams-update`, and non-mutating `assessment-diagrams`

## Implementation Steps

1. Author all 10 capability entries and evidence examples using architect/customer language; distinguish self-report, customer evidence, architect judgment, and demo illustration.
2. Author vendor-neutral logical architecture patterns and link every critical finding family to at least one appropriate pattern.
3. Author the AWS-first profile with the single role selections in PD-21, then map the existing local sandbox as demo evidence and list deferred alternatives. Verify no technology name appears in maturity anchors/gates, no two selected products compete for one role, and no cloud action exists.
4. Pin the build-only Node/Mermaid toolchain, then create the seven diagram source/render pairs above with accessible title/description and adjacent textual/table alternatives; use the explicit update target to normalize/record source/tool/output digests and the non-mutating target to reproduce them in a temporary directory.
5. Author the versioned Demo Guide/stage catalog with presenter goal, prerequisites, read-only artifact locations, expected evidence, limitation, cleanup, and non-scoring disclaimer.
6. Implement catalog loading/query/rendering and wire report/web read-only views through it; unavailable artifacts display as unavailable, not failed customer capabilities.
7. Add semantic checks for unique/resolved IDs, audience/purpose, diagram source/render parity, technology neutrality, and complete finding links.
8. Review the executive, architect, security, lineage, and presenter views with their intended reading level; record edits in content, not route/report code.

## Todo list

- [x] Complete all 10 capability catalog entries.
- [x] Complete vendor-neutral architecture patterns and mappings.
- [x] Add the AWS-first profile, local demo-evidence profile, and alternatives without scoring vendors.
- [x] Produce and review seven audience-specific diagram pairs.
- [x] Complete versioned Demo Guide/stage content.
- [x] Wire read-only catalog/report/web presentation.
- [x] Pass semantic, diagram parity, and technology-neutrality checks.

## Success Criteria

- Every domain, critical finding, recommendation, architecture, technology mapping, and Demo Guide reference resolves.
- The catalog contains all seven diagram pairs with audience, purpose, accessible alternative, and deterministic source/render parity.
- Maturity/gate modules and framework anchors contain no technology/product-presence criterion.
- AWS mappings are content only; no credentials, SDK calls, Terraform, or provisioning command exists.
- Report and web display catalog/demo content through validated services and honestly mark missing artifacts.
- After the explicit diagram/bootstrap install, `make assessment-diagrams assessment-contract assessment-build assessment-e2e` passes with network disabled and no heavy services; the installed Python package/runtime has no Node or Mermaid dependency.

## Risk Assessment

- Catalog scope can expand indefinitely; limit v1 to the 10 domains and finding patterns proven in Phase 1.
- Technology mappings age faster than logical patterns; version them independently and record tested/published date.
- Rendered diagrams can drift from source; verify normalized content digest and fail build on mismatch.
- Audience views may conflict; derive shared facts through references and review each view's intended decisions.
- Rollback: restore the prior catalog/demo-content version pointer and remove only the new additive content/rendered assets after retaining their source. Engine and engagement schemas require no rollback.

## Security Considerations

Diagram and Markdown rendering must disallow raw HTML, script, foreign-object, remote images, and external fetches. Catalog technology mappings cannot embed credentials/account IDs. Demo links are normalized repository-relative paths and displayed read-only; unavailable path resolution never falls back outside configured roots.

## Next steps

Review P4–P5 as a slice. Then Phase 6 may add only the missing golden retail evidence and bind its manifests to the already-versioned read-only Demo Guide contract.
