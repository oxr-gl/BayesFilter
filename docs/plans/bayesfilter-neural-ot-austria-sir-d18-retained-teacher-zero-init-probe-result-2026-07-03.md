# Austria SIR d18 Retained-Teacher Zero-Init Budget Probe Result

## Decision

`AUSTRIA_SIR_D18_ZERO_INIT_DISCRIMINATING_BUDGETS_IDENTIFIED`

## Decision Table

| Budget | Regime | Zero-init mean RMSE | Zero-init max RMSE | Zero-init max residual | Heldout examples |
| --- | --- | ---: | ---: | ---: | ---: |
| `1` | `discriminating` | `2.317e-02` | `3.466e-02` | `4.188e-03` | `4` |
| `2` | `discriminating` | `6.644e-04` | `1.488e-03` | `1.881e-04` | `4` |
| `3` | `discriminating` | `2.357e-05` | `6.621e-05` | `8.849e-06` | `4` |
| `5` | `discriminating` | `3.913e-08` | `1.307e-07` | `1.789e-08` | `4` |

## Probe Summary

- Discriminating budgets: `[1, 2, 3, 5]`
- Saturated budgets: `[]`
- Recommended primary budgets: `[3, 5]`
- Recommended explanatory budgets: `[]`

## Interpretation

The current Austria SIR d18 artifact furnishes a governed discriminating rung. Future donor-aligned replay evaluation should be bound to the recommended primary budgets rather than reusing any saturated higher-budget comparison as if it were informative.

## Non-Implications

- No donor-aligned student win/loss claim is concluded by this zero-init-only probe.
- No large-particle or N=10000 claim is concluded.
- No GPU scaling claim is concluded.
- No production-readiness claim is concluded.
