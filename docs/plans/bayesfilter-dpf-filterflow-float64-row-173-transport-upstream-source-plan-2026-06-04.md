# Plan: Row 173 Transport-Upstream Source Probe

## Scope

This is a BayesFilter-owned difference-audit diagnostic for the row-173
float64 BayesFilter/FilterFlow smoothness-gradient mismatch. It follows the
historical-transport VJP result:

`filterflow_float64_row_173_historical_transport_h3_upstreams_or_masks_diverge`

The diagnostic compares BayesFilter TF/TFP against the local executable
float64 FilterFlow reference only. It does not claim either implementation is
mathematically correct.

Allowed write set:

- `docs/plans/bayesfilter-dpf-filterflow-float64-row-173-transport-upstream-source-*.md`
- `experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_row_173_transport_upstream_source_probe_tf.py`
- `experiments/dpf_implementation/reports/dpf-filterflow-float64-row-173-transport-upstream-source-2026-06-04.md`
- `experiments/dpf_implementation/reports/outputs/dpf_filterflow_float64_row_173_transport_upstream_source_2026-06-04.json`

Forbidden write set:

- production `bayesfilter/`
- `tests/`
- `docs/chapters/`
- `.localsource/filterflow`
- vendored/student/highdim/DSGE/NAWM lanes

## Current Evidence

The historical-transport VJP probe compared all transport nodes from time 0
through target time 93 and found:

- full gradient delta: `[5.302734403676368, -0.1337765252068337]`;
- cumulative historical transport VJP delta:
  `[-3.8733078526274767, 0.03330367154740088]`;
- reconstruction residual: `[9.176042256303845, -0.16708019675423458]`;
- first raw upstream elementwise delta above `2e-4`: time 43;
- first clipped upstream elementwise delta above `2e-4`: time 52;
- largest transport VJP delta: time 52;
- clip-mask mismatch count: `0`;
- resampling flags matched and scalar values matched.

Therefore the next question is not whether a single target-time transport VJP
rule explains the mismatch. The next question is where the adjoint entering the
transport boundary first becomes different.

## Evidence Contract

Question:

At times 43 and 52, is the BayesFilter-vs-FilterFlow transport-upstream
divergence explained by forward tensor drift at the transport boundary, or by
different downstream adjoint/topology after otherwise matching forward values?

Comparator:

The local executable float64 FilterFlow reference in `.localsource/filterflow`,
validated by the existing marker/fingerprint policy.

Target scalar:

Mean accumulated log likelihood at target time 93 for row 173:

- `T=100`;
- `N=50`;
- `data_seed=123`;
- `filter_seed=1234`;
- theta row 173:
  `[0.9710526315789474, 0.9842105263157894]`;
- epsilon `0.25`;
- scaling `0.85`;
- convergence threshold `1e-6`;
- max iterations `500`;
- resampling threshold `0.9999`;
- executable float64 FilterFlow observation path and initial particles.

Probe times:

- time 43: first raw transport-upstream elementwise delta above tolerance;
- time 52: first clipped transport-upstream delta above tolerance and largest
  transport VJP contribution.

Primary diagnostics:

For each probe time, compare BayesFilter and FilterFlow:

- forward pre-transport particles, log weights, ESS/log-ESS, resampling flags;
- transport matrix and transport residual summaries;
- post-transport particles and log weights;
- proposal mean, proposed particles, observation log likelihood, transition
  log likelihood, proposal log likelihood, unnormalized weights, increment,
  normalized log weights, and post-update log likelihoods;
- adjoints of the target scalar with respect to the same boundary and
  downstream tensors;
- transport upstream raw/clipped deltas and clip-mask mismatch counts;
- scalar target value and total transition-parameter gradient.

Hypothesis classifications:

- `h1_forward_boundary_drift`: forward values at or before the transport
  boundary differ above tolerance at the first divergent time.
- `h2_downstream_adjoint_topology_mismatch`: forward values at the transport
  boundary match, but adjoints at post-transport/downstream nodes differ above
  tolerance.
- `h3_proposal_update_adjoint_source`: the first large adjoint difference is
  localized to proposal/update nodes after the transport application.
- `h4_transport_boundary_only`: downstream adjoints match, but the raw upstream
  into the transport matrix differs at the transport boundary in a way not
  explained by recorded downstream nodes.
- `blocked_or_vetoed`: comparator drift, scalar mismatch, resampling mismatch,
  non-finite tensors, CPU-only violation, path-boundary violation, or missing
  instrumentation.

Veto diagnostics:

- comparator fingerprint drift;
- scalar-value mismatch beyond `5e-8`;
- resampling flag mismatch at the probe times;
- non-finite forward tensors or adjoints;
- CPU-only manifest violation;
- path-boundary contamination;
- missing local float64 FilterFlow executable reference.

Explanatory diagnostics:

- per-node forward max/sum deltas;
- per-node adjoint max/sum deltas;
- first node above tolerance among the recorded downstream nodes;
- transport matrix residuals and clip-mask mismatch counts;
- whether time 52 amplification is already visible at time 43.

What must not be concluded:

- correctness of either implementation;
- analytic gradient correctness;
- posterior correctness;
- global gradient agreement;
- full mesh/surface agreement;
- production readiness;
- that the mismatch is fixed;
- that FilterFlow is the mathematical truth beyond being the canonical
  executable reference for this audit lane.

## Skeptical Pre-Execution Audit

- Wrong baseline risk: use only the local executable float64 FilterFlow
  reference, not paper notation or pristine upstream.
- Proxy risk: finite tensors and matching scalar values are veto/smoke checks;
  localization depends on node-by-node forward and adjoint deltas.
- Hidden assumption risk: forward values may match while adjoints differ; the
  plan explicitly separates forward and adjoint evidence.
- Over-attribution risk: if multiple downstream nodes diverge at once, the
  result may localize a region, not a single line of code.
- Environment risk: force `CUDA_VISIBLE_DEVICES=-1` before TensorFlow import;
  ignore TensorFlow CUDA factory noise unless visible GPU devices are nonempty.
- Runtime risk: bound the run to one row, one target time, and two probe times.
- Write-boundary risk: do not edit production code, tests, chapters, or
  `.localsource/filterflow`.

The audit passes because the proposed artifact directly tests the next
smallest discriminating question raised by the accepted historical-transport
result: whether upstream divergence is caused by forward drift or downstream
adjoint topology.

## Phase Order

1. Claude Code reviews this plan read-only.
2. Codex audits Claude findings as `ACCEPT`, `PARTIAL`, `DISPUTE`, or
   `CLARIFY` in the review-loop artifact.
3. If accepted, implement the bounded source-localization runner.
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
  experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_row_173_transport_upstream_source_probe_tf.py

CUDA_VISIBLE_DEVICES=-1 python -m \
  experiments.dpf_implementation.tf_tfp.runners.run_filterflow_float64_row_173_transport_upstream_source_probe_tf

CUDA_VISIBLE_DEVICES=-1 python -m \
  experiments.dpf_implementation.tf_tfp.runners.run_filterflow_float64_row_173_transport_upstream_source_probe_tf \
  --validate-only

python -m json.tool \
  experiments/dpf_implementation/reports/outputs/dpf_filterflow_float64_row_173_transport_upstream_source_2026-06-04.json

rg -n "import numpy|from numpy" \
  experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_row_173_transport_upstream_source_probe_tf.py

rg -n "student|highdim|DSGE|NAWM|third_party|vendored" \
  experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_row_173_transport_upstream_source_probe_tf.py \
  docs/plans/bayesfilter-dpf-filterflow-float64-row-173-transport-upstream-source-plan-2026-06-04.md

rg -n "[ \t]+$" \
  experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_row_173_transport_upstream_source_probe_tf.py \
  docs/plans/bayesfilter-dpf-filterflow-float64-row-173-transport-upstream-source-plan-2026-06-04.md \
  docs/plans/bayesfilter-dpf-filterflow-float64-row-173-transport-upstream-source-result-2026-06-04.md \
  docs/plans/bayesfilter-dpf-filterflow-float64-row-173-transport-upstream-source-review-loop-2026-06-04.md

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
- the source-localization scan is too expensive for a bounded CPU run;
- Claude/Codex disagreement persists after round 5 without human direction.
