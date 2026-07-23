# Threat Model and Security

## Scope and Assets

Stage A protects release lineage, 33 protected architecture identities, 21 released learning
contracts, the exact 50-path write set, locked tools, module/template/trace truth, visible render
semantics, bounded subprocesses, private raw evidence, and unrelated repository/ignored bytes.
There is no cloud or hosted runtime. Stage B security claims remain blocked.

Actors are the plan author, future independent validator, future readiness reviewer, future cook,
future implementation reviewer, repository approver, and untrusted curriculum/fixture/tool output.
Roles do not collapse: author self-checks are not independent validation; cook self-inspection is
not independent review.

## Threat Crosswalk

| ID | Threat | Required control and real negative |
|---|---|---|
| `S3-01` | Wrong base or remote race | Direct `5644f01b…` ancestry; local/upstream/fetched/live equality; mismatch stops |
| `S3-02` | Failed v1/v2/v3 byte reuse | Non-ancestry and patch/source audit; forbid `c07c9a0…` and failed evidence |
| `S3-03` | Scope smuggling | Three-range path decomposition; exact 50 creates; 33/21 per-path equality |
| `S3-04` | Fixture drives oracle | Strip metadata; real repositories; forbid booleans/dictionaries/echo/fallback/mocks/skips |
| `S3-05` | Template confusion | Exact 12 discovery/registry/instance closure and canonical hash lifecycle |
| `S3-06` | Trace/topology substitution | Real source, reciprocal relation/topology, protected governance identity mutations |
| `S3-07` | Render semantic spoofing | Locked LikeC4/DOT/Graphviz sole source; visible SVG/HTML/text parity and mutation |
| `S3-08` | Unsafe SVG/HTML/content | Reject script, event handler, `foreignObject`, URLs, data URI, hidden/duplicate semantics |
| `S3-09` | Secret/private locator leakage | Closed env; symbolic roots; scan raw and sanitized evidence; fail/quarantine on detection |
| `S3-10` | Process/resource escape | New session/PGID, aggregate sampling, deadline, TERM→KILL→wait, zero descendants |
| `S3-11` | Evidence fabrication | Retain contemporaneous raw bytes and separate derived logs; source hashes; closed index |
| `S3-12` | False independent claim | Exact role/class/independent/synthesized fields; separate immutable bundles |
| `S3-13` | Cleanup destroys or hides data | Owner/mode/type/link/device/inode closure; real porcelain; ignored-inclusive inventory |
| `S3-14` | Cloud/deployment side effect | No credentials, Docker/container action, AWS/Terraform/provider command, plan/apply/deploy |
| `S3-15` | Stage boundary forgery | No runtime reset/progress/completion/learner evidence or Stage B command in Stage A |

## Closed Runtime and Process Boundary

The controller owns a mode-0700 parent and `$I11_RUNTIME`, applies `umask 077`, uses
`$I11_RUNTIME/venv/bin/python` for every future I5-06 workload while preserving the frozen
released Make launchers, fixes cwd to a clean exact checkout, and admits a minimal explicit
`env -i` environment. The normative command amendment enumerates every key/value and phase,
including the admitted Python-parent `PATH`, private HOME/TMP/cache roots, locale, pip/Git controls,
and the exact command-specific Make additions. It rejects caller root/interpreter/PATH/tool,
proxy, loader, cloud, and credential overrides. Children use fixed argv and constructed
environments with admitted hashes; no shell text, caller executable, or `os.environ` copy is
accepted. Network is open only for exact hash/lock-verified bootstrap and is closed before
validation/rendering.

Released commands create only the enumerated `.artifacts/evidence/**` and
`.artifacts/workspaces/golden/**` layouts. Complete evidence directories are copied and verified in
the private bundle before exact-owner source cleanup; unlisted byproducts, run-ID collisions,
pre-existing-byte adoption, or residual nonignored bytes fail. Locked renderer stage and backup
names are transient only, and any protected-render change fails.

Every child starts a new session/process group. The controller streams stdout and stderr while it
samples all descendants, enforces the amendment's deadline/RSS/process/output/file bounds, and on
breach signals only the owned PGID: TERM, five-second wait, KILL remaining processes, wait/reap,
then zero-descendant proof. Real tests spawn grandchildren, ignore TERM, allocate RSS, flood output,
and create too many/large files. Missing measurement is failure.

## Input, Template, and Render Boundary

Parsers accept regular bounded UTF-8/NFC/LF files, reject duplicate keys, BOM, unsafe integers,
deep/large structures, special files, links, traversal, and unknown fields. Template hashes use a
defined canonical hash-excluded body; instance bindings cannot select an unregistered copy or
precomputed Boolean. LikeC4 source and locked DOT/Graphviz output are the sole render authority;
Python cannot synthesize parallel visible relation cards.

SVG and fitted HTML reject active content, external/local references, absolute/private paths,
credentials, account/resource IDs, hidden semantic substitutes, and cloud/apply claims. Vietnamese
labels and text alternatives are content, not trusted markup.

## Evidence and Privacy Boundary

Raw normalized mutation bytes, raw stdout, and raw stderr are bounded and mode 0600. Passing
evidence must pass secret/private-path/URL scans; detection fails the run and leaves the raw bytes
privately quarantined for incident review. Sanitized logs are separate derived files with exact
source hashes and redaction summaries. A hash without retained raw bytes is not evidence.

The closed index covers owner markers, every payload, byte count, hash, media type, mode, file
type/link status, render/resource/S3 records, and cleanup. It rejects missing, duplicate, orphan,
extra, stale, tampered, executable, linked, or wrong-owner content. It stores symbolic root IDs,
never host-local user-directory, home-directory, or worktree locators, and never caller
environment dumps or authentication material.

## Cleanup and Rollback Boundary

Deletion is confined to controller-owned temporary roots after exact marker, normalized path,
device, inode, and manifest checks. Retained evidence and fitted inspection HTML are not temporary.
No root `make clean`, recursive broad delete, reset, rebase, history rewrite, worktree removal, or
foreign ignored cleanup is authorized. Real Git status bytes, including ignored NUL output, drive
handoff. Exit 0 with nonempty porcelain fails.

Rollback removes only exact Stage A creates and verified temporary state, keeps the plan lineage
and retained evidence, and re-proves all 33 protected and 21 released identities plus unrelated
tracked/untracked/ignored bytes.

## Residual Risks

- Static Stage A content does not prove learner effectiveness or hosted security.
- WASM/layout correctness is bounded by locked tool identities and visible parity/determinism,
  not formal verification.
- Cook self-inspection can miss usability defects; fresh independent exact-head review remains a
  separate mandatory future gate.
- Conceptual AWS topology and costs require a new owner-approved Stage B/cloud threat model before
  any implementation; this plan authorizes no action.
