# Risk and S3 Threat Model

## Scope and assets

Security level `S3`, risk `high`. Protected assets:

- immutable repository/golden contracts, models, views, fixtures and readers;
- isolated lab workspace, warehouse, release staging, manifests and current pointer;
- local object-store bytes, Iceberg catalog/snapshots and OpenMetadata entities/edges;
- runner command authority, process/resource budget and optional service credentials;
- evidence index/artifacts and learner completion state;
- unrelated workspaces, namespaces, objects, catalog entities and private host paths.

Trust boundaries: untrusted learner input → contract parser → runner/operation registry → isolated
workspace/process → local data services → evidence writer → portal renderer. Browser is never the
privileged execution boundary.

## Threat register

| ID | Threat / abuse case | Required control | Negative test | Residual disposition |
|---|---|---|---|---|
| TH-01 | Traversal, absolute path, encoded separator, Git ref ambiguity | Typed relative refs, containment and allow-list before open | `DL-SEC-001` | STOP on ambiguous resolver |
| TH-02 | Symlink/hardlink/swap/TOCTOU or FIFO/socket/device/other special file reaches repo, blocks a reader or exposes foreign bytes | Descriptor/realpath/regular-file/ownership checks defined by released #9; refuse unsafe source/destination before read/write | `DL-SEC-002` | No weak fallback |
| TH-03 | SQL or template injection changes query/catalog target | Released fixed query/assertion IDs; typed values; no learner raw SQL/template | `DL-SEC-003` | Reject unsupported exercise |
| TH-04 | Env/credentials/private path/PII leaks to evidence or error | Minimal env, redaction, safe relative locators, no raw rows/full dumps | `DL-SEC-004` | Quarantine and rotate exposed secret |
| TH-05 | Broad object/catalog/namespace delete | Exact release ID/FQN + managed marker + run-owned ownership index | `DL-SEC-005`, `DL-OM-001` | Manual cleanup for unknown owner |
| TH-06 | Prefix collision (`lab-a` vs `lab-a2`) deletes neighbor | Equality on canonical namespace/FQN, never starts-with matching | `DL-OM-001` | Broad API incapable ⇒ block seam |
| TH-07 | Retry/replay duplicates publish or completion | Released idempotency contract + operation/tree/input binding | `DL-ORCH-001`, `DL-EVD-002` | Conflict instead of second effect |
| TH-08 | Evidence edited, reordered, artifact swapped or replayed on another tree | Canonical payload, artifact index/hash, tested-tree/dependency/content/verifier bindings | `DL-SEC-006` | Local integrity only; no authenticity claim |
| TH-09 | Timeout leaves child writing later | Scoped process group termination + post-timeout no-effect oracle | `DL-ORCH-002` | Host cannot contain ⇒ runner disabled |
| TH-10 | CPU/RAM/disk/output/process storm on 16GB laptop | Serial default, bounded concurrency/time/output/disk; preflight quota | `DL-ORCH-003`, `DL-RES-001` | No auto-scale/cloud escape |
| TH-11 | Optional service outage presented as lesson-controlled failure | Separate controlled/environmental/unexpected classes | `DL-OPT-001` | No affected completion |
| TH-12 | Crash after partial 11-asset/object/catalog mutation | Immutable staging, validated manifest, atomic pointer, journal/recovery | `DL-REL-003`, `DL-ICE-003`, `DL-OM-004` | Prior complete release stays current |
| TH-13 | Stale writer overwrites newer Iceberg snapshot | Verified catalog conflict semantics; input/snapshot precondition | `DL-ICE-002` | If no conflict primitive, use admitted serialized writer only |
| TH-14 | Starter/solution/fault injector mutates golden files | Read-only base; copy to private run root; before/after protected hashes | `DL-PROT-001` | Any drift is release STOP |
| TH-15 | Browser deep link triggers privileged local action directly | Browser uses released #10 API flow backed by #9 authority; no shell/command secret | `DL-ORCH-004`, `DL-SEC-007` | Disable action when dependency unavailable |

## Data classification

| Data | Allowed | Forbidden |
|---|---|---|
| Lab inputs | Bounded enums/numbers/stable IDs | Shell fragments, raw SQL, arbitrary path/ref/env/network destination |
| Retail data | Synthetic Issue #6 aggregate/golden workspace copy | Raw customer/order rows in evidence; PII-looking identifiers outside contract |
| Credentials | Process-local minimum for optional local services | Content, starter, logs, evidence, Git, browser response |
| Paths | Repository-relative or evidence-relative safe locator | Absolute home/private/tmp path in retained artifact |
| Evidence | Sanitized assertion summaries, versions, hashes, relative locators | Full env, tokens, private URLs, mutable external-only proof |

## Security release gates

1. Threat-control-test map is complete for the cooked stage.
2. Negative tests create no repository, foreign object, catalog or namespace mutation.
3. Required missing containment/registry/API capabilities fail; no preference-only fallback.
4. Optional services may be absent only with explicit `not-run-optional`; a real-service pass is
   still needed before that service-backed lab is published as verified.
5. Credential/private-path/PII and protected-path scans pass on exact reviewed head.
6. Standard focused review has zero unresolved Critical/Important findings; fresh tests, PR/CI and
   post-merge smoke pass without a separate red-team/security/human ceremony lane.

## Explicit exclusions

- No AWS credentials, AWS/S3 resources, Terraform plan/apply/destroy or cloud network action.
- No arbitrary browser execution, shell strings, user-selected executable or raw environment.
- No evidence authenticity/non-repudiation/signing claim; local SHA-256 is corruption detection.
- No cleanup of foreign/unowned state and no broad repository clean/reset.
