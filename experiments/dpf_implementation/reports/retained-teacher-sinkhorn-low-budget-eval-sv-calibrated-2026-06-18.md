# Retained-Teacher Sinkhorn SV Calibrated Evaluation Result

## Decision

`RETAINED_TEACHER_SINKHORN_LOW_BUDGET_EVAL_SV_CALIBRATED_PASSED`

## Decision Table

| Budget | Student mean RMSE | Zero-init mean RMSE | Student max residual | Zero-init max residual | Student better-or-equal |
| --- | ---: | ---: | ---: | ---: | ---: |
| `10` | `1.346e-05` | `5.098e-05` | `8.462e-06` | `3.022e-05` | `4/4` |
| `20` | `7.737e-09` | `0.000e+00` | `1.483e-09` | `6.427e-09` | `0/4` |

## Interpretation

This rung asks a narrower first-cross-envelope question: whether the retained-teacher warm-start effect survives on stochastic volatility when the family is evaluated at a calibrated low-budget replay setting centered on `K_corr = 10`.

## Non-Implications

- No posterior correctness is concluded.
- No HMC readiness is concluded.
- No broad nonlinear generalization claim is concluded.
- No production-readiness claim is concluded.
- No success on harsher SV budget-5 replay is concluded from this calibrated rung.
