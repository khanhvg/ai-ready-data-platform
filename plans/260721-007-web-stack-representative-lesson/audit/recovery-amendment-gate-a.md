---
title: "Recovery Amendment — Issue #7 Gate 0/Gate A Fresh RED Rerun"
issue: 7
phase: fresh-post-block-readiness-recovery-audit
status: recovery-ready
oldImplementationInputSha: "e8ca5f3ee9e8976a4b92915fd7d7dc687609f7a9"
newImplementationInputSha: "exact-amendment-output-sha-attested-in-issue-7-publication-comment"
authorizedScope: gate-0-and-gate-a-recovery-rerun-only
recoveryKind: recovery-rerun
auditedAt: "2026-07-21"
---

# Recovery Amendment — Gate 0/Gate A Fresh RED Rerun

## Verdict

`RECOVERY_READY` for one fail-closed `recovery-rerun` of the already authorized Gate 0/Gate A
scope. Recovery is authorized only after this amendment's plan-only output commit is published on
the plan branch and attested in issue #7.

The useful uncommitted source may be preserved outside the repository, but it cannot remain in the
product worktree for the new RED. The fresh cook must start from tests and inert invalid fixtures
only, capture a deterministic whole-working-tree digest before test execution, obtain intended RED
failures, and only then restore or reimplement non-test behavior incrementally. The quarantined
source is developer input, not evidence and not an implementation result that can be accepted
without a new RED/GREEN/verification sequence.

This amendment does not authorize product implementation in the plan worktree, a success cook in
this audit, a preview process, package/browser installation, a candidate, Barrier B, Gate C/D,
score, ADR, review, PR, merge, cloud action, history rewrite, or destructive cleanup. Issue #7
remains open and labelled `ready to cook`; this publication does not claim the preview is runnable.

## Immutable Old Inputs and Observed Blocker

| Item | Immutable value / observation |
|---|---|
| Previous readiness output and first implementation input | `e8ca5f3ee9e8976a4b92915fd7d7dc687609f7a9` |
| Previous audit input / validation output | `0486642528b9a6ba8e96cee18d6eda76c3b5deb9` |
| Planner output | `0890c4abab46f81d110be6cbd6de3560e631a735` |
| Discovery output | `a39251d45a56124322b9143ad16b926b2656073b` |
| Integration input | `f9a87d0ebdb72c014a6f8c6eaae865dad4d2188c` |
| Master readiness input | `e440c5855732d5d8f5d634e3cc1359c010cc5ed3` |
| Product worktree / branch | Exact sibling worktree `ai-ready-data-platform-issue-5-02-web-spike`; `feature/issue-5-02-web-spike` |
| Product local/tracking/live state observed by this audit | All exactly `e8ca5f3ee9e8976a4b92915fd7d7dc687609f7a9` |
| First cook transcript | `.hermes/logs/claudekit/issue-7-cook-gate-a.log`; 899,374 bytes; SHA-256 `82ac63f67967da634c4dc67c2492b0f1b64689c265eb76c71fd643916b4a444d` |
| Current authorized source set | 43 untracked regular files, all mode `0644`; no symlink, hard link, non-regular entry, staged path, tracked edit, or protected-path edit |
| Current source manifest observation | SHA-256 `c45fc62d99737f588ae596150e606c6758a8c75349518e564fb97b3eb5a42a94` over the exact sorted `sha256 two-spaces relative-path newline` manifest below |
| Current transient state | Zero `.artifacts` files; only empty generated directories may remain. Port `4174` is free. A foreign listener on `127.0.0.1:4173` is outside issue ownership and must not be signalled. |
| GitHub state observed by this audit | Issue #7 is open with `ready to cook`, `risk:high`, `tdd`, `security:S3`, `frontend`, `accessibility`, and `decision-gate` |

The first cook ran genuine Gate 0 and Gate A RED tests and later observed 27/27 harness and 27/27
common GREEN. It correctly stopped before commit or publication because it did not capture the
normatively required contemporaneous whole-working-tree digest for the original RED preimage.
Git, reflog, object recovery, transient artifacts, and the transcript cannot reconstruct the exact
preimage. Computing a digest now and attaching it to that old run would be fabrication.

The current 43-file manifest digest is only a post-block source-preservation observation. It is
not the missing digest, not a tested-tree digest, and not evidence that the old RED or GREEN is
acceptable. The old transcript and its copied archive remain provenance only.

## Recovery Compatibility Decision

The recovery is compatible with the binding rules when all controls below pass:

- **Path authority:** the repository receives only the already authorized Gate 0/A files; the
  quarantine is external, mode `0700`, never staged, and contains no candidate, issue #6, ADR, or
  protected path.
- **No-destructive-clean:** every source byte is archived and independently verified before any
  move; the move is reversible; no `git clean`, reset, checkout, broad delete, or overwrite is
  allowed. Exact empty directories may be removed only with `rmdir` after proving they contain no
  files.
- **Lease:** the same exact product worktree and feature branch are reused. No second product
  worktree or replacement branch is created.
- **Security:S3:** quarantine is owner-only; real credential/private-key/credentialed-URI hits
  stop recovery; the one inert test canary and example path are allowed only in their exact invalid
  fixture. The developer transcript stays external because it can contain absolute paths and raw
  tool context.
- **TDD and evidence:** all behavior is absent at the fresh pre-RED boundary; the digest is
  captured before execution; intended failures and outputs are retained; old RED output is not
  cited as acceptance evidence.
- **Rollback:** a verified archive, an extracted verification copy, and the moved payload all map
  to the same 43-file manifest. Partial moves restore without overwriting. Any byte or path
  variance is a STOP.
- **Three-hour Gate A budget:** quarantine, clean-old-input proof, and plan-only fast-forward are
  recovery preflight. The Gate A timer begins at the first common/lifecycle test or invalid-fixture
  write/restore and includes digest capture, RED execution, implementation, fixes, and final Gate A
  verification. It is not restarted after RED.
- **Remote equality:** old equality is proven before quarantine; new equality is proven after a
  normal fast-forward/push; final local/tracking/live equality is required again after the fresh
  cook. Rebase, reset, force push, or history rewrite is forbidden.
- **Issue state:** this amendment keeps `ready to cook`. It authorizes only the recovery rerun and
  does not open any deferred stage.

If the exact 43-file bytes cannot be preserved and restored, or any control above fails, the
effective verdict becomes `NOT_READY`. Deletion, variance acceptance, or retrospective evidence
is not an alternative.

## External Quarantine Root and Allowed Files

Resolve `workspace-parent` as the parent directory containing both issue worktrees. The exact
quarantine naming rule is:

```text
<workspace-parent>/.quarantine/issue-7-gate-a/
  recovery-rerun-<UTC-YYYYMMDDTHHMMSSZ>-e8ca5f3ee9e/
```

The timestamp is captured once with `date -u +%Y%m%dT%H%M%SZ`. The final component must not
already exist; collision, reuse, a symlink in any quarantine parent, or a root inside any Git
worktree is a STOP. Create it with `umask 077` and mode `0700`. Do not use a random fallback name
after a collision because the recorded root must stay unambiguous.

The payload may contain exactly these 43 relative files:

```text
mk/issue-5/i5-02.mk
spikes/web/common/contracts/candidate-evidence-record.schema.json
spikes/web/common/contracts/evidence-index-view.schema.json
spikes/web/common/contracts/failure-codes.json
spikes/web/common/contracts/journey-state-view.schema.json
spikes/web/common/contracts/lab-client-view.schema.json
spikes/web/common/contracts/lesson-manifest-view.schema.json
spikes/web/common/contracts/mart-evidence-view.schema.json
spikes/web/common/fixtures/synthetic-promotion-trust-v1.json
spikes/web/common/state/preview-state-vectors.json
spikes/web/common/state/preview-state.mjs
spikes/web/common/tests/browser-authority.test.mjs
spikes/web/common/tests/contract-schema.test.mjs
spikes/web/common/tests/failure-taxonomy.test.mjs
spikes/web/common/tests/fixtures/invalid-completed-state.json
spikes/web/common/tests/fixtures/invalid-cross-grain-attribution.json
spikes/web/common/tests/fixtures/invalid-executable-content.json
spikes/web/common/tests/fixtures/invalid-secret-canary.json
spikes/web/common/tests/fixtures/invalid-stale-digest.json
spikes/web/common/tests/fixtures/invalid-unknown-field.json
spikes/web/common/tests/four-grain.test.mjs
spikes/web/common/tests/journey-contract.test.mjs
spikes/web/common/tests/non-copy.test.mjs
spikes/web/common/tests/preview-authority.test.mjs
spikes/web/common/tests/preview-label.test.mjs
spikes/web/common/tests/state-navigation.test.mjs
spikes/web/common/tests/state-reset.test.mjs
spikes/web/common/tests/static-facts.test.mjs
spikes/web/harness/authority.json
spikes/web/harness/candidate-modes.json
spikes/web/harness/score-anchors.json
spikes/web/harness/scripts/authority-check.mjs
spikes/web/harness/scripts/preview-control.mjs
spikes/web/harness/scripts/static-host.mjs
spikes/web/harness/stage-status.json
spikes/web/harness/test-ids.json
spikes/web/harness/tests/authority.test.mjs
spikes/web/harness/tests/preview-control.test.mjs
spikes/web/harness/toolchain.json
spikes/web/non-copy-inventory.md
spikes/web/preview/index.html
spikes/web/preview/preview.css
spikes/web/preview/preview.mjs
```

Directories are structural only. No `.git`, `.hermes`, `.artifacts`, plan, retained evidence,
package/lock, candidate, fixture-handoff, ADR, issue #6, portal, runner, root, shared, ignored data,
or other file is payload-authorized.

## Quarantine Manifest, Archive, and Security Verification

The recovery controller must perform these checks from the product worktree after this amendment
is published but before moving any source:

1. Re-prove exact worktree/branch, `HEAD == tracking == live == old input`, clean tracked/index
   state, the exact 43 untracked paths, protected hashes, discovery tree, no port `4174` listener,
   and zero `.artifacts` files. Do not touch the foreign `4173` listener.
2. Materialize `expected-paths.txt` from the exact block above, `LC_ALL=C` sort it, require 43
   unique newline-safe paths, and compare it byte-for-byte with sorted
   `git ls-files --others --exclude-standard` output. Reject absolute paths, `..`, backslashes,
   control characters, or characters outside `[A-Za-z0-9._/-]`.
3. For every path, use `lstat`/`stat`, not a followed-link test. Require a regular file, link count
   1, and observed mode `0644`. Reject symlinks, hard links, sockets, devices, FIFOs, directories
   in the file list, or a real path escaping the product worktree.
4. Write `source.sha256` as 43 sorted UTF-8 lines of
   `<lowercase-sha256><two spaces><relative-path><newline>`. Require its SHA-256 to equal the
   audit-observed `c45fc62d99737f588ae596150e606c6758a8c75349518e564fb97b3eb5a42a94`.
   A mismatch means the source changed after audit and is a STOP, not a permitted update.
5. Write `metadata.tsv` with relative path, mode, byte count, and link count. Write
   `source-manifest.sha256` for `source.sha256`. Neither file is release evidence.
6. Run high-confidence credential/private-key/credentialed-URI/sensitive-file scans across the
   exact 43 paths. The only allowed policy fixtures are the exact literal
   `Bearer TEST_SECRET_CANARY_DO_NOT_ACCEPT` and `/Users/example/private/evidence.json` in
   `spikes/web/common/tests/fixtures/invalid-secret-canary.json`. Any other credential-like or
   personal absolute-path hit is a STOP.
7. Create `authorized-source.tar` from `expected-paths.txt` with paths relative to the product
   root. Record `authorized-source.tar.sha256`. Reject an archive member that is absolute,
   contains `..`, is not in the exact list, or is a symlink/non-regular entry.
8. Extract the archive into `archive-verify/` inside the quarantine. Recompute its path list and
   `source.sha256`; both must match exactly. Keep this verification copy until the recovery rerun
   is published.
9. Copy the first cook log separately to
   `blocked-attempt/issue-7-cook-gate-a.log`, require its SHA-256 to equal
   `82ac63f67967da634c4dc67c2492b0f1b64689c265eb76c71fd643916b4a444d`, and mark it
   `noncanonical-developer-transcript` in `quarantine-record.json`. It must not enter the payload,
   archive, Git index, retained Gate A evidence, or release evidence.

The archive must be created and extraction-verified while the source still exists in the product
worktree. Archive digest, archive member list, source manifest digest, extracted manifest digest,
file count, metadata digest, transcript digest, quarantine root name, old input, and later new
input are required fields in `quarantine-record.json`.

## Exact Move, Clean Proof, Restore, and Rollback

### Move to quarantine

After all pre-move checks pass:

1. Create `payload/` below the quarantine root.
2. Iterate `expected-paths.txt` in order. Create only the corresponding payload parent, then move
   the source file to `payload/<relative-path>`. Do not overwrite any destination.
3. If any move fails, stop immediately and run the partial-move rollback below.
4. Recompute the payload path list and manifest. Require exact equality with
   `expected-paths.txt` and `source.sha256`; require 43 regular non-symlink files.
5. Prove every listed product path is absent. Remove only now-empty `mk/**` and `spikes/**`
   directories with `rmdir` in depth-first order. Do not use `rm`, `git clean`, reset, checkout,
   or a recursive delete.
6. Prove `.artifacts` contains zero files. Remove only the known empty generated directory chain
   with exact `rmdir` calls; any non-empty directory is a STOP.
7. Prove the product worktree is clean at the old input: empty porcelain status, no staged or
   tracked diff, local/tracking/live all `e8ca5f3ee9e8976a4b92915fd7d7dc687609f7a9`, protected
   hashes/tree exact, and port `4174` free.

This is a byte-preserving reversible move, not authorization to delete product work.

### Partial-move rollback

For each path in order:

- if it exists only in `payload/`, recreate its product parent and move it back;
- if it exists in both locations, STOP without overwriting either copy;
- if it exists in neither, restore only from the verified `archive-verify/` copy, then recheck the
  archive digest and record the exceptional recovery;
- after restoration, require the product path list and manifest to equal the original 43-file
  set and leave the quarantine archive/transcript intact.

Any inability to restore exact bytes changes the verdict to `NOT_READY`. Do not compensate with a
fresh implementation or a deleted path.

### Normal restore for the fresh cook

The quarantine remains immutable developer input. Restore by copying, never by consuming the last
quarantine copy. Before RED, recreate only the 19 test/invalid-fixture paths in the tests-only list
below. After valid RED, restore or reimplement non-test files one audited slice at a time. Every
copied file is reviewed and updated for the new input/ancestry before execution; the old bytes do
not receive grandfathered acceptance.

## Branch Fast-Forward and Sole New Input Rule

Only after the source is quarantined and the product worktree is proven clean at the old input:

1. Require this amendment output to be a strict descendant of
   `e8ca5f3ee9e8976a4b92915fd7d7dc687609f7a9`, contain only the exact issue #7 plan/audit change,
   and equal local/tracking/live on `plan/issue-7-web-stack-representative-lesson`.
2. Fetch normally. Fast-forward `feature/issue-5-02-web-spike` to the published amendment output
   with `git merge --ff-only <OUTPUT_SHA>`.
3. Push normally to `origin/feature/issue-5-02-web-spike`; fetch again and require local,
   tracking, and live remote to equal the output SHA.
4. Do not rebase, reset, force push, cherry-pick, recreate the branch/worktree, or rewrite history.

The exact amendment output SHA is the sole new `IMPLEMENTATION_INPUT_SHA`. The old input remains a
required ancestor and provenance value but is invalid as an implementation input for the rerun.
No branch name, tag, predecessor, reconstructed SHA, or later descendant may substitute without a
new readiness decision.

## Fresh Tests-Only RED Boundary

### Only paths allowed before RED

Exactly these 19 untracked files may exist in addition to the new tracked input:

```text
spikes/web/common/tests/browser-authority.test.mjs
spikes/web/common/tests/contract-schema.test.mjs
spikes/web/common/tests/failure-taxonomy.test.mjs
spikes/web/common/tests/fixtures/invalid-completed-state.json
spikes/web/common/tests/fixtures/invalid-cross-grain-attribution.json
spikes/web/common/tests/fixtures/invalid-executable-content.json
spikes/web/common/tests/fixtures/invalid-secret-canary.json
spikes/web/common/tests/fixtures/invalid-stale-digest.json
spikes/web/common/tests/fixtures/invalid-unknown-field.json
spikes/web/common/tests/four-grain.test.mjs
spikes/web/common/tests/journey-contract.test.mjs
spikes/web/common/tests/non-copy.test.mjs
spikes/web/common/tests/preview-authority.test.mjs
spikes/web/common/tests/preview-label.test.mjs
spikes/web/common/tests/state-navigation.test.mjs
spikes/web/common/tests/state-reset.test.mjs
spikes/web/common/tests/static-facts.test.mjs
spikes/web/harness/tests/authority.test.mjs
spikes/web/harness/tests/preview-control.test.mjs
```

The six JSON files are inert invalid data only. No valid fixture, schema, state/reducer, registry,
score anchor, stage status, Make fragment, non-copy inventory, preview HTML/CSS/JS, controller,
host, authority checker, retained evidence, package, candidate, or other non-test behavior may be
present. `.artifacts` may contain only the new recovery evidence written after the path check and
is excluded from the digest by rule.

Tests are recreated from the audited requirements. Quarantine copies may be consulted, but before
RED the two harness tests must replace the old input literal with the published new input;
`authority.test.mjs` must also require the old readiness output as an immutable ancestor. Prefix
the 17 lifecycle subtests with the evidence aliases below. These are provenance strengthening,
not expected-result changes. Any removal, relaxation, skip, todo, narrowed hostile input, or
changed expected product behavior is a STOP.

### Failure IDs and commands

Run exactly, separately, and retain full TAP plus exit status:

```bash
node --test spikes/web/harness/tests/authority.test.mjs
node --test spikes/web/harness/tests/preview-control.test.mjs
node --test spikes/web/common/tests/*.test.mjs
```

Expected Gate 0 failures are the exact ten IDs:

```text
G0-AUTH-001 G0-REMOTE-001 G0-ANCESTRY-001 G0-PROTECTED-001 G0-PATH-001
G0-TOOLCHAIN-001 G0-REGISTRY-001 G0-ANCHOR-001 G0-STAGE-001 G0-DEFERRED-001
```

Expected lifecycle aliases, in test order, are:

```text
GA-LIFE-001 invalid port/no scan
GA-LIFE-002 occupied test-owned port/no signal
GA-LIFE-003 fixed 10-second timeout/scoped attempted-group cleanup
GA-LIFE-004 surviving attempted process is reported
GA-LIFE-005 stale/reused PID and locator-field mismatch/no signal
GA-LIFE-006 exact route/path/symlink/traversal/query/method rejection
GA-LIFE-007 wrong lesson or fixture digest rejected
GA-LIFE-008 only new audited input and canonical fixture digest accepted
GA-LIFE-009 double reset/baseline/audit counter/history contract
GA-LIFE-010 down without locator is idempotent/no signal
GA-LIFE-011 foreign listener or locator mismatch/no signal
GA-LIFE-012 observed authority binds fixed host/requested port
GA-LIFE-013 surviving verified owned process is reported
GA-LIFE-014 readiness binds lesson/digest/run/input
GA-LIFE-015 canonical fixture bytes/digest validation
GA-LIFE-016 redirect rejection and fixed host authority
GA-LIFE-017 real asset rejects symlink/outside/non-regular before read
```

The common command must execute 27 subtests and cover all 19 canonical `WEB-*` IDs from the
existing audit. Every subtest must fail for absent required behavior/data/source, while browser and
manual facets remain `required-pending`. A top-level import crash that prevents named subtests from
executing, a syntax/tool failure, an unexpected pass, a failure caused by a foreign port/process,
or a missing ID is not valid RED.

### Deterministic contemporaneous pre-RED digest

Use algorithm `recovery-working-tree-v1`:

1. Require no staged/unstaged tracked change.
2. Read tracked paths from `git ls-files -z` and untracked paths from
   `git ls-files --others --exclude-standard -z`.
3. Require the untracked set to equal the 19-path list above.
4. Exclude path prefixes `.git/`, `.hermes/`, and `.artifacts/` only. No other exclusion is
   permitted.
5. Sort unique relative paths by raw UTF-8 bytes under bytewise/C ordering.
6. Reject absolute paths, `.`/`..` segments, symlinks, Git links, and non-regular files.
7. For each file append this canonical binary record:
   `F NUL four-digit-octal-mode NUL decimal-byte-count NUL relative-UTF8-path NUL lowercase-content-SHA256 NUL`.
8. Concatenate records in sorted order. SHA-256 of those bytes is the working-tree digest. Retain
   the exact binary manifest and a JSON record before executing any RED command.

The following is the normative capture command. Substitute the published full SHA and a safe run
ID literally; do not pass or record an environment dump:

```bash
node --input-type=module - <NEW_IMPLEMENTATION_INPUT_SHA> <run-id> <<'NODE'
import { execFileSync } from 'node:child_process';
import { createHash } from 'node:crypto';
import { lstatSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs';

const implementationInputSha = process.argv[2];
const runId = process.argv[3];
const authorizedUntracked = [
  'spikes/web/common/tests/browser-authority.test.mjs',
  'spikes/web/common/tests/contract-schema.test.mjs',
  'spikes/web/common/tests/failure-taxonomy.test.mjs',
  'spikes/web/common/tests/fixtures/invalid-completed-state.json',
  'spikes/web/common/tests/fixtures/invalid-cross-grain-attribution.json',
  'spikes/web/common/tests/fixtures/invalid-executable-content.json',
  'spikes/web/common/tests/fixtures/invalid-secret-canary.json',
  'spikes/web/common/tests/fixtures/invalid-stale-digest.json',
  'spikes/web/common/tests/fixtures/invalid-unknown-field.json',
  'spikes/web/common/tests/four-grain.test.mjs',
  'spikes/web/common/tests/journey-contract.test.mjs',
  'spikes/web/common/tests/non-copy.test.mjs',
  'spikes/web/common/tests/preview-authority.test.mjs',
  'spikes/web/common/tests/preview-label.test.mjs',
  'spikes/web/common/tests/state-navigation.test.mjs',
  'spikes/web/common/tests/state-reset.test.mjs',
  'spikes/web/common/tests/static-facts.test.mjs',
  'spikes/web/harness/tests/authority.test.mjs',
  'spikes/web/harness/tests/preview-control.test.mjs',
];
const git = (args, encoding = 'buffer') => execFileSync('git', args, { encoding });
const splitNul = (bytes) => bytes.subarray(0, -1).toString('utf8').split('\0').filter(Boolean);
const byteSort = (values) => [...values].sort((a, b) => Buffer.compare(Buffer.from(a), Buffer.from(b)));
const excluded = (path) => ['.git', '.hermes', '.artifacts'].some((root) => path === root || path.startsWith(`${root}/`));
const sha256 = (bytes) => createHash('sha256').update(bytes).digest('hex');

if (!/^[0-9a-f]{40}$/.test(implementationInputSha)) throw new Error('new input must be literal full SHA');
if (!/^[A-Za-z0-9][A-Za-z0-9._-]*$/.test(runId)) throw new Error('unsafe run ID');
if (git(['rev-parse', 'HEAD'], 'utf8').trim() !== implementationInputSha) throw new Error('HEAD/input mismatch');
if (git(['status', '--porcelain=v1', '--untracked-files=no'], 'utf8') !== '') throw new Error('tracked/index change present');

const tracked = splitNul(git(['ls-files', '-z']));
const untracked = byteSort(splitNul(git(['ls-files', '--others', '--exclude-standard', '-z'])));
if (JSON.stringify(untracked) !== JSON.stringify(byteSort(authorizedUntracked))) throw new Error('untracked set is not tests-only');
const paths = byteSort([...new Set([...tracked, ...untracked].filter((path) => !excluded(path)))]);
const records = [];
for (const path of paths) {
  if (path.startsWith('/') || path.split('/').some((part) => part === '' || part === '.' || part === '..')) throw new Error(`unsafe path: ${path}`);
  const stat = lstatSync(path);
  if (!stat.isFile() || stat.isSymbolicLink()) throw new Error(`non-regular digest member: ${path}`);
  const bytes = readFileSync(path);
  const mode = (stat.mode & 0o7777).toString(8).padStart(4, '0');
  records.push(Buffer.concat([
    Buffer.from('F\0'), Buffer.from(mode), Buffer.from('\0'),
    Buffer.from(String(bytes.length)), Buffer.from('\0'), Buffer.from(path), Buffer.from('\0'),
    Buffer.from(sha256(bytes)), Buffer.from('\0'),
  ]));
}
const manifest = Buffer.concat(records);
const treeDigest = sha256(manifest);
const evidenceRoot = `.artifacts/evidence/web-spike/${runId}/recovery-rerun/red`;
mkdirSync(evidenceRoot, { recursive: true, mode: 0o700 });
writeFileSync(`${evidenceRoot}/pre-red-tree.manifest.bin`, manifest, { mode: 0o600 });
writeFileSync(`${evidenceRoot}/pre-red-record.json`, `${JSON.stringify({
  schemaVersion: 'recovery-pre-red-v1',
  recoveryKind: 'recovery-rerun',
  issue: 7,
  branch: git(['branch', '--show-current'], 'utf8').trim(),
  implementationInputSha,
  capturedAtUtc: new Date().toISOString(),
  algorithm: 'recovery-working-tree-v1',
  trackedPathCount: tracked.filter((path) => !excluded(path)).length,
  authorizedUntrackedPathCount: untracked.length,
  totalPathCount: paths.length,
  treeDigest,
  manifestSha256: treeDigest,
  excludedRoots: ['.git', '.hermes', '.artifacts'],
  environmentRecorded: false,
  absolutePathsRecorded: false,
}, null, 2)}\n`, { mode: 0o600 });
process.stdout.write(`${treeDigest}\n`);
NODE
```

Immediately verify the two retained file digests, then write a separate pre-execution record with:

- `recoveryKind: recovery-rerun`;
- old blocked input and exact new implementation input;
- branch/worktree lease identity using safe relative/named values, not a personal absolute path;
- capture timestamp, algorithm, path counts, digest, manifest digest, and artifact digests;
- exact three commands, ten G0 IDs, 17 lifecycle aliases, 19 WEB IDs, and expected absent behavior;
- protected hashes/tree, clean tracked/index result, tests-only path result, remote equality result,
  timer start, and the assertion that no non-test behavior exists.

Only after that record is fsynced/closed may the first RED command execute. Retain each command's
start/end UTC, exit code, complete TAP, TAP SHA-256, named actual failures, intended-failure
classification, and the pre-RED digest. Write the result immediately after each command; do not
wait until GREEN or reconstruct it from a transcript.

## Non-Test Restore Boundary and GREEN Sequence

After and only after all three RED commands meet the intended-failure contract:

1. Restore Gate 0 registries, checker, and exact 12-target Make fragment from quarantine as
   developer input. Update the authorized input to the new SHA and require the old input plus all
   earlier immutable SHAs in ancestry. Recompute registry digests. Run the 10 authority tests to
   GREEN while lifecycle/common remain RED for missing behavior.
2. Restore/reimplement the six logical schemas, safe valid fixture, failure taxonomy, state
   vectors, and reducer behavior. Run the narrow common contract/state/failure/trust tests. Do not
   copy an old passing result or change an assertion to match the source.
3. Restore/reimplement semantic HTML, then CSS, then the smallest progressive script. Run static,
   label, no-authority, navigation, non-copy, and source/logical accessibility tests after each
   slice. Browser/manual facets stay `required-pending`.
4. Restore/reimplement static host and controller last. Run the 17 lifecycle tests, test-owned
   collision/foreign-process negatives, real start/status/reset/down on port `4174`, security/CSP/
   route/network/source/credential checks, and prove the foreign `4173` listener was never
   signalled.
5. Run the complete existing Gate 0/A command spine, protected/discovery/changed-path/stage/
   deferred scans, `git diff --check`, rollback drill, and both harness/common suites. Correct root
   causes only. The old 27/27 outputs are not evidence for this run.
6. Create a source commit, rerun the full suite at that exact `testedTreeSha`, retain only sanitized
   `fitness-result-v1` evidence under `spikes/web/evidence/retained/gate-a/<run-id>/**`, create the
   separate attestation commit, push normally, and prove clean local/tracking/live equality.

Tests may be strengthened from the audited requirements. They must not be removed, skipped,
renamed away from canonical IDs, relaxed, or edited to accept the quarantined implementation.
Behavior files may be copied only one audited slice at a time; broad restore followed by a single
GREEN run is prohibited.

## Allowed, Protected, and STOP Boundaries

### Allowed repository paths

The final recovery cook retains the exact original Gate 0/A allow-list in
[cook-scope-gate-a.md](./cook-scope-gate-a.md): the 43 paths above plus sanitized retained evidence
at `spikes/web/evidence/retained/gate-a/<run-id>/**`. Fresh evidence may exist transiently only
under `.artifacts/evidence/web-spike/<run-id>/{gate-0,gate-a,recovery-rerun}/**` and the exact
runtime locator grammar. It is never staged.

This amendment changes no implementation path authority. It adds recovery controls only.

### Protected paths and state

All original protected paths remain binding, including root `Makefile`, `.gitignore`,
`release-manifest.json`, absent `docs/code-standards.md`, immutable discovery, shared contracts/
schemas, issue #6 fixtures, portal, runner, existing product/data/config/runtime paths, candidate
paths/packages/locks, ADR/score paths, plans during implementation, foreign processes, cloud, and
Git history. Required baselines remain:

```text
Makefile                 6b75a7a1f8e516e8967d317edb9de35378c02eddd645d2731dcf5cfc9bf52f54
.gitignore               aa93e47707e95286126f47b3d70fe7fc6c047b49c861184533e38b3c5a971316
release-manifest.json    f9037b5d946d14f7b1b9c020939f1a44961011f2ad933db9f2b69054abbf9539
issue-7 discovery tree   ed45ef287be3c0830466ae4a6b60a6bf22b1eb70
```

### Additional recovery STOP conditions

Stop without deletion, workaround, or scope expansion on:

- plan-branch drift before this amendment publication;
- source-manifest, path-count, mode, type, link, archive, extraction, transcript, or credential
  mismatch;
- quarantine inside a Git worktree, a reused root, insecure permissions, or symlinked parent;
- partial move that cannot be exactly rolled back;
- product worktree not clean at the old input before fast-forward;
- non-fast-forward relation, rebase/reset/force requirement, or new input not equal on all refs;
- any non-test behavior present at digest/RED time;
- any untracked path outside the exact 19-file pre-RED list;
- digest capture after test execution, missing/changed manifest, or evidence that records an
  absolute path/environment dump;
- unexpected pass, missing named subtest, syntax/tool/top-level failure, or RED caused by an
  unrelated environment/process;
- timer overrun, test weakening, bulk behavior restore, old-output reuse, evidence contamination,
  protected/deferred path, orphan process, or failure of any original STOP condition.

## Evidence Classification and Lifecycle

| Artifact | Classification | May be release/Gate A evidence? | Lifecycle |
|---|---|---:|---|
| Original cook log | Noncanonical developer transcript / provenance | No | External quarantine only; never staged |
| Original 43-file source manifest/archive/payload | Quarantined developer input | No | Keep through successful recovery publication and owner review |
| Old RED/GREEN output | Blocked-attempt provenance | No | May be referenced only to explain why recovery occurred |
| Fresh pre-RED manifest/digest and pre-execution record | Canonical `recovery-rerun` RED evidence | Yes, after sanitation/retention | Hash-index and retain |
| Fresh TAP and immediate RED result records | Canonical `recovery-rerun` RED evidence | Yes, only when intended failures validate | Hash-index and retain |
| Fresh GREEN/final suite at exact tested tree | Canonical Gate 0/A engineering evidence | Yes | Retain under the existing schema |
| Browser/manual facets | `required-pending` | No pass claim | Remain deferred to Gate C |

The quarantine is not automatically deleted. After fresh source and attestation commits are
pushed, final equality and retained-evidence hashes pass, and the issue comment is published, mark
the quarantine `superseded-awaiting-owner-cleanup`. Actual removal requires separate explicit
owner authorization and a final archive/payload verification; it is never part of the cook's
rollback or publication command.

## Final Publication and Label Rules

### This amendment publication

- Force-add only the exact issue #7 plan directory after ignore probing.
- Commit and push only this recovery amendment on
  `plan/issue-7-web-stack-representative-lesson`.
- The issue #7 comment must state the old input, exact blocker, amendment output/new sole
  implementation input, quarantine/tests-only/fresh-digest boundary, and that no product change,
  success cook, preview, PR, merge, or cloud action occurred.
- Keep `ready to cook` and every risk/security/TDD/frontend/accessibility/decision label. Do not
  claim preview runnable.

### Future recovery-cook publication

- Identify `recovery-rerun`, the exact new input, fresh pre-RED digest/manifest, exact RED command
  outputs, final tested tree, source commit, attestation commit, timer, rollback, protected/path/
  credential results, and pending browser/manual facets.
- Reference the first blocked attempt only as provenance. Do not attach, stage, or reclassify the
  old transcript/archive as release evidence.
- Stop after Gate A. Do not auto-open candidate work, score, ADR, PR, or merge. Any later phase
  requires a new readiness decision and human gates.

## No Retrospective Acceptance

No retrospective digest, reconstructed preimage, post-hoc label on the old RED, or current-source
digest may satisfy the missing evidence field. No old RED output is accepted. Only a genuinely
fresh tests-only RED run, with the deterministic working-tree digest captured and retained before
execution at the new implementation input, can reopen implementation.

`RECOVERY_VERDICT=RECOVERY_READY`

`ISSUE_STATE=ready to cook`
