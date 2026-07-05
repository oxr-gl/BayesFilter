# BayesFilter Analytical-Gradient Leaderboard Repair Result

Date: 2026-06-30

Plan: `docs/plans/bayesfilter-analytical-gradient-leaderboard-repair-plan-2026-06-30.md`

## Decision

The corrective pass is partially complete. The leaderboard now enforces the strict rule that `executed_value_score` rows must carry finite score vectors and must not use autodiff, `GradientTape`, or `gradient_tape` provenance. The June 30 JSON/Markdown leaderboard was regenerated under this rule.

No additional non-SGQF high-dimensional SV score row was admitted in this pass. Two tempting analytical routes were audited and rejected for default leaderboard admission:

- Actual-SV UKF: a no-tape `tf_svd_ukf_score` wrapper attempt hit the derivative contract veto `blocked_weak_spectral_gap` on the structurally singular augmented-noise covariance. The historical GradientTape wrapper remains diagnostic only, and the leaderboard row remains `executed_value_only`.
- KSC UKF: `independent_panel_sv_mixture_ukf_score` is an analytical route and passes small focused tests, but the full T1000 source-scope execution was too slow for the default leaderboard builder without batching/caching. The row remains demoted until a row-specific performance subplan supplies a feasible source-scope artifact.

Zhao-Cui SV rows also remain demoted because the scalar fixed-design analytical TT score path is currently pinned to exactly two observations, not the T1000 source rows.

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | Which high-dimensional leaderboard cells can be admitted as value plus analytical score after removing autodiff score admissions? |
| Primary criterion | Passed for the regenerated artifact: admitted score rows have finite score vectors and no autodiff/tape provenance. |
| Veto diagnostics | No admitted autodiff/tape score rows. Actual-SV UKF analytical attempt vetoed by weak spectral gap; KSC UKF full T1000 default-builder admission vetoed by runtime feasibility. |
| Explanatory diagnostics | Small KSC UKF analytical FD test passes; actual-SV UKF historical FD diagnostic remains GradientTape only and is not admitted. |
| Not concluded | No completion of all `n/a` cells, no broad Zhao-Cui production claim, no HMC readiness, no production GPU timing. |
| Preserved artifact | Regenerated `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-06-30.json` and `.md`. |

## Artifacts Changed

- `docs/plans/bayesfilter-analytical-gradient-leaderboard-repair-plan-2026-06-30.md`
- `docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py`
- `tests/test_two_lane_highdim_leaderboard_analytical_scores.py`
- `bayesfilter/highdim/sv_mixture_cut4.py`
- `tests/highdim/test_p43_sv_value_gradient_cut4_zhaocui.py`
- `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-06-30.json`
- `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-06-30.md`
- `docs/plans/bayesfilter-analytical-gradient-leaderboard-repair-result-2026-06-30.md`

`bayesfilter/highdim/sv_mixture_cut4.py` and `tests/highdim/test_p43_sv_value_gradient_cut4_zhaocui.py` already contained the earlier manual fixed-SGQF actual-SV score changes in the working tree. This corrective pass preserved that manual SGQF route, restored the actual-SV UKF wrapper to its historical diagnostic behavior, and retained tensor-construction safety fixes in `_actual_augmented_noise_initial_covariance_derivatives` and `_actual_transformed_sv_augmented_noise_ukf_structural_derivatives`.

## Checks

All TensorFlow checks below were run CPU-only with `CUDA_VISIBLE_DEVICES=-1`. TensorFlow still emitted CUDA factory/cuInit startup warnings despite CPU masking; these are not GPU diagnostics.

| Check | Result |
| --- | --- |
| `CUDA_VISIBLE_DEVICES=-1 python -m py_compile docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py tests/test_two_lane_highdim_leaderboard_analytical_scores.py bayesfilter/highdim/sv_mixture_cut4.py tests/highdim/test_p43_sv_value_gradient_cut4_zhaocui.py` | Passed |
| `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m pytest tests/highdim/test_p43_sv_value_gradient_cut4_zhaocui.py::test_p43_ksc_ukf_two_observation_wrapper_score_matches_centered_finite_difference tests/highdim/test_p43_sv_value_gradient_cut4_zhaocui.py::test_p43_lane_b_principal_sqrt_ukf_wrapper_score_matches_centered_finite_difference -q` | Passed: 4 passed, 2 warnings |
| `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m pytest tests/test_two_lane_highdim_leaderboard_analytical_scores.py -q` | Passed: 4 passed, 2 warnings, 396.50 s |
| `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py --output docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-06-30.json --markdown-output docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-06-30.md` | Passed |

## Current Admitted Score Rows

- LGSSM: fixed-SGQF, UKF, Zhao-Cui exact-oracle adapter.
- Actual SV: fixed-SGQF only.
- KSC surrogate SV: fixed-SGQF only.
- Spatial SIR, predator-prey, generalized SV: no admitted analytical score rows beyond the existing value/status rows.

## Remaining Blockers

1. Actual-SV UKF analytical score needs a derivative route that handles the augmented-noise structural singularity without violating the SVD/UKF score contract.
2. KSC UKF analytical score needs batching/caching or another source-scope T1000 artifact path before default leaderboard admission.
3. Zhao-Cui actual-SV/KSC analytical score needs scalar fixed-design TT score horizon generalization beyond the current exactly-two-observation path.
4. Predator-prey T20 needs source-scope fixed-SGQF/UKF/Zhao-Cui evaluators and analytical scores; P47 two-observation diagnostics remain non-admission evidence.
5. Spatial SIR needs a full observed-data/filtering route; P91 remains scoped local complete-data sidecar evidence only.
6. Generalized-SV exact source row needs its own exact-row evaluator; KSC/actual-SV/precursor evidence remains non-admission evidence.

## Claude Review

Claude reviewed the plan in bounded read-only mode and returned `VERDICT: AGREE`. During execution, the plan was visibly patched to record the scalar fixed-design T1000 horizon blocker found by local audit.
