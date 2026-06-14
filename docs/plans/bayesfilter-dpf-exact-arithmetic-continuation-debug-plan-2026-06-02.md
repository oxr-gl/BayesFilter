# BayesFilter DPF Exact-Arithmetic Continuation Debug Plan

## Evidence Contract

Question: after the R1 filterflow-exact arithmetic fix, where is the next BayesFilter/filterflow discrepancy in the scalar 1D-to-smoothness debugging ladder?

Comparator: the current local executable `.localsource/filterflow` checkout, treated as the canonical executable reference for this audit lane.

Primary criterion: exact-arithmetic BayesFilter must match filterflow on scalar, trigger flags, per-step ledger fields, and row/column residual deltas for every evidence-bearing rung whose inputs can be explicitly replayed.

Veto diagnostics: filterflow subprocess blocker, comparator drift, non-finite scalar/weights/transport, trigger mismatch, scalar mismatch, field mismatch, residual-delta mismatch, or a rung whose required filterflow random stream is not explicitly replayable.

Explanatory diagnostics: BF64 contrast is not rerun here; residual quality is diagnostic only when shared; gradients are smoke diagnostics unless scalar contract and random streams are aligned.

Not concluded: correctness of either implementation, production readiness, posterior correctness, HMC readiness, smoothness-surface gradient correctness, nonlinear-SSM validity, monograph claim, or tolerance-policy change.

Artifact: `docs/plans/bayesfilter-dpf-exact-arithmetic-continuation-debug-result-2026-06-02.md` and `experiments/dpf_implementation/reports/outputs/dpf_exact_arithmetic_continuation_debug_2026-06-02.json`.

## Rungs

1. R1: filterflow observation path with fixed controlled initial particles and controlled transition noises.
2. R2: same as R1, but initial particles switch to the filterflow fixture draw.
3. R3: transition proposal random stream. This rung is expected to block unless exact per-time proposal draws are available without mutating filterflow source.
4. R4-R8: blocked after the first mismatch or blocker.

## Skeptical Pre-Execution Audit

Wrong baseline risk: comparator is local executable filterflow only, not paper truth or student code.

Wrong arithmetic risk: BayesFilter must use the `filterflow_exact_float32` path from the R1 fix, not the old BF64 path.

Proxy metric risk: shared residual magnitude is not a discrepancy unless residual deltas differ.

Hidden assumption: changing to exact arithmetic is an audit-lane reproduction convention, not a production default.

Stop condition: stop downstream rungs after the first direct mismatch, blocker, comparator drift, or unreplayable filterflow random stream.

Artifact adequacy: the JSON stores every evidence-bearing cell plus the first failing or blocked cell, which answers the debugging question.

## Verification

- `python -m py_compile` for touched Python files.
- CPU-only exact-arithmetic continuation runner.
- CPU-only validate-only rerun.
- JSON parse/schema check.
- NumPy import gate over touched BayesFilter TF/TFP files.
- Import-boundary check for student/vendored/highdim/DSGE/NAWM references.
- Lane-scoped trailing whitespace check.
- `git diff --check`.
- `git status --short -- bayesfilter tests docs/chapters`.
- `git status --short --branch`.
