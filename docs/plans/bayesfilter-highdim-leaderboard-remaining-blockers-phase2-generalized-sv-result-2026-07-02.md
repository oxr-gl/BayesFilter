# Phase 2 Result: Generalized-SV Zhao-Cui Source-Row Evaluator And Manual Score

Date: 2026-07-02

Status: `PASS_PHASE2_GENERALIZED_SV_ZHAOCUI_VALUE_SCORE_ROW_LOCAL`

## Decision Table

| Field | Decision |
| --- | --- |
| Decision | Admit a row-local Zhao-Cui generalized-SV prior-mean source-row value/manual-score adapter for the generated T1008 scalar target. |
| Primary criterion status | Passed row-local gate: finite full-horizon value, finite three-coordinate manual score, exact generated source-row observations/theta, and no admitted autodiff/FD provenance. |
| Veto diagnostic status | Passed: actual-SV, KSC, precursor, auxiliary, and native-oracle evidence are not used for row admission; the admitted score route uses explicit model parameter-score methods with `finite_difference_h=()`; source anchors are included without claiming adaptive source-faithful TT-cross/SIRT reproduction. |
| Main uncertainty | Runtime is high for the full T1008 smoke (`454.6250707899453` seconds CPU-only) because the scalar fixed-branch score path replays the path separately per parameter. This is not a tuned performance configuration and does not settle Phase 6 full-regeneration cost. |
| Next justified action | Advance to Phase 3 spatial SIR full observed-data/filtering route repair. |
| Not concluded | No exact likelihood correctness proof, no SP500 posterior estimate, no finite-tail generalized-SV claim, no adaptive MATLAB Zhao-Cui TT-cross/SIRT reproduction, no full-regeneration validation/certification, no production GPU/XLA readiness, no HMC readiness, no posterior correctness, and no timing/ranking claim. |

## Row-Local Result

Artifact:

- `docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-phase2-generalized-sv-zhaocui-row-2026-07-02.json`

Key row values:

| Field | Value |
| --- | --- |
| `row_id` | `zhao_cui_generalized_sv_synthetic_from_estimated_values` |
| `algorithm_id` | `zhao_cui_scalar_or_multistate` |
| `comparison_status` | `executed_value_score` |
| `numeric_execution_status` | `executed_zhao_cui_generalized_sv_prior_mean_scalar_tt_value_score` |
| `average_log_likelihood` | `-1.4266238463369423` |
| `log_likelihood` | `-1438.036837107638` |
| `score_coordinate_system` | `theta=(z_gamma,log_tau,mu_over_tau); gamma=Phi(z_gamma), tau=exp(log_tau), mu=mu_over_tau*tau` |
| `score` | `[2.348688687464202, 1.09941572140932, -0.06740000139302951]` |
| `score_l2_norm` | `2.5941465338897247` |
| `score_status` | `analytical_score_emitted` |
| `score_derivative_provenance` | `zhao_cui_generalized_sv_prior_mean_scalar_fixed_design_tt_manual_parameter_score_methods_only` |
| `runtime_seconds` | `454.6250707899453` |

The row's Phase 7 status remains `not_ranked_by_phase7_timing`; the runtime
above is CPU-only explanatory evidence and is not a production timing artifact.

## Source-Target Binding

The admitted row uses:

- generated observations from
  `scripts/filtering_value_gradient_benchmark_generate_p8_datasets.py::_generalized_sv_prior_mean_dataset(81105)`;
- horizon `1008`;
- theta coordinate
  `source_route_active_transformed_prior_mean`;
- source-route transformed parameter convention
  `theta=(z_gamma,log_tau,mu_over_tau)`,
  `gamma=Phi(z_gamma)`, `tau=exp(log_tau)`, and
  `mu=mu_over_tau*tau`.

Source anchors used for the model route:

- `third_party/audit/zhao_cui_tensor_ssm_p10/source/models/svmodels/ftt2true.m:6-14`;
- `third_party/audit/zhao_cui_tensor_ssm_p10/source/models/svmodels/st_process.m:13-15`;
- `third_party/audit/zhao_cui_tensor_ssm_p10/source/models/svmodels/like.m:4-7`;
- `third_party/audit/zhao_cui_tensor_ssm_p10/source/models/svmodels/boxcoxinv.m:10-14`.

Implementation classification:

- `fixed_hmc_adaptation` / documented-deviation fixed-design substitute for
  the generated scalar prior-mean row;
- not a source-faithful adaptive MATLAB TT-cross/SIRT reproduction.

## Implementation Summary

Changed files:

- `bayesfilter/highdim/models.py`
  - Added `GeneralizedSVPriorMeanSSM` with explicit manual density-score
    methods for initial, transition, and observation densities.
- `bayesfilter/highdim/__init__.py`
  - Exported `GeneralizedSVPriorMeanSSM` from the highdim subpackage.
- `docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py`
  - Added generated source-row theta/observation helpers.
  - Added `_zhao_cui_generalized_sv_tt_cell()` and row-local admission through
    the analytical-score guard.
- `scripts/filtering_value_gradient_benchmark_generate_p8_datasets.py`
  - Clarified the third generalized-SV source-route coordinate as
    `mu_over_tau` in the manifest wording.
- `tests/highdim/test_phase2_generalized_sv_exact_source_row_admission.py`
  - Added source-row identity, manual formula diagnostic, and saved artifact
    admission tests.

## Checks Run

| Check | Result |
| --- | --- |
| `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p44_generalized_sv_target.py tests/highdim/test_p47_generalized_sv_equality.py` | `26 passed, 2 warnings` |
| `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_phase2_generalized_sv_exact_source_row_admission.py` | `3 passed, 2 warnings` |
| `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q bayesfilter/highdim/models.py bayesfilter/highdim/__init__.py docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py scripts/filtering_value_gradient_benchmark_generate_p8_datasets.py tests/highdim/test_phase2_generalized_sv_exact_source_row_admission.py` | passed |
| Row-local `_apply_phase7_status` and `_validate_analytical_score_contract([row])` on the saved artifact | passed |
| `git diff --check -- ...` for Phase 2 touched code/test/artifact paths | passed |

The route/provenance scan still finds `GradientTape` in diagnostic tests and
historical/blocked routes. These are not admitted row provenance. The admitted
generalized-SV row provenance is
`manual_parameter_score_methods_only`, and the derivative config disables FD.

## Runtime Note

The first full-row attempt with a larger scalar TT budget was interrupted after
it exceeded the focused budget. The second smoke-budget full T1008 attempt
completed with finite value and score after `454.6250707899453` seconds. This
settles the Phase 2 target/evaluator/manual-score blocker as a row-local
admission smoke. It does not settle production performance, full leaderboard
wall time, or GPU/XLA readiness.

This Phase 2 closure does not admit, validate, or certify any full-regeneration
route; full-regeneration correctness/readiness remains separately gated in
Phase 6.

## Handoff

Phase 2 is closed as row-local admitted for the Zhao-Cui generalized-SV
prior-mean source row. Phase 3 may begin after its refreshed subplan review.
Phase 3 must preserve the boundary that P91 local complete-data SIR evidence is
sidecar evidence only until a full observed-data/filtering value/manual-score
route is built or precisely blocked.
