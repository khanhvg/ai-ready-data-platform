---
phase: 6
title: "Architecture Curriculum Templates and Fitness Functions"
status: pending
priority: P1
dependencies: [3, 5]
effort: "L"
---

# Phase 6: Architecture Curriculum Templates and Fitness Functions

<!-- Updated: Validation Session 1 - placed curriculum expansion after the runnable journey. -->

## Overview

Publish the foundation-to-mid architecture curriculum, reusable templates, minimum useful local
and AWS C4 sources, ADR/traceability conventions and executable architecture fitness functions.
Every pattern/view exists only for a stakeholder concern or controlled failure. Expansion starts
only after the merged Phase 5 promotion-trust E2E SHA, so the first accepted runner-backed journey
remains the earliest accepted product outcome.

## Context Links

- [Curriculum and competency map](./curriculum-and-competency-map.md)
- [Requirements/view catalogue](./requirements-traceability.md)
- [ADR backlog](./architecture-decisions.md)
- C4 official sources S01-S03 and API sources S04-S05 in discovery source register

## Requirements

- Implement competency/prerequisite graph and diagnostic/remediation paths.
- Provide templates for stakeholder/outcome, capability/value stream, FR/NFR/ASR, C4 concern,
  ADR, API taxonomy, threat model, cost/state/recovery and fitness evidence.
- Structurizr sources cover C4-L0/L1, local/AWS containers, runner component, local/AWS deployment,
  and only the named critical dynamic views.
- Each view declares audience, scope, concern, legend, source version and text alternative.
- Validate OpenAPI and only create AsyncAPI on actual channel admission.
- Encode pattern-admission test: pattern/service must reference a failure/quality attribute and
  verifier.
- Teach DNS/TLS/gateway/LB/subnets/routes/NAT-or-endpoints/SG/service discovery/mTLS where the
  local/AWS deployment concern requires them.
- Keep technology and numeric claims sourced/versioned.
- Consume the six I5-01 local views read-only; own curriculum/AWS expansion and `DYN-PUBLISH`.
- Ship one executable F01→F04→J01/J04/J05 architecture lab with controlled boundary/resilience
  failure, hints, reset, fitness verification, evidence and reflection; templates are insufficient.

## Architecture

`architecture/structurizr/workspace.dsl` includes stable model and view fragments. A manifest
maps view IDs to stakeholder concern, lesson, ADR and rendered/text outputs. The portal consumes
generated assets, never hand-copied diagrams. Source is authoritative.

## File Inventory

| Action | Planned path | Rough size | Test impact |
|---|---|---:|---|
| Modify under released include seams | `architecture/structurizr/{model/**,views/**}` excluding I5-01 local sources | 600-1,000 lines | Curriculum/AWS expansion and DYN-PUBLISH |
| Modify under a time-bounded sequential view lease | `architecture/structurizr/view-manifest.yaml` and workspace expansion includes | 120-200 lines | Add only P6 expansion rows/includes; I5-01 local rows and sources remain read-only |
| Create | `architecture/rendered/<P6-owned-view-id>.{svg,txt}` | generated | Expansion-only portal/review artifacts; no overwrite of I5-01 local renders |
| Create | `learning/curriculum/{competencies,pathways}.yaml` | 300-500 lines | DAG/coverage |
| Create | `learning/templates/{stakeholder,requirements,c4-view,adr,threat-model,state-cost-recovery,fitness}.yaml` | 500-800 lines | Template validation |
| Create | `learning/labs/architecture/first-boundary-journey/**` | 500-800 lines | Executable architecture-first lab |
| Create | `docs/decisions/template.md` and initial implementation ADRs | 150-300 lines | ADR lint |
| Create | `tests/architecture/**`, `tests/curriculum/**` | 600-900 LOC | Broken IDs/links/views/pattern admission |
| Create | `scripts/architecture/{check,render}.sh` or platform-neutral wrapper | 150-250 LOC | Pinned tool command |
| Create | `mk/issue-5/i5-06.mk` | 20-40 lines | Fitness targets via root include |

## Interface Checklist

- [ ] stable element/view/relationship IDs
- [ ] view manifest schema and `concernId/lessonId/adrIds`
- [ ] competency/prerequisite DAG
- [ ] template registry/versioning
- [ ] pattern `addressesFailure/qualityAttribute/verifierId`
- [ ] render manifest with source hash/tool version/output hashes/text alternative

## Dependency Map

- Depends on released contract/reference IDs.
- No Phase 6 branch, generated asset, contract write, or merge begins before the merged Phase 5
  E2E SHA. Read-only notes drafted earlier are not implementation inputs.
- Feeds data/AWS/AI lessons and release checks.

## Test Scenario Matrix

| Priority | Scenario | Expected |
|---|---|---|
| High | Missing/stale element or view ref | Architecture check fails |
| High | View has no audience/concern/text equivalent | Manifest validation fails |
| High | Pattern/service without failure/verifier | Curriculum check fails |
| High | Cyclic prerequisite/unreachable foundation route | DAG check fails |
| High | Logical API layer treated as service count | Container/taxonomy assertion fails |
| Medium | Unrenderable diagram/font/label overlap | Render/visual review fails |

## Tests Before

Create broken DSL, stale-ref, missing-concern, circular-prerequisite and technology-museum
fixtures. Write expected minimum view list and render manifest assertions.

## Refactor

Move Phase 1 skeleton into include fragments only if it reduces merge/conflict complexity.
Preserve IDs and generated artifact paths.

## Tests After

Validate/export every source, compare manifest hashes, run link/ID/concern coverage and inspect
rendered local/AWS deployment and dynamic views at desktop/mobile/200% portal contexts.

## Regression Gate

```bash
make curriculum-check
make architecture-check
make architecture-render
make traceability-check
make api-contracts-check
make architecture-lab-e2e
```

## Implementation Steps

1. Write failing competency/view/template/pattern fitness fixtures.
2. Encode curriculum graph and reusable architecture/decision templates.
3. Preserve the released I5-01 local views and add the publish/AWS expansions under include seams.
4. Add AWS model/deployment/office-hours/restore source with TBC labels, not false decisions.
5. Pin renderer/validator and emit render manifest/text alternatives.
6. Add portal asset integration and review all diagrams for purpose/readability.
7. Build and verify the executable architecture lab; cross-link requirements, ADRs, phases/issues,
   tests and evidence.

## Success Criteria

- [ ] Foundation→mid curriculum graph is acyclic, reachable and competency-based.
- [ ] Required minimum useful C4/dynamic/deployment views validate/render with text alternatives.
- [ ] The architecture-view lease changes only P6-owned expansion rows/includes/renders and closes
  at one exact release SHA before any downstream consumer starts.
- [ ] Logical taxonomy and physical container count are explicitly separate.
- [ ] Every named pattern/service maps to a failure/quality attribute and evidence.
- [ ] Portal can consume generated diagrams without duplicating source.

## Risk, Security, and Rollback

Diagram breadth can become decorative debt. The manifest rejects views without a concern/lesson.
AWS secrets/endpoints never appear in sources. Rollback restores the prior DSL/manifest version;
generated renders are disposable.

## Next Steps

Use templates in Phase 7 data labs and Phase 9 AWS decisions.
