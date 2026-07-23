---
type: host-capability-readiness-audit
issue: 9
date: "2026-07-22"
status: blocked-dependency
verdict: BLOCKED
auditInputSha: "dc8b6d2cb46c8101bd8f1309acc7f12e5da7e090"
blockedCookInputSha: "9eb31075aeb0e7b974ad15645460ab4987570f20"
releasedStageASha: "fecf6bb8e5dfa7cc69f9766f72ac6f5b9301dad9"
forkExecNegatives: "7/7"
setsidPidReap: PASS
operationFeasibility: "7/8"
cookScope: none
descendantStrategy: none
s3: PASS
cloudAction: none
---

# Fresh Host-Capability Readiness Audit — Issue #9

## Verdict

`BLOCKED`; `COOK_SCOPE=none`; `DESCENDANT_STRATEGY=none`.

The exact host provides a narrow secure prevention primitive: Seatbelt `deny process-fork`
prevents every tested descendant-creation family before the first child, and the parent can own
one worker by exact PID/start identity through same-process `setsid`, TERM-ignore, KILL, and
`wait`. This is stronger than the former discovery design, and user launchd/process groups/polling
are not accepted substitutes.

The primitive is not a complete Issue #9 backend. The released `retail.dbt-build` command, using
public pinned `dbt-core==1.11.12` and `dbt-duckdb==1.10.1` APIs, starts Python's multiprocessing
resource tracker and fails `EPERM` under fork denial. A diagnostic private multiprocessing-context
mutation made the SQL workload run, but that startup/private-state hook remains forbidden. The
plan cannot silently remove dbt, weaken the rapid-double-fork negative, or advertise seven of the
eight released commands.

## Readiness Matrix

| Gate | Result | Consequence |
|---|---|---|
| Fork/spawn/subprocess/multiprocessing/double-fork prevention | PASS `7/7` | viable conditional zero-descendant worker primitive |
| Exact same-process `setsid` worker cleanup | PASS | exact single PID/start TERM→KILL→wait is viable |
| Network, base write, fake-secret and credential negatives | PASS | containment properties retained |
| User launchd `setsid` negative control | FAIL as authority | launchd is rejected |
| Released operation feasibility | FAIL `7/8` | no implementation cook scope |
| Plan structure/catalog/hash validation | PASS | amendment is publishable as a blocked decision |
| Independent xhigh whole-plan validation | PASS; semantic readiness `blocked-honest` | no unresolved audit finding |
| S3 planning scans | PASS | no cloud/source/private-path authority added |

## Conditional Future Cook Invariant

Only after a separately approved backend passes all eight released operations may the plan select
`prevent-fork-exec-single-worker`:

1. the parent creates exactly one fixed worker and the admitted Seatbelt profile permits zero
   descendants;
2. the parent records exact worker PID/start identity and performs bounded TERM 5 seconds, KILL 5
   seconds, then `wait` after normal completion, same-process `setsid`, image replacement, crash,
   or timeout;
3. any reviewed adapter that requires fork, spawn, subprocess, multiprocessing process
   synchronization/resource tracking, or exec is unavailable and fails readiness before workspace
   or operation allocation;
4. all existing network/base-write/credential/quota/output/fencing/evidence/rollback requirements
   and the 44 RED / 9 S3 catalogs remain mandatory.

That strategy is not selected now because the released operation set does not satisfy item 3.

## Required Owner/Platform Decision

Choose and separately release/review one route:

1. a pinned public dbt backend that runs the exact 51-model / 186-node build in process without a
   resource-tracker child, private state mutation, dynamic startup hook, or caller-selected plugin;
2. a documented no-sudo Darwin lifetime primitive that controls every allowed helper including
   rapid reparent/`setsid`—none is currently proven; or
3. an explicit upstream rerelease of a useful staged command contract.

Until then the correct workflow label is `blocked-dependency`, the former `ready to cook` label is
removed, no RED/source phase resumes, and the next phase is `owner-platform-decision`.

## Audit Closure

- Only Issue #9 plan, validation, audit, and checksum artifacts change from the requested input.
- Product source, runner tests/implementation, portal, contracts, golden core, Airflow, data
  callables, other worktrees, PR/merge state, credentials, and cloud state remain unchanged.
- Historical reports retain their exact prior-input verdicts and are explicitly superseded.
- The output commit is recorded in the Issue #9 publication comment after it exists; no future SHA
  is invented inside recursively hashed plan content.
