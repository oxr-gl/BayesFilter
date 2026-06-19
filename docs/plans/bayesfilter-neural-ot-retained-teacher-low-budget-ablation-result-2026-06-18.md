# Retained-Teacher Sinkhorn Low-Budget Warm-Start Ablation Result

## Decision

`RETAINED_TEACHER_SINKHORN_LOW_BUDGET_ABLATION_PASSED`

## Decision Table

| Budget | Method | Mean RMSE | Max RMSE | Max residual |
| --- | --- | ---: | ---: | ---: |
| `5` | `zero_init` | `5.921e-05` | `2.705e-04` | `8.372e-05` |
| `5` | `heuristic` | `5.921e-05` | `2.705e-04` | `8.372e-05` |
| `5` | `learned_base` | `2.659e-05` | `1.809e-04` | `6.642e-05` |
| `5` | `learned_wide` | `2.405e-05` | `1.352e-04` | `4.963e-05` |
| `10` | `zero_init` | `9.271e-08` | `3.864e-07` | `1.197e-07` |
| `10` | `heuristic` | `9.271e-08` | `3.864e-07` | `1.197e-07` |
| `10` | `learned_base` | `7.706e-08` | `6.159e-07` | `2.262e-07` |
| `10` | `learned_wide` | `6.398e-08` | `4.603e-07` | `1.691e-07` |
| `20` | `zero_init` | `0.000e+00` | `0.000e+00` | `5.709e-10` |
| `20` | `heuristic` | `8.567e-17` | `1.066e-16` | `5.709e-10` |
| `20` | `learned_base` | `2.896e-09` | `2.378e-08` | `8.658e-09` |
| `20` | `learned_wide` | `2.142e-10` | `1.706e-09` | `5.191e-11` |

## Interpretation

This rung attributes the low-budget effect across zero-init, heuristic, learned-base, and learned-wide warm-start regimes on the expanded LGSSM artifact. Passing here means the learned-base model remains competitive with both zero-init and heuristic at the primary budgets.

## Non-Implications

- No posterior correctness is concluded.
- No HMC readiness is concluded.
- No production-readiness claim is concluded.
- No broad cross-model generalization claim is concluded.
- No universal architecture recommendation is concluded beyond this envelope.
