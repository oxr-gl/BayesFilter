# Annealed Transport Gradient Contract

## Decision

`annealed_transport_gradient_contract_severe_unreconciled_magnitude_risk_recorded`

## Scalar Contract Ledger

| Key | Value |
| --- | --- |
| `status` | `severe_unreconciled_gradient_magnitude_mismatch_risk_recorded` |
| `filterflow_status` | `filterflow_smoothness_executed` |
| `filterflow_scalar` | `total_log_likelihood_from_simple_linear_smoothness` |
| `bayesfilter_scalar` | `total_log_likelihood_common_observations_common_random_numbers` |
| `normalization_variants_recorded` | `total, negative total, per-time` |
| `filterflow_gradient_count` | `16` |
| `bayesfilter_gradient_count` | `16` |
| `comparable_gradient_count` | `16` |
| `bayesfilter_all_finite` | `True` |
| `interpretation` | `BayesFilter GradientTape surface is finite, but filterflow/BayesFilter same-randomness and gradient-magnitude agreement are severely unreconciled. Gradient agreement is not concluded.` |

## Gradient Claim Status

`finite_gradient_smoke_not_agreement`

## Non-Implications

- No gradient agreement is concluded.
- No posterior correctness is concluded.
- No HMC readiness is concluded.
- No production readiness is concluded.
- No full supplement figure or table reproduction is concluded.
