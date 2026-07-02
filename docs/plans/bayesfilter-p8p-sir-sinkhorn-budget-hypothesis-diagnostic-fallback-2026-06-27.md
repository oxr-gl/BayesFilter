# P8p SIR Sinkhorn Budget Hypothesis Diagnostic

Date: 2026-06-26T19:51:49.517956+00:00

Status: `budget10_row_residual_already_passes_this_screen`

## Question

Does the P8p SIR d18 gradient mismatch track finite Sinkhorn under-convergence when only the transport budget is varied?

## Evidence Contract

- Same fixed-randomness SIR target, theta, seeds, route, chunks, dtype, and TF32 policy across candidate budgets.
- Primary transport veto: streaming row residual must be below the predeclared threshold.
- FD comparator: 13-point raw-coordinate regression FD, dropping the lowest and highest objective values before fitting.
- Report slope standard error explicitly; errors beyond 2 slope SE remain suspect.
- No SIR gradient correctness, HMC readiness, production readiness, or posterior claim is made.

## Run Summary

- Shape: `T=3`, `N=64`, seeds `[81120, 81121, 81122, 81123, 81124]`
- Candidate steps: `[1, 2, 5, 10, 20]`
- Row residual threshold: `0.001`
- Device expectation: `gpu`, outputs `['/job:localhost/replica:0/task:0/device:GPU:0', '/job:localhost/replica:0/task:0/device:GPU:0']`

## Budget Table

| Steps | row residual | row pass | max |z| | all within 2 SE | objective |
| ---: | ---: | --- | ---: | --- | ---: |
| 1 | 3.900111e-03 | False | 46.263 | False | -125.470177 |
| 2 | 3.252864e-03 | False | 220.170 | False | -125.472839 |
| 5 | 7.109642e-04 | True | 359.337 | False | -125.475380 |
| 10 | 1.418591e-05 | True | 441.064 | False | -125.474632 |
| 20 | 1.907349e-06 | True | 394.230 | False | -125.474709 |

## Direction Details

### Steps 1

| Parameter | manual grad | FD slope | manual-FD | slope SE | z | R2 | within 2 SE |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `log_kappa_scale` | -308.159241 | -262.926483 | -45.232758 | 0.977730 | -46.263 | 0.999876 | False |
| `log_nu_scale` | 108.000870 | 105.036568 | 2.964302 | 0.158118 | 18.747 | 0.999980 | False |
| `log_obs_noise_scale` | 44.690441 | 46.686340 | -1.995899 | 0.087183 | -22.893 | 0.999969 | False |

### Steps 2

| Parameter | manual grad | FD slope | manual-FD | slope SE | z | R2 | within 2 SE |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `log_kappa_scale` | -170.172424 | -263.071838 | 92.899414 | 1.041443 | 89.203 | 0.999859 | False |
| `log_nu_scale` | 72.359230 | 104.971588 | -32.612358 | 0.148124 | -220.170 | 0.999982 | False |
| `log_obs_noise_scale` | 45.341766 | 46.605194 | -1.263428 | 0.118021 | -10.705 | 0.999942 | False |

### Steps 5

| Parameter | manual grad | FD slope | manual-FD | slope SE | z | R2 | within 2 SE |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `log_kappa_scale` | -128.917358 | -263.132538 | 134.215179 | 1.008169 | 133.128 | 0.999868 | False |
| `log_nu_scale` | 63.575481 | 105.049477 | -41.473995 | 0.115418 | -359.337 | 0.999989 | False |
| `log_obs_noise_scale` | 45.412880 | 46.768051 | -1.355171 | 0.105785 | -12.811 | 0.999954 | False |

### Steps 10

| Parameter | manual grad | FD slope | manual-FD | slope SE | z | R2 | within 2 SE |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `log_kappa_scale` | -121.829636 | -263.216583 | 141.386948 | 1.023150 | 138.188 | 0.999864 | False |
| `log_nu_scale` | 61.905548 | 105.087280 | -43.181732 | 0.097903 | -441.064 | 0.999992 | False |
| `log_obs_noise_scale` | 45.218079 | 46.746548 | -1.528469 | 0.093660 | -16.319 | 0.999964 | False |

### Steps 20

| Parameter | manual grad | FD slope | manual-FD | slope SE | z | R2 | within 2 SE |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `log_kappa_scale` | -138.169250 | -263.221130 | 125.051880 | 1.035010 | 120.822 | 0.999861 | False |
| `log_nu_scale` | 63.498390 | 105.090340 | -41.591949 | 0.105502 | -394.230 | 0.999991 | False |
| `log_obs_noise_scale` | 45.698563 | 46.748138 | -1.049576 | 0.090716 | -11.570 | 0.999966 | False |

## Interpretation

{
  "best_fd_z_steps": 1,
  "best_max_abs_fd_z": 46.26304495407833,
  "caution": "This diagnostic can implicate finite Sinkhorn budget, but it cannot certify SIR gradient correctness or rule out reset/covariance or objective-semantics errors.",
  "fd_z_drop_from_steps10": true,
  "lowest_row_residual": 1.9073486328125e-06,
  "lowest_row_steps": 20,
  "residuals_drop": true,
  "row10_residual": 1.4185905456542969e-05,
  "row_pass_exists": true,
  "status": "budget10_row_residual_already_passes_this_screen"
}
