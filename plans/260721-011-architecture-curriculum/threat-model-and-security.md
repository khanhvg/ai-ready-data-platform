# Threat Model and Security

## Security Disposition

Issue #11 is `security:S3`. Here “S3” is the security tier, not authorization to use Amazon S3.
This plan authorizes no implementation yet and no runtime, credential, cloud, AWS, Terraform,
portal, shared-contract, or protected architecture-toolchain change. The proposed Stage A scope
covers only structured curriculum and isolated generated static architecture expansions after
fresh independent validation/readiness. Future Stage B adds one local architecture lab only
through exact released Issue #8/#10 seams.

The protected assets are dependency contract truth, completion/evidence authority, the released
portal renderer, the six Issue #6 local views and toolchain, repository/user files, learner
evidence, and truthful architecture claims. Synthetic retail architecture content is not secret,
but paths, environment values, credentials, host identity, evidence integrity, and control-plane
boundaries still require protection.

## Actors and Trust Boundaries

| Actor | Allowed role | Not trusted for |
|---|---|---|
| Learner | Read curriculum; perform bounded Stage B task; request released reset/verify | Authoring completion, evidence, arbitrary paths/commands, portal/runner credentials |
| Curriculum author | Edit exact Issue #11-owned content in an authorized cook | Shared contract/portal/toolchain/root/cloud changes |
| Released Issue #8 authority | Define schema, prerequisite, lifecycle, completion, evidence, operation truth | Portal rendering implementation |
| Released Issue #10 portal | Render/discover released content and mediate released local journey | Curriculum contract invention or privileged direct execution |
| Issue #6 architecture toolchain | Validate/render protected local source and, after Gate A2, the proposed expansion seam | Portal completion or AWS deployability |
| Stage implementer | Execute one exact closed allow-list in one worktree | Rebase/merge around drift, expand authority, approve own merge |
| Independent reviewer | Validate implementation and evidence at exact head | Synthetic human approval |
| Human approver | Explicit exact-head pre-merge decision | Waiving failed tests/dependencies/security by implication |

Trust boundaries:

1. Plan → exact amendment/readiness authority.
2. Issue #11 static schemas/content → released Issue #8 contracts and validators read-only.
3. Static architecture expansion → protected Issue #6 sources/toolchain/renders.
4. Browser/portal → released Issue #10 same-origin renderer/BFF boundary.
5. Portal/BFF → private released execution boundary; browser never receives privileged authority.
6. Workspace → repository/protected dependency bytes.
7. Evidence staging → ignored app-owned or approved external private root → immutable retained
   evidence/index; nonignored worktree cleanliness remains separate.
8. Local content/model → AWS teaching boundary; no live account/network/action.

## Threat and Control Register

| ID | Threat / abuse case | Stage | Required control and negative evidence | Residual / STOP |
|---|---|---|---|---|
| I11-T-01 | Draft dependency or mutable branch substituted for release | A/B | Fresh merge ancestry, blob SHA-256, external release attestation; reject known plan/readiness heads | Any mismatch STOP |
| I11-T-02 | Duplicate/forked lesson, progress, completion, evidence, operation, or renderer truth | A/B | Read-only consumption; exact import/reference inventory; no schema/validator/route copy | No fallback authority |
| I11-T-03 | Malformed/malicious content escapes schema or renderer | A/B | I5-06 schema plus released dependency validation, bounded input size/depth/count, duplicate-key/I-JSON checks, safe text rendering | Raw HTML/script path STOP unless exact renderer contract safely owns it |
| I11-T-04 | Traversal, symlink, hardlink, special file, absolute/private path in content/starter/solution/evidence | A/B | Stage A exact regular-file allow-list; Stage B released workspace containment; relative locators only | Containment downgrade STOP |
| I11-T-05 | Learner/browser forges progress, completion, verifier result, or evidence | B | Issue #8 sole server authority; fresh exact verifier; digest/index checks; reflection/solution/local storage cannot complete | Local same-user non-repudiation not claimed |
| I11-T-06 | Reset races verify/evidence or erases prior evidence | B | Released idempotency/CAS/lock/reconciliation; barrier/process-kill/retry tests; evidence preserved | Unclear commit point STOP |
| I11-T-07 | Portal content or evidence causes XSS/session/operation abuse | B | Exact released renderer; escaping/sanitization/CSP/download rules; hostile content tests; no portal-source workaround | Missing safe seam STOP |
| I11-T-08 | Browser gains runner/service token or calls private runner | B | Same-origin portal/BFF only; no token in Web Storage/URL/content/evidence; Host/Origin/CSRF/CORS rules from release | Direct browser path STOP |
| I11-T-09 | Pattern without failure/evidence normalizes unsafe design theater | A/B | Admission predicate and `pattern-without-failure` negative fixture | Generic prose cannot clear |
| I11-T-10 | Architecture expansion shadows/changes protected six | A/B | Exact source/row/render/tool hashes, unique IDs/keys/paths, semantic overlap check | Any protected drift STOP |
| I11-T-11 | SVG/text embeds scripts, external URLs/images, private paths, credentials, or misleading hidden content | A | Parser/normalizer policy, semantic text comparison, high-confidence scans | Fail artifact; no silent redaction to pass |
| I11-T-12 | AWS teaching material is mistaken for a real/deployed/secure/zero-cost platform | A/B | `architecture-content-only` and `TBC — blocks aws-apply`; no account IDs/endpoints; no apply/credential command | Any deployment claim STOP |
| I11-T-13 | OpenAPI/AsyncAPI curriculum invents unowned operations/channels or drives service proliferation | A | Exact #8 operation/channel inventory; no duplicate specs; taxonomy-versus-physical checks | Missing real contract rejects topic |
| I11-T-14 | Evidence/log includes environment dump, home/user path, token, private URL, raw identifier, or unbounded output | A/B | Allow-listed schema fields; size bounds; canary/private-path/credential scans; store minimal failure hash only | Detection fails run |
| I11-T-15 | Cleanup/rollback deletes foreign worktree, dependency, protected render, or evidence | A/B | Exact stage manifest, owner marker/nonce/inode, no broad recursive delete, preserve immutable evidence | Ownership ambiguity STOP |
| I11-T-16 | Concurrent contract/view/portal writer creates mixed generation | A/B | Serialized lease, exact base/owner/duration, no stale lease auto-break, atomic full-set publication | Active/stale lease requires human inspection |
| I11-T-17 | Required validator/renderer missing and a newer/global/browser/native tool is used | A/B | Exact released tool/lock/integrity; missing tool = fail; network denied after bounded bootstrap | No silent fallback |
| I11-T-18 | Automated result is presented as human review/approval | A/B | Separate implementation review and human exact-head attestation outside evidence producer | Missing attestation blocks merge |
| I11-T-19 | Impossible pristine tests-only rule produces a common behavior-absent guard | A | Exact 7-path semantics-free scaffold, direct-child complete 5-path tests, four-entrypoint named semantic RED, commit/AST inspection | Any precondition-only RED STOP |
| I11-T-20 | Promotion decision/reason drifts while grain checks still pass | A | Exact released schema constants and independent decision/reason mutations | Any drift STOP |
| I11-T-21 | Template count hides unregistered copies or unsafe version removal | A | Exact registry tokens, compatibility, reciprocal instance ID/version/hash, supersession/removal negatives | One-way/unregistered binding STOP |
| I11-T-22 | Generic flow steps or conceptual AWS mapping assert runtime truth | A | Exact 11 relation-order/topology bindings and eight conceptual-only bridge records | Prefix/generic/runtime-bridge pass STOP |
| I11-T-23 | Timed-out renderer leaves descendants or breaches host resources | A | Owned PGID, 120 s/180 s, aggregate RSS/output/file/process bounds, TERM→KILL→wait, measurements | Missing ownership/measurement STOP |
| I11-T-24 | Fresh SVG is unreadable, English-first, double-numbered or semantically reordered | A | Exact fit/font/contrast/aspect/geometry/language/numbering/text-parity gates plus independent static inspection | Any five-view visual failure STOP |
| I11-T-25 | Exit-0 Git status masks nonignored evidence or unowned ignored bytes | A/B | Private ignored/external root, zero-byte nonignored porcelain, ignored-inclusive ownership delta, closed index | Ambiguous/dirty handoff STOP |

## Stage A Security Contract

Future Stage A is content/static only under the exact released #8 binding and the independently
validated/readiness-authorized view lease.

- Future implementation begins only from clean `c07c9a0…` plus the exact independently
  validated/audited plan-only diff. The current author output grants no cook authority.
- Create only the exact seven generic public scaffold files first; they contain no target rules,
  fixture IDs, final content, hardcoded result, mock/skip, expected-value echo, or unconditional
  not-implemented branch. Complete tests follow and must reach all four entrypoints before named
  semantic RED.
- No portal renderer dependency read or portal path write.
- No executable lab, privileged command, progress/completion mutation, workspace runner, or fresh
  learner evidence claim.
- Validate I5-06 content through its machine-valid schemas and read-only released Issue #8
  validators where applicable. Do not copy released validator/schema source.
- The isolated I5-06 expansion adapter consumes the exact Issue #6 locked toolchain read-only and
  maps only five extension rows. No Java, Structurizr fallback, browser/Playwright/native GUI,
  native Graphviz, `npx`, global tool, or unpinned network resolver.
- Network is allowed only for the exact released digest/lock-verified Python and Node bootstrap.
  Rendering and validation are offline afterward.
- Scan Vietnamese/English content, YAML/JSON, SVG/text, manifests, evidence metadata, and staged
  diff for secrets/private paths/cloud actions.

## Stage B Security Contract

Stage B adds one bounded architecture lab through released #8/#10 interfaces.

- Browser never calls a runner or privileged service directly and never receives service tokens.
- Inputs are structured architectural choices/IDs, not shell, raw SQL, paths, environment, URLs,
  cloud variables, or Terraform arguments.
- Starter/task/hints/solution are project-owned and size/path bounded. Solution reveal cannot
  mutate verifier or completion.
- Controlled failure has a stable released-compatible code and is distinct from environment or
  unexpected failure. An environment failure cannot advance progress.
- Reset is idempotent, scoped, evidence-preserving, and proves the exact starter oracle.
- Verify uses released deterministic assertions and produces evidence through the one Issue #8
  authority. Browser state, reflection, elapsed time, scroll position, solution presence, or an
  imported bundle never completes.
- Process kill, duplicate request, delayed result, retry, stale evidence, tampered content, and
  cleanup failures are mandatory negative scenarios when supported by exact released semantics.

## Evidence Integrity and Redaction

Stage A retained evidence root:

```text
.claude/evidence/issue-11-stage-a/<run-id>/
```

The released ignore rule already covers `/.claude/`; no ignore change is authorized. A separately
approved external mode-0700 app-state root may substitute. Nonignored `.artifacts/**` is forbidden.
These use the existing `fitness-result-v1` command envelope and released canonicalization rule.
They do not emit Issue #8 learner evidence. Required logical fields include schema version, exact
commands, tool versions, plan/scaffold/tests/RED/first-semantic/final SHAs, dependency merge SHAs,
contract/fixture hashes, resource/visual/porcelain measurements, result status, artifact hashes,
redaction class, ownership/index closure, and rollback result.

- Use SHA-256 for byte integrity and the released canonicalization rule for structured payloads.
- Local hashes detect corruption/inconsistent edits only. Do not claim signing, authorship,
  anti-forgery, or non-repudiation.
- Evidence never contains full environment dumps, credentials, cookies/tokens, private URLs,
  absolute local paths, raw Terraform plan/state, cloud IDs, or unnecessary synthetic row IDs.
- On sensitive-content detection, fail and retain only a bounded reason plus offending-content
  hash. Do not replace a secret with placeholder text and report pass.

## Security Scan Classes

Every planner/future stage scans exact staged/candidate files for:

- PEM/private key markers; AWS access key/session/secret patterns; GitHub/npm/token/password
  assignments; credential-bearing URLs;
- macOS/Linux/Windows home-directory prefixes, local-file URI schemes, workspace absolute paths,
  usernames, and private registry/proxy/endpoint values;
- `terraform apply|destroy`, `aws ... create|delete|put`, cloud SDK apply/provision calls, Docker or
  shell execution in curriculum content represented as runnable Issue #11 commands;
- `<script`, `foreignObject`, external SVG image/link URLs, event-handler attributes;
- unexpected binary/large artifacts and generated runtime/evidence files in Git index.

Tutorial prose may mention forbidden commands only as explicit “not authorized” examples and must
not expose a copy-paste execution route. Scanner exceptions are exact-line, reviewed, and retained
as evidence; broad ignore patterns are forbidden.

## Cleanup and Rollback

- Plan phase: no runtime cleanup.
- Cook runs allocate one exact ignored app-owned or approved external retained root plus a
  separate temporary runtime root using an exact owner marker. Roots/directories are 0700,
  retained files 0600, and no caller-chosen arbitrary root or absolute locator enters evidence.
- Cleanup removes only the run’s mutable workspace/temporary render staging after marker,
  identity, manifest, and boundary verification. It never invokes root `make clean`, deletes a
  worktree, follows links, scans broad roots, or deletes retained evidence.
- Rollback restores the exact prior curriculum/expansion set and shared manifest state as one
  reviewed unit; removes only newly authorized Issue #11 candidate bytes; reruns protected hashes;
  retains failure and rollback evidence.
- If rollback cannot preserve the protected six, dependency contracts, portal renderer, prior
  evidence, and unrelated data, the stage cannot begin.
- Final clean handoff requires exit 0 and zero stdout bytes from nonignored porcelain. A separate
  NUL-terminated ignored-inclusive inventory must classify every record as pre-existing unchanged
  or exact retained-owned evidence; exit 0 alone and ignored omission never mean clean.

## Residual Risks

- A same-account/root actor can replace local bytes and recompute unkeyed hashes. Accepted within
  the local single-actor model; no authenticity claim.
- A crash can leave a scoped failed workspace or lease requiring verified manual inspection.
- Static Stage A cannot prove learning effectiveness or runtime lifecycle; those claims wait for
  Stage B plus later human curriculum review.
- AWS topology/cost/security remain design teaching, not provider compatibility or deployment
  evidence.

## Security Exit Criteria

- Every I11-T row maps to a negative test or explicit stage-blocking control.
- No Critical/High unresolved finding within the authorized stage.
- Protected/secret/private-path/cloud-action scans pass on the exact staged head.
- Cleanup/rollback rehearsal is bounded and evidence-preserving.
- Independent implementation security review and repository-authorized human exact-head approval
  exist before any future merge.

## Unresolved Questions

None for Stage A. Exact Issue #10 portal/lifecycle security semantics remain Stage B blockers.
