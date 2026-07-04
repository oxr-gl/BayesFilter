# Reset Memo: LEDH-Inclusive Highdim Leaderboard

Date: 2026-07-03

## Current State

The LEDH-inclusive highdim leaderboard has been produced:

- `docs/plans/bayesfilter-two-lane-highdim-ledh-inclusive-leaderboard-results-2026-07-03.json`
- `docs/plans/bayesfilter-two-lane-highdim-ledh-inclusive-leaderboard-results-2026-07-03.md`

It uses comparator mode
`frozen_non_ledh_baseline_plus_fresh_ledh`. Non-LEDH rows are frozen copies of
the July 3 baseline and were not rerun. Runtime ranking against fresh LEDH rows
is forbidden.

## What Is Actually Established

- LGSSM `benchmark_lgssm_exact_oracle_m3_T50`: LEDH same-target value-only row
  ran at `N=10000` on trusted GPU/XLA/TF32.
- Fixed spatial SIR `zhao_cui_spatial_sir_austria_j9_T20`: LEDH value-only row
  ran at `N=10000` on trusted GPU/XLA/TF32.
- Both value ladders passed the predeclared adjacent-rung stability rule, and
  MCSE decreased from `N=1000` to `N=10000`.

## What Is Not Established

- No LEDH leaderboard score row is admitted.
- LGSSM LEDH score is blocked because the same-target total derivative for
  `m3_T50` is not implemented in the value runner.
- Fixed SIR LEDH score is blocked.
- Parameterized SIR is scoped component evidence only, not a full
  observed-data leaderboard LEDH score row.
- Actual SV, KSC SV, predator-prey, and generalized SV remain blocked for LEDH.
- No HMC readiness, posterior correctness, scientific superiority, or runtime
  ranking claim is established.

## Critical Target-Mismatch Repair

Contract E LGSSM is `D=2`, `T=10`, three parameters. The leaderboard LGSSM row
is `D=3`, `T=50`, five parameters, dataset seed `81100`, theta
`[0.72, 0.55, 0.35, 0.35, 0.45]`.

Therefore Contract E can be used only as route evidence. It must not be used as
same-target value or score evidence for `benchmark_lgssm_exact_oracle_m3_T50`.

## Main New Files

- `docs/benchmarks/benchmark_ledh_same_target_lgssm_m3_t50_value.py`
- `docs/benchmarks/benchmark_two_lane_highdim_ledh_inclusive_results.py`
- `tests/test_two_lane_highdim_ledh_leaderboard.py`
- `docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-phase4-ledh-particle-ladders-result-2026-07-03.md`
- `docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-phase5-merge-comparison-result-2026-07-03.md`
- `docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-phase6-closeout-result-2026-07-03.md`

## Next Smallest Useful Work

Implement and test a same-target total-derivative LEDH score route for
`benchmark_lgssm_exact_oracle_m3_T50`, or leave the score blocked. Do not reuse
Contract E as a substitute.
