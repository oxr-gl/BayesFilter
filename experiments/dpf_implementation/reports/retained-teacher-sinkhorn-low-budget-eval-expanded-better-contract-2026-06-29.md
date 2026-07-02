# Retained-Teacher Sinkhorn Expanded Better-Contract Evaluation Result

## Decision

`RETAINED_TEACHER_SINKHORN_EXPANDED_HELDOUT_LOCAL_USEFULNESS_ON_DISCRIMINATING_BUDGETS`

## Decision Table

| Budget | Regime | Student mean RMSE | Zero-init mean RMSE | Student max residual | Zero-init max residual | Student better-or-equal |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| `5` | `discriminating` | `1.644e-05` | `5.921e-05` | `2.906e-05` | `8.372e-05` | `7/9` |
| `10` | `discriminating` | `3.372e-08` | `9.271e-08` | `5.680e-08` | `1.197e-07` | `2/9` |
| `20` | `saturated_zero_init` | `3.090e-09` | `0.000e+00` | `8.184e-09` | `5.709e-10` | `0/9` |

## Interpretation

This broader better-contract rung asks whether the donor-aligned one-half route still shows local usefulness when the heldout split is expanded and the primary interpretation is restricted to discriminating budgets. Saturated zero-init rungs remain explanatory only.

## Non-Implications

- No posterior correctness is concluded.
- No HMC readiness is concluded.
- No production-readiness claim is concluded.
- No broad cross-model generalization claim is concluded.
- No superiority at larger corrective budgets is concluded from this expanded low-budget rung.
