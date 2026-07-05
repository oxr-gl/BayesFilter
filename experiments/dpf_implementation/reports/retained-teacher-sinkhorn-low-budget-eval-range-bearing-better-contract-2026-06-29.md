# Retained-Teacher Sinkhorn Range-Bearing Better-Contract Evaluation Result

## Decision

`RETAINED_TEACHER_SINKHORN_RANGE_BEARING_LOCAL_USEFULNESS_ON_DISCRIMINATING_BUDGETS`

## Decision Table

| Budget | Regime | Student mean RMSE | Zero-init mean RMSE | Student max residual | Zero-init max residual | Student better-or-equal |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| `2` | `discriminating` | `2.352e-10` | `8.465e-08` | `2.126e-08` | `1.051e-05` | `18/18` |
| `3` | `discriminating` | `4.687e-13` | `2.252e-10` | `5.401e-11` | `3.010e-08` | `17/18` |
| `5` | `saturated_zero_init` | `1.585e-16` | `1.819e-15` | `4.441e-16` | `2.386e-13` | `5/18` |

## Interpretation

This range-bearing better-contract rung uses the P6-calibrated discriminating budgets (`2`, `3`) as the primary evidence and keeps the first saturated rung (`5`) explanatory only. The decision should therefore be read as governed local usefulness or local non-promotion on an actually informative range-bearing ladder, not as a replay of the earlier saturated `10`/`20` comparison.

## Non-Implications

- No posterior correctness is concluded.
- No HMC readiness is concluded.
- No broad nonlinear generalization claim is concluded.
- No production-readiness claim is concluded.
- No success on structural families is concluded from this range-bearing rung.
