# LEDH-Inclusive Highdim Leaderboard Plan Review Packet

Date: 2026-07-03

Status: `PACKET_FOR_CLAUDE_READONLY_REVIEW`

## Role Boundary

Codex is supervisor and executor. Claude is a read-only reviewer only.

Claude must not edit files, run experiments, launch agents, or change state.

## Review Scope

Review these exact paths:

- `docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-master-program-2026-07-03.md`
- `docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-visible-gated-execution-runbook-2026-07-03.md`
- `docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-phase0-launch-boundary-freeze-subplan-2026-07-03.md`
- `docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-phase1-row-admission-adapter-inventory-subplan-2026-07-03.md`
- `docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-phase2-runner-schema-subplan-2026-07-03.md`
- `docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-phase3-tiny-gpu-xla-gates-subplan-2026-07-03.md`
- `docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-phase4-ledh-particle-ladders-subplan-2026-07-03.md`
- `docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-phase5-merge-comparison-subplan-2026-07-03.md`
- `docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-phase6-closeout-subplan-2026-07-03.md`

## Objective

The program should produce a LEDH-inclusive highdim leaderboard comparable to
`docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py`, across all current
highdim model rows, while keeping target status, value status, score status,
GPU/XLA evidence, and nonclaims separate.

## Known Baseline Fact

The current July 3 highdim leaderboard is not a LEDH run. It lists
`ledh_pfpf_alg1_ukf_current` and `ledh_pfpf_ot` as excluded and states that
LEDH/PFPF-OT and DPF transport rows are omitted.

## Required Plan Properties

- Per-phase subplans exist before execution.
- Each subplan states objective, entry conditions, artifacts, checks/reviews,
  evidence contract, forbidden claims/actions, next-phase handoff, and stop
  conditions.
- Claude review is read-only and cannot authorize scientific, runtime,
  product-policy, or pass/fail changes.
- Repair loop patches fixable issues visibly and stops after five Claude rounds
  for the same blocker.
- GPU/XLA/TF32 LEDH runs require trusted/escalated execution.
- Value evidence, score evidence, runtime evidence, and HMC readiness are
  separate claims.
- A row is full only if LEDH computes the same observed-data filtering target.
  Otherwise it must be scoped or blocked.
- Default comparator mode is
  `frozen_non_ledh_baseline_plus_fresh_ledh`; runtime cross-ranking is forbidden
  unless all algorithms are rerun under one reviewed harness.
- Every requested row must appear in the final artifact as full, scoped, or
  blocked. No row may be silently omitted or replaced by a different target.
- Default LEDH ladder uses seeds `81120..81124` and rungs `N=1000,10000`;
  `N=50000` is optional only if budget and memory estimates pass before row
  execution. Deviations require a blocker or reviewed row-specific ladder before
  seeing results.
- Score admission requires a row-specific total-derivative artifact: exact
  derivation, trusted same-target finite difference with fixed randomness, or
  exact oracle.

## Review Questions

1. Does the plan avoid claiming that LEDH already has a current full leaderboard
   run?
2. Does it avoid comparing scoped/component rows as full observed-data
   filtering rows?
3. Does it avoid promoting MCSE, ESS, runtime, smoke tests, or finite values
   into score correctness or HMC readiness?
4. Does it require total-derivative evidence before any LEDH score claim?
5. Are the phase gates and stop conditions sufficient to prevent drifting into
   unsupported claims?
6. Is there any artifact mismatch, missing phase artifact, or missing handoff
   condition that would block visible execution?

## Verdict Format

Findings first. End with exactly one line:

`VERDICT: AGREE`

or

`VERDICT: REVISE`
