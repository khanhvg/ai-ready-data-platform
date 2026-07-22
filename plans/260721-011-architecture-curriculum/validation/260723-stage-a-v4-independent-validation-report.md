# Issue #11 Stage A v4 Independent Validation Report

## Verdict

**PASS with one bounded plan-only fix.** This result validates the corrected plan at input
`dfd8e4c7704de5e1392d1028f5a25757a3e77166`. It is not readiness, cook authority,
implementation approval, product evidence, merge approval, or release approval. A different fresh
reviewer must bind the exact pushed validation output before deciding readiness.

The validator did not author the v4 correction. The session ran through Herdr with Codex
`gpt-5.6-sol` and reasoning effort `xhigh`; Herdr process inspection confirmed those exact runtime
arguments. CK reported CLI `4.5.2` and kit `engineer@v2.20.0`.

## Authority and Frozen Input

| Item | Exact result |
|---|---|
| Required branch | `plan/issue-11-architecture-curriculum` |
| Validation input | `dfd8e4c7704de5e1392d1028f5a25757a3e77166` |
| Input tree | `8eccbebd31ab5746b933b60bded73f46edb6107a` |
| Integration release | `5644f01b4c0443a81f3af0bcce80f44c847cd986` |
| Integration tree | `a38594d420fe7df2b30265a8a72bb5fad1698012` |
| PR #30 finding authority | [comment 5050486239](https://github.com/khanhvg/ai-ready-data-platform/pull/30#issuecomment-5050486239) |
| v4 recovery authority | [comment 5050513064](https://github.com/khanhvg/ai-ready-data-platform/issues/11#issuecomment-5050513064) |
| correction handoff | [comment 5050835678](https://github.com/khanhvg/ai-ready-data-platform/issues/11#issuecomment-5050835678) |

Before edits, the worktree and index were clean and local HEAD, tracking ref, `git ls-remote`, and
the live GitHub branch API all equalled the validation input. Integration is the exact merge base
and ancestor. The nine post-integration commits were linear, single-parent, and plan-only; the
direct diff was 20 additions under this plan directory and no other path. Failed v1/v2/v3 feature
heads, including `c07c9a080be7be88447aac497bdf0a2b5fddd020`, are not ancestors. No failed
product, test, render, or evidence byte entered the lineage.

## Bounded Fix

The corrected template registry specified compatibility on each registry row and reciprocal
instance version/hash bindings, but did not explicitly require every consuming instance to carry
a stable `instanceId` and the exact compatibility binding. The normative amendment, design,
requirement, and phase text now require:

- a stable unique `instanceId` per consuming binding;
- exact registry ID, template ID, version, content hash, and compatibility equality per instance;
- registry consuming-ID discovery equal to the instance-ID set; and
- real independent duplicate/drifted instance-ID and instance-compatibility mutations using the
  existing nonreciprocal and compatibility codes.

This changes no frozen path, command, family, code, template, module, flow, bridge, view,
protected, released, Stage B, or promotion count.

## Independent Results

| Gate | Result and evidence |
|---|---|
| Eight PR #30 findings | `8/8`; integration derivation, real repository RED, runtime shape, template lifecycle, visible render parity, module lifecycle, governance topology, and evidence truth are all closed |
| Stage A paths | `50/50` unique, absent at both integration and validation input; partition is exact `C1=7`, direct-child `C2=5`, semantic complement `38` |
| Commands | `16/16` unique; every literal line passed Bash syntax and argv parsing; runtime uses `$I11_RUNTIME/venv/bin/python` with candidate `$I11_RUNTIME` and direct parent root `$I11_RUNTIME/..` |
| RED catalogue | `22/22` families and `82/82` unique codes |
| Templates | `12/12` exact IDs at `1.0.0`; closed registration, instance identity/compatibility, canonical hash, predecessor, semantic-version, migration, rollback, supersession, tombstone, replacement, and orphan rules |
| Modules | `20/20` exact IDs: 4 foundation, 6 junior, 6 data, 4 mid; fixed acyclic progression and all ten meaningful lifecycle fields are mandatory and uniqueness-checked |
| Trace/render | `11/11` flows, `8/8` conceptual-only bridges, `5/5` useful views; LikeC4 JSON/DOT and locked WASM Graphviz are the sole visible semantic chain |
| Governance | `BR-GOVERNANCE-01` binds protected `learning.adapters -> retail` to `local.developer_host.adapters_instance -> local.developer_host.retail_instance`; reciprocal one-side and both-wrong mutations are required |
| Protected/released | `33/33` protected and `21/21` released paths match integration by Git blob and content SHA-256; all descriptor content hashes recompute |
| OpenAPI/golden | 16 released operation-matrix rows, zero released AsyncAPI channels, existing Python lock and architecture package lock present and hashed |
| Stage B | file, command, dependency-SHA, and renderer lists are empty; Issue #10 remains open without a passing merged journey, so Stage B is blocked |
| S3/resource | private ownership, raw retention, secret/private-path/URL/action scans, real process/resource mutations, TERM→KILL→wait/reap, and the `120 s`/`180 s` bounds are specified and implementable |

### Repository-Level RED

The fixed chronology is implementable without false RED: C1 creates only the seven generic
callable/router paths; direct-child C2 creates the four complete tests and one fixture; target
semantic rules arrive only in C3+. At C2, complete mode-0700 repository copies contain the real
schema, registry, source, render, manifest, evidence, and Git prerequisites. The harness strips
`expectedCode`, IDs, and assertion text before invoking production.

All 82 mutations must reach `check_repository()`, `_verify_repository()`,
`_toolchain_verification()`, and `_repository_handoff()` plus the matching Python CLI or Make
route. The mutation catalogue covers actual file/schema/template/trace/LikeC4/topology/visible
render/process/resource/raw-evidence/index/mode/type/link/porcelain state. Abstract Booleans or
dictionaries, expected-code echo/fallback, fixture dispatch, predicate-only checks, mocks,
monkeypatches, skips, and missing tool/import/path failures are explicitly forbidden. Raw stdout
and stderr, sanitized derivatives, and exact source/tree/repository-fixture/tool identities are
retained contemporaneously.

### Literal Command Simulation

The 16 literal shapes were parsed in order. Existing targets `help`, runtime admission, the three
released contract checks, and both protected architecture commands resolve today. The future
`curriculum-check` and `traceability-check` targets resolve through the existing sorted
`mk/issue-5/*.mk` include seam and the allow-listed `i5-06.mk`; all three future controller modes
map to the allow-listed `learning.curriculum.tools.architecture_expansion` module. Python 3.12,
Node 22.22.3, npm 10.9.8, the golden Python lock, and the exact LikeC4/WASM Graphviz package lock
are present. Candidate/root normalization is the direct-child layout required by released runtime
admission. No command needs an undocumented path correction.

### Visible Semantics, Curriculum, and Evidence

The render contract forbids hard-coded cards, manual parallel edges, fallback renderers, and
hidden hash-only freshness. A real relation endpoint, label, technology, or ordinal mutation must
rerun the locked pipeline and change visible SVG, fitted HTML, text, and hashes. Source, manifest,
parsed projection, DOT, visible DOM, and text must agree on nodes, boundaries, relations, labels,
technology, and order. Two-run byte determinism, Vietnamese-first labels, single numbering,
1440/1024 fit, contrast, clipping/overlap, accessibility metadata, and text alternatives remain
mandatory for all five views.

Every module must carry module-specific `starter`, `task`, `controlledFailure`, `verify`,
`evidence`, `reset`, progressive `hints`, gated `solution`, `tradeOffReflection`, and
`operationsConsequence`. Canonical meaningful bodies and whole learning signatures must be unique;
renamed filler fails. Promotion remains exactly `insufficient-evidence` / `no-common-grain` and
does not claim execution, progress, completion, or learner evidence.

Evidence retains the actual bounded raw RED bytes rather than only hashes, plus separate sanitized
logs bound to their raw sources. Owner, role, privacy class, media type, byte count, mode, file
type, link count, SHA-256, index closure, privacy scan, resource/render records, real Git porcelain,
and ignored-inclusive ownership are closed. Cook visual evidence is truthfully self-inspection
with `independent=false` and honest synthesis metadata; later independent implementation review
is a separate immutable bundle.

## Whole-Plan Checks

- CK strict JSON: `valid=true`, zero issues; status: seven pending phases and valid dependency
  chain.
- Markdown: 21 current plan artifacts, 53 local links, 18 checked anchors, zero failures.
- Static catalogue parser: `50/16/22/82/12/20/11/8/5`, all unique; protected/released
  `33/21`, all exact.
- Diff and scope: no whitespace errors; plan-only changes; no product/test/config/data path.
- Placeholder/private-path/secret scans: no unresolved authority placeholder, host-private path,
  credential, token value, private key, or action-bearing cloud command.
- Active lanes: Issue #9 owns `apps/lab-runner/**` and `i5-04.mk`; Issue #10 owns
  `apps/learning-portal/**` and `i5-05.mk`; Issue #12 remains dependency-empty with future
  `learning/labs/data-platform/**` and `i5-07.mk`; Issue #13 remains dependency-empty with future
  profile/Compose scope and `i5-08.mk`. The exact Issue #11 namespaces are disjoint.
- No product test, render, feature-worktree write, container, cloud, AWS, Terraform, merge, or
  approval action was performed.

## Handoff

After final checks, this report and the bounded normative fix may be committed and pushed as
plan-only provenance. The containing output SHA and local/upstream/live equality are reported in
the external Issue #11 handoff because a tracked file cannot truthfully contain its own commit
identity. On successful publication, the next gate is `fresh-plan-readiness-audit`; implementation
authority remains `none` and Stage B remains blocked.

`VALIDATION_VERDICT=PASS`
