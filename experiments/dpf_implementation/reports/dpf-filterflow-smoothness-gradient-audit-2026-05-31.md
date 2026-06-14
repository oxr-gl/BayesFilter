# Filterflow Smoothness Gradient Audit

## Decision

`smoothness_gradient_severe_unreconciled_magnitude_risk_recorded`

## Scalar Normalization Ledger

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

## Gradient Claim Status

`finite_gradient_smoke_not_agreement`

## BayesFilter Gradient Status

| Key | Value |
| --- | --- |
| `status` | `not_run_structured_scope_limit` |
| `reason` | `Current matched BayesFilter table runner is likelihood-table oriented. A same-scalar BayesFilter GradientTape surface requires a separate differentiable scalar harness after the filterflow scalar contract is reconciled.` |

## Non-Implications

- No gradient agreement is concluded.
- No posterior correctness is concluded.
- No HMC readiness is concluded.
- No production readiness is concluded.
- No full supplement figure or table reproduction is concluded.
