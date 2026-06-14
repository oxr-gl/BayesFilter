# Plan: Row 173 BayesFilter Carryover Split Probe

## Scope

This is a BayesFilter-owned DPF difference-audit diagnostic. It compares
BayesFilter TF/TFP graph-edge interventions against the local executable
float64 FilterFlow reference for the row-173 smoothness-gradient mismatch.
It does not claim either implementation is mathematically correct.

Allowed write set:

- `docs/plans/bayesfilter-dpf-filterflow-float64-row-173-bayesfilter-carryover-split-*.md`
- `experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_row_173_bayesfilter_carryover_split_tf.py`
- `experiments/dpf_implementation/reports/dpf-filterflow-float64-row-173-bayesfilter-carryover-split-2026-06-05.md`
- `experiments/dpf_implementation/reports/outputs/dpf_filterflow_float64_row_173_bayesfilter_carryover_split_2026-06-05.json`

Forbidden write set:

- production `bayesfilter/`
- `tests/`
- `docs/chapters/`
- `.localsource/filterflow`
- vendored/student/highdim/DSGE/NAWM lanes

## Current Evidence

The accepted state/update identity-route probe concluded:

- direct full gradient delta remains `[5.302734403676368, -0.1337765252068337]`;
- FilterFlow identity residuals are clean:
  `same_tape_identity = 3.4869329645914604e-13`,
  `same_tape_post_state_identity = 3.490541189421492e-13`, and
  `same_tape_full_recorded_state_identity = 1.0805911720979111e-11`;
- BayesFilter identity residuals are material:
  `same_tape_identity = 0.6735763083742867`,
  `same_tape_post_state_identity = 0.6735763083742867`, and
  `same_tape_full_recorded_state_identity = 15.29031158182802`;
- the largest BayesFilter carryover rows are
  `same_tape_pre_log_weights_carryover_vjp = 15.290311581828018` and
  `same_tape_pre_current_ll_carryover_vjp = 0.6735763083742855`.

The next smallest question is which BayesFilter graph edge carries the material
identity residual relative to the executable float64 FilterFlow comparator.

## Evidence Contract

Question:

At row 173 and target time 93, does the BayesFilter-only identity residual split
localize to carried log weights, carried current log likelihoods, target-time
transport-log-weight input, post-particle proposal sample path, or remain
unresolved when compared against the local executable float64 FilterFlow
reference?

Comparator:

The local executable float64 FilterFlow reference in `.localsource/filterflow`,
validated by the exact marker/fingerprint controls used in the row-173 VJP
harness:

- `FILTERFLOW_BRANCH_MARKER` from
  `experiments/dpf_implementation/tf_tfp/runners/filterflow_reference_policy.py`;
- `FILTERFLOW_MARKER_PATH = .localsource/filterflow / FILTERFLOW_BRANCH_MARKER`;
- `r3._filterflow_status()` from
  `run_filterflow_r3_float64_trace_replay_tf.py`;
- `validate_filterflow_reference_status(reference_status, marker_path=FILTERFLOW_MARKER_PATH)`;
- `continuation._filterflow_fingerprint()` and
  `continuation._fingerprints_drifted(...)` from
  `run_filterflow_1d_to_smoothness_ladder_tf.py`.

The reference checkout is read-only.

Inputs:

- row 173 mesh parameters from `run_filterflow_float64_row_173_vjp_decomposition_tf.py`;
- target time index `93`;
- `CUDA_VISIBLE_DEVICES=-1` set before TensorFlow import in parent and
  FilterFlow subprocess;
- BayesFilter boundary modes:
  `raw`,
  `target_transport_log_weights_stop_gradient`,
  `all_times_transport_log_weights_stop_gradient`,
  `carry_log_weights_stop_gradient`,
  `carry_log_likelihoods_stop_gradient`,
  `carry_both_stop_gradient`,
  `target_proposal_sample_filterflow_contract`,
  `proposal_sample_noise_stop_gradient`,
  and `filterflow_custom_transport_gradient`.

Tolerance controls:

- `VALUE_TOLERANCE = 5e-8`, inherited from
  `run_filterflow_float64_row_173_vjp_decomposition_tf.py`;
- `GRADIENT_TOLERANCE = 2e-4`, inherited from
  `run_filterflow_float64_row_173_vjp_decomposition_tf.py`;
- a residual or cross-side delta is `clean` when `max_abs <= 2e-4`;
- a residual or cross-side delta is `material` when `max_abs > 2e-4`.

Primary criterion:

With vetoes clear, classify the BayesFilter residual split by comparing each
diagnostic mode to the raw BayesFilter and raw FilterFlow target-time-93
identity rows:

- `same_tape_identity_residual`;
- `same_tape_post_state_identity_residual`;
- `same_tape_full_recorded_state_residual`;
- `same_tape_pre_log_weights_carryover_vjp`;
- `same_tape_pre_current_ll_carryover_vjp`;
- total gradient delta against raw FilterFlow.

Hypothesis classifications:

- `h1_blocked_or_vetoed`: comparator, CPU, scalar, value, finite, resampling, or
  lane-boundary veto failed.
- `h2_target_transport_log_weight_edge`: stopping the target-time transport
  log-weight input materially reduces the raw BayesFilter identity residual
  while preserving scalar value agreement.
- `h3_carried_log_weight_edge`: stopping carried log weights materially reduces
  the raw BayesFilter identity residual while preserving scalar value agreement.
- `h4_carried_log_likelihood_edge`: stopping carried cumulative log likelihoods
  materially reduces the raw BayesFilter identity residual while preserving
  scalar value agreement.
- `h5_post_particle_sample_edge`: proposal-sample/post-particle boundary modes
  materially reduce the raw BayesFilter identity residual while preserving
  scalar value agreement.
- `h6_transport_custom_gradient_not_edge`: whole-transport custom-gradient mode
  leaves the BayesFilter residual materially unchanged; this is a classification
  only if no earlier edge classification fires.
- `h7_unresolved_split`: finite value-valid evidence does not isolate a single
  edge.

Decision precedence after vetoes clear:

1. If any required raw or mode identity tensor is missing/non-finite, classify
   `h1_blocked_or_vetoed`.
2. If `target_transport_log_weights_stop_gradient` materially reduces raw
   `same_tape_identity_residual` or
   `same_tape_post_state_identity_residual`, classify
   `h2_target_transport_log_weight_edge`.
3. Else if `carry_log_weights_stop_gradient` or
   `all_times_transport_log_weights_stop_gradient` materially reduces raw
   `same_tape_full_recorded_state_residual` or
   `same_tape_pre_log_weights_carryover_vjp`, classify
   `h3_carried_log_weight_edge`.
4. Else if `carry_log_likelihoods_stop_gradient` materially reduces raw
   `same_tape_identity_residual`,
   `same_tape_post_state_identity_residual`, or
   `same_tape_pre_current_ll_carryover_vjp`, classify
   `h4_carried_log_likelihood_edge`.
5. Else if `target_proposal_sample_filterflow_contract` or
   `proposal_sample_noise_stop_gradient` materially reduces raw identity
   residuals, classify `h5_post_particle_sample_edge`.
6. Else if `filterflow_custom_transport_gradient` leaves raw residuals material,
   classify `h6_transport_custom_gradient_not_edge`.
7. Else classify `h7_unresolved_split`.

Material reduction threshold:

- `material_reduction = raw_max_abs - mode_max_abs > 2e-4`;
- `collapse = mode_max_abs <= 2e-4`;
- reductions are interpreted only for modes whose target scalar remains within
  `VALUE_TOLERANCE` of raw FilterFlow and whose resampling flag matches raw
  FilterFlow.

Veto diagnostics:

- FilterFlow subprocess cannot execute;
- raw BayesFilter target-time-93 VJP decomposition cannot execute;
- comparator fingerprint changes during the run;
- CPU-only manifest violation in parent or subprocess;
- raw scalar mismatch beyond `VALUE_TOLERANCE = 5e-8`;
- raw value-path mismatch before identity interpretation;
- raw resampling flags differ;
- required raw or mode identity tensors are missing or non-finite;
- path-boundary contamination.

Explanatory diagnostics:

- per-mode scalar deltas, gradient deltas, and resampling flags;
- per-mode identity residual summaries and reductions from raw BayesFilter;
- per-mode deltas against raw FilterFlow identity residuals;
- total-gradient collapse or worsening;
- prior state/update identity-route result digest.

What must not be concluded:

- correctness of FilterFlow or BayesFilter;
- analytic-gradient correctness;
- posterior correctness;
- global smoothness-surface agreement;
- that any boundary mode is a code fix;
- production readiness;
- public API readiness;
- monograph, highdim, DSGE, NAWM, or banking/model-risk claims.

Artifact:

`experiments/dpf_implementation/reports/outputs/dpf_filterflow_float64_row_173_bayesfilter_carryover_split_2026-06-05.json`

## Skeptical Pre-Execution Audit

- Wrong baseline risk: use only the local executable float64 FilterFlow
  reference, not paper notation, fixed-target Sinkhorn, or upstream source.
- Proxy risk: total-gradient collapse/worsening is explanatory only; the
  primary criterion is identity-residual reduction at named BayesFilter edges.
- Unfair comparison risk: boundary modes are BayesFilter-only interventions and
  must not be described as FilterFlow behavior or correctness.
- Stale-context risk: use target time 93 and row 173, not the older time-1 VJP
  decomposition.
- Hidden-assumption risk: scalar/value agreement and resampling flags must pass
  before interpreting any mode.
- Stop-condition risk: stop as blocked if required identity tensors or CPU-only
  manifests are missing.
- Runtime risk: one row, one target time, bounded list of existing modes.
- Lane risk: do not edit production code, tests, chapters, or FilterFlow source.

Audit status: passed for planning. This is the smallest direct split after the
accepted identity-route probe because it reuses existing boundary modes and
tests the exact BayesFilter carryover rows with material residuals.

## Phase Order

1. Claude Code reviews this plan read-only.
2. Codex audits Claude findings as `ACCEPT`, `PARTIAL`, `DISPUTE`, or
   `CLARIFY` in the review-loop artifact.
3. If accepted, implement the focused carryover-split runner.
4. Run CPU-only targeted execution and validations.
5. Claude Code reviews the result read-only.
6. Codex audits Claude findings and patches only if materially required.

Claude command:

```bash
claude -p --model claude-opus-4-7 --effort max
```

Codex must run Claude with trusted/escalated cross-agent execution per
`AGENTS.md`. Non-escalated Claude hangs, auth failures, or missing output are
sandbox evidence only.

Maximum review iterations: 5 for plan review and 5 for result review. On the
fifth iteration, accept only for user inspection unless a major blocker remains.

## Review-Finding Classification Rule

Claude should `REJECT` only for material missing controls that would invalidate
the evidence contract, lane governance, CPU-only policy, exact input/output
reproducibility, ordered decision rule, or stated non-conclusions.

Codex must classify each Claude finding:

- `ACCEPT`: materially correct; patch required.
- `PARTIAL`: directionally correct, but patch narrower or different.
- `DISPUTE`: incorrect, over-scoped, inconsistent with governance, or would
  weaken the evidence contract.
- `CLARIFY`: cannot evaluate without more evidence or human direction.

## Planned Commands

```bash
python -m py_compile experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_row_173_bayesfilter_carryover_split_tf.py
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_float64_row_173_bayesfilter_carryover_split_tf
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_float64_row_173_bayesfilter_carryover_split_tf --validate-only
python -m json.tool experiments/dpf_implementation/reports/outputs/dpf_filterflow_float64_row_173_bayesfilter_carryover_split_2026-06-05.json
rg -n "import numpy|from numpy" experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_row_173_bayesfilter_carryover_split_tf.py
rg -n "student|highdim|DSGE|NAWM|\\.localsource" experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_row_173_bayesfilter_carryover_split_tf.py
git diff --check -- experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_row_173_bayesfilter_carryover_split_tf.py docs/plans/bayesfilter-dpf-filterflow-float64-row-173-bayesfilter-carryover-split-plan-2026-06-05.md docs/plans/bayesfilter-dpf-filterflow-float64-row-173-bayesfilter-carryover-split-result-2026-06-05.md docs/plans/bayesfilter-dpf-filterflow-float64-row-173-bayesfilter-carryover-split-review-loop-2026-06-05.md
git status --short -- bayesfilter tests docs/chapters .localsource/filterflow
git status --short -- experiments/controlled_dpf_baseline third_party docs/plans/bayesfilter-highdim-* docs/plans/*highdim* docs/plans/*DSGE* docs/plans/*NAWM* tests/highdim bayesfilter/highdim
git status --short --branch
```

The `.localsource` search is expected to find only read-only comparator
identity paths; it is a contamination check, not a ban on the canonical
executable reference.

## Claude Review Prompt

Plan review:

```text
Read docs/plans/bayesfilter-dpf-filterflow-float64-row-173-bayesfilter-carryover-split-plan-2026-06-05.md plus AGENTS.md and CLAUDE.md read-only. Review whether the plan is adequate to test the current row-173 BayesFilter carryover/identity residual split hypotheses under BayesFilter-vs-local-float64-FilterFlow difference-audit governance. Check evidence contract, exact inputs/outputs, lane boundaries, CPU-only controls, stop conditions, non-conclusions, decision rule, and Claude/Codex finding-classification rules. Output ACCEPT or REJECT first. REJECT only for material missing controls that would invalidate the evidence contract, lane governance, CPU-only policy, exact I/O reproducibility, ordered decision rule, or stated non-conclusions; otherwise ACCEPT. If REJECT, list findings as exact missing required controls. Do not edit files.
```

Result review:

```text
Read docs/plans/bayesfilter-dpf-filterflow-float64-row-173-bayesfilter-carryover-split-result-2026-06-05.md, docs/plans/bayesfilter-dpf-filterflow-float64-row-173-bayesfilter-carryover-split-plan-2026-06-05.md, docs/plans/bayesfilter-dpf-filterflow-float64-row-173-bayesfilter-carryover-split-review-loop-2026-06-05.md, and experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_row_173_bayesfilter_carryover_split_tf.py read-only. Review whether the result follows the accepted plan, uses the decision rule correctly, preserves difference-audit governance, records exact inputs/fingerprints, lane-boundary and CPU-only controls, and avoids non-concluded claims. Output ACCEPT or REJECT first. REJECT only for material missing controls that would invalidate the evidence contract, lane governance, CPU-only policy, exact I/O reproducibility, ordered decision rule, or stated non-conclusions; otherwise ACCEPT. If REJECT, list findings as exact missing required controls. Do not edit files.
```
