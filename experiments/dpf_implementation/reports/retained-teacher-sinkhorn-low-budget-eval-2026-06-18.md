# Retained-Teacher Sinkhorn Low-Budget Heldout Evaluation Result

## Decision

`RETAINED_TEACHER_SINKHORN_LOW_BUDGET_EVAL_PASSED`

## Decision Table

| Budget | Student mean RMSE | Zero-init mean RMSE | Student max residual | Zero-init max residual | Student better-or-equal |
| --- | ---: | ---: | ---: | ---: | ---: |
| `5` | `1.670e-05` | `1.378e-04` | `9.878e-06` | `8.372e-05` | `2/2` |
| `10` | `2.284e-08` | `1.932e-07` | `1.408e-08` | `1.197e-07` | `1/2` |
| `20` | `9.728e-11` | `0.000e+00` | `2.727e-11` | `9.026e-11` | `0/2` |

## Interpretation

This rung asks a narrower question than the earlier heldout evaluation: whether the warm-start student helps in the low-budget regime where corrective Sinkhorn iterations are intentionally scarce. A pass here is local evidence for low-budget acceleration only.

## Non-Implications

- No posterior correctness is concluded.
- No HMC readiness is concluded.
- No production-readiness claim is concluded.
- No broad cross-model generalization claim is concluded.
- No superiority at larger corrective budgets is concluded from this low-budget rung.
