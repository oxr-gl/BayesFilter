# Plan: Row 173 Proposal-Likelihood Wiring Probe

## Scope

This is a BayesFilter-owned difference-audit diagnostic for the row-173
float64 BayesFilter/FilterFlow smoothness-gradient mismatch. It follows the
accepted proposal/update adjoint-topology result, which found matching forward
tensors at time 43 but a narrow proposal-likelihood wiring difference:
FilterFlow's official proposal-likelihood path has a nonzero VJP to proposed
particles, while BayesFilter's direct sampled-distribution `log_prob` path does
not.

Allowed write set:

- `docs/plans/bayesfilter-dpf-filterflow-float64-row-173-proposal-likelihood-wiring-*.md`
- `experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_row_173_proposal_likelihood_wiring_probe_tf.py`
- `experiments/dpf_implementation/reports/dpf-filterflow-float64-row-173-proposal-likelihood-wiring-2026-06-05.md`
- `experiments/dpf_implementation/reports/outputs/dpf_filterflow_float64_row_173_proposal_likelihood_wiring_2026-06-05.json`

Forbidden write set:

- production `bayesfilter/`
- `tests/`
- `docs/chapters/`
- `.localsource/filterflow`
- vendored/student/highdim/DSGE/NAWM lanes

## Current Evidence

The accepted proposal/update adjoint-topology probe found, at row 173, target
time 93, probe time 43:

- scalar delta `6.2123888255882775e-09`, within the value gate;
- full gradient delta `[5.302734403676368, -0.1337765252068337]`;
- no forward tensor above tolerance;
- `proposal_ll_to_proposed_particles` max delta `28.749898405961705`;
- direct sampled-distribution `proposal_dist_log_prob_to_proposed_particles`
  max delta `0.0`;
- fresh-distribution `fresh_dist_log_prob_to_proposed_particles` max delta
  `0.0`;
- stop-gradient ablations were explanatory only and did not reduce the full
  gradient gap.

This says the next smallest question is not whether generic log-prob gradients
differ. It is whether BayesFilter's proposal-likelihood construction should
use a FilterFlow-style freshly rebuilt proposal distribution, and whether that
only fixes a local VJP without closing the row gradient.

## Evidence Contract

Question:

At row 173, target time 93, and probe time 43, does a FilterFlow-style freshly
rebuilt proposal-likelihood path reproduce the executable FilterFlow official
proposal-likelihood VJP in BayesFilter, and does that change the row gradient
gap?

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

- time 43, the first raw transport-upstream divergence above tolerance and
  the proposal-likelihood wiring delta isolated by the accepted previous
  result.

Primary diagnostics:

Compare FilterFlow official proposal likelihood against BayesFilter variants:

- `direct_sampled_distribution`: current BayesFilter construction,
  `proposal_dist.log_prob(proposed_particles)`;
- `fresh_recomputed_distribution_at_time_43`: use a freshly recomputed
  proposal distribution for `proposal_ll` at time 43 only;
- `fresh_recomputed_distribution_all_times`: use a freshly recomputed proposal
  distribution for `proposal_ll` at all times;
- `helper_function_recomputed_distribution_all_times`: same arithmetic as the
  fresh distribution but routed through a small BayesFilter helper function, to
  test whether Python function boundaries matter.

For each variant, record:

- scalar value and scalar delta to FilterFlow;
- total row-gradient delta to FilterFlow;
- time-43 proposal-likelihood forward equality;
- time-43 `proposal_ll_to_proposed_particles`;
- time-43 `proposal_ll_to_proposal_mean` or fresh proposal mean as applicable;
- time-43 target adjoints to proposal mean and proposed particles;
- finite tensor/gradient status;
- resampling flag agreement.

Pass criterion:

The probe answers the stated difference-audit question if all veto diagnostics
pass and the result classifies the behavior into exactly one of the outcomes
below. A passing diagnostic does not require small BayesFilter-vs-FilterFlow
gradient error; it requires a finite, reproducible, comparator-valid
localization of the wiring effect.

Hypothesis classifications:

- `h1_forward_or_scalar_veto`: a proposal-likelihood variant changes the
  forward scalar or local proposal-likelihood value beyond tolerance.
- `h2_fresh_wiring_reproduces_local_vjp_only`: fresh FilterFlow-style wiring
  reproduces the official time-43 proposal-likelihood VJP but does not reduce
  the full row-gradient gap materially.
- `h3_fresh_wiring_reduces_global_gap`: fresh wiring reproduces the official
  local VJP and materially reduces the full row-gradient gap.
- `h4_helper_boundary_not_material`: fresh direct and helper-function variants
  match each other, showing Python helper boundaries are not material.
- `h5_fresh_wiring_reproduces_proposed_particles_vjp_only`: fresh wiring
  reproduces `proposal_ll_to_proposed_particles` but not the full local
  proposal-likelihood VJP because `proposal_ll_to_proposal_mean` or the fresh
  proposal-mean analogue still differs from FilterFlow. This is a clean
  negative/localization outcome, not an execution blocker or veto.
- `blocked_or_vetoed`: comparator drift, CPU-only violation, non-finite
  tensors, missing reference, forbidden write, or unresolved scalar/resampling
  mismatch.

Veto diagnostics:

- comparator fingerprint drift;
- scalar-value mismatch beyond `5e-8`;
- proposal-likelihood value mismatch beyond `5e-8`;
- resampling flag mismatch at time 43;
- non-finite forward tensors, adjoints, or gradients;
- CPU-only manifest violation;
- path-boundary contamination;
- missing local float64 FilterFlow executable reference.

Explanatory diagnostics:

- raw direct-vs-fresh local VJP deltas;
- all-time versus time-43-only fresh wiring effects;
- helper-function versus inline fresh wiring deltas;
- total row-gradient residual after each value-valid variant;
- whether any variant materially reduces the full gradient gap.

What must not be concluded:

- correctness of either implementation;
- analytic gradient correctness;
- posterior correctness;
- global gradient agreement;
- full mesh/surface agreement;
- production readiness;
- that fresh proposal-likelihood wiring is a preferred algorithm;
- that FilterFlow is mathematically true beyond being the canonical executable
  reference for this audit lane.

## Skeptical Pre-Execution Audit

- Wrong baseline risk: use only the local executable float64 FilterFlow
  reference, not paper notation or pristine upstream.
- Proxy risk: matching the local proposal-likelihood VJP is not enough to claim
  row-gradient agreement; the full row-gradient residual remains a separate
  diagnostic.
- Hidden assumption risk: the previous artifact already showed fresh local
  distribution gradients match, while older all-time fresh boundary runs did
  not close the full gap. The plan therefore separates local VJP reproduction
  from full-gradient closure.
- Over-attribution risk: if fresh wiring fixes the local VJP but leaves the
  full gap unchanged, classify as local-only and do not claim the row mismatch
  is solved.
- Environment risk: force `CUDA_VISIBLE_DEVICES=-1` before TensorFlow import;
  ignore TensorFlow CUDA factory noise unless visible GPU devices are nonempty.
- Runtime risk: bound the run to one row, one target time, one probe time, and
  four BayesFilter wiring variants.
- Write-boundary risk: do not edit production code, tests, chapters, or
  `.localsource/filterflow`.

The audit passes because the artifact directly tests the next smallest
discriminating question raised by the accepted previous result: whether exact
FilterFlow-style proposal-likelihood wiring is the local VJP cause and whether
it explains the global row-gradient residual.

## Phase Order

1. Claude Code reviews this plan read-only.
2. Codex audits Claude findings as `ACCEPT`, `PARTIAL`, `DISPUTE`, or
   `CLARIFY` in the review-loop artifact.
3. If accepted, implement the bounded proposal-likelihood wiring runner.
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

## Verification Commands

```bash
python -m py_compile \
  experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_row_173_proposal_likelihood_wiring_probe_tf.py

CUDA_VISIBLE_DEVICES=-1 python -m \
  experiments.dpf_implementation.tf_tfp.runners.run_filterflow_float64_row_173_proposal_likelihood_wiring_probe_tf

CUDA_VISIBLE_DEVICES=-1 python -m \
  experiments.dpf_implementation.tf_tfp.runners.run_filterflow_float64_row_173_proposal_likelihood_wiring_probe_tf \
  --validate-only

python -m json.tool \
  experiments/dpf_implementation/reports/outputs/dpf_filterflow_float64_row_173_proposal_likelihood_wiring_2026-06-05.json

rg -n "import numpy|from numpy" \
  experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_row_173_proposal_likelihood_wiring_probe_tf.py

rg -n "student|highdim|DSGE|NAWM|third_party|vendored" \
  experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_row_173_proposal_likelihood_wiring_probe_tf.py \
  docs/plans/bayesfilter-dpf-filterflow-float64-row-173-proposal-likelihood-wiring-plan-2026-06-05.md

rg -n "[ \t]+$" \
  experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_row_173_proposal_likelihood_wiring_probe_tf.py \
  docs/plans/bayesfilter-dpf-filterflow-float64-row-173-proposal-likelihood-wiring-plan-2026-06-05.md \
  docs/plans/bayesfilter-dpf-filterflow-float64-row-173-proposal-likelihood-wiring-result-2026-06-05.md \
  docs/plans/bayesfilter-dpf-filterflow-float64-row-173-proposal-likelihood-wiring-review-loop-2026-06-05.md

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
