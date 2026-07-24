# AI-ready assessment Phases 1–2

This isolated Python 3.12 package proves the Issue #38 rubric, scoring/gates, synthetic
calibration, canonical report shape, v1 public contracts, authoritative local engagement
folders, prototype migration, and safe deterministic portability. It is deliberately offline
after dependency installation and does not import, scan, or control the retail data platform.

From the repository root:

```bash
make assessment-install
make assessment-schema assessment-contract
make assessment-scenarios assessment-calibration
make assessment-report assessment-test
make assessment-store assessment-migration assessment-import-export
make assessment-portability assessment-security-scan
make assessment-lint assessment-typecheck assessment-build
```

`assessment-install` is the only Phase 1 target that acquires Python dependencies. It creates
the separate `.assessment-venv` from hash-locked files. The other targets use
`assessment/tools/run-offline.sh` to deny outbound network access with the audited macOS
runtime's `sandbox-exec`; they use local files and start no services or containers.

Generated reports are written to the ignored
`assessment/.generated/prototype/<scenario>/` tree. Each scenario has top-level canonical
artifacts for Architect A plus explicitly labeled `architect-a/` and `architect-b/` artifacts
for calibration inspection. Source fixtures and the migration freeze manifest remain tracked.

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
a canonical SHA-256 manifest. V1 admits inspectable UTF-8 text/JSON/CSV and metadata-free
PNG/JPEG evidence. Import validates all names, ZIP features, limits, hashes, versions, content
hygiene, and destination state before writing a sibling stage and atomically promoting it.

```bash
.assessment-venv/bin/python -m assessment export ENGAGEMENT_ROOT engagement.zip
.assessment-venv/bin/python -m assessment import engagement.zip NEW_ENGAGEMENT_ROOT
.assessment-venv/bin/python -m assessment migrate prototype-fixture.json NEW_ENGAGEMENT_ROOT
```

The future object-store boundary is documentation-only in
`assessment/docs/object-engagement-store.md`. There is no SDK, S3 upload, credential, bucket,
Terraform, SQLite authority, cloud resource, FastAPI/browser workflow, catalog/diagram, golden
pipeline, customer data, or deployment behavior in Phase 2.
