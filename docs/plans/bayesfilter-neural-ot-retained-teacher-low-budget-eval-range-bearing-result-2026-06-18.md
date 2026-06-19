# Retained-Teacher Sinkhorn Range-Bearing Evaluation Result

## Decision

`RETAINED_TEACHER_SINKHORN_LOW_BUDGET_EVAL_RANGE_BEARING_FAILED`

## Decision Table

| Budget | Student mean RMSE | Zero-init mean RMSE | Student max residual | Zero-init max residual | Student better-or-equal |
| --- | ---: | ---: | ---: | ---: | ---: |
| `10` | `1.611e-16` | `0.000e+00` | `4.441e-16` | `2.220e-16` | `0/18` |
| `20` | `1.611e-16` | `0.000e+00` | `4.441e-16` | `2.220e-16` | `0/18` |

## Interpretation

This rung asks whether the retained-teacher warm-start effect survives the move to the range-bearing family under a calibrated low-budget replay contract.

## Non-Implications

- No posterior correctness is concluded.
- No HMC readiness is concluded.
- No broad nonlinear generalization claim is concluded.
- No production-readiness claim is concluded.
- No success on structural families is concluded from this range-bearing rung.
