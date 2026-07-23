# Phase 6 — Prove S3, Resources, Rollback and Handoff

## Objective

Close every contract, threat, supply-chain, containment, recovery, evidence, ownership and exact-head
gate before implementation review. No merge or future head is approved by this plan.

## Full Verification

First run the fixed no-argument shard harness from the clean exact implementation tree:

    python3.12 apps/lab-runner/tools/run-gate.py

It must execute every declared shard and close fresh exact-head/image/policy evidence. Then run the
four public verifiers:

    make runner-test
    make runner-security-test
    make runner-race-test
    make data-contracts-check

Every S3 catalog row must have no skipped required assertion. The three I5-04 verifiers emit
fitness-result-v2; protected I5-01 data-contracts-check remains fitness-result-v1. Both are
validated against their released registry versions and hash-referenced detailed artifacts.

## Required Closure

1. Recompute Stage A 38-pin and 21-member contract closures and the Issue #9 activation instance.
2. Run all eight exact real operations against the final actual image digest. Capture peak wall,
   CPU, worker/container memory, PIDs, workspace/tmpfs, files, FDs and output. Prove one active
   container and the explicit 16 GiB host reserves.
3. Repeat every adversarial container test: double-fork/reparent/setsid/daemon, fork bomb,
   TERM-to-KILL timeout, main crash, dbt tracker, network/DNS/metadata, read-only root/base,
   link/special files, env canary, output flood, cgroup enforcement and lifecycle residue.
4. Prove stopped/missing engine is RUNNER_ENGINE_UNAVAILABLE with no host fallback or state
   allocation. Prove ignored/unavailable containment is RUNNER_CONTAINMENT_UNAVAILABLE.
5. Close base/image/wheel hashes, SBOM, provenance, license obligations, Critical/High scans,
   deterministic context and actual OCI manifest/config digest. Runtime is pull-never and offline.
6. Kill at every durable boundary and verify idempotency, CAS, append-only audit, recovery, reset and
   exact eleven-asset old-or-new publication.
7. Rehearse rollback twice, including interrupted cleanup and stale identity. Confirm it touches
   only exact owner-recorded containers and marker-owned state.
8. Compare changed paths to the exact allow-list, protected hashes to the pre-cook baseline and
   Issue #13 paths to zero overlap. Root Make, Compose/profile, Airflow, contracts and golden source
   remain unchanged. Prove the app-owned ignore rule covers only .local-state, runtime artifacts
   are marker-owned, a neighboring unlisted path is not ignored, and the deterministic image
   context contains no ignored runtime byte.
9. Scan code/evidence/diff for secrets, private absolute paths, ambient credential/proxy/cloud
   access, raw output, placeholders and fabricated future digests.
10. Obtain two fresh independent strict implementation reviews on the same exact remote-equal
    head. Resolve every Critical/High and rerun affected gates. A changed head invalidates review.

## Image Release Admission

Only after all closure passes, write runner-image-release-v1 with the actual image manifest/config
digest, platform, build lock hash, SBOM/provenance/license/vulnerability evidence hashes, exact
eight-operation results and S3/rollback aggregate. Issue #13 consumes this released record and the
launcher; it may not substitute a tag or rebuild runner internals.

## Evidence Rules

- Evidence root is apps/lab-runner/.local-state/evidence/<run-id>/ under an owner marker.
- Each real test shard records a closed app-owned artifact. Each I5-04 public verifier checks a
  complete fresh shard set and emits a bounded fitness-result-v2 envelope within 120000 ms.
- The protected I5-01 data-contracts-check envelope remains fitness-result-v1; the aggregate index
  validates both versions and never relabels one as the other.
- Every referenced artifact has exact size and SHA-256; unknown/missing/duplicate entries fail.
- Process inventories demonstrate observation only. Effective Engine state and container
  lifecycle prove containment.
- Evidence never claims a commit/PR/image/release digest that was not observed.

## Handoff Gate

The implementation is reviewable only when the local, tracking and remote heads are equal; tracked
and ordinary untracked state is clean; the ignored-inclusive delta from the exact Phase 1 baseline
contains only marker-owned .local-state and bounded build/evidence roles while unrelated ignored
entries remain unchanged; all required gates and scans pass; operation feasibility is measured
8/8; no Critical/High remains; and Issue #13 overlap is zero. Separate human approval of that exact
head is still required before merge.

## Rollback

Disable runner admission, converge exact owned container identities to absent, restore the previous
verified release pointer, retain audit/evidence and remove only verified marker-owned transient
state. No Docker prune, engine state change, cloud action, source deletion or unrelated cleanup is
authorized.
