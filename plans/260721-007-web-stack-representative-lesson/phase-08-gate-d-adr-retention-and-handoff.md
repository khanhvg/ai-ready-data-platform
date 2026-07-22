---
phase: 8
title: "Gate D ADR Retention and Handoff"
status: pending
priority: P1
dependencies: [7]
effort: "remaining portion of Gate C final 2-hour window"
barrier: blocked-on-complete-gate-c-evidence
---

# Phase 8: Gate D ADR Retention and Handoff

## Context Links

- [Candidate protocol](./candidate-protocol.md)
- [Implementation handoff](./implementation-handoff.md)
- [Master ADR-005](../260721-005-enterprise-learning-sandbox/architecture-decisions.md#adr-005-web-stack-scorecard)

## Overview

Publish a machine/human-readable ADR-005 proposal backed by the complete Gate C record, or an
explicit no-winner proposal when evidence is invalid/incomplete or all candidates are eliminated.
Retain the neutral preview, sources, locks, commands, hashes, raw evidence, browser/manual records,
timers, eliminations, and non-copy inventory through I5-05. This phase proposes; human pre-merge
approval and later issue-specific gates remain mandatory.

## Requirements

- Write `docs/decisions/0005-web-stack.md` with status `Proposed`, exact tested/dependency SHAs,
  fixture/contract/mode/lock/test digests, decision or no-winner, consequences, rejected/eliminated
  alternatives, risks, rollback, and I5-05 boundary.
- Write scorecard Markdown/JSON at the issue-authorized exact paths. JSON is the machine gate and
  contains no score for eliminated/incomplete candidates.
- A winner requires full must-pass and comparable score evidence. A no-winner is mandatory for
  absent/mixed fixture, unavailable browser/manual review, invalid comparability, no passing
  candidate, or cap expiry.
- Exclude losing candidate builds from all default/product/workspace entrypoints. Keep explicit
  issue-local reproduction targets; do not wire a root `make learn-preview` alias here.
- Retain all three candidate source trees and lockfiles through I5-05. Transient `node_modules`
  and build caches may be safely removed after hashed artifacts/commands are retained; losing
  source deletion requires separate post-I5-05 authority.
- Keep common tests/contract and neutral preview independent of the selected framework.

## Architecture

Machine scorecard JSON is generated from verified Gate C indexes and is authoritative for
consistency; human Markdown and ADR explain the same result. A retention index separates tracked
reproducibility inputs from transient build/runtime state. No product selector or root command is
created.

## File Inventory

| Action | Planned path | Purpose | Test impact |
|---|---|---|---|
| Create | `docs/decisions/0005-web-stack.md` | Proposed winner/no-winner ADR | Decision gate |
| Create | `docs/decisions/evidence/adr-0005-web-stack-scorecard.md` | Human evidence/rationale | Review |
| Create | `docs/decisions/evidence/adr-0005-web-stack-scorecard.json` | Machine must-pass/score/retention | Non-zero checker |
| Create/modify | `spikes/web/evidence/retained/**` | Sanitized raw/reproducibility artifacts | Retain through I5-05 |
| Create | `spikes/web/evidence/retention-index.json` | Source/lock/command/artifact hashes and cleanup state | Rollback/reproduction |
| Modify | `mk/issue-5/i5-02.mk` | Explicit winner/no-winner/check/cleanup targets only | Root Make unchanged |

## Related Code Files

- Create only the ADR/scorecard/retained-evidence/issue-local Make paths above.
- Read Gate C evidence indexes and all candidate sources/locks.
- Delete no candidate source before I5-05 and no shared/protected file ever.

## Dependency Map

```text
complete Gate C must-pass + score/no-winner rules
  -> scorecard JSON/Markdown
  -> ADR-005 Proposed winner OR Proposed no-winner
  -> losing-build exclusion + retained reproduction
  -> I5-03/I5-05 remain blocked until required approval/merge semantics
```

## Interface Checklist

- [ ] ADR and scorecard name the exact same outcome/digests/candidate dispositions.
- [ ] `Accepted` is never written by automation; human decision gate remains visible.
- [ ] No-winner has no hidden default/fallback framework.
- [ ] Winner entry contains exact candidate path, build/start/test commands, mode, and lock hash.
- [ ] Losing candidates are absent from default/product build selection but remain reproducible.
- [ ] Retention index can reproduce/verify source and evidence without protected/shared edits.

## Test Scenario Matrix

| Priority | Scenario | Expected result |
|---|---|---|
| Critical | ADR winner differs from scorecard/digests | Non-zero; no publication |
| Critical | Missing must-pass/manual/browser data | No-winner only |
| High | Loser wired into default/product build | Non-zero changed-path/build-selection check |
| High | Losing source removed before I5-05 | Non-zero retention check; restore from bundle |
| High | Root Make alias added | Non-zero ownership check |
| High | Rollback invoked | Remove selection/scores, retain preview/source/evidence, ADR Proposed no-winner |

## Implementation Steps

1. Write ADR/scorecard/retention mismatch and illegal-status tests.
2. Generate machine scorecard from verified Gate C evidence.
3. Author matching Proposed winner/no-winner ADR and human rationale.
4. Run retention/reproduction/rollback and final scope/security checks.

## Tests Before

Write scorecard/ADR/retention schema tests for mismatched outcomes, recursive/self SHA claims,
illegal `Accepted`, unsupported winner, numeric eliminated score, absent retention hashes, root
alias, and premature losing-source removal.

## Refactor

Generate the JSON from verified Gate C indexes, then author the human scorecard and ADR without
recomputing evidence by hand. Select no winner automatically when any decision precondition is
false. Do not implement portal integration or shared contract changes.

## Tests After

- Run scorecard/ADR/retention consistency, link, schema, redaction, credential, changed-path, and
  protected-hash checks.
- Reproduce the selected candidate or no-winner neutral preview from clean source using exact
  issue-local/direct commands.
- Exercise local prior-artifact rollback without cloud action or destructive shared cleanup.

## Regression Gate

Planned future commands:

```bash
make -f mk/issue-5/i5-02.mk web-spike-scorecard-check
make -f mk/issue-5/i5-02.mk web-retention-check
make -f mk/issue-5/i5-02.mk web-winner-reproduce
make -f mk/issue-5/i5-02.mk web-local-rollback-check
```

Each emits `fitness-result-v1` evidence and exits non-zero on inconsistent/missing/unsafe evidence,
illegal winner/score/status, cap breach, losing-build inclusion, premature deletion, failed
reproduction/rollback, or protected/shared path drift. In no-winner state,
`web-winner-reproduce` must refuse with non-zero and direct the caller to the retained neutral
preview; scorecard validation can still pass the explicit no-winner schema while leaving I5-05
blocked.

## Success Criteria

- [ ] ADR-005 is an evidence-backed Proposed winner or explicit Proposed no-winner.
- [ ] Human and machine artifacts are consistent and safely retained.
- [ ] Neutral preview/common tests survive every outcome.
- [ ] Losing builds are excluded without losing reproducibility.
- [ ] No root/shared/portal/runner/cloud/merge authority is implied.

## Risk, Security, and Rollback

The risk is turning a partial experiment into durable architecture authority. Rollback removes the
winner selection and numeric scores, restores ADR-005 to Proposed/no-winner, disables candidate
default execution, and keeps the neutral preview plus all source/lock/raw evidence. A later cleanup
may remove losing source only after I5-05 merge, explicit review, retained reproducible source
bundle/hash, and clean changed-path proof.

## Next Steps

After implementation, I5-03/I5-05 consume only the reviewed merged ADR/handoff; human pre-merge
approval remains mandatory. A future root alias is a shared/root-Make owner task, not issue #7
acceptance. The independent validation and readiness audit that authorize Phase 1 occur before
this phase and are not repeated as post-implementation work.
