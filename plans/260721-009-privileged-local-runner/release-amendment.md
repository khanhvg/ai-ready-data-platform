---
type: dependency-release-amendment
issue: 9
date: "2026-07-22"
inputSha: "5cea5ce248b49ff8741af1b1e65f8ac2eb64698f"
releasedStageASha: "fecf6bb8e5dfa7cc69f9766f72ac6f5b9301dad9"
dependencyBinding: PASS
ownership: PASS
cookScope: whole-plan
cloudAction: none
---

# Issue #9 Dependency-Release Amendment

## Purpose and Boundary

This is the bounded release overlay for the existing validated six-phase plan. It replaces only
the stale fact that Issue #8 Stage A was unreleased, binds the released read-only interfaces, and
resolves two Issue #9-owned admission policies. It does not copy or modify shared contract truth,
implement the runner, create runtime/data/config outside the plan directory, perform cloud action,
or invent a future Git or file SHA.

The historical validation and blocked-readiness reports retain their exact earlier inputs. This
amendment remains current authority only for the released Stage A identity and exact contract pins.
The later [local container platform amendment](./platform-amendment.md) supersedes every platform,
ownership, containment, TDD execution and readiness clause below where they differ.

## Released Identity and Evidence

| Fact | Exact value |
|---|---|
| Current integration / Stage A release | `fecf6bb8e5dfa7cc69f9766f72ac6f5b9301dad9` |
| Release tree | `27fc3667ef37892dad5c3fbfd76769f65a0760be` |
| PR #23 Stage A merge / release ancestor | `5c2244c2c860234d0df49cf0a42ad950c6495717` |
| PR #25 second parent / approved composition-fix head | `734cf637a20ae186597e23d96a194ed4e30220ea` |
| Release evidence | <https://github.com/khanhvg/ai-ready-data-platform/issues/8#issuecomment-5043195549> |
| Released verification | Stage A `56/56`; invalid `65/65`; operations `16`; final `4/4`; inherited `19/19 + 1/1 + 13/13` |
| Issue #7 composition fix | shipped in the same current integration SHA |

Fresh fetch and Git-object checks prove the live integration ref equals the release, the release's
ordered first parent is PR #23 merge, PR #23 is an ancestor, and the release tree is exact. All
release bytes were read and hashed from that Git object, never from this feature worktree or an
ignored artifact.

## Contract Binding

[Phase 2](./phase-02-bind-released-issue-8-stage-a-contract.md#exact-read-only-interface-pins)
is the exact path/version/SHA-256 lock for the release set, version overlay, base and command-owner
registries, activation schema/example, operation matrix, completion/state/progress, lab/lesson/
manifest, OpenAPI/profile/problem, evidence/fitness, canonicalization, Make input, released readers,
checker, and I5-03 Make fragment. Its 21-entry contract-set closure and registry pointer reproduce
without mismatch.

The version matrix has ten owned families with one current/readable identity each. The only
extension is `fitness-result-v2`: base current remains v1, v2 is additionally readable, and
`emissionFallback` is null. The command-owner registry reserves exactly `runner-test`,
`runner-security-test`, and `runner-race-test` for I5-04 / `mk/issue-5/i5-04.mk` / S3. The generic
activation schema and released verifier accept owner I5-04 with exact base/fragment/command/v2
binding. No shared write is needed.

Stage A publishes no generated-binding command, output list, output hash set, or generator path.
The binding procedure is therefore direct read-only JSON/schema/reader consumption. Any
`apps/lab-runner/src/lab_runner/generated/**` output is denied.

## Exact Runner-Owned Decisions

- Activation instance:
  `apps/lab-runner/config/command-owner-activation-i5-04-v1.json`. It contains the released base
  registry hash and the actual I5-04 fragment hash. The fragment, instance, and implementation
  hashes are recorded only after those bytes exist.
- Private request body ceiling: exactly `16384` bytes, enforced during input reading and before
  JSON parsing or audit/operation/workspace allocation. It is a stricter private IPC policy because
  released minimum-only integer fields do not define a finite serialized maximum.
- Private transport: owner-only UDS by default, or explicit random `127.0.0.1` fallback; exact
  runner Host, no Origin/cookie/browser path, launch-scoped bearer plus CSRF, and no permissive CORS.
  The future Issue #10 BFF—not this runner—maps the released public OpenAPI Host/Origin profile.

## Lease and Ownership

At `2026-07-22T08:05:02Z`, the latest Issue #8 Stage B handoff
<https://github.com/khanhvg/ai-ready-data-platform/issues/8#issuecomment-5043335319> records a
blocked plan-only attempt with `OUTPUT_SHA=none` and no amended paths. There is no actual write
overlap. The original conditional Airflow seam is superseded and denied. Under the platform
amendment, Issue #9 consumes released Stage A read-only and may write only:

- exact named paths under `apps/lab-runner/**`;
- `mk/issue-5/i5-04.mk` with only the three reserved runner targets.

Root Make, portal/framework, shared contracts, golden core, other Make fragments, cloud,
Terraform, Compose/profile/Airflow paths, and all other existing source/config/data paths are
denied. Issue #9-owned runner Dockerfile/context/lock/launcher paths are inside
`apps/lab-runner/**`; they are not shared Compose ownership. A later real overlapping write lease
is a STOP; read-only consumption alone is not.

## Readiness Effect

`COOK_SCOPE=whole-plan`. The dependency-safe staged subset is not selected because the released
contract supports the ordered plan without shared writes. The platform amendment replaces host
execution with one local PID-namespace container backend for all eight operations. Phase 3 retains
a test-only RED commit: long real cases run through the fixed no-argument shard harness; the three
public I5-04 Make targets verify fresh shard closure and emit bounded fitness-result-v2, while the
protected I5-01 data-contracts-check remains v1. Security, S3, evidence, rollback, independent
exact-head reviews, and human approval remain mandatory execution/release gates.
