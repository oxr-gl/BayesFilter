# Matched Filterflow LGSSM LEDH-PF-PF-OT Diagnostics

## Decision

`matched_ledh_pfpf_ot_finite_diagnostics`

## Settings

- Horizon: `150`
- Particles: `25`
- Theta grid: `[0.25, 0.5, 0.75]`
- Epsilon grid: `[0.25, 0.5, 0.75]`
- Realization indices: `[0, 1, 2]`
- Transition covariance: `I_2 executable filterflow convention`
- Observation covariance: `0.1 I_2`

## Summary

| Key | Value |
| --- | --- |
| `row_count` | `27` |
| `executed_row_count` | `27` |
| `finite_row_count` | `27` |
| `nonfinite_row_count` | `0` |
| `max_abs_error_per_time` | `0.015366632407813465` |
| `max_sinkhorn_residual` | `9.479688597990865e-08` |
| `max_abs_corrected_log_weight` | `14.856345448972045` |
| `min_jacobian_singular_value` | `0.30151134457776363` |
| `interpretation` | `finite bounded diagnostics on the matched filterflow LGSSM protocol; not a requirement that LEDH equal filterflow RegularisedTransform` |

## Rows

| theta | eps | realization | status | finite | error/time | resamples | max residual | max abs weight |
| ---: | ---: | ---: | --- | --- | ---: | ---: | ---: | ---: |
| 0.25 | 0.25 | 0 | `executed` | True | -0.00221581 | 2 | 3.08702e-08 | 11.2928 |
| 0.25 | 0.25 | 1 | `executed` | True | -0.000922017 | 1 | 1.64045e-08 | 12.2634 |
| 0.25 | 0.25 | 2 | `executed` | True | -0.000711355 | 2 | 4.10152e-12 | 11.4208 |
| 0.25 | 0.5 | 0 | `executed` | True | -0.00216056 | 2 | 2.43865e-08 | 11.2818 |
| 0.25 | 0.5 | 1 | `executed` | True | -0.000901431 | 1 | 5.66491e-14 | 12.2634 |
| 0.25 | 0.5 | 2 | `executed` | True | -0.000692618 | 2 | 3.09418e-11 | 11.4208 |
| 0.25 | 0.75 | 0 | `executed` | True | -0.00214008 | 2 | 4.3711e-11 | 11.2756 |
| 0.25 | 0.75 | 1 | `executed` | True | -0.000893589 | 1 | 2.22045e-16 | 12.2634 |
| 0.25 | 0.75 | 2 | `executed` | True | -0.000682271 | 2 | 3.03924e-14 | 11.4208 |
| 0.5 | 0.25 | 0 | `executed` | True | -0.00728308 | 6 | 2.95111e-09 | 11.2574 |
| 0.5 | 0.25 | 1 | `executed` | True | -0.00446153 | 5 | 3.0881e-08 | 13.9436 |
| 0.5 | 0.25 | 2 | `executed` | True | -0.00365826 | 5 | 3.11231e-08 | 12.2863 |
| 0.5 | 0.5 | 0 | `executed` | True | -0.0071537 | 6 | 1.09293e-09 | 11.2472 |
| 0.5 | 0.5 | 1 | `executed` | True | -0.00495111 | 5 | 5.53516e-08 | 13.9436 |
| 0.5 | 0.5 | 2 | `executed` | True | -0.00420873 | 5 | 3.06547e-10 | 12.2547 |
| 0.5 | 0.75 | 0 | `executed` | True | -0.00870048 | 6 | 3.84344e-11 | 11.2049 |
| 0.5 | 0.75 | 1 | `executed` | True | -0.00436215 | 5 | 9.78166e-11 | 13.9436 |
| 0.5 | 0.75 | 2 | `executed` | True | -0.00502051 | 6 | 6.29965e-10 | 11.3767 |
| 0.75 | 0.25 | 0 | `executed` | True | -0.0153666 | 11 | 6.49549e-08 | 13.2503 |
| 0.75 | 0.25 | 1 | `executed` | True | -0.00303061 | 13 | 3.48687e-08 | 14.8563 |
| 0.75 | 0.25 | 2 | `executed` | True | -0.00969681 | 14 | 5.51027e-08 | 13.0933 |
| 0.75 | 0.5 | 0 | `executed` | True | -0.0144274 | 13 | 3.58966e-08 | 13.1398 |
| 0.75 | 0.5 | 1 | `executed` | True | -0.000575088 | 13 | 8.608e-08 | 14.8563 |
| 0.75 | 0.5 | 2 | `executed` | True | -0.0101196 | 13 | 9.47969e-08 | 13.0031 |
| 0.75 | 0.75 | 0 | `executed` | True | -0.0152262 | 11 | 2.05824e-12 | 13.0948 |
| 0.75 | 0.75 | 1 | `executed` | True | -0.00057655 | 13 | 5.53426e-09 | 14.8563 |
| 0.75 | 0.75 | 2 | `executed` | True | -0.0109131 | 12 | 2.59453e-09 | 12.8552 |

## Non-Implications

- No production readiness is concluded.
- No public API readiness is concluded.
- No posterior correctness is concluded.
- No HMC readiness is concluded.
- No general nonlinear-SSM validity is concluded.
- No claim that LEDH must match filterflow RegularisedTransform is concluded.
