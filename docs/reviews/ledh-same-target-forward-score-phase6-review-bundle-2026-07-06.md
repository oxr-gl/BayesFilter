# Claude Read-Only Review Bundle: LEDH Same-Target Forward Score Phase 6

Review name: `ledh-same-target-forward-score-phase6`

## Role Contract

Codex is supervisor and executor. Claude is read-only reviewer only.

Do not edit files, run commands, authorize claims, or approve human/runtime/
model-file/funding/product/scientific boundaries.

## Objective

Review the Phase 6 integration and leaderboard rebuild closeout. Decide whether
the artifacts truthfully admit only the Phase 5-passing LEDH rows and preserve
blocked/scoped statuses for the remaining rows.

## Files To Inspect

- `docs/plans/bayesfilter-ledh-same-target-forward-score-phase6-integration-leaderboard-subplan-2026-07-06.md`
- `docs/plans/bayesfilter-ledh-same-target-forward-score-phase6-integration-leaderboard-result-2026-07-06.md`
- `docs/benchmarks/benchmark_two_lane_highdim_ledh_inclusive_results.py`
- `tests/test_two_lane_highdim_ledh_leaderboard.py`
- `docs/plans/bayesfilter-two-lane-highdim-ledh-inclusive-leaderboard-results-2026-07-06.md`
- `docs/plans/bayesfilter-two-lane-highdim-ledh-inclusive-leaderboard-results-2026-07-06.json`

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the LEDH-inclusive leaderboard truthfully report all admitted LEDH values and scores? |
| Baseline/comparator | Phase 5 per-model score-memory tests and July 3/July 5 leaderboard artifacts. |
| Primary criterion | Only LGSSM and fixed SIR are admitted as LEDH value/score rows; actual SV, KSC SV, predator-prey, and generalized SV remain blocked; scoped parameterized SIR remains scoped. |
| Veto diagnostics | Value/score algorithm mismatch; blocked row promoted; scoped row promoted; runtime ranking against frozen rows; unsupported scientific/HMC/posterior claim. |
| Explanatory diagnostics | Runtime, memory, compile status, MCSE, and frozen non-LEDH context. |
| Not concluded | HMC readiness, posterior correctness, scientific superiority, exact nonlinear SIR likelihood correctness, or fair runtime ranking. |

## Local Checks Run By Codex

```text
python -m py_compile docs/benchmarks/benchmark_two_lane_highdim_ledh_inclusive_results.py tests/test_two_lane_highdim_ledh_leaderboard.py
python -m pytest tests/test_two_lane_highdim_ledh_leaderboard.py -q
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python docs/benchmarks/benchmark_two_lane_highdim_ledh_inclusive_results.py > /tmp/ledh_phase6_builder_stdout_cpuhidden.json
```

Results:

- `py_compile`: passed.
- Phase 6 integration pytest: `9 passed, 2 warnings`.
- Builder regeneration: exit 0. TensorFlow emitted import-time CUDA plugin/cuInit
  warnings with GPU hidden; this was artifact generation, not GPU evidence.

## Expected Accepted State

- `benchmark_lgssm_exact_oracle_m3_T50` LEDH status:
  `executed_value_score`, score route
  `compact_forward_sensitivity_no_autodiff_same_scalar_lgssm_ledh_pfpf_ot`.
- `zhao_cui_spatial_sir_austria_j9_T20` LEDH status:
  `executed_value_score`, score route
  `manual_total_vjp_no_autodiff_same_scalar_fixed_sir_logscale_ledh_pfpf_ot`.
- Fixed SIR uses the amended free-theta coordinate
  `(log_kappa_scale, log_nu_scale, log_obs_noise_scale)`.
- Actual SV, KSC SV, predator-prey, and generalized SV remain blocked.
- Parameterized SIR log-scale row remains scoped and not full observed-data
  evidence.
- `runtime_cross_ranking_allowed` remains `false`.

## Review Questions

Return `VERDICT: AGREE` only if all are true:

1. The Phase 6 result matches the subplan and evidence contract.
2. The leaderboard builder and tests prevent blocked/scoped LEDH rows from
   being promoted.
3. The admitted LGSSM and fixed SIR rows use Phase 5 same-target no-tape score
   evidence and preserve value/score target identity.
4. The artifacts do not claim HMC readiness, posterior correctness,
   scientific superiority, exact nonlinear SIR likelihood correctness, or fair
   runtime ranking.

Return `VERDICT: REVISE` if any item fails, and list the minimal required
repair.

End with exactly one verdict line:

```text
VERDICT: AGREE
```

or

```text
VERDICT: REVISE
```
