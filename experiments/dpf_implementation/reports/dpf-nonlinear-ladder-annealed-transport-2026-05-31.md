# Nonlinear Ladder Annealed Transport

## Decision

`nonlinear_ladder_annealed_transport_executed_with_caveats`

## Rows

| Model | Source decision | Promotion status | Interpretation |
| --- | --- | --- | --- |
| `range_bearing` | `DPF_NONLINEAR_SSM_RANGE_BEARING_STRESS_PASSED` | `bounded_diagnostic_not_general_validity` | UKF approximate diagnostic; range-bearing stress |
| `stochastic_volatility` | `DPF_NONLINEAR_SSM_SV_GRADIENT_MLE_PASSED_SMOKE` | `bounded_diagnostic_not_general_validity` | CUT4 differentiable comparator; scalar/gradient/MLE smoke |
| `structural_ar1` | `DPF_STRUCTURAL_INTERFACE_NONLINEAR_AR1_EXECUTED_WITH_POLICY_LADDER` | `bounded_diagnostic_not_general_validity` | CUT4 comparator and deterministic residual contract |

## Non-Implications

- No general nonlinear-SSM validity is concluded.
- No posterior correctness is concluded.
- No HMC readiness is concluded.
- No production readiness is concluded.
- No DSGE or NAWM validation is concluded.
