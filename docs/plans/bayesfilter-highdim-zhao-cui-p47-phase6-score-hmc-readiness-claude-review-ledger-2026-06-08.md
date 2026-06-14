# P47-M6 Claude Review Ledger

metadata_date: 2026-06-08
phase: P47-M6
status: `DRAFT_REVIEW_PENDING`

## Review Protocol

Claude is read-only reviewer.  Codex is supervisor and execution agent.
Claude must not edit files, run experiments, launch agents, or change state.

Expected terminal token:

```text
PASS_P47_M6_SCORE_HMC_READINESS
```

or

```text
BLOCK_P47_M6_SCORE_HMC_READINESS
```

The pass token means the evidence-class score/HMC readiness table is correctly
scoped.  It does not mean production HMC readiness.

## Iteration 1

Claude returned:

```text
PASS_P47_M6_SCORE_HMC_READINESS
```

Nonblocking findings:

- The M6 subplan still used broader stable production score API and HMC
  readiness wording than the implemented evidence-class table.
- The row validator allowed a future positive HMC-readiness phrase if
  `hmc_status="not_requested"`, although the shipped manifest was safe.

Resolution after pass:

- Narrowed the M6 subplan purpose/tasks to the implemented evidence-class
  readiness table and experimental subpackage helper.
- Tightened the row validator to reject positive HMC-readiness wording
  regardless of `hmc_status`, while allowing explicit nonclaims.
- Added a focused regression for that overclaim guard.
