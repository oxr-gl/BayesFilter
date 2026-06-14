# Result: FilterFlow Float64 Full 2D No-Replay Comparison

## Decision

`filterflow_float64_full_2d_no_replay_pass`

## Evidence

- Comparator: local float64 FilterFlow reference commit
  `1e5fbc288c1c11fc18ba01bb4842832e2088b800`.
- Trace gate: the external eager loop reproduced official FilterFlow `pf(...)`
  output before BayesFilter comparison.
- Trace-gate deltas:
  particles `0.0`, log weights `0.0`, log likelihoods
  `9.947598300641403e-14`.
- BayesFilter no-replay full 2D series deltas:
  particles `8.506845006195363e-09`, log weights
  `1.8203278884243446e-08`, log likelihoods
  `6.673630537079589e-09`.
- First failure: none observed.
- Time-0 proposal-particle delta: `0.0`.
- Runtime shims: none.

## Interpretation

The random stream/full-SMC execution axis is cleared for this bounded 2D
constant-velocity float64 setting. BayesFilter matches the local executable
FilterFlow reference without replaying proposal particles, and the tiny deltas
are below the existing float64 audit tolerance.

The next useful debugging axis is the actual smoothness/gradient surface:
compare the scalar used by FilterFlow `simple_linear_smoothness.py` against a
BayesFilter TF/TFP scalar over the same theta grid and seeds, now using the
cleaned float64 reference. Value agreement should be checked before promoting
any GradientTape comparison.

## Artifacts

- Plan:
  `docs/plans/bayesfilter-dpf-filterflow-float64-full-2d-no-replay-plan-2026-06-03.md`
- Runner:
  `experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_full_2d_no_replay_tf.py`
- Report:
  `experiments/dpf_implementation/reports/dpf-filterflow-float64-full-2d-no-replay-2026-06-03.md`
- JSON:
  `experiments/dpf_implementation/reports/outputs/dpf_filterflow_float64_full_2d_no_replay_2026-06-03.json`

## Non-Implications

- No mathematical correctness claim.
- No posterior correctness claim.
- No gradient correctness claim.
- No production BayesFilter claim.
- No paper-authority claim.
- No full smoothness-surface alignment claim.
