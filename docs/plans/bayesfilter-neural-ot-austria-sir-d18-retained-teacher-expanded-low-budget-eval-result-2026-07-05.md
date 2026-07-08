# Austria SIR d18 Expanded Retained-Teacher Low-Budget Evaluation Result

## Decision

`RETAINED_TEACHER_SINKHORN_AUSTRIA_SIR_D18_EXPANDED_NON_PROMOTED_ON_DISCRIMINATING_BUDGETS`

## Plan reference
- `docs/plans/bayesfilter-neural-ot-austria-sir-d18-retained-teacher-nonpromotion-disambiguation-plan-2026-07-05.md`

## Command actually run
```bash
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_retained_teacher_sinkhorn_low_budget_eval_austria_sir_d18_expanded_tf
```

## Decision Table

| Budget | Regime | Student mean RMSE | Zero-init mean RMSE | Student max residual | Zero-init max residual | Student better-or-equal |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| `3` | `discriminating` | `2.310e-05` | `1.874e-05` | `9.235e-06` | `8.849e-06` | `2/9` |
| `5` | `discriminating` | `3.254e-08` | `2.654e-08` | `1.674e-08` | `1.789e-08` | `2/9` |

## Interpretation

This expanded Austria SIR d18 run keeps the same model, teacher-generation repair, and replay semantics while modestly strengthening the artifact from `4/4` train/heldout examples to `9/9` train/heldout examples.

The result remains **non-promoted on discriminating budgets**:
- the donor-aligned route still loses to zero-init at budget `3`, and
- still loses to zero-init at budget `5`.

Under the governing disambiguation plan, this strengthens the **local non-usefulness explanation** relative to the “first artifact too weak” explanation. The modest artifact-strengthening pass did not flip the route into a discriminating-budget win.

## Non-Implications

- No large-particle or N=10000 claim is concluded.
- No GPU scaling claim is concluded.
- No production-readiness claim is concluded.
- No parameterized-SIR claim is concluded.
