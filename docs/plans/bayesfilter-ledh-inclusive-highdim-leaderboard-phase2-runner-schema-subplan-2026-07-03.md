# Phase 2 Subplan: Runner And Artifact Schema

Date: 2026-07-03

Status: `DRAFT_PENDING_PHASE1`

## Phase Objective

Implement a separate LEDH-inclusive highdim leaderboard runner and schema
without changing the meaning of the current non-LEDH runner.

## Entry Conditions Inherited From Previous Phase

- Phase 1 admission ledger exists.
- Same-target, scoped, and blocked rows are separated.
- Required LEDH adapters are known.
- Default comparator mode is `frozen_non_ledh_baseline_plus_fresh_ledh`.
- Initial executable LEDH arms are only:
  - `benchmark_lgssm_exact_oracle_m3_T50:ledh_value_dry_run_or_tiny_value_gate_only`;
  - `zhao_cui_spatial_sir_austria_j9_T20:fixed_spatial_sir_value_arm_only`.
- All LEDH score arms and all other rows are emitted as blocked/scoped unless
  this phase creates and reviews more same-target adapters before execution.

## Required Artifacts

- Runner:
  `docs/benchmarks/benchmark_two_lane_highdim_ledh_leaderboard.py`.
- Tests, likely:
  `tests/test_two_lane_highdim_ledh_leaderboard.py`.
- Dry-run artifact:
  `docs/plans/bayesfilter-two-lane-highdim-ledh-inclusive-leaderboard-dry-run-2026-07-03.json`.
- Phase 2 result:
  `docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-phase2-runner-schema-result-2026-07-03.md`.
- Updated Phase 3 subplan.

## Required Checks, Tests, Reviews

- `python -m py_compile docs/benchmarks/benchmark_two_lane_highdim_ledh_leaderboard.py`.
- Focused pytest for schema and row-status generation.
- JSON row coverage check against the seven requested highdim rows.
- Check that every non-executed row and every non-executed score arm has an
  explicit blocked/scoped reason in the dry-run artifact.
- `git diff --check` on touched files.
- Claude read-only review of runner schema and claim boundaries.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the runner emit a LEDH-inclusive leaderboard schema that preserves row status, value status, score status, MCSE fields, device metadata, and nonclaims? |
| Baseline/comparator | Existing highdim leaderboard JSON schema, plus Phase 1 admission ledger. |
| Primary pass criterion | Runner can emit a dry-run artifact for all rows without running expensive GPU ladders, preserving full/scoped/blocked status, arm-level value/score status, explicit blocked/scoped reasons, and frozen-vs-fresh provenance. |
| Veto diagnostics | Runner hides GPU with `CUDA_VISIBLE_DEVICES=-1` by default for LEDH; existing baseline rows are mutated silently; LEDH rows omit MCSE fields; score status is not separate from value status; runtime cross-ranking is enabled in frozen-baseline mode; blocked rows disappear. |
| Explanatory diagnostics | Static schema tests and dry-run artifact content. |
| Not concluded | No LEDH value correctness or score correctness until Phase 3/4. |
| Artifact | Runner, tests, dry-run JSON/MD, Phase 2 result. |

## Forbidden Claims And Actions

- Do not overwrite the July 3 baseline artifact.
- Do not make CPU the LEDH production path.
- Do not add LEDH to `HIGHDIM_ALGOS` in the existing runner unless the change is
  separately justified and reviewed.
- Do not call a dry-run row executed.
- Do not implement new row adapters for blocked rows unless the same-target
  proof and score/value status are updated before execution.

## Exact Next-Phase Handoff Conditions

Advance to Phase 3 only if:

- dry-run artifact has every model row and every comparison algorithm;
- LEDH statuses are explicit;
- LEDH executable arms are limited to the two enumerated value arms unless a
  same-target adapter review expands the scope before execution;
- all non-executed rows and score arms carry explicit reasons;
- tests pass;
- Claude review agrees or fixable issues are patched.

## Stop Conditions

- Runner cannot represent blocked/scoped/executed LEDH rows cleanly.
- Existing code lacks a stable import path for LEDH value/score routines.
- A required schema change would invalidate the non-LEDH leaderboard without
  human approval.
