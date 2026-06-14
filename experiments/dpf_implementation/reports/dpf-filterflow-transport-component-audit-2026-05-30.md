# Filterflow Transport Component Audit

## Decision

`transport_formula_mismatch_identified`

## Frozen State

- Time index: `1`
- Batch index: `3`
- Selected ESS: `1.09993`
- ESS threshold: `12.5`
- Triggered batches: `100`

## Filterflow Transport Versus `transport_from_potentials`

| eps | matrix max diff | particle max diff | row residual | column residual |
| ---: | ---: | ---: | ---: | ---: |
| 0.25 | 0.000e+00 | 0.000e+00 | 1.372e-04 | 1.192e-07 |
| 0.50 | 0.000e+00 | 0.000e+00 | 1.329e-05 | 1.907e-06 |
| 0.75 | 0.000e+00 | 0.000e+00 | 3.457e-06 | 1.490e-07 |

## Candidate Variants

| variant | eps | matrix max diff | particle max diff | alpha diff | beta diff | iterations | row residual | column residual |
| --- | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: |
| `legacy_axis_row_epsilon0_max_cost` | 0.25 | 9.895e-01 | 1.709e+00 | 3.459e-03 | 3.468e-03 | 25/28 | 2.293e+00 | 2.279e+01 |
| `axis_column_epsilon0_max_cost` | 0.25 | 1.103e-05 | 8.166e-06 | 3.459e-03 | 3.468e-03 | 25/28 | 1.251e-04 | 1.907e-06 |
| `axis_row_epsilon0_filterflow_range` | 0.25 | 9.895e-01 | 1.709e+00 | 1.192e-07 | 2.086e-07 | 28/28 | 2.293e+00 | 2.279e+01 |
| `axis_column_epsilon0_filterflow_range` | 0.25 | 4.172e-07 | 2.384e-07 | 1.192e-07 | 2.086e-07 | 28/28 | 1.372e-04 | 1.192e-07 |
| `legacy_axis_row_epsilon0_max_cost` | 0.50 | 9.797e-01 | 4.942e+00 | 3.457e-03 | 3.460e-03 | 21/24 | 8.831e+00 | 2.281e+01 |
| `axis_column_epsilon0_max_cost` | 0.50 | 1.729e-06 | 1.132e-06 | 3.457e-03 | 3.460e-03 | 21/24 | 1.162e-05 | 3.815e-06 |
| `axis_row_epsilon0_filterflow_range` | 0.50 | 9.797e-01 | 4.942e+00 | 1.490e-07 | 1.490e-07 | 24/24 | 8.831e+00 | 2.281e+01 |
| `axis_column_epsilon0_filterflow_range` | 0.50 | 2.384e-07 | 1.788e-07 | 1.490e-07 | 1.490e-07 | 24/24 | 1.305e-05 | 1.907e-06 |
| `legacy_axis_row_epsilon0_max_cost` | 0.75 | 1.136e+00 | 5.153e+00 | 3.457e-03 | 3.458e-03 | 19/22 | 1.320e+01 | 2.281e+01 |
| `axis_column_epsilon0_max_cost` | 0.75 | 6.557e-07 | 4.768e-07 | 3.457e-03 | 3.458e-03 | 19/22 | 2.801e-06 | 1.907e-06 |
| `axis_row_epsilon0_filterflow_range` | 0.75 | 1.136e+00 | 5.153e+00 | 8.941e-08 | 1.788e-07 | 22/22 | 1.320e+01 | 2.281e+01 |
| `axis_column_epsilon0_filterflow_range` | 0.75 | 2.384e-07 | 1.788e-07 | 8.941e-08 | 1.788e-07 | 22/22 | 3.397e-06 | 1.192e-07 |

## Interpretation

The dominant mismatch is the log-weight axis in transport_from_potentials. The failed audit-only mirror used row-axis log weights; filterflow uses column-axis log weights, giving row sums near one and column sums near N times the source weights. The max-cost epsilon-start variant changes potentials and iteration counts on this frozen state, but still matches the transported particles once the log-weight axis is corrected.

## Non-Implications

- No production readiness is concluded.
- No public API readiness is concluded.
- No HMC readiness is concluded.
- No posterior correctness is concluded.
- No general nonlinear-SSM validity is concluded.
- No claim that finite relaxed OT is categorical PF is concluded.
- No claim that the BayesFilter outer matched audit runner is fixed is concluded.
- No claim that patched filterflow is untouched upstream code is concluded.
