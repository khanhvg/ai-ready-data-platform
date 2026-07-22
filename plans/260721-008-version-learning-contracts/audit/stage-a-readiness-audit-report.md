---
title: "Issue #8 Stage A Staged Readiness Audit"
date: "2026-07-22"
issue: 8
inputSha: "6e488a410081f12726375ca7aa2f27f62c0105cc"
verdict: "STAGE_A_READY_WITH_GATES"
boundary: "STAGE_A_READINESS_PASS_NOT_IMPLEMENTATION"
stageA: "ready-to-cook"
stageB: "blocked-on-issue-7-merged-sha"
implementationInput: "externally-published-containing-commit"
---

# Issue #8 Stage A Staged Readiness Audit

## Verdict

`STAGE_A_READY_WITH_GATES` for one serialized Stage A TDD cook covering Phases 1-5 and exactly the
121 tracked paths in the plan allow-list. Stage A is framework-neutral, independently releasable in
one coherent contract set, and has zero shipped-file writes. The containing audit commit is the
only implementation input and is recorded externally after publication so this report does not
claim its own commit recursively.

This verdict authorizes implementation only. It does not authorize a pull request, merge, contract
release, Issue #8 closure, downstream cook, cloud action or synthetic approval. Fresh independent
review of the exact implemented head and separate human exact-head pre-merge approval remain
mandatory.

Stage B remains `blocked-on-issue-7-merged-sha`, `cookable: false`, with zero current paths,
commands, tools, adapters, dependency reads or future SHA authority. It requires the exact merged
Issue #7 Vite handoff, a concrete plan amendment, independent revalidation and fresh readiness.

## Scope and Independence

- Worktree: `/Users/khanhvg/Documents/work/ai-ready-data-platform-issue-8-contracts` only.
- Branch: `plan/issue-8-version-learning-contracts` only.
- Audit input: `6e488a410081f12726375ca7aa2f27f62c0105cc`.
- Workflow: isolated staged-readiness/plan-to-cook equivalent; no red-team activity.
- Permitted writes: Issue #8 plan wording and this audit artifact only.
- Excluded: Stage A behavior, RED/GREEN execution, code/config/contracts, PR, merge, future Issue #7
  SHA consumption, other worktree mutation and `.github/**` expansion.
- Requested runtime profile: Codex `gpt-5.6-sol`, reasoning effort `xhigh`; recorded as supplied
  session context, not an independently signed model attestation.

The audit read Issue #9 planning content through Git objects at
`4cea857fd4a79dca966f4c6b8d4350b4e5d372a2` only to verify downstream contract consumption. It did
not enter or modify the Issue #9 worktree.

## Exact Authority and Lease Baseline

| Check | Result |
|---|---|
| Initial local HEAD | `6e488a410081f12726375ca7aa2f27f62c0105cc` |
| Initial tracking ref | `6e488a410081f12726375ca7aa2f27f62c0105cc` |
| Fresh live plan branch | `6e488a410081f12726375ca7aa2f27f62c0105cc` |
| Shipped integration authority | `24be3b34c6b0fcdbd07c5800dcab349054e34713`; fresh live and ancestor of input |
| Worktree/branch | exact requested path and `plan/issue-8-version-learning-contracts` |
| Initial tracked tree | clean |
| Issue #8 | OPEN; exactly `ready for plan audit`, `risk:high`, `tdd`, `security:S3`, `shared-core`, `api` |
| Validation authority | comment `5036827527`; `PASS_WITH_FIXES`, 10 fixed, 0 unresolved |
| Parallelization authority | issue #5 comment `5036142770`; permits dependency-independent Stage A only and one shared writer |
| Shared-core conflict scan | Issue #8 is the sole OPEN issue carrying `shared-core` |
| Open PR scan | zero open PRs |
| Implementation branch | `feature/issue-5-03-learning-contracts` absent locally and remotely |
| Branch/worktree writer scan | no local or remote branch beyond shipped integration changes any Stage A shared-contract prefix; no I5-03 implementation worktree exists |
| Issue #7 | OPEN/unmerged; no merged Vite handoff SHA |
| Issue #9 | OPEN; must consume an externally released Stage A SHA read-only |

The readiness publication grants the time-bounded shared-core lease only to the future
`feature/issue-5-03-learning-contracts` branch created from the audit output. The unchanged branch
must be pushed and freshly proven local = tracking = live before the first tracked write. One actor
owns the entire Phase 1-5 cook; no phase fan-out or second shared writer is allowed.

## Findings and Plan-Only Corrections

| ID | Severity | Readiness defect at input | Correction | Status |
|---|---:|---|---|---|
| R-01 | Critical | `fitness-result-v2` fixed `owner=I5-03`, omitted fields promised by the evidence section, and offered no reusable command-activation seam. Issue #9 would have needed another shared-contract edit or local fork. | V2 now binds owner/command/evidence version to an exact hash-bound activation row; its closed fields include invocation, input/dependency/schema/contract/fixture hashes, redaction, retention and rollback. A generic activation schema plus the I5-03 instance lets later reserved owners add only issue-owned instances. | Fixed |
| R-02 | High | “Bounded” execution had no numeric command/output/disk/RSS ceilings and the exact runtime was absent from the ambient interpreter. | Added a fail-closed pre-cook golden-runtime gate and explicit 30/60/120/300/600-second, 2/16 MiB output, 256 MiB run-state and 2 GiB RSS ceilings. | Fixed |
| R-03 | High | `I8-IDEMPOTENCY-DUPLICATE-123` used a descriptive assertion instead of an exact failure oracle. | Froze `IDEMPOTENCY_DUPLICATE_EFFECT` while retaining one-result/one-effect semantics. | Fixed |
| R-04 | High | Phase 5 still stopped for another readiness decision, obscuring the requested one-coherent-release cook handoff. | Current readiness now authorizes one serialized cook; Phase 5 stops only for independent exact-head implementation review and human pre-merge approval. | Fixed |

Four readiness defects were fixed in plan text; zero readiness blockers remain. No product contract,
schema, source, test, fixture, Make/config or workflow file was created or changed by this audit.

## Stage A Ownership and 121-Path Proof

The allow-list parser expanded the exact Markdown table and RED matrix into 121 unique paths:

| Category | Count | Disposition |
|---|---:|---|
| Invalid tracked fixtures | 65 | Create in Phase 1 before behavior |
| Valid/index fixtures | 6 | Create in Phase 1 or their named phase |
| Test modules | 14 | Create in Phase 1; later phases modify only these new files |
| Python implementation modules | 13 | Create after RED |
| Learning contract/content paths | 19 | Create after RED |
| OpenAPI paths | 3 | Create after RED |
| Make fragment | 1 | Create after RED |
| **Total** | **121** | **One coherent Stage A release** |

Results:

- 121/121 are relative, normalized, unique and absent at the audit input.
- 121/121 are Issue #8-owned exact paths; there are no directory-wide write globs.
- The union of Phase 1-5 `Create`/`Modify` table paths is exactly all 56 non-invalid-fixture
  allow-list paths; zero phase path falls outside the master list. The 65 remaining paths are the
  exact indexed invalid fixtures linked from Phase 1.
- Zero paths target `Makefile`, `.github/**`, `requirements/**`, `scripts/golden/**`, existing
  `tests/contracts/**`, `tests/golden/**`, shipped promotion fixtures, Issue #7/Vite/React/ADR,
  portal, runner, data-platform, Docker, cloud, AWS or Terraform surfaces.
- Zero Stage A modification rows target shipped files. Later “Modify” rows refer only to files first
  created earlier within this same Stage A cook.
- Runtime evidence is generated only below marker-owned `.artifacts/{workspaces,evidence}/learning-
  contracts/<run-id>/`, is never staged, and is not part of the 121 tracked paths.
- The 71 fixture/index files make 58.7% of the tracked scope. The high path count is deliberate
  negative-contract coverage, not uncontrolled production surface.

The full immutable allow-list is the
[`Exact Stage A Implementation Allow-List`](../requirements-and-risk-traceability.md#exact-stage-a-implementation-allow-list).
Any unlisted tracked path is a hard STOP.

## Shipped Issue #6 Immutability and Blast Radius

The diff from shipped authority
`24be3b34c6b0fcdbd07c5800dcab349054e34713` to the audit input contains only the nine Issue #8
plan/validation files. The protected Issue #6 tree selection contains 82 Git entries at each SHA;
both produce tree-manifest SHA-256
`875cdab7eefd7fd0e67e7be98a4bc3f170ab8a4aafe4268c70eb505665ee5ce0`.

Exact protected anchors:

| Path | SHA-256 |
|---|---|
| `Makefile` | `12926b16a797fded79b0b11b00147887258721f145c79e66472f44c5f0228458` |
| `mk/issue-5/i5-01.mk` | `d38dfb497161aa20761de7fcef7ae0fb09015adfdee885331ee1fba9403f9028` |
| `learning/contracts/schema-version-registry.json` | `8e18588f63b5d99c0b60a229758575e8badf0f055bfcb4f89908f9fa2684a57e` |
| `learning/contracts/command-owner-registry-v1.json` | `a94ac86bda0b70643edef9f144a59d8753d91f963b83d22cd510adbc31970e80` |
| `requirements/golden-py312-macos-arm64.lock` | `f41c727b39f99106f95b7937b2811e8d27db89d1d5106e9f1d9effd4403143d2` |
| promotion evidence fixture | `2f4d90228fa2ea8859a8db630ff587b6cebdc10a0bf6b7db25e46c3dc27181d5` |
| promotion fixture manifest | `0a1dcd4023648f52009bfd4dc5d529c00ce66f42cd0e725732b972b0b78df341` |

One shipped `make golden-clean PROFILE=small SEED=42` run passed in 17.408 seconds and established
the exact locked runtime. Existing Issue #6 suites then passed as one serial invocation:

- `data-contracts-check`: 19 tests passed;
- `evidence-contracts-check`: 13 tests passed;
- `migration-contracts-check`: 1 test passed;
- total: 33 passed, 0 failed.

`make help` passed, reported all four I5-03 names as reserved `future-owner`, and emitted valid
I5-01 evidence. Audit-created untracked Issue #6 run state is removed before final publication; no
shipped byte is written.

## Tool, Package and API Feasibility

| Capability | Verified result | Stage A rule |
|---|---|---|
| Host | Darwin arm64; `17179869184` bytes physical memory | exact supported 16 GiB lane |
| Python | CPython 3.12.3 | exact golden policy `>=3.12,<3.13`; patch recorded |
| Node/npm | Node `v22.22.3`, npm `10.9.8` present | not imported or executed by Stage A |
| Make | GNU Make 3.81; root wildcard at `Makefile:120-121` | new `mk/issue-5/i5-03.mk` auto-included; no root edit |
| `jsonschema` | 4.26.0; `Draft202012Validator` present | Draft 2020-12 schema/meta-schema validation |
| `rfc8785` | 0.1.4; `dumps(obj) -> bytes` present | existing JCS wrapper/cross-reader profile |
| PyYAML | 6.0.3; `SafeLoader` and `load_all` present | OpenAPI-only constrained single-document loader |
| Dependency health | exact golden runtime `pip check`: pass | no new distribution/import/lock/manifest |

The ambient `/usr/local/bin/python3.12` lacks exact `rfc8785` and has older `jsonschema`/PyYAML,
so ambient imports are explicitly inadmissible. Before RED, the implementation worktree must have a
manifest-admitted golden runtime matching lock SHA-256 `f41c727b...` and freeze SHA-256
`cdb87ed...`. If absent, only the shipped I5-01 `golden-clean` target may establish it as a pre-cook
dependency step. Stage A checks then run post-install with network and cloud credentials absent.

All proposed Issue #6 imports exist with the named public symbols:

- `canonical`: `CanonicalizationError`, `parse_json`, `dumps`;
- `dependency_lock`: `LockError`, `platform_preflight`, `verify_lock`;
- `runtime`: `RuntimeErrorTyped`, `require_platform`, `clean_env`, `run`;
- `source_state`: `SourceStateError`, `identity`, `assert_unchanged`;
- `workspace`: `WorkspaceError`, `OwnedWorkspace`, `validate_relative_path`, `allocate_family`,
  `atomic_write`.

No proposed API is invented. JSON Schema Draft 2020-12 is verified against the official
<https://json-schema.org/draft/2020-12> authority. OpenAPI 3.2.0 and its 2025-09-19 publication are
verified against <https://spec.openapis.org/oas/v3.2.0.html>. The plan truthfully implements a
closed project profile for the used OpenAPI subset plus semantic/reference/example/matrix checks;
it does not claim a universal OpenAPI validator. The locked YAML strategy rejects duplicate keys,
aliases/anchors/merges, tags, multiple documents, non-JSON scalars, BOM/trailing content and unsafe
numbers before profile validation.

Dependency disposition is exact: Stage A adds zero distributions and zero admitted third-party
imports. It inherits the shipped Issue #6 graph without claiming that an offline check proves the
graph vulnerability-free. Any lock/freeze/import change or new advisory requires review and stops
this cook; no scanner, fetch, automated update or waiver is invented.

## Deterministic Serialized Cook

The implementation sequence is fixed:

1. Create/push the unchanged `feature/issue-5-03-learning-contracts` branch from the exact audit
   output; prove local = tracking = fresh live, required ancestry, clean tree and sole lease.
2. Verify or establish the exact generated golden runtime before tracked RED writes.
3. Phase 1 only: create all 14 test modules, fixture index, 6 valid/index fixtures and all 65 invalid
   fixtures; run shipped characterizers, then capture the intended 76 RED failures.
4. Phase 2: schemas, strict parsing, registry composition, canonicalization and references.
5. Phase 3: operation matrix, state/CAS/idempotency, completion/reconciliation, probes and hints.
6. Phase 4: OpenAPI, learner/fitness evidence and promotion-trust documents.
7. Phase 5: activation/release set, Make fragment, exact public/blast checks, offline rerun,
   dependency-absence/decoy proof and rollback rehearsal.
8. Stop for independent exact-head implementation review and human exact-head pre-merge approval.

Numeric ceilings are contractual: focused subprocesses 60 seconds, 2 MiB per output stream and
16 MiB retained aggregate; public targets 30/60/120 seconds as named in traceability; primary
invocation 300 seconds; full ordered gate/rollback 600 seconds; 256 MiB run state; 2 GiB peak RSS.
No parallel Make flag or internal shared-core writer is permitted. A ceiling breach is failure.

## TDD RED Readiness

The stable matrix has 76 rows and 76 unique IDs. It references 65 unique tracked invalid fixtures
plus 13 generated-private rows. Every row now has an exact typed failure oracle; syntax/import/
fixture-index noise cannot satisfy RED. Phase 1 creates the complete negative corpus before any
schema, validator, OpenAPI, Make, registry instance or production module.

Coverage includes:

- exact head, lease, protected bytes and base-registry fixture pin;
- absent Issue #7/framework/portal/runner reads and inert-decoy invariance;
- closed schemas, duplicate names, non-I-JSON numbers, surrogates, unsafe integers, invalid UTF-8,
  BOM and trailing documents;
- missing/cyclic/traversal/remote/hash-invalid references;
- illegal/stale state, equal/unequal idempotency, duplicate effects and CAS conflicts;
- forged/dual completion, orphan attach/quarantine and reconciliation tamper;
- payload/artifact/verifier/fixture tamper, replay, recursive identity and descriptor-bound locators;
- unknown/lossy/cyclic/colliding migrations and retained old readers;
- operation uniqueness/taxonomy/neutral roles/authorization/evidence;
- OpenAPI matrix/auth/idempotency/raw-query/ref/version/request/response/error/YAML and no-channel;
- probe mutation/required/optional behavior, hint ordering/reveal/no-completion;
- promotion grains/limitations/hashes;
- fitness v1 mismatch, v2 owner/command activation mismatch, dependency drift, command activation
  and rollback scope.

Expected RED is executable rather than tautological: each new behavior assertion must fail because
the named behavior file/contract is absent while all shipped characterizers and fixture-index/
import/syntax preconditions pass.

## Contract and API Semantics

- Lesson, lab, progress, learner evidence, completion/reconciliation, operation matrix, promotion
  manifest, fitness v2, registries and release set are closed and bounded at every object boundary.
- One mutable authority, `learning-progress-authority-v1`, performs the CAS completion transaction.
  Browser state, operation journals and evidence presence are projections/inputs, never completion
  truth.
- Same key and same canonical request returns the stored result with one effect. Changed payload is
  `409 IDEMPOTENCY_KEY_REUSE`; stale revision is `412 PROGRESS_VERSION_CONFLICT`. Reconciliation has
  exactly `already-attached`, `attachable-orphan` and `invalid-or-conflicting-orphan` dispositions.
- Required probes are non-mutating and block honestly; optional unavailability cannot pass. Hints
  and reflection are ordered evidence events and cannot complete.
- The operation inventory contains 16 unique operation IDs and 16 unique method/path pairs across
  Experience, Process, System, Backend and Technical taxonomy, with five mutations. Every row has
  abstract process role, authn/authz/CSRF, idempotency, request/response/error/version and evidence
  metadata.
- OpenAPI freezes `/v1`, exact content/version headers, five closed mutation request bodies, closed
  response envelopes, exact common and operation-specific errors and bounded `202` + GET polling.
  `channels` is exactly empty and no AsyncAPI path exists.
- Promotion trust retains four independent grains and only
  `insufficient-evidence/no-common-grain`; no causal join is invented.
- The generic activation schema plus release set lets Issue #9 pin and consume Stage A JSON
  contracts directly. An I5-04-owned activation instance can select v2 for already reserved rows;
  no shared edit, copied schema or guessed adapter is required.

## Make, Release and Rollback Authority

Root `Makefile` already includes sorted `mk/issue-5/*.mk`. The current Make database contains one
owner each for shipped `data-contracts-check`, `evidence-contracts-check` and
`migration-contracts-check`; all I5-03 names are reserved once in the immutable command registry
and have no recipe at the input. Stage A adds only `mk/issue-5/i5-03.mk`; it neither edits root Make
nor duplicates I5-01 `evidence-contracts-check`.

The required primary gate remains exactly:

```bash
make learning-contracts-check api-contracts-check evidence-contracts-check
```

Then, serially:

```bash
make lesson-check LESSON=promotion-trust
make data-contracts-check migration-contracts-check
make help
git diff --check
```

The emitted learning-contract evidence locator is then verified with `make evidence-verify`; the
primary command is rerun post-install with network and cloud credentials absent.

The version overlay is bound to the shipped registry hash and adds v2 readability without changing
the base current/reader. The I5-03 activation binds its four exact rows and v2 emission; it never
falls back to owner-invalid v1. `learning-contract-set-v1.json` hashes sorted release inputs without
its own bytes or containing commit. Tested/reviewed/human/merge SHAs remain external attestations.

Rollback disables I5-03 activation but retains released v1/v2 schemas/readers/evidence. Runtime
cleanup enumerates only a marker/inode/nonce-bound Issue #8 manifest, refuses traversal, symlink,
hardlink, special/foreign entries, and removes only listed mutable bytes. Evidence, foreign
sentinels, unrelated state and every Issue #6 file remain intact. Broad glob/delete, reset, down
migration, evidence rewrite and last-write rollback are forbidden.

## S3 Disposition

The Stage A S3 contract covers traversal, symlink/hardlink/special-file and reference substitution;
duplicate JSON and YAML keys; UTF-8/I-JSON/JCS ambiguity; tamper/replay/recursive identity;
authorization/CSRF/idempotency and raw SQL/command/path/URL/template injection; absolute/private
paths; credential/private-key/PII canaries; dependency/lock/import drift; evidence redaction,
retention, descriptor-bound open and hash/size verification; and marker-bound rollback.

Evidence readers retain directory descriptors, use no-follow component opens, require regular
single-link files, recheck device/inode, bound bytes and verify declared size/SHA-256. Sensitive
canaries are generated only in private test roots and must be absent from retained output. Local
SHA-256 claims corruption detection only, not same-host authenticity or non-repudiation.

There is no Docker, browser, service, cloud SDK, AWS, S3 bucket, Terraform, network destination or
destructive migration in the Stage A command graph. Here `security:S3` is the repository security
classification; it grants no Amazon S3 or cloud authority.

## CI, Review and Final Gates

The repository has zero `.github/**` files at the audit input. CI absence is therefore an external
pre-merge concern, not a local cook blocker and not authority to add workflow files. Stage A must
pass all local commands and exact-head evidence first. Before any PR merge:

1. one fresh independent read-only implementation review must pass at the exact committed head;
2. repository-required checks, if any, must pass at that same head;
3. a repository-authorized human must approve that exact head;
4. any head change invalidates review and approval;
5. the remotely observed Stage A merge/release SHA is recorded externally.

Issue #8 stays incomplete after Stage A release. Stage B and downstream cooks remain separately
gated.

## Verification Record

| Verification | Result |
|---|---|
| fresh local/tracking/live equality at input | pass |
| Issue #6 ancestry and fresh integration identity | pass |
| label/state/comment authority | pass |
| no open PR and sole OPEN shared-core issue | pass |
| protected 82-entry tree manifest equality | pass |
| shipped `golden-clean` | pass; 17.408 seconds |
| existing Issue #6 contract tests | pass; 33/33 |
| exact locked imports and `pip check` | pass |
| proposed public Issue #6 symbols | all present |
| path inventory | 121 unique, 121 absent, 0 protected/cross-owner |
| RED inventory | 76 unique IDs, 65 unique tracked invalid fixtures, exact oracles |
| operation inventory | 16 unique IDs/pairs, 5 mutations |
| local Markdown links | pass |
| strict plan validation | pass; 6 phases, 0 issues |
| Stage A/Stage B/static/unresolved-marker scan | pass |
| AsyncAPI file inventory | 0 |
| Stage B 40-hex future identities | 0 |
| Stage B authorized paths/commands | 0 |
| `git diff --check` | pass |

## Cook Gates and STOP Conditions

Stage A cook starts only when the future implementation branch equals the externally published
audit output locally, in tracking and on the fresh live remote; the worktree is clean; Issue #8 is
OPEN with `ready to cook`; the sole lease remains uncontested; and the exact golden runtime is
verified. Any mismatch stops before write.

Stop on an unlisted path, Issue #7/framework/portal/runner read, protected drift, missing/changed
package or public API, failed intended RED oracle, command/resource ceiling, non-closed schema,
operation/API mismatch, second completion authority, unsafe evidence locator, sensitive retained
content, unreviewed advisory/dependency delta, non-idempotent rollback, required check failure or
attempted Stage B/cloud/PR/merge action.

`STAGE_A_READINESS_PASS_NOT_IMPLEMENTATION`
