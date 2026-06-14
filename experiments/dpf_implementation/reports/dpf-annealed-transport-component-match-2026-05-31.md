# Annealed Transport Component Match

## Decision

`annealed_transport_component_matched_filterflow`

## Reference Hierarchy

| Key | Value |
| --- | --- |
| `canonical_executable_reference` | `patched local filterflow bayesfilter-py311-compat` |
| `transition_covariance` | `I_2 executable filterflow reproduction setting` |
| `fixed_target_sinkhorn` | `local BayesFilter diagnostic/comparator only` |
| `component_under_test` | `reusable TF/TFP annealed_transport_resample_tf` |

## Summary

| Key | Value |
| --- | --- |
| `row_count` | `9` |
| `within_band_count` | `9` |
| `nonfinite_count` | `0` |
| `max_abs_delta` | `0.026786881508458538` |
| `max_row_residual` | `0.5659112334251404` |
| `max_column_residual` | `2.1316282072803006e-14` |
| `min_triggered_rows` | `14900.0` |
| `fixed_target_sinkhorn_status` | `not_used_local_comparator_only` |

## Nine-Cell Comparison

| epsilon | theta | filterflow mean | component mean | delta | within 1 sd | max row residual | max column residual |
| ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: |
| 0.25 | 0.25 | -1.02566 | -1.04875 | -0.0230848 | True | 5.659e-01 | 1.776e-14 |
| 0.25 | 0.5 | -0.857608 | -0.874091 | -0.0164834 | True | 4.772e-01 | 2.132e-14 |
| 0.25 | 0.75 | -0.91767 | -0.944457 | -0.0267869 | True | 3.348e-01 | 2.132e-14 |
| 0.5 | 0.25 | -1.02654 | -1.04911 | -0.0225735 | True | 1.635e-01 | 2.132e-14 |
| 0.5 | 0.5 | -0.860413 | -0.876199 | -0.0157859 | True | 9.726e-02 | 2.132e-14 |
| 0.5 | 0.75 | -0.925254 | -0.945166 | -0.0199113 | True | 9.211e-02 | 2.132e-14 |
| 0.75 | 0.25 | -1.02692 | -1.04926 | -0.0223452 | True | 5.976e-02 | 2.132e-14 |
| 0.75 | 0.5 | -0.860785 | -0.876965 | -0.0161795 | True | 4.702e-02 | 2.132e-14 |
| 0.75 | 0.75 | -0.930679 | -0.948929 | -0.0182495 | True | 3.614e-02 | 2.132e-14 |

## Non-Implications

- No production readiness is concluded.
- No posterior correctness is concluded.
- No HMC readiness is concluded.
- No general nonlinear-SSM validity is concluded.
- No gradient correctness is concluded.
