---
title: "Issue #13 S3 Threat Model"
status: planned-unvalidated
security: S3
created: "2026-07-22"
---

# Issue #13 S3 Threat Model

## Scope and Assets

Protect:

- host availability on a 16 GiB developer Mac;
- foreign Compose projects, containers, networks, volumes, ports, files, and processes;
- released portal/runner/lab artifacts and their immutable digests;
- synthetic retail/golden semantics and protected repository files;
- local credentials/private paths and evidence integrity;
- the guarantee that Docker-free core does not cross a privileged/container/cloud boundary.

The supported security boundary is the I5-08 admission/measurement/teardown commands and the exact
Compose/config they render. A local user with unrestricted Docker CLI access is already equivalent
to privileged host control and can bypass any wrapper; that actor is outside enforcement. Inputs
accepted by the supported commands, dependency artifacts, images, and co-resident foreign projects
are inside the threat model. The implementation must not imply that Compose profiles are an OS
authorization mechanism.

## Trust Boundaries

```text
untrusted CLI/env/profile request
        |
        v
static parser + exact allowlist + dependency closure + budget/security gates
        |
        v
private run manifest / admitted Compose invocation
        |
        +--> local engine --> exact digest containers --> run-owned volumes/networks
        |
        +--> sampler --> private raw evidence --> canonical summary/hash index/completion
        |
        v
ownership-scoped teardown (foreign resources are observe-only sentinels)
```

Portal/browser is never trusted with engine control. The portal and any web-facing service receive
no Docker socket, engine API, host-root bind, teardown capability, or raw environment/evidence.
Runner boundaries remain owned by the released runner contract and are consumed read-only.

## Threats and Required Controls

| ID | Threat | Required design/control | Required proof |
|---|---|---|---|
| TM-01 | Malicious/ambiguous profile string | Parse an exact grammar; reject empty, duplicate, unknown, reordered alias tricks, glob, newline, option, path, and Unicode-confusable values | RED invalid/missing/duplicate/unknown tests; no Compose call |
| TM-02 | Env or Compose interpolation injects files/profiles/project/network/volume/commands | Start from a minimal explicit env allowlist; clear/deny `COMPOSE_FILE`, `COMPOSE_PROFILES`, project/path override and proxy/credential surprises; never invoke a shell with user text | Interpolation fixtures; rendered config hash and argv capture |
| TM-03 | Compose silently activates dependency outside admission | Resolve transitive `depends_on` closure from the exact render; compare every service/profile to the signed/hashed allowlist | Dependency-expansion RED; exact closure evidence |
| TM-04 | All-three or unauthorized pair bypass | Combination rule is independent of numeric budget; only exact `lake+governance` pair has a guarded token bound to run/config/workload digest | All-three and pair RED; Compose invocation absent on denial |
| TM-05 | Missing/forged resource limit enables host exhaustion | Schema requires memory, CPU, PID, disk, log, deadline and port/volume owner per service; reject null/zero/duplicate/overflow/unit ambiguity | Limit mutation matrix; static aggregate summary |
| TM-06 | PID/fork/thread/resource exhaustion | `pids_limit`, CPU/memory caps, concurrency lock, bounded subprocess tree and termination grace; Java/thread needs stay inside declared cap | PID omission/mutation tests; live limit/result |
| TM-07 | Disk/log exhaustion | Read-only roots where compatible; only declared volumes/tmpfs; tmpfs sizes; byte-growth ceiling and kill; Docker log rotation; output byte caps | Disk/log mutations; growth/teardown evidence |
| TM-08 | Readiness hang or restart loop | Health/one-shot hard deadlines, `restart: "no"` for acceptance, restart/OOM count zero, bounded build/pull/workload/teardown | Missing-timeout RED; timeout/restart live negative |
| TM-09 | Port hijack/public exposure | Bind only `127.0.0.1`; declare owner; reject wildcard, duplicate, occupied, unexpected and dependency-added ports | Port collision/public-bind RED; socket ownership snapshot |
| TM-10 | Volume/project collision or adoption | Exact project/run labels and private owner manifest; existing foreign object causes denial; never relabel/adopt/delete it | Volume/project collision RED; foreign sentinel survives |
| TM-11 | Host mount, socket, privilege, capability or network escape | No Docker socket to web/portal; no privileged/host PID/host network/devices; drop capabilities and set no-new-privileges; read-only code/base; explicit private networks; exact required writable paths only | Static Compose security mutations and rendered inventory |
| TM-12 | Registry tag drift/wrong architecture | Tags alone fail; record registry index and resolved platform digest; no pull during acceptance; architecture must match | Digest/platform mutation; `--pull never` argv/result |
| TM-13 | Malicious image or opaque supply chain | Require exact image policy decision, SBOM digest, signature/provenance verification, registry/source identity, and vulnerability disposition before Stage B | Per-image verification artifact; absent/failed policy blocks |
| TM-14 | Secret/private path/PII leakage | Synthetic inputs only; do not dump environment; redact values and `/Users/...`; private 0700 roots/0600 files; cap logs; scan evidence before completion | Canary secret/private-path tests; redaction result |
| TM-15 | Path traversal, symlink/hardlink/special-file attack | Repo-relative allowlist; lexical and resolved containment; `lstat`/no-follow; reject symlink, device, FIFO, socket, wrong owner/mode/link count; atomic create | Path/symlink/special-file RED matrix |
| TM-16 | Evidence tamper, partial publication or replay | Random run ID, tested-tree/config/image/tool hashes, monotonic sequence, canonical bytes, locator allowlist, hash index, completion written last/atomically; reject duplicate/replayed completion | Tamper/replay/truncation tests and N-1 reader tests |
| TM-17 | Teardown destroys foreign/retained state | Select by exact run/project labels and owner nonce; enumerate before delete; no broad glob/default project; evidence and retained volumes excluded; post-delete residue diff | Actual foreign Compose sentinel survives recovery test |
| TM-18 | Engine absent is converted into a fake pass | Static checks remain distinct; live required result is typed blocked/non-zero; no fixture/sample substitutes for measurements | Engine-unavailable RED and command result |
| TM-19 | Cloud/AWS/Terraform or network side effect | No cloud credentials/actions; no AWS/Terraform command; image pull only in separately recorded admitted pre-stage; acceptance uses local exact images | Command allowlist and credential/network scan |
| TM-20 | Protected semantics/contracts drift | Hash/diff guard for root/shared/golden/portal/runner/lab/migration/release/code-standard paths; only exact Phase 8 allowlist writable | Protected-hash report and blast-radius tests |

## Image Admission Policy

The current tag strings are inventory only. Before Stage B, each actual service entry must bind:

- registry/repository identity;
- immutable registry index digest and resolved host-platform manifest digest;
- architecture/OS;
- SBOM locator and SHA-256;
- signature or provenance attestation verifier, identity, policy, result, and tool version;
- vulnerability/license disposition and expiry/revalidation rule;
- local-build context/Dockerfile/lock hashes and image digest when applicable.

If a third-party image lacks the required signature/provenance evidence, the owner must issue an
explicit exact policy amendment with compensating controls; the planner/implementer cannot assume
an exception. Portal/runner image names and digests remain empty until dependency release. Do not
copy a future SHA from an unmerged plan branch.

## Compose and Runtime Security Contract

Static `compose-security-check` rejects:

- `privileged`, host PID/IPC/network, devices, Docker socket/API, wildcard binds, external networks
  or volumes, unowned writable mounts, RW repository/base code, added capabilities, missing
  `cap_drop`/`no-new-privileges`, or unapproved user/root execution;
- missing immutable digest policy, limits, log rotation, health/exit deadline, owner labels, or
  expected dependency closure;
- shell-form command/entrypoint or interpolation in a security-sensitive field unless the actual
  immutable image contract requires and tests a fixed non-user string;
- environment keys/values not named by the per-service allowlist or containing secret material;
- service, image, port, mount, network, volume, profile or project not in the exact amended config.

Image compatibility may prevent read-only root/capability/user hardening for an existing service.
That is a typed Stage A blocker requiring an exact threat disposition; it is not silently waived.

## Evidence Security

Evidence root is `.artifacts/evidence/local-profiles/<run-id>/`. Requirements:

- private parent/run directories; run ID unguessable and unique;
- repo-relative logical locators only; absolute host paths normalized/redacted;
- command argv recorded as a string array, not a shell reconstruction;
- environment records names plus redacted/presence classification, never secret values;
- raw samples immutable after completion; summary derived from retained raw; both hashed;
- index covers byte length and SHA-256 for every retained artifact except its own non-recursive
  integrity envelope; released completion authority defines the exact commit point;
- reject stale tested tree, dependency/image/config/tool mismatch, missing artifact, duplicate
  locator/hash, malformed order, future timestamp, replayed run ID, or completion before teardown;
- retained evidence is never mounted writable into web/portal containers.

The existing owner-fixed `fitness-result-v1` cannot be repurposed. Exact field/status/commit rules
come from the released completion/evidence authority in the dependency amendment.

## Recovery Security

Teardown obtains targets only from the immutable run manifest and verifies engine labels plus the
owner nonce before every operation. It removes run-owned containers, networks, explicitly
ephemeral volumes, temp directories, child processes, port reservations, and bounded logs. It
preserves:

- `.artifacts/evidence/local-profiles/<run-id>/` and its completed index;
- explicitly retained run-owned data named by policy;
- every foreign project/container/network/volume/sentinel;
- repository files and user data.

Interruption is recoverable by rerunning teardown with the same manifest. A missing/mismatched
manifest blocks deletion and reports manual locators; it never broadens target selection.

## Residual Risks and Decisions Deferred

- A Docker-authorized local user can bypass supported admission. Document this honestly.
- Docker Desktop/cgroup/volume accounting differs from Linux. Raw layers stay separate; no opaque
  total or portability claim.
- Exact portal/runner/lab/image/command/completion contracts are absent. Their threat boundaries
  require future exact amendment and independent review.
- Image signature/SBOM availability is unknown. Stage B stays blocked until policy is satisfied.
- Persistent named-volume hard quota support is engine-specific. The admitted engine must provide
  enforceable/observable bounds; otherwise the affected scenario is blocked.
- Existing local-only credential defaults are not production secrets, but evidence/log scanning
  and loopback/private network controls remain mandatory.
