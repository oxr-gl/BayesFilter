# LEDH-PFPF-OT LGSSM OT-Reset Moment Diagnostic Result

Date: 2026-06-26T10:52:35.193364+00:00

## Manifest

| Field | Value |
|---|---|
| num_particles | `128` |
| dense_parity_particles | `64` |
| seed_count | `10` |
| time_steps | `10` |
| xla | `True` |
| device_scope | `cpu` |
| cuda_visible_devices | `-1` |
| tf32_execution_enabled | `True` |
| runtime_seconds | `32.600918470008764` |

## Decision Table

| Field | Status |
|---|---|
| decision | H1 remains live: dense/streaming parity or mass residual veto failed. |
| primary_criterion_status | FAIL parity vetoes: state_dim=1 setting=eps0.5_steps8, state_dim=2 setting=eps0.5_steps8 |
| veto_diagnostic_status | FAIL |
| main_uncertainty | Whether tighter Sinkhorn changes the qualitative reset-moment pattern or merely attenuates the same barycentric contraction. |
| next_justified_action | Inspect transport orientation/normalization on the small shared cloud first. |
| not_concluded | No gradient correctness, SIR correctness, HMC readiness, posterior correctness, production readiness, or broad scientific validity. |

## Summary

| State dim | Setting | Total mean | Kalman | Delta | SD | MCSE | t0 cov ratio | t0 mean shift | t1 inc delta | Parity max diff | Dense col residual |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | eps0.5_steps8 | -6.497418 | -6.914505 | 0.417087 | 0.030462 | 0.009633 | 0.361629 | 1.432e-09 | 0.054821 | 1.490e-07 | 5.960e-07 |
| 2 | eps0.5_steps8 | -12.851150 | -13.784139 | 0.932989 | 0.045863 | 0.014503 | 0.274686 | 8.919e-09 | 0.127646 | 1.192e-07 | 5.960e-07 |

## Per-Time Records

### state_dim=1, setting=eps0.5_steps8

| t | inc delta | next inc delta | prefix delta | pre trace | post trace | Kalman trace | post/pre trace | pre-post mean L2 | ESS mean | row residual |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 0.027900 | 0.054821 | 0.027900 | 0.195481 | 0.070692 | 0.198061 | 0.361629 | 1.432e-09 | 118.557 | 9.934e-01 |
| 1 | 0.054821 | 0.045230 | 0.082721 | 0.133550 | 0.055298 | 0.155462 | 0.414062 | 3.725e-09 | 127.757 | 9.263e-01 |
| 2 | 0.045230 | 0.042534 | 0.127951 | 0.142084 | 0.055036 | 0.150148 | 0.387347 | 1.490e-09 | 127.844 | 9.525e-01 |
| 3 | 0.042534 | 0.042349 | 0.170485 | 0.133536 | 0.054072 | 0.149457 | 0.404922 | 3.725e-09 | 127.909 | 9.187e-01 |
| 4 | 0.042349 | 0.043418 | 0.212833 | 0.130573 | 0.049436 | 0.149367 | 0.378607 | 7.451e-10 | 127.961 | 9.526e-01 |
| 5 | 0.043418 | 0.039831 | 0.256251 | 0.134095 | 0.050058 | 0.149355 | 0.373306 | 3.725e-10 | 127.899 | 9.416e-01 |
| 6 | 0.039831 | 0.038223 | 0.296082 | 0.134367 | 0.055079 | 0.149354 | 0.409911 | 2.235e-09 | 127.604 | 9.150e-01 |
| 7 | 0.038223 | 0.039454 | 0.334305 | 0.141343 | 0.058273 | 0.149353 | 0.412279 | 4.470e-09 | 127.539 | 9.388e-01 |
| 8 | 0.039454 | 0.043327 | 0.373759 | 0.127265 | 0.050422 | 0.149353 | 0.396196 | 2.235e-09 | 127.900 | 9.533e-01 |
| 9 | 0.043327 | N/A | 0.417087 | 0.132052 | 0.051392 | 0.149353 | 0.389182 | 6.054e-10 | 127.853 | 9.347e-01 |

### state_dim=2, setting=eps0.5_steps8

| t | inc delta | next inc delta | prefix delta | pre trace | post trace | Kalman trace | post/pre trace | pre-post mean L2 | ESS mean | row residual |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 0.027318 | 0.127646 | 0.027318 | 0.392810 | 0.107899 | 0.396122 | 0.274686 | 8.919e-09 | 107.709 | 8.535e-01 |
| 1 | 0.127646 | 0.102255 | 0.154964 | 0.276264 | 0.083501 | 0.310925 | 0.302250 | 1.782e-09 | 127.701 | 8.589e-01 |
| 2 | 0.102255 | 0.100117 | 0.257219 | 0.264576 | 0.077867 | 0.300296 | 0.294309 | 5.296e-09 | 127.837 | 8.559e-01 |
| 3 | 0.100117 | 0.096015 | 0.357336 | 0.269066 | 0.083876 | 0.298914 | 0.311731 | 5.783e-09 | 127.880 | 7.558e-01 |
| 4 | 0.096015 | 0.098615 | 0.453351 | 0.257147 | 0.077613 | 0.298734 | 0.301824 | 2.829e-09 | 127.903 | 8.297e-01 |
| 5 | 0.098615 | 0.094676 | 0.551966 | 0.271227 | 0.083785 | 0.298710 | 0.308911 | 7.670e-09 | 127.850 | 7.661e-01 |
| 6 | 0.094676 | 0.094589 | 0.646642 | 0.261327 | 0.076173 | 0.298707 | 0.291486 | 3.744e-09 | 127.510 | 8.444e-01 |
| 7 | 0.094589 | 0.095904 | 0.741231 | 0.270653 | 0.081568 | 0.298707 | 0.301377 | 3.744e-09 | 127.509 | 8.698e-01 |
| 8 | 0.095904 | 0.095854 | 0.837134 | 0.267321 | 0.081282 | 0.298707 | 0.304061 | 7.264e-09 | 127.858 | 8.378e-01 |
| 9 | 0.095854 | N/A | 0.932989 | 0.274910 | 0.084178 | 0.298707 | 0.306201 | 2.172e-09 | 127.795 | 8.601e-01 |

## Interpretation

- state_dim=1 setting=eps0.5_steps8: total_delta=0.417087, t0_pre_post_mean_l2=1.432e-09, t0_post_pre_cov_trace_ratio=0.361629, t1_increment_delta=0.054821, parity_max_diff=1.490e-07, dense_col_resid=5.960e-07.
- state_dim=2 setting=eps0.5_steps8: total_delta=0.932989, t0_pre_post_mean_l2=8.919e-09, t0_post_pre_cov_trace_ratio=0.274686, t1_increment_delta=0.127646, parity_max_diff=1.192e-07, dense_col_resid=5.960e-07.
