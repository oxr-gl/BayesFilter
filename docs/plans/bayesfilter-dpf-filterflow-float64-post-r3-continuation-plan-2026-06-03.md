# Plan: FilterFlow Float64 Post-R3 Continuation

## Question

After the local float64 FilterFlow optimal-proposal dtype fix, does the bounded
BayesFilter-vs-FilterFlow continuation ladder pass through the 2D R3/R4
trace-replay rung, and what is the next smallest comparison rung?

## Evidence Contract

- Comparator: `.localsource/filterflow` on
  `bayesfilter-py311-float64-reference` at
  `1e5fbc288c1c11fc18ba01bb4842832e2088b800`.
- Primary criterion for this step: the continuation ladder consumes the
  no-runtime-shim float64 R3 trace/replay result and reports no direct mismatch
  through R4.
- Veto diagnostics: wrong FilterFlow branch/commit, comparator drift, failed
  R3 trace validation, non-finite replay values, CPU-only invariant failure,
  JSON/schema failure, or protected path drift.
- Explanatory only: float64 roundoff deltas, gradient diagnostics embedded in
  older scalar rungs, and transport residual magnitudes.
- Not concluded: mathematical correctness, posterior correctness, gradient
  correctness, production readiness, paper authority, or full smoothness
  alignment.

## Allowed Write Set

- `experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_continuation_debug_tf.py`
- `docs/plans/bayesfilter-dpf-filterflow-float64-post-r3-continuation-plan-2026-06-03.md`
- `docs/plans/bayesfilter-dpf-filterflow-float64-post-r3-continuation-result-2026-06-03.md`
- Refreshed float64 continuation result/report/JSON artifacts.

## Forbidden Write Set

- `bayesfilter/`
- `tests/`
- `docs/chapters/`
- high-dimensional nonlinear filtering lane artifacts
- vendored/student code
- `.localsource/filterflow` source

## Skeptical Pre-Execution Audit

- Stale context risk: the existing continuation runner still audits the old
  float32 R3 helper, so it cannot answer the post-fix R4 question without a
  narrow harness update.
- Wrong comparator risk: enforce branch/commit/marker through the existing
  reference-policy helper.
- Overclaim risk: even a full pass through R4 is only a bounded replay pass; it
  does not prove same random-stream sampling or smoothness-surface gradients.
- Hidden drift risk: protected paths remain forbidden and are checked.
- Artifact relevance: refreshed continuation JSON/report records the first
  mismatch or first blocker after the cleaned R3 checkpoint.

Audit result: pass.

## Verification

- `python -m py_compile experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_continuation_debug_tf.py`
- `CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_float64_continuation_debug_tf`
- `CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_float64_continuation_debug_tf --validate-only`
- JSON parse/content check.
- NumPy import gate over the touched BayesFilter runner.
- Import-boundary search for protected lanes.
- Lane-scoped trailing whitespace check.
- `git diff --check`.
- `git status --short -- bayesfilter tests docs/chapters`.
- `git -C .localsource/filterflow status --short --branch`.
- `git status --short --branch`.
