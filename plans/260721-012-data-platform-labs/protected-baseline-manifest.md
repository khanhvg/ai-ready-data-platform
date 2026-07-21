# Protected Baseline Manifest

## Mục đích

Chốt read-only Git objects tại planner input. Git object IDs dùng để phát hiện byte/tree drift;
semantic assertions vẫn lấy từ Issue #6 readers/contracts, không chỉ từ hash.

## Input object inventory

| Protected target | Git object at `24be3b34c6b0fcdbd07c5800dcab349054e34713` | Disposition |
|---|---|---|
| `Makefile` | `e1a4332a9645ccbd37bec4be1f70372241e16b7b` | Deny write |
| `release-manifest.json` | `b27d231c5ee6d48fd7932b06807ef6a9a2220e21` | Deny write |
| `docs/code-standards.md` | `ABSENT` | Preserve absence |
| `learning/contracts/` | `07371ff254c0d531dc470ff77a09f647199c053b` | Deny write until exact contract lease |
| `contracts/data/` | `ed56fef97ce114250b37a68e092bc1b26d708921` | Issue #6 read-only until exact serialized lease |
| `tests/fixtures/learning/promotion-trust/` | `7b2389765373f09971784f6b3f0b6569dc16d08f` | Read-only immutable fixtures |
| `architecture/` | `cd020fce1d525dd6fe414d5db28748911b7cf300` | Deny write |
| `transform/dbt/` | `28932692fc20e079eecbe7ab1c9f93b2a94a8bbf` | Golden SQL/YAML/grain semantics read-only |
| `serving/rill/` | `27bda8a14222cae083d480275453659adb85b3ff` | Golden metric semantics read-only |
| `lake/curated_assets.json` | `fc4b04aca3d4941d06658f27c58d078299301200` | Exact ordered 11-set read-only |
| `lake/publish_iceberg.py` | `f929090963f94e0847231558271d176f3c8b714c` | Write only under later admitted seam |
| `governance/openmetadata/` | `47583e22c4702f0de0608482c60649e99cc7e6d4` | Write only under later admitted seam |
| `orchestration/airflow/` | `1cff31770c4d98b7591b1d077064194b7b902675` | Runner/pipeline protected until Stage B lease |

## Critical file SHA-256

| File | SHA-256 |
|---|---|
| `Makefile` | `12926b16a797fded79b0b11b00147887258721f145c79e66472f44c5f0228458` |
| `release-manifest.json` | `f9037b5d946d14f7b1b9c020939f1a44961011f2ad933db9f2b69054abbf9539` |
| `contracts/data/retail-golden-v1.json` | `f303282e3b524e1273e702c9b8b24b500aaa01afdd3c3b623ac997afba8840cc` |
| `contracts/data/promotion-trust-v1.yaml` | `c30e1938aae6eeffa2adf0c0b3bdee15f7f877d769cce09e171d43dc2f153cfe` |
| `contracts/data/curated-release-manifest.schema.json` | `dcad3a4c04f44e207a26f985702db6926d4c85545d85ef5481faf036dded4e33` |
| `tests/fixtures/learning/promotion-trust/evidence-v1.json` | `2f4d90228fa2ea8859a8db630ff587b6cebdc10a0bf6b7db25e46c3dc27181d5` |
| `tests/fixtures/learning/promotion-trust/manifest.json` | `0a1dcd4023648f52009bfd4dc5d529c00ce66f42cd0e725732b972b0b78df341` |

## Frozen semantic anchors

- Generator: profile `small`, seed `42`, 18 CSVs, 6,812 rows and exact Issue #6 file hashes.
- dbt: 18 sources, 51 models, 141 generic tests; canonical graph projection SHA-256
  `9cc9079097c4891e2939085729f23d0649af4ded52518966a6c0988991d533df`; clean build
  179 pass, 7 warn, 0 fail, 186 total; nine warn-configured identities retain seven warn/two
  pass distinction. Historical “130 edges” remains context, not current exact lineage proof.
- Marts: exact ordered 11 IDs, row/content/schema/grain truth from `retail-golden-v1`.
- Rill: expression/source/dimension/weighting semantics, including intentional weighted and
  explicitly unweighted measures, remain unchanged.
- Airflow: six default + two optional task IDs/edges remain characterized until a narrow lease.
- Publication: current sequential drop/create and shallow read-back are a known gap, not an atomic
  guarantee.
- Catalog: current verification checks non-zero service populations/count context; it is not exact
  namespace reconciliation.

## Recheck rule

Before each stage and immediately before exact-head approval:

1. Resolve every protected target from the amended input SHA.
2. Compare Git objects and critical SHA-256 values.
3. Run the released Issue #6 semantic readers/tests in read-only mode.
4. Allow drift only for paths explicitly named by an active serialized lease; record before/after
   object IDs, additive reader compatibility and rollback.
5. STOP on any unleased change, absent-to-present protected file, semantic mismatch or fixture
   mutation.
