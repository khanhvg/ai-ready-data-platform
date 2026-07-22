---
type: independent-capability-amendment-validation
issue: 9
date: "2026-07-22"
inputSha: "dc8b6d2cb46c8101bd8f1309acc7f12e5da7e090"
blockedCookInputSha: "9eb31075aeb0e7b974ad15645460ab4987570f20"
releasedStageASha: "fecf6bb8e5dfa7cc69f9766f72ac6f5b9301dad9"
verdict: PASS
semanticReadiness: BLOCKED_HONEST
sourceImmutability: PASS
cloudAction: none
---

# Independent Validation of the Issue #9 Capability Amendment

## Verdict

`PASS` for plan structure, evidence propagation, catalog closure, and source immutability.
Implementation readiness remains honestly `BLOCKED`; `COOK_SCOPE=none`.

A fresh read-only Herdr invocation used Codex `gpt-5.6-sol` with
`model_reasoning_effort="xhigh"` against the stable final active-plan diff. Its terminal result was:

```text
INDEPENDENT_VALIDATION=PASS
STRUCTURE=pass
SEMANTIC_READINESS=blocked-honest
SOURCE_IMMUTABILITY=pass
FINDINGS=none
```

The validation result does not convert a successful host primitive into whole-contract
readiness. Exact pinned `dbtRunner` still requires a resource-tracker child, so the released
eight-command contract closes only `7/8` under descendant prevention.

## Capability Evidence Reviewed

| Evidence | Result |
|---|---|
| Exact host | macOS `26.5.1` build `25F80`, Darwin arm64, 16 GiB, Python `3.12.3` |
| Child-creation negative controls | all seven succeeded unsandboxed and produced their marker |
| Fork-denied worker | `7/7` returned denial before a first child marker; final inventory empty |
| Same-process `setsid` | exact PID/start identity retained; TERM ignored; KILL + `wait` reaped; no survivor |
| Same-PID direct exec control | no descendant; PID/start identity retained; exact KILL + `wait` reaped |
| Network/base/secret | network denied; workspace write passed; base write and fake-secret read denied; fake ambient credential absent |
| User launchd | detached `setsid` child survived `bootout`; exact cleanup removed it; rejected as authority |
| Operation feasibility | seven fixed in-process adapters pass; `retail.dbt-build` fails on resource-tracker child |

The probe scripts were bounded throwaway inputs under `/tmp` and used public fake canaries. Their
SHA-256 identities at validation time were:

- capability controller: `8e2bab2455be1e987be4012b94cb2971778eaef5a7794302c167eaf189cf6dea`;
- unsandboxed control: `73b2221add7b0617b2097dba192a72a4c6dab5f14d0ee8b3f361e99a9013e4c6`;
- sandbox worker: `cb8d391253ecdc023e4eb8d2222a3c6a08afdc5e0fb8240b591bec28b4c273c9`;
- primary operation probe: `bfe013488b9c0e8c13db7f17a449370d901e576db869abed5a02defbc2b8c5b8`;
- remaining-operation probe: `6f7c80c3bf67e95fcbf6d238469e4c172aa86fc5074b1da29446b5c52d8b65cd`.

The exact final capability command was
`/usr/local/bin/python3.12 controller.py --probe-id issue9cap-20260722-final` from the bounded
probe root. Stage A feasibility used an exact Git archive and hash-complete
`golden-py312-macos-arm64.lock`; no repository source was used as writable probe input.

## Deterministic Closure

| Check | Result |
|---|---|
| Strict CK validation | PASS; 0 errors, 0 warnings, 6 phases |
| CK status | PASS; pending 0/6, as required before cook |
| Release pins / contract set | `38/38`; `21/21`; zero mismatch |
| Planned paths | 67 create, 1 conditional modify, 50 read-only; reality checks pass |
| Operation table | 8 exact rows in released order; only `retail.dbt-build` fails |
| Catalogs | 20 requirements, 15 threats, 44 RED assertions, 9 S3 rows |
| Commands | four exact future Make commands |
| Markdown links/anchors | 42 local links; zero broken after current reports exist |
| Placeholders/future SHAs | none |
| Protected/private/secret scan | no non-plan change, private absolute path, high-confidence secret, or source mutation |
| Diff | `git diff --check` PASS |

The plan-only input is not a Stage A descendant. The amendment states that fact explicitly and
keeps clean remote-equal Stage A ancestry as a future pre-write gate; no history operation was
performed or implied by validation.

## Semantic Decision

The active plan correctly supersedes historical READY reports without rewriting them. It removes
process-tree discovery as authority, retains all released operations and security negatives, and
makes the stronger single-worker/zero-descendant invariant conditional on a separately approved
all-eight backend. No source/RED phase is authorized at this input.
