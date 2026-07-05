# Retained-Teacher Sinkhorn SV Better-Contract Evaluation Result

## Decision

`RETAINED_TEACHER_SINKHORN_SV_HELDOUT_LOCAL_USEFULNESS_ON_DISCRIMINATING_BUDGETS`

## Decision Table

| Budget | Regime | Student mean RMSE | Zero-init mean RMSE | Student max residual | Zero-init max residual | Student better-or-equal |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| `10` | `discriminating` | `6.030e-06` | `5.098e-05` | `3.953e-06` | `3.022e-05` | `4/4` |
| `20` | `saturated_zero_init` | `6.620e-09` | `0.000e+00` | `8.405e-10` | `6.427e-09` | `0/4` |

## Interpretation

This calibrated SV better-contract rung asks whether the donor-aligned one-half route survives an envelope shift when the primary budget remains discriminating and the larger budget is treated as explanatory only.

## Non-Implications

- No posterior correctness is concluded.
- No HMC readiness is concluded.
- No broad nonlinear generalization claim is concluded.
- No production-readiness claim is concluded.
- No success on harsher SV budget-5 replay is concluded from this calibrated rung.
