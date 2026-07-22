---
phase: 6
title: "Stage B executable architecture lab and publication"
status: pending
priority: P1
dependencies: [5]
effort: "L after Stage B readiness"
---

# Phase 6: Stage B executable architecture lab and publication

## Context Links

- [Architecture and Curriculum Design](./architecture-and-curriculum-design.md)
- [Threat Model](./threat-model-and-security.md)
- [Verification and Evidence](./verification-evidence-and-protected-assets.md)

## Overview

Build and publish the one executable architecture lab through exact released Issue #8/#10 seams.
The lab covers F01→F04→J01/J04/J05 and is the only stage allowed to claim controlled failure,
hint, reset, deterministic verify, retained evidence, completion, and portal delivery.

At the current planner output this phase is hard-blocked and has no file or command authority.
Nothing in the post-review scaffold-first Stage A correction supplies an Issue #10 renderer,
journey, runtime completion path, or Stage B command/file authority.

## Requirements

- Functional: real released lifecycle; bounded architecture task; controlled boundary/resilience
  failure; hints; evidence-preserving reset; verifier; solution/reflection; portal publication.
- Non-functional: deterministic, Vietnamese-first, keyboard/static/no-JS equivalent per exact
  renderer contract; no duplicate state/contract/renderer truth.
- Security: structured inputs only, private execution boundary, tamper/retry/crash/cleanup tests,
  no cloud or arbitrary execution.

## Architecture

The lab teaches a promotion-evidence publication design under a slow/unavailable downstream
catalog/governance dependency. It asks the learner to trace outcome/concerns/requirements,
compare options, choose a bounded resilience/security design, record an ADR, and satisfy fitness
evidence. It does not implement a queue, broker, cache, pipeline, AWS resource, or portal module.

## Related Code Files

- Current Create/Modify/Delete: none (`[]`).
- Exact Stage B lab/content/solution/verifier-publication paths come from the Phase 5 amendment.
- Released #8/#10, portal, runner, architecture six, root Makefile, and cloud paths are read-only.

## Implementation Steps

1. Repeat Phase 5 exact-head preflight and confirm Phase 2/3/4 Stage A evidence remains valid.
2. Write Stage B runtime tests first against exact released #8/#10 interfaces: content discovery,
   Vietnamese/static render, prerequisite gate, controlled/environmental distinction, history/
   reload, hint ordering, reset idempotency, verifier/evidence/completion, solution/reflection
   bypass, unavailable state, cleanup.
3. Add crash/retry/tamper negatives at exact supported commit points: duplicate request, delayed
   result, process/browser interruption, stale evidence, changed content/verifier hash, reset
   conflict, evidence committed before completion reconciliation.
4. Register the lab through the exact released portal content seam without portal-source edits.
5. Provide a bounded starter with concern, FR/NFR, option, view, ADR, and fitness trace inputs.
6. Implement the controlled failure: a proposed pattern/boundary lacks a named failure/verifier or
   its retry design omits required deadline/idempotency/backpressure links. Return the exact
   released-compatible controlled failure and useful Vietnamese remediation.
7. Provide progressive hints that expose trace links without mutating the learner artifact,
   verifier result, evidence, or completion.
8. Use the released reset operation to restore exact starter state, preserve prior immutable
   evidence, and prove readiness before another run.
9. Verify deterministic requirements/trace/ADR/pattern/view/resilience/security assertions and
   retain exact evidence through the Issue #8 authority.
10. Require completion only after fresh committed verifier result plus valid immutable evidence.
    Solution presence, reflection, scroll, elapsed time, client storage, or imported evidence
    cannot complete.
11. Render/publish through exact #10; test keyboard/static/no-JS and bounded required browser
    contexts from the release, with no native GUI/manual broad automation matrix.
12. Run S3, protected-hash, dependency-hash, exact-diff, process-group resource, truthful
    nonignored/ignored-inclusive cleanup, and rollback gates inherited from the final Stage B
    amendment; do not infer Stage B bounds from a Stage A static result.

## Tests Before

- Component/contract tests for content discovery and released types.
- Prerequisite/controlled-versus-environmental/hint/reset/verify/evidence/completion negatives.
- Crash/retry/idempotency/reconciliation/tamper/history/unavailable/cleanup negatives.
- Portal/shared-contract/protected/root/cloud changed-path denials.

## Refactor

No dependency or portal refactor. Refactor only Issue #11-owned lab/content when tests protect
released IDs and lifecycle behavior.

## Tests After

- Full Vietnamese foundation path and junior decision path.
- Mid-level challenge/alternative path without verification bypass.
- Real controlled failure → hint → reset → fresh verify → evidence → completion.
- Exact evidence/content/verifier/dependency hashes and completion authority.
- Static/no-JS/keyboard/status/evidence presentation per released #10 test contract.
- Every Stage A static/render/trace/protected check rerun.

## Regression Gate

At exact Stage B authority:

```bash
make curriculum-check architecture-check architecture-render architecture-lab-e2e traceability-check
```

The amendment may add exact blast-radius commands from #8/#10 releases; it may not replace or
weaken the five required acceptance names.

## Success Criteria

- [ ] Real portal-published architecture lab consumes exact #8/#10 releases without duplicate truth.
- [ ] F01→F04→J01/J04/J05 trace is visible and verified.
- [ ] Controlled failure, hints, reset, fresh verify, evidence, and completion all pass.
- [ ] Reflection/solution/client/navigation cannot forge completion.
- [ ] Required accessibility/static/no-JS and failure/recovery/security cases pass.
- [ ] No portal/shared-contract/protected/root/cloud/AWS/Terraform drift.

## Risk Assessment

The lab can become a disguised code simulator or pattern quiz. Keep one bounded architecture
artifact and one real lifecycle; verify forces/failure/evidence and trade-offs, not class names.

## Security Considerations

No raw shell/SQL/path/environment/URL/cloud arguments. Browser has no private token. Evidence is
bounded/redacted and locally integrity-checked only.

## Next Steps

Proceed to Phase 7 for whole-stage evidence, rollback, review, and exact-head human gate.
