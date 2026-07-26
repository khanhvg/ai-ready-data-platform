# AI-ready assessment Phases 1–6

This isolated Python 3.12 package proves the Issue #38 rubric, scoring/gates, synthetic
calibration, v1 public contracts, authoritative local engagement folders, prototype migration,
safe deterministic portability, and the final deterministic engine and canonical report
generation. Phase 4 adds a local server-rendered architect workflow without adding a pipeline
control surface. Phase 5 adds a versioned capability, architecture, technology-option, diagram,
and Demo Guide catalog without changing assessment truth. It is deliberately offline after
dependency and pinned-browser/diagram-tool installation
and does not control the retail data platform. Phase 6 displays validated repository-relative
golden evidence and manifests through the same read-only, non-scoring boundary.

From the repository root:

```bash
make assessment-install
make assessment-schema assessment-contract
make assessment-scenarios assessment-calibration
make assessment-report assessment-test
make assessment-store assessment-migration assessment-import-export
make assessment-portability assessment-security-scan
make assessment-engine
make assessment-browser-install assessment-diagram-install
make assessment-diagrams
make assessment-e2e assessment-runtime-smoke
make assessment-lint assessment-typecheck assessment-build
```

`assessment-install` is the only Phase 1 target that acquires Python dependencies. It creates
the separate `.assessment-venv` from hash-locked files. The other targets use
`assessment/tools/run-offline.sh` to deny outbound network access with the audited macOS
runtime's `sandbox-exec`; they use local files and start no containers. The two browser targets
start and stop their own real loopback server and Chromium while a second sandbox profile denies
non-loopback network access.

`assessment-diagram-install` is the only target allowed to provision the exact npm dependencies
for diagram builds. It uses the committed npm v3 lock with Node 22/npm 10.9.8 and does not place
Node tooling in the Python package. The existing browser install target supplies the pinned
Chromium build. `assessment-diagrams-update` is the explicit regeneration target;
`assessment-diagrams` performs adversarial renderer tests plus two deterministic renders and
non-mutating parity checks under the loopback-only network sandbox.

## Local architect workflow

Install the pinned Python environment and the repository-scoped Chromium build, then start the
single-worker server:

```bash
make assessment-install
make assessment-browser-install
make assessment-web
```

Open `http://127.0.0.1:8765`. Override engagement and runtime roots with
`ASSESSMENT_ENGAGEMENT_ROOT` and `ASSESSMENT_RUNTIME_ROOT`; override the loopback port with
`ASSESSMENT_PORT`. A literal non-loopback host fails closed. The CLI exposes
`--allow-unsupported-non-loopback` only as an explicit unsupported development escape hatch;
it is not a hosted or deployment mode.

The workflow supports local engagement create/list/open, all 30 quick questions, explicit
readiness facts, evidence status and attachment-only evidence, visible autosave/revision state,
review and architect finding dispositions, deep-dive planning, deterministic reports, and
bounded archive preflight/import into a different configured root. Every operation also works
through ordinary POST/Redirect/GET forms with JavaScript disabled. JavaScript only serializes
autosave requests and improves disclosure/status feedback.

Deep dives are selection records only. Their question banks remain honestly
`planned-content-pending`/`not-installed` until Phase 7. Catalog and demo pages are read-only
views of validated package assets; unavailable repository evidence stays visibly unavailable.
The catalog contains exactly ten capability domains, nine vendor-neutral logical patterns,
an AWS-first content-only option set, a separate read-only local sandbox mapping, deferred
alternatives, and seven reviewed accessible SVG/source pairs. The Demo Guide contains nine
presenter stages with prerequisites, repository-relative artifact locations, expected evidence,
limitations, cleanup, and an explicit non-scoring disclaimer. There
is no run, command, SQL, credential, network-fetch, pipeline, Docker, cloud, or deployment route.

The app uses signed ephemeral local sessions, signed CSRF tokens, host/origin checks, optimistic
revision checks under the engagement writer lock, strict upload and archive limits, escaped
templates, attachment-only evidence responses, local static assets, CSP and related secure
headers. It binds to `127.0.0.1` by default.

`make assessment-e2e` runs one Playwright worker through the complete synthetic Solution
Architect journey. `make assessment-runtime-smoke` repeats that same real journey and retains
ignored standalone report, archive, imported-report, screenshot, transcript, result, and digest
evidence under `assessment/.generated/runtime-smoke/`. It proves 30 answers, all seven gate
traces, deep-dive pending state, deterministic export/import/reopen equality, no-JavaScript
completion, catalog/Demo Guide wide and narrow reflow, seven local diagrams, honest
available/unavailable artifact status, browser back/reload behavior, no remote browser requests,
and clean server/browser teardown.

Prototype scenario reports are written to the ignored
`assessment/.generated/prototype/<scenario>/` tree. Each scenario has top-level canonical
artifacts for Architect A plus explicitly labeled `architect-a/` and `architect-b/` artifacts
for calibration inspection. Source fixtures and the migration freeze manifest remain tracked.

## Deterministic engine and reports

Package `0.3.0` adds pure maturity and coverage aggregation, independent confidence summaries,
complete operand-level traces for the pinned seven-gate bundle, deterministic findings and
recommendations, a canonical source-state digest, and exactly 12 ordered report sections.
Architect review state remains separate from generated engine truth, and demo illustration
references cannot change maturity, confidence, priority, gates, or readiness.

The final CLI never infers a workspace. Both commands require an existing engagement folder and
an explicit output directory:

```bash
.assessment-venv/bin/python -m assessment evaluate \
  --engagement-root /absolute/path/to/engagement \
  --output-root /absolute/path/to/evaluation-output

.assessment-venv/bin/python -m assessment report \
  --engagement-root /absolute/path/to/engagement \
  --output-root /absolute/path/to/report-output
```

`evaluate` writes canonical `assessment-result.json`. `report` writes canonical `report.json`,
byte-stable standalone `report.html`, and a last-written `report-manifest.json` that binds the
two required report artifacts by digest. Publication failure restores the prior coherent set.
HTML has embedded CSS, no script or remote resources, and no manual-edit step. Output roots may
not alias the engagement source state; failures are machine-readable on stderr and return
nonzero.

The installed package carries all seven public v1 JSON Schemas under
`assessment.public_schemas`. `assessment schema` validates that installed authority, while
`assessment schema --repo-root <checkout>` validates the repository authority. Either form
fails when the complete seven-schema authority is unavailable; wheel and sdist build checks
also require exactly those seven schema files.

## Portable engagement authority

`LocalEngagementStore` owns one explicit root. Engagement IDs and document keys are validated
stable IDs/relative POSIX paths. JSON writes use adjacent temporary files, file fsync, atomic
replace, and parent-directory fsync where the operating system supports it. Per-engagement
writer locks reject concurrent mutation; stale adjacent temporary files are recoverable without
changing the last valid document.

Every root path component must be a real directory; symlink components are rejected to prevent
filesystem race redirection. On macOS, use the canonical `/private/var/...` spelling rather than
the `/var` compatibility symlink when selecting a root below the system temporary directory.

The `0.1.0-prototype -> 1.0.0` registry transforms frozen synthetic fixtures without modifying
their source. It writes a deterministic receipt and fails unknown versions before creating a
destination.

Exports use sorted NFC names, canonical content, normalized modes/timestamps, `ZIP_STORED`, and
a canonical SHA-256 manifest. Per-file and total expanded-byte limits apply to the canonical
bytes actually stored, including generated checksums and the manifest. V1 admits inspectable
UTF-8 text/JSON/CSV and metadata-free PNG/JPEG evidence. Import validates all names, ZIP
features, limits, hashes, versions, content hygiene, and destination state before writing a
sibling stage and atomically promoting it.

```bash
.assessment-venv/bin/python -m assessment export ENGAGEMENT_ROOT engagement.zip
.assessment-venv/bin/python -m assessment import engagement.zip NEW_ENGAGEMENT_ROOT
.assessment-venv/bin/python -m assessment migrate prototype-fixture.json NEW_ENGAGEMENT_ROOT
```

The future object-store boundary is documentation-only in
`assessment/docs/object-engagement-store.md`. There is no SDK, S3 upload, credential, bucket,
Terraform execution, SQLite authority, cloud resource, customer data, or deployment behavior.
The AWS profile is content only and the local demo mapping is read only. Phase 6 adds
deterministic local retail evidence, a fixed application policy export, and versioned manifests
outside assessment truth; Phases 7–8 remain pending.
