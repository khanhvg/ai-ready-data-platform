# Independent initial plan validation — issue #6 / I5-01

**Verdict: PASS** after bounded planning corrections. No unresolved blocker requires planner rework. Implementation remains prohibited until a separate fresh readiness audit publishes the exact accepted implementation input and the human authorizes the later implementation phase.

This was a fresh `$ck:plan validate` full-tier session. It did **not** run plan red-team, readiness audit, `$ck:cook`, implementation, dependency-lock publication, product/config/data edits, architecture-source creation, fixture generation, cloud actions, destructive migration, PR creation or merge.

## Inputs and authority

| Input | Verified value / disposition |
|---|---|
| Repository | `khanhvg/ai-ready-data-platform` |
| Worktree | Exact user-authorized issue #6 worktree verified by `pwd`; absolute host locator intentionally omitted from the publishable report |
| Branch | `plan/issue-6-freeze-golden-baseline-contracts` |
| Planner artifact / validation input | `cec9f6b02cb3bf9f2aa7e2cf26af32692008aacd` |
| Discovery | `7a65da010abf0e3730731b6d744b532156c48fdc` |
| Integration | `f9a87d0ebdb72c014a6f8c6eaae865dad4d2188c` |
| Binding master readiness | `e440c5855732d5d8f5d634e3cc1359c010cc5ed3` |
| Runtime request | Codex `gpt-5.6-sol`, `model_reasoning_effort="xhigh"`; recorded as user-specified validation identity |
| Issue state at entry | `ready for plan validation`; preserved labels: `risk:high`, `tdd`, `security:S3`, `shared-core`, `data-integrity` |
| Fixture authority | [Issue #6 owner clarification](https://github.com/khanhvg/ai-ready-data-platform/issues/6#issuecomment-5027528463) explicitly permits only `evidence-v1.json`, `manifest.json` and `invalid/**` under the promotion-trust fixture root |

Before any edit, local `HEAD`, upstream tracking ref and live remote branch all equalled the planner artifact SHA. Discovery, integration and master-readiness SHAs exist and are ancestors. The worktree was clean. This satisfied the immutable-input STOP gate.

The validator read the complete issue #6 body and all six comments; issue #7 body, all comments and the issue #7 validation-SHA fixture handoff; every issue #6 discovery and planning artifact; binding master P1, execution-authority, architecture, security, audit and traceability artifacts; and current repository generator, dbt, Rill, Airflow, curated, Iceberg, OpenMetadata, Make and ignore-rule sources.

## Method and evidence classes

The full tier used all four required perspectives: implementation feasibility, architecture/data integrity, operations/recovery and security/QA. The sample below contains 15 high-risk claims per phase, 120 total. Results mean:

- `VRF-REPO`: independently verified against immutable repository bytes or a disposable archive.
- `VRF-TOOL`: independently verified from primary package/tool metadata or a disposable tool probe.
- `FIXED`: a correctable planning defect was confirmed and repaired only inside this plan directory.
- `GATE`: honest future implementation/readiness/merge evidence is still required; the plan names a test, failure and rollback.

## High-risk validation sample — 120 claims

### Phase 1 — immutable anchors and tests-first harness

| ID | Perspective | Claim checked | Evidence / result |
|---|---|---|---|
| P1-01 | Operations | Branch, remote and ancestry are exact before edits | `rev-parse`, `merge-base`, live `ls-remote`; `VRF-REPO` |
| P1-02 | Integrity | `small`/`42` generates 18 CSVs and 6,812 rows | Disposable archive run; `VRF-REPO` |
| P1-03 | Integrity | Every listed CSV byte hash matches the matrix | All 18 recomputed; `VRF-REPO` |
| P1-04 | Integrity | Generator domain is 2025-07-01 through 2026-06-30 | Generated manifest; `VRF-REPO` |
| P1-05 | Integrity | Configured anomaly rates and observed counts are separate | Manifest targets/observed objects; `VRF-REPO` |
| P1-06 | Integrity | PO-item orphan is configured yet observed zero | Manifest and dbt test configuration; `VRF-REPO` |
| P1-07 | Feasibility | dbt has 18 sources, 51 models, 141 generic tests and one singular file | Manifest plus source tree; `VRF-REPO` |
| P1-08 | Integrity | Model layers are 18 staging, 6 ephemeral, 16 core and 11 marts | dbt manifest/source inventory; `VRF-REPO` |
| P1-09 | QA | Build is 179 pass, 7 warn, 0 error, 186 total | Corrected-lock disposable build; `VRF-REPO` |
| P1-10 | QA | Nine warning-configured IDs remain distinct from seven observed warns/two passes | YAML plus run results; `VRF-REPO` |
| P1-11 | Integrity | Actual 11 mart IDs, rows and every listed content hash match, including three corrected shorthand names | Exact headered-LF-CSV reproduction; `VRF-REPO` |
| P1-12 | Integrity | Rill expressions preserve exact ratio/weighting semantics | All 11 metrics YAML files; `VRF-REPO` |
| P1-13 | Feasibility | Airflow is six default tasks plus two optional publish tasks | DAG source; `VRF-REPO` |
| P1-14 | Security | Current Airflow callables omit/override private raw/warehouse/export/profile paths | Callable source; narrow exception is justified; `VRF-REPO` |
| P1-15 | QA | Normative 11-mart summary is executable JCS SHA `4b8a16…`; opaque discovery `8ffb3e…` is contextual only | Projection gap corrected; `FIXED` |

### Phase 2 — dependency baseline and hashed lock

| ID | Perspective | Claim checked | Evidence / result |
|---|---|---|---|
| P2-01 | Feasibility | Host proof is CPython 3.12.3 on Darwin arm64 with pip 26.1.1 | Runtime probe; `VRF-TOOL` |
| P2-02 | Feasibility | dbt-core 1.11.12 supports Python 3.12 and adapters 1.24.4 | PyPI release JSON; `VRF-TOOL` |
| P2-03 | Feasibility | dbt-duckdb 1.10.1 accepts core/adapters below 2 and DuckDB at least 1.0 | PyPI release JSON; `VRF-TOOL` |
| P2-04 | Feasibility | DuckDB 1.5.4 has a CPython-3.12 macOS-arm64 wheel | PyPI file SHA `ff96d2…`; `VRF-TOOL` |
| P2-05 | Feasibility | Faker 40.28.1 and RFC 8785 0.1.4 have compatible pure wheels | PyPI release JSON; `VRF-TOOL` |
| P2-06 | Integrity | Original six-root 837-line candidate omits required `rfc8785` | Reproduced SHA `042ca2…`; import contract impossible; `FIXED` |
| P2-07 | Integrity | Corrected seven-root candidate has 56 locked distributions and 840 lines | Two compiles; `VRF-TOOL` |
| P2-08 | Integrity | Generic corrected lock SHA is `08ad36…` | Two byte-identical compiles; `VRF-TOOL` |
| P2-09 | Integrity | Repository-relative output-header lock SHA is `f41c72…` | Exact command/header projection; `VRF-TOOL` |
| P2-10 | Security | Compiler lock is 40 lines, eight wheels and repository-relative SHA `ece1d2…` | Recompiled and hash-checked; `VRF-TOOL` |
| P2-11 | Integrity | Tool freeze claim must use exact sorted-lines algorithm and SHA `432758…` | Empty-cache tool install; prior unexplained hash corrected; `FIXED` |
| P2-12 | Integrity | Two application installs pass `pip check`, required imports and freeze SHA `cdb87e…` | Separate venv/cache roots; `VRF-TOOL` |
| P2-13 | Feasibility | Corrected lock runs the full current pipeline unchanged | 18/6,812; 179/7/0/186; 11 marts; `VRF-REPO` |
| P2-14 | Security | Wrong Python/platform, sdist, missing hash, ambient index or resolver upgrade fails before generation | Explicit parser/preflight cases; `GATE` |
| P2-15 | Operations | Two complete C1 archive runs, exact rollback and no runtime resolution remain mandatory | Phase 2/8 acceptance; `GATE` |

### Phase 3 — private workspace and provenance envelope

| ID | Perspective | Claim checked | Evidence / result |
|---|---|---|---|
| P3-01 | Security | Workspace and evidence roots are disjoint and repository-relative | S3 disposition; `VRF-REPO` |
| P3-02 | Security | Public commands cannot accept arbitrary run paths or IDs | Allocation contract; `GATE` |
| P3-03 | Security | Absolute, parent, empty, NUL and normalization-ambiguous paths reject before allocation | Negative matrix; `GATE` |
| P3-04 | Security | Existing components open no-follow and retain directory descriptors | Required algorithm and FS STOP; `GATE` |
| P3-05 | Security | Exclusive run creation plus nonce marker prevents foreign-root reuse | Allocation steps and mutations; `GATE` |
| P3-06 | Security | Symlink, hardlink, FIFO, device and socket entries cannot become owned output | Negative matrix; `GATE` |
| P3-07 | Security | TOCTOU swaps either remain bound to opened inode or fail typed | Interleaving tests; `GATE` |
| P3-08 | Operations | Writes use exclusive temp-in-destination, fsync, atomic rename and directory fsync | Publication rule; `GATE` |
| P3-09 | Operations | Concurrent publication uses an exclusive lease and never auto-breaks stale state | Lease rule; `GATE` |
| P3-10 | Security | Child environment is allow-listed and excludes credentials, proxy and `PYTHONPATH` | Environment contract; `GATE` |
| P3-11 | Security | Evidence scanning covers credentials, private paths/URLs and raw PII-like identifiers | Scanner contract and canaries; `GATE` |
| P3-12 | Operations | Per-stream, per-run and time bounds have typed non-zero failures | 2 MiB/2 MiB/16 MiB plus TERM/KILL/reap; `GATE` |
| P3-13 | Operations | `golden-clean` never calls current root `clean` or broadly deletes | Cleanup contract; `GATE` |
| P3-14 | Recovery | Forged marker, renamed parent or cleanup symlink preserves the target and fails | Cleanup negative tests; `GATE` |
| P3-15 | Security | Generalized privileged-runner containment remains I5-04 | Threat-model boundary; `VRF-REPO` |

### Phase 4 — data and evidence contract schemas

| ID | Perspective | Claim checked | Evidence / result |
|---|---|---|---|
| P4-01 | Integrity | Raw bundle, semantic projection and envelope are non-interchangeable | Three-layer contract; `VRF-REPO` |
| P4-02 | Integrity | Semantic projection has no allowed drift | Contract and phase gate; `VRF-REPO` |
| P4-03 | Integrity | Raw normalized index permits exactly five JSON pointers | Exact pointer registry; `VRF-REPO` |
| P4-04 | Integrity | Schemas explicitly use JSON Schema 2020-12 `$schema` | Ambiguous wording corrected; `FIXED` |
| P4-05 | Feasibility | Version registry defines current/readable versions, schema hashes and migration edges | Registry plan; `GATE` |
| P4-06 | Recovery | v1 remains readable and synthetic v0/v2 exercise migration/rollback without fictional history | Migration test plan; `GATE` |
| P4-07 | Integrity | Only payload is canonicalized; sibling digest is excluded | Envelope shape; `VRF-REPO` |
| P4-08 | Integrity | `testedTreeSha`, external C2 and external M have different locations/meanings | Provenance contract; `VRF-REPO` |
| P4-09 | Security | Unkeyed SHA-256 is local integrity, not publisher authenticity | Explicit threat-model wording; `VRF-REPO` |
| P4-10 | QA | Duplicate decoded names reject before map conversion | Raw parser vector; independently exercised; `VRF-TOOL` |
| P4-11 | QA | NaN, positive/negative Infinity and lone surrogates reject | Parser/library probes; `VRF-TOOL` |
| P4-12 | Integrity | Numeric negative zero becomes `0`; business `-0.00` rejects by schema | RFC library plus schema rule; `VRF-TOOL` |
| P4-13 | Integrity | Canonical key order is raw UTF-16 and Unicode normalization is forbidden | Mandatory vectors; independently exercised; `VRF-TOOL` |
| P4-14 | Operations | dbt build evidence is captured before docs into a separate immutable raw path | Ordering contract and mutation test; `GATE` |
| P4-15 | QA | Missing tool/schema/evidence emits fail or non-zero stderr, never skip | FitnessResult contract; `GATE` |

### Phase 5 — curated release and promotion-trust handoff

| ID | Perspective | Claim checked | Evidence / result |
|---|---|---|---|
| P5-01 | Integrity | Curated allow-list is exactly the 11 current mart IDs in order | `lake/curated_assets.json`; `VRF-REPO` |
| P5-02 | Integrity | All release entries share release/data-run/tree/input/contract/engine identity | Schema semantic contract; `GATE` |
| P5-03 | Integrity | Current pointer identifies one complete immutable manifest | Separate pointer contract; `GATE` |
| P5-04 | QA | Missing, duplicate, extra or mixed-generation assets reject | Mutation matrix; `GATE` |
| P5-05 | Authority | I5-01 defines schema only; publisher stays I5-07 | Issue/master ownership; `VRF-REPO` |
| P5-06 | Integrity | Current publisher is sequential drop/create and is only characterized as a gap | Publisher source; `VRF-REPO` |
| P5-07 | Authority | Exact fixture paths match the owner clarification | Issue comment and handoff; `VRF-REPO` |
| P5-08 | Integrity | Fixture contains four separate source grains and no shared join key | Contract handoff; `VRF-REPO` |
| P5-09 | Integrity | Promotion, fulfillment, returns and DQ rows total exactly 89 | 7 + 25 + 47 + 10; `VRF-REPO` |
| P5-10 | Integrity | Fixture DQ source uses actual mart values 879/9, not generator anomaly values 1/10 | Disposable DuckDB query exposed conflation; `FIXED` |
| P5-11 | QA | Headline sufficiency is a controlled failure | `PROMOTION_HEADLINE_INSUFFICIENT`; `GATE` |
| P5-12 | Integrity | Only conclusion is `insufficient-evidence` for `no-common-grain` | Contract and issue #7 handoff; `VRF-REPO` |
| P5-13 | Security | Raw rows, IDs, secrets, paths, URLs, score, ADR and causal attribution are forbidden | Closed fields/scanner/mutations; `GATE` |
| P5-14 | Integrity | Tracked negative fixtures are limited to six raw-parser cases | Exact authorized paths; `VRF-REPO` |
| P5-15 | Recovery | Any fixture/contract/schema/tree/digest change invalidates issue #7 samples and scores | Merge gate and rollback rule; `GATE` |

### Phase 6 — architecture source validation and deterministic render

| ID | Perspective | Claim checked | Evidence / result |
|---|---|---|---|
| P6-01 | Feasibility | LikeC4 1.59.1 requires Node at least 22.22.3 and is MIT | npm metadata/release; `VRF-TOOL` |
| P6-02 | Feasibility | hpcc wasm Graphviz 1.22.2 is Apache-2.0 and embeds Graphviz 15.0.0 | npm metadata/runtime probe; `VRF-TOOL` |
| P6-03 | Integrity | Node 22.22.3 tar.xz hashes for Darwin/Linux tuples match official archive | Node SHASUMS; `VRF-TOOL` |
| P6-04 | Integrity | Exact package document SHA is `5cebd6…` | Recreated bytes; `VRF-TOOL` |
| P6-05 | Integrity | npm lock is lockfile v3, 119 records and SHA `7a56d8…` | Empty private reproduction; `VRF-TOOL` |
| P6-06 | Security | Ignored architecture lock needs exact-path force-add; `.gitignore` stays protected | Ignore probe; gap corrected; `FIXED` |
| P6-07 | Feasibility | `format --check` is supported | Installed CLI help and source probe; `VRF-TOOL` |
| P6-08 | Feasibility | `validate --json` is supported and invalid references exit 1 | Installed CLI probe; `VRF-TOOL` |
| P6-09 | Feasibility | `export json --skip-layout --pretty` is supported | Six-view source probe; `VRF-TOOL` |
| P6-10 | Feasibility | `gen dot -o` emits exactly six DOT files | Six-view source probe; `VRF-TOOL` |
| P6-11 | Integrity | Two DOT generations and wasm SVG renders are byte-identical | Disposable six-view probe; `VRF-TOOL` |
| P6-12 | Integrity | External IDs map to exactly six underscore-safe LikeC4 keys | Computed JSON key set; `VRF-TOOL` |
| P6-13 | Integrity | Semantic text is generated from computed JSON, never SVG | Toolchain contract; `GATE` |
| P6-14 | Security | SVG normalization removes only declaration/DTD/generator comments and preserves semantics | Gap tightened with semantic mutations; `FIXED` |
| P6-15 | Authority | No Java/Structurizr/browser/native fallback; later I5-06 is additions-only | Tool/scope STOP and lease; `VRF-REPO` |

### Phase 7 — Make registry and Airflow seam

| ID | Perspective | Claim checked | Evidence / result |
|---|---|---|---|
| P7-01 | Integrity | Current Makefile has exactly 15 unique targets | Source parse; `VRF-REPO` |
| P7-02 | Authority | Master owner table has 14 owners and sums to 54 targets | Plan/master cross-check; `VRF-REPO` |
| P7-03 | Authority | I5-01 owns exactly seven future commands | Registry table; `VRF-REPO` |
| P7-04 | Integrity | None of the seven future target definitions exists at input | Make parse; `VRF-REPO` |
| P7-05 | Authority | Later 47 commands are declarations, not recipes | Phase contract; `GATE` |
| P7-06 | Feasibility | Root change is one include/help seam with recipes in `i5-01.mk` | File inventory; `GATE` |
| P7-07 | Recovery | Root seam and issue fragment roll back together | Regression/rollback contract; `GATE` |
| P7-08 | Security | Golden targets never invoke current broad `clean` | Mutation and command graph test; `GATE` |
| P7-09 | Integrity | Help reports existing/implemented/future states honestly | Registry evidence contract; `GATE` |
| P7-10 | QA | Duplicate command, owner, recipe or 53/55 registry fails | Test matrix; `GATE` |
| P7-11 | Feasibility | Generator already supports explicit `--out` | Source probe; `VRF-REPO` |
| P7-12 | Feasibility | Loader/export already support explicit raw/warehouse/export paths | Source probe; `VRF-REPO` |
| P7-13 | Feasibility | Airflow callable forwarding is absent/overridden at input | Source probe; `VRF-REPO` |
| P7-14 | Authority | Conditional Airflow diff is limited to path forwarding; DAG and `_run` containment stay out | Handoff/phase scope; `VRF-REPO` |
| P7-15 | QA | Missing required tool/evidence is non-zero with FitnessResult, never skip | Command contract; `GATE` |

### Phase 8 — two-run evidence, rollback and merge handoff

| ID | Perspective | Claim checked | Evidence / result |
|---|---|---|---|
| P8-01 | Authority | Validation and fresh readiness precede implementation | Incorrect ordering text corrected; `FIXED` |
| P8-02 | Authority | Future implementation input is readiness output, not discovery/planner SHA | Provenance text corrected; `FIXED` |
| P8-03 | Integrity | `baselineSourceSha` and future C1 `testedTreeSha` are distinct | Golden matrix corrected; `FIXED` |
| P8-04 | Operations | A/B use separate archives, homes, venvs, caches, data and evidence | Phase requirement; `GATE` |
| P8-05 | Operations | Each run has a 300-second monotonic guard and pair has 600 seconds | Runtime plan; `GATE` |
| P8-06 | Security | Timeout kills/reaps process group and preserves bounded failure evidence | S3/runtime contract; `GATE` |
| P8-07 | Integrity | Projection equality is exact; raw drift is only five pointers | Comparison contract; `GATE` |
| P8-08 | Recovery | Lock, registry/readers, pointer model, Make and architecture rollback are rehearsed | Phase test plan; `GATE` |
| P8-09 | Security | Protected hash for root release manifest is `f9037b5d…` | Repository bytes; wrong plan hash corrected; `FIXED` |
| P8-10 | Security | Protected/ignored/unrelated sentinels and credential/private-path scans gate completion | Phase requirement; `GATE` |
| P8-11 | Integrity | C1 contains producer/contracts/readers/tests and is run twice | Non-recursive handoff; `GATE` |
| P8-12 | Integrity | C2 adds only authorized fixture/attestation bytes and never contains itself | C1/C2 protocol; `GATE` |
| P8-13 | Authority | M is externally observed; squash merge uses host record plus exact blob equality | Issue #7 handoff; `GATE` |
| P8-14 | Integrity | Issue #7 verifies exactly four merged paths/digests before scoring | Issue #7 validation-SHA handoff; `VRF-REPO` |
| P8-15 | Authority | Human pre-merge remains outstanding; no plan validation action merges or creates a PR | Scope and success criterion; `VRF-REPO` |

## Findings and exact fixes

| Finding | Severity | Evidence | Exact bounded fix | State |
|---|---|---|---|---|
| VAL-01 — accepted Python candidate omitted required canonicalizer | High | Six-root candidate reproduced at 837 lines/`042ca2…`; no `rfc8785` entry while phase 4 imports it | Added direct `rfc8785==0.1.4`; corrected graph to 56, line count to 840, fingerprints to `08ad36…`/`f41c72…`, install freeze to `cdb87e…`; retained old fingerprint only as superseded provenance | Resolved |
| VAL-02 — implementation/discovery/tested-tree identities were conflated | High | Plan called discovery SHA the exact implementation input and retail identity implied the same SHA was `testedTreeSha` | Defined discovery, planner, readiness output and future C1 separately; added `baselineSourceSha`; kept C1/C2/M non-recursive | Resolved |
| VAL-03 — protected release-manifest SHA was false | High | Recomputed SHA-256 is `f9037b5d…`, not `f9037b714…` | Corrected the handoff and master PH-H12 crosswalk | Resolved |
| VAL-04 — architecture package lock is ignored without staging rule | Medium | `git check-ignore -v requirements/architecture/package-lock.json` resolves to repository `package-lock.json` rule | Required exact-path force-add only after hash verification; `.gitignore` remains protected | Resolved |
| VAL-05 — SVG normalizer could be read as semantically broad | Medium | Original prose named removal/normalization but not a closed semantic-preservation list | Closed removals/rewrites and added ID/text/style/path/geometry mutation obligations | Resolved |
| VAL-06 — readiness ordering in phase 8 was backward | Medium | Phase 8 placed validation/readiness after future implementation | Restored initial validation/readiness before implementation and separate post-implementation gates | Resolved |
| VAL-07 — master PH/authority trace was implicit | Medium | F/SC trace was complete but PH-C01/C02/C06/C10 and PH-H02/H11/H12 were not ID-addressable | Added binding PH and authority crosswalk with owner/path/test/evidence/rollback/STOP | Resolved |
| VAL-08 — JSON Schema dialect wording omitted the `$schema` keyword | Low | Canonicalization contract stated only the dialect URL | Made the exact `$schema` declaration executable | Resolved |
| VAL-09 — fixture data-quality values came from the wrong evidence layer | High | Actual `mart_data_quality` rows are null-promotion 879 and invalid-status 9; the plan specified generator observations 1 and 10 while claiming all 89 mart rows | Corrected fixture expectations to 879/9 and explicitly retained generator 1/10 only in the anomaly projection | Resolved |
| VAL-10 — canonical 11-mart summary bytes were unspecified | Medium | All 11 content hashes independently reproduce with the discovered exact CSV serializer, but discovery retained only aggregate hash `8ffb3e…`, not its source projection | Defined the exact content serializer and normative JCS summary with SHA `4b8a16…`; retained `8ffb3e…` only as contextual legacy evidence | Resolved |

No Critical finding and no unresolved High finding remain. No correction changes product behavior, expands ownership or edits raw discovery history.

## External/tool verification

- Python compatibility and hashes came from primary PyPI release JSON for [dbt-core 1.11.12](https://pypi.org/pypi/dbt-core/1.11.12/json), [dbt-adapters 1.24.4](https://pypi.org/pypi/dbt-adapters/1.24.4/json), [dbt-duckdb 1.10.1](https://pypi.org/pypi/dbt-duckdb/1.10.1/json), [DuckDB 1.5.4](https://pypi.org/pypi/duckdb/1.5.4/json), [Faker 40.28.1](https://pypi.org/pypi/Faker/40.28.1/json), [pip-tools 7.6.0](https://pypi.org/pypi/pip-tools/7.6.0/json) and [rfc8785 0.1.4](https://pypi.org/pypi/rfc8785/0.1.4/json).
- Hash-only policy matches pip’s [secure-install guidance](https://pip.pypa.io/en/stable/topics/secure-installs/): all requirements pinned/hashed, binary-only and no dependency resolution during install.
- Architecture versions/integrities/licenses came from the npm registry entries for [LikeC4 1.59.1](https://registry.npmjs.org/likec4/1.59.1) and [hpcc wasm Graphviz 1.22.2](https://registry.npmjs.org/@hpcc-js%2fwasm-graphviz/1.22.2), official [LikeC4 CLI documentation](https://likec4.dev/tooling/cli/), installed CLI help, and Node’s [22.22.3 SHASUMS](https://nodejs.org/dist/v22.22.3/SHASUMS256.txt).
- Canonicalization behavior was checked against [RFC 8785](https://www.rfc-editor.org/rfc/rfc8785.html), [I-JSON RFC 7493](https://www.rfc-editor.org/rfc/rfc7493.html) and [JSON Schema 2020-12](https://json-schema.org/draft/2020-12/json-schema-core).

## Commands and results

| Command family | Result |
|---|---|
| `git rev-parse`, `git merge-base --is-ancestor`, live `git ls-remote` | Exact input and ancestry PASS before edits |
| `ck plan status plans/260721-006-freeze-golden-baseline/plan.md` | Pending, 0/8, correct branch/tags |
| Two `pip-compile` runs from exact pip-tools 7.6.0 | Corrected locks byte-identical; 840 lines; SHA `08ad36…` |
| Two `pip install --require-hashes --only-binary=:all: --no-deps` runs | `pip check`, imports and freeze SHA `cdb87e…` PASS |
| Disposable corrected-lock generator/load/dbt/export run | 18/6,812; 179/7/0/186; 51/141/18; 11 exports; PASS |
| npm lock reproduction and `npm ci --ignore-scripts` | Package SHA `5cebd6…`; 119 records; lock SHA `7a56d8…`; PASS |
| LikeC4 `format --check`, `validate --json`, `export json --skip-layout --pretty`, `gen dot` | Six computed IDs/DOTs; invalid reference exits 1; PASS |
| hpcc `Graphviz.load()` and two six-view SVG renders | Graphviz 15.0.0; DOT/SVG bytes equal; PASS |
| Structure/frontmatter/DAG/link/anchor/ID/command/ownership/trace/version/hash sweeps | Eight phases and DAG PASS; F=12, SC=15, owners=54, issue targets=7; PASS after report link creation |
| `git diff --check`, changed-path, protected-hash and sensitive-content checks | Required final publication gate; PASS recorded only on the exact staged diff |

## Whole-plan consistency

- Eight phases are numbered once, all frontmatter is parseable and dependencies are acyclic: `1→2→3→4`, then `5` and `6`, then `7→8`.
- All local Markdown links and anchors resolve after this report is present.
- Authority matches issue #6: exact fixture clarification; evidence-core and three named data contracts; dependency and six-view paths; one Make include/help seam; conditional Airflow path forwarding only. No I5-02/I5-03/I5-04/I5-06/I5-07/I5-14 or cloud implementation is absorbed.
- The corrected dependency versions, counts, commands and hashes agree across plan, phase 2, decision and handoff artifacts. The old six-root hashes occur only in an explicitly superseded-provenance paragraph.
- The architecture versions, package/lock hashes, six IDs, supported commands, semantic text rule, SVG preservation rule and later additions-only lease agree across plan, phase 6 and toolchain decision.
- Generator, dbt, warning, mart, Rill, Airflow, curated, Iceberg/OpenMetadata and historical/current anchors agree across the golden matrix, phases and fixture handoff. Generator anomaly values 1/10 and mart DQ values 879/9 are deliberately separate.
- Raw/projection/envelope, allowed drift, JCS/I-JSON, version registry, local integrity, C1/C2/M and four-path issue #7 handoff are non-recursive and mutually consistent.
- Every F-01…F-12 and SC-01…SC-15 has exactly one complete trace row. The added master crosswalk retains relevant PH and authority items.
- All commands are explicitly future commands; none is misrepresented as existing. Missing required tools/evidence fail, and every phase keeps tests-before, implementation/refactor, tests-after, regression/evidence and rollback obligations.

## Remaining honest gates

1. A separate fresh readiness audit must review this validation output and publish the exact remotely observed `IMPLEMENTATION_INPUT_SHA`; until then cook remains prohibited.
2. Implementation must create the reviewed locks/contracts/tests/sources only inside its allow-list and prove the complete changed-path/protected-state manifest.
3. C1 must pass two genuinely independent, empty-cache, full `small`/`42` runs under 300 seconds each and 600 seconds combined. This validation’s two installs and one compatibility run do not substitute for that release evidence.
4. Architecture implementation must reproduce the pinned lock, validate exactly six real project views, prove second-install/two-render determinism and complete any claimed Linux compatibility lane; no current Linux byte-equality claim is made.
5. C2 may add only the authorized fixture bytes after C1 evidence. Human pre-merge review remains required. No PR/merge is authorized here.
6. Issue #7 remains read-only and unscored until remote M and exact equality of the four merged path blobs/digests are externally verified.

## Decision

The corrected plan is internally consistent, executable within its stated boundaries and explicit about every evidence that can exist only during implementation, readiness or post-merge handoff. The resolved defects were planning-document defects, not product changes. The next state is `ready for plan audit`.

`VALIDATION_VERDICT=PASS`
