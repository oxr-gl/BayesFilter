# Filterflow Gap-Closure Program

## Decision

`filterflow_gap_closure_program_completed_with_severe_unreconciled_gradient_mismatch_risk`

## Gap Status

| Gap | Status | Detail |
| --- | --- | --- |
| `fixed_target_sinkhorn_ess_gating` | `closed_nontriggered_veto_removed` | fixed-target Sinkhorn is now computed only on ESS-triggered rows in the matched audit path; unconditional residual ladder remains a component diagnostic |
| `filterflow_style_annealed_transport_reference` | `within_filterflow_mc_band` | paper-style annealed transport mirror preserved |
| `matched_ledh_pfpf_ot` | `matched_ledh_pfpf_ot_finite_diagnostics` | finite bounded diagnostics on the matched filterflow LGSSM protocol; not a requirement that LEDH equal filterflow RegularisedTransform |
| `gradient_smoothness_audit` | `smoothness_gradient_severe_unreconciled_magnitude_risk_recorded` | finite_gradient_smoke_not_agreement |
| `filterflow_environment_freeze` | `recorded_and_smoke_passed` | pass |
| `covariance_ambiguity_ledger` | `recorded_permanent_note` | paper/supplement 0.5 I_2 versus executable I_2 recorded |

## Filterflow Environment Freeze

| Key | Value |
| --- | --- |
| `status` | `recorded_and_smoke_passed` |
| `branch` | `bayesfilter-py311-compat` |
| `commit` | `5d8300ba247c4c17e1a301a22560c24fd0670bfe` |
| `upstream_base` | `5d8300ba247c4c17e1a301a22560c24fd0670bfe` |
| `source_status` | `## bayesfilter-py311-compat
 M scripts/base.py
 M scripts/simple_linear_common.py
 M scripts/simple_linear_smoothness.py` |
| `diff_summary` | `scripts/base.py                     | 7 ++++---
 scripts/simple_linear_common.py     | 5 +++++
 scripts/simple_linear_smoothness.py | 6 ++++--
 3 files changed, 13 insertions(+), 5 deletions(-)` |
| `python` | `3.11.14` |
| `tensorflow` | `2.19.1` |
| `numpy` | `1.26.4` |
| `command` | `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=.cache/filterflow-mpl PYTHONPATH=.localsource/filterflow /home/chakwong/BayesFilter/.localenv/filterflow-py311/bin/python -c <filterflow smoke>` |
| `smoke_status` | `pass` |
| `stderr_excerpt` | `acer already registered. Please check linkage and avoid linking the same target more than once.
W0000 00:00:1780252093.538927    4836 computation_placer.cc:177] computation placer already registered. Please check linkage and avoid linking the same target more than once.
W0000 00:00:1780252093.538929    4836 computation_placer.cc:177] computation placer already registered. Please check linkage and avoid linking the same target more than once.
2026-06-01 02:28:13.540998: I tensorflow/core/platform/cpu_feature_guard.cc:210] This TensorFlow binary is optimized to use available CPU instructions in performance-critical operations.
To enable the following instructions: SSE4.1 SSE4.2 AVX AVX2 AVX512F AVX512_VNNI AVX512_BF16 AVX_VNNI FMA, in other operations, rebuild TensorFlow with the appropriate compiler flags.
2026-06-01 02:28:15.606456: E external/local_xla/xla/stream_executor/cuda/cuda_platform.cc:51] failed call to cuInit: INTERNAL: CUDA error: Failed call to cuInit: UNKNOWN ERROR (100)
` |

## Covariance Ambiguity Ledger

| Key | Value |
| --- | --- |
| `status` | `recorded_permanent_note` |
| `paper_supplement_statement` | `transition covariance 0.5 I_2` |
| `executable_filterflow_setting` | `transition covariance I_2` |
| `current_reproduction_policy` | `Use executable filterflow I_2 for code comparisons because prior bounded reruns indicate Table 1 scale matches executable I_2.` |
| `future_reversal_condition` | `separate paper-notation audit overturns the executable-code interpretation` |

## Matched LEDH Summary

| Key | Value |
| --- | --- |
| `row_count` | `27` |
| `executed_row_count` | `27` |
| `finite_row_count` | `27` |
| `nonfinite_row_count` | `0` |
| `max_abs_error_per_time` | `0.015512713400855773` |
| `max_sinkhorn_residual` | `3.552713678800501e-15` |
| `max_abs_corrected_log_weight` | `14.856345448972045` |
| `min_jacobian_singular_value` | `0.30151134457776363` |
| `interpretation` | `finite bounded diagnostics on the matched filterflow LGSSM protocol; not a requirement that LEDH equal filterflow RegularisedTransform` |

## Gradient Audit Summary

| Key | Value |
| --- | --- |
| `status` | `severe_unreconciled_gradient_magnitude_mismatch_risk_recorded` |
| `filterflow_surface_scalar` | `total_log_likelihood_from_filterflow_simple_linear_smoothness` |
| `kalman_reference_scalar` | `total_log_likelihood_from_filterflow_get_surface_kf_finite_difference` |
| `negative_scalar_available` | `True` |
| `per_time_normalization_available` | `True` |
| `horizon` | `100.0` |
| `total_likelihood_rmse` | `323943.654172315` |
| `per_time_likelihood_rmse` | `3239.4365417231497` |
| `total_gradient_rmse` | `144487904.8897196` |
| `per_time_gradient_rmse_proxy` | `1444879.048897196` |
| `gradient_norm_ratio_dpf_to_kalman_fd` | `137214.58717183248` |
| `gradient_cosine_vs_kalman_fd` | `0.8895568190836275` |
| `gradient_sign_agreement` | `0.9375` |
| `interpretation` | `Finite gradients are present, but total/per-time normalization does not by itself explain the severe gradient magnitude mismatch. Gradient agreement is not concluded.` |

## Non-Implications

- No production readiness is concluded.
- No public API readiness is concluded.
- No posterior correctness is concluded.
- No HMC readiness is concluded.
- No general nonlinear-SSM validity is concluded.
- No external macro-model validation is concluded.
- No banking/model-risk claim is concluded.
- No monograph claim is concluded.
- No claim that fixed-target Sinkhorn is filterflow-equivalent is concluded.
- No claim that finite gradients establish gradient correctness is concluded.
