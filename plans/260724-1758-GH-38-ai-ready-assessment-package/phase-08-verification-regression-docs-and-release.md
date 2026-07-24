# Phase 8: Verification, regression, documentation, and release readiness

## Context links

- Parent: [plan.md](./plan.md)
- Dependencies: [Phases 1–7](./plan.md#delivery-phases)
- Decisions: [all plan decisions](./architecture-decisions.md)
- Traceability: [all AC and SM rows](./requirements-traceability.md)
- Current docs: repository `README.md`, `docs/system-architecture.md`, `docs/demo-runbook.md`, `versions.md`

## Overview

- Date: 2026-07-24
- Description: Execute portability, security, resource, regression, clean-checkout, documentation, compatibility, rollback, and release verification.
- Priority: P2
- Implementation status: Pending
- Review status: Final implementation review; independent authorization/audit status must be reported separately and truthfully.

## Key Insights

- A green unit suite does not prove a portable engagement or installable package.
- Assessment verification is lightweight by default; live golden proof is a separate staged run.
- Existing data-platform behavior is a public compatibility boundary.
- Durable evidence belongs under tracked `docs/verification/`, not ignored plan/runtime directories.

## Requirements

- Exact/discoverable install, unit, schema, semantic, scenarios/calibration, import/export, report, lint, typecheck, build, browser, clean-checkout, secret/path, cleanup, and existing-regression commands.
- Full different-path export/import/reopen/report roundtrip and deterministic ZIP/report checks.
- Secret/credential/URI and POSIX/macOS/Windows absolute-path scans.
- Resource-safe heavy verification with current Compose limits and no assessment-triggered profiles.
- Additive compatibility/migration, rollback, generated-data cleanup preserving engagements.
- User/maintainer docs, multiple audience diagrams, version matrix, release manifest/package content, and tracked empirical evidence.
- No cloud/GitHub publication, deployment, label changes, or destructive infrastructure action.

## Architecture

Verification has three independent lanes:

1. **Assessment lane:** fresh `.assessment-venv`, pinned Chromium, and the build-only locked Mermaid toolchain are bootstrapped from declared locks (network may be used only for these three acquisitions unless verified caches are supplied); contracts/unit/scenarios/report/archive/security/build/diagram-parity/e2e/runtime-smoke then run with outbound network blocked and no Docker.
2. **Core compatibility lane:** existing `.venv` and `make seed SCALE=small SEED=42 && make load && make health && make dbt && make bi`; no containers.
3. **Optional golden live lane:** Airflow, lake, and governance staged as documented; only existing guarded lake+governance window.

`make assessment-clean-checkout` creates a temporary git worktree at the implementation commit, never the repository root/home, bootstraps the locked assessment dependencies, browser, and build-only diagram toolchain with an explicit online-or-verified-cache mode, then blocks outbound network while running the assessment and core compatibility commands. It captures versions/results and removes the explicit temporary worktree on success/failure. It does not use `git reset --hard`, AWS, Terraform, GitHub mutation, or undeclared hidden local state.

Durable evidence: `docs/verification/GH-38-assessment-package-evidence.md` records commit, platform, commands, exit summaries, scenario/calibration metrics, portability digests, standalone report render, archive/security findings, resource staging, core regression, known limitations, and cleanup. It never records tokens, customer content, absolute home paths, or claims beyond executed proof.

## Related code files

- Modify: `Makefile` for the complete assessment target contract in `architecture-decisions.md`
- Create: `assessment/scripts/{verify-clean-checkout.sh,scan-export-hygiene.py,verify-package.py}`
- Create/modify: all `assessment/tests/` lanes and fixtures needed to close traceability
- Modify: `.gitignore` for `.assessment-venv/`, package/cache/browser/generated demo artifacts only
- Modify: `README.md`, `docs/system-architecture.md`, `docs/demo-runbook.md`, `versions.md`
- Create: `docs/assessment-guide.md`, `docs/assessment-framework.md`, `docs/engagement-portability.md`, `docs/verification/GH-38-assessment-package-evidence.md`
- Modify: `release-manifest.json` if this repository uses it to enumerate shipped package/docs
- Verify: `docker-compose.yml` limits remain Airflow 4g; MinIO 1g/init 256m; Lakekeeper DB/migration 512m/server 1g; OpenMetadata DB 1g/search 1g/server 2g

## Implementation Steps

1. Complete the Make target help/contract and prove each target invokes only the intended isolated environment. Exact assessment gate:
   ```bash
   make assessment-install
   make assessment-browser-install
   make assessment-diagram-install
   make assessment-schema assessment-contract
   make assessment-test
   make assessment-scenarios assessment-calibration
   make assessment-import-export assessment-report
   make assessment-lint assessment-typecheck assessment-build assessment-diagrams
   make assessment-e2e assessment-runtime-smoke
   ```
   The first three bootstrap commands may fetch only hash/version-pinned artifacts. All subsequent commands run with network denied; a no-network bootstrap is claimed only with supplied verified caches.
2. Run portability: create a complete synthetic engagement through the UI, generate report, export, copy ZIP and unpacked folder to two distinct temporary absolute roots, import/reopen, regenerate, compare canonical source/report digests, and verify deterministic ZIP bytes via `make assessment-portability`.
3. Run hostile archive/export hygiene corpus via `make assessment-security-scan`: traversal, archive/pre-existing/destination symlink, absolute/drive/UNC, Unicode/case/destination duplicate, excessive count/depth/file/expanded-total/compression ratio, encrypted/unsupported ZIP features, unknown-newer version, corrupt checksum, opaque evidence, PEM/token/key/entropy markers, credentialed URI, `/Users/`, `/home/`, `file://`, `C:\`, `C:/`, and `\\server\share`.
4. Run no-demo and demo-mutation tests, `make assessment-runtime-smoke` standalone HTML/JSON artifact journey with browser network blocked, CSRF/headers/loopback/upload tests, single-worker browser bounds, wheel/sdist install/content checks, and prove assessment tests never invoke Docker/`make airflow`/`lake`/`catalog`.
5. Run existing core regression exactly:
   ```bash
   make seed SCALE=small SEED=42
   make load
   make health
   make dbt
   make bi
   ```
   Compare 18 raw tables, 51 dbt models, canonical 11 marts, Rill exports, and existing command behavior with baseline contracts.
6. Run golden verification in resource-safe stages: `make demo-contract demo-verify`; `make demo-airflow-verify` (which must trigger/poll the default DAG and tear down); `make lake-up && make lake-publish && make down`; then `make catalog-ingest` only after Airflow stops, followed by `make down`. Preserve the sole guarded lake+governance co-run and record corrected memory limits. If credentials/local service availability prevent the OpenMetadata rerun, record that stage as unexecuted and do not close the all-stage metric from process exit; previously tracked GH-3 evidence may be linked as historical proof only.
7. Run `make assessment-clean-checkout` from a fresh temporary worktree at the implementation commit. Rebuild both venvs from declared inputs, provision the pinned browser and build-only Mermaid toolchain in explicit online-or-cache mode, then execute network-blocked assessment and core compatibility lanes with no reliance on undeclared ignored artifacts.
8. Verify compatibility and migration matrix: v0.1 prototype imports/migrates to v1, v1 roundtrips, unknown newer rejects non-mutatingly, old existing Make commands remain, public data assets do not drift unintentionally, and report/content schema versions are pinned.
9. Verify cleanup/rollback: place an engagement sentinel, run `make assessment-clean`, confirm only generated report/cache/tmp/browser/build artifacts are removed and source/evidence/sentinel remain; run existing `make down`; run `make clean` only after copying/preserving engagement root and verify it does not target engagements.
10. Update the smallest owning documentation surfaces: quick start/user workflow, framework/gates/confidence, portable folder/import safety, architecture/core separation, Demo Guide/staging, seven audience diagrams, tested dependencies/resources, limitations, cleanup/rollback.
11. Build distribution and verify installed CLI/content/templates/schemas/static assets; update release manifest/version evidence as repository convention requires. Do not publish a package, deploy, push, open PR, create issues, or change GitHub labels.
12. Write tracked empirical evidence from actual command outputs, close every traceability row, record unresolved failures/limitations, and request independent final review. Do not state “ready to cook” or independent-audit pass unless an authorized external result actually exists.

## Todo list

- [ ] Run every post-bootstrap network-blocked assessment gate.
- [ ] Prove copied-folder/ZIP portability and deterministic reports/archives.
- [ ] Pass hostile archive, secret, URI, and cross-platform path scans.
- [ ] Pass browser/runtime-artifact/security/package isolation tests.
- [ ] Pass exact existing core data-platform regression.
- [ ] Run optional heavy proof only in staged resource-safe order.
- [ ] Pass fresh temporary-worktree verification.
- [ ] Prove migration/compatibility and cleanup preservation.
- [ ] Update user, maintainer, architecture, portability, demo, version, and diagram docs.
- [ ] Verify built distribution contents and release manifest.
- [ ] Publish tracked verification evidence and close traceability.
- [ ] Request independent review without asserting its result.

## Success Criteria

- All commands in Steps 1–7 pass from declared dependencies; only the three explicit bootstrap targets may fetch pinned artifacts, and subsequent assessment tests make no network or heavy-service calls.
- Portability roundtrip preserves all source state and regenerates identical canonical report data; ZIP/report determinism passes.
- Zero secrets, credentialed URIs, or absolute POSIX/macOS/Windows paths occur in exported engagement content.
- Malicious/unsupported archives reject before destination mutation.
- Existing 18-table/51-model/11-mart core path and public Make commands regress green.
- Airflow proof triggers/polls a real DAG run; heavy proof respects one-profile sequencing and the sole guarded lake+governance exception; documented Compose limits match source.
- Cleanup removes generated assessment artifacts while preserving engagements/evidence; rollback is documented and tested.
- Built package includes schemas/content/templates/static assets and works in a clean worktree.
- All 12 issue criteria and 17 success metrics have executed evidence or an explicit blocking failure; no unsupported audit/release claim is made.

## Risk Assessment

- Clean-checkout scripts can delete the wrong path; create with `mktemp -d`, validate explicit worktree path, trap cleanup, and never target root/home/current repository recursively.
- Local ignored artifacts can mask packaging omissions; install built wheel in fresh worktree/venv and enumerate contents.
- Heavy tests may be unavailable on some machines; separate offline release gate from optional live proof, but do not mark golden-stage acceptance complete without recorded live evidence.
- Documentation can overstate controls; align every claim with test/manifest evidence and retain limitations.
- Release manifest updates can accidentally absorb secrets/runtime files; generate candidate list, review, scan, then update only intended tracked files.
- Rollback: withdraw the un-published build, restore the previous framework/catalog version pointers and release manifest, run `make down` plus generated-artifact cleanup, and reopen preserved engagements with the last compatible reader. Any schema rollback is read-only/export-first, never an in-place downgrade.

## Security Considerations

Run dependency/audit tooling offline where lock/cache supports it and document the limitation; do not fetch or upload customer content. Redact temp roots/usernames from durable evidence. Use synthetic fixtures only. No AWS/Terraform apply/destroy, credentials, hosted binding, publication, customer scan, arbitrary SQL/command execution, or GitHub/cloud mutation is part of verification.

## Next steps

Submit the complete implementation and empirical evidence for independent review. Address evidence-backed findings without reversing verified/user decisions silently. Implementation authorization and any GitHub/release action remain separate owner-controlled steps.
