# Plan: FilterFlow Float64 Full 2D No-Replay Comparison

## Question

After the R4 trace replay passes, does BayesFilter still match the local
float64 FilterFlow reference when BayesFilter runs the same 2D constant-velocity
LGSSM loop without replaying FilterFlow proposal particles?

## Evidence Contract

- Comparator: `.localsource/filterflow` branch
  `bayesfilter-py311-float64-reference` at
  `1e5fbc288c1c11fc18ba01bb4842832e2088b800`.
- Baseline gate: an external eager trace loop must reproduce FilterFlow's
  official `pf(...)` state series before BayesFilter no-replay comparison is
  evidence.
- Primary criterion: BayesFilter no-replay loop agrees with the validated
  FilterFlow official series for particles, log weights, log likelihoods, and
  resampling flags within float64 audit tolerance.
- Localization diagnostics: compare BayesFilter sampled proposals to traced
  FilterFlow proposals, post-resampling state, likelihood components, and
  per-time deltas.
- Veto diagnostics: wrong reference commit, trace validation failure,
  non-finite values, CPU-only invariant failure, JSON/schema failure,
  protected-path drift, or comparator drift.
- Explanatory only: exact random-sample deltas, transport residuals, runtime,
  and gradient information.
- Not concluded: mathematical correctness, posterior correctness, gradient
  correctness, production readiness, paper authority, or full smoothness
  alignment.

## Allowed Write Set

- `experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_full_2d_no_replay_tf.py`
- `docs/plans/bayesfilter-dpf-filterflow-float64-full-2d-no-replay-plan-2026-06-03.md`
- `docs/plans/bayesfilter-dpf-filterflow-float64-full-2d-no-replay-result-2026-06-03.md`
- `experiments/dpf_implementation/reports/dpf-filterflow-float64-full-2d-no-replay-2026-06-03.md`
- `experiments/dpf_implementation/reports/outputs/dpf_filterflow_float64_full_2d_no_replay_2026-06-03.json`

## Forbidden Write Set

- `bayesfilter/`
- `tests/`
- `docs/chapters/`
- high-dimensional nonlinear filtering lane artifacts
- vendored/student code
- `.localsource/filterflow` source

## Skeptical Pre-Execution Audit

- Stale context risk: R4 trace replay already passed, so replaying FilterFlow
  proposal particles again would not answer the next question.
- Wrong baseline risk: compare against validated official FilterFlow `pf(...)`
  output, not an unvalidated hand loop.
- Randomness risk: use the same `samplers.split_seed(..., salt="update")`
  protocol, but do not force proposal samples. Proposal-particle deltas are
  localization diagnostics.
- Overclaim risk: a pass only clears this bounded full-loop setting; a failure
  localizes a cross-implementation difference, not correctness of either code.
- Hidden drift risk: keep edits under the allowed write set and verify protected
  paths.

Audit result: pass.

## Verification

- `python -m py_compile experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_full_2d_no_replay_tf.py`
- `CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_float64_full_2d_no_replay_tf`
- `CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_float64_full_2d_no_replay_tf --validate-only`
- JSON parse/content checks.
- NumPy import gate over the touched BayesFilter runner, allowing only external
  FilterFlow subprocess fixture strings.
- Import-boundary search for protected lanes.
- Lane-scoped trailing whitespace check.
- `git diff --check`.
- `git status --short -- bayesfilter tests docs/chapters`.
- `git -C .localsource/filterflow status --short --branch`.
- `git status --short --branch`.
