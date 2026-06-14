# Result: FilterFlow Float64 Row Gradient Discrepancy Localization

## Decision

`filterflow_float64_clipped_gradient_residual_not_closed`

## Evidence Contract

This is a BayesFilter-vs-local-FilterFlow difference audit only. The comparator
is the local float64 FilterFlow branch `bayesfilter-py311-float64-reference`.
The question is whether BayesFilter TF/TFP matches that executable reference on
the failing smoothness rows. No correctness claim is made for either
implementation.

## Row Summary

| Mesh row | Theta | Scalar delta | Raw final gradient delta | Clipped/default final gradient delta | Status |
| --- | --- | --- | --- | --- | --- |
| `173` | `[0.9710526315789474, 0.9842105263157894]` | `7.407919611068792e-09` | `[1.3515114431922745e+218, -1.1290717972775883e+218]` | `[5.302725651367837, -0.13377635800236476]` | clipped/default still outside tolerance |
| `244` | `[0.981578947368421, 0.9605263157894737]` | `1.262566229343065e-08` | `[3.5292220582944188e+221, -3.0311612499507055e+221]` | `[0.4181310430146823, -0.005394760596573178]` | clipped/default still outside tolerance |

## Interpretation

The scalar/value path remains aligned on both localized rows. The raw
BayesFilter gradient through the transport solve is explosively different from
FilterFlow, and FilterFlow-style upstream clipping is the best ablation. But the
clipped/default path does not fully match FilterFlow: row `173` still differs by
about `5.3` in the first diagonal gradient component, and row `244` still
differs by about `0.42`.

That means the remaining issue is not just float64 versus float32, not seed
drift, and not the raw transport-gradient explosion alone. The next debugging
target is the clipped/default gradient residual at the first resampling step
(`time_index=1`), with per-term VJP diagnostics for the resampled particles,
transport matrix, optimal proposal mean, transition log probability, proposal
log probability, and normalized weights.

## Artifacts

- Row `173` result:
  `docs/plans/bayesfilter-dpf-filterflow-float64-row-173-gradient-localization-result-2026-06-03.md`
- Row `173` JSON:
  `experiments/dpf_implementation/reports/outputs/dpf_filterflow_float64_row_173_gradient_localization_2026-06-03.json`
- Row `244` result:
  `docs/plans/bayesfilter-dpf-filterflow-float64-row-244-gradient-localization-result-2026-06-03.md`
- Row `244` JSON:
  `experiments/dpf_implementation/reports/outputs/dpf_filterflow_float64_row_244_gradient_localization_2026-06-03.json`
- Parameterized runner:
  `experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_smoothness_gradient_localization_tf.py`

## Verification

- `python -m py_compile experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_smoothness_gradient_localization_tf.py`
- `CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_float64_smoothness_gradient_localization_tf --theta 0.9710526315789474 0.9842105263157894 --tag row-173 --mesh-index 173`
- `CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_float64_smoothness_gradient_localization_tf --theta 0.981578947368421 0.9605263157894737 --tag row-244 --mesh-index 244`
- Validate-only reruns passed for both row artifacts.
- NumPy import gate over the touched BayesFilter runner found no direct NumPy
  import.
- Import-boundary search found no student, controlled-DPF, highdim, DSGE, or
  NAWM imports in the touched runner.

## Non-Implications

- No mathematical correctness claim is made for BayesFilter or FilterFlow.
- No analytic gradient correctness is concluded.
- No posterior correctness is concluded.
- No production readiness is concluded.
- No public API readiness is concluded.
- No HMC readiness is concluded.
- No monograph claim is concluded.

## Next Action

Build a first-resampling-step clipped/default VJP decomposition for row `173`.
Start at `time_index=1`, because both localized rows first fail there while the
scalar path is still aligned. The decomposition should compare the local
FilterFlow gradient contribution and the BayesFilter contribution term by term,
instead of only comparing the final accumulated gradient.
