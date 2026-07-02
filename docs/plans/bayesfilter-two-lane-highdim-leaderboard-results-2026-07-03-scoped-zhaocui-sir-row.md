# Scoped Zhao-Cui SIR Row Validation

Authoritative JSON artifact: `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-03-scoped-zhaocui-sir-row.json`.

This is scoped affected-row validation only, not a full leaderboard regeneration.

| Row | Algorithm | Status | Row admission | Target scope | Avg loglik | Score L2 | Reason |
| --- | --- | --- | --- | --- | ---: | ---: | --- |
| zhao_cui_spatial_sir_austria_j9_T20_parameterized_logscale | fixed_sgqf | blocked | not_applicable_to_scoped_component_row | local_complete_data_zhao_cui_sir_d18_component | n/a | n/a | fixed_sgqf is not admitted for the scoped Zhao-Cui parameterized SIR local complete-data component row; the scoped row is a fixed-variant Zhao-Cui manual-score component cell. |
| zhao_cui_spatial_sir_austria_j9_T20_parameterized_logscale | ukf | blocked | not_applicable_to_scoped_component_row | local_complete_data_zhao_cui_sir_d18_component | n/a | n/a | ukf is not admitted for the scoped Zhao-Cui parameterized SIR local complete-data component row; the scoped row is a fixed-variant Zhao-Cui manual-score component cell. |
| zhao_cui_spatial_sir_austria_j9_T20_parameterized_logscale | zhao_cui_scalar_or_multistate | executed_value_score | scoped_component_row_admitted | local_complete_data_zhao_cui_sir_d18_component | -60.446411 | 1269.738 | Zhao-Cui parameterized SIR T20 local complete-data score emitted by manual parameter-score methods |

## Nonclaims

- not a full leaderboard regeneration artifact
- not full observed-data/filtering SIR likelihood
- not full observed-data/filtering SIR score identity
- not a timing ranking artifact
- not a GPU result
