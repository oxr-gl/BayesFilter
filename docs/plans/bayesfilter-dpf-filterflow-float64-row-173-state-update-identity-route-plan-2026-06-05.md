# Plan: Row 173 State/Update Identity-Route Probe

## Scope

This is a BayesFilter-owned DPF difference-audit diagnostic. It compares
BayesFilter TF/TFP against the local executable float64 FilterFlow reference
for the row-173 smoothness-gradient mismatch. It does not claim either
implementation is mathematically correct.

Allowed write set:

- `docs/plans/bayesfilter-dpf-filterflow-float64-row-173-state-update-identity-route-*.md`
- `experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_row_173_state_update_identity_route_tf.py`
- `experiments/dpf_implementation/reports/dpf-filterflow-float64-row-173-state-update-identity-route-2026-06-05.md`
- `experiments/dpf_implementation/reports/outputs/dpf_filterflow_float64_row_173_state_update_identity_route_2026-06-05.json`

Forbidden write set:

- production `bayesfilter/`
- `tests/`
- `docs/chapters/`
- `.localsource/filterflow`
- vendored/student/highdim/DSGE/NAWM lanes

## Current Evidence

The accepted downstream-adjoint-route classifier concluded:

- direct full gradient delta:
  `[5.302734403676368, -0.1337765252068337]`;
- local official proposal-likelihood VJPs can be matched, but the local match
  worsens the full gradient gap to `544.9274396565979`;
- the direct residual is reconstructed by `post_update_log_likelihoods`;
- adjacent-boundary evidence shows material state/update adjoint-route deltas:
  `same_tape_post_particles_vjp`, `same_tape_transport_matrix_vjp`,
  `same_tape_identity_residual`, and
  `same_tape_full_recorded_state_residual`.

The next smallest question is whether the state/update identity equations hold
inside each implementation, and whether BayesFilter differs from FilterFlow in
which identity residual is material.

## Evidence Contract

Question:

At row 173 and target time 93, does the BayesFilter-vs-float64-FilterFlow
gradient difference localize to a downstream state/update identity route when
we test the same identity equations inside each side?

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

Tolerance controls:

- `VALUE_TOLERANCE = 5e-8`, inherited from
  `run_filterflow_float64_row_173_vjp_decomposition_tf.py`;
- `GRADIENT_TOLERANCE = 2e-4`, inherited from
  `run_filterflow_float64_row_173_vjp_decomposition_tf.py`;
- an identity residual is `clean` when its within-side `max_abs <= 2e-4`;
- an identity residual is `material` when its within-side `max_abs > 2e-4`.

Primary criterion:

With vetoes clear, rerun the row-173 target-time-93 VJP decomposition and
classify the within-side identity residuals:

- transport identity:
  `pre_particles_adjoint == T^T post_particles_adjoint + VJP(transport_matrix wrt pre_particles)`;
- post-state identity:
  `pre_particles_adjoint == VJP(post_particles wrt pre_particles) + VJP(post_log_weights wrt pre_particles)`;
- full recorded-state identity:
  `pre_particles_adjoint == post-state VJP + carryover VJPs through pre_log_weights, pre_current_log_likelihoods, and log_ess`.

Hypothesis classifications:

- `h1_blocked_or_vetoed`: comparator, CPU, scalar, value, finite, resampling, or
  lane-boundary veto failed.
- `h2_bayesfilter_identity_residual_filterflow_identity_clean`: FilterFlow
  identity residuals are near zero while BayesFilter identity residuals are
  material for at least one identity contract.
- `h3_both_identity_residuals_material`: both sides have material identity
  residuals, so the route is not a BayesFilter-only identity residual relative
  to FilterFlow.
- `h4_identity_residual_not_material_cross_side_vjp_diff`: within-side
  identities are clean, but cross-side VJPs differ.
- `h5_unresolved_identity_route`: evidence is finite and value-valid but does
  not isolate the state/update identity route.

Decision precedence after vetoes clear:

1. If any FilterFlow identity residual is material and any BayesFilter identity
   residual is material, classify `h3_both_identity_residuals_material`.
2. Else if all FilterFlow identity residuals are clean and any BayesFilter
   identity residual is material, classify
   `h2_bayesfilter_identity_residual_filterflow_identity_clean`.
3. Else if all within-side identity residuals are clean but any cross-side VJP
   row among the identity tensors has `max_abs_delta > 2e-4`, classify
   `h4_identity_residual_not_material_cross_side_vjp_diff`.
4. Else classify `h5_unresolved_identity_route`.

Veto diagnostics:

- FilterFlow subprocess cannot execute;
- BayesFilter target-time-93 VJP decomposition cannot execute;
- comparator fingerprint changes during the run;
- CPU-only manifest violation in parent or subprocess;
- scalar mismatch beyond `VALUE_TOLERANCE = 5e-8`;
- value-path mismatch before identity interpretation;
- resampling flags differ;
- required identity tensors are missing or non-finite;
- path-boundary contamination.

Explanatory diagnostics:

- cross-side deltas for each decomposition tensor;
- within-side residual max/sum norms for each identity;
- direct total gradient delta;
- post-update parameter-path residual from the accepted prior artifact;
- boundary-mode rows from the existing VJP harness;
- transport upstream clipping fraction and residuals.

What must not be concluded:

- correctness of FilterFlow or BayesFilter;
- analytic-gradient correctness;
- posterior correctness;
- global smoothness-surface agreement;
- that a code fix is proven;
- production readiness;
- public API readiness;
- monograph, highdim, DSGE, NAWM, or banking/model-risk claims.

Artifact:

`experiments/dpf_implementation/reports/outputs/dpf_filterflow_float64_row_173_state_update_identity_route_2026-06-05.json`

## Skeptical Pre-Execution Audit

- Wrong baseline risk: use only the local executable float64 FilterFlow
  reference, not paper notation, fixed-target Sinkhorn, or upstream source.
- Proxy risk: cross-side adjoint magnitudes are explanatory only; the primary
  test is within-side identity residual behavior.
- Stale-context risk: use target time 93 and row 173, not the older time-1 VJP
  decomposition where total gradients matched despite intermediate VJP deltas.
- Overclaim risk: if BayesFilter identity residuals are material and FilterFlow
  residuals are clean, conclude only a difference-audit localization.
- Stop-condition risk: stop as blocked if required identity tensors or CPU-only
  manifests are missing.
- Runtime risk: one row, one target time, one bounded VJP decomposition.
- Lane risk: do not edit production code, tests, chapters, or FilterFlow source.

Audit status: passed for planning. This is the smallest direct test after the
accepted downstream classifier because it checks the actual identity contracts
nominated by the adjacent-boundary evidence.

## Phase Order

1. Claude Code reviews this plan read-only.
2. Codex audits Claude findings as `ACCEPT`, `PARTIAL`, `DISPUTE`, or
   `CLARIFY` in the review-loop artifact.
3. If accepted, implement the focused identity-route runner.
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
python -m py_compile experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_row_173_state_update_identity_route_tf.py
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_float64_row_173_state_update_identity_route_tf
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_filterflow_float64_row_173_state_update_identity_route_tf --validate-only
python -m json.tool experiments/dpf_implementation/reports/outputs/dpf_filterflow_float64_row_173_state_update_identity_route_2026-06-05.json
rg -n "import numpy|from numpy" experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_row_173_state_update_identity_route_tf.py
rg -n "student|highdim|DSGE|NAWM|\\.localsource" experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_row_173_state_update_identity_route_tf.py
git diff --check -- experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_row_173_state_update_identity_route_tf.py docs/plans/bayesfilter-dpf-filterflow-float64-row-173-state-update-identity-route-plan-2026-06-05.md docs/plans/bayesfilter-dpf-filterflow-float64-row-173-state-update-identity-route-result-2026-06-05.md docs/plans/bayesfilter-dpf-filterflow-float64-row-173-state-update-identity-route-review-loop-2026-06-05.md
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
Read docs/plans/bayesfilter-dpf-filterflow-float64-row-173-state-update-identity-route-plan-2026-06-05.md plus AGENTS.md and CLAUDE.md read-only. Review whether the plan is adequate to test the current row-173 downstream state/update identity-route hypotheses under BayesFilter-vs-local-float64-FilterFlow difference-audit governance. Check evidence contract, exact inputs/outputs, lane boundaries, CPU-only controls, stop conditions, non-conclusions, decision rule, and Claude/Codex finding-classification rules. Output ACCEPT or REJECT first. REJECT only for material missing controls that would invalidate the evidence contract, lane governance, CPU-only policy, exact I/O reproducibility, ordered decision rule, or stated non-conclusions; otherwise ACCEPT. If REJECT, list findings as exact missing required controls. Do not edit files.
```

Result review:

```text
Read docs/plans/bayesfilter-dpf-filterflow-float64-row-173-state-update-identity-route-result-2026-06-05.md, docs/plans/bayesfilter-dpf-filterflow-float64-row-173-state-update-identity-route-plan-2026-06-05.md, docs/plans/bayesfilter-dpf-filterflow-float64-row-173-state-update-identity-route-review-loop-2026-06-05.md, and experiments/dpf_implementation/tf_tfp/runners/run_filterflow_float64_row_173_state_update_identity_route_tf.py read-only. Review whether the result follows the accepted plan, uses the decision rule correctly, preserves difference-audit governance, records exact inputs/fingerprints, lane-boundary and CPU-only controls, and avoids non-concluded claims. Output ACCEPT or REJECT first. REJECT only for material missing controls that would invalidate the evidence contract, lane governance, CPU-only policy, exact I/O reproducibility, ordered decision rule, or stated non-conclusions; otherwise ACCEPT. If REJECT, list findings as exact missing required controls. Do not edit files.
```
