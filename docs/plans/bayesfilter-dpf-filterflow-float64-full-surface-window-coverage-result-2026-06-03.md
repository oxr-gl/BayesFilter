# Result: FilterFlow Float64 Full-Surface Window Coverage

## Decision

`filterflow_float64_full_surface_first_gradient_mismatch_localized`

## Evidence Contract

This is a BayesFilter-vs-local-FilterFlow difference audit only. The comparator
is the local float64 FilterFlow branch
`bayesfilter-py311-float64-reference` at
`1e5fbc288c1c11fc18ba01bb4842832e2088b800`. A pass means scalar and diagonal
GradientTape values agree within the existing float64 audit tolerances for the
covered row window. It does not imply mathematical correctness of either
implementation.

## Window Coverage

| Window | Status | Notes |
| --- | --- | --- |
| `0-19` | pass | Prior pass; no first failure. |
| `20-39` | pass | Completed in this continuation. |
| `40-59` | pass | Completed in this continuation. |
| `60-79` | pass | Completed in this continuation. |
| `80-99` | pass | Completed in this continuation. |
| `100-119` | pass | Completed in this continuation. |
| `120-139` | pass | Completed in this continuation. |
| `140-159` | pass | Completed in this continuation. |
| `160-179` | gradient mismatch | First failing row is mesh index `173`. |
| `200-219` | pass | Prior sampled middle-window pass. |
| `380-399` | pass | Prior sampled final-window pass. |

The batch was stopped after the first newly observed mismatch. Windows
`180-199` and `220-379` remain unrun in this full coverage pass because the next
debugging action should localize the first mismatch at row `173` before adding
more surface evidence.

## First Mismatch

| Field | Value |
| --- | --- |
| Mesh index | `173` |
| Theta | `[0.9710526315789474, 0.9842105263157894]` |
| Decision | `filterflow_float64_smoothness_gradient_full_surface_gradient_mismatch` |
| Scalar delta | `7.407919611068792e-09` |
| FilterFlow gradient diag | `[7019.871883303286, 713.5990730344417]` |
| BayesFilter gradient diag | `[7025.174609829531, 713.465296654367]` |
| Gradient delta | `[5.302726526244442, -0.133776380074778]` |
| Max absolute gradient delta | `5.302726526244442` |
| Max relative gradient delta | `0.0007553879350500595` |

## Interpretation

The scalar path remains aligned at the first failure, so the current discrepancy
is not a value/log-likelihood scalar mismatch. It is a gradient-only mismatch at
one full-grid theta point. Earlier bounded `mesh_size=4` evidence, row-window
passes, and sampled middle/final passes remain valid difference-audit evidence,
but full `mesh_size=20` surface agreement is not closed.

## Artifacts

- Plan:
  `docs/plans/bayesfilter-dpf-filterflow-float64-smoothness-gradient-full-surface-plan-2026-06-03.md`
- First failing window result:
  `docs/plans/bayesfilter-dpf-filterflow-float64-smoothness-gradient-full-surface-rows-160-179-result-2026-06-03.md`
- First failing window JSON:
  `experiments/dpf_implementation/reports/outputs/dpf_filterflow_float64_smoothness_gradient_full_surface_rows_160_179_2026-06-03.json`

## Non-Implications

- No correctness claim is made for either implementation.
- No analytic smoothness-gradient correctness is concluded.
- No posterior correctness is concluded.
- No production readiness is concluded.
- No HMC readiness is concluded.
- No monograph claim is concluded.

## Next Action

Create a row-173 per-time gradient localization runner/report. The runner should
keep the scalar contract fixed and compare cumulative/per-time gradient
contributions, resampling trigger locations, transport-gradient mode, and
transport diagnostics between BayesFilter and local float64 FilterFlow at
theta `[0.9710526315789474, 0.9842105263157894]`.
