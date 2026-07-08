# Retained-Teacher Sinkhorn Better-Contract Heldout Evaluation Result

## Decision

`RETAINED_TEACHER_SINKHORN_HELDOUT_EVAL_LOCAL_USEFULNESS_ON_DISCRIMINATING_BUDGETS`

## Decision Table

| Budget | Regime | Student mean RMSE | Zero-init mean RMSE | Student max residual | Zero-init max residual | Student better-or-equal |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| `5` | `discriminating` | `7.246e-06` | `1.378e-04` | `4.430e-06` | `8.372e-05` | `2/2` |
| `10` | `discriminating` | `1.030e-08` | `1.932e-07` | `6.329e-09` | `1.197e-07` | `1/2` |
| `20` | `saturated_zero_init` | `1.030e-08` | `0.000e+00` | `6.329e-09` | `9.026e-11` | `0/2` |

## Interpretation

This better-contract rung separates discriminating budgets from saturated zero-init budgets. Failure to beat zero-init on a saturated high-budget rung is not treated as algorithm failure by itself; the result is instead interpreted through the discriminating budget rows and the residual contract.

## Non-Implications

- No posterior correctness is concluded.
- No HMC readiness is concluded.
- No production-readiness claim is concluded.
- No broad cross-model generalization claim is concluded.
- No promotion of the student over the retained teacher beyond this heldout rung is concluded.
