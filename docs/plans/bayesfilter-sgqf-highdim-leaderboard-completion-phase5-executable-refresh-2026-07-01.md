# Phase 5 Executable Refresh: Final SGQF Leaderboard Regeneration

Date: 2026-07-01

## Status

`EXECUTABLE_REFRESH_PENDING_REVIEW`

## Purpose

Regenerate the authoritative highdim leaderboard artifacts so that the SGQF row
statuses produced by this completion program are reflected honestly and without
silent upgrades.

## Exact Scope

Update the final authoritative SGQF/UKF/Zhao-Cui highdim leaderboard only for
row-status changes justified by the reviewed SGQF completion phases.

Rows that must remain preserved exactly as already admitted baselines:

- `benchmark_lgssm_exact_oracle_m3_T50`
- `zhao_cui_sv_actual_nongaussian_T1000`
- `zhao_cui_sv_ksc_gaussian_mixture_surrogate_T1000`

Rows whose SGQF statuses must be updated from this program's results:

- `zhao_cui_spatial_sir_austria_j9_T20` -> remains blocked
- `zhao_cui_predator_prey_T20` -> reviewed SGQF candidate should become executed
  with analytical score if the emitter path already supports the existing tested
  route
- `zhao_cui_generalized_sv_synthetic_from_estimated_values` -> remains blocked

## Exact Files To Modify

Implementation / emitter:

- `docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py`

Artifacts to regenerate:

- `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-01.json`
- `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-01.md`
- `docs/plans/bayesfilter-sgqf-highdim-leaderboard-completion-phase5-final-regeneration-result-2026-07-01.md`

## Exact Checks To Run

CPU-only focused checks only:

```bash
CUDA_VISIBLE_DEVICES=-1 pytest -q \
  tests/highdim/test_p47_predator_prey_filtering.py \
  tests/highdim/test_filtering_value_gradient_benchmark_source_paper_scope.py \
  tests/highdim/test_filtering_value_gradient_benchmark_gradient_semantics.py
```

```bash
CUDA_VISIBLE_DEVICES=-1 python docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py \
  --output docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-01.json \
  --markdown-output docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-01.md
```

```bash
git diff --check -- \
  docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py \
  docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-01.json \
  docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-01.md \
  docs/plans/bayesfilter-sgqf-highdim-leaderboard-completion-phase5-final-regeneration-result-2026-07-01.md
```

## Exact Interpretation Rules

- Already-complete SGQF baseline rows remain unchanged unless a reviewed
  contradiction is discovered.
- The SIR SGQF row must remain blocked.
- The generalized-SV SGQF row must remain blocked.
- The predator-prey SGQF row may be upgraded only if the regenerated emitter
  path now truly emits the same T20 value/analytical-score route covered by the
  reviewed row contract and tests.
- No row may be silently promoted from value-only to value+score.
- No blocked row may become executed without an explicit reviewed row result
  supporting that change.

## Preserved Nonclaims

- no HMC readiness;
- no top-level API promotion;
- no production/default claim;
- no broad SGQF exactness claim beyond the reviewed per-row contracts.
