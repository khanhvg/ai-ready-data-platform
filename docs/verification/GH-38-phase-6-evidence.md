# Issue 38 Phase 6 verification evidence

Date: 2026-07-26

This record covers only the bounded golden-retail evidence and manifest slice.
Its immutable implementation input is
`7687a666cce3f533d4adac542ada34037b91ed8c`. The exact published and tested
implementation commit is recorded in the Phase 6 pull request and Issue 38
comment after the commit exists.

All data used here was generated locally with `SCALE=small SEED=42`. No
customer data, cloud API, credential, account, upload, deployment, Terraform
apply/destroy, object-store implementation, or named-volume deletion was used.

## Policy compatibility and data evidence

The PD-16 compatibility spike ran with Python 3.12.3 and DuckDB 1.5.4 before
product implementation. The corrected real-interface harness proved:

- raw, staging, classified-email, unknown-role, and unknown-asset requests
  exited nonzero;
- `--sql` and `--output-path` were rejected by argument parsing;
- the fixed safe role/asset request succeeded with the declared nine-column
  schema;
- the fixed entrypoint accepted no SQL, database path, output path, relation,
  or shell input.

The current `make demo-verify` result is seven denied decisions, one allowed
decision, and 990 safe output rows. The local application boundary is not
DuckDB IAM: a machine owner can open the database directly.

The exact core sequence exited zero:

```text
make seed SCALE=small SEED=42
make load
make health
make dbt
make dbt-docs
make bi
make demo-contract
make demo-verify
```

The generator produced 6,812 rows across 18 source tables. The dbt graph
contained 54 models, including six ephemeral models; dbt executed 48
materialized models and 164 tests. The final result was PASS=205, WARN=7,
ERROR=0, SKIP=0, TOTAL=212. The complementary partition contained 990
accepted orders and 10 quarantined orders over 1,000 deduplicated staged
orders, with zero overlap and zero quarantined keys in the governed product.
The product contained no raw email or raw customer/order identifier. The
canonical publication inventory remained exactly 11 legacy business marts.

The nine stage manifests and AI-ready dataset manifest validated against the
versioned public schemas and semantic checks. Automation is derived from every
run and cleanup row, then reconciled to the Demo Guide’s explicit numerator and
denominator; the current result is 30/30 (100%). Demo evidence remains
non-scoring.

## Staged local profiles

`make demo-airflow-verify` exited zero after starting Airflow alone. Import
errors were empty, the exact run ID was
`phase6__20260726T124806Z`, and all six default DAG tasks reached terminal
`success`:

- `generate.seed`
- `load.load_raw`
- `load.health_check`
- `transform.dbt_build`
- `transform.dbt_docs_generate`
- `serve.export_marts_snapshot`

The verifier always ran `make down`; the final Compose service list was empty.

The lake sequence ran only after Airflow stopped:

```text
make lake-up
make lake-publish
make lake-publish
make down
```

Both publication runs exited zero. Each published and read back all 11
canonical marts with nonzero rows. The second run proved sequential
idempotence. A fresh local Lakekeeper database initially exposed the existing
missing-bootstrap defect; the publisher now uses the supported management API,
rechecks the required default project, and fails closed otherwise. Final
teardown left no Compose services and retained named volumes.

`OPENMETADATA_JWT_TOKEN` was absent. Current OpenMetadata ingestion was
therefore not executed and no governance profile was started. The metadata
stage remains visibly historical/current-unexecuted, references the prior GH-3
proof only as historical evidence, and records the current search/server
limits as 1g/2g.

## Assessment and browser separation

Independent non-profile verification exited zero:

- demo contract/verification: 37 focused tests passed;
- assessment contract: 40 tests passed;
- engine: 28 tests passed;
- complete non-E2E suite: 188 passed, one unchanged documented platform
  object-store boundary skipped, and two E2E tests deselected;
- Ruff and mypy: zero findings;
- wheel/sdist build: 113 packaged files checked;
- diagram renderer/security: five tests and seven deterministic rendered pairs
  passed with render parity;
- Compose configuration, tracked Python compilation, and `git diff --check`:
  exit zero.

The `--pending` specification review completed with Critical 0, Important 0,
and Minor 0. The `--pending` code-quality re-review completed with Critical 0,
Important 0, and Minor 1. Its non-blocking robustness note is that the web
presentation derives manifest availability from repository-file presence while
the required contract gate performs the semantic validation.

The real loopback Chromium journey used Playwright Chromium 149.0.7827.55.
It displayed all nine stage manifests and declared artifacts, the available
current product, the historical/current-unexecuted metadata state, and a
separate repository view in which the product and stage provenance were
unavailable. It exposed no demo controls, made no remote requests, produced no
console or page errors, preserved back/reload state, and shut down every
browser context and loopback server.

The mutation proof physically removed a stage-manifest artifact in a temporary
repository view. Only artifact availability changed; the canonical maturity,
confidence, gate, and finding-priority JSON projection remained byte-identical.

## Cleanup, limitations, and rollback

Generated current demo evidence is ignored and removed by `make clean`.
Browser binaries, virtual environments, package builds, dbt output, warehouse
files, Parquet, screenshots, and runtime evidence remain generated/ignored.
`make down` is the only profile teardown used; it does not remove named
volumes.

Rollback is to run `make down`, revert the additive Phase 6 source/content
changes, and run `make clean` before regenerating the baseline core path.
Engagement data and named volumes are preserved. Phases 7–8, assessment
mapping promotion, recipe execution, and release work remain out of scope.
