# Retained-Teacher Sinkhorn Heldout Evaluation Result

## Decision

`RETAINED_TEACHER_SINKHORN_HELDOUT_EVAL_FAILED`

## Decision Table

| Budget | Student mean RMSE | Zero-init mean RMSE | Student max residual | Zero-init max residual | Student better-or-equal |
| --- | ---: | ---: | ---: | ---: | ---: |
| `5` | `1.670e-05` | `1.378e-04` | `9.878e-06` | `8.372e-05` | `2/2` |
| `10` | `2.284e-08` | `1.932e-07` | `1.408e-08` | `1.197e-07` | `1/2` |
| `20` | `9.728e-11` | `0.000e+00` | `2.727e-11` | `9.026e-11` | `0/2` |

## Interpretation

This rung compares student-warm-started retained Sinkhorn replay against zero-init replay on heldout teacher-data examples at fixed corrective budgets. Passing here is local evidence only for this deterministic LGSSM envelope and does not support posterior, HMC, or broad deployment claims.

## Non-Implications

- No posterior correctness is concluded.
- No HMC readiness is concluded.
- No production-readiness claim is concluded.
- No broad cross-model generalization claim is concluded.
- No promotion of the student over the retained teacher beyond this heldout rung is concluded.
