# LEDH-PFPF-OT LGSSM Reset-Variant Diagnostic

Date: 2026-06-27T06:42:22.970096+00:00

Status: `supports_barycentric_covariance_loss_root_cause`

## Manifest

- num_particles: `64`
- time_steps: `10`
- device_scope: `cpu`
- cuda_visible_devices: `-1`

## Variant Table

| dim | setting | variant | mean | Kalman | delta | abs z MCSE | cov ratio t0 | max row residual |
| ---: | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | eps0.5_steps20 | `ledh_no_ot` | -6.902608 | -6.914505 | 0.011897 | 1.778 | 1.000000 | NA |
| 1 | eps0.5_steps20 | `current_ot` | -6.641897 | -6.914505 | 0.272608 | 95.539 | 0.592853 | 2.041e-01 |
| 1 | eps0.5_steps20 | `row_normalized_ot` | -6.645216 | -6.914505 | 0.269289 | 102.854 | 0.604121 | 2.384e-07 |
| 1 | eps0.5_steps20 | `moment_restored_current_ot` | -6.893988 | -6.914505 | 0.020517 | 4.004 | 0.999965 | 1.833e-01 |
| 1 | eps0.5_steps100 | `ledh_no_ot` | -6.902608 | -6.914505 | 0.011897 | 1.778 | 1.000000 | NA |
| 1 | eps0.5_steps100 | `current_ot` | -6.643739 | -6.914505 | 0.270766 | 100.319 | 0.599533 | 6.803e-02 |
| 1 | eps0.5_steps100 | `row_normalized_ot` | -6.643816 | -6.914505 | 0.270689 | 100.509 | 0.599537 | 2.384e-07 |
| 1 | eps0.5_steps100 | `moment_restored_current_ot` | -6.892545 | -6.914505 | 0.021960 | 4.192 | 0.999966 | 9.478e-02 |
| 2 | eps0.5_steps20 | `ledh_no_ot` | -13.705706 | -13.784139 | 0.078433 | 2.417 | 1.000000 | NA |
| 2 | eps0.5_steps20 | `current_ot` | -12.929207 | -13.784139 | 0.854932 | 35.838 | 0.357120 | 8.130e-02 |
| 2 | eps0.5_steps20 | `row_normalized_ot` | -12.929556 | -13.784139 | 0.854583 | 35.759 | 0.358358 | 2.384e-07 |
| 2 | eps0.5_steps20 | `moment_restored_current_ot` | -13.683838 | -13.784139 | 0.100301 | 4.347 | 0.999893 | 1.474e-01 |
| 2 | eps0.5_steps100 | `ledh_no_ot` | -13.705706 | -13.784139 | 0.078433 | 2.417 | 1.000000 | NA |
| 2 | eps0.5_steps100 | `current_ot` | -12.929407 | -13.784139 | 0.854731 | 35.825 | 0.357876 | 1.976e-04 |
| 2 | eps0.5_steps100 | `row_normalized_ot` | -12.929407 | -13.784139 | 0.854731 | 35.825 | 0.357876 | 2.384e-07 |
| 2 | eps0.5_steps100 | `moment_restored_current_ot` | -13.682816 | -13.784139 | 0.101323 | 4.394 | 0.999893 | 4.768e-04 |

## Interpretation

```json
{
  "caution": "Moment restoration is diagnostic only; this does not approve a production reset route or certify gradients.",
  "status": "supports_barycentric_covariance_loss_root_cause",
  "summaries": [
    {
      "current_abs_delta": 0.27260828641650736,
      "current_cov_ratio_t0": 0.5928526520729065,
      "moment_cov_ratio_t0": 0.9999650120735168,
      "moment_restoration_improvement_factor": 13.28702534101245,
      "moment_restored_abs_delta": 0.020516878640628455,
      "no_ot_abs_delta": 0.011896616494632362,
      "row_normalized_abs_delta": 0.2692894997954136,
      "setting": "eps0.5_steps20",
      "state_dim": 1
    },
    {
      "current_abs_delta": 0.2707657876372105,
      "current_cov_ratio_t0": 0.5995326042175293,
      "moment_cov_ratio_t0": 0.999966025352478,
      "moment_restoration_improvement_factor": 12.33007299980127,
      "moment_restored_abs_delta": 0.02195978788135111,
      "no_ot_abs_delta": 0.011896616494632362,
      "row_normalized_abs_delta": 0.2706885400175816,
      "setting": "eps0.5_steps100",
      "state_dim": 1
    },
    {
      "current_abs_delta": 0.8549317019464837,
      "current_cov_ratio_t0": 0.3571203351020813,
      "moment_cov_ratio_t0": 0.9998930096626282,
      "moment_restoration_improvement_factor": 8.523689739409557,
      "moment_restored_abs_delta": 0.10030065946601496,
      "no_ot_abs_delta": 0.07843290739081965,
      "row_normalized_abs_delta": 0.854582657146679,
      "setting": "eps0.5_steps20",
      "state_dim": 2
    },
    {
      "current_abs_delta": 0.8547314303400384,
      "current_cov_ratio_t0": 0.3578760623931885,
      "moment_cov_ratio_t0": 0.9998931884765625,
      "moment_restoration_improvement_factor": 8.435710000697364,
      "moment_restored_abs_delta": 0.10132299833320246,
      "no_ot_abs_delta": 0.07843290739081965,
      "row_normalized_abs_delta": 0.8547314303400384,
      "setting": "eps0.5_steps100",
      "state_dim": 2
    }
  ]
}
```
