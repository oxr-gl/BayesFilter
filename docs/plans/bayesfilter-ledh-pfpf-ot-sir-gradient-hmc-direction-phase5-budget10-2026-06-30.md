# P8p SIR Sinkhorn Budget Hypothesis Diagnostic

Date: 2026-06-30T16:20:41.632721+00:00

Status: `budget10_row_residual_already_passes_this_screen`

## Question

Does the P8p SIR d18 gradient mismatch track finite Sinkhorn under-convergence when only the transport budget is varied?

## Evidence Contract

- Same fixed-randomness SIR target, theta, seeds, route, chunks, dtype, and TF32 policy across candidate budgets.
- Primary transport veto: streaming row residual must be below the predeclared threshold.
- FD comparator: 13-point raw-coordinate regression FD, dropping the lowest and highest objective values before fitting.
- Report slope standard error, seed-gradient MCSE, combined SE, precision vetoes, and direction pass reasons explicitly.
- No SIR gradient correctness, HMC readiness, production readiness, or posterior claim is made.

## Run Summary

- Shape: `T=3`, `N=64`, seeds `[81120, 81121, 81122, 81123, 81124]`
- Candidate steps: `[10]`
- Row residual threshold: `0.001`
- Device expectation: `gpu`, outputs `['/job:localhost/replica:0/task:0/device:GPU:0', '/job:localhost/replica:0/task:0/device:GPU:0']`

## Budget Table

| Steps | route pass | row residual | row pass | max slope z | max combined z | all HMC direction pass | objective |
| ---: | --- | ---: | --- | ---: | ---: | --- | ---: |
| 10 | True | 1.472235e-05 | True | 362.544 | 2.828 | False | -125.473839 |

## Direction Details

### Steps 10

| Parameter | manual grad | FD slope | manual-FD | slope SE | seed MCSE | combined SE | combined z | precision pass | direction pass | reason | supportive |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- | --- | --- |
| `log_kappa_scale` | -143.369888 | -263.185455 | 119.815567 | 1.046763 | 48.939884 | 48.951077 | 2.448 | False | False | `inconclusive_precision_veto` | False |
| `log_nu_scale` | 68.266624 | 105.052803 | -36.786179 | 0.101467 | 13.006544 | 13.006940 | -2.828 | True | False | `within_4_combined_se_requires_ladder_certificate` | False |
| `log_obs_noise_scale` | 46.060081 | 46.766800 | -0.706718 | 0.065962 | 0.542973 | 0.546964 | -1.292 | True | True | `within_2_combined_se` | False |

## Interpretation

{
  "best_fd_z_steps": 10,
  "best_max_abs_fd_z": 362.54378733987676,
  "caution": "This diagnostic can implicate finite Sinkhorn budget, but it cannot certify SIR gradient correctness or rule out reset/covariance or objective-semantics errors.",
  "fd_z_drop_from_steps10": false,
  "hmc_direction_pass_exists": false,
  "lowest_row_residual": 1.4722347259521484e-05,
  "lowest_row_steps": 10,
  "residuals_drop": false,
  "row10_residual": 1.4722347259521484e-05,
  "row_pass_exists": true,
  "status": "budget10_row_residual_already_passes_this_screen"
}
