---
title: "Authorized Cook Scope — Issue #6 Full Eight-Phase Serialized Core"
issue: 6
status: authorized-with-gates
authorization: full-eight-phase
auditInputSha: "c27d5fdadbf5bcf4f635de14241250d5ac238e45"
plannerSha: "cec9f6b02cb3bf9f2aa7e2cf26af32692008aacd"
discoverySha: "7a65da010abf0e3730731b6d744b532156c48fdc"
integrationSha: "f9a87d0ebdb72c014a6f8c6eaae865dad4d2188c"
masterReadinessSha: "e440c5855732d5d8f5d634e3cc1359c010cc5ed3"
implementationInputSha: "exact-audit-output-sha-attested-in-issue-6-publication-comment"
futureBranch: "feature/issue-6-golden-baseline-contracts"
futureWorktreeName: "ai-ready-data-platform-issue-6-implementation"
writerCount: 1
---

# Authorized Cook Scope — Full Eight-Phase Serialized Core

This is the complete and only issue #6 implementation lease. It authorizes one future cook to
execute phases 1–8 sequentially and stop after the C2 fixture attestation. It does not authorize a
PR, merge, tag, integration rebase/merge, destructive cleanup, cloud action, generalized runner,
publisher implementation, framework scoring/ADR, or human-gate bypass.

## Exact Input, Branch and Worktree

The only valid `IMPLEMENTATION_INPUT_SHA` is the full audit output commit published in the issue
#6 readiness comment. It is the commit containing this file. A literal SHA cannot be embedded in
its own containing commit without recursion; the issue comment is the external authority. Do not
use the audit input, planner SHA, branch tip by name, abbreviated SHA or `HEAD` as a substitute.

Resolve `{workspace-parent}` as the parent directory of the primary repository. The only future
product lease is:

```text
branch:   feature/issue-6-golden-baseline-contracts
worktree: {workspace-parent}/ai-ready-data-platform-issue-6-implementation
writer:   one sequential implementation actor
```

Before creation, run read-only absence and drift checks:

```bash
set -euo pipefail
PRIMARY_REPO_ROOT="$(git rev-parse --show-toplevel)"
WORKSPACE_PARENT="$(dirname "$PRIMARY_REPO_ROOT")"
IMPLEMENTATION_BRANCH='feature/issue-6-golden-baseline-contracts'
IMPLEMENTATION_WORKTREE="$WORKSPACE_PARENT/ai-ready-data-platform-issue-6-implementation"
IMPLEMENTATION_INPUT_SHA="$(gh issue view 6 --repo khanhvg/ai-ready-data-platform --json comments --jq '[.comments[].body | try capture("(?m)^OUTPUT_SHA=(?<sha>[0-9a-f]{40})$").sha] | last // ""')"
test "${#IMPLEMENTATION_INPUT_SHA}" -eq 40
case "$IMPLEMENTATION_INPUT_SHA" in (*[!0-9a-f]*) exit 1;; esac
git -C "$PRIMARY_REPO_ROOT" fetch --prune origin
if git -C "$PRIMARY_REPO_ROOT" show-ref --verify --quiet "refs/heads/$IMPLEMENTATION_BRANCH"; then exit 1; fi
test -z "$(git -C "$PRIMARY_REPO_ROOT" ls-remote --heads origin "refs/heads/$IMPLEMENTATION_BRANCH")"
if git -C "$PRIMARY_REPO_ROOT" worktree list --porcelain | grep -Fq "$IMPLEMENTATION_BRANCH"; then exit 1; fi
if git -C "$PRIMARY_REPO_ROOT" worktree list --porcelain | grep -Fq "$IMPLEMENTATION_WORKTREE"; then exit 1; fi
test ! -e "$IMPLEMENTATION_WORKTREE"
git -C "$PRIMARY_REPO_ROOT" cat-file -e "$IMPLEMENTATION_INPUT_SHA^{commit}"
```

The local `show-ref` command must exit non-zero, `ls-remote` must return no row, no worktree record
may name the branch/path, and the path must be absent. If any is present, STOP. Do not reuse,
delete, detach, prune around, reset or overwrite it.

Only after all absence checks pass:

```bash
git -C "$PRIMARY_REPO_ROOT" worktree add -b "$IMPLEMENTATION_BRANCH" "$IMPLEMENTATION_WORKTREE" "$IMPLEMENTATION_INPUT_SHA"
git -C "$IMPLEMENTATION_WORKTREE" push -u origin "HEAD:refs/heads/$IMPLEMENTATION_BRANCH"
git -C "$IMPLEMENTATION_WORKTREE" fetch origin "refs/heads/$IMPLEMENTATION_BRANCH"
LOCAL_SHA="$(git -C "$IMPLEMENTATION_WORKTREE" rev-parse HEAD)"
TRACKING_SHA="$(git -C "$IMPLEMENTATION_WORKTREE" rev-parse '@{upstream}')"
LIVE_SHA="$(git -C "$IMPLEMENTATION_WORKTREE" ls-remote origin "refs/heads/$IMPLEMENTATION_BRANCH" | awk '{print $1}')"
test "$LOCAL_SHA" = "$IMPLEMENTATION_INPUT_SHA"
test "$TRACKING_SHA" = "$IMPLEMENTATION_INPUT_SHA"
test "$LIVE_SHA" = "$IMPLEMENTATION_INPUT_SHA"
test -z "$(git -C "$IMPLEMENTATION_WORKTREE" status --porcelain=v1 --untracked-files=all)"
AUDIT_INPUT_SHA='c27d5fdadbf5bcf4f635de14241250d5ac238e45'
PLANNER_SHA='cec9f6b02cb3bf9f2aa7e2cf26af32692008aacd'
test "$(git -C "$IMPLEMENTATION_WORKTREE" rev-parse "$AUDIT_INPUT_SHA^")" = "$PLANNER_SHA"
for AUTHORITY_SHA in \
  "$AUDIT_INPUT_SHA" \
  "$PLANNER_SHA" \
  '7a65da010abf0e3730731b6d744b532156c48fdc' \
  'f9a87d0ebdb72c014a6f8c6eaae865dad4d2188c' \
  'e440c5855732d5d8f5d634e3cc1359c010cc5ed3'
do
  git -C "$IMPLEMENTATION_WORKTREE" merge-base --is-ancestor "$AUTHORITY_SHA" "$IMPLEMENTATION_INPUT_SHA"
done
ISSUE_GATE="$(gh issue view 6 --repo khanhvg/ai-ready-data-platform --json state,labels --jq '.state == "OPEN" and ([.labels[].name] | index("ready to cook") != null) and ([.labels[].name] | index("risk:high") != null) and ([.labels[].name] | index("tdd") != null) and ([.labels[].name] | index("security:S3") != null) and ([.labels[].name] | index("shared-core") != null) and ([.labels[].name] | index("data-integrity") != null)')"
test "$ISSUE_GATE" = 'true'
```

Before the first implementation write, require all of the following:

- clean staged/unstaged/untracked status;
- local HEAD = upstream = freshly observed live remote = exact implementation input;
- the audit input has the planner SHA as its first parent;
- implementation input ancestry contains audit input, planner, discovery, integration and master
  readiness SHAs from frontmatter;
- issue #6 remains open with `ready to cook`, `risk:high`, `tdd`, `security:S3`, `shared-core` and
  `data-integrity` labels;
- no other writer or shared-core/view/root-Make lease is active.

After creation, never rebase, merge integration/main, force-push, reset, replace the worktree or
create a second product worktree. An upstream/authority change requires STOP and a new
validation/readiness descendant. Ordinary issue-owned commits and non-force pushes are allowed;
before every external attestation, fetch and require exact local/upstream/live equality.

## Allowed Tracked Paths

No path outside this list is writable:

```text
scripts/golden/**
contracts/data/retail-golden-v1.json
contracts/data/promotion-trust-v1.yaml
contracts/data/curated-release-manifest.schema.json
learning/contracts/**
tests/golden/**
tests/contracts/**
tests/fixtures/learning/promotion-trust/evidence-v1.json
tests/fixtures/learning/promotion-trust/manifest.json
tests/fixtures/learning/promotion-trust/invalid/**
requirements/golden-py312-macos-arm64.in
requirements/golden-py312-macos-arm64.lock
requirements/golden-py312-macos-arm64.metadata.json
requirements/golden-lock-tools.in
requirements/golden-lock-tools.lock
requirements/architecture/package.json
requirements/architecture/package-lock.json
architecture/likec4/specification.c4
architecture/likec4/model/people-and-systems.c4
architecture/likec4/model/learning-platform.c4
architecture/likec4/model/data-platform.c4
architecture/likec4/model/local-deployment.c4
architecture/likec4/views/C4-L0.c4
architecture/likec4/views/C4-L1.c4
architecture/likec4/views/C4-L2-LOCAL.c4
architecture/likec4/views/C4-L3-RUNNER.c4
architecture/likec4/views/DEP-LOCAL.c4
architecture/likec4/views/DYN-JOURNEY.c4
architecture/likec4/view-manifest.yaml
architecture/rendered/C4-L0.svg
architecture/rendered/C4-L0.txt
architecture/rendered/C4-L1.svg
architecture/rendered/C4-L1.txt
architecture/rendered/C4-L2-LOCAL.svg
architecture/rendered/C4-L2-LOCAL.txt
architecture/rendered/C4-L3-RUNNER.svg
architecture/rendered/C4-L3-RUNNER.txt
architecture/rendered/DEP-LOCAL.svg
architecture/rendered/DEP-LOCAL.txt
architecture/rendered/DYN-JOURNEY.svg
architecture/rendered/DYN-JOURNEY.txt
architecture/rendered/render-manifest.json
Makefile
mk/issue-5/i5-01.mk
orchestration/airflow/callables/pipeline.py
```

`Makefile` is limited to the two-line ordered optional-fragment seam. The Airflow file is
deny-by-default and becomes writable only after the retained phase-7 RED proves explicit private
path forwarding is absent. `requirements/architecture/package-lock.json` is the only ignored path
that may be exact-path force-added, after its 119-record/hash check. Never force-add a directory.

The plan/discovery/validation/audit directory is read-only during implementation. Record phase
status and implementation evidence externally; do not edit planning history to satisfy the cook.

## Protected Input Baseline

These are exact at audit input and remain the future input baseline because the audit changes only
the issue #6 plan directory:

| Path/state | SHA-256 or Git identity | Rule |
|---|---|---|
| `release-manifest.json` | SHA-256 `f9037b5d946d14f7b1b9c020939f1a44961011f2ad933db9f2b69054abbf9539`; blob `b27d231c5ee6d48fd7932b06807ef6a9a2220e21` | byte-identical |
| `.gitignore` | SHA-256 `aa93e47707e95286126f47b3d70fe7fc6c047b49c861184533e38b3c5a971316`; blob `712af7b245326ea6e193818fa928028875fab657` | byte-identical |
| `docs/code-standards.md` | `ABSENT` | remain absent; never create/delete/overwrite |
| discovery tree | tree `ece71d086b36a439c86c645222fc503a17d19539` | byte-identical |
| `Makefile` before narrow seam | SHA-256 `6b75a7a1f8e516e8967d317edb9de35378c02eddd645d2731dcf5cfc9bf52f54`; blob `41b385c2119520e8925fb1a48ef291e9e64154cb` | only exact two-line seam |
| Airflow callable before exception | SHA-256 `cb610c5fc4c52f149dfe0d97fd0fcca44fd4ff67bf28c19d662b1f4d41e5ee2d`; blob `9e67d230a199768c7a4b6e1be4387a386002d930` | only proven forwarding diff |
| `orchestration/airflow/dags/retail_batch_pipeline.py` | SHA-256 `0c0579c4950c145b66ab1b089af0b35ac1d30656310c6caa95ae19c7a1ef8814`; blob `77b1fd204c1340ff62fd376651da0b67d1a9b423` | byte-identical |
| `data/raw/.gitkeep` | SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`; blob `e69de29bb2d1d6434b8b29ae775ad8c2e48c5391` | byte-identical |
| `data-generator/` | tree `833fad3dd01a9130ccadd48a958c3b2cd952422e` | read-only |
| `ingestion/` | tree `662d07e475e69e0cb23110df3dec4d0bf52636a6` | read-only |
| `transform/dbt/` | tree `28932692fc20e079eecbe7ab1c9f93b2a94a8bbf` | read-only |
| `serving/rill/` | tree `27bda8a14222cae083d480275453659adb85b3ff` | read-only |
| `lake/` | tree `2c072d268e9d56bb3b29abd78e8b53fef6a03220` | read-only; no publisher edit |
| `governance/` | tree `dcc91c9a0776df32377bea2f3948eb5c0864c0a7` | read-only |
| `mk/issue-5/i5-02.mk` through `i5-14.mk` | all `ABSENT` in issue #6 input | remain absent/read-only in this worktree |
| `portal/`, `runner/`, `terraform/`, `.artifacts/` | all `ABSENT` at input | no tracked creation; `.artifacts` may be cook-created untracked only |
| promotion fixture root | `ABSENT` | created only at C2 under exact authority |

Snapshot all tracked paths plus visible untracked/ignored sentinels before work. The new worktree
must start with no unrelated state. Never delete or stage state owned by another worktree; issue
#7's concurrent Gate A work is outside this lease.

## Serialized Task Order

At most one task is active. Do not bulk-generate locks, schemas, views, fixture or evidence before
the corresponding RED task finishes and its failure record is retained.

| Task | Work | Exit gate |
|---|---|---|
| `L-01` | Create/publish the exact branch/worktree and freeze input/authority/protected state | all entry checks pass |
| `P1-R` | Add only phase-1 tests, test-private fixtures/helpers and bounded RED recorder | named P1 RED failures retained; current static readers pass |
| `P2-R` | Add only dependency-lock parser/platform/install tests | named P2 RED failures retained |
| `P2-I` | Materialize exact compiler lock, compile 840-line application lock, add read-only verifier/bootstrap | tool/app hashes exact; no full data run yet |
| `P1-G` | Use the private locked environment to close all current dynamic characterization and mutation tests | exact generator/dbt/mart/Rill/Airflow/curated/history anchors green |
| `P2-G` | Run two independent empty-cache installs, `pip check`, imports, freeze/package checks and focused rollback | both environments exact; phase 1/2 complete |
| `P3-R` | Add workspace/process/evidence attack and failure tests only | named P3 RED failures retained |
| `P3-I/G` | Implement minimum private allocator/process/atomic evidence core; refactor only green | all S3 path/process/redaction/cleanup cases green |
| `P4-R` | Add schema/JCS/registry/drift/capture-order tests only | named P4 RED failures retained |
| `P4-I/G` | Implement strict parser, schemas, registry, readers, projection/envelope and migrations | raw/projection/envelope and mutation gates green |
| `P5-R` | Add retail/promotion/release/pointer/fixture-candidate tests only | named P5 RED failures retained |
| `P5-I/G` | Implement three data contracts and pure validators; generate private fixture candidate only | exact 11-set/four-grain/89-row gates green; tracked fixture absent |
| `P6-R` | Add architecture tool/source/fitness/text/SVG/freshness/atomicity tests only | named P6 RED failures retained |
| `P6-I/G` | Add exact package/lock, six sources, wrapper and complete rendered set | Darwin two-install/three-render equality and mutations green |
| `P7-R` | Add command registry/Make compatibility/Airflow forwarding tests only | named P7 RED failures retained and line-scoped exception proven |
| `P7-I/G` | Add 54-row registry, seven-recipe fragment, exact root seam and only proven Airflow forwarding | 15 old targets preserved; seven new targets; graph/callers green |
| `P8-R` | Add two-run/shared-state/timeout/rollback/C1-C2-M/handoff tests only | named P8 RED failures retained |
| `P8-C1` | Run the entire pre-C1 suite, commit all producer/contracts/readers/tests except tracked fixture | clean C1 pushed; exact changed paths |
| `P8-A/B` | Execute two sequential formal runs from read-only C1 with disjoint private state | each ≤300 s, pair ≤600 s, exact projection equality |
| `P8-RB` | Rehearse lock/registry/schema/pointer/Make/architecture/workspace rollback before publication | old complete/readable state restored in private tests |
| `P8-C2` | Derive/scan/validate and commit only authorized fixture/manifest/raw-parser invalid files | clean tracked/index C2 child; only allow-listed untracked `.artifacts` evidence may remain; tracked bytes non-recursive |
| `P8-ATT` | Third-reader verify C1 evidence/C2 fixture, push, externally record C1/C2/four digests | local/upstream/live equal; issue #7 still merge-blocked; STOP |

Refactoring is allowed only inside the current phase after green and before its evidence
finalization. Any behavior change after C1 invalidates C1 and requires a new C1 plus both formal
runs. No task may be parallelized or silently merged with a later phase.

## RED Contract

All Python issue tests use `unittest`; no unreviewed test dependency is added. The first
test-infrastructure write may create `scripts/golden/tdd-red-capture.py`. It accepts a fixed
phase/expected-ID set, closes stdin, bounds stdout/stderr, executes the exact test command and
writes sanitized local evidence to:

```text
.artifacts/evidence/tdd-red/P<phase>/<run-id>/red-result.json
```

Required fields are phase, stable RED IDs, implementation input, clean-tree digest, exact command,
start/finish/duration, expected missing behavior, actual failure, exit code and bounded output
hash/relative locator. No absolute path, environment dump, credential, score, fixture publication
or false pass. These records remain untracked; phase 4 validates them against the final evidence
schema without rewriting the original capture.

Named RED IDs that must fail for the intended reason before their phase behavior:

| Phase | Required RED IDs |
|---:|---|
| 1 | `P1-RED-RETAIL-CONTRACT-MISSING`, `P1-RED-EVIDENCE-SCHEMA-MISSING`, `P1-RED-COMMANDS-MISSING`, `P1-RED-ARCH-SOURCES-MISSING`, `P1-RED-SEMANTIC-MUTATION-UNDETECTED` |
| 2 | `P2-RED-TOOL-LOCK-MISSING`, `P2-RED-APP-LOCK-MISSING`, `P2-RED-RFC8785-ROOT-MISSING`, `P2-RED-UNSUPPORTED-TUPLE`, `P2-RED-SDIST-OR-RESOLVER` |
| 3 | `P3-RED-PARENT-ESCAPE`, `P3-RED-SYMLINK-TOCTOU`, `P3-RED-FOREIGN-DESTINATION`, `P3-RED-CONCURRENT-PUBLISH`, `P3-RED-TIMEOUT-DESCENDANT`, `P3-RED-SENSITIVE-OUTPUT` |
| 4 | `P4-RED-DUPLICATE-NAME`, `P4-RED-NON-IJSON`, `P4-RED-JCS-VECTOR`, `P4-RED-FIVE-POINTER-DRIFT`, `P4-RED-REGISTRY-MIGRATION`, `P4-RED-DBT-CAPTURE-ORDER` |
| 5 | `P5-RED-RETAIL-CONTRACT`, `P5-RED-EXACT-11-ASSETS`, `P5-RED-MIXED-GENERATION`, `P5-RED-FOUR-GRAINS`, `P5-RED-INSUFFICIENT-EVIDENCE`, `P5-RED-FIXTURE-DENYLIST` |
| 6 | `P6-RED-TOOL-LOCK`, `P6-RED-SIX-VIEW-SET`, `P6-RED-C4-FITNESS`, `P6-RED-TEXT-FROM-MODEL`, `P6-RED-SVG-SEMANTICS`, `P6-RED-STALE-OR-NONDETERMINISTIC` |
| 7 | `P7-RED-54-OWNER-REGISTRY`, `P7-RED-15-TARGET-COMPAT`, `P7-RED-SEVEN-RECIPES`, `P7-RED-HELP-AVAILABILITY`, `P7-RED-AIRFLOW-PRIVATE-PATHS`, `P7-RED-AIRFLOW-GRAPH-CALLERS` |
| 8 | `P8-RED-SHARED-STATE`, `P8-RED-300-600-TIMEOUT`, `P8-RED-PROJECTION-DRIFT`, `P8-RED-ROLLBACK`, `P8-RED-C1-C2-M-RECURSION`, `P8-RED-FOUR-DIGEST-INVALIDATION`, `P8-RED-ARTIFACT-STAGING` |

The phase test modules and exact first-run command families are:

```bash
env -u PYTHONPATH PYTHONDONTWRITEBYTECODE=1 python3.12 -m unittest \
  tests.golden.test_generator_characterization \
  tests.golden.test_dbt_characterization \
  tests.golden.test_mart_rill_characterization \
  tests.golden.test_airflow_curated_characterization \
  tests.golden.test_historical_evidence_reader \
  tests.contracts.test_semantic_mutations -v

env -u PYTHONPATH PYTHONDONTWRITEBYTECODE=1 python3.12 -m unittest tests.golden.test_dependency_lock -v
env -u PYTHONPATH PYTHONDONTWRITEBYTECODE=1 python3.12 -m unittest tests.golden.test_workspace_security tests.golden.test_process_security tests.contracts.test_fitness_result_envelope -v
env -u PYTHONPATH PYTHONDONTWRITEBYTECODE=1 python3.12 -m unittest tests.contracts.test_canonicalization tests.contracts.test_schema_mutations tests.contracts.test_version_migration tests.golden.test_dbt_capture_order -v
env -u PYTHONPATH PYTHONDONTWRITEBYTECODE=1 python3.12 -m unittest tests.contracts.test_retail_golden_contract tests.contracts.test_curated_release_manifest tests.contracts.test_promotion_trust -v
env -u PYTHONPATH PYTHONDONTWRITEBYTECODE=1 python3.12 -m unittest tests.contracts.test_architecture_contract tests.golden.test_architecture_determinism -v
env -u PYTHONPATH PYTHONDONTWRITEBYTECODE=1 python3.12 -m unittest tests.contracts.test_command_registry tests.golden.test_make_compatibility -v
env -u PYTHONPATH PYTHONDONTWRITEBYTECODE=1 python3.12 -m unittest tests.golden.test_two_run_release tests.contracts.test_issue7_handoff -v
```

After the lock exists, rerun applicable modules using the private locked interpreter. A RED is
valid only if the named assertion fails because required behavior is missing; syntax/import/test-
harness errors, wrong input, missing unrelated tools, timeouts or fabricated failures do not pass
the gate. Never weaken an expectation to turn RED green.

## Dependency and Architecture Bootstrap

Dependency implementation is exact:

- native CPython 3.12 on Darwin arm64; every other tuple fails before network;
- compiler lock is materialized from the exact 40-line literal in
  [dependency-lock-decision.md](../dependency-lock-decision.md) and must hash `ece1d206…`;
- application `.in` has exactly seven roots, including direct `rfc8785==0.1.4`;
- two compiler runs must produce the same 840-line/56-distribution repository-relative lock SHA
  `f41c727b39f99106f95b7937b2811e8d27db89d1d5106e9f1d9effd4403143d2`;
- application installs use only `--require-hashes --only-binary=:all: --no-deps`, empty cache,
  private home/venv and `PIP_CONFIG_FILE=/dev/null`;
- both pass `pip check`, exact imports and sorted-`pip freeze --all` SHA
  `cdb87ed71e0996f90041371cc25138afa02d78b134cbdc4afe9c25baa6649bba`;
- sdist, alternate index, ambient resolver/config/cache and missing wheel fail non-zero.

Architecture implementation is exact:

- private official Node `22.22.3` Darwin-arm64 archive SHA
  `753c1629e168cc788ccc46ab61e0b35549fce08c07f82fcd3bb0d41f7fb01e7b` and npm `10.9.8`;
- package document SHA `5cebd6d09ecef1334a492b871e388049392b6c0f6c9738873438b88958bd475d`;
- 119-record npm lock SHA `7a56d803a47454023f40a04bcdb3b037f4ab2c2a05321292ad3b7f7225c2118c`;
- LikeC4 `1.59.1` and hpcc wasm Graphviz `1.22.2` exact integrities/licenses;
- two empty-cache `npm ci --ignore-scripts` installs; no `npx`, Java, Structurizr, browser,
  native Graphviz or global fallback;
- exact `format --check`, `validate --json`, `export json --skip-layout --pretty`, `gen dot`,
  computed-model text, wasm SVG and controlled normalization commands;
- exactly `C4-L0`, `C4-L1`, `C4-L2-LOCAL`, `C4-L3-RUNNER`, `DEP-LOCAL`, `DYN-JOURNEY`;
- validation/render is offline after bootstrap. Linux/Windows are unclaimed and not a cook gate.

## Green and Blast-Radius Spine

Run focused tests after each smallest implementation, then all issue tests before C1. The public
acceptance spine is:

```bash
make help
make golden-clean PROFILE=small SEED=42
make data-contracts-check
make evidence-contracts-check
make migration-contracts-check
make architecture-check
make architecture-render
git diff --check "$IMPLEMENTATION_INPUT_SHA"...HEAD
```

The issue fragment owns all and only those seven targets. The registry contains exactly 54
owner-command rows; later 47 rows are `future-owner` and have no recipe in this worktree. The root
Make diff is exactly:

```make
ISSUE_5_MAKE_FRAGMENTS := $(sort $(wildcard mk/issue-5/*.mk))
-include $(ISSUE_5_MAKE_FRAGMENTS)
```

`help` lives in `i5-01.mk` and derives existing/implemented/future availability from the registry.
Snapshot and compare the current 15 targets and their prerequisites/recipes/variables. Do not run
Docker/heavy targets or the existing broad `clean` to prove compatibility.

The conditional Airflow diff may only add default-preserving explicit raw, warehouse, private dbt
profile/target/log and export path parameters. Tests must prove import, AST/DAG parse, default
callers, explicit callers and exact six/eight task IDs/edges. The DAG remains byte-identical.

Before C1 and again at C2:

- run all `unittest` modules with the private locked interpreter;
- run all seven public commands and their missing-tool/mutation cases;
- compare protected hashes/absence markers and exact changed paths;
- scan tracked candidates and bounded evidence for credentials, private URLs/paths, usernames,
  raw PII-like identifiers, scores/ADR/causal attribution and recursive SHAs;
- require `git ls-files '.artifacts/**'` empty and no staged `.artifacts/**` path;
- require root release manifest, `.gitignore`, DAG, discovery, data/dbt/Rill/lake/governance and
  unrelated state unchanged.

## Formal C1/C2 Evidence

C1 contains producer, locks, contracts, readers, tests, six architecture sources/outputs, Make
registry/seam and the proven Airflow forwarding only. It contains no tracked promotion fixture.
Push C1 normally, fetch, and require clean local/upstream/live equality before formal runs.

Run A then B from the same read-only C1 source tree with distinct generated IDs and no shared
home, venv, pip/npm cache, raw data, warehouse, dbt target/log, export, architecture stage,
workspace or evidence root. Each `golden-clean` has one 300-second monotonic deadline; the pair has
one 600-second deadline. Python/bootstrap is inside the core guard. Lock compilation and
architecture bootstrap/render are separate evidenced commands and never inflate the core result.

Compare:

- exact 18 CSV bytes/6,812 rows and anomaly layers;
- exact 51/141/18 and 179/7/0/186 dbt results;
- exact 11 mart content/schema/null-position hashes and Rill/Airflow/curated/catalog identities;
- lock/package/environment/tool/schema/registry/tested-tree hashes;
- raw normalized equality after only five declared pointer removals;
- exact projection canonical bytes/hash with no drift;
- valid non-recursive envelope/artifact hash graph;
- exact six architecture SVG/text/render-manifest bytes.

Rehearse rollback before fixture publication. Then derive the complete 89-row aggregate fixture
from C1's equal projection. C2 adds only:

```text
tests/fixtures/learning/promotion-trust/evidence-v1.json
tests/fixtures/learning/promotion-trust/manifest.json
tests/fixtures/learning/promotion-trust/invalid/**
```

The fixture decision is `insufficient-evidence`; it has four independent grains/calculations/
limitations and no raw ID, secret, private locator/URL, framework score, ADR, causal attribution,
self digest, C2 or M. Its manifest records `testedTreeSha=C1`. C2 and later M exist only in the
external attestation. A third reader from a clean tracked/index source state verifies both retained
run bundles and C2 bytes without regenerating producer output; only the allow-listed untracked
`.artifacts` evidence roots may remain.

The issue #6 external record contains full C1, full C2, exact SHA-256 and Git blob IDs for:

```text
contracts/data/retail-golden-v1.json
contracts/data/promotion-trust-v1.yaml
tests/fixtures/learning/promotion-trust/evidence-v1.json
tests/fixtures/learning/promotion-trust/manifest.json
```

It states integrity-not-authenticity and leaves merge/tag identity absent. Issue #7 consumes only
a later reviewed remote M plus those four exact digests. Neither C1, C2, a feature-branch SHA,
local cook output nor synthetic Gate A evidence opens scoring.

## Time, Output and Disk Bounds

- one formal core run: 300 seconds; sequential pair: 600 seconds;
- Python bootstrap: 120 seconds inside each core run; generator/load/dbt/docs/export/evidence step
  bounds are those in [implementation-handoff.md](../implementation-handoff.md);
- help: 10 seconds; each data/evidence/migration check: 60 seconds; architecture check/render:
  120 seconds each outside the core guard;
- stdout/stderr: 2 MiB each per step; retained combined logs: 16 MiB/run;
- mutable golden root: 2 GiB; architecture bootstrap/stage: 2 GiB; retained evidence:
  256 MiB/run; preflight free space: 6 GiB.

On timeout or output/disk overflow, terminate the owned process group (TERM 5 seconds, KILL/reap
5 seconds), retain bounded sanitized failure evidence and STOP. At most one owner-approved retry
may repeat the identical network command/lock in a new root; retain the first failure. Never vary a
version/hash/index/binary flag, reuse a partial venv/cache, or delete prior/foreign state to retry.

## STOP Conditions

Stop without expanding scope on any:

- input/branch/worktree/upstream/live/ancestry/issue-label/lease mismatch or dirty entry base;
- pre-existing future branch/worktree, second writer/worktree, rebase/merge/force/reset request;
- unauthorized path, protected hash/absence drift, later fragment/fixture/product/cloud path;
- missing/incomplete/wrong lock, hash, distribution count, platform, wheel or compiler identity;
- sdist, resolver/index/config drift, dynamic installer, hidden network or unsupported host;
- failed required test, wrong/missing RED evidence, test weakening, bulk artifact generation before
  RED, required missing tool/evidence represented as skip;
- unsafe workspace/locator/permission/symlink/hardlink/special-file/TOCTOU/concurrency/cleanup;
- timeout, output/disk overflow, descendant leak or unsanitized evidence;
- raw/projection/envelope conflation, undeclared drift, schema/JCS/version/provenance recursion,
  authenticity overclaim or mutated retained v1;
- generator/dbt/mart/Rill/Airflow/curated/catalog/historical-context semantic drift;
- partial/mixed/extra release, publisher implementation, cross-grain attribution, score/ADR/raw ID;
- wrong/missing/extra architecture view, stale/nondeterministic render, semantic-erasing
  normalization, Java/Structurizr/browser/native/global fallback;
- Make target/owner/current-target collision, broad clean, later recipe, unproven Airflow edit;
- any tracked/staged `.artifacts`, unsafe fixture, failed rollback or self-containing C2/M claim;
- issue #7 treating anything before reviewed M/four digests as scoreable; or
- request for PR, merge, tag, cloud action, destructive migration or human-gate bypass.

## Rollback and Refusal

Failure before C1 preserves the implementation worktree and RED/failure evidence for review. Do
not run destructive Git checkout/reset or automatically delete tracked work. A reviewed inverse
patch or later `git revert` is the only tracked rollback, and only after owner direction.

Runtime cleanup is narrower:

1. open the exact issue-owned base through retained no-follow descriptors;
2. verify repository/base/run device/inode, marker schema, nonce, run ID and purpose;
3. signal only a fully matched owned process group;
4. preserve bounded failure evidence;
5. remove only verified cook-created mutable descendants, never evidence/foreign/user state;
6. refuse on any mismatch, link, mount/device change, unexpected type or active/stale lease.

Phase rollback restores coherent sets: tool/app lock+metadata, schema+registry+reader, prior private
current-pointer model, source+manifest+Node lock+six renders, and root Make seam+fragment. It never
hand-edits a lock/hash/SVG, invokes the existing root `clean`, changes `.gitignore`, deletes a
prior fixture/evidence version, or auto-breaks a lease.

## Explicitly Deferred and Human Gates

- independent post-implementation review/security validation and mandatory human pre-merge
  approval;
- PR, merge/tag and any integration update;
- I5-07 publisher staging/switch/read-back/reconciliation implementation;
- I5-04 generalized privileged runner containment;
- I5-06 additions-only view lease and every view after the original six;
- I5-14 signing/authenticity;
- issue #7 Barrier B until reviewed M and four exact digests, then its browser/manual/score/ADR
  gates;
- portal, runner, Docker/Compose mutation, Terraform/AWS/cloud, AI and destructive migration;
- Linux/Windows dependency or architecture support.

After `P8-ATT`, stop. The feature branch is implementation evidence, not a merged release.
