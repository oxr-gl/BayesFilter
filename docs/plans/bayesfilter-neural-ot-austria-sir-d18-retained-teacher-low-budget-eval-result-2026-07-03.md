# Austria SIR d18 Retained-Teacher Low-Budget Evaluation Result

## Decision

`RETAINED_TEACHER_SINKHORN_AUSTRIA_SIR_D18_NON_PROMOTED_ON_DISCRIMINATING_BUDGETS`

## Plan reference
- `docs/plans/bayesfilter-neural-ot-austria-sir-d18-retained-teacher-smoke-test-plan-2026-07-03.md`

## Command actually run
```bash
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_retained_teacher_sinkhorn_low_budget_eval_austria_sir_d18_tf
```

## Decision Table

| Budget | Regime | Student mean RMSE | Zero-init mean RMSE | Student max residual | Zero-init max residual | Student better-or-equal |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| `2` | `discriminating` | `7.490e-04` | `6.644e-04` | `2.143e-04` | `1.881e-04` | `1/4` |
| `3` | `discriminating` | `2.789e-05` | `2.357e-05` | `8.943e-06` | `8.849e-06` | `1/4` |
| `5` | `discriminating` | `4.488e-08` | `3.913e-08` | `1.674e-08` | `1.789e-08` | `1/4` |

## Interpretation

The Austria SIR d18 smoke-test interface now works end to end:
- teacher-data generation succeeds under the reviewed scale-adaptive teacher-generation repair,
- the zero-init probe identifies a fully discriminating low-budget ladder,
- and the donor-aligned replay evaluation runs to completion on that governed ladder.

However, on this first high-dimensional smoke-test artifact the donor-aligned route is **non-promoted on discriminating budgets**: student replay is slightly worse than zero-init at budgets `2`, `3`, and `5`.

This should therefore be interpreted as:
- **engineering interface success**,
- **high-dimensional discriminating-rung availability**,
- but **no local usefulness win on this first Austria SIR d18 artifact**.

## Non-Implications

- No large-particle or N=10000 claim is concluded.
- No GPU scaling claim is concluded.
- No production-readiness claim is concluded.
- No parameterized-SIR claim is concluded.
