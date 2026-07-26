---
title: "Issue #38 Phase 7 mappings, deep dives, and recipe extension"
date: 2026-07-26
type: technical-journal
status: implementation-complete
authority: work-history-only
---

# Issue #38 Phase 7 mappings, deep dives, and recipe extension

## Context

Phase 7 started from the clean, immutable Phase 6 integration input
`b24fc56546f3f70a2057c0b9dde3f35874a0f5ab` and the audited plan package at
`0b5335d907397bb8fd4f7a8c794ff2e930b6fe6b`. The slice was deliberately bounded
to mappings, three deep dives, reviewed promotion, report/web integration, and
one inert recipe fixture. Phase 8 release, deployment, hosted operation, cloud
actions, alternate pipelines, and engine/schema forks remained outside scope.

This entry is chronological work history. Current contracts, architecture
documentation, tests, and published verification evidence remain authoritative.

## What happened

1. Provenance was checked before product edits: the branch was clean at the
   required input, the audited Phase 7 plan and dependencies were read, and no
   rebase onto later integration work was performed.
2. Tests-first RED evidence established that mapping, deep-dive, and recipe
   modules did not yet exist. The first GREEN slice added a read-only
   `MappingResolver`, eight deterministic critical-finding chains, and complete
   resolution of recommendation, architecture, technology, optional demo, and
   accountable-roadmap references.
3. Three versioned advisory question banks were added with the planned
   20/24/20 split. All 64 questions have complete 0–4 anchors, evidence
   guidance, duration, confidence semantics, and recommendation links.
4. Quick results and deep-dive documents were separated. Promotion became an
   explicit architect-reviewed operation bound to source and target digests,
   capability IDs, rationale, engagement-metadata time, and complete conflict
   choices. Successful promotion creates a new engine-produced revision with
   seven fresh gate traces while retaining the prior reportable revision.
5. Review, report, CLI, and loopback views gained mapping chains, technology
   options, roadmap actions, advisory completion, explicit promotion, and
   active/prior revision selection. Demo leaves remained read-only and
   non-scoring for present, absent, unavailable, and corrupt states.
6. An inert, non-production manufacturing-maintenance fixture was loaded only
   through the public additive recipe extension. Its add/remove proof preserved
   engine source, core schemas, existing scenario outputs, and report hashes.

## Verification and review corrections

Specification review first found no Critical findings and five Important
findings. The implementation was corrected to:

- bind promotion targets to active revision, active result, and selected answer
  state, rejecting stale replay;
- make retained revisions explicitly selectable and reportable in CLI and web
  flows without implicit latest-wins behavior;
- resolve vendor-neutral alternatives and content-only profile tools through
  validated catalog role IDs;
- label authored action and technology content as catalog references instead of
  architect judgment; and
- exercise corrupt demo validation through a real loopback browser response
  while proving the assessment source remains recoverable.

Later review cycles tightened revision and archive semantics further:

- report status now evaluates the source state of the selected revision,
  distinguishing a mutable first active quick report from an explicitly
  retained prior report;
- mixed assessed and `Not assessed` advisory answers aggregate evidence from
  assessed answers without allowing an unanswered item to overwrite their
  evidence status;
- archive preflight validates the complete cross-document revision graph,
  active pointer, answer documents, result digests, promotion records, and
  before/after links;
- imported reviewed promotions are semantically replayed through the same
  answer merge and engine behavior instead of trusting internally consistent
  hashes alone;
- contradictory or duplicate conflict choices are rejected before promotion;
  and
- portability coverage includes standard quick state, `use-quick` promotion,
  and quick-synchronization cases in addition to promoted deep-dive state.

Review-driven tests covered all three deep dives and every declared capability.
The final producer exact gate recorded 225 passed, one unchanged documented
skip, and two deselected tests. The two real-browser end-to-end journeys passed,
strict type checking and lint remained clean, and runtime acceptance completed
with local-only requests and clean browser/server teardown. Representative
retail regression retained 6,812 synthetic source rows, dbt
`PASS=205 WARN=7 ERROR=0`, the canonical 11 marts, nine demo stages, and the
existing deterministic policy/demo truth.

Final producer specification review and code-quality review each closed with
Critical=0, Important=0, and Minor=0. Publication and the mandatory
controller-managed fresh independent exact-head verifier were still pending at
this journal checkpoint.

## Decisions

- An explicit active pointer owns assessment revision selection; file ordering
  and modification time never choose truth.
- Advisory output cannot change readiness without a complete, digest-bound
  promotion record.
- Prior revisions remain immutable and explicitly reportable after promotion.
- Mapping URLs and demo references are inert presentation data and never feed
  scoring, gates, priority, network access, or execution.
- The manufacturing fixture remains under tests and is evidence of additive
  extensibility, not a supported production recipe.

## Reflection

The most valuable review pressure was on provenance and revision identity.
Preserving old files was insufficient until users could deliberately select and
regenerate them, and a target digest was insufficient until it bound all state
that could change the promotion result. Likewise, typed graph edges only became
trustworthy when technology and action nodes resolved to their actual catalog
owners. The corrupt-demo browser path confirmed that fail-closed validation and
recoverable assessment truth must be demonstrated together.

## Next

- Publish the bounded Phase 7 branch in a non-draft PR without merging it.
- Record exact tested-head commands, review counts, runtime evidence, inertness
  proofs, configured-check state, limitations, and rollback in the PR and Issue
  #38 evidence.
- Run the controller-managed fresh detached exact-head verifier.
- Leave Phase 8 clean-checkout, portability, security, resource, regression,
  documentation, and release finalization for its own slice.
- AgentWiki publication was skipped because authorization is limited to the
  GitHub workflow for this issue.
