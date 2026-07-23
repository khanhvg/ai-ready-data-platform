# Architecture and API Boundaries

## Current Stage B Addendum

The Stage A architecture below is shipped historical context. Current Stage B authority is the
18-path Phase 6 amendment at integration
`671201f78024786a9f2eba5e9e5fce7c78b4443d`: the same Node process serves the closed static
inventory plus a small authenticated same-origin loopback BFF. The BFF maps nine fixed journey
actions to eight exact released runner CLI operations plus one non-executing learner decision. It
owns session/CSRF, Host/Origin/body/method/concurrency/output/time admission, progress/evidence/
completion persistence, child lifecycle, and cleanup. Browser input cannot select an operation,
command, argv, environment, path, URL, SQL, image, package, plugin, Docker option, or cloud option.

The BFF uses the released Issue #9 owner CLI and immutable evidence store. It does not expose the
runner's private transport, invent a runner HTTP API, parse runner SQLite, or change runner/shared
contracts. `progress-v1`, `learning-evidence-v1`, and `learning-progress-authority-v1` remain the
only learning truth. The exact design, operations, request schemas, and reset/completion order are
in [Phase 6](./phase-06-stage-b-real-journey-and-completion-integration.md).

## Decision

Stage A is one Vite-built React enhancement plus deterministic static documents and one minimal
Node static-file process. It has no BFF, product API, runner adapter, completion repository,
session, database, mutation, or canonical learner state. Static documents remain complete without
JavaScript.

Production has exactly one content/route authority:

```text
exact released integration 5644f01...
  -> released validators
  -> learning-contract-set-v1.json (sole descriptor-registry root)
  -> exact hash-bound manifest + lesson + lab + shared Vite binding
  -> immutable ReleasedPortalDescriptorRegistry
  -> catalog + app + router + static routes + React/static render
  -> closed inventoried build
  -> loopback GET/HEAD server
```

At the Stage A release this was intentionally static and Issue #9-blocked. That historical boundary
remains true for the shipped Stage A commit; the current Stage B addendum above supersedes only the
future-state column.

## Stage Separation

| Concern | Stage A | Stage B |
|---|---|---|
| Framework | Exact released Vite/React toolchain | No authority |
| Content | Exact released Issue #8 descriptor/binding/contract hashes | No additional authority |
| Server | Inventoried static GET/HEAD process plus private lifecycle control listener | No BFF authority |
| Runner | Absent; visible unavailable state | Blocked on exact released Issue #9 |
| State | URL/history presentation only | No progress/completion authority |
| Evidence | Released facts plus implementation-review evidence, never learner-run evidence | Blocked |
| Claim | Understandable static vertical slice | None |

## Exact Ownership

Stage A creates exactly the 33 paths in the
[v3 amendment](./stage-a-release-amendment.md#exact-stage-a-tracked-write-allowlist). It modifies
and deletes no released path. Root Make remains unchanged and includes the issue-local fragment
through its released sorted include seam.

Stage B authority is exactly the 18 paths, 15 commands, and eight operations in Phase 6. Shared
contracts, released lessons, validators, fixtures, root files, runner source, Issue #11
curriculum, Issue #12 labs, Issue #13 profiles, README/docs, CI, container definitions, cloud,
AWS, and Terraform remain read-only or denied.

## Released Descriptor Registry Admission

`learning/contracts/learning-contract-set-v1.json` at SHA-256
`92aaf9a573f5d23b5bf5d8d7db1e68150d4b0944f0e6ab6e651b1a3d34408638` is the sole released
descriptor-registry root. The current admitted graph is:

- `learning/manifests/promotion-trust-v1.json` at its exact 85-row catalogue hash;
- its exact hash-bound `lesson-v1` and `lab-v1` members;
- `learning/bindings/vite/promotion-trust-v1.json`, binding ID
  `promotion-trust-vite-binding-v1`, SHA-256
  `03d2aa6bd9fa178e6075865364a8ae8b83ce548c42b450d1858b451b45d0d1d0`;
- the exact contract-set, binding-schema, fixture, protected, operation, and tool hashes in the
  released-input catalogue.

The released Python validators remain semantic authority. The Node verifier independently binds
the release tree and all 85 rows, runs those validators through the exact admitted runtime, then
builds one immutable `ReleasedPortalDescriptorRegistry` containing only safe released fields.
Unknown/extra/unhashed/draft/wrong-family/version/path/hash/field/state fails before catalog
construction. There is no permissive fallback, portal-local schema, copied registry, generated
binding type, or duplicate alias map.

The shared binding's ordered `grainBindings` are iterated directly. Portal source never restates
`region→region_name`, `category→category_name`, or `dq→data-quality`.

## Catalog, App, Router, and Renderer Contract

All production consumers accept one explicit registry argument. None imports content directly or
creates default truth:

- `released-module-provider` performs production admission and safe projection;
- `module-catalog` orders admitted descriptors;
- `portal-router` derives routes and resolves views from that catalog;
- `generate-static-routes`, `static-document`, `main`, and app/navigation components consume the
  same derived catalog and route objects;
- the promotion-trust feature renders generic safe-model fields for the currently admitted lesson
  and is not a portal-wide switch.

The router owns no `defaultCatalog`, `STEP_IDS`, 13-route constant, promotion-specific branch, or
fallback lesson. Acceptance tests may enumerate the current expected route output, but production
derives it from released `lesson.id` and ordered `narrativeSteps`.

`PortalCatalog` and safe view objects are internal immutable projections, not new contracts. They
carry only released IDs/versions, title/summary/level, stakeholder question, ordered narrative
steps, accessibility flags, source grains/limitations, binding-derived aliases, decision status,
and explicit Stage A capability absence.

## Test-Only Structural Descriptors

Unit tests may construct in-memory structural values with
`authorityKind: test-only-structure`. These values:

- use neutral unit-test tokens and never claim a release, Issue #11/#12 identity, path, hash, or
  authority;
- enter only pure catalog/route/render derivation functions;
- never enter `admitReleasedRegistry`, build inputs, static output, runtime catalogs, Chromium
  evidence, or public evidence;
- are production-rejected with `PORTAL_DESCRIPTOR_AUTHORITY_FORBIDDEN`;
- are absent from bundle/build/runtime inventories and string scans.

Metamorphic tests use both the exact current released descriptor and branded test-only structure
to prove order, uniqueness, route-count, escaping, rename locality, and add/remove locality. They
prove generic mechanics only—not that another release exists.

## Future #11/#12 Entry

Future content can enter without code-level content-ID hardcoding only through this sequence:

1. the owning issue releases validated curriculum/module/lesson/lab documents;
2. a reviewed integration release adds exact hash-bound entries to the released contract set and,
   when aliases are needed, a compatible released binding;
3. a later Issue #10 amendment pins the new integration and expands the read-only input catalogue;
4. the unchanged family-driven provider enumerates the recognized entries and pure derivation
   creates catalog/routes/documents;
5. fresh tests, validation, readiness, implementation review, and evidence run at that head.

No current code names or guesses an Issue #11/#12 route, ID, level, content, or release hash.

## State and Routing

The only browser state is the selected catalog/module/lesson/narrative-step view. Navigation uses
same-origin links first and may enhance with `pushState`; popstate, back, forward, and reload
select a view only. They cannot invoke a request, mutation, runner, progress, evidence, or
completion path.

The current registry derives exactly 13 public documents: catalog root, presentation-only module
root, the released promotion-trust lesson, and its ten released steps. `/module` has no fabricated
module identifier. Unknown, malformed, overlong, percent-ambiguous, traversal, dot-segment, or
unregistered routes fail closed.

No state lives in cookies, local/session storage, IndexedDB, Cache Storage, service workers,
query secrets, fragments, ambient globals, or a database.

## Static and No-JavaScript Path

`generate-static-routes.mjs` renders the registry-derived routes from the same safe model used by
React. Each built HTML document contains semantic navigation, Vietnamese-first guidance, released
facts, four independent-grain limitations, `insufficient-evidence/no-common-grain`, explanation-
only run/reset/verify, runner unavailable, and explicit non-completion/not-full-product wording.

There is no hand-maintained second page, raw HTML/MDX execution, copied fixture, or separate route
truth. Stable fact-ID, escaping, built-output, and JavaScript-disabled Chromium tests prove parity.

## Static Server and Build Inventory

After two deterministic builds compare equal, the server admits one closed inventory containing
only regular single-link files with exact path/media/size/SHA-256. It serves no filesystem path
outside that inventory. Public listener policy is exact loopback Host plus GET/HEAD, zero body,
no transfer encoding, bounded target, and strict decoding. It rejects method/body/chunking/length/
Host/path ambiguity before opening content.

The separate private lifecycle control listener is not a product API. It accepts only bounded
authenticated status/shutdown messages carrying the child-held instance nonce and capability.
The child performs its own shutdown. Parent commands never signal a PID from mutable state.

One Node process and one Playwright worker are allowed. There is no broker, database, worker
fleet, BFF, runner, service worker, poller, container, optional profile, external fetch, or cloud
component.

## Capability Boundary

| Capability | Stage A disposition |
|---|---|
| catalog/lesson read | Build-time validated released projection only |
| navigation | URL/history view only |
| runner | Constant visible unavailable state; no probe |
| run/reset/verify | Explanation only |
| progress/completion | Absent; no store or derived truth |
| evidence | Released baseline facts plus implementation-review artifacts, never fresh learner evidence |
| arbitrary command/path/URL/SQL/upload/proxy | No surface |

Every route states that Stage A is a static portal slice, not the complete learning product.
