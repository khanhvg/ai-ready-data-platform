# Architecture and API Boundaries

## Decision

Stage A is one Vite-built React application plus one minimal Node static-file process. It has no
BFF, HTTP API, runner adapter, completion repository, session, database, or mutation surface.
The built static documents are complete without JavaScript; React progressively enhances the same
validated read-only view model.

```text
released #8 files + validators + exact shared Vite binding
                         |
                         v
              released-module-provider
                         |
                         v
            closed safe PortalCatalog model
                         |
          catalog -> module -> lesson -> step
                    /                    \
        static document             React shell
                    \                    /
             Node GET/HEAD-only static server
                         |
                   loopback browser
```

Stage B is a separate future architecture decision. It may add a server-only BFF and released
private Issue #9 adapter only after an exact #9 release amendment. Nothing in Stage A anticipates
that dependency through a placeholder, probe, client, route, token, or browser contract.

## Stage Separation

| Concern | Stage A | Stage B |
|---|---|---|
| Framework | Exact #7 Vite/React toolchain | Accepted Stage A or explicit compatible successor |
| Content/contracts | Exact released #8 files and validators | Same authority or released compatible successor |
| Server | Built-in static GET/HEAD server | Deferred BFF, if exact #9 release requires it |
| Runner | Absent; explicit unavailable state | Exact released #9 server-only client/API |
| State | URL/history presentation state only | Deferred canonical runner/#8 completion state |
| Evidence | Released fixture facts labelled retained baseline | Deferred fresh runner evidence |
| Claim | Understandable portal lesson slice | Deferred complete local journey |

## Exact Ownership and Files

The issue-level ceiling is `apps/learning-portal/**`, `mk/issue-5/i5-05.mk`, and Issue #10
plan/evidence artifacts. Stage A is narrower: exactly the 33 creates in the
[release amendment](./stage-a-release-amendment.md#exact-stage-a-tracked-write-allowlist), with no
modifies or deletes. Root Make already supplies the fragment include seam and remains unchanged.

Stage B paths, commands, and dependency identities are `[]`. Shared contracts, released lessons,
validators, fixtures, root files, dependency source, runner source, `README.md`, `docs/**`, cloud,
AWS, Terraform, CI, and other issues remain read-only or denied.

## Contract Binding Policy

The portal consumes the released shared binding exactly at
`learning/bindings/vite/promotion-trust-v1.json`, version/binding ID
`promotion-trust-vite-binding-v1`, SHA-256
`03d2aa6bd9fa178e6075865364a8ae8b83ce548c42b450d1858b451b45d0d1d0`. Its released schema
SHA-256 is `74035baee08b378e46421466333d6933d1bad820337acd1b80a633d236173a43`; the bound Stage A
contract-set SHA-256 is `92aaf9a573f5d23b5bf5d8d7db1e68150d4b0944f0e6ab6e651b1a3d34408638`.

The released public Python validators are the sole binding semantic authority. The portal may
iterate the accepted ordered `grainBindings` to project safe labels, but it must not create a
portal-local binding, alias/mapping table, copied schema, generated binding type, default,
transform, operation list, canonicalizer, or identifier truth. The release verifier separately
pins the #7 tool graph, all 85 consumed release paths, protected identities, and the two read-only
OpenAPI operation identities `listLessons` and `getLesson`; neither operation is exposed or
called.

The separate app-owned command activation is validated against the released generic activation
schema and immutable command-owner registry. It binds the final I5-05 fragment digest and emits
truthful `fitness-result-v2` results; it does not edit or replace shared registry truth.

The portal reads tracked released files at build time after the released validators pass. An
unknown field, family, version, path, hash, operation identity, content type, registry state,
binding authority, grain, key, alias, fixture reference, or special-file state fails the build
before render. There is no permissive fallback, local schema, copied registry, hand-written
lesson, or draft #9 value.

## PortalCatalog and Extension Seams

`PortalCatalog` is a closed internal projection with stable catalog, module, lesson, and narrative
step identities plus only safe released facts. The initial catalog contains one module entry and
one promotion-trust lesson vertical slice. It is never described as the entire course.

The seams are deliberately content-driven:

1. `released-module-provider` accepts only paths/families/versions/hashes recognized by the exact
   released contract set, shared Vite binding, and their validators.
2. `module-catalog` orders module and lesson descriptors without hard-coded route switches.
3. `portal-router` resolves catalog/module/lesson/step identities and stores only the selected
   read-only view in the URL/history.
4. static and React renderers consume the same `PortalCatalog` and stable fact IDs.

Later #11/#12 releases can contribute curriculum/module/lesson/lab manifests through that
provider after a new exact release binding. They do not require a shell, router, navigation, or
rendering redesign. Stage A does not invent their content, metadata, levels, routes, commands, or
contracts. Vietnamese is the default shell language; canonical released English IDs, questions,
failure codes, and decision values remain visibly distinguishable.

## Runtime Loading Boundary

The production build resolves only exact #7 packages and exact #8 read-only files/validators.
The browser bundle and static server must contain no Issue #9 path, module, URL, transport,
credential, registry, command, environment, dynamic optional import, storage adapter, or
completion code. Static startup must not probe Docker, a runner, optional tools, external network,
or cloud.

Bundle/import and network/storage tests make this absence executable. A missing or incompatible
Stage B capability leaves Stage A fully readable and reports `runner unavailable`; it is not a
controlled lesson failure.

## Logical Capability Boundary

| Capability | Stage A disposition | Authority |
|---|---|---|
| lesson/catalog read | Build-time validated projection only | exact released #8 files |
| read-only navigation | URL and `history.state`; no canonical progress | portal view state |
| runner/tool status | Constant explicit unavailable copy; no probe | Stage A claim boundary |
| run/reset/verify | Explanation only; no control or request | denied |
| progress/completion | No read/write/store/derived truth | denied |
| evidence | Released baseline facts only, never fresh/downloadable evidence | exact #6/#8 release |
| arbitrary command/path/URL/SQL/upload/proxy | No surface | denied |

Stage B logical operations remain descriptive historical requirements only. None becomes Stage A
route, type, module, or test double.

## State, Routing, and History

The only browser state is the selected catalog/module/lesson/narrative-step view. Canonical route
generation is deterministic from validated IDs. Navigation uses same-origin links first, with
React enhancement for `pushState`; `popstate`, back, forward, and reload select a view only. They
cannot initiate a request, replay a mutation, advance progress, or complete anything.

Unknown, malformed, overlong, percent-ambiguous, traversal, dot-segment, or unregistered routes
fail closed to a safe not-found document. No state lives in local/session storage, IndexedDB,
Cache Storage, cookies, service workers, query secrets, fragments, or ambient globals.

### Exact Stage A public route set

The static and enhanced portal expose exactly 13 canonical public documents:

```text
/
/module
/lesson/promotion-trust
/lesson/promotion-trust/step/frame
/lesson/promotion-trust/step/inspect
/lesson/promotion-trust/step/run
/lesson/promotion-trust/step/fail
/lesson/promotion-trust/step/trace
/lesson/promotion-trust/step/decide
/lesson/promotion-trust/step/reset
/lesson/promotion-trust/step/configure
/lesson/promotion-trust/step/verify
/lesson/promotion-trust/step/reflect
```

`/` is the catalog. `/module` is a presentation-only Stage A grouping view with no fabricated
module identifier; it does not claim released curriculum/module truth. The lesson ID and ten step
IDs come directly from the released `lesson-v1` document. Later #11/#12 route additions require
their released identifiers and a new exact binding; no current route guesses them.

Every route carries the same machine-readable non-claim attributes on its primary content root:

```text
data-product-scope="static-portal-slice"
data-runner="unavailable"
data-execution="disabled"
data-reset="not-run"
data-fresh-evidence="false"
data-progress="disabled"
data-completion="disabled"
```

These attributes are render assertions, not a new schema or state store. Visible Vietnamese-first
copy must also say this is a Stage A static learning slice, not the full learning product.

## Static and No-JavaScript Path

`generate-static-routes.mjs` renders the admitted route set from the same safe model used by
React. Every required route is a built HTML document with semantic navigation, breadcrumbs,
released lesson facts, independent-grain limitations, canonical decision, explanation-only
run/reset/verify steps, runner-unavailable notice, and explicit non-completion wording.

There is no second hand-maintained page or raw HTML/MDX execution. Stable fact-ID equivalence,
escaping tests, a built-output parser, and JavaScript-disabled Chromium prove parity. Missing JS,
runner, network, animation, hover, or optional tools cannot hide required facts.

## Stage A Data Flow

1. Verify final integration `5644f01b4c0443a81f3af0bcce80f44c847cd986`, the shared binding,
   all 85 consumed bytes, protected identities, lock, and command owner.
2. Run released #8 learning, lesson, and API validators.
3. Map only admitted released fields into `PortalCatalog`.
4. Render Vietnamese-first catalog/module/lesson/step static documents.
5. Build the React enhancement from the same model.
6. Serve only bounded built regular files over loopback GET/HEAD.
7. Explain the four independent grains and canonical
   `insufficient-evidence / no-common-grain` outcome.
8. Report runner unavailable and completion disabled; perform no lab action.

No step produces a workspace, run, reset, fresh verification, evidence, progress, completion, or
course claim.

## Static Server and Performance Shape

The Node server binds `127.0.0.1` on a runtime-selected port, accepts exact local Host values,
serves GET/HEAD only, and rejects bodies, traversal, ambiguous decoding, unknown routes, and
foreign Hosts. It serves only admitted build-root regular files with declared media types and the
strict Stage A headers/CSP.

One Node process and one Playwright worker are allowed. Install/build/test/server/output/review
ceilings are exact in the amendment. There is no broker, worker fleet, database, service worker,
poller, container, optional profile, API buffering, external fetch, runner, or cloud component.
