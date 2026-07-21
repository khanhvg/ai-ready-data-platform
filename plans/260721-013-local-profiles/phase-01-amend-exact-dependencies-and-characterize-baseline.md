---
phase: 1
title: "Amend Exact Dependencies and Characterize Baseline"
status: pending
priority: P1
dependencies: []
effort: "M"
---

# Phase 1: Amend Exact Dependencies and Characterize Baseline

## Overview

Create the exact implementation authority only after the dependency releases exist, then freeze
current Docker-free/profile/Compose/protected behavior before writing new behavior. This phase is
blocked today; it must not be satisfied with plan-branch or placeholder SHAs.

## Context Links

- [Inventory](./inventory.md)
- [Requirements and traceability](./requirements-and-traceability.md)
- `plans/260721-005-enterprise-learning-sandbox/phase-08-local-compose-profiles-and-resource-measurement.md`
- `plans/260721-005-enterprise-learning-sandbox/implementation-issue-graph.md`
- GitHub Issues #10, #12, and #13

## Requirements

- Functional: record exact passing merged Issue #10 journey and released/admitted Issue #12 labs,
  plus actual portal/runner images, commands, completion/evidence contract and service allowlist.
- Functional: select a clean future implementation input descending from both dependencies and
  record exact Stage A writable/protected paths.
- Functional: characterize current Docker-free command closure, profile namespaces, Compose
  render/dependency closure, limits/gaps, ports, volumes, health/deadlines and existing lifecycle.
- Non-functional: never infer a SHA from a plan branch; never modify another worktree; never start,
  build or pull a container in this phase.
- Non-functional: independently revalidate the amended plan and run a fresh readiness audit before
  implementation. This planner session does neither.

## Architecture

The future `dependency-amendment.md` is an immutable gate ledger, not implementation config. It
maps released authority to the exact input and hashes. Any empty/mismatched field stops Stage A.
Characterization then produces tests against the amended tree so dependency changes are not
mistaken for the current `24be3b3` inventory.

Required amendment fields:

```text
issue10PassingMergeSha
issue10JourneyCommandAuthoritySha
issue12ReleaseSha
issue12AdmittedLabManifestSha
portalImageIndexAndPlatformDigest
runnerImageIndexAndPlatformDigest
profileServiceAllowlistSha
commandAuthoritySha
completionEvidenceAuthoritySha
implementationInputSha
protectedManifestSha256
```

## Related Code Files

- Create as a plan gate: `plans/260721-013-local-profiles/dependency-amendment.md`
- Read: `README.md`, `Makefile`, `docker-compose.yml`, `.env.example`
- Read: actual released dependency contracts/images/labs at their future exact merge/release SHAs
- Read: `data-generator/generate.py`, `data-generator/schema.md`, Docker-free/golden tests
- Read/protect: root/shared/golden/architecture/portal/runner/lab/migration/release paths
- Modify product/config: none in this phase

## Tests Before

- Add/freeze `LP-CHAR-CORE-001` through `LP-CHAR-SCALE-005` before any behavior change.
- Prove current protected presence/absence and hashes at the amended input.
- Prove Docker-free commands contain no Docker/cloud/privilege closure.
- Canonically render actual Compose without contacting/starting the engine and enumerate every
  service, profile, dependency, port, volume, healthcheck and configured limit.

## Refactor

None. This is an authority and characterization phase.

## Tests After

- Re-run characterization twice from the same clean tree/config and require identical normalized
  inventories/hashes.
- Reject stale dependency, image, lab, command, completion/evidence or allowlist authority.
- Reject a dirty input, protected mismatch, absent required dependency or newly required
  out-of-allowlist path.

## Regression Gate

Static/plan gate only: exact SHA/ancestry, dependency state, link, protected hash, placeholder and
Docker-free command-closure checks. No container or heavy acceptance command.

## Implementation Steps

1. Wait for Issue #10 to be passing and remotely merged; record the public merge SHA and exact
   Docker-free real journey command authority.
2. Wait for Issue #12 to publish a released/admitted lab manifest; record release and manifest
   SHA, completion authority and exact allowed workloads.
3. Inventory actual released portal/runner services and immutable image authorities. Do not carry
   names from an unmerged plan.
4. Select a clean implementation input descending from both dependency SHAs. Record ancestry and
   remote observation.
5. Re-inventory the entire current Compose/runtime and recompute the protected manifest.
6. Resolve any new service/group against the owner aggregate. Unknown/unbudgeted groups remain
   denied; amendment requires owner decision.
7. Record exact commands, writable allowlist and evidence/command/completion authorities.
8. Commit/push the amendment alone, then hand it to a fresh independent validator and readiness
   auditor. Stop on any BLOCK/FAIL.

## Success Criteria

- [ ] All required dependency/authority fields contain exact verified SHAs/digests; none is empty.
- [ ] Implementation input is clean, remotely observed and descends from both dependencies.
- [ ] Actual service/image/lab/command inventory contains no invented item.
- [ ] Current Docker-free/profile/Compose behavior and protected hashes are characterized first.
- [ ] Exact writable/protected boundaries are accepted without shared-owner conflict.
- [ ] Independent plan revalidation and fresh readiness audit pass at the amendment SHA.

## Risk Assessment

Largest risk is treating a dependency plan as a released contract. Enforce remote merge/release
identity and exact manifests. If dependencies change topology/contracts, revise this plan visibly;
do not stretch the current allowlist or preserve stale budget math.

## Security Considerations

Do not fetch/run dependency images or expose credentials during inventory. Redact private paths.
Hash public-safe metadata only. A shared-contract update requires its serialized owner; I5-08
cannot self-grant it.

## Next Steps

Only after every success criterion: begin Phase 2 RED tests. Otherwise remain implementation
blocked while Docker-free core stays usable.
