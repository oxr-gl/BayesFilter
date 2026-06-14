# Plan: R3 Float64 Trace Replay

## Question

Can BayesFilter TF/TFP match the local float64 filterflow executable reference
through the 2D R3 proposal/transport trace when proposal particles are traced
from filterflow?

## Evidence Contract

- Comparator: `.localsource/filterflow` on
  `bayesfilter-py311-float64-reference` at
  `ff0048060fd4cff43dbea606d14275e40e2ac084`.
- Baseline validity gate: a non-mutating eager trace loop must reproduce the
  official filterflow state-series output before BayesFilter replay is evidence.
- Primary criterion: BayesFilter replay agrees with the validated filterflow
  trace on particles, log weights, log likelihoods, trigger flags, transport,
  and likelihood components within float64 trace tolerances.
- Diagnostic replay modes:
  - computed resampling state;
  - traced resampling state;
  - traced input with computed resampling state;
  - traced input with traced transport matrix.
- Veto diagnostics: wrong filterflow branch/commit, trace validation failure,
  non-finite values, CPU-only invariant failure, JSON/schema failure, protected
  path drift.
- Explanatory only: runtime, absolute shared transport residual magnitude,
  AD/FD behavior outside this value trace.
- Not concluded: mathematical correctness, posterior correctness, gradient
  correctness, production readiness, general nonlinear SSM validity, DSGE/NAWM
  validity, monograph claims.

## Inputs

- Existing float64 filterflow branch reference artifacts.
- Existing float32 R3 runner as a template only.
- Filterflow source read-only: `smc.py`, `simple_linear_gaussian.py`,
  `optimal_proposal.py`, `regularized_transport/*`, `utils.py`.

## Outputs

- `experiments/dpf_implementation/tf_tfp/runners/run_filterflow_r3_float64_trace_replay_tf.py`
- `experiments/dpf_implementation/reports/dpf-filterflow-r3-float64-trace-replay-2026-06-03.md`
- `experiments/dpf_implementation/reports/outputs/dpf_filterflow_r3_float64_trace_replay_2026-06-03.json`
- `docs/plans/bayesfilter-dpf-filterflow-r3-float64-trace-replay-result-2026-06-03.md`

## Allowed Write Set

- The output paths above.

## Forbidden Write Set

- `bayesfilter/`
- `tests/`
- `docs/chapters/`
- high-dimensional nonlinear filtering lane artifacts
- vendored or student code
- `.localsource/filterflow` source

## Skeptical Pre-Execution Audit

- Stale context: the old R3 helper is float32-specific and cannot provide
  float64-lane evidence.
- Wrong comparator risk: enforce branch/commit/marker before running.
- Wrong arithmetic risk: use a single float64 dtype in the new trace and replay
  code; do not reuse float32 casts.
- Trace validity risk: BayesFilter comparison is blocked unless the external
  eager trace reproduces official filterflow first.
- Stop-condition risk: report the first replay mode that passes or localizes the
  mismatch; do not continue to broader claims.
- Hidden drift risk: write set excludes production, tests, monograph, highdim,
  vendored/student, and filterflow source.
- Artifact relevance: the output answers the previous blocker directly.

Audit result: pass.

## Verification

- `python -m py_compile experiments/dpf_implementation/tf_tfp/runners/run_filterflow_r3_float64_trace_replay_tf.py`
- `CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_r3_float64_trace_replay_tf`
- `CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_r3_float64_trace_replay_tf --validate-only`
- JSON parse/schema check
- NumPy import gate over touched BayesFilter runner, allowing only subprocess
  fixture code strings
- import-boundary check for student/vendored/highdim/DSGE/NAWM imports
- lane-scoped trailing whitespace check
- `git diff --check`
- `git status --short -- bayesfilter tests docs/chapters`
- `git -C .localsource/filterflow status --short --branch`
- `git status --short --branch`
