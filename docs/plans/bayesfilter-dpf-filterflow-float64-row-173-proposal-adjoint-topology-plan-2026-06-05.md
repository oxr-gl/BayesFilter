# Plan: Row 173 Proposal/Update Adjoint-Topology Probe

## Scope

This is a BayesFilter-owned difference-audit diagnostic for the row-173
float64 BayesFilter/FilterFlow smoothness-gradient mismatch. It follows the
accepted transport-upstream-source result, which found matching forward
tensors but divergent adjoints at times 43 and 52.

The diagnostic compares BayesFilter TF/TFP against the local executable
float64 FilterFlow reference only. It does not claim either implementation is
mathematically correct.

Allowed write set:

- `docs/plans/bayesfilter-dpf-filterflow-float64-row-173-proposal-adjoint-topology-*.md`
- `experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_row_173_proposal_adjoint_topology_probe_tf.py`
- `experiments/dpf_implementation/reports/dpf-filterflow-float64-row-173-proposal-adjoint-topology-2026-06-05.md`
- `experiments/dpf_implementation/reports/outputs/dpf_filterflow_float64_row_173_proposal_adjoint_topology_2026-06-05.json`

Forbidden write set:

- production `bayesfilter/`
- `tests/`
- `docs/chapters/`
- `.localsource/filterflow`
- vendored/student/highdim/DSGE/NAWM lanes

## Current Evidence

The accepted transport-upstream-source probe found:

- no forward node above tolerance at times 43 or 52;
- time 43 first adjoint delta node: `pre_particles`, max delta `5.500608568351231`;
- time 43 dominant adjoint contributors:
  `proposal_mean` and `proposed_particles`, max delta `14.4878444484294`;
- time 52 first/max adjoint node: `pre_particles`, max delta `5.757224499990219`;
- time 52 proposal mean/proposed particles adjoint delta:
  `4.655565035713791`;
- clip masks and resampling flags matched.

Therefore the next question is whether the adjoint mismatch is caused by the
proposal/update graph itself, especially the `MultivariateNormalTriL` proposal
sample/log-prob path, or by how its outputs are connected to later update
terms.

## Evidence Contract

Question:

At row 173, target time 93, and probe time 43, do BayesFilter and executable
float64 FilterFlow differ in the local proposal/update adjoint contract when
given matching forward tensors?

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

Probe time:

- time 43, because it is the first raw transport-upstream divergence above
  tolerance and has dominant proposal-mean/proposed-particle adjoint deltas.

Primary diagnostics:

At time 43, compare BayesFilter and FilterFlow:

- forward values and adjoints for proposal inputs:
  post-transport particles, observation, transition matrix, proposal mean,
  proposal covariance/Cholesky, sample noise implied by
  `proposed_particles - proposal_mean`, and proposed particles;
- forward values and adjoints for proposal/update terms:
  proposal log-prob, transition log-prob, observation log-prob, unnormalized
  weights, increment, normalized log weights, and post-update log likelihoods;
- direct local-gradient probes for the same scalar target:
  `d target / d proposal_mean`,
  `d target / d proposed_particles`,
  `d proposal_ll / d proposal_mean`,
  `d transition_ll / d proposed_particles`,
  `d observation_ll / d proposed_particles`, and
  `d proposal_sample / d proposal_mean` where meaningful;
- a stop-gradient ablation table that recomputes the BayesFilter scalar
  gradient under narrowly named local stops:
  `stop_proposed_particles`,
  `stop_proposal_mean`,
  `stop_proposal_ll`,
  `stop_transition_ll`,
  `stop_observation_ll`, and
  `stop_proposal_sample_noise`.

Pass criterion:

The probe answers the stated difference-audit question if all veto diagnostics
pass and the result classifies the observed row-173 target-time-93
BayesFilter-vs-float64-FilterFlow gradient mismatch into exactly one of the
listed hypothesis outcomes, or explicitly records a bounded multi-hypothesis
classification when the evidence supports more than one local mechanism. A
passing diagnostic does not require small BayesFilter-vs-FilterFlow gradient
error; it requires a finite, reproducible, comparator-valid localization of
the difference.

Hypothesis classifications:

- `h1_forward_contract_drift`: local proposal/update forward tensors differ
  above tolerance.
- `h2_proposal_sample_gradient_contract`: forward tensors match, but the
  proposal sample path has a different adjoint contract.
- `h3_log_prob_gradient_contract`: forward tensors match, but proposal,
  transition, or observation log-prob local adjoints differ.
- `h4_downstream_update_topology`: local proposal/update direct adjoints match
  but the target-scalar adjoint entering the region differs from downstream
  topology.
- `blocked_or_vetoed`: comparator drift, scalar mismatch, resampling mismatch,
  non-finite tensors, CPU-only violation, path-boundary violation, or missing
  instrumentation.

Veto diagnostics:

- comparator fingerprint drift;
- scalar-value mismatch beyond `5e-8`;
- resampling flag mismatch at time 43;
- non-finite forward tensors or adjoints;
- CPU-only manifest violation;
- path-boundary contamination;
- missing local float64 FilterFlow executable reference.

Explanatory diagnostics:

- local proposal/update forward deltas;
- local proposal/update adjoint deltas;
- stop-gradient ablation residuals relative to the full row gradient delta;
- whether sample-noise stop changes the BayesFilter-vs-FilterFlow gap;
- distinction between first adjoint difference and largest adjoint contributor.

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
- Proxy risk: finite tensors and matching scalar values are veto checks only;
  localization depends on direct local adjoint comparisons and ablations.
- Hidden assumption risk: proposal formulas may match while TFP sample/log-prob
  graph connectivity differs; the plan explicitly separates forward values,
  local adjoints, and downstream target adjoints.
- Over-attribution risk: if multiple local adjoints diverge, classify the
  region, not a single line of code.
- Environment risk: force `CUDA_VISIBLE_DEVICES=-1` before TensorFlow import;
  ignore TensorFlow CUDA factory noise unless visible GPU devices are nonempty.
- Runtime risk: bound the run to one row, one target time, one probe time, and
  a small stop-gradient ablation table.
- Write-boundary risk: do not edit production code, tests, chapters, or
  `.localsource/filterflow`.

The audit passes because the proposed artifact directly tests the next
smallest discriminating question raised by the accepted source probe: whether
the proposal/update local gradient contract matches when forward tensors do.

## Phase Order

1. Claude Code reviews this plan read-only.
2. Codex audits Claude findings as `ACCEPT`, `PARTIAL`, `DISPUTE`, or
   `CLARIFY` in the review-loop artifact.
3. If accepted, implement the bounded proposal/update topology runner.
4. Run CPU-only targeted probe and validations.
5. Claude Code reviews the result read-only.
6. Codex audits Claude findings and patches only if materially required.

Claude command:

```bash
claude -p --model claude-opus-4-7 --effort max
```

Codex must run the Claude command in trusted/escalated cross-agent execution
per `AGENTS.md`; non-escalated Claude hangs, auth failures, or missing output
are sandbox evidence only and must not be treated as a substantive review.

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
  experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_row_173_proposal_adjoint_topology_probe_tf.py

CUDA_VISIBLE_DEVICES=-1 python -m \
  experiments.dpf_implementation.tf_tfp.runners.run_filterflow_float64_row_173_proposal_adjoint_topology_probe_tf

CUDA_VISIBLE_DEVICES=-1 python -m \
  experiments.dpf_implementation.tf_tfp.runners.run_filterflow_float64_row_173_proposal_adjoint_topology_probe_tf \
  --validate-only

python -m json.tool \
  experiments/dpf_implementation/reports/outputs/dpf_filterflow_float64_row_173_proposal_adjoint_topology_2026-06-05.json

rg -n "import numpy|from numpy" \
  experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_row_173_proposal_adjoint_topology_probe_tf.py

rg -n "student|highdim|DSGE|NAWM|third_party|vendored" \
  experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_row_173_proposal_adjoint_topology_probe_tf.py \
  docs/plans/bayesfilter-dpf-filterflow-float64-row-173-proposal-adjoint-topology-plan-2026-06-05.md

rg -n "[ \t]+$" \
  experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_row_173_proposal_adjoint_topology_probe_tf.py \
  docs/plans/bayesfilter-dpf-filterflow-float64-row-173-proposal-adjoint-topology-plan-2026-06-05.md \
  docs/plans/bayesfilter-dpf-filterflow-float64-row-173-proposal-adjoint-topology-result-2026-06-05.md \
  docs/plans/bayesfilter-dpf-filterflow-float64-row-173-proposal-adjoint-topology-review-loop-2026-06-05.md

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
- the probe is too expensive for a bounded CPU run;
- Claude/Codex disagreement persists after round 5 without human direction.
