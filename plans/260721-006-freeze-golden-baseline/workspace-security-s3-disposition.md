# Workspace security S3 disposition

## Scope and threat model

“S3” here is the master security/preservation gate, not authorization for Amazon S3. This issue performs no cloud action and stores no production secret. It runs repository-controlled generator/dbt/export/architecture tools against synthetic data, but those tools write files and spawn children, so the realistic threats are:

- an absolute/parent path or symlink escaping the issue-owned workspace;
- a pre-existing foreign directory being treated as owned and deleted;
- check/use or cleanup-time symlink swaps, hardlinks, special files or concurrent publishers;
- inherited credentials, proxy/private URLs, `PYTHONPATH`, user home/config or ambient tool caches changing behavior or leaking into evidence;
- unbounded output, timeout-resistant descendants, partial writes and stale locks;
- a compromised same-user process replacing bytes and recomputing an unkeyed digest.

The protected assets are repository files outside issue authority, user/private host data, credentials, reproducibility evidence and the integrity of the current pointer contract. This issue does not claim hostile-root isolation, generalized privileged-runner containment, hosted signing or cloud publisher safety.

## Private roots and allocation contract

Mutable state and retained evidence use disjoint repository-relative roots:

```text
.artifacts/workspaces/golden/<run-id>/
.artifacts/evidence/golden/<run-id>/
```

Other public fitness commands use the same allocator under the exact allow-listed family root
`.artifacts/evidence/<fitness-id>/<run-id>/`; caller-supplied fitness IDs, paths and run IDs are
not accepted. `.artifacts` is visible/unignored at the immutable input. It is always transient or
locally retained evidence and must never appear in the Git index.

The runner generates a collision-resistant run ID; normal public targets do not accept an arbitrary path or run ID. Test-only injection is behind an explicit test interface and never shipped as a Make parameter. Parent and run directories are mode `0700` subject to a checked restrictive umask.

Allocation procedure:

1. Resolve the tracked repository root from the approved Git worktree, not CWD text or an environment override.
2. Reject empty/NUL components, absolute paths, `.`/`..`, alternate separators, normalization ambiguity and any target outside the exact two base directories.
3. Open each existing base component with no-follow/directory semantics; record device/inode identity and retain the directory descriptor.
4. Create the run directory exclusively relative to that descriptor; fail on collision rather than reuse.
5. Create an owner marker exclusively containing schema, random ownership nonce, run ID, base tree, device/inode and purpose. Re-read it through the retained descriptor.
6. Perform child operations relative to retained directory descriptors. Reject symlinks, hardlink count greater than one for mutable regular files, FIFOs/devices/sockets and pre-existing foreign entries.

If the host filesystem cannot supply the required no-follow, same-filesystem atomic-rename and identity checks, fail `WORKSPACE_FS_UNSUPPORTED`; never downgrade quietly.

The current support tuple is native Darwin arm64 with POSIX private modes. Every created parent,
run directory and file is verified after creation (`0700` directories, `0600` mutable/evidence
files, restrictive umask). Linux and Windows are unclaimed; a non-Darwin host fails the platform
preflight before allocation or network. A future platform lane must define equivalent private
permission/no-follow/atomic semantics and pass the same attack suite.

## TOCTOU, write and publication rules

- Never validate a pathname and later reopen it by uncontrolled absolute text. Use open directory descriptors/no-follow operations and compare device/inode after each boundary transition.
- Create immutable output files exclusively. For replaceable indexes, write a unique temporary regular file in the destination directory, bound length and permissions, flush/fsync, verify identity/content, atomic rename, then fsync the directory.
- Cross-device rename is forbidden. A partial set never becomes current.
- Publication uses an exclusive issue-owned lease containing owner nonce/tree/run identity. Another active or stale lease fails `PUBLICATION_LEASE_HELD` with manual inspection instructions; code never auto-breaks it.
- Independent runs never share a venv, cache, home, dbt target/log, raw data, warehouse, export, architecture staging, or evidence directory.
- The tracked promotion fixture and rendered architecture set are replaced only after staging and validating the entire authorized set.

Tests interleave path validation with symlink swaps, rename the parent after descriptor capture, replace a temporary file before rename, attempt cross-device publication, and race two publishers. Success requires either safe completion against the originally opened object or a typed failure—never writing/deleting the attacker target.

## Environment and redaction contract

Each child receives a new allow-listed environment, not a lightly filtered copy. Stable required values include `PATH` pointing only to the private pinned toolchain plus minimal system binaries, `TZ=UTC`, `LC_ALL=C.UTF-8` (or the verified platform-equivalent), `LANG`, `PYTHONHASHSEED=0`, private `HOME`, explicit dbt/project/input/output paths and the requested profile/seed.

Explicitly absent values include `PYTHONPATH`, user pip/npm/dbt config variables, cloud/AWS/GCP/Azure credentials, GitHub/token variables, OpenMetadata/MinIO secrets, SSH agent/socket, Docker/Compose state, proxy/private registry variables, tracing exporters and unrelated `*_TOKEN`, `*_PASSWORD`, `*_SECRET`, `*_KEY`, `*_CREDENTIAL*`. The dependency-download step uses the single explicit public index in the reviewed compiler/install contract; pipeline execution is offline.

Before persistence, a structured allow-list selects evidence fields. Secondary redaction scans bounded stdout/stderr and candidate JSON/text for:

- credential/private-key/token patterns and test canaries;
- home paths, usernames, absolute workspace paths and runtime IDs;
- private or credential-bearing URLs, proxy strings and environment dumps;
- raw customer/order records or identifiers.

Detection fails `EVIDENCE_SENSITIVE_CONTENT`; it does not replace the offending value with a misleading passing artifact. Store a minimal reason and content hash, not the secret. Raw synthetic aggregate evidence remains subject to the same path/credential rules.

## Bounded processes and failure retention

Each step starts in its own process group/session with explicit CWD, environment, stdin closed and stdout/stderr captured separately. Default bounds:

- 2 MiB stdout and 2 MiB stderr per step;
- 16 MiB combined retained output per run;
- 2 GiB maximum mutable bytes for one golden run, 2 GiB for one architecture bootstrap/stage and
  256 MiB retained evidence per run; preflight requires 6 GiB free on the containing volume;
- step deadline from [implementation-handoff.md](./implementation-handoff.md);
- timeout: send TERM to the process group, wait 5 seconds, send KILL, wait/reap up to 5 seconds;
- detect/reap descendants and fail if any child remains.

Output overflow is `PROCESS_OUTPUT_LIMIT`, not silent truncation; retain a prefix/suffix plus full-stream hash and byte count without retaining sensitive overflow. Timeout is `PROCESS_TIMEOUT`; descendant leakage is `PROCESS_CLEANUP_FAILED`. The runner finalizes bounded failure evidence after termination and does not claim a semantic projection for incomplete work.

## Cleanup and `golden-clean`

Despite its name, future `golden-clean` means “run from newly allocated private state.” It must never invoke the existing root `make clean`, shell out to a recursive broad delete, scan the worktree for targets, follow symlinks, delete retained evidence, or touch another run.

Cleanup:

1. Reopen the exact base through the recorded no-follow descriptor chain.
2. Verify repository/base/run device/inode, owner marker schema, nonce and run ID.
3. Refuse a symlink, marker mismatch, foreign/pre-existing root, mount/device change or unexpected entry type.
4. Delete only descendants reached relative to the verified run descriptor, never following links.
5. Remove the run directory only after a complete owned traversal; fsync the parent.

Successful runs may remove their private mutable workspace after evidence finalization. Failed workspaces are preserved by default for diagnosis and referenced only by a sanitized relative locator. A separate future manual cleanup mode may remove them only with the same owner proof; it is not a broad root clean.

The two formal runs execute sequentially so their mutable roots are never intentionally active at
the same time. Disk-limit or free-space failure emits bounded evidence and stops; it does not
delete an earlier run, user state or foreign `.artifacts` content to make room.

## Required negative tests

| Class | Mutation | Required result |
|---|---|---|
| Path | absolute, parent escape, empty/NUL, alternate normalization | reject before allocation |
| Symlink | component symlink at allocation, child symlink, post-check swap, cleanup swap | reject or remain bound to safe opened inode |
| Foreign state | pre-existing directory without marker, wrong nonce/tree, hardlink, FIFO/device/socket | refuse reuse/deletion |
| Concurrency | same forced run ID, two publication attempts, stale/active lease | one exclusive owner; other typed failure |
| Atomicity | kill before fsync, after fsync/before rename, after rename/before dir fsync | no partial current set; recovery identifies staged state |
| Process | timeout, TERM-ignoring child, grandchild, stdout/stderr flood | bounded termination, reap, typed failure evidence |
| Environment | credential/cloud/proxy/private-URL/path canaries; ambient pip/npm/dbt config | absent from child or detected before retention |
| Preservation | root `release-manifest.json`, `.gitkeep`, absent `docs/code-standards.md`, unrelated ignored file | exact pre/post state unchanged |
| Cleanup | forged marker, parent renamed/replaced, evidence symlink | preserve target and fail safely |

## Security dispositions and residual risks

- **Contained by this issue:** accidental/malicious path escape within the golden workflow, inherited-secret leakage, common symlink/TOCTOU races, concurrent publication, partial evidence writes, output/process exhaustion, and broad-clean damage.
- **Accepted residual:** a same-account or root actor can replace bytes and recompute unkeyed hashes. Local SHA-256 is corruption detection only.
- **Accepted residual:** a crash can leave a scoped private directory or lease requiring verified manual cleanup.
- **STOP condition:** filesystem semantics cannot enforce no-follow/atomic identity, or the selected tool writes outside explicit paths.
- **Deferred by authority:** generalized privileged execution isolation (I5-04), trusted publisher/signing (I5-14), cloud/S3 containment and real publisher reconciliation (I5-07/later cloud issues).

Redaction is a secondary defense. The primary defenses are a no-secret allow-listed environment, private roots and allow-listed tracked fields.
