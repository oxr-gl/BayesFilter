# Plan: Row 173 Direct-Theta Hypothesis Test

## Decision

`planned_pending_claude_review`

## Scope

This is a BayesFilter-owned experimental DPF difference audit. It compares
BayesFilter TF/TFP replay against the local float64 FilterFlow executable
reference for smoothness row `173`, time `93`, theta
`[0.9710526315789474, 0.9842105263157894]`.

Allowed write set:

- `experiments/dpf_implementation/tf_tfp/`
- `experiments/dpf_implementation/reports/`
- `docs/plans/`

Forbidden write set:

- `bayesfilter/`
- `tests/`
- `docs/chapters/`
- `.localsource/filterflow/`
- vendored student code
- high-dimensional nonlinear filtering lane artifacts
- DSGE/NAWM-specific implementations or tests

## Evidence Contract

Question: Which direct current-step theta derivative mechanism explains the
remaining row-173/time-93 BayesFilter-vs-FilterFlow gradient mismatch?

Comparator: local float64 FilterFlow branch, executed as a read-only subprocess.
This local checkout is the canonical executable reference for this audit lane.

Primary criterion: the new probe must identify whether one of the four stated
hypotheses reproduces the observed direct-theta gradient delta
`[5.302734403676368, -0.1337765252068337]` after the post-resampling state is
held fixed, or must report that none of the four explains the mismatch.

Veto diagnostics:

- FilterFlow subprocess cannot run.
- BayesFilter TF/TFP path cannot run CPU-only.
- Values of frozen post-resampling state, proposed particles, term tensors, or
  scalar increment disagree beyond the existing value tolerance before gradient
  interpretation.
- Any direct-gradient tensor is non-finite.
- The probe writes outside the allowed lane.
- The result cannot be parsed as JSON or validated.

Explanatory-only diagnostics:

- Per-term gradient magnitudes.
- Full-matrix off-diagonal gradients.
- Proposal-sample path VJPs.
- Individual particle contribution summaries.
- Scalar/log-likelihood agreement once it has passed the value gate.

Non-conclusions:

- No claim that either implementation is mathematically correct.
- No production readiness, public API readiness, posterior correctness, HMC
  readiness, DSGE/NAWM validation, banking/model-risk claim, or monograph claim.
- No claim that finite gradients establish gradient correctness.
- No mutation of FilterFlow source and no claim about pristine upstream
  FilterFlow.

## Hypotheses To Test

H1. Direct current-step term algebra mismatch:
`transition_ll + observation_ll - proposal_ll` has one term whose direct theta
VJP differs under matched frozen state and matched upstream weights.

H2. Optimal-proposal cancellation/topology mismatch:
FilterFlow's fresh proposal-log-probability topology changes cancellation
between transition, observation, proposal, and proposal-sample branches in a way
not captured by the BayesFilter replay.

H3. Parameter embedding mismatch:
FilterFlow differentiates a full `2x2` transition matrix and then takes the
diagonal, while BayesFilter differentiates a length-2 theta vector used to build
a diagonal-plus-superdiagonal matrix. The embedding may change direct AD paths
or watched variables.

H4. Current-step direct derivative is not the source:
when the post-resampling state and current random draw are frozen, the
current-step direct gradients match; the remaining mismatch must be in a
different boundary than the current-step term derivative despite earlier
localization.

## Planned Probe

Create:

- `experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_row_173_direct_theta_hypothesis_tf.py`
- `docs/plans/bayesfilter-dpf-filterflow-float64-row-173-direct-theta-hypothesis-result-2026-06-04.md`
- `experiments/dpf_implementation/reports/dpf-filterflow-float64-row-173-direct-theta-hypothesis-2026-06-04.md`
- `experiments/dpf_implementation/reports/outputs/dpf_filterflow_float64_row_173_direct_theta_hypothesis_2026-06-04.json`
- `docs/plans/bayesfilter-dpf-filterflow-float64-row-173-direct-theta-hypothesis-review-loop-2026-06-04.md`

The runner will:

1. Execute local float64 FilterFlow in a subprocess with `CUDA_VISIBLE_DEVICES=-1`.
2. Reproduce row `173`, time `93`, `T=100`, `N=50`, data seed `123`, filter seed
   `1234`, epsilon `0.25`, scaling `0.85`, max iterations `500`, and
   `Neff=0.9999`.
3. Capture the time-93 post-resampling state, observation, proposed particles,
   log weights, and term tensors.
4. Recompute direct current-step terms with post-resampling particles and
   proposed particles held fixed as values.
5. Compare FilterFlow and BayesFilter direct gradients for:
   - `transition_ll`;
   - `observation_ll`;
   - fresh `proposal_ll`;
   - `transition_ll + observation_ll - proposal_ll`;
   - `reduce_logsumexp(term + post_log_weights)`;
   - sample-path active versus sample-path stopped controls.
6. Run each BayesFilter direct-gradient probe in two parameterizations:
   - length-2 theta variable;
   - full `2x2` transition matrix variable with diagonal entries set to theta
     and superdiagonal fixed to one.

## Skeptical Pre-Execution Audit

- Stale context: use the current row-173 summary and current VJP JSON as inputs,
  then regenerate the FilterFlow tensors in the new subprocess.
- Wrong baseline: comparator is local float64 FilterFlow only; do not compare to
  paper notation or pristine upstream.
- Proxy metric risk: scalar agreement and finite gradients are gates only; they
  do not establish correctness.
- Missing stop conditions: stop on subprocess failure, value mismatch, nonfinite
  gradients, lane contamination, Claude/Codex unresolved major disagreement, or
  JSON validation failure.
- Unfair comparison risk: use fixed post-resampling state, fixed proposed
  particles, fixed observation, same covariance convention, same dtype, and same
  upstream softmax weights.
- Hidden production drift: do not edit production `bayesfilter/`.
- Monograph/highdim/vendored/DSGE drift: no reads beyond optional status checks
  and no writes.
- Artifact fit: the planned runner directly tests the four hypotheses and writes
  a parseable result.

The audit passes for planning because the proposed artifacts answer only the
current difference-audit question and do not promote broader correctness claims.

## Verification Commands

Plan review:

```bash
claude -p --model claude-opus-4-7 --effort max
```

Execution:

```bash
python -m py_compile experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_row_173_direct_theta_hypothesis_tf.py
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_float64_row_173_direct_theta_hypothesis_tf
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_float64_row_173_direct_theta_hypothesis_tf --validate-only
python -m json.tool experiments/dpf_implementation/reports/outputs/dpf_filterflow_float64_row_173_direct_theta_hypothesis_2026-06-04.json
rg -n "import numpy|from numpy" experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_row_173_direct_theta_hypothesis_tf.py
rg -n "student|highdim|DSGE|NAWM|\\.localsource" experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_row_173_direct_theta_hypothesis_tf.py
git diff --check -- experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_row_173_direct_theta_hypothesis_tf.py docs/plans/bayesfilter-dpf-filterflow-float64-row-173-direct-theta-hypothesis-plan-2026-06-04.md docs/plans/bayesfilter-dpf-filterflow-float64-row-173-direct-theta-hypothesis-result-2026-06-04.md docs/plans/bayesfilter-dpf-filterflow-float64-row-173-direct-theta-hypothesis-review-loop-2026-06-04.md
git status --short -- bayesfilter tests docs/chapters .localsource/filterflow
git status --short --branch
```

## Claude Review Protocol

Use exactly:

```bash
claude -p --model claude-opus-4-7 --effort max
```

Claude reviews read-only and returns `ACCEPT` or `REJECT` with findings. Codex
must independently classify every Claude finding as `ACCEPT`, `PARTIAL`,
`DISPUTE`, or `CLARIFY` in the review-loop artifact. Accepted or partially
accepted findings must be patched with the exact control recorded. Disputed
findings must receive a concise rebuttal in the next Claude prompt. Loop until
`ACCEPT` or max five rounds. If a major blocker remains after round five, block
execution pending human direction.

After execution, repeat the same review loop for the result artifact.

