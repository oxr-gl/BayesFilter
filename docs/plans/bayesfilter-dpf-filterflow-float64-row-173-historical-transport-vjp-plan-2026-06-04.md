# Plan: Row 173 Historical Transport VJP Hypothesis Probe

## Scope

This is a BayesFilter-owned difference-audit diagnostic for the row-173
float64 BayesFilter/FilterFlow smoothness-gradient mismatch. It compares
BayesFilter TF/TFP against the local executable float64 FilterFlow reference.
It does not claim either implementation is mathematically correct.

Allowed write set:

- `docs/plans/bayesfilter-dpf-filterflow-float64-row-173-historical-transport-vjp-*.md`
- `experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_row_173_historical_transport_vjp_probe_tf.py`
- narrowly scoped instrumentation in
  `experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_row_173_vjp_decomposition_tf.py`
- `experiments/dpf_implementation/reports/dpf-filterflow-float64-row-173-historical-transport-vjp-2026-06-04.md`
- `experiments/dpf_implementation/reports/outputs/dpf_filterflow_float64_row_173_historical_transport_vjp_2026-06-04.json`

Forbidden write set:

- production `bayesfilter/`
- `tests/`
- `docs/chapters/`
- `.localsource/filterflow`
- vendored/student/highdim/DSGE/NAWM lanes

## Current Evidence

The row-173 target-time transport-upstream clipping probe classified
`h3_transport_custom_vjp_rule_mismatch`:

- raw target-time transport upstream max delta: `3.36e-08`;
- clipped target-time transport upstream max delta: `1.75e-08`;
- target-time clip-mask delta: `0.0`;
- target-time transport VJP max delta: `8.78e-04`;
- full scalar-gradient row residual remains `[5.3027344, -0.1337765]`.

Therefore the target-time transport node has a real VJP mismatch, but it is too
small by itself to explain the full residual.

## Evidence Contract

Question:

Do accumulated historical transport-node VJP deltas reconstruct the row-173
BayesFilter-vs-FilterFlow scalar-gradient residual, or does a substantial
residual remain outside the transport-node VJP sum?

Comparator:

The local executable float64 FilterFlow reference in `.localsource/filterflow`,
validated by the existing marker/fingerprint policy.

Primary diagnostic:

For target time 93 and scalar objective `post_update_mean`, collect every
transport matrix node from time 0 through target time 93 and compare:

- raw upstream tensor `d target / d transport_matrix_t`;
- clipped upstream tensor after the implementation's `[-1, 1]` transport
  backward convention;
- clip masks and mask counts;
- per-time transport-node VJP to the transition parameter;
- cumulative per-time VJP sums;
- cumulative BayesFilter-minus-FilterFlow VJP delta;
- reconstruction residual:
  `full_scalar_gradient_delta - cumulative_transport_vjp_delta`.

Hypothesis classifications:

- `h1_accumulated_transport_vjp_reconstructs_residual`: historical transport
  VJP deltas reconstruct the full row residual within tolerance.
- `h2_historical_transport_vjp_partially_explains_residual`: accumulated
  historical transport VJP deltas materially reduce the residual but leave a
  nontrivial remainder.
- `h3_transport_upstreams_or_masks_diverge_historically`: upstream or clip-mask
  deltas exceed tolerance at some historical transport node, so transport VJP
  differences are not solely rule/Jacobian differences.
- `h4_residual_outside_transport_nodes`: historical transport-node VJP deltas
  are small relative to the full residual, so carryover/state/proposal/topology
  outside transport nodes remains the leading explanation.
- `blocked_or_vetoed`: comparator drift, resampling mismatch, non-finite
  tensors, CPU-only violation, path-boundary violation, or missing
  instrumentation.

Veto diagnostics:

- comparator drift;
- resampling flag mismatch at any recorded time;
- scalar-value mismatch beyond `5e-8`;
- non-finite upstream/VJP tensors;
- CPU-only manifest violation;
- path-boundary contamination;
- missing local float64 FilterFlow executable reference.

Explanatory diagnostics:

- top per-time VJP deltas by magnitude;
- cumulative VJP-delta trajectory;
- per-time clip-count and clip-mask mismatch counts;
- current target-time contribution versus the full cumulative contribution;
- residual norm before and after subtracting accumulated transport VJP deltas.

What must not be concluded:

- correctness of either implementation;
- analytic gradient correctness;
- posterior correctness;
- global gradient agreement;
- full mesh/surface agreement;
- production readiness;
- that historical transport explains the full residual unless the explicit
  reconstruction residual is within tolerance.

## Skeptical Pre-Execution Audit

- Wrong baseline risk: use only local executable float64 FilterFlow, not paper
  notation or pristine upstream.
- Proxy risk: finite per-time VJPs are smoke only; the primary criterion is
  reconstruction of the observed scalar-gradient residual.
- Hidden assumption risk: transport-node VJP deltas may only partially explain
  the row residual; the plan requires an explicit residual remainder.
- Attribution risk: if upstreams or masks diverge historically, do not label
  the issue as a pure VJP-rule mismatch.
- Environment risk: force `CUDA_VISIBLE_DEVICES=-1` before TensorFlow import;
  ignore TensorFlow CUDA factory noise unless visible GPU devices are nonempty.
- Runtime risk: the probe is bounded to one mesh row, one target time, and
  94 historical transport nodes; no full-surface or multi-row sweep.
- Write-boundary risk: do not edit production code, tests, chapters, or
  `.localsource/filterflow`.

The audit passes because the proposed probe directly tests the current leading
hypothesis, preserves the target-time versus historical-node distinction, and
has explicit stop conditions and non-implication controls.

## Phase Order

1. Claude Code reviews this plan read-only.
2. Codex audits Claude findings as `ACCEPT`, `PARTIAL`, `DISPUTE`, or
   `CLARIFY` in the review-loop artifact.
3. If accepted, implement a bounded historical transport VJP probe.
4. Run CPU-only targeted probe and validations.
5. Claude Code reviews the result read-only.
6. Codex audits Claude findings and patches only if materially required.

Claude command:

```bash
claude -p --model claude-opus-4-7 --effort max
```

Maximum review iterations: 5 for plan review and 5 for result review. On the
fifth iteration, accept only for user inspection unless a major blocker remains.

## Codex-Supervisor Audit Protocol

Before execution proceeds, the review-loop artifact must record one Codex
classification for every Claude finding:

- `ACCEPT`: materially correct; patch required.
- `PARTIAL`: directionally correct, but the patch must be narrower or
  different.
- `DISPUTE`: incorrect, over-scoped, inconsistent with governance, or would
  weaken the evidence contract.
- `CLARIFY`: cannot evaluate without more evidence or human direction.

If Codex classifies a finding as `ACCEPT` or `PARTIAL`, Codex must patch the
plan/result or implementation and record the exact control added in the
review-loop artifact before resubmitting to Claude.

If Codex classifies a finding as `DISPUTE`, Codex must write a concise rebuttal
with file/section evidence in the review-loop artifact and include the rebuttal
in the next Claude prompt, asking Claude to withdraw, revise, or explain why
the rebuttal is wrong.

Codex must not silently ignore any Claude finding, and Claude `ACCEPT` is not
sufficient by itself: Codex must independently agree that the current artifact
enforces the required governance controls before allowing execution.

Execution is blocked until either:

- Claude returns `ACCEPT` and Codex records an independent `ACCEPT`; or
- round 5 is reached and no major blocker remains, in which case the result is
  accepted only for user inspection.

## Verification Commands

```bash
python -m py_compile \
  experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_row_173_vjp_decomposition_tf.py \
  experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_row_173_historical_transport_vjp_probe_tf.py

CUDA_VISIBLE_DEVICES=-1 python -m \
  experiments.dpf_implementation.tf_tfp.runners.run_filterflow_float64_row_173_historical_transport_vjp_probe_tf

CUDA_VISIBLE_DEVICES=-1 python -m \
  experiments.dpf_implementation.tf_tfp.runners.run_filterflow_float64_row_173_historical_transport_vjp_probe_tf \
  --validate-only

python -m json.tool \
  experiments/dpf_implementation/reports/outputs/dpf_filterflow_float64_row_173_historical_transport_vjp_2026-06-04.json

rg -n "import numpy|from numpy" \
  experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_row_173_vjp_decomposition_tf.py \
  experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_row_173_historical_transport_vjp_probe_tf.py

rg -n "student|highdim|DSGE|NAWM|third_party|vendored" \
  experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_row_173_vjp_decomposition_tf.py \
  experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_row_173_historical_transport_vjp_probe_tf.py \
  docs/plans/bayesfilter-dpf-filterflow-float64-row-173-historical-transport-vjp-plan-2026-06-04.md

rg -n "[ \t]+$" \
  experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_row_173_vjp_decomposition_tf.py \
  experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_row_173_historical_transport_vjp_probe_tf.py \
  docs/plans/bayesfilter-dpf-filterflow-float64-row-173-historical-transport-vjp-plan-2026-06-04.md

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
- all-history VJP scan is too expensive for a bounded CPU run;
- Claude/Codex disagreement persists after round 5 without human direction.
