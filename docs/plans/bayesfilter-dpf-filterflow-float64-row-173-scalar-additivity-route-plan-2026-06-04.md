# Plan: Row 173 Scalar-Additivity Route Probe

## Scope

This is a BayesFilter-owned difference-audit diagnostic for the local float64
FilterFlow reference and the BayesFilter TF/TFP replay. It does not assert that
either implementation is mathematically correct.

## Evidence Contract

- Question: for row 173 at target time 93, do direct scalar gradients for
  `post_update_log_likelihoods`, `pre_current_log_likelihoods + increment`,
  `pre_current_log_likelihoods`, and `increment` agree between BayesFilter and
  the local float64 FilterFlow reference?
- Comparator: `.localsource/filterflow` on the canonical local float64
  reference branch, identified by the existing fingerprint/marker policy.
- Primary criterion: compare BayesFilter gradient vectors against FilterFlow
  transition-matrix diagonal gradients for the four scalar objectives.
- Veto diagnostics: comparator drift, resampling-flag mismatch, non-finite
  scalar gradients, scalar-value mismatch beyond the existing value tolerance,
  CPU-only policy failure, or path-boundary contamination.
- Explanatory diagnostics: within-implementation additivity gaps and
  consistency between `post_update_mean` and the already-recorded total
  gradient.
- Not concluded: correctness of either implementation, global smoothness
  agreement, production readiness, posterior correctness, or analytic-gradient
  correctness.
- Artifact: JSON under `experiments/dpf_implementation/reports/outputs/` and
  mirrored Markdown result under `docs/plans/`.

## Skeptical Pre-Execution Audit

- Wrong baseline: use only the local float64 FilterFlow reference, not paper
  notation or pristine upstream.
- Proxy metric risk: finite gradients are smoke only; the comparison is the
  direct scalar-gradient delta by field.
- Hidden assumption: direct scalar additivity may hold while intermediate VJP
  row additivity fails; record both instead of collapsing the distinction.
- Environment mismatch: force `CUDA_VISIBLE_DEVICES=-1` before TensorFlow
  import; use the existing FilterFlow subprocess environment.
- Stop conditions: stop on comparator drift, missing FilterFlow env, non-finite
  gradients, resampling mismatch, or path-boundary contamination.
- Write boundary: only write this plan/result, one runner, one report, and one
  JSON output. Do not edit production `bayesfilter/`, tests, chapters, or
  `.localsource/filterflow`.

The audit passes because the proposed runner reuses the already instrumented
VJP helper, narrows the output to direct scalar-gradient route evidence, and
does not change implementation semantics.

## Commands

```bash
python -m py_compile \
  experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_row_173_vjp_decomposition_tf.py \
  experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_row_173_scalar_additivity_route_tf.py

CUDA_VISIBLE_DEVICES=-1 python -m \
  experiments.dpf_implementation.tf_tfp.runners.run_filterflow_float64_row_173_scalar_additivity_route_tf

CUDA_VISIBLE_DEVICES=-1 python -m \
  experiments.dpf_implementation.tf_tfp.runners.run_filterflow_float64_row_173_scalar_additivity_route_tf \
  --validate-only
```
