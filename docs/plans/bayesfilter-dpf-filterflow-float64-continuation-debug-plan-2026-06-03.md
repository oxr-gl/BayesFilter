# Plan: Filterflow Float64 Continuation Debug

## Question

Continue the BayesFilter TF/TFP OT-DPF versus filterflow debugging comparison
using the local float64 filterflow reference branch only. The goal is to find
the first remaining cross-implementation discrepancy or blocker in the bounded
1D-to-R3 debugging ladder.

## Evidence Contract

- Comparator: `.localsource/filterflow` on branch
  `bayesfilter-py311-float64-reference`, commit
  `ff0048060fd4cff43dbea606d14275e40e2ac084`.
- BayesFilter path: experimental TF/TFP code under
  `experiments/dpf_implementation/tf_tfp/`.
- Primary criterion: BayesFilter and filterflow ledgers agree within the stated
  float64 comparison tolerances, with matching resampling triggers.
- Veto diagnostics: wrong filterflow branch/commit, filterflow source mutation,
  CPU-only invariant failure, non-finite scalar/ledger values, JSON/schema
  failure, protected-path drift.
- Explanatory-only diagnostics: AD-vs-FD gradient deltas, absolute transport
  residual quality when both implementations share the same residual, runtime,
  Monte Carlo table scale.
- Not concluded: mathematical correctness of either implementation, production
  readiness, posterior correctness, gradient correctness, general nonlinear SSM
  validity, DSGE/NAWM validity, monograph claims.
- Preserved artifact:
  `experiments/dpf_implementation/reports/outputs/dpf_filterflow_float64_continuation_debug_2026-06-03.json`.

## Inputs

- `AGENTS.md`
- `CLAUDE.md`
- `docs/plans/bayesfilter-dpf-filterflow-float64-branch-reference-result-2026-06-03.md`
- Existing 1D and R3 comparison runners under
  `experiments/dpf_implementation/tf_tfp/runners/`
- `.localsource/filterflow` float64 reference branch

## Outputs

- `experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_continuation_debug_tf.py`
- `experiments/dpf_implementation/reports/dpf-filterflow-float64-continuation-debug-2026-06-03.md`
- `experiments/dpf_implementation/reports/outputs/dpf_filterflow_float64_continuation_debug_2026-06-03.json`
- `docs/plans/bayesfilter-dpf-filterflow-float64-continuation-debug-result-2026-06-03.md`

## Allowed Write Set

- `docs/plans/bayesfilter-dpf-filterflow-float64-continuation-debug-*.md`
- `experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_continuation_debug_tf.py`
- `experiments/dpf_implementation/reports/dpf-filterflow-float64-continuation-debug-2026-06-03.md`
- `experiments/dpf_implementation/reports/outputs/dpf_filterflow_float64_continuation_debug_2026-06-03.json`

## Forbidden Write Set

- `bayesfilter/`
- `tests/`
- `docs/chapters/`
- high-dimensional nonlinear filtering lane artifacts
- vendored or student code
- `.localsource/filterflow` source

## Phase Order

1. Validate float64 filterflow branch/commit/marker and record clean status.
2. Run controlled scalar 1D T=2 and T=4 comparisons with filterflow and
   BayesFilter both forced to float64.
3. Run R1/R2 scalar smoothness-fixture comparisons against float64 filterflow.
4. Run or summarize a float64-aware R3 trace replay, requiring the external
   filterflow trace to reproduce official filterflow before comparing.
5. Record first mismatch or first blocker.
6. Validate and write JSON/report/result artifacts.

## Stop Conditions

- Stop immediately if the filterflow branch or commit is not the float64
  reference branch.
- Stop downstream rungs after the first direct mismatch unless the later rung is
  explicitly diagnostic-only.
- Mark R3 blocked if the non-mutating external trace cannot reproduce official
  filterflow.
- Do not mutate filterflow to obtain a trace.

## Skeptical Pre-Execution Audit

- Stale context: old float32 exact-arithmetic artifacts are historical only and
  cannot govern this run.
- Wrong reference hierarchy: the local float64 filterflow branch is the
  executable comparator; fixed-target Sinkhorn is not authoritative.
- Wrong covariance: executable `I_2` convention remains the reproduction
  setting.
- Unfair comparison: use CPU-only execution and force float64 on both sides.
- Proxy metric risk: transport residuals and AD-vs-FD are explanatory unless
  they differ across implementations.
- Hidden production drift: no production or test files are in the write set.
- Monograph/highdim/vendored drift: forbidden by write set and verified.
- Artifact relevance: a rung ledger with first mismatch/blocker directly
  answers the debugging question.

Audit result: pass after revising the plan to avoid reusing the old float32
continuation runner as evidence.

## Verification Commands

- `python -m py_compile experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_continuation_debug_tf.py`
- `CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_float64_continuation_debug_tf`
- `CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_float64_continuation_debug_tf --validate-only`
- JSON parse/schema check for the output artifact
- NumPy import gate over the touched runner
- import-boundary search for student/vendored/highdim/DSGE/NAWM imports
- lane-scoped trailing whitespace check
- `git diff --check`
- `git status --short -- bayesfilter tests docs/chapters`
- `git -C .localsource/filterflow status --short --branch`
- `git status --short --branch`

## Review Policy

No Claude review was requested for this continuation turn. The artifact follows
the repository skeptical-audit and evidence-contract policy.
