# Filterflow Float64 Reference Probe Result

## Decision

`float64_filterflow_variant_preserves_table_scale`

## Interpretation

This probe established that a float64 filterflow execution preserves the
Section-5.1-style table scale.  A committed local branch now carries that
reference path: `bayesfilter-py311-float64-reference` at
`ff0048060fd4cff43dbea606d14275e40e2ac084`.

## Summary

| Key | Value |
| --- | --- |
| `kalman_row_count` | `3` |
| `stochastic_row_count` | `12` |
| `kalman_all_within_tolerance` | `True` |
| `stochastic_all_within_band` | `True` |
| `finite` | `True` |
| `max_kalman_abs_delta_per_time` | `0.0` |
| `max_stochastic_abs_delta_mean_error_per_time` | `0.026267172345360468` |
| `outside_band_rows` | `0` |

## Kalman Rows

| theta | canonical per-time | float64 per-time | delta | within tol |
| ---: | ---: | ---: | ---: | --- |
| 0.25 | -3.05175478 | -3.05175478 | 0.000e+00 | True |
| 0.5 | -2.95832537 | -2.95832537 | 0.000e+00 | True |
| 0.75 | -3.01466259 | -3.01466259 | 0.000e+00 | True |

## PF And RegularisedTransform Rows

| method | eps | theta | canonical mean error | float64 mean error | delta | canonical sd | within band |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| filterflow_pf | N/A | 0.25 | -1.02586739 | -1.03736363 | -1.150e-02 | 0.175800963 | True |
| filterflow_pf | N/A | 0.5 | -0.862692288 | -0.862021761 | 6.705e-04 | 0.154706681 | True |
| filterflow_pf | N/A | 0.75 | -0.939248961 | -0.912981789 | 2.627e-02 | 0.196021532 | True |
| filterflow_regularized | 0.25 | 0.25 | -1.02566412 | -1.03962815 | -1.396e-02 | 0.17914568 | True |
| filterflow_regularized | 0.25 | 0.5 | -0.857607764 | -0.864563121 | -6.955e-03 | 0.155003544 | True |
| filterflow_regularized | 0.25 | 0.75 | -0.917670344 | -0.914134717 | 3.536e-03 | 0.192042721 | True |
| filterflow_regularized | 0.5 | 0.25 | -1.02653622 | -1.0398187 | -1.328e-02 | 0.178527736 | True |
| filterflow_regularized | 0.5 | 0.5 | -0.860413093 | -0.863700935 | -3.288e-03 | 0.154139148 | True |
| filterflow_regularized | 0.5 | 0.75 | -0.925254357 | -0.914230443 | 1.102e-02 | 0.188726382 | True |
| filterflow_regularized | 0.75 | 0.25 | -1.02691872 | -1.03987301 | -1.295e-02 | 0.178189959 | True |
| filterflow_regularized | 0.75 | 0.5 | -0.860785035 | -0.862901794 | -2.117e-03 | 0.153780292 | True |
| filterflow_regularized | 0.75 | 0.75 | -0.930679373 | -0.914533138 | 1.615e-02 | 0.187785012 | True |

## Reference Policy

| Key | Value |
| --- | --- |
| `canonical_reference` | `local executable filterflow float64 branch for BayesFilter difference audits` |
| `float64_status` | `committed local branch bayesfilter-py311-float64-reference` |
| `source_mutation` | `branch source intentionally mutated and committed after this probe` |
| `use_decision` | `Going forward, BayesFilter/filterflow difference audits should compare to the float64 branch unless explicitly auditing native upstream float32 behavior.` |

## Non-Implications

- No production readiness claim.
- No paper correctness claim.
- No posterior correctness claim.
- No gradient correctness claim.
- No public API readiness claim.
- No monograph claim.
- No DSGE/NAWM validation claim.
- No claim that the float64 variant is pristine upstream filterflow.
