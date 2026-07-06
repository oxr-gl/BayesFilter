# Austria SIR d18 Expanded Retained-Teacher Zero-Init Budget Probe Result

## Decision

`AUSTRIA_SIR_D18_EXPANDED_ZERO_INIT_DISCRIMINATING_BUDGETS_IDENTIFIED`

## Decision Table

| Budget | Regime | Zero-init mean RMSE | Zero-init max RMSE | Zero-init max residual | Heldout examples |
| --- | --- | ---: | ---: | ---: | ---: |
| `1` | `discriminating` | `1.974e-02` | `3.609e-02` | `4.484e-03` | `9` |
| `2` | `discriminating` | `5.617e-04` | `1.488e-03` | `1.881e-04` | `9` |
| `3` | `discriminating` | `1.874e-05` | `6.621e-05` | `8.849e-06` | `9` |
| `5` | `discriminating` | `2.654e-08` | `1.307e-07` | `1.789e-08` | `9` |

## Probe Summary

- Discriminating budgets: `[1, 2, 3, 5]`
- Saturated budgets: `[]`
- Recommended primary budgets: `[3, 5]`
- Recommended explanatory budgets: `[]`

## Interpretation

The expanded Austria SIR d18 artifact still furnishes a governed discriminating rung, so the non-promotion disambiguation step can remain on the same ladder family rather than drifting into a ladder-calibration problem.

## Non-Implications

- No donor-aligned student win/loss claim is concluded by this zero-init-only probe.
- No large-particle or N=10000 claim is concluded.
- No GPU scaling claim is concluded.
- No production-readiness claim is concluded.
