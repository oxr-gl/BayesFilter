# DPF Cross-Implementation Common-Sense Tie-Out Result

metadata_date: 2026-06-06

## Decision

`cross_impl_tieout_first_slice_pass_with_interface_blockers`

## Summary

- Cells: `7`
- Status counts: `{'MATCHED': 2, 'PREP_ONLY': 2, 'INTERFACE_BLOCKED': 3}`

## Cell Table

| model | cell type | status | decision | mismatch class |
|---|---|---|---|---|
| lgssm_1d_step_gradient | value_and_gradient | `MATCHED` | `one_d_lgssm_step_gradient_filterflow_contract_matches_fd_veto` | N/A |
| lgssm_2d_paper_table_contract | value_table | `MATCHED` | `lgssm_table_full_within_filterflow_mc_band` | N/A |
| stochastic_volatility | interface_probe | `PREP_ONLY` | `sv_filterflow_model_surface_identified_no_value_gradient_tieout_yet` | fixture_preparation_needed |
| student_lgssm_fixtures | student_reference_consistency | `PREP_ONLY` | `student_lgssm_reference_panel_available_not_yet_bayesfilter_filterflow_tieout` | student_phase_preparation |
| scalar_nonlinear | interface_inventory | `INTERFACE_BLOCKED` | `scalar_nonlinear_interface_blocked` | no_comparable_interface_identified |
| spatial_sir | interface_inventory | `INTERFACE_BLOCKED` | `spatial_sir_interface_blocked` | no_comparable_interface_identified |
| predator_prey | interface_inventory | `INTERFACE_BLOCKED` | `predator_prey_interface_blocked` | no_comparable_interface_identified |

## Interpretation

This first slice confirms the already-hardened LGSSM BayesFilter-vs-FilterFlow
value/gradient and table contracts, identifies stochastic-volatility as a
fixture-preparation target, confirms student LGSSM artifacts exist for the
next phase, and explicitly blocks scalar nonlinear, SIR, and predator-prey
tie-outs until comparable interfaces are built.

## Non-Claims

- no filtering-algorithm correctness claim
- no implementation is treated as an oracle
- no TT-filter correctness claim
- no paper-scale validation claim
- no HMC/DSGE/GPU/production readiness claim
- interface-blocked models are not counted as failures
