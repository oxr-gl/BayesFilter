# BayesFilter DPF R1 Filterflow-Exact Arithmetic Plan

## Evidence Contract

Question: when BayesFilter uses the same arithmetic convention as the local executable filterflow reference, does the R1 1D LGSSM comparison still diverge?

Comparator: the current local executable `.localsource/filterflow` checkout, run through the existing CPU-only subprocess harness.

Primary criterion: the BayesFilter experimental `tf.float32` filterflow-style path matches filterflow on scalar, trigger flags, and per-step ledger fields for the matched control, the first failing R1 prefix `T=4`, and the full R1 `T=100` case within the existing filterflow-agreement tolerances.

Veto diagnostics: filterflow subprocess blocker, comparator drift, non-finite scalar/weights/transport, trigger mismatch, scalar mismatch, or field mismatch after exact arithmetic.

Explanatory diagnostics: BF64-vs-filterflow deltas, BF32-vs-filterflow deltas, first failing time/fields, transport residual deltas, and source-arithmetic audit tokens.

Not concluded: mathematical correctness of filterflow, mathematical correctness of BayesFilter, production readiness, posterior correctness, HMC readiness, nonlinear-SSM validity, monograph claims, or a default production dtype policy.

Artifact: `docs/plans/bayesfilter-dpf-r1-filterflow-exact-arithmetic-result-2026-06-02.md` and `experiments/dpf_implementation/reports/outputs/dpf_filterflow_r1_filterflow_exact_arithmetic_2026-06-02.json`.

## Scope

Allowed writes:
- `experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py`
- `experiments/dpf_implementation/tf_tfp/runners/run_filterflow_1d_lgssm_step_gradient_comparison_tf.py`
- `experiments/dpf_implementation/tf_tfp/runners/run_filterflow_r1_filterflow_exact_arithmetic_tf.py`
- `experiments/dpf_implementation/reports/`
- `docs/plans/bayesfilter-dpf-r1-filterflow-exact-arithmetic-*.md`

Forbidden writes:
- production `bayesfilter/`
- `tests/`
- `docs/chapters/`
- high-dimensional nonlinear filtering lane artifacts
- vendored student code
- `.localsource/filterflow`
- DSGE/NAWM artifacts

## Arithmetic Controls

The experimental exact-arithmetic path must:
- use `tf.float32` for the filterflow-exact comparison path;
- use the filterflow squared-distance formula `xx - 2 xy + yy`, clipped at zero, rather than pairwise-difference squaring;
- use filterflow-style diameter scaling and `max_min` epsilon-start arithmetic;
- preserve ESS-triggered transport semantics;
- keep fixed-target Sinkhorn out of this comparison.

## Skeptical Pre-Execution Audit

Stale context: the previous micro-audit localized the first R1 failure to time-3 observation log-probability arithmetic under the R1 observation path. This plan directly tests that localized issue.

Wrong baseline: comparator remains local executable filterflow, not the paper, not student code, and not mathematical truth.

Proxy metric risk: absolute transport residual quality is diagnostic only unless it differs across implementations; the primary question is cross-implementation agreement.

Hidden assumption: `tf.float32` arithmetic is a reproduction convention for this audit lane, not a production default.

Stop conditions: stop and report blocker if filterflow cannot run, if comparator fingerprint drifts, if exact arithmetic still mismatches, or if verification detects forbidden writes/imports.

Artifact adequacy: the JSON stores per-case scalar/field deltas and first failures, which answers whether exact arithmetic removes the observed R1 discrepancy.

## Verification

- `python -m py_compile` on touched Python files.
- CPU-only targeted runner.
- CPU-only validate-only rerun.
- JSON parse/schema check.
- NumPy import gate over touched BayesFilter TF/TFP files.
- Import-boundary check for student/vendored/highdim/DSGE/NAWM references.
- Lane-scoped trailing whitespace check.
- `git diff --check`.
- `git status --short -- bayesfilter tests docs/chapters`.
- `git status --short --branch`.
