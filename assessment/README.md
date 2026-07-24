# AI-ready assessment Phases 1–3

This isolated Python 3.12 package proves the Issue #38 rubric, scoring/gates, synthetic
calibration, v1 public contracts, authoritative local engagement folders, prototype migration,
safe deterministic portability, and the final deterministic engine and canonical report
generation. It is deliberately offline after dependency installation and does not import,
scan, or control the retail data platform.

From the repository root:

```bash
make assessment-install
make assessment-schema assessment-contract
make assessment-scenarios assessment-calibration
make assessment-report assessment-test
make assessment-store assessment-migration assessment-import-export
make assessment-portability assessment-security-scan
make assessment-engine
make assessment-lint assessment-typecheck assessment-build
```

`assessment-install` is the only Phase 1 target that acquires Python dependencies. It creates
the separate `.assessment-venv` from hash-locked files. The other targets use
`assessment/tools/run-offline.sh` to deny outbound network access with the audited macOS
runtime's `sandbox-exec`; they use local files and start no services or containers.

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
Terraform, SQLite authority, cloud resource, FastAPI/browser workflow, catalog/diagram, golden
pipeline, customer data, or deployment behavior in Phases 1–3. Phases 4–8 remain pending.
