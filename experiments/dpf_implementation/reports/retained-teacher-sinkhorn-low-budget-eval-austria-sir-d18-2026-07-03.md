# Austria SIR d18 Retained-Teacher Low-Budget Evaluation Result

## Decision

`RETAINED_TEACHER_SINKHORN_AUSTRIA_SIR_D18_NON_PROMOTED_ON_DISCRIMINATING_BUDGETS`

## Decision Table

| Budget | Regime | Student mean RMSE | Zero-init mean RMSE | Student max residual | Zero-init max residual | Student better-or-equal |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| `2` | `discriminating` | `7.490e-04` | `6.644e-04` | `2.143e-04` | `1.881e-04` | `1/4` |
| `3` | `discriminating` | `2.789e-05` | `2.357e-05` | `8.943e-06` | `8.849e-06` | `1/4` |
| `5` | `discriminating` | `4.488e-08` | `3.913e-08` | `1.674e-08` | `1.789e-08` | `1/4` |

## Interpretation

This Austria SIR d18 smoke-test rung uses the discriminating budgets identified by the zero-init probe as the primary evidence and keeps the first saturated rung explanatory only. The result should therefore be read first as interface success or failure, and only second as local usefulness or non-promotion on an informative high-dimensional ladder.

## Non-Implications

- No large-particle or N=10000 claim is concluded.
- No GPU scaling claim is concluded.
- No production-readiness claim is concluded.
- No parameterized-SIR claim is concluded.
