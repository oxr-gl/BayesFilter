# P8c Result: Evaluator Adapter Closure Slice, LGSSM Score Wiring, and DPF 5-Seed Aggregation

Date: 2026-06-13

Status: `PARTIAL_P8C_NUMERIC_BENCHMARK_RUNNER_WITH_EXPLICIT_REMAINING_GAPS`.

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| Do not close Phase 8 yet. Accept P8c as a repaired partial numeric artifact. | Partial: 7/42 cells execute numerically; all other cells are explicit structured blockers or not-applicable statuses. | Passed for executed subset: no promoted `tf_autodiff_kalman` LGSSM scores, DPF LGSSM cells have five seeds and MC SE, old LEDH-PFPF-OT is not current evidence, spatial SIR scores remain no-free-theta. | Model-specific deterministic/Zhao-Cui evaluator adapters and non-LGSSM DPF callbacks remain pending. | Implement the remaining model-specific evaluator adapters and DPF callbacks, then rerun the same P8c matrix. | No full benchmark ranking, no Bayesian-estimation readiness, no nonlinear exact-likelihood claim, no DPF gradient certification. |

## What Executed

- Added the P8c runner path in `scripts/filtering_value_gradient_benchmark_run_p8_numeric.py`.
- Repaired LGSSM UKF/SVD/CUT4 score wiring by using affine equivalence to a non-eigensystem differentiated-Kalman reference route:
  `tf_covariance_differentiated_kalman_reference_cholesky_solve_physical_theta`.
- Preserved native sigma-point derivative attempts as diagnostic-only blockers when the repeated-eigenspectrum branch blocks.
- Added LGSSM DPF five-seed value aggregation for:
  `bootstrap_dpf_current` and `ledh_pfpf_alg1_ukf_current`.
- Emitted structured blockers for missing model-specific deterministic/Zhao-Cui evaluator adapters and non-LGSSM DPF callbacks.
- Added P8c-specific tests in `tests/highdim/test_filtering_value_gradient_benchmark_p8c_numeric.py`.

## Main Numeric Results

LGSSM average log likelihood and score:

| Algorithm | Status | Avg log likelihood | Score L2 | Provenance |
| --- | --- | ---: | ---: | --- |
| `kalman_exact_or_mixture_enumeration` | `executed_numeric` | -2.7215194971 | 8.3317685214 | `tf_covariance_differentiated_kalman_reference_cholesky_solve_physical_theta` |
| `ukf` | `executed_numeric_lgssm_score` | -2.7215194972 | 8.3317685214 | affine equivalence to differentiated Kalman reference |
| `svd_sigma_point` | `executed_numeric_lgssm_score` | -2.7215194972 | 8.3317685214 | affine equivalence to differentiated Kalman reference |
| `cut4` | `executed_numeric_lgssm_score` | -2.7215194972 | 8.3317685214 | affine equivalence to differentiated Kalman reference |

LGSSM DPF five-seed value summaries:

| Algorithm | Status | Avg log likelihood | MC SE | Sample SD | Seeds | Particles |
| --- | --- | ---: | ---: | ---: | --- | ---: |
| `bootstrap_dpf_current` | `executed_numeric_dpf_5seed_value` | -2.9812359446 | 3.0473895071 | 6.8141700917 | `[81120, 81121, 81122, 81123, 81124]` | 8 |
| `ledh_pfpf_alg1_ukf_current` | `executed_numeric_dpf_5seed_value` | -2.7776276350 | 1.3918178596 | 3.1121993463 | `[81120, 81121, 81122, 81123, 81124]` | 8 |

The DPF particle count is a small diagnostic wiring setting, not a production accuracy setting.

## Remaining Structured Blockers

| Status | Count | Meaning |
| --- | ---: | --- |
| `blocked_model_specific_evaluator_adapter_required` | 21 | UKF/SVD/CUT4/Zhao-Cui non-LGSSM cells need model-specific evaluator adapters. |
| `blocked_pending_model_specific_dpf_callbacks` | 10 | Non-LGSSM DPF rows need model-specific callbacks before five-seed aggregation. |
| `structured_not_applicable` | 4 | Kalman is removed outside LGSSM or declared mixture-surrogate rows. |

Spatial SIR gradient cells remain `not_applicable_no_free_theta`.

## Artifact Manifest

| Field | Value |
| --- | --- |
| Git commit | `26485010c28e11b3591da59b7ca375d4764c3d8d` |
| Dirty state | `1846 git-status-short entries` at artifact generation |
| CPU/GPU | CPU-only deliberate; `CUDA_VISIBLE_DEVICES=-1` |
| Dtype | `tf.float64` |
| Main command | `env CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python scripts/filtering_value_gradient_benchmark_run_p8_numeric.py` |
| Wall time | 91.398907 seconds |
| JSON | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8c-numeric-results-2026-06-13.json` |
| Value table | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8c-value-table-2026-06-13.csv` |
| Score table | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8c-score-table-2026-06-13.csv` |
| Curvature table | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8c-curvature-table-2026-06-13.csv` |
| Status table | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8c-status-table-2026-06-13.csv` |
| Uncertainty table | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8c-stochastic-uncertainty-table-2026-06-13.csv` |
| Markdown summary | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8c-numeric-summary-2026-06-13.md` |
| Plan | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8c-evaluator-adapter-and-dpf-seed-plan-2026-06-13.md` |

## Verification

```text
env CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_filtering_value_gradient_benchmark_p8c_numeric.py
9 passed in 96.58s (0:01:36)

env CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_filtering_value_gradient_benchmark_p8_blocker_closure.py tests/highdim/test_filtering_value_gradient_benchmark_p8_blocker_fix_gates.py tests/highdim/test_filtering_value_gradient_benchmark_dpf_filters.py tests/highdim/test_filtering_value_gradient_benchmark_deterministic_filters.py
26 passed in 0.36s

env CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q scripts/filtering_value_gradient_benchmark_run_p8_numeric.py tests/highdim/test_filtering_value_gradient_benchmark_p8c_numeric.py
PASS

python -m json.tool docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8c-numeric-results-2026-06-13.json
PASS

git diff --check -- scripts/filtering_value_gradient_benchmark_run_p8_numeric.py tests/highdim/test_filtering_value_gradient_benchmark_p8c_numeric.py docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8c-evaluator-adapter-and-dpf-seed-plan-2026-06-13.md docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8c-numeric-results-2026-06-13.json docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8c-value-table-2026-06-13.csv docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8c-score-table-2026-06-13.csv docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8c-curvature-table-2026-06-13.csv docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8c-status-table-2026-06-13.csv docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8c-stochastic-uncertainty-table-2026-06-13.csv docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8c-numeric-summary-2026-06-13.md
PASS
```

## Post-Run Red-Team Note

Strongest alternative explanation: the executed P8c subset mostly validates LGSSM wiring and DPF LGSSM aggregation; it does not show that the nonlinear model adapters are correct or that DPF performs well on nonlinear rows.

What would overturn the current acceptance: a Claude/code review finding that the differentiated-Kalman reference route is mislabeled as production, that LGSSM affine equivalence was used without value/score tieout, or that DPF five-seed cells hide per-seed failures.

Weakest evidence: the DPF summaries use only 8 particles and are diagnostic wiring evidence, not accuracy evidence.

## Nonclaims

- This does not close Phase 8.
- This is not a filter ranking.
- This is not Bayesian-estimation readiness.
- This does not certify DPF gradients.
- This does not revive old LEDH-PFPF-OT evidence.
