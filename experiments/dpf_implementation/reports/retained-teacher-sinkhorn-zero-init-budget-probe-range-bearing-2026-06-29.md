# P6 Result: Range-Bearing Discriminating-Rung Recovery

## Decision

`RANGE_BEARING_ZERO_INIT_DISCRIMINATING_BUDGETS_IDENTIFIED`

## Decision Table

| Budget | Regime | Zero-init mean RMSE | Zero-init max RMSE | Zero-init max residual | Heldout examples |
| --- | --- | ---: | ---: | ---: | ---: |
| `1` | `discriminating` | `3.683e-05` | `5.117e-04` | `3.420e-03` | `18` |
| `2` | `discriminating` | `8.465e-08` | `1.389e-06` | `1.051e-05` | `18` |
| `3` | `discriminating` | `2.252e-10` | `3.884e-09` | `3.010e-08` | `18` |
| `5` | `saturated_zero_init` | `1.819e-15` | `3.051e-14` | `2.386e-13` | `18` |
| `8` | `saturated_zero_init` | `8.226e-17` | `1.903e-16` | `4.441e-16` | `18` |
| `10` | `saturated_zero_init` | `0.000e+00` | `0.000e+00` | `2.220e-16` | `18` |
| `20` | `saturated_zero_init` | `0.000e+00` | `0.000e+00` | `2.220e-16` | `18` |

## Probe Summary

- Discriminating budgets: `[1, 2, 3]`
- Saturated budgets: `[5, 8, 10, 20]`
- Recommended primary budgets: `[2, 3]`
- Recommended explanatory budgets: `[5]`

## Interpretation

The current range-bearing artifact does furnish a governed discriminating rung. Future donor-aligned range-bearing evaluation should be rebound to the recommended primary budgets rather than reusing the already-saturated `10`/`20` pair as if it were a valid promotion comparator.

## Non-Implications

- No donor-aligned student win/loss claim is concluded by this zero-init-only probe.
- No algorithm-failure claim is concluded.
- No posterior correctness is concluded.
- No HMC readiness is concluded.
- No broad range-bearing generalization claim is concluded.
