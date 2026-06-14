# Plan: Row 173 Transport-Upstream Clipping Hypothesis Probe

## Scope

This is a BayesFilter-owned difference-audit diagnostic for the row-173
float64 BayesFilter/FilterFlow smoothness-gradient mismatch. It compares
BayesFilter TF/TFP against the local executable float64 FilterFlow reference.
It does not claim either implementation is mathematically correct.

Allowed write set:

- `docs/plans/bayesfilter-dpf-filterflow-float64-row-173-transport-upstream-clipping-*.md`
- `experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_row_173_vjp_decomposition_tf.py`
- `experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_row_173_transport_upstream_clipping_probe_tf.py`
- `experiments/dpf_implementation/reports/dpf-filterflow-float64-row-173-transport-upstream-clipping-2026-06-04.md`
- `experiments/dpf_implementation/reports/outputs/dpf_filterflow_float64_row_173_transport_upstream_clipping_2026-06-04.json`

Forbidden write set:

- production `bayesfilter/`
- `tests/`
- `docs/chapters/`
- `.localsource/filterflow`
- vendored/student/highdim/DSGE/NAWM lanes

## Current Evidence

The scalar-additivity route probe produced
`filterflow_float64_row_173_scalar_additivity_sum_route_residual`:

- scalar values match within `6.36e-9`;
- component scalar gradients match within `9.0e-5`;
- `post_update_mean` and `sum_pre_current_plus_increment_mean` retain the row
  residual `[5.3027344, -0.1337765]`;
- within each implementation, `grad(pre_current + increment)` is not equal to
  `grad(pre_current) + grad(increment)`, consistent with nonlinear custom
  transport-gradient clipping.

## Evidence Contract

Question:

Does the row-173 residual arise from the target-time transport custom-gradient
clipping route, from a cross-implementation upstream/clipping-mask difference,
or from graph/topology outside the target-time transport node?

Comparator:

The local executable float64 FilterFlow reference in `.localsource/filterflow`,
validated by the existing marker/fingerprint policy.

Primary diagnostic:

At target time 93, for scalar objectives `post_update_mean`,
`sum_pre_current_plus_increment_mean`, `pre_current_mean`, and
`increment_mean`, compare:

- raw upstream tensors into the target-time transport matrix;
- clipped upstream tensors after `clip_by_value(upstream, -1, 1)`;
- clipping masks and mask mismatches;
- target-time transport-node parameter VJPs under the raw upstream, relying on
  each implementation's custom transport-gradient rule;
- target-time transport-node parameter VJPs under manually clipped upstreams;
- within-side additivity gaps for raw upstreams, clipped upstreams, and
  target-time transport-node VJPs.

Hypothesis classifications:

- `h1_expected_clipping_nonlinearity`: raw upstreams are additive, clipped
  upstreams and target-time transport-node VJPs are non-additive within each
  implementation.
- `h2_cross_impl_clip_mask_or_upstream_mismatch`: BayesFilter and FilterFlow
  have materially different raw/clipped upstream tensors or clipping masks at
  the target-time transport node.
- `h3_transport_custom_vjp_rule_mismatch`: raw/clipped upstreams match, but
  target-time transport-node VJPs differ between implementations.
- `h4_residual_outside_target_transport_node`: target-time upstreams,
  clipping masks, and target-time transport-node VJPs match within tolerance,
  so the row residual must be explained by historical transport nodes,
  carryover graph topology, or another non-target transport route.
- `blocked_or_vetoed`: comparator drift, resampling mismatch, non-finite values,
  CPU-only violation, path-boundary violation, or missing instrumentation.

Veto diagnostics:

- comparator drift;
- resampling flag mismatch;
- scalar-value mismatch beyond `5e-8`;
- non-finite upstream/VJP tensors;
- CPU-only manifest violation;
- path-boundary contamination;
- missing local float64 FilterFlow executable reference.

Explanatory diagnostics:

- count and fraction of active clipped entries;
- max distance to clipping threshold;
- mask mismatch count;
- current target-time transport-node VJP contribution relative to the full
  observed row residual.

What must not be concluded:

- correctness of either implementation;
- analytic gradient correctness;
- global gradient agreement;
- full mesh/surface agreement;
- posterior correctness;
- production readiness;
- that target-time transport explains all residuals unless the VJP residual
  reconstruction actually shows it.

## Skeptical Pre-Execution Audit

- Wrong baseline risk: use only local executable float64 FilterFlow, not paper
  notation or pristine upstream.
- Proxy risk: finite upstreams/VJPs are smoke only; classification depends on
  fieldwise deltas and reconstruction diagnostics.
- Hidden assumption risk: target-time transport may not explain the residual;
  the plan includes `h4_residual_outside_target_transport_node`.
- Clipping nonlinearity risk: do not demand additivity after clipping; measure
  raw additivity and clipped non-additivity separately.
- Environment risk: force `CUDA_VISIBLE_DEVICES=-1` before TensorFlow import;
  ignore TensorFlow CUDA factory noise unless visible GPU devices are nonempty.
- Write-boundary risk: do not edit production code, tests, chapters, or
  `.localsource/filterflow`.
- Artifact-answer risk: the JSON must preserve raw upstreams, clipped
  upstreams, masks, target-time VJPs, and classification. Otherwise it does not
  answer the hypotheses.

The audit passes because the probe is narrow, difference-audit-only, preserves
the target-time versus historical-node distinction, and has explicit vetoes.

## Phase Order

1. Claude Code reviews this plan read-only.
2. Codex audits Claude findings as `ACCEPT`, `PARTIAL`, `DISPUTE`, or
   `CLARIFY` in the review-loop artifact.
3. If accepted, instrument the existing VJP helper with
   `transport_clipping_probe` and add a small comparison runner.
4. Run CPU-only targeted probe and validations.
5. Claude Code reviews the result read-only.
6. Codex audits Claude findings and patches only if materially required.

Claude command:

```bash
claude -p --model claude-opus-4-7 --effort max
```

Maximum review iterations: 5 for plan review and 5 for result review. On the
fifth iteration, accept only for user inspection unless a major blocker remains.

## Verification Commands

```bash
python -m py_compile \
  experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_row_173_vjp_decomposition_tf.py \
  experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_row_173_transport_upstream_clipping_probe_tf.py

CUDA_VISIBLE_DEVICES=-1 python -m \
  experiments.dpf_implementation.tf_tfp.runners.run_filterflow_float64_row_173_transport_upstream_clipping_probe_tf

CUDA_VISIBLE_DEVICES=-1 python -m \
  experiments.dpf_implementation.tf_tfp.runners.run_filterflow_float64_row_173_transport_upstream_clipping_probe_tf \
  --validate-only

python -m json.tool \
  experiments/dpf_implementation/reports/outputs/dpf_filterflow_float64_row_173_transport_upstream_clipping_2026-06-04.json

rg -n "import numpy|from numpy" \
  experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_row_173_vjp_decomposition_tf.py \
  experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_row_173_transport_upstream_clipping_probe_tf.py

rg -n "student|highdim|DSGE|NAWM|third_party|vendored" \
  experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_row_173_vjp_decomposition_tf.py \
  experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_row_173_transport_upstream_clipping_probe_tf.py \
  docs/plans/bayesfilter-dpf-filterflow-float64-row-173-transport-upstream-clipping-plan-2026-06-04.md

rg -n "[ \t]+$" \
  experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_row_173_vjp_decomposition_tf.py \
  experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_row_173_transport_upstream_clipping_probe_tf.py \
  docs/plans/bayesfilter-dpf-filterflow-float64-row-173-transport-upstream-clipping-plan-2026-06-04.md

git diff --check

git status --short -- \
  bayesfilter \
  tests \
  docs/chapters \
  .localsource/filterflow \
  third_party \
  experiments/controlled_dpf_baseline

git status --short --branch
```

## Stop Conditions

Stop and report blocker if:

- exact Claude command/model/effort is unavailable;
- local float64 FilterFlow executable reference cannot run;
- TensorFlow/TFP cannot run CPU-only;
- instrumentation requires editing `.localsource/filterflow` or production
  code;
- result validation fails in a way that invalidates the evidence;
- Claude/Codex disagreement persists after round 5 without human direction.
