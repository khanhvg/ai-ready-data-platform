# AI-ready assessment Phase 1 prototype

This isolated Python 3.12 package proves the Issue #38 rubric, scoring/gates, synthetic
calibration, and canonical report shape. It is deliberately offline after dependency
installation and does not import, scan, or control the retail data platform.

From the repository root:

```bash
make assessment-install
make assessment-schema assessment-contract
make assessment-scenarios assessment-calibration
make assessment-report assessment-test
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

This slice does not provide engagement storage/migration services, import/export, FastAPI,
browser workflow, catalog/diagrams, golden-pipeline integration, cloud actions, or deployment.
