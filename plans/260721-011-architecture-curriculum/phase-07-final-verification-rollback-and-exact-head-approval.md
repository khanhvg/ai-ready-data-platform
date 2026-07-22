---
phase: 7
title: "Final verification rollback and exact-head approval"
status: pending
priority: P1
dependencies: [6]
effort: "M"
---

# Phase 7: Final verification rollback and exact-head approval

## Context Links

- [Requirements and Risk Traceability](./requirements-and-risk-traceability.md)
- [Verification, Evidence, and Protected Assets](./verification-evidence-and-protected-assets.md)
- [Threat Model](./threat-model-and-security.md)

## Overview

Run the exact full acceptance and blast-radius suite at the final future Stage B head, prove
evidence/cleanup/rollback/protected preservation, obtain independent implementation review and
human exact-head approval, then hand off for a separately authorized PR/merge workflow. This
phase does not itself create a PR or merge.

At the current planner output this phase is hard-blocked and has no file or command authority.
The corrected Stage A plan passed independent validation but still awaits readiness; this final
phase cannot treat plan validation as implementation review or approval.

## Requirements

- Functional: full required command set, dependency/contract/renderer/protected checks, evidence
  validation, cleanup/rollback, review/approval.
- Non-functional: exact tested tree and hashes; clean local/tracking/live equality; bounded and
  reproducible results; no weakened/skipped required gates.
- Security: all S3 negatives and scans; no credential/cloud/private path; no synthetic approval.

## Architecture

Final provenance separates:

```text
implementation input -> scaffoldCommitSha -> testsCommitSha/redTestedTreeSha
  -> firstSemanticCommitSha -> finalSemanticHeadSha/finalTestedTreeSha
  -> optional attestation commit -> external PR/merge SHA
```

A tracked file never recursively claims its own containing commit. Human approval names the exact
tested head and stage outside the evidence producer.

## Related Code Files

- Current Create/Modify/Delete: none (`[]`).
- Future final candidate paths are exactly the union of the separately authorized Stage A and
  Stage B closed allow-lists; no new path may first appear in this phase.

## Implementation Steps

1. Fetch fresh; verify required branch, exact Stage B readiness input ancestry, current #8/#10/
   Stage A releases, active leases, clean status, and local = tracking = fresh-live.
2. Run tests-before evidence audit: exact seven-path scaffold commit, direct-child five-path
   complete tests/fixture commit, valid controls parsed/reached through all four exact `I11-EP-*`
   public entrypoints at the tests tree, and every required named exact-code semantic RED failed
   before the first semantic commit for the intended reason.
3. Run the full practical acceptance line exactly, followed by every amendment-bound #8/#10,
   security, accessibility, lifecycle, renderer, compatibility, and rollback blast-radius command.
4. Run two isolated deterministic expansion renders and semantic mutation/overlap/freshness tests.
5. Validate every evidence bundle against the exact released #8 schema/canonicalization and the
   owner-authorized command-result compatibility mapping; verify the closed run index plus
   input/output/tested-tree/dependency/contract/fixture/tool/artifact/rollback hashes.
6. Compare Issue #6 protected sources/rows/renders/tool blobs and all dependency/portal/root
   deny-list paths to their exact baselines.
7. Scan exact candidate/staged/evidence metadata for secrets, credentials, private paths, unsafe
   SVG/HTML, cloud actions, runtime artifacts, and unbounded/binary content.
8. Rehearse cleanup and rollback from the exact candidate: remove only owned temporary/candidate
   state, retain evidence, restore protected/shared state, verify no descendants/foreign bytes,
   then reconstruct/retest only under exact authorized procedure.
9. Run formatting, exact staged allow-list, local link/ID/trace, dependency, zero-byte nonignored
   porcelain, and ignored-inclusive ownership checks. Exit 0 with output is not clean.
10. Obtain a fresh independent implementation review at exact tested head; resolve findings
    without weakening tests or expanding authority.
11. Re-run affected/full gates at any changed head.
12. Obtain repository-authorized human pre-merge approval naming the exact final 40-hex head.
13. Publish a handoff that authorizes no PR/merge/cloud action by itself. A separate git workflow
    may act only if explicitly requested and all state is still current. Record user-facing
    docs/release-note impact; any `README.md`, `docs/**`, or release-metadata edit remains a
    separate owner-authorized serialized change.

## Tests Before

- Audit existence/integrity/order of every Phase 2 and Stage B RED result.
- Fail forged/missing/stale evidence, wrong tested tree, wrong dependency, missing command,
  protected drift, false human approval, and incomplete rollback.

## Tests After

- Full required and blast-radius suite at exact final head.
- Evidence schema/hash/canonicalization and dependency release verification.
- Protected/deny-list/staged-path/secret/private-path/cloud-action/formatting/clean checks.
- Independent review and human exact-head approval.

## Regression Gate

```bash
make curriculum-check architecture-check architecture-render architecture-lab-e2e traceability-check
```

Plus exact dependency-owner commands from the Stage A/B amendments. Missing required tools or
commands fail; no native GUI/manual broad automation substitute.

## Success Criteria

- [ ] All five practical acceptance commands and exact blast-radius commands pass at one head.
- [ ] Deterministic render/text/semantic overlap/freshness and protected hashes pass.
- [ ] Complete S3/evidence/cleanup/rollback results validate with no Critical/High residual blocker.
- [ ] Candidate diff equals the exact authorized union; nonignored porcelain has zero records;
      every ignored byte is classified; local/tracking/live equal.
- [ ] Fresh independent implementation review passes at exact head.
- [ ] Repository-authorized human pre-merge approval names that exact 40-hex head.
- [ ] Docs/release impact is classified without expanding the exact Stage A/B union.
- [ ] No PR, merge, cloud/AWS/Terraform, destructive migration, or other worktree action occurred
  within this plan phase.

## Risk Assessment

Late evidence or review fixes can invalidate exact-head results. Any change requires rerunning the
affected and full required gates and obtaining approval for the new head. Do not chase approval by
rewriting evidence to include its own commit SHA.

## Security Considerations

Passing automation does not waive S3 or human gates. Rollback must preserve evidence and unrelated
state; broad destructive cleanup is forbidden.

## Next Steps

After all criteria, hand off to a separately authorized PR workflow. Otherwise report the exact
blocker and keep Issue #11 unmerged/open.
