# Golden Evidence Decision Inputs

## Purpose

These are the repository-verified inputs the planner must turn into explicit decisions. They are not an implementation plan and confer no cook authority. Defaults below are recommendations; any different choice must preserve the binding issue/master contracts and explain its evidence and rollback.

## Decision matrix

| ID | Decision | Repository evidence | Recommended decision | Acceptance and rollback consequence |
|---|---|---|---|---|
| D-01 | Which Python/dbt dependency baseline is golden? | Direct pins resolve dbt-core 1.12.0/dbt-adapters 1.24.5 today, while historical full-flow evidence names dbt-core 1.11.12 and the master records adapters 1.24.4. | Prefer the historically proven 1.11.12-compatible set unless a focused compatibility matrix demonstrates that 1.12.0 is the intentionally accepted new baseline. Check in a complete transitive lock with hashes and interpreter/platform policy. | Two empty-cache installs must have one lock fingerprint and one semantic result. Retain the prior lock and reader; STOP cook while the baseline is unresolved. |
| D-02 | What is hashed versus retained raw? | Generator `generated_at`; dbt generated times, invocation IDs, elapsed times, and absolute paths; Airflow/runtime logs are volatile. Raw dbt results can be overwritten by docs. | Retain immutable raw artifacts, but hash a named deterministic comparison projection. Capture dbt build results before docs. Allowed drift must be an explicit JSON-pointer registry, not wildcard deletion. | A semantic mutation fails while only registered volatile fields differ across two runs. Rollback reads the previous projection version and retains both raw runs. |
| D-03 | What JSON canonicalization is normative? | Plain sorted JSON is underspecified for number/string edge cases and duplicate keys. | Use JSON Schema draft 2020-12 plus RFC 8785 JSON Canonicalization Scheme for the integrity payload. Enforce I-JSON: UTF-8, no duplicate object names, no NaN/Infinity, and a verified negative-zero rule. Use `additionalProperties: false` on stable contract boundaries and explicit extension objects where evolution is intended. | Canonicalization vectors and corrupt/duplicate/negative-zero fixtures must be machine-tested. The authoritative references are [JSON Schema 2020-12](https://json-schema.org/draft/2020-12), [RFC 8785](https://www.rfc-editor.org/info/rfc8785/), and its [verified errata](https://www.rfc-editor.org/errata/rfc8785/). |
| D-04 | How are evidence versions registered and read backward? | Master requires `fitness-result-v1`; future contracts and migrations need stable readers. | Add a machine-readable registry with contract ID, current write version, supported read versions, schema hash, canonicalization ID/version, producer command, migrations, and deprecation state. Writers emit only the current version; readers retain v1 support through at least the next promoted version. | Migration tests read a retained v1 fixture and round-trip supported projections. Rollback changes the current writer/pointer, never deletes prior evidence or schemas. |
| D-05 | How are integrity, provenance, and authenticity separated? | A file cannot contain the SHA of the commit/artifact that contains that same field without recursion. A local SHA-256 is not a signature. | Hash a canonical payload that excludes its own integrity envelope. Record `testedTreeSha` in the artifact, `attestationCommitSha` in a child/external publication record, and `mergeOrTagSha` only after the host observes it. Label SHA-256 as corruption/tamper detection, not authorship. Hosted signing remains I5-14. | Recompute payload/schema/artifact hashes; corrupt copies fail. No self-containing exact-SHA requirement. Rollback points to the last valid attestation while preserving the failed one for forensics. |
| D-06 | What is the clean-run workspace and cleanup policy? | Root `clean` removes broad project paths and scans `.DS_Store`; generated paths, symlinks, concurrent runs, and ignored user fixtures are threats. | Allocate a private run root under an issue-owned artifact/workspace root using exclusive creation. Resolve every output beneath it; reject absolute, parent, symlink, and pre-existing foreign destinations. `golden-clean` accepts/derives one validated run ID and deletes only that owned run. | Adversarial path/symlink/concurrency/interruption tests; root release manifest, tracked `.gitkeep`, absent `docs/code-standards.md`, and unrelated ignored files remain unchanged. No broad `make clean` dependency. |
| D-07 | What runtime bound is meaningful? | Both independent clean runs completed in 155 seconds on the discovery host, with network bootstrap dominating. | Treat 300 seconds per clean run and 600 seconds for the required two-run comparison as an initial host-local hard bound, split into explicit bootstrap/generator/load/dbt/docs/export step budgets. The planner may adjust only with recorded platform evidence. Timeouts must terminate children and preserve bounded/redacted failure logs. | Evidence records per-step and total duration. A timeout is `fail`, never skip. Runtime is a reproducibility guard, not a cross-platform performance SLO. |
| D-08 | How should Make own the 54-command registry? | Master registry has exactly 54 targets; current Make has 15; issue #6 owns only seven future targets. | Make one root include/help change, load disjoint `mk/issue-5/*.mk` fragments, and keep the registry as machine-readable owner/target metadata. I5-01's fragment defines only its seven recipes. | Check uniqueness, declared owner, discoverability, and current-target behavior. Revert root include plus I5-01 fragment together. STOP on overlapping target ownership. |
| D-09 | How are the six architecture views rendered and leased? | The clean host lacks Java/Structurizr. Structurizr CLI does not directly export PNG/SVG; browser export introduces a different toolchain. | Pin a supported source validator/export plus a deterministic renderer and normalization policy, including artifact/tool hashes. Register exactly `C4-L0`, `C4-L1`, `C4-L2-LOCAL`, `C4-L3-RUNNER`, `DEP-LOCAL`, and `DYN-JOURNEY`. Serialize a later I5-06 lease for additions only. | All six source/render/text artifacts and manifest freshness hashes pass; missing tool fails. Preserve prior renders and source. STOP until the output-format/tool mismatch is resolved. |
| D-10 | How is historical evidence parsed? | `GH-3-full-flow-evidence.md` reports 2026-07-10 `demo-large`, 620,340 rows, dbt 1.11.12, `177/9`, and OM 11/45/130; current `small/42` is 6,812 rows and `179/7`. | Store evidence kind (`historical` or `current-run`), capture date, profile/seed, input identity, platform, tool versions, command, exact observations, parser version, and source hash. Never compare counts across contexts without an explicit rule. | Machine fixtures prove the parser does not relabel historical Markdown as a current attestation. Preserve source bytes for reparse/rollback. |
| D-11 | What does `CuratedReleaseManifest` guarantee? | Current Iceberg publication is sequential drop/create; issue #6 owns schema only and I5-07 owns atomic publication. | Require one common release/data-run/input/contract identity and exactly all 11 curated asset entries with schema hash, row count, canonical content checksum, immutable staged locator, and engine snapshot/version. Define a single atomically replaceable `current` pointer whose payload identifies one complete immutable manifest. | Schema/negative fixtures reject missing, duplicate, extra, or mixed-generation assets. I5-07 must stage, validate, switch, reconcile, and roll back pointer. I5-01 must not edit the current publisher. |
| D-12 | What may `promotion-trust-v1` claim? | Current promotion, fulfillment, returns, and data-quality marts have different grains; no governed causal/campaign attribution exists. | Declare each mart/grain and permit only independent aggregate assertions. Publish sanitized aggregates with no raw customer/order IDs, secrets, absolute paths, credentials, or causal join. Any future attribution requires an additive I5-07 data product. | Negative tests reject cross-grain joins and attribution language. Rollback invalidates the fixture/version; it does not rewrite historical evidence. |
| D-13 | When may issue #7 score? | Issue #7 requires a real tracked fixture and merged exact-SHA provenance; issue #6's fixture-path authority is currently missing. | Before merge, allow only unscored preview and common assertion/test development. After explicit path authority, issue #6 publishes the fixture; after merge, issue #7 records the externally observed merge SHA and may score. | Scorecard/ADR checks fail on provisional, dirty, unmerged, hash-mismatched, or self-referential fixtures. Issue #6 never emits the framework score or ADR. |

## Canonical evidence layers

Use three distinct layers:

1. **Raw run bundle** — complete command/status/stdout/stderr/tool artifacts with bounded size, timestamps, timings, and sanitized paths. It is retained for diagnosis and is not expected to be byte-identical.
2. **Deterministic comparison projection** — only contract-relevant content, canonicalized with a registered algorithm and explicit allowed-drift pointers. This is the two-run determinism oracle.
3. **Integrity/provenance envelope** — schema/canonicalization IDs, payload/artifact hashes, tested tree SHA, producer/tool/lock identities, and externally completed attestation/merge records.

Suggested explicit allowed-drift pointers for v1 are limited to run ID, start/end timestamps, duration, and an explicitly sanitized temporary workspace locator. Tool versions, lock hash, input SHA, profile/seed, command, result statuses, model/test IDs, schema/lineage/semantic hashes, row counts, anomaly observations, and artifact hashes are not allowed to drift.

## `fitness-result-v1` minimum stable boundary

The planner should bind at least:

- `schemaVersion`, `fitnessId`, `runId`, `status`, and required/optional classification.
- `testedTreeSha`, dirty-base decision, profile/seed, host/platform class, producer command, lock hash, and tool versions.
- Started/finished/duration fields in the raw layer, not the deterministic equality set.
- Assertions with stable IDs, expected/actual summary, severity, and evidence locators.
- Artifact inventory with media type, byte length, schema/canonicalization ID where relevant, and SHA-256.
- Integrity envelope whose own digest field is excluded from its canonical payload by definition.
- Retention/rollback locator and redaction statement.

Allowed statuses remain `pass`, `fail`, `blocked-tbc`, and `not-run-optional`. Missing required tools, missing required evidence, timeout, dirty immutable input, schema failure, and drift are `fail`, never skip.

## Fixture publication boundary

If and only if F-05 authority is resolved, the issue #6 fixture may contain:

- the exact contract and evidence schema versions;
- sanitized aggregate results for the four grain-separated promotion-trust sources;
- stable assertion IDs and expected outcomes;
- tested tree SHA, lock/tool identity, canonical artifact hashes, and producer command;
- a manifest with retention/provenance metadata that does not recursively claim its own containing commit.

It must not contain raw PII-like customer/order rows, credentials, host usernames, absolute temporary paths, Docker/volume identifiers, private URLs, framework scores, ADR choices, or any campaign-attribution claim. The externally observed merge SHA belongs in the issue #7 handoff record after merge, not in a self-referential fixture generated before that merge.

## Planner resolution gates

The planner must not declare local cook ready until it can cite evidence for all of the following:

1. Explicit write authority for the tracked promotion fixture path.
2. Accepted dbt/Python lock baseline and complete hash strategy.
3. Supported, pinned architecture validation/render toolchain and artifact formats.
4. Canonicalization/schema/version registry with backward-read and corruption fixtures.
5. Scoped workspace, symlink/TOCTOU/atomic-write, runtime, and cleanup design.
6. Exact 18-table, dbt, mart, Rill, Airflow, curated-asset, Iceberg, and OpenMetadata contract projections.
7. Grain-honest promotion contract and issue #7 post-merge scoring barrier.
