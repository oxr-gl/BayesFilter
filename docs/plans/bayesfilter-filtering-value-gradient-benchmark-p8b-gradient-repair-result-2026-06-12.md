# P8b Gradient Repair Result

Date: 2026-06-12

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| Accept narrow LGSSM score repair | Passed for LGSSM UKF/SVD/CUT4 affine-equivalence score cells | Passed: no silent score holes, DPF remains MC-SE blocked, nonlinear rows remain pending | Native analytic sigma-point scores branch-block on repeated placement eigenvalues | Continue P8 adapters/seed ladders for non-LGSSM and DPF rows | Full P8 closeout, nonlinear gradient correctness, DPF gradient validity, filter ranking |

## What Changed

- Added `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8b-gradient-repair-plan-2026-06-12.md`.
- Added a physical-theta LGSSM first-derivative adapter in `scripts/filtering_value_gradient_benchmark_run_p8_numeric.py`.
- The runner now attempts `tf_svd_ukf_score`, `tf_svd_cubature_score`, and `tf_svd_cut4_score` for LGSSM.
- All three native analytic sigma-point score attempts blocked with:

```text
blocked_weak_spectral_gap: SVD sigma-point placement spectrum is not separated
```

- Because each sigma-point value tied out exactly to the Kalman LGSSM value, the emitted score for UKF/SVD/CUT4 uses explicit `lgssm_affine_equivalence_to_tf_autodiff_kalman_physical_theta_after_sigma_value_tieout` provenance.
- DPF and non-LGSSM cells remain pending or MC-SE blocked; no ranking is claimed.

## Result Snapshot

LGSSM physical-theta score for Kalman/UKF/SVD/CUT4:

```text
[5.655446880394444, -3.8350564588644085, 0.3023616838294117, -1.9171802706079974, 4.354265919011986]
score_l2_norm = 8.331768835665503
average_log_likelihood = -2.721519497158494
absolute_value_gap_to_kalman = 0.0 for UKF/SVD/CUT4
absolute_score_l2_gap_to_kalman = 0.0 for UKF/SVD/CUT4
```

## Claude Review

- Plan review attempt 1 and compact retry hung despite no output.
- Small Claude probe returned `PROBE_OK`, so the issue was prompt/review-worker behavior rather than Claude availability.
- Final compact execution review returned:

```text
PASS
```

with the scope limitation that this supports only the LGSSM affine-equivalence score repair, not full P8 closeout.

## Validation

Commands run:

```bash
env CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python scripts/filtering_value_gradient_benchmark_run_p8_numeric.py
env CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_filtering_value_gradient_benchmark_p8b_numeric.py tests/highdim/test_filtering_value_gradient_benchmark_p8_blocker_closure.py tests/highdim/test_filtering_value_gradient_benchmark_p8_blocker_fix_gates.py
env CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q scripts/filtering_value_gradient_benchmark_run_p8_numeric.py tests/highdim/test_filtering_value_gradient_benchmark_p8b_numeric.py
python -m json.tool docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8b-numeric-results-2026-06-12.json
git diff --check -- scripts/filtering_value_gradient_benchmark_run_p8_numeric.py tests/highdim/test_filtering_value_gradient_benchmark_p8b_numeric.py docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8b-numeric-results-2026-06-12.json docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8b-value-table-2026-06-12.csv docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8b-score-table-2026-06-12.csv docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8b-curvature-table-2026-06-12.csv docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8b-status-table-2026-06-12.csv docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8b-stochastic-uncertainty-table-2026-06-12.csv docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8b-numeric-summary-2026-06-12.md docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8b-gradient-repair-plan-2026-06-12.md
```

Validation outcome:

```text
23 passed
compileall passed
json.tool passed
git diff --check passed
```

TensorFlow printed CUDA plugin/cuInit warnings even with `CUDA_VISIBLE_DEVICES=-1`; this was a deliberate CPU-only run and exited successfully.

## Nonclaims

- Not a full Phase 8 closeout.
- Not a nonlinear benchmark score repair.
- Not DPF gradient certification.
- Not a filter ranking.
- Not Bayesian-estimation readiness.

