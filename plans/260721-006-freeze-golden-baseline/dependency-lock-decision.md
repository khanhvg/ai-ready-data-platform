# Dependency lock decision

## Decision

The golden baseline is **CPython 3.12.x on macOS arm64** (planning proof: CPython 3.12.3), with a platform-named pip requirements lock whose resolved versions are fixed and whose accepted wheel artifacts carry SHA-256 hashes. The implementation must pin these direct roots:

```text
pip==26.1.1
faker==40.28.1
duckdb==1.5.4
dbt-core==1.11.12
dbt-adapters==1.24.4
dbt-duckdb==1.10.1
rfc8785==0.1.4
```

This selects the historically proven dbt 1.11.12 family rather than allowing the resolver to choose a later core. `dbt-core==1.12.0` is not a patch-equivalent refresh: current metadata requires `dbt-adapters>=1.24.5` and adds `dbt-core-experimental-parser`, MetricFlow, and `python-dotenv`. Adopting it would change the parser/semantic dependency surface without a product requirement or golden evidence. A resolver that selects 1.12.0 or any version not listed below is a hard failure `LOCK_RESOLUTION_DRIFT`.

The support claim is intentionally exact: `implementation_name=cpython`, `3.12 <= version < 3.13`, native darwin-arm64. Record the exact patch/build in evidence. Issue #3 proves the dbt 1.11.12 macOS-arm64 family and the planning proof uses 3.12.3. Linux, Windows, x86 emulation, CPython 3.11/3.13+, and PyPy are not claimed; adding a platform requires a separately named lock and two clean full-run results. Unsupported tuples fail preflight with `PYTHON_BASELINE_UNSUPPORTED`, never opportunistic resolution.

## Planned lock artifacts and exact format

Future owned paths:

```text
requirements/golden-py312-macos-arm64.in
requirements/golden-py312-macos-arm64.lock
requirements/golden-py312-macos-arm64.metadata.json
requirements/golden-lock-tools.in
requirements/golden-lock-tools.lock
```

The application `.in` contains the seven direct roots above. `rfc8785` is direct because phase 4 imports it for the normative evidence canonicalizer; relying on an unrelated transitive graph would make the required import unverifiable. The application `.lock` is pip requirements hash-checking syntax emitted by `pip-tools==7.6.0`: every package is exact `==`, every accepted wheel has `--hash=sha256:…`, and global policy is wheel-only. No editable/local/VCS/path/sdist entry, unbounded specifier, index/trusted-host override, or unhashed line is allowed. The metadata records schema version, Python/platform policy, direct pins, compiler identity, command, distribution count, lock byte SHA-256, and two run evidence locators. Metadata never replaces `pip --require-hashes`.

`golden-lock-tools.in` contains exactly `pip==26.1.1` and `pip-tools==7.6.0`. Its independently reproduced 40-line wheel-only lock has exact path-sensitive SHA-256 `ece1d20658685e8673a98a12135e1680321f0c04e0f1ec35b5c30e15135a7bc4` and this complete eight-package graph:

| Tool distribution | Version | Accepted wheel SHA-256 |
|---|---:|---|
| build | 1.5.0 | `13f3eecb844759ab66efec90ca17639bbf14dc06cb2fdf37a9010322d9c50a6f` |
| click | 8.4.2 | `e6f9f66136c816745b9d65817da91d61d957fb16e02e4dcd0552553c5a197b76` |
| packaging | 26.2 | `5fc45236b9446107ff2415ce77c807cee2862cb6fac22b8a73826d0693b0980e` |
| pip-tools | 7.6.0 | `4bd99155b6d8de358a214b0865e1a2855a453570c1a83d40f7b564870b8657be` |
| pyproject-hooks | 1.2.0 | `9e5c6bfa8dcc30091c74b0cf803c81fdd29d94f01992a7707bc97babb1141913` |
| wheel | 0.47.0 | `212281cab4dff978f6cedd499cd893e1f620791ca6ff7107cf270781e587eced` |
| pip | 26.1.1 | `99cb1c2899893b075ff56e4ed0af55669a955b49ad7fb8d8603ecdaf4ed653fb` |
| setuptools | 83.0.0 | `29b23c360f22f414dc7336bb39178cc7bcbf6021ed2733cde173f09dba19abb3` |

`pip` and `setuptools` remain pinned/hashed in the compiler lock’s allow-unsafe section. The accepted CPython 3.12 distribution and its stdlib `venv`/bundled pip are the explicit local bootstrap trust anchor; pinning the CPython installer itself is outside this issue’s dependency-lock scope. Bundled pip may install only this pre-reviewed hash-closed tool lock. The independent validation empty-cache proof installed exactly these eight wheels with `--require-hashes --only-binary=:all: --no-deps`, passed `pip check`, reported pip 26.1.1/pip-compile 7.6.0, and produced SHA-256 `432758222db2606f750ec97edbbe96510cbf3e42a8704c4d59d0982ff37928f8` from the exact algorithm `sorted(pip freeze --all lines)`, LF-joined with one final LF. The metadata must name this algorithm; “normalized freeze” without it is not an executable claim.

Exact tool-lock regeneration command, using the previously accepted compiler environment, is:

```bash
( cd "$REPO_ROOT" && PIP_CONFIG_FILE=/dev/null "$RUN_ROOT/lock-compiler/bin/pip-compile" - < requirements/golden-lock-tools.in --output-file=requirements/golden-lock-tools.lock --no-config --resolver=backtracking --generate-hashes --allow-unsafe --strip-extras --no-reuse-hashes --no-emit-index-url --no-emit-trusted-host --pip-args='--only-binary=:all: --no-cache-dir --index-url https://pypi.org/simple' )
```

Exact compile command, run after the secure runner binds `RUN_ROOT` to a new private directory and `REPO_ROOT` to the verified worktree, with an empty pip cache:

```bash
python3.12 -m venv "$RUN_ROOT/lock-compiler"
TOOL_LOCK="$REPO_ROOT/requirements/golden-lock-tools.lock" python3.12 -c 'import hashlib,os,pathlib; p=pathlib.Path(os.environ["TOOL_LOCK"]); assert hashlib.sha256(p.read_bytes()).hexdigest()=="ece1d20658685e8673a98a12135e1680321f0c04e0f1ec35b5c30e15135a7bc4"'
PIP_CONFIG_FILE=/dev/null PIP_CACHE_DIR="$RUN_ROOT/compiler-pip-cache" "$RUN_ROOT/lock-compiler/bin/python" -m pip install --isolated --disable-pip-version-check --no-input --no-cache-dir --require-hashes --only-binary=:all: --no-deps -r "$REPO_ROOT/requirements/golden-lock-tools.lock"
"$RUN_ROOT/lock-compiler/bin/python" -m pip check
"$RUN_ROOT/lock-compiler/bin/python" -m pip --version
"$RUN_ROOT/lock-compiler/bin/pip-compile" --version
( cd "$REPO_ROOT" && PIP_CONFIG_FILE=/dev/null PIP_CACHE_DIR="$RUN_ROOT/compiler-pip-cache" "$RUN_ROOT/lock-compiler/bin/pip-compile" - < requirements/golden-py312-macos-arm64.in --output-file=requirements/golden-py312-macos-arm64.lock --no-config --resolver=backtracking --generate-hashes --allow-unsafe --strip-extras --no-reuse-hashes --no-emit-index-url --no-emit-trusted-host --pip-args='--only-binary=:all: --no-cache-dir --index-url https://pypi.org/simple' )
```

The compiler version itself must be checked before compile. `--allow-unsafe` makes installer-class roots such as the explicit pip pin visible rather than silently omitting them. The implementer regenerates the candidate once, reviews the complete diff, then records the exact byte fingerprint. Regeneration that differs from the reviewed graph or expected candidate SHA is `LOCK_REGEN_MISMATCH`, not an implicit update.

## Exact selected locked graph

Independent validation on 2026-07-21 resolved exactly 56 distributions in the application lock: 55 runtime/import distributions plus the explicit `pip` installer root. The separate compiler lock independently pins the compiler environment.

| Distribution | Version | Distribution | Version |
|---|---:|---|---:|
| agate | 1.9.1 | annotated-types | 0.7.0 |
| attrs | 26.1.0 | babel | 2.18.0 |
| certifi | 2026.6.17 | charset-normalizer | 3.4.9 |
| click | 8.4.2 | colorama | 0.4.6 |
| daff | 1.4.2 | dbt-adapters | 1.24.4 |
| dbt-common | 1.38.0 | dbt-core | 1.11.12 |
| dbt-duckdb | 1.10.1 | dbt-extractor | 0.6.0 |
| dbt-protos | 1.0.541 | dbt-semantic-interfaces | 0.9.0 |
| deepdiff | 8.6.2 | duckdb | 1.5.4 |
| faker | 40.28.1 | idna | 3.18 |
| importlib-metadata | 8.9.0 | isodate | 0.7.2 |
| jinja2 | 3.1.6 | jsonschema | 4.26.0 |
| jsonschema-specifications | 2025.9.1 | leather | 0.4.1 |
| markupsafe | 3.0.3 | mashumaro | 3.14 |
| more-itertools | 10.8.0 | msgpack | 1.2.1 |
| networkx | 3.6.1 | orderly-set | 5.5.0 |
| packaging | 26.2 | parsedatetime | 2.6 |
| pathspec | 0.12.1 | protobuf | 6.33.6 |
| pydantic | 2.13.4 | pydantic-core | 2.46.4 |
| python-dateutil | 2.9.0.post0 | python-slugify | 8.0.4 |
| pytimeparse | 1.1.8 | pytz | 2026.2 |
| pyyaml | 6.0.3 | referencing | 0.37.0 |
| requests | 2.34.2 | rfc8785 | 0.1.4 |
| rpds-py | 2026.6.3 | six | 1.17.0 |
| snowplow-tracker | 1.1.0 | sqlparse | 0.5.5 |
| text-unidecode | 1.3 | typing-extensions | 4.16.0 |
| typing-inspection | 0.4.2 | urllib3 | 2.7.0 |
| zipp | 4.1.0 | pip | 26.1.1 |

The superseded six-root planner probe remains provenance only: it produced a byte-identical 837-line lock with generic SHA-256 `042ca2a806328067b1ce8584bfd0cd3ab18255c3dde71a0854d10c2cc71ea9bf` and repository-relative output-header SHA-256 `6552bc4c96df53656a83f5c4d7e01317bc29a094fa7e3ac948d35f8d1b997d6a`, but it omitted `rfc8785` and therefore could not satisfy the required import. It is not an acceptable implementation lock.

Two independent disposable validation compiles from separately bootstrapped compiler environments produced byte-identical corrected 840-line locks. With a generic same-directory output filename the SHA-256 is `08ad36af321bac52a32f160694b98446e07d74c971116dfd5afd16cf1af712c1`. With the exact repository-relative output header produced by the commands above, the expected lock byte SHA-256 is:

```text
f41c727b39f99106f95b7937b2811e8d27db89d1d5106e9f1d9effd4403143d2
```

This fingerprint is a decision input, not a published repository lock at the planner SHA. The implementer must fail if the tracked lock produced from the reviewed input differs.

## Empty-cache install and compatibility tests

Each of two independent tests allocates a new `0700` run root, new venv, empty cache, dbt target, logs, raw data, warehouse, and export directories. The exact install core is:

```bash
python3.12 -m venv "$RUN_ROOT/venv"
"$RUN_ROOT/venv/bin/python" -c 'import platform,sys; assert sys.implementation.name == "cpython"; assert sys.version_info[:2] == (3,12); assert platform.system() == "Darwin" and platform.machine() == "arm64"'
PIP_CONFIG_FILE=/dev/null PIP_NO_INPUT=1 PIP_DISABLE_PIP_VERSION_CHECK=1 PIP_CACHE_DIR="$RUN_ROOT/pip-cache" "$RUN_ROOT/venv/bin/python" -m pip install --no-cache-dir --require-hashes --only-binary=:all: --no-deps -r "$REPO_ROOT/requirements/golden-py312-macos-arm64.lock"
"$RUN_ROOT/venv/bin/python" -m pip check
"$RUN_ROOT/venv/bin/dbt" --version
DBT_PROFILES_DIR="$REPO_ROOT/transform/dbt" "$RUN_ROOT/venv/bin/dbt" parse --project-dir "$REPO_ROOT/transform/dbt" --target-path "$RUN_ROOT/dbt-target" --log-path "$RUN_ROOT/dbt-logs"
"$RUN_ROOT/venv/bin/python" -c 'import dbt, duckdb, faker, jsonschema, rfc8785, yaml'
VENV_PY="$RUN_ROOT/venv/bin/python" "$RUN_ROOT/venv/bin/python" -c 'import hashlib,os,subprocess; rows=sorted(subprocess.check_output([os.environ["VENV_PY"],"-m","pip","freeze","--all"], text=True).splitlines()); print(hashlib.sha256(("\n".join(rows)+"\n").encode()).hexdigest())'
```

Two independent validation installs used separate homes, venvs and empty caches. Both passed the hash-only install and `pip check`, imported `dbt`, `duckdb`, `faker`, `jsonschema`, `rfc8785` and `yaml`, and produced the same exact sorted-`pip freeze --all` SHA-256:

```text
cdb87ed71e0996f90041371cc25138afa02d78b134cbdc4afe9c25baa6649bba
```

One independent disposable archive then produced 18 tables/6,812 rows, returned dbt 179 pass/7 warn/0 error/186 total, reported 51 models/141 tests/18 sources, and exported all 11 marts in 13 seconds on the validation host. These checks substantiate compatibility, not the formal two-clean-full-run release gate. Implementation must perform both complete runs from C1 and record their exact evidence.

Implementation repeats these as formal tests, then each environment executes the full `small`/`42` pipeline. Independent test A and B must agree on lock bytes, freeze hash, package inventory, dbt graph, semantic projection, and artifact hashes. Network access is permitted only during the bounded artifact-download step; the pipeline run is offline. Missing binary wheels fail `LOCK_BINARY_UNAVAILABLE`; source builds and relaxed hashes are forbidden.

A focused disposable 1.12.0 comparator also completed the same 6,812-row and 179/7/0/186 result, so compatibility alone does not justify migration. It resolved a 60-package graph, reported 486 rather than 485 macros, and added `dbt-core-experimental-parser==2.0.0a4`, `metricflow==0.211.0`, `python-dotenv`, `rapidfuzz`, `sqlglot` and `tabulate` while removing `dbt-semantic-interfaces`; the macOS-arm64 experimental-parser wheel alone was about 43.4 MB. This proves 1.12.0 is a future explicit migration candidate, not an implicit golden refresh.

## Tests before implementation

- Reject a lock with one missing hash, an added index/URL/editable, a range specifier, a duplicate normalized distribution, or any selected version drift.
- Reject Python/platform mismatch and a venv inheriting system site packages.
- Seed an artifact cache with unrelated bytes; prove install uses the newly allocated empty cache.
- Mutate `dbt-core` to 1.12.0, remove `dbt-adapters==1.24.4`, or allow normal dependency resolution; expect typed failure before data generation.
- Prove both venvs are independent and no prior `.venv`, dbt package cache, raw data, or warehouse is used.
- Parse and run the current 51-model project with the locked environment; assert the graph and results in the golden matrix.

## Primary sources and compatibility evidence

- [pip repeatable installs](https://pip.pypa.io/en/stable/topics/repeatable-installs/) and [secure installs](https://pip.pypa.io/en/stable/topics/secure-installs/) define exact pins, hashes, and `--only-binary`/`--no-deps` hardening.
- [pip requirements file format](https://pip.pypa.io/en/stable/reference/requirements-file-format/) is the lock syntax authority.
- [pip-tools documentation](https://pip-tools.readthedocs.io/en/stable/) is the compiler authority.
- [dbt-core 1.11.12 metadata/files](https://pypi.org/pypi/dbt-core/1.11.12/json) (wheel SHA-256 `3b7760a3760a6db8a14a6ef38fb86532b2c2b150d49beaa1feb0f50170baa86e`), [dbt-core 1.12.0 metadata/files](https://pypi.org/pypi/dbt-core/1.12.0/json) (wheel SHA-256 `8a91ec6aabaf329efc603330b629e72551ea6be8321483d7c284c598541faaab`), [dbt-adapters 1.24.4](https://pypi.org/project/dbt-adapters/1.24.4/), and [dbt-duckdb 1.10.1 metadata](https://pypi.org/pypi/dbt-duckdb/1.10.1/json) (wheel SHA-256 `90658ecb367082786c5ea2ffbf9e35bb4116fa5ad1bc2f287c4dc1f3984bafa1`) are the version/requirement sources.
- Historical issue #3 evidence under `plans/260708-003.../reports/` is contextual compatibility evidence, not a substitute for the two fresh formal runs.

## Update and rollback policy

Lock updates are explicit baseline migrations: change the `.in`, compile in a new private root, inspect every graph change, run both clean installs/full pipelines, update metadata/schema readers, and use a new contract version if outputs change. No automated “latest” update is accepted.

Rollback restores the prior `.in`, `.lock`, tool lock and metadata atomically as a set, deletes only the issue-owned private failed run, reinstalls into a fresh venv/cache, and reruns the old reader plus the two-run oracle. Never reuse a partially installed venv or edit hashes by hand. A failed dependency experiment must leave product requirements and protected files byte-identical. Removing the first lock returns exact input behavior but also removes the new reproducibility guarantee; it is a recovery state, not a passing golden state.
