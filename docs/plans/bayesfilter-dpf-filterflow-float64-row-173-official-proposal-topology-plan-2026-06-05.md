# Plan: Row 173 Official Proposal-Likelihood Topology Probe

## Scope

This is a BayesFilter-owned DPF implementation/evidence diagnostic.  It compares
BayesFilter TF/TFP against the local executable float64 FilterFlow checkout for a
single localized smoothness-gradient discrepancy.

Do not edit:

- production `bayesfilter/`
- `tests/`
- `docs/chapters/`
- `.localsource/filterflow/`
- vendored/student/high-dimensional/DSGE/NAWM lanes

Allowed artifacts:

- `experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_row_173_official_proposal_topology_tf.py`
- `experiments/dpf_implementation/reports/outputs/dpf_filterflow_float64_row_173_official_proposal_topology_2026-06-05.json`
- `experiments/dpf_implementation/reports/dpf-filterflow-float64-row-173-official-proposal-topology-2026-06-05.md`
- `docs/plans/bayesfilter-dpf-filterflow-float64-row-173-official-proposal-topology-result-2026-06-05.md`
- `docs/plans/bayesfilter-dpf-filterflow-float64-row-173-official-proposal-topology-review-loop-2026-06-05.md`

## Current Evidence Being Tested

The latest reviewed result
`bayesfilter-dpf-filterflow-float64-row-173-proposal-likelihood-wiring-result-2026-06-05.md`
classified the remaining local evidence as
`h5_fresh_wiring_reproduces_proposed_particles_vjp_only`:

- direct BayesFilter sampled-distribution proposal likelihood has
  `proposal_ll_to_proposed_particles` delta `28.749898405961705`;
- fresh BayesFilter proposal-likelihood wiring makes
  `proposal_ll_to_proposed_particles` delta `0.0`;
- fresh BayesFilter proposal-likelihood wiring has
  `proposal_ll_to_proposal_mean` delta `28.749898405961705`;
- full row-173 gradient gap remains about `5.30`;
- scalar, forward-value, resampling, transport, helper-boundary, CPU-only, and
  reference controls were clear.

## Hypotheses

H1. The remaining discrepancy is an internal-node mismatch: FilterFlow's official
`OptimalProposalModel.loglikelihood` constructs an internal proposal mean whose
VJP matches BayesFilter's fresh proposal mean, while the sampling proposal mean
has zero VJP because it is not on the official likelihood graph.

H2. The remaining discrepancy is a state-object topology mismatch: passing
`proposed_state` and `resampled_state` through FilterFlow's official
`loglikelihood` creates a graph route that is not reproduced by BayesFilter's
direct sampled-distribution log-prob call.

H3. The remaining discrepancy is not caused by the functional expression for the
fresh proposal likelihood.  A BayesFilter helper with exact FilterFlow arithmetic
should match an inline BayesFilter fresh log-prob expression at both values and
VJPs.

H4. Even if the official proposal-likelihood local VJP is mirrored, the full
row-173 gradient gap may remain.  In that case this diagnostic should classify
the proposal-likelihood topology as locally reconciled but not globally closed.

## Evidence Contract

Question: Which proposal-likelihood graph construction reproduces the
executable float64 FilterFlow official `OptimalProposalModel.loglikelihood`
VJP pattern at row `173`, target time `93`, probe time `43`?

Comparator: local canonical executable float64 FilterFlow checkout at
`.localsource/filterflow`, validated by the existing reference-status and
fingerprint helpers.  The checkout is read-only for this plan.

Primary criterion:

- with vetoes clear, classify whether BayesFilter can reproduce FilterFlow's
  official proposal-likelihood VJP pattern for all three decision-critical
  local routes:
  - `proposal_ll_to_proposed_particles`;
  - `proposal_ll_to_sampling_proposal_mean`;
  - `proposal_ll_to_internal_likelihood_mean`;
- and record whether any value-preserving variant materially reduces the full
  row-173 gradient gap.

Veto diagnostics:

- FilterFlow subprocess cannot execute;
- comparator fingerprint changes during the run;
- CPU-only policy fails, meaning `CUDA_VISIBLE_DEVICES=-1` was not set before
  TensorFlow import in the parent runner;
- path-boundary manifest detects forbidden production/test/chapter/highdim/etc.
  drift caused by this diagnostic;
- target scalar or proposal-likelihood forward values differ above tolerance;
- resampling flags differ;
- forward tensors, adjoints, or local gradients are non-finite;
- the instrumented FilterFlow official internal proposal mean cannot be captured
  without editing `.localsource/filterflow`.

Explanatory diagnostics:

- direct sampled-distribution log-prob VJPs;
- inline fresh log-prob VJPs;
- helper fresh log-prob VJPs;
- official FilterFlow loglikelihood VJPs to proposed particles, sampling mean,
  and internal likelihood mean;
- BayesFilter mirrored variants with direct, fresh, helper, and detached
  sampling-mean constructions;
- first forward/adjoint/local-gradient delta nodes;
- row/column transport residuals and transport upstream deltas;
- total row-gradient deltas for each value-valid variant.

Not concluded:

- no correctness claim for FilterFlow or BayesFilter;
- no analytic-gradient correctness claim;
- no posterior correctness claim;
- no global smoothness-surface agreement claim;
- no production readiness or public API readiness;
- no monograph, high-dimensional, DSGE, NAWM, or banking/model-risk claim.

Artifact:

`experiments/dpf_implementation/reports/outputs/dpf_filterflow_float64_row_173_official_proposal_topology_2026-06-05.json`

Exact canonical input sources:

- Primary prior evidence:
  `experiments/dpf_implementation/reports/outputs/dpf_filterflow_float64_row_173_proposal_likelihood_wiring_2026-06-05.json`
- Prior reviewed result:
  `docs/plans/bayesfilter-dpf-filterflow-float64-row-173-proposal-likelihood-wiring-result-2026-06-05.md`
- Constants reused by the runner:
  `experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_row_173_vjp_decomposition_tf.py`

The output JSON and report must echo or fingerprint:

- row/mesh index;
- target time and probe time;
- data and filter seeds;
- theta vector;
- number of particles, batch size, and horizon;
- initial-particle digest;
- observation-path digest;
- transition covariance and its Cholesky digest;
- observation covariance and its Cholesky digest;
- ESS threshold and resampling settings;
- transport epsilon, scaling, convergence threshold, max iterations, gradient
  mode, and application mode;
- FilterFlow reference branch/commit/status fingerprint before and after the
  run.

## Skeptical Pre-Execution Audit

- Stale context: use the latest reviewed row-173 proposal-likelihood wiring
  result as the baseline, not earlier float32 or 1D artifacts.
- Wrong reference hierarchy: the comparator is the local executable float64
  FilterFlow checkout, not the paper table, fixed-target Sinkhorn, or pristine
  upstream source.
- Proxy metric risk: transport residuals and finite gradients are explanatory
  only; the primary criterion is local VJP-pattern agreement to executable
  FilterFlow.
- Missing stop condition: stop as blocked if official internal likelihood mean
  cannot be instrumented without mutating `.localsource/filterflow`.
- Unfair comparison risk: use the same observations, initial particles, seeds,
  theta, transition covariance, observation path, ESS/resampling policy, and
  transport settings as the reviewed row-173 artifacts.
- Hidden environment mismatch: set `CUDA_VISIBLE_DEVICES=-1` before TensorFlow
  import in parent and subprocess.
- Hidden production drift: verify status for forbidden lanes and do not edit
  production/test/chapter files.
- Artifact-answer fit: the JSON must expose both local VJP rows and full
  gradient deltas for each construction, otherwise it does not answer the
  question.

Audit status: passed for planning.  The proposed diagnostic is localized, uses
the current reviewed comparator evidence, has explicit vetoes, and does not use
transport residuals or finite gradients as proof of correctness.

## Review-Finding Classification Rule

Claude should `REJECT` only for material missing controls that would invalidate
the evidence contract, lane governance, CPU-only policy, exact I/O
reproducibility, ordered decision rule, or stated non-conclusions.  Non-blocking
style preferences or broader future-work suggestions should not be marked as
reject-worthy findings.

Codex must independently classify every Claude finding as `ACCEPT`, `PARTIAL`,
`DISPUTE`, or `CLARIFY`.  Accepted or partially accepted findings must be
patched and recorded with the exact control added.  Disputed findings must carry
a concise evidence-based rebuttal into the next Claude prompt.

## Decision Rule

If any veto fires, classify `blocked_or_vetoed`.

Otherwise classify:

- `h1_internal_node_reconciles_official_vjp`: instrumented FilterFlow shows the
  official VJP is zero to the sampling proposal mean, nonzero to proposed
  particles, nonzero to the internal likelihood proposal mean, and BayesFilter
  reproduces all three official VJPs with a fresh/internal likelihood mean.
- `h2_state_object_topology_required`: BayesFilter reproduces the official VJP
  only when using a state-object/official-call mirror, not a pure fresh helper.
- `h3_functional_fresh_expression_reconciles_local_vjp`: inline/helper fresh
  expressions reproduce the official VJP pattern without needing object
  topology.
- `h4_local_reconciled_global_gap_remains`: local official proposal-likelihood
  VJPs are reconciled, but the full row-173 gradient gap remains above
  tolerance.
- `h5_unresolved_official_topology_gap`: the diagnostic is value-valid and
  finite, but none of the tested BayesFilter constructions reproduces the
  FilterFlow official VJP pattern.

When multiple labels apply, use the most specific local-topology label first,
and record `global_gap_remaining: true/false` separately.

## Planned Commands

```bash
python -m py_compile experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_row_173_official_proposal_topology_tf.py
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_float64_row_173_official_proposal_topology_tf
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_float64_row_173_official_proposal_topology_tf --validate-only
python -m json.tool experiments/dpf_implementation/reports/outputs/dpf_filterflow_float64_row_173_official_proposal_topology_2026-06-05.json
rg -n "import numpy|from numpy" experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_row_173_official_proposal_topology_tf.py
rg -n "student|highdim|DSGE|NAWM|\\.localsource" experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_row_173_official_proposal_topology_tf.py
git diff --check -- experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_row_173_official_proposal_topology_tf.py docs/plans/bayesfilter-dpf-filterflow-float64-row-173-official-proposal-topology-plan-2026-06-05.md docs/plans/bayesfilter-dpf-filterflow-float64-row-173-official-proposal-topology-result-2026-06-05.md docs/plans/bayesfilter-dpf-filterflow-float64-row-173-official-proposal-topology-review-loop-2026-06-05.md
git status --short -- bayesfilter tests docs/chapters .localsource/filterflow
git status --short -- experiments/controlled_dpf_baseline third_party docs/plans/bayesfilter-highdim-* docs/plans/*highdim* docs/plans/*DSGE* docs/plans/*NAWM* tests/highdim bayesfilter/highdim
git status --short --branch
```

The `.localsource` string search is expected to find only read-only reference
path constants/import-policy checks; it is a contamination check, not a blanket
ban on comparing to the canonical executable reference.

## Claude Review Prompt

Plan review:

```text
Read docs/plans/bayesfilter-dpf-filterflow-float64-row-173-official-proposal-topology-plan-2026-06-05.md plus AGENTS.md and CLAUDE.md read-only. Review whether the plan is adequate to test the current row-173 official proposal-likelihood topology hypotheses under BayesFilter-vs-local-float64-FilterFlow difference-audit governance. Check evidence contract, exact inputs/outputs, lane boundaries, CPU-only controls, stop conditions, non-conclusions, decision rule, and Claude/Codex finding-classification rules. Output ACCEPT or REJECT first. REJECT only for material missing controls that would invalidate the evidence contract, lane governance, CPU-only policy, exact I/O reproducibility, ordered decision rule, or stated non-conclusions; otherwise ACCEPT. If REJECT, list findings as exact missing required controls. Do not edit files.
```

Result review:

```text
Read docs/plans/bayesfilter-dpf-filterflow-float64-row-173-official-proposal-topology-result-2026-06-05.md, docs/plans/bayesfilter-dpf-filterflow-float64-row-173-official-proposal-topology-plan-2026-06-05.md, docs/plans/bayesfilter-dpf-filterflow-float64-row-173-official-proposal-topology-review-loop-2026-06-05.md, and experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_row_173_official_proposal_topology_tf.py read-only. Review whether the result follows the accepted plan, uses the ordered decision rule correctly, preserves difference-audit governance, records exact inputs/outputs, lane-boundary and CPU-only controls, and avoids non-concluded claims. Output ACCEPT or REJECT first. REJECT only for material missing controls that would invalidate the evidence contract, lane governance, CPU-only policy, exact I/O reproducibility, ordered decision rule, or stated non-conclusions; otherwise ACCEPT. If REJECT, list findings as exact missing required controls. Do not edit files.
```
