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

Independent verification of frozen head
`0d43cb383dee57ba61d609c238118d5718becf93` invalidated the earlier Airflow
pass recorded here. The verifier unpaused the daily DAG before triggering the
required manual run, and scheduled run
`scheduled__2026-07-26T00:00:00+00:00` raced manual run
`phase6__20260726T134543Z`. DuckDB writer contention failed
`transform.dbt_build`; the docs and snapshot tasks became `upstream_failed`.
The immutable independent report remains in
[Issue 38](https://github.com/khanhvg/ai-ready-data-platform/issues/38#issuecomment-5083768869).

Before changing product behavior, a contemporaneous retry of the live
frozen-head command happened to pass, demonstrating that the defect was a
race rather than a deterministic command failure. The focused regression then
failed three assertions on the frozen source: the scheduled DAG had no
single-active-run bound, the verifier emitted no zero-concurrency evidence,
and it did not fail closed when presented with two running DAG runs.

The bounded review-fix keeps `schedule="@daily"` and adds
`max_active_runs=1`, so scheduled and manual instances of this single-writer
pipeline cannot execute concurrently. The verifier also lists running DAG runs
during every task-state poll, fails closed if more than one is running, and
records `concurrent_writer_runs: 0`.

After that source change, `make demo-airflow-verify` exited zero after starting
Airflow alone with deterministic `SCALE=small SEED=42`. Import errors were
empty, the exact required manual run ID was
`phase6__20260726T141507Z`, `concurrent_writer_runs` was zero, and all six
default DAG tasks reached terminal `success`:

- `generate.seed`
- `load.load_raw`
- `load.health_check`
- `transform.dbt_build`
- `transform.dbt_docs_generate`
- `serve.export_marts_snapshot`

The verifier ran `make down`; the final Compose service list was empty and
the existing named volumes remained present.

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

The producing review-fix context is not an independent or post-merge verifier.
It freshly executed the checks invalidated by the bounded source, test, and
manifest changes:

- the genuine Airflow RED regression failed 3 and passed 1 on frozen source,
  then the focused Airflow plus Phase 6 demo suite passed 15/15 after the fix;
- `make demo-contract demo-verify` passed, including 41 policy, manifest,
  contract, catalog, and non-scoring tests;
- the focused catalog-web and non-scoring rerun brought the combined focused
  result to 19 passed;
- the exact small/42 core prerequisites passed with PASS=205, WARN=7, ERROR=0,
  SKIP=0, TOTAL=212 before the representative demo regression;
- assessment Ruff and strict mypy reported zero findings; wheel/sdist
  build-check inspected 113 packaged files;
- Compose configuration, compilation of 88 tracked/new Python files, changed
  source lint, and `git diff --check` exited zero.

The producing `--pending` specification and code-quality review completed in
that order with Critical 0, Important 0, and Minor 0. The retained earlier
browser, full-suite, diagram, lake, and catalog statements are prior producer
claims, not fresh replacement-head verification by this review-fix context.
Fresh independent replacement-head verification remains required.

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
