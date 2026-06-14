# Plan: Row 173 Log-Weight Edge Factorization Probe

## Scope

This is a BayesFilter-owned DPF difference-audit diagnostic. It factorizes the
row-173 BayesFilter log-weight carryover residual into target-time transport
log-weight input and previous-update carried normalized-log-weight routes,
using the local executable float64 FilterFlow reference as comparator. It does
not claim either implementation is mathematically correct.

Allowed write set:

- `docs/plans/bayesfilter-dpf-filterflow-float64-row-173-log-weight-edge-factorization-*.md`
- `experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_row_173_log_weight_edge_factorization_tf.py`
- `experiments/dpf_implementation/reports/dpf-filterflow-float64-row-173-log-weight-edge-factorization-2026-06-05.md`
- `experiments/dpf_implementation/reports/outputs/dpf_filterflow_float64_row_173_log_weight_edge_factorization_2026-06-05.json`

Forbidden write set:

- production `bayesfilter/`
- `tests/`
- `docs/chapters/`
- `.localsource/filterflow`
- vendored/student/highdim/DSGE/NAWM lanes

## Current Evidence

The accepted carryover-split probe concluded:

- decision:
  `filterflow_float64_row_173_bayesfilter_carryover_split_carried_log_weight_edge`;
- classification: `h3_carried_log_weight_edge`;
- raw BayesFilter
  `same_tape_full_recorded_state_residual = 15.29031158182802`;
- raw BayesFilter
  `same_tape_pre_log_weights_carryover_vjp = 15.290311581828018`;
- `carry_log_weights_stop_gradient` collapses both to numerical zero;
- `target_transport_log_weights_stop_gradient` also collapses both
  full-recorded-state/log-weight fields, but does not reduce
  `same_tape_identity_residual` or `same_tape_post_state_identity_residual`.

The next smallest question is whether the large log-weight carryover VJP is
explained by the target-time upstream into `pre_log_weights`, by the previous
update's normalized-log-weight carry into target-time `pre_log_weights`, or by
their composition.

## Evidence Contract

Question:

At row 173 and target time 93, does the BayesFilter-vs-float64-FilterFlow
log-weight carryover residual factorize into:

- target-time transport log-weight input upstream only;
- previous-update normalized-log-weight carry Jacobian only;
- the composition of the target-time upstream and previous-time carry Jacobian;
- or an unresolved route?

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
- previous time index `92`;
- `CUDA_VISIBLE_DEVICES=-1` set before TensorFlow import in parent and
  FilterFlow subprocess;
- BayesFilter replay modes:
  `raw`,
  `target_transport_log_weights_stop_gradient`,
  `previous_carry_log_weights_stop_gradient`,
  `previous_and_target_log_weights_stop_gradient`,
  and `all_times_transport_log_weights_stop_gradient`.

Tolerance controls:

- `VALUE_TOLERANCE = 5e-8`, inherited from
  `run_filterflow_float64_row_173_vjp_decomposition_tf.py`;
- `GRADIENT_TOLERANCE = 2e-4`, inherited from
  `run_filterflow_float64_row_173_vjp_decomposition_tf.py`;
- a residual or cross-side delta is `clean` when `max_abs <= 2e-4`;
- a residual or cross-side delta is `material` when `max_abs > 2e-4`.

Primary criterion:

With vetoes clear, compute target-time-93 BayesFilter mode rows containing:

- `target_to_pre_log_weights = d target / d pre_log_weights`;
- `pre_log_weights_to_pre_particles =
  VJP(pre_log_weights wrt pre_particles, ones_like(pre_log_weights))`, a
  BayesFilter-only previous-carry Jacobian probe with unit upstream;
- `same_tape_pre_log_weights_carryover_vjp`;
- `same_tape_full_recorded_state_residual`;
- `same_tape_identity_residual`;
- total gradient delta against raw FilterFlow.

Classify by which stop-gradient mode materially reduces the raw BayesFilter
log-weight carryover VJP while preserving scalar value and resampling flag
agreement.

Hypothesis classifications:

- `h1_blocked_or_vetoed`: comparator, CPU, scalar, value, finite, resampling, or
  lane-boundary veto failed.
- `h2_composition_edge`: target-only and previous-only modes each collapse the
  composed carryover VJP while reducing different factors; the evidence supports
  a target-upstream by previous-carry-Jacobian composition route.
- `h3_target_upstream_edge`: stopping only the target-time transport
  log-weight input materially reduces `target_to_pre_log_weights` and the
  log-weight carryover VJP, while previous-only stopping does not materially
  reduce the composed VJP.
- `h4_previous_carry_jacobian_edge`: stopping only the previous update's
  carried normalized log weights materially reduces
  `pre_log_weights_to_pre_particles` and the log-weight carryover VJP, while
  target-only stopping does not materially reduce the composed VJP.
- `h5_all_times_transport_only`: only all-times transport-log-weight stopping
  materially reduces the log-weight carryover VJP.
- `h6_unresolved_log_weight_edge`: finite value-valid evidence does not isolate
  the factorization.

Decision precedence after vetoes clear:

1. If required raw or mode tensors are missing/non-finite, classify
   `h1_blocked_or_vetoed`.
2. If target-only and previous-only modes each collapse
   `same_tape_pre_log_weights_carryover_vjp`, target-only materially reduces
   `target_to_pre_log_weights`, and previous-only materially reduces
   `pre_log_weights_to_pre_particles`, classify `h2_composition_edge`.
3. Else if `target_transport_log_weights_stop_gradient` materially reduces both
   `target_to_pre_log_weights` and `same_tape_pre_log_weights_carryover_vjp`,
   classify `h3_target_upstream_edge`.
4. Else if `previous_carry_log_weights_stop_gradient` materially reduces both
   `pre_log_weights_to_pre_particles` and
   `same_tape_pre_log_weights_carryover_vjp`, classify
   `h4_previous_carry_jacobian_edge`.
5. Else if only all-times transport-log-weight stopping materially reduces the
   log-weight carryover VJP, classify `h5_all_times_transport_only`.
6. Else classify `h6_unresolved_log_weight_edge`.

Material reduction threshold:

- `material_reduction = raw_max_abs - mode_max_abs > 2e-4`;
- `collapse = mode_max_abs <= 2e-4`;
- reductions are interpreted only for modes whose target scalar remains within
  `VALUE_TOLERANCE` of raw FilterFlow and whose resampling flag matches raw
  FilterFlow.

Veto diagnostics:

- FilterFlow subprocess cannot execute;
- raw BayesFilter target-time-93 replay cannot execute;
- comparator fingerprint changes during the run;
- CPU-only manifest violation in parent or subprocess;
- raw scalar mismatch beyond `VALUE_TOLERANCE = 5e-8`;
- raw value-path mismatch before edge interpretation;
- raw or mode resampling flags differ;
- required raw or mode edge tensors are missing or non-finite;
- path-boundary contamination.

Explanatory diagnostics:

- per-mode scalar deltas, gradient deltas, and resampling flags;
- per-mode edge tensor summaries and reductions from raw BayesFilter;
- per-mode deltas against raw FilterFlow edge summaries where comparable;
  the unit-upstream `pre_log_weights_to_pre_particles` factor is explicitly
  BayesFilter-only unless a matching FilterFlow unit-upstream probe is added;
- total-gradient collapse or worsening;
- prior carryover-split result digest.

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

`experiments/dpf_implementation/reports/outputs/dpf_filterflow_float64_row_173_log_weight_edge_factorization_2026-06-05.json`

## Skeptical Pre-Execution Audit

- Wrong baseline risk: use only the local executable float64 FilterFlow
  reference, not paper notation, fixed-target Sinkhorn, or upstream source.
- Proxy risk: total-gradient collapse/worsening is explanatory only; the
  primary criterion is the log-weight edge factorization.
- Hidden-assumption risk: target-time transport stopping and carried-log-weight
  stopping are diagnostic interventions, not claimed fixes.
- Stale-context risk: use target time 93 and row 173, plus previous time 92,
  not the older time-1 VJP decomposition.
- Unfair-comparison risk: mode interventions are BayesFilter-only; FilterFlow
  remains the raw executable comparator.
- Stop-condition risk: stop as blocked if required edge tensors or CPU-only
  manifests are missing.
- Runtime risk: one row, one target time, bounded list of modes.
- Lane risk: do not edit production code, tests, chapters, or FilterFlow source.

Audit status: passed for planning. This is the smallest direct factorization
after the accepted carryover-split probe because it measures the two necessary
pieces of the log-weight carryover VJP rather than adding a broader ladder.

## Phase Order

1. Claude Code reviews this plan read-only.
2. Codex audits Claude findings as `ACCEPT`, `PARTIAL`, `DISPUTE`, or
   `CLARIFY` in the review-loop artifact.
3. If accepted, implement the focused log-weight edge factorization runner.
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
python -m py_compile experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_row_173_log_weight_edge_factorization_tf.py
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_float64_row_173_log_weight_edge_factorization_tf
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_float64_row_173_log_weight_edge_factorization_tf --validate-only
python -m json.tool experiments/dpf_implementation/reports/outputs/dpf_filterflow_float64_row_173_log_weight_edge_factorization_2026-06-05.json
rg -n "import numpy|from numpy" experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_row_173_log_weight_edge_factorization_tf.py
rg -n "student|highdim|DSGE|NAWM|\\.localsource" experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_row_173_log_weight_edge_factorization_tf.py
git diff --check -- experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_row_173_log_weight_edge_factorization_tf.py docs/plans/bayesfilter-dpf-filterflow-float64-row-173-log-weight-edge-factorization-plan-2026-06-05.md docs/plans/bayesfilter-dpf-filterflow-float64-row-173-log-weight-edge-factorization-result-2026-06-05.md docs/plans/bayesfilter-dpf-filterflow-float64-row-173-log-weight-edge-factorization-review-loop-2026-06-05.md
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
Read docs/plans/bayesfilter-dpf-filterflow-float64-row-173-log-weight-edge-factorization-plan-2026-06-05.md plus AGENTS.md and CLAUDE.md read-only. Review whether the plan is adequate to test the current row-173 BayesFilter log-weight edge factorization hypotheses under BayesFilter-vs-local-float64-FilterFlow difference-audit governance. Check evidence contract, exact inputs/outputs, lane boundaries, CPU-only controls, stop conditions, non-conclusions, decision rule, and Claude/Codex finding-classification rules. Output ACCEPT or REJECT first. REJECT only for material missing controls that would invalidate the evidence contract, lane governance, CPU-only policy, exact I/O reproducibility, ordered decision rule, or stated non-conclusions; otherwise ACCEPT. If REJECT, list findings as exact missing required controls. Do not edit files.
```

Result review:

```text
Read docs/plans/bayesfilter-dpf-filterflow-float64-row-173-log-weight-edge-factorization-result-2026-06-05.md, docs/plans/bayesfilter-dpf-filterflow-float64-row-173-log-weight-edge-factorization-plan-2026-06-05.md, docs/plans/bayesfilter-dpf-filterflow-float64-row-173-log-weight-edge-factorization-review-loop-2026-06-05.md, and experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_row_173_log_weight_edge_factorization_tf.py read-only. Review whether the result follows the accepted plan, uses the decision rule correctly, preserves difference-audit governance, records exact inputs/fingerprints, lane-boundary and CPU-only controls, and avoids non-concluded claims. Output ACCEPT or REJECT first. REJECT only for material missing controls that would invalidate the evidence contract, lane governance, CPU-only policy, exact I/O reproducibility, ordered decision rule, or stated non-conclusions; otherwise ACCEPT. If REJECT, list findings as exact missing required controls. Do not edit files.
```
