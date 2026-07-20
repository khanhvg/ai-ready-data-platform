# Architecture toolchain decision

## Decision and truthful capability claim

Use this pinned, Java-free chain:

1. LikeC4 `1.59.1` validates `.c4` syntax/references and emits computed JSON plus DOT.
2. `@hpcc-js/wasm-graphviz` `1.22.2`, with embedded Graphviz `15.0.0`, renders DOT to SVG.
3. Issue-owned scripts under `scripts/golden/**` enforce the project’s C4 fitness profile, generate semantic text alternatives from computed JSON, normalize SVG, compute freshness hashes, and emit evidence.

Do **not** plan Structurizr CLI. The clean host has no usable Java/Structurizr installation, and [Structurizr’s official export documentation](https://docs.structurizr.com/cli/export) states that the CLI does not export PNG/SVG; those formats use browser/Puppeteer automation. Do not use LikeC4 PNG/JPEG export either, because [LikeC4 CLI documentation](https://likec4.dev/tooling/cli/) requires Playwright. The selected chain makes no Structurizr compatibility/export claim.

LikeC4 validates its own language and model but does not enforce strict C4 abstraction levels. Therefore the issue-owned computed-model fitness layer is required, not optional.

## Exact tool lock, versions, integrity and license

Future `requirements/architecture/package.json` is exactly:

```json
{
  "name": "ai-ready-data-platform-architecture-toolchain",
  "version": "1.0.0",
  "private": true,
  "engines": {
    "node": "22.22.3",
    "npm": "10.9.8"
  },
  "devDependencies": {
    "@hpcc-js/wasm-graphviz": "1.22.2",
    "likec4": "1.59.1"
  }
}
```

The lock is npm `package-lock.json`, `lockfileVersion: 3`, generated only with npm 10.9.8. The disposable reviewed decision candidate contains 119 locked package records, including platform-optionals:

| Artifact | SHA-256 / integrity |
|---|---|
| exact package document above | `5cebd6d09ecef1334a492b871e388049392b6c0f6c9738873438b88958bd475d` |
| candidate `package-lock.json` | `7a56d803a47454023f40a04bcdb3b037f4ab2c2a05321292ad3b7f7225c2118c` |
| LikeC4 1.59.1 | npm `sha512-uYbh3EnVlhL+LL2eolASHPcePvjduMazI28tzfyDXTSxkXSPT0hv5y05MhEZacoa//RT4cuxFGZyD473kFP+WQ==`; tag commit `d583a1c46eff4cfbc3b6ae9a6fb4635c8ff35f42` |
| hpcc wasm Graphviz 1.22.2 | npm `sha512-qofkC1bxiQKljs95A/7a0j3mvjEdTBiDPq2W6Eh3mJGOLJ+CEtLVe5pFtzf+FZhYW/V9p9hssS1TRl9PxoV8Sw==`; tag commit `8b86e2f83cc7344aca44fb3d8aa29a227358c5c4` |

LikeC4 is MIT ([release](https://github.com/likec4/likec4/releases/tag/v1.59.1), [license](https://github.com/likec4/likec4/blob/v1.59.1/LICENSE)). The hpcc package is Apache-2.0 ([official wrapper documentation](https://github.com/hpcc-systems/hpcc-js-wasm/tree/main/packages/graphviz)); embedded Graphviz is EPL-2.0 ([license](https://graphviz.org/license/)). Retain all applicable notices.

Exact Node 22.22.3 official tar.xz SHA-256 values from the [signed release archive](https://nodejs.org/en/download/archive/v22.22.3):

| Tuple | SHA-256 |
|---|---|
| darwin-arm64 | `753c1629e168cc788ccc46ab61e0b35549fce08c07f82fcd3bb0d41f7fb01e7b` |
| linux-arm64 | `1c4a9933a5e45bc88f54f70b5f91232c127ec49f1a5989d23fb85824c7adf9b7` |
| linux-x64 | `2e5d13569282d016861fae7c8f935e741693c269101a5bebcf761a5376d1f99f` |

The initial golden render claim is darwin-arm64. Linux tuples are required compatibility runs; byte equality is an implementation gate, not a completed planner claim.

## Exact source/output layout

The master’s older `architecture/structurizr/**` path was a placeholder, not an obligation to mislabel a non-Structurizr format. The truthful issue-owned layout is:

```text
architecture/
  likec4/
    specification.c4
    model/
      people-and-systems.c4
      learning-platform.c4
      data-platform.c4
      local-deployment.c4
    views/
      C4-L0.c4
      C4-L1.c4
      C4-L2-LOCAL.c4
      C4-L3-RUNNER.c4
      DEP-LOCAL.c4
      DYN-JOURNEY.c4
    view-manifest.yaml
  rendered/
    C4-L0.svg
    C4-L0.txt
    C4-L1.svg
    C4-L1.txt
    C4-L2-LOCAL.svg
    C4-L2-LOCAL.txt
    C4-L3-RUNNER.svg
    C4-L3-RUNNER.txt
    DEP-LOCAL.svg
    DEP-LOCAL.txt
    DYN-JOURNEY.svg
    DYN-JOURNEY.txt
    render-manifest.json
requirements/architecture/package.json
requirements/architecture/package-lock.json
scripts/golden/architecture-check*
scripts/golden/architecture-render*
scripts/golden/architecture-text*
scripts/golden/architecture-normalize*
```

LikeC4 identifiers cannot contain the required hyphens. `view-manifest.yaml` is the binding external-to-internal mapping:

| External stable ID | LikeC4 key |
|---|---|
| `C4-L0` | `index` |
| `C4-L1` | `c4_l1` |
| `C4-L2-LOCAL` | `c4_l2_local` |
| `C4-L3-RUNNER` | `c4_l3_runner` |
| `DEP-LOCAL` | `dep_local` |
| `DYN-JOURNEY` | `dyn_journey` |

Explicitly declaring `view index` for `C4-L0` suppresses LikeC4’s implicit extra index. The computed key set must equal those six values; extra/later IDs fail.

## Bootstrap and planned commands

The public registry owns only `make architecture-check` and `make architecture-render`. Their internal bootstrap verifies the exact Node/npm versions, package/lock hashes and platform digest, allocates a new issue-private directory, and runs:

```bash
npm ci --prefix "$RUN_ROOT/toolchain" --cache "$RUN_ROOT/npm-cache" --ignore-scripts --no-audit --no-fund
```

The wrapper must never invoke `npx`, an unpinned resolver, a global tool, lifecycle scripts, Java, a browser, or native Graphviz. It copies the exact package/renderer files into the private root, then executes:

```bash
"$TOOL_ROOT/node_modules/.bin/likec4" format --check architecture/likec4
"$TOOL_ROOT/node_modules/.bin/likec4" validate --json architecture/likec4
"$TOOL_ROOT/node_modules/.bin/likec4" export json --skip-layout --pretty -o "$RUN_ROOT/model.json" architecture/likec4
"$TOOL_ROOT/node_modules/.bin/likec4" gen dot -o "$RUN_ROOT/dot" architecture/likec4
node "$TOOL_ROOT/architecture-render.mjs" --manifest architecture/likec4/view-manifest.yaml --model "$RUN_ROOT/model.json" --dot-dir "$RUN_ROOT/dot" --out-dir "$RUN_ROOT/rendered"
```

`$RUN_ROOT/dot` must be newly created. The probe established that `likec4 gen dot -o EXISTING_DIR` leaves stale files and could preserve an obsolete view. The renderer calls `Graphviz.load()` followed by `graphviz.layout(dotSource, 'svg', 'dot')`.

`architecture-render` renders all six into a private staging directory and atomically replaces committed outputs only after the complete set validates and two staged renders are byte-identical. `architecture-check` regenerates privately and byte-compares without modifying committed output.

## Minimum-useful-view fitness contract

The project fitness wrapper reads computed JSON plus the manifest and enforces:

| ID | Type | Audience / concern | Required content |
|---|---|---|---|
| C4-L0 | landscape/capability | product owner / business outcomes and external tools | learner, instructor/operator evolution, learning platform, retail platform, optional AWS/identity as future external context only |
| C4-L1 | system context | learner/security/maintainer / trust and ownership | browser, platform, data tools, hosted identity future, evidence boundary |
| C4-L2-LOCAL | container | developer/learner / actual local processes | portal modular monolith, isolated runner, progress/evidence repository, data adapters, Rill/Airflow/Iceberg/OpenMetadata |
| C4-L3-RUNNER | component | security/reviewer / privileged execution design only | BFF client, transport auth, policy chain, command registry, workspace manager, state/idempotency, verifier/evidence |
| DEP-LOCAL | deployment | learner/operator / 16-GiB runtime and trust | browser/host, loopback or Unix socket, read-only base, workspace/evidence, mutually exclusive Compose profiles |
| DYN-JOURNEY | dynamic | learner/product/security / complete first journey | load, start, run, controlled failure, diagnose, reset, verify, evidence, completion in source order |

This view is descriptive architecture, not implementation of the generalized runner. The wrapper also requires correct abstraction types/scope, unique stable elements, descriptions, technology/protocol for containers/components and inter-process relations, labelled unidirectional relations, a legend, no unexplained orphan, audience/concern/owner/scope, traceability IDs, and minimum required elements/relations. It rejects duplicate paths, undeclared references, later views (`DYN-PUBLISH`, AWS, AI), layout coordinates in semantics, and decorative containers.

`DYN-JOURNEY` uses ordinary ordered steps only; LikeC4 flow-control blocks are currently experimental. Avoid unsupported deployment-view `with` expressions/shared styles. C4 semantics follow the official [diagram overview](https://c4model.com/diagrams), [landscape](https://c4model.com/diagrams/system-landscape), [context](https://c4model.com/diagrams/system-context), [container](https://c4model.com/diagrams/container), [component](https://c4model.com/diagrams/component), [deployment](https://c4model.com/diagrams/deployment), [dynamic](https://c4model.com/diagrams/dynamic), and [notation/legend](https://c4model.com/diagrams/notation) guidance. LikeC4 feature authority is its [views](https://likec4.dev/dsl/views/), [dynamic view](https://likec4.dev/dsl/views/dynamic/), [deployment model](https://likec4.dev/dsl/deployment/model/), and [deployment view](https://likec4.dev/dsl/deployment/views/) documentation.

## Semantic text alternative

Each `.txt` is generated from `export json --skip-layout`, never scraped from SVG. It is UTF-8/NFC, LF-only, one final newline. It contains:

- external ID, title, view type, audience, concern, scope, owner and legend;
- elements sorted by stable ID: ID, C4 type/notation, title, description, technology, parent/scope;
- relations sorted by `(source,target,label,technology)`: source, target, label, technology/protocol;
- deployment hierarchy/instances for `DEP-LOCAL`;
- source-order numbered steps for `DYN-JOURNEY`;
- limitations and future-state annotations.

Absolute/private paths and coordinates are forbidden. Text semantics must hash the same computed projection as the manifest entry.

## Deterministic SVG normalization and freshness

The normalizer parses with external entities and network disabled; rejects scripts, `foreignObject`, external images/URLs and private/absolute paths; removes DTD and generator comments; normalizes NFC/LF; deterministically sorts attributes; injects stable `<title>`, `<desc>`, `role="img"`, and `aria-labelledby`; preserves geometry/child order; and emits one final newline. [Graphviz documents SVG output](https://graphviz.org/docs/outputs/svg/).

For each view, `render-manifest.json` records source-closure hashes, semantic manifest-row hash, computed semantic-projection hash, lock/package/renderer/normalizer hashes and tool versions, SVG/text byte lengths and SHA-256, review status, and evidence locator. JCS `renderInputSha256` covers source closure, semantic manifest fields, tool lock, renderer and normalization versions; it excludes generated hashes to prevent recursion.

Required failure codes:

```text
ARCH_NODE_VERSION_MISMATCH
ARCH_TOOL_LOCK_MISMATCH
ARCH_TOOL_MISSING
ARCH_SOURCE_INVALID
ARCH_VIEW_SET_MISMATCH
ARCH_C4_FITNESS_FAILED
ARCH_RENDER_FAILED
ARCH_TEXT_ALTERNATIVE_FAILED
ARCH_OUTPUT_STALE
ARCH_OUTPUT_NONDETERMINISTIC
```

No required failure becomes a skip or fallback.

## Disposable capability probe

On the planning darwin-arm64 host, a `/tmp` probe:

- validated scoped element, deployment and dynamic sources;
- made an undeclared target fail with structured errors and exit 1;
- produced exactly six computed view keys and six DOT files in a new directory;
- reported embedded Graphviz 15.0.0 and rendered six SVGs;
- produced byte-identical SHA-256 values across two renders and a second empty-cache `npm ci --ignore-scripts` installation;
- installed no Playwright browser and ran no lifecycle script;
- changed no worktree file.

These are capability results only; probe SVG hashes are not future golden output claims.

## Serialized I5-06 additions-only lease and rollback

Only after merged I5-05 may I5-06 acquire a time-bounded, exclusive lease to add new extension `.c4` files, manifest rows and render pairs. It may not alter the six original source files, mappings, paths, semantic projections, outputs, or tool lock. The six source/output hashes must remain byte-identical during an additions-only lease.

Rollback restores the previous `.c4` source closure, manifest, package lock, renderer/normalizer version and committed SVG/text/render manifest as one reviewed set; it never hand-edits SVG. If the tool becomes unavailable or cross-platform output differs, STOP for a separately authorized equivalence/toolchain migration. Never silently fall back to Structurizr, browser rendering, native Graphviz, or a newer npm resolution.
