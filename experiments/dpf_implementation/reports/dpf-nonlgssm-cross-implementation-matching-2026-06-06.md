# DPF Non-LGSSM Cross-Implementation Matching Result

metadata_date: 2026-06-06

## Decision

`nonlgssm_matching_sv_density_pass_with_interface_blockers`

## Summary

- Cells: `5`
- Status counts: `{'MATCHED': 1, 'PREP_ONLY': 2, 'INTERFACE_BLOCKED': 2}`

## Cell Table

| model | cell type | status | decision | mismatch class |
|---|---|---|---|---|
| stochastic_volatility | density_value_gradient | `MATCHED` | `sv_density_value_gradient_matched` | N/A |
| student_stochastic_volatility | interface_inventory | `PREP_ONLY` | `student_sv_surfaces_identified_not_yet_density_matched` | student_parameterization_adapter_needed |
| student_range_bearing_nonlinear | student_reference_panel | `PREP_ONLY` | `student_range_bearing_panel_available_comparison_only` | not_same_as_bayesfilter_sir_or_predator_prey |
| spatial_sir | interface_inventory_with_bayesfilter_smoke | `INTERFACE_BLOCKED` | `spatial_sir_no_comparable_second_implementation_identified` | no_comparable_filterflow_or_student_sir_interface |
| predator_prey | interface_inventory_with_bayesfilter_smoke | `INTERFACE_BLOCKED` | `predator_prey_no_comparable_second_implementation_identified` | no_comparable_filterflow_or_student_predator_prey_interface |

## SV Match

The stochastic-volatility density cell compared BayesFilter and executable
float64 FilterFlow on the same 1D transition and observation density scalar,
using physical parameters `(gamma,beta)` for the gradient comparison.

- Max absolute value delta:
  `1.1102230246251565e-16`
- Max absolute gradient delta:
  `1.7763568394002505e-15`

## Interpretation

The non-LGSSM slice promotes one actual equality cell: stochastic-volatility
transition/observation density value and physical-parameter gradient match
between BayesFilter and float64 FilterFlow.  Student SV and range-bearing rows
remain preparation/comparison-only evidence.  SIR and predator-prey remain
interface-blocked for cross-implementation matching because no same-model
FilterFlow or student surface was identified.

## Non-Claims

- no filtering-algorithm correctness claim
- no implementation is treated as an oracle
- no TT-filter correctness claim
- no paper-scale validation claim
- no HMC/DSGE/GPU/production readiness claim
- interface-blocked models are not counted as failures
- student nonlinear panel is comparison-only evidence
