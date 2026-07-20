# Issue #5 Follow-up Implementation Map

## Publication Identity

- Master epic: [#5](https://github.com/khanhvg/ai-ready-data-platform/issues/5)
- Readiness verdict: `READY_WITH_GATES`
- Immutable readiness report SHA:
  `e440c5855732d5d8f5d634e3cc1359c010cc5ed3`
- [Readiness report at that SHA](https://github.com/khanhvg/ai-ready-data-platform/blob/e440c5855732d5d8f5d634e3cc1359c010cc5ed3/plans/260721-005-enterprise-learning-sandbox/audit/readiness-audit-report.md)
- Integration branch target: `integration/issue-5-local-learning` at the commit containing this
  map. That final commit SHA is recorded externally after publication to avoid recursive
  self-reference.

All 14 follow-ups are OPEN and start at canonical `triaged` with `risk:high`, `tdd`,
`security:S3`, and their specialty labels. None is `ready to cook`. Every issue requires a fresh
per-issue plan -> independent validation -> fresh readiness audit before cook and mandatory human
pre-merge approval. No AWS apply is authorized.

## Actual Issue and Dependency Map

| ID | GitHub issue | Actual dependency issue numbers | Labels in addition to inherited gates | Exclusive owner | Initial state |
|---|---|---|---|---|---|
| I5-01 | [#6](https://github.com/khanhvg/ai-ready-data-platform/issues/6) | Master audit only | `shared-core`, `data-integrity` | Shared-core / golden-contract owner | **Wave 0**; `triaged`; may enter its own planning pipeline |
| I5-02 | [#7](https://github.com/khanhvg/ai-ready-data-platform/issues/7) | #6 before scoring/ADR; unscored preview may start under the two-stage barrier | `frontend`, `accessibility`, `decision-gate` | Portal spike and accessibility owner | **Wave 0**; `triaged`; preview/common tests only until #6 merges |
| I5-03 | [#8](https://github.com/khanhvg/ai-ready-data-platform/issues/8) | #6, #7 | `shared-core`, `api` | Active serialized shared-contract lease holder | Dependency-blocked; `triaged` |
| I5-04 | [#9](https://github.com/khanhvg/ai-ready-data-platform/issues/9) | #6, #8 | `backend` | Privileged runner security owner | Dependency-blocked; `triaged` |
| I5-05 | [#10](https://github.com/khanhvg/ai-ready-data-platform/issues/10) | #7, #8, #9 | `frontend`, `accessibility`, `vertical-slice` | Portal vertical-slice owner | Dependency-blocked; `triaged` |
| I5-06 | [#11](https://github.com/khanhvg/ai-ready-data-platform/issues/11) | #8, #10 | `architecture`, `curriculum` | Architecture/curriculum owner under bounded view lease | Dependency-blocked; `triaged` |
| I5-07 | [#12](https://github.com/khanhvg/ai-ready-data-platform/issues/12) | #6, #8, #9, #10 | `data-platform`, `recovery` | Data-platform lab owner under later data-contract lease | Dependency-blocked; `triaged` |
| I5-08 | [#13](https://github.com/khanhvg/ai-ready-data-platform/issues/13) | #10, #12 | `performance`, `compose` | Local runtime/resource owner | Dependency-blocked; `triaged` |
| I5-09 | [#14](https://github.com/khanhvg/ai-ready-data-platform/issues/14) | #6, #11 | `decision-gate`, `aws`, `finops`, `recovery` | AWS architecture / FinOps / operations decision owners | Dependency-blocked; `triaged`; all apply TBCs retained |
| I5-10 | [#15](https://github.com/khanhvg/ai-ready-data-platform/issues/15) | #14 | `terraform`, `no-apply` | Terraform platform owner | Dependency-blocked; `triaged`; non-applying only |
| I5-11 | [#16](https://github.com/khanhvg/ai-ready-data-platform/issues/16) | Adapter work: #12, #14; composition: #15 plus frozen adapter output | `aws`, `data-platform`, `persistence`, `no-apply` | AWS adapter/composition owner; never Terraform | Dependency-blocked; `triaged`; no real readiness claim |
| I5-12 | [#19](https://github.com/khanhvg/ai-ready-data-platform/issues/19) | Local profile: #12; hosted profile: #14, #15, #16, #18 | `ai`, `optional`, `cost` | AI governance/admission owner | Dependency-blocked; `triaged`; admission only, runtime separately authorized |
| I5-13 | [#17](https://github.com/khanhvg/ai-ready-data-platform/issues/17) | #6, #7, #8, #9, #10, #11, #12, #13 | `release`, `evidence` | Release-evidence owner | Dependency-blocked; `triaged`; local release human gate |
| I5-14 | [#18](https://github.com/khanhvg/ai-ready-data-platform/issues/18) | #17 plus separate hosted-product decision | `identity`, `hosted` | Hosted identity/tenant-security owner | Dependency-blocked; `triaged`; blocks learner AWS ingress/hosted AI |

Inherited labels on every row: `triaged`, `risk:high`, `tdd`, `security:S3`.

## Ownership and Wave Guardrails

- Wave 0 consists only of I5-01/#6 and I5-02/#7. I5-02 may run its fixture-labelled,
  non-completing `learn-preview` early; no candidate score or ADR survives unless rerun against
  the merged tracked I5-01 fixture.
- I5-03 and I5-07 receive non-overlapping, time-bounded shared-contract leases. I5-06 receives a
  separate expansion-only architecture-view lease after the merged I5-05 journey.
- I5-01 is the only normal root `Makefile` owner; I5-02 through I5-14 own disjoint
  `mk/issue-5/i5-<nn>.mk` fragments.
- I5-10 owns Terraform for accepted AWS state/key/backup rows. I5-11 owns adapters and exact-output
  composition only and never edits Terraform paths.
- I5-12 produces profile-specific AI admission evidence and an ADR only. It cannot create an
  agent runtime, portal route, AgentCore adapter, AWS resource, or core dependency.
- Root `release-manifest.json`, `docs/code-standards.md`, raw discovery history, ignored runtime
  fixtures, unrelated user files, and paths owned by another active lease remain protected.

## Publication Verification

- Exact-title duplicate check: 14 unique I5 titles, zero duplicates.
- Labels: all required inherited and specialty labels present; no follow-up has `ready to cook`,
  `ready for plan audit`, or `shipped`.
- Bodies: all contain master #5, immutable report and predecessor SHAs, actual dependency links,
  exclusive ownership, tests-before/implementation/tests-after, S3 disposition, exact evidence
  root, migration/rollback and STOP/TBC boundaries.
- GitHub state: all follow-ups OPEN and `triaged`; only the two Wave 0 bodies are marked as
  starting points.

No implementation, product/config/data edit, AWS apply, cloud action, destructive migration or
merge occurred while creating this map.
