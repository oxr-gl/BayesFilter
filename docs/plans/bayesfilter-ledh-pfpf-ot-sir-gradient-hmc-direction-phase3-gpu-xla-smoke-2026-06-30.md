# P8p SIR Sinkhorn Budget Hypothesis Diagnostic

Date: 2026-06-30T11:55:01.245863+00:00

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

- Shape: `T=1`, `N=16`, seeds `[81120, 81121]`
- Candidate steps: `[10]`
- Row residual threshold: `0.001`
- Device expectation: `gpu`, outputs `['/job:localhost/replica:0/task:0/device:GPU:0', '/job:localhost/replica:0/task:0/device:GPU:0']`

## Budget Table

| Steps | route pass | row residual | row pass | max slope z | max combined z | all HMC direction pass | objective |
| ---: | --- | ---: | --- | ---: | ---: | --- | ---: |
| 10 | True | 3.933907e-06 | True | 9.194 | 5.151 | False | -36.171509 |

## Direction Details

### Steps 10

| Parameter | manual grad | FD slope | manual-FD | slope SE | seed MCSE | combined SE | combined z | precision pass | direction pass | reason | supportive |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- | --- | --- |
| `log_kappa_scale` | -9.373708 | 20.216122 | -29.589829 | 5.734514 | 0.340763 | 5.744629 | -5.151 | False | False | `inconclusive_precision_veto` | False |
| `log_nu_scale` | 3.432503 | 0.301634 | 3.130869 | 1.221258 | 0.125077 | 1.227646 | 2.550 | False | False | `inconclusive_precision_veto` | False |
| `log_obs_noise_scale` | 4.548911 | 4.643304 | -0.094393 | 0.010266 | 0.311326 | 0.311495 | -0.303 | True | True | `within_2_combined_se` | False |

## Interpretation

{
  "best_fd_z_steps": 10,
  "best_max_abs_fd_z": 9.194453644584426,
  "caution": "This diagnostic can implicate finite Sinkhorn budget, but it cannot certify SIR gradient correctness or rule out reset/covariance or objective-semantics errors.",
  "fd_z_drop_from_steps10": false,
  "hmc_direction_pass_exists": false,
  "lowest_row_residual": 3.933906555175781e-06,
  "lowest_row_steps": 10,
  "residuals_drop": false,
  "row10_residual": 3.933906555175781e-06,
  "row_pass_exists": true,
  "status": "budget10_row_residual_already_passes_this_screen"
}
