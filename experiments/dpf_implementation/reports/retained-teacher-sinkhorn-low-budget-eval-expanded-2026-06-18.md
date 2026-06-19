# Retained-Teacher Sinkhorn Expanded Low-Budget Evaluation Result

## Decision

`RETAINED_TEACHER_SINKHORN_LOW_BUDGET_EVAL_EXPANDED_PASSED`

## Decision Table

| Budget | Student mean RMSE | Zero-init mean RMSE | Student max residual | Zero-init max residual | Student better-or-equal |
| --- | ---: | ---: | ---: | ---: | ---: |
| `5` | `2.552e-05` | `5.921e-05` | `6.389e-05` | `8.372e-05` | `8/9` |
| `10` | `7.424e-08` | `9.271e-08` | `2.176e-07` | `1.197e-07` | `2/9` |
| `20` | `2.374e-09` | `0.000e+00` | `7.023e-09` | `5.709e-10` | `0/9` |

## Interpretation

This rung checks whether the earlier low-budget warm-start effect survives a modest expansion of train and heldout seed coverage on the same LGSSM family. A pass remains local evidence only for this envelope.

## Non-Implications

- No posterior correctness is concluded.
- No HMC readiness is concluded.
- No production-readiness claim is concluded.
- No broad cross-model generalization claim is concluded.
- No superiority at larger corrective budgets is concluded from this expanded low-budget rung.
