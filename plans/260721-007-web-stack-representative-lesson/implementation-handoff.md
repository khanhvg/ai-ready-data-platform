# Implementation Handoff

## Boundary

This handoff becomes executable only after issue #7's independent plan validation and fresh
readiness audit authorize cook from one exact full `IMPLEMENTATION_INPUT_SHA`. Before any write,
local HEAD, tracking, and freshly fetched live remote must all equal that SHA; the SHA must contain
planner output `0890c4abab46f81d110be6cbd6de3560e631a735` and the recorded validation/audit ancestry.
It does not itself authorize implementation. Use the current worktree/branch assigned by that
later phase; stop on a different repository, branch, dirty protected/shared path, upstream drift,
missing dependency merge, or conflicting lease.

## Exact Allowed Paths

Future implementation may create/modify only:

```text
spikes/web/**
docs/decisions/0005-web-stack.md
docs/decisions/evidence/adr-0005-web-stack-scorecard.md
docs/decisions/evidence/adr-0005-web-stack-scorecard.json
mk/issue-5/i5-02.mk
plans/260721-007-web-stack-representative-lesson/**
```

Within the plan package, `discovery/**` is immutable. Plan status/checklist sync is allowed only
after actual work/evidence. No other path is implicit.

Forbidden examples:

```text
Makefile
.gitignore
release-manifest.json
docs/code-standards.md
contracts/**
schemas/**
tests/fixtures/learning/**
apps/learning-portal/**
apps/lab-runner/**
existing data/dbt/Rill/Airflow/Iceberg/OpenMetadata/product/config paths
ignored generated fixture/data/warehouse/export paths
unrelated user files
```

Issue #6's four handoff files are read-only even though they are present after merge.

Generated-only runtime paths `.artifacts/evidence/web-spike/**` and
`.artifacts/runtime/i5-02/**` may exist while commands run. They are never staged or treated as
implementation ownership. Before publication, sanitize/hash-index required raw evidence into
`spikes/web/evidence/retained/**`, remove transient generated state, and require the Git changed
set to match only the explicit tracked allow-list.

## Planned Layout

```text
spikes/web/
  common/
    contracts/
    fixtures/
    state/
    tests/
  preview/
    index.html
    preview.css
    preview.mjs
  harness/
    authority.json
    toolchain.json
    candidate-modes.json
    test-ids.json
    score-anchors.json
    fixture-handoff.json          # only after Barrier B
    scripts/
    tests/
  candidates/
    astro/                        # own package.json + package-lock.json
    next/                         # own package.json + package-lock.json
    vite/                         # own package.json + package-lock.json
  evidence/
    retained/
    retention-index.json
  non-copy-inventory.md
mk/issue-5/i5-02.mk
docs/decisions/0005-web-stack.md
docs/decisions/evidence/adr-0005-web-stack-scorecard.{md,json}
```

No root package workspace/lockfile is added. The common harness is dependency-free and has no
manifest/lock. Each candidate has its own exact manifest/lock so one install cannot mutate another
candidate's dependency evidence. Root `.gitignore` ignores `package-lock.json`; force-add exactly
the three candidate locks and prove they are tracked, never edit `.gitignore` or broadly add
ignored paths.

## Start Conditions by Gate

| Work | May begin when | Must remain blocked while |
|---|---|---|
| Gate 0 registry/tests/checker/make fragment | Independent validation + readiness audit name exact `IMPLEMENTATION_INPUT_SHA`; initial local/tracking/live remote equality passes | Wrong/dirty/drifted base, missing ancestry, path lease conflict, protected drift |
| Gate A common tests + neutral preview | Gate 0 passes | Common contract unstable; S3/path failure |
| Astro/Next/Vite foundations | Gate A contract/test-ID digest frozen | Before Gate A; each stays provisional before #6 |
| Barrier B check | #6 reviewed merge SHA is in tested ancestry and four tracked files exist | #6 open/unmerged; any digest/schema/read-only mismatch |
| Gate C decision rerun | Barrier B passes and current browsers/manual named-AT session are available/frozen | Browser/manual evidence absent; mixed environment/fixture |
| Gate D ADR/retention | Gate C full must-pass/comparability result exists | Partial/invalid evidence; cap overrun |

Before issue #6 merges, only Gate A and candidate foundations may run. Nothing before that merge
can produce a numeric score, winner, or decision-grade ADR. Browser discovery unavailability does
not block authoring/preview, but it blocks Gate C.

## Bite-Sized TDD Order

1. Gate 0: write wrong-SHA/hash/path/toolchain/mode/ID tests; implement registry/checker; pass clean
   case and all negatives.
2. Gate A: write shared WEB contract/state/failure/trust/static/security tests; retain failing IDs;
   implement semantic HTML; then CSS; then optional navigation/reset/verify/evidence enhancement.
3. For each candidate independently: point unchanged common tests at missing candidate; add only
   framework-mode/build tests; start timer; implement to 90m foundation; continue to 3h
   provisional must-pass or eliminate.
4. Barrier B: write absent/unmerged/mixed/tampered fixtures; implement read-only merge/digest/schema
   checker; populate observed digests only from merged bytes.
5. Gate C: write scoring rejection cases before measurement; run clean identical real-fixture,
   current-browser/manual AT, measurement, content-authoring and security/non-copy gates; score only
   complete survivors.
6. Gate D: write ADR/scorecard/retention mismatch tests; generate JSON from verified indexes;
   author Proposed winner or no-winner; reproduce/rollback; retain evidence.

Never change expected results to make an implementation pass. A shared assertion correction
requires returning to Gate A, invalidating all candidates, and staying inside the original cap.

## Issue-Local and Direct Commands

All future Make invocations use:

```bash
make -f mk/issue-5/i5-02.mk <target>
```

The target and failure/evidence contracts are complete in
[Candidate protocol](./candidate-protocol.md#planned-command-registry). Minimum workflow:

```bash
make -f mk/issue-5/i5-02.mk i5-02-authority-check IMPLEMENTATION_INPUT_SHA=<full-40-hex-authorized-sha>
make -f mk/issue-5/i5-02.mk i5-02-security-check
make -f mk/issue-5/i5-02.mk i5-02-credential-check
make -f mk/issue-5/i5-02.mk i5-02-non-copy-check
make -f mk/issue-5/i5-02.mk web-common-test
make -f mk/issue-5/i5-02.mk learn-preview LESSON=promotion-trust
make -f mk/issue-5/i5-02.mk learn-preview-status
make -f mk/issue-5/i5-02.mk learn-preview-reset-check LESSON=promotion-trust
make -f mk/issue-5/i5-02.mk learn-preview-down

make -f mk/issue-5/i5-02.mk web-astro-install
make -f mk/issue-5/i5-02.mk web-astro-build
make -f mk/issue-5/i5-02.mk web-astro-test
make -f mk/issue-5/i5-02.mk web-astro-evidence SCOPE=foundation

# Repeat the same four foundation commands with web-next-* and web-vite-*.
# After all three locks exist, stage only the ignored lockfiles explicitly:
git add -f -- spikes/web/candidates/astro/package-lock.json spikes/web/candidates/next/package-lock.json spikes/web/candidates/vite/package-lock.json

make -f mk/issue-5/i5-02.mk web-barrier-b-check I5_01_MERGE_SHA=<full-40-hex-merged-sha>
make -f mk/issue-5/i5-02.mk web-real-fixture-rerun I5_01_MERGE_SHA=<full-40-hex-merged-sha>
make -f mk/issue-5/i5-02.mk web-browser-evidence
make -f mk/issue-5/i5-02.mk web-manual-a11y-check
make -f mk/issue-5/i5-02.mk web-spike-scorecard-check
make -f mk/issue-5/i5-02.mk web-retention-check
make -f mk/issue-5/i5-02.mk web-winner-reproduce
make -f mk/issue-5/i5-02.mk web-local-rollback-check
```

Direct no-build review fallback:

```bash
python3 -m http.server 4173 --bind 127.0.0.1 --directory spikes/web/preview
```

Direct test/check scripts are the source of behavior; Make targets are thin issue-local wrappers.
A future root `make learn-preview` include/alias belongs to the root/shared owner and is not issue
#7 acceptance.

## Evidence/Exit Contract

- Canonical generated root: `.artifacts/evidence/web-spike/<run-id>/`.
- Schema: `fitness-result-v1`; exact command/tool/input/tested-tree/dependency SHAs, file/lock/mode/
  test digests, timer, must-pass, artifacts/hashes, redaction, retention, rollback.
- Required missing tool, browser, manual record, input, or assertion is non-zero `fail`; no silent
  skip. `not-run-optional` never applies to a must-pass.
- Barrier B non-readiness is expected but still non-zero; it is not a pass/score.
- Candidate pre-B evidence has `evidenceScope: foundation`, is `PROVISIONAL_UNSCORED` or
  `ELIMINATED` with score null, and enumerates browser/manual/real-fixture gates as required pending
  `decision` scope. Gate C runs candidate a11y/E2E; they are never optional or provisional passes.
- A valid explicit no-winner scorecard can pass schema/consistency while leaving I5-05 blocked.

## Changed-Path and Protected Checks

The future `i5-02-changed-path-check` evaluates committed, staged, unstaged, and untracked paths
relative to the exact `IMPLEMENTATION_INPUT_SHA`. It allows only the explicit list above, rejects
raw discovery changes, and requires all three exact ignored candidate locks to be tracked. It must
not rely on a broad glob that includes all `docs/**`, `mk/**`, or `plans/**`.

Required protected baselines from Gate 0:

- `Makefile`: `6b75a7a1f8e516e8967d317edb9de35378c02eddd645d2731dcf5cfc9bf52f54`
- `.gitignore`: `aa93e47707e95286126f47b3d70fe7fc6c047b49c861184533e38b3c5a971316`
- `release-manifest.json`: `f9037b5d946d14f7b1b9c020939f1a44961011f2ad933db9f2b69054abbf9539`
- `docs/code-standards.md`: absent and must remain absent
- discovery tree: `ed45ef287be3c0830466ae4a6b60a6bf22b1eb70`

Dependency paths may become present only through the recorded #6 merge and must have zero issue #7
diff. Portal/runner roots must remain absent.

Credential checks use high-confidence key/private-key/credential-assignment patterns plus bundle,
source-map, trace/header/cookie/path canaries. Ordinary planning words such as “token” are not a
secret finding; a matched value is a hard publication STOP and triggers purge/regeneration/rotation
as applicable.

## Rollback and Cleanup

1. Stop only the PID/process tree recorded under the issue-scoped runtime locator; reject foreign
   or reused PIDs.
2. Remove only candidate-local `node_modules`, build output, caches, and generated runtime state
   after retention indexes/hashes exist. Evidence remains.
3. On candidate failure, mark `ELIMINATED`, remove default execution selection, retain source/lock/
   commands/raw evidence, and keep the neutral preview.
4. On comparison contamination, close Barrier B/C, remove numeric scores/winner selection, return
   ADR-005 to Proposed/no-winner, and rerun equally if still inside cap.
5. Do not delete losing source before I5-05. Later cleanup requires explicit authority and a
   reproducible source bundle/hash.
6. Never use a broad recursive delete, destructive Git reset/checkout, shared contract edit,
   migration, cloud action, or root Make change as rollback.

## Handoff Completion

Implementation is complete only when the exact issue acceptance, S3 disposition, TDD evidence,
changed-path/protected/credential checks, retention/reproduction/rollback, human pre-merge approval,
and downstream independent gates pass. No score or automation may waive the human gate.
