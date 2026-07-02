# Phase P4 Subplan: Execution Protocol

metadata_date: 2026-06-24
status: DRAFT_PENDING_P3_CLOSEOUT
master_program: docs/plans/bayesfilter-two-lane-filter-comparison-master-program-2026-06-24.md
phase: P4
executor: Claude Code
reviewer: read-only bounded reviewer only

## Phase Objective

Freeze the exact execution protocol for the leaderboard runs: commands,
environment, timing method, warmup policy, repeats, seeds, and CPU/GPU/dtype
settings.

This phase exists to prevent accidental unfair timing and accidental promotion of
smoke or one-off runs into leaderboard evidence.

## Entry Conditions Inherited From Previous Phase

- P3 result must define the required output artifact families.

## Required Artifacts

- Phase P4 result:
  `docs/plans/bayesfilter-two-lane-filter-comparison-p4-execution-protocol-result-2026-06-24.md`
- Refreshed Phase P5 subplan:
  `docs/plans/bayesfilter-two-lane-filter-comparison-p5-lowdim-execution-subplan-2026-06-24.md`

## Required Checks, Tests, And Reviews

Protocol checks must explicitly freeze:
- CPU-only vs GPU lanes,
- dtype / TF32 policy,
- whether compile/warmup time is included,
- repeat count,
- seed policy for stochastic algorithms,
- output artifact paths.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is the execution protocol fixed tightly enough that runtime comparisons will be fair and reproducible? |
| Baseline/comparator | Existing CPU-only governance commands and any future explicitly approved GPU lane. |
| Primary pass criterion | The protocol fixes environment, timing definition, repeat policy, and seed policy with no ambiguity. |
| Veto diagnostics | Mixed CPU/GPU interpretation, mixed dtype policy, compile/warmup timing ambiguity, or stochastic runs without a fixed seed/repeat policy. |
| Explanatory diagnostics | Command inventory and manifest design. |
| Not concluded | No results yet, only protocol freeze. |
| Artifact preserving result | P4 result and refreshed P5 subplan. |

## Frozen First-Pass Environment Choice

For the first overnight leaderboard pass, use:
- CPU-only execution with `CUDA_VISIBLE_DEVICES=-1`,
- harness-reported first-call and steady-call timing where available,
- explicit repeat counts recorded in the run manifest,
- explicit seed accounting for stochastic methods,
- no GPU timing claim unless a later reviewed GPU lane is opened under a new subplan/result.

This keeps the first pass comparable and avoids confusing current governance work
with the repo's broader production-GPU policy.

## Stop Conditions

Stop with a blocked P4 result if timing protocol fairness cannot be stated
precisely enough for the intended lane(s).
