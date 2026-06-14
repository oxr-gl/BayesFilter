# DPF Structural Interface Linear AR(1) Result

## Decision

`DPF_STRUCTURAL_INTERFACE_LINEAR_AR1_POLICY_MATCHED_KALMAN_GRID_MLE`

Kalman grid MLE for `b`: `0.650000`.

| Policy | DPF median grid MLE b | SE-scaled distance | DPF gradient at true b | max completion residual |
| --- | ---: | ---: | ---: | ---: |
| none | 0.650000 | 0.000000 | 0.633403 | 0.000e+00 |
| categorical_ancestor | 0.650000 | 0.000000 | -0.014472 | 0.000e+00 |
| sinkhorn_current_z | 0.800000 | 0.628773 | -4.100836 | 0.000e+00 |
| sinkhorn_full_context | 0.800000 | 0.628773 | -4.133094 | 0.000e+00 |

Exact Kalman validates only this `c=d=0` toy structural fixture.
