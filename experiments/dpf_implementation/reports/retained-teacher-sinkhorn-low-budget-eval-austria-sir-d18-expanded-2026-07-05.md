# Austria SIR d18 Expanded Retained-Teacher Low-Budget Evaluation Result

## Decision

`RETAINED_TEACHER_SINKHORN_AUSTRIA_SIR_D18_EXPANDED_NON_PROMOTED_ON_DISCRIMINATING_BUDGETS`

## Decision Table

| Budget | Regime | Student mean RMSE | Zero-init mean RMSE | Student max residual | Zero-init max residual | Student better-or-equal |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| `3` | `discriminating` | `2.310e-05` | `1.874e-05` | `9.235e-06` | `8.849e-06` | `2/9` |
| `5` | `discriminating` | `3.254e-08` | `2.654e-08` | `1.674e-08` | `1.789e-08` | `2/9` |

## Interpretation

This expanded Austria SIR d18 run keeps the same model, repair, and replay semantics while modestly strengthening the artifact. Its role is to distinguish weak-artifact non-promotion from persistent local non-usefulness on the fixed family.

## Non-Implications

- No large-particle or N=10000 claim is concluded.
- No GPU scaling claim is concluded.
- No production-readiness claim is concluded.
- No parameterized-SIR claim is concluded.
