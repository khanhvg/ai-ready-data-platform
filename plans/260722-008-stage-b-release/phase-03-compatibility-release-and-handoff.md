---
phase: 3
title: "Compatibility, S3, release, and handoff"
status: pending
priority: P1
dependencies: [2]
stage: "B"
---

# Phase 3: Compatibility, S3, Release, and Handoff

## Context Links

- [Verification commands](./plan.md#verification-commands)
- [Resource and evidence contract](./plan.md#resource-and-evidence-contract)
- [Migration and rollback](./plan.md#migration-and-rollback)
- [Command/evidence matrix](./requirements-and-risk-traceability.md#command-and-evidence-matrix)

## Overview

Prove the additive binding against the complete Stage A/Issue #6/Issue #7 blast radius, rehearse
binding-only rollback, publish bounded S3/evidence results at one exact committed implementation
head, and stop for independent/human merge gates. This phase changes no product behavior.

## Requirements

- All focused, primary, blast-radius, offline, S3, resource, cleanup, rollback, changed-path, and
  protected-hash checks pass at the same exact clean committed head.
- The binding schema/document hashes and every pinned dependency hash appear in `fitness-result-v2`
  evidence; no output artifact embeds its containing commit recursively.
- Stage A set/registry/manifest, 65-fixture result, 16-operation matrix, final four I5-03 checks, and
  inherited Issue #6 19/19 + 1/1 + 13/13 results do not regress.
- The focused Issue #7 Node suite remains 5/5 without editing or installing its package.
- The final handoff publishes two immutable components: Stage A set byte hash
  `92aaf9a573f5d23b5bf5d8d7db1e68150d4b0944f0e6ab6e651b1a3d34408638` and the observed binding
  document hash. The latter is computed only after bytes stabilize.
- Stage B release SHA is recorded externally only after the remote merge is observed.
- The shared-contract lease stays active through release and is released only in the final external
  handoff.

## Exact Phase Write Allow-List

This phase may modify only the already-created/modified Stage B implementation paths listed in the
plan to fix defects found by required checks. It creates no new tracked path. Tests and binding
semantics may not be weakened to close a failure.

Generated evidence remains ignored and marker-owned under
`.artifacts/evidence/learning-contracts/<run-id>/`; it is not a tracked product path.

## Verification Order

1. Commit the exact testable implementation source head before final evidence.
2. Run focused contract checks:

```bash
python3 -m unittest tests.contracts.learning.test_vite_consumer_binding
node --test spikes/web/candidates/vite/tests/promotion-trust-contract.test.mjs
```

3. Run the primary contract as one Make invocation:

```bash
make learning-contracts-check api-contracts-check evidence-contracts-check
```

4. Run the blast radius:

```bash
make lesson-check LESSON=promotion-trust
make data-contracts-check migration-contracts-check
make help
git diff --check
```

5. Obtain the emitted locator and run:

```bash
make evidence-verify EVIDENCE="$EVIDENCE_LOCATOR"
```

6. Re-run the primary/focused checks with network unavailable and AWS/cloud variables absent,
   using only already-admitted local runtimes.
7. Run exact input/protected hashes, 21-entry contract-set validation, changed/open/import/subprocess
   inventories, no-generated-types/downstream-path checks, high-confidence secret/private-path/PII
   scans, dependency/lock/import checks, and resource ceilings.
8. Rehearse rollback in a disposable marker-owned copy: binding selection absent, Stage A still
   readable/green, binding v1 still readable, evidence retained, foreign sentinels unchanged.

Missing required runtime, evidence, hash, command, or result is `fail`, never optional.

## S3 and Browser Boundary Gates

- No binding or evidence may contain fixture records, record values, private paths, credentials,
  environment dumps, PII canaries, raw SQL/commands, URLs, template/expression code, auth policy,
  or learner evidence.
- Browser projection cannot validate/authorize/mutate/complete/emit. Mutation of any trust boolean
  away from `false` fails `BINDING_AUTHORITY_FORBIDDEN`.
- Dependency paths are exact regular single-link files with verified sizes/hashes; traversal,
  remote ref, symlink/hardlink/special-file, or substitution fails before parsing/use.
- No AWS, Terraform, cloud SDK, Docker, browser, server, npm install, network fetch, destructive
  migration, or broad cleanup command appears in the Stage B command graph.
- Bounded stdout/stderr is sanitized before retention. Any high-confidence secret/private-path hit
  quarantines the evidence and fails release.

## Release and Review Steps

1. Record exact command/result/tool/resource/protected/hash/rollback outputs for the committed head.
2. Compute the binding schema/document hashes after stabilization; run the full verification again
   if either byte changes.
3. Obtain at least one fresh independent exact-head read-only implementation review. The reviewer
   verifies requirement coverage, mapping totality/bijection, trust boundary, changed paths, tests,
   evidence, S3, resource, and rollback results.
4. Run repository-required checks at the same head.
5. Obtain a separate repository-authorized human approval for that exact head before merge.
6. After authorized merge, fresh-fetch and observe the remote merge/release SHA and exact ancestry.
7. Publish the two-component handoff, input/output/tested/reviewed/approved/merge identities,
   commands/results, consumer procedure, rollback result, residual risks, and lease release.
8. Move Issue #8 to closure review or close only under current repository policy; do not infer
   authority from this plan.

## Success Criteria

- [ ] Focused Python and Issue #7 Node suites pass at exact protected hashes.
- [ ] Stage A public results and inherited Issue #6 results remain exact.
- [ ] All S3, offline, resource, changed-path, protected-hash, cleanup, and rollback gates pass.
- [ ] Evidence binds exact Stage A and binding components without secrets/private paths or recursive
  identity.
- [ ] Independent exact-head review, repository checks, and human exact-head approval all match.
- [ ] Remote release SHA and binding hash are observed and published externally.
- [ ] Shared-contract lease is released only after the final handoff.

## Rollback

Rollback disables consumer selection of the binding; it does not delete the released binding,
schema, reader, or evidence. Stage A remains the readable base, while downstream portal cook
stops rather than inventing an alias. Runtime cleanup uses the existing marker/nonce/device/inode
protocol and refuses unowned/foreign/symlink/hardlink/special-file paths before deletion.

## Next Steps

After the final release/handoff, Issue #9 may repin the shared release without consuming the Vite
binding, while Issue #10 consumes the Stage A set plus binding read-only under its own fresh
amendment, validation, readiness, implementation-review, and human gates.
