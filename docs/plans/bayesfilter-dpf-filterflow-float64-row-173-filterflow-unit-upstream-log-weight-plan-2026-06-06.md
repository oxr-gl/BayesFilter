# Plan: Row 173 FilterFlow Unit-Upstream Log-Weight Probe

## Scope

This is a BayesFilter-owned DPF difference-audit diagnostic. It compares the
BayesFilter unit-upstream previous log-weight carry Jacobian from the accepted
log-weight factorization probe against a matching unit-upstream probe executed
inside the local float64 FilterFlow reference. It does not claim either
implementation is mathematically correct.

Allowed write set:

- `docs/plans/bayesfilter-dpf-filterflow-float64-row-173-filterflow-unit-upstream-log-weight-*.md`
- `experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_row_173_filterflow_unit_upstream_log_weight_tf.py`
- `experiments/dpf_implementation/reports/dpf-filterflow-float64-row-173-filterflow-unit-upstream-log-weight-2026-06-06.md`
- `experiments/dpf_implementation/reports/outputs/dpf_filterflow_float64_row_173_filterflow_unit_upstream_log_weight_2026-06-06.json`

Forbidden write set:

- production `bayesfilter/`
- `tests/`
- `docs/chapters/`
- `.localsource/filterflow`
- vendored/student/highdim/DSGE/NAWM lanes

## Current Evidence

The accepted log-weight edge factorization probe concluded:

- decision:
  `filterflow_float64_row_173_log_weight_edge_factorization_composition_edge`;
- classification: `h2_composition_edge`;
- raw BayesFilter target-time upstream:
  `target_to_pre_log_weights = 1.1695816018044372`;
- raw BayesFilter unit-upstream previous-carry factor:
  `pre_log_weights_to_pre_particles = 7.930673258917527`;
- raw BayesFilter composed log-weight carryover VJP:
  `same_tape_pre_log_weights_carryover_vjp = 15.290311581828018`;
- target-only stopping collapses target upstream and the composed VJP while not
  reducing the unit previous-carry factor;
- previous-only stopping collapses the unit previous-carry factor and the
  composed VJP.

The remaining gap is whether the unit-upstream previous-carry Jacobian itself
is a BayesFilter-vs-FilterFlow difference, or whether the cross-side difference
only appears when composed with the target-time upstream.

## Evidence Contract

Question:

At row 173 and target time 93, does executable float64 FilterFlow's
unit-upstream VJP
`VJP(pre_log_weights wrt pre_particles, ones_like(pre_log_weights))`
match BayesFilter's unit-upstream previous-carry factor, or is the
unit-upstream factor itself a cross-implementation difference?

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
- local executable float64 FilterFlow unit-upstream probe at the target-time
  `state_with_ess.log_weights` / `state_with_ess.particles` edge;
- BayesFilter unit-upstream factor loaded from the accepted
  `dpf_filterflow_float64_row_173_log_weight_edge_factorization_2026-06-05.json`
  artifact and recomputed in the same runner if needed for validation.

Tolerance controls:

- `VALUE_TOLERANCE = 5e-8`, inherited from
  `run_filterflow_float64_row_173_vjp_decomposition_tf.py`;
- `GRADIENT_TOLERANCE = 2e-4`, inherited from
  `run_filterflow_float64_row_173_vjp_decomposition_tf.py`;
- a unit-upstream VJP delta is `match` when `max_abs_delta <= 2e-4`;
- a unit-upstream VJP delta is `material` when `max_abs_delta > 2e-4`.

Primary criterion:

With vetoes clear, compare:

- FilterFlow `target_to_pre_log_weights`;
- BayesFilter `target_to_pre_log_weights`;
- FilterFlow
  `pre_log_weights_to_pre_particles_unit_upstream`;
- BayesFilter
  `pre_log_weights_to_pre_particles_unit_upstream`;
- FilterFlow composed `same_tape_pre_log_weights_carryover_vjp`;
- BayesFilter composed `same_tape_pre_log_weights_carryover_vjp`.

Hypothesis classifications:

- `h1_blocked_or_vetoed`: comparator, CPU, scalar, value, finite, resampling, or
  lane-boundary veto failed.
- `h2_unit_upstream_factor_differs`: unit-upstream previous-carry VJPs differ
  by more than `2e-4`.
- `h3_unit_upstream_matches_composed_differs`: unit-upstream VJPs match, but
  the composed log-weight carryover VJP differs.
- `h4_log_weight_unit_probe_matches`: unit-upstream and composed log-weight
  VJPs both match within tolerance.
- `h5_unresolved_unit_probe`: finite value-valid evidence does not isolate the
  unit-upstream factor.

Decision precedence after vetoes clear:

1. If required unit/composed tensors are missing/non-finite, classify
   `h1_blocked_or_vetoed`.
2. If unit-upstream previous-carry VJPs differ materially, classify
   `h2_unit_upstream_factor_differs`.
3. Else if unit-upstream VJPs match but composed carryover VJPs differ
   materially, classify `h3_unit_upstream_matches_composed_differs`.
4. Else if both unit-upstream and composed carryover VJPs match, classify
   `h4_log_weight_unit_probe_matches`.
5. Else classify `h5_unresolved_unit_probe`.

Veto diagnostics:

- FilterFlow unit-upstream subprocess cannot execute;
- BayesFilter factorization artifact is missing or invalid;
- comparator fingerprint changes during the run;
- CPU-only manifest violation in parent or subprocess;
- scalar mismatch beyond `VALUE_TOLERANCE = 5e-8`;
- resampling flags differ;
- required unit/composed tensors are missing or non-finite;
- path-boundary contamination.

Explanatory diagnostics:

- target-to-pre-log-weight upstream delta;
- composed log-weight carryover VJP delta;
- raw total-gradient delta inherited from the factorization artifact;
- previous factorization digest;
- TensorFlow package versions and CPU-only manifests.

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

`experiments/dpf_implementation/reports/outputs/dpf_filterflow_float64_row_173_filterflow_unit_upstream_log_weight_2026-06-06.json`

## Skeptical Pre-Execution Audit

- Wrong baseline risk: use only the local executable float64 FilterFlow
  reference, not paper notation, fixed-target Sinkhorn, or upstream source.
- Proxy risk: total-gradient deltas are explanatory only; the primary criterion
  is the unit-upstream previous-carry VJP comparison.
- Hidden-assumption risk: unit-upstream VJP is a diagnostic factor, not a
  correctness proof.
- Stale-context risk: use target time 93 and row 173, not older time-1 probes.
- Unfair-comparison risk: the FilterFlow unit-upstream probe must be computed
  in the executable FilterFlow subprocess, not inferred from BayesFilter.
- Stop-condition risk: stop as blocked if required tensors, CPU-only manifests,
  or comparator fingerprint checks are missing.
- Runtime risk: one row, one target time, one bounded FilterFlow subprocess.
- Lane risk: do not edit production code, tests, chapters, or FilterFlow source.

Audit status: passed for planning. This is the smallest direct test after the
accepted factorization result because it adds the exact missing FilterFlow
unit-upstream factor.

## Phase Order

1. Claude Code reviews this plan read-only.
2. Codex audits Claude findings as `ACCEPT`, `PARTIAL`, `DISPUTE`, or
   `CLARIFY` in the review-loop artifact.
3. If accepted, implement the focused unit-upstream comparison runner.
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
python -m py_compile experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_row_173_filterflow_unit_upstream_log_weight_tf.py
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_float64_row_173_filterflow_unit_upstream_log_weight_tf
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_float64_row_173_filterflow_unit_upstream_log_weight_tf --validate-only
python -m json.tool experiments/dpf_implementation/reports/outputs/dpf_filterflow_float64_row_173_filterflow_unit_upstream_log_weight_2026-06-06.json
rg -n "import numpy|from numpy" experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_row_173_filterflow_unit_upstream_log_weight_tf.py
rg -n "student|highdim|DSGE|NAWM|\\.localsource" experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_row_173_filterflow_unit_upstream_log_weight_tf.py
git diff --check -- experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_row_173_filterflow_unit_upstream_log_weight_tf.py docs/plans/bayesfilter-dpf-filterflow-float64-row-173-filterflow-unit-upstream-log-weight-plan-2026-06-06.md docs/plans/bayesfilter-dpf-filterflow-float64-row-173-filterflow-unit-upstream-log-weight-result-2026-06-06.md docs/plans/bayesfilter-dpf-filterflow-float64-row-173-filterflow-unit-upstream-log-weight-review-loop-2026-06-06.md
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
Read docs/plans/bayesfilter-dpf-filterflow-float64-row-173-filterflow-unit-upstream-log-weight-plan-2026-06-06.md plus AGENTS.md and CLAUDE.md read-only. Review whether the plan is adequate to test the current row-173 FilterFlow-vs-BayesFilter unit-upstream log-weight factor hypotheses under BayesFilter-vs-local-float64-FilterFlow difference-audit governance. Check evidence contract, exact inputs/outputs, lane boundaries, CPU-only controls, stop conditions, non-conclusions, decision rule, and Claude/Codex finding-classification rules. Output ACCEPT or REJECT first. REJECT only for material missing controls that would invalidate the evidence contract, lane governance, CPU-only policy, exact I/O reproducibility, ordered decision rule, or stated non-conclusions; otherwise ACCEPT. If REJECT, list findings as exact missing required controls. Do not edit files.
```

Result review:

```text
Read docs/plans/bayesfilter-dpf-filterflow-float64-row-173-filterflow-unit-upstream-log-weight-result-2026-06-06.md, docs/plans/bayesfilter-dpf-filterflow-float64-row-173-filterflow-unit-upstream-log-weight-plan-2026-06-06.md, docs/plans/bayesfilter-dpf-filterflow-float64-row-173-filterflow-unit-upstream-log-weight-review-loop-2026-06-06.md, and experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_row_173_filterflow_unit_upstream_log_weight_tf.py read-only. Review whether the result follows the accepted plan, uses the decision rule correctly, preserves difference-audit governance, records exact inputs/fingerprints, lane-boundary and CPU-only controls, and avoids non-concluded claims. Output ACCEPT or REJECT first. REJECT only for material missing controls that would invalidate the evidence contract, lane governance, CPU-only policy, exact I/O reproducibility, ordered decision rule, or stated non-conclusions; otherwise ACCEPT. If REJECT, list findings as exact missing required controls. Do not edit files.
```
