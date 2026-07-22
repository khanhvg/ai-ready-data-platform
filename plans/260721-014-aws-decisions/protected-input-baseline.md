# Protected Input Baseline

## Scope

This planner may add only files below `plans/260721-014-aws-decisions/`. The groups below freeze
the read-only input at `24be3b34c6b0fcdbd07c5800dcab349054e34713` for planner-static checks and
the future exact-SHA amendment. Group digests are SHA-256 over the NUL-delimited `git ls-tree -r`
records for the named paths; individual-file digests are SHA-256 over file bytes.

These hashes prove path/mode/blob preservation at this Git input. They do not substitute for the
future released Issue #11 concern handoff or human review.

## Baseline digests

| Protected group | Input paths / method | SHA-256 |
|---|---|---|
| Root Makefile | file bytes: `Makefile` | `12926b16a797fded79b0b11b00147887258721f145c79e66472f44c5f0228458` |
| Root release manifest | file bytes: `release-manifest.json` | `f9037b5d946d14f7b1b9c020939f1a44961011f2ad933db9f2b69054abbf9539` |
| Ignore rules | file bytes: `.gitignore` | `aa93e47707e95286126f47b3d70fe7fc6c047b49c861184533e38b3c5a971316` |
| Shared contracts | tree records: `contracts`, `learning/contracts` | `b03df171afbba42382a4ef8320adf33dcab2e2cd87c58e6e75e18b88b5a970f2` |
| Architecture sources/views/renders | tree records: `architecture` | `8b300c30f26c62367a79c987c8a4f269ee2c777947af27987813828f53cd85ed` |
| Golden runtime/data semantics | tree records: `data-generator`, `ingestion`, `transform`, `serving`, `lake`, `governance`, `orchestration` | `231f4f177cc6c51485e2070b27576b9a790fdeb306b11b9f87e6586a87ce4b8a` |
| Golden tools/tests/locks/fixtures | tree records: `scripts/golden`, `tests/golden`, `tests/contracts`, `tests/fixtures/learning`, `requirements` | `d6138bfa800be482b0e5a548ae0fa60694c306883d93d583f158e67b7a989016` |
| Portal/runner/lab tracked tree | tree records: `apps`, `learning/portal`, `learning/runner`, `learning/labs` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (empty) |

## Protected absences

The following were absent from the input Git tree and must remain absent during this planner
phase:

```text
docs/code-standards.md
apps
learning/portal
learning/runner
learning/labs
infra/aws
scripts/aws
tests/aws
docs/decisions/aws
mk/issue-5/i5-09.mk
```

The last four are expected candidate ownership families for later Issue #14 implementation, but
their absence now is intentional. No exact implementation path may be authorized until the
dependency amendment.

## Planner-static preservation checks

After plan commit, the planner checks:

```text
git diff --name-only 24be3b34c6b0fcdbd07c5800dcab349054e34713...HEAD
git diff --check 24be3b34c6b0fcdbd07c5800dcab349054e34713...HEAD
git ls-tree -r -z 24be3b34c... -- <protected group> | sha256
git ls-tree -r -z HEAD -- <protected group> | sha256
```

Allowed diff names are exact regular files below `plans/260721-014-aws-decisions/` only. No
symlink, hardlink, special file, submodule, or path escaping the repository is allowed. Because
`plans/**/*` is ignored, publication force-adds each enumerated file separately; broad
`git add -f plans` or directory force-add is forbidden.

## Future implementation blast-radius check

The exact-SHA amendment must regenerate this baseline from its approved input and add:

- exact released Issue #11 paths/digests and concern IDs;
- exact non-empty implementation allow-list and exact protected deny-list;
- exact Issue #6/#11 changed-path and semantic compatibility commands;
- protected absent paths that must remain absent;
- exact allowed file types/modes and maximum sizes;
- before/after digest comparison and an unrelated sentinel check outside issue-owned roots.

Any mismatch is a STOP, not a reason to widen the allow-list.
