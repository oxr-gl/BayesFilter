# Phase 7A Repair Subplan: Model-C Structural Fixed-Support Value/Score Branch Alignment

Date: 2026-07-01

## Status

`DRAFT_PENDING_REVIEW`

## Phase Objective

Repair the model-C structural fixed-support value/score branch-alignment defect
that blocked broad Phase 7 score admission, using the structural deterministic-
completion discipline from Chapter 18b and preserving all current nonclaims.

## Entry Conditions Inherited From Previous Phase

- Phase 7 blocked with token:
  `GENERIC_NSSM_PHASE7_BLOCKED_PENDING_MODEL_C_STRUCTURAL_FIXED_SUPPORT_VALUE_SCORE_ALIGNMENT`.
- The reviewed issue is that the score-side structural fixed-support branch and
  the value-side finite-difference comparator are not yet uniformly aligned for
  the reviewed model-C approximate lane.
- No broad score admission, HMC readiness, top-level API promotion, or
  production/default claim is authorized.

## Required Artifacts

- repair result:
  `docs/plans/bayesfilter-generic-nonlinear-ssm-likelihood-gradient-phase7a-model-c-structural-fixed-support-repair-result-2026-07-01.md`
- refreshed Phase 7 gradient result or refreshed Phase 8 final-decision subplan,
  depending on the repair outcome
- focused repair surfaces:
  - `tests/test_nonlinear_sigma_point_scores_tf.py`
  - optionally `bayesfilter/testing/nonlinear_diagnostics_tf.py` if value-side
    branch metadata or dispatch needs explicit structural fixed-support handling
- visible execution ledger:
  `docs/plans/bayesfilter-generic-nonlinear-ssm-likelihood-gradient-visible-execution-ledger-2026-07-01.md`
- Claude review ledger:
  `docs/plans/bayesfilter-generic-nonlinear-ssm-likelihood-gradient-claude-review-ledger-2026-07-01.md`
- stop handoff if the repair re-blocks

## Required Checks/Tests/Reviews

Allowed repair actions are limited to the smallest seam needed to align the
value-side comparator with the reviewed structural fixed-support score branch.

Allowed local checks:

```bash
rg -n "_model_c_structural_fixed_support_value|allow_fixed_null_support|structural_fixed_support_no_active_floor|blocked_active_floor" tests/test_nonlinear_sigma_point_scores_tf.py bayesfilter/testing/nonlinear_diagnostics_tf.py bayesfilter/nonlinear/svd_sigma_point_derivatives_tf.py
git diff --check -- docs/plans/bayesfilter-generic-nonlinear-ssm-likelihood-gradient-phase7a-model-c-structural-fixed-support-repair-*.md tests/test_nonlinear_sigma_point_scores_tf.py bayesfilter/testing/nonlinear_diagnostics_tf.py
```

Focused repair runtime must stay CPU-only and is limited to the exact reviewed
node set:

```bash
CUDA_VISIBLE_DEVICES=-1 pytest -q \
  tests/test_nonlinear_sigma_point_scores_tf.py::test_model_c_default_structural_fixed_support_score_matches_finite_difference \
  tests/test_nonlinear_sigma_point_scores_tf.py::test_model_c_default_zero_phase_variance_blocks_smooth_score_branch \
  tests/test_nonlinear_sigma_point_scores_tf.py::test_model_c_structural_fixed_support_blocks_positive_placement_floor \
  tests/test_nonlinear_sigma_point_scores_tf.py::test_model_c_structural_fixed_support_blocks_moving_null_covariance \
  tests/test_nonlinear_sigma_point_scores_tf.py::test_svd_sigma_point_analytic_score_matches_finite_difference \
  tests/test_svd_sigma_point_branch_diagnostics_tf.py::test_default_model_c_structural_fixed_support_score_branch_summary_passes \
  tests/test_svd_sigma_point_branch_diagnostics_tf.py::test_default_model_c_structural_fixed_support_diagnostics
```

Required read-only Claude reviews:

- this repair subplan,
- the repair result,
- and the next refreshed handoff artifact.

No benchmark, HMC, top-level API, production, release, CI, or default-policy
command is authorized in this repair phase.

## Skeptical Plan Audit

| Risk Checked | Phase 7A Control |
| --- | --- |
| Wrong baseline | The repair is anchored to the reviewed Phase 7 blocker and Chapter 18b structural deterministic-completion logic. |
| Proxy metric promoted | A passing narrow comparator repair does not by itself justify broader lane promotion beyond the reviewed claim level. |
| Missing stop condition | If the repaired comparator still leaves the declared branch on either side, the lane remains blocked. |
| Unfair comparison | The model-C approximate lane remains approximate-only; no exact-target reinterpretation is allowed. |
| Hidden assumption | The repair must keep the score-side structural fixed-support branch and align the value comparator to it, not vice versa by silent widening. |
| Stale context | The repair may not reopen lane taxonomy or generic support policy. |
| Environment mismatch | This is a narrow CPU-only repair/test phase. |
| Artifact-answer mismatch | The phase must yield a specific repaired same-branch comparator outcome or a re-blocked result, not general program conclusions. |

Audit status: executable only after this repair subplan is reviewed closed.
The reviewed repair result then determines whether the blocker is closed or
preserved.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the model-C structural fixed-support value-side finite-difference comparator be aligned with the reviewed score-side structural fixed-support branch so the Phase 7 same-branch contract is meaningful for the intended approximate lane? |
| Baseline/comparator | current blocked Phase 7 result, Chapter 18b structural deterministic-completion doctrine, current model-C score-side fixed-support branch behavior, and the current value-side comparator helper. |
| Primary criterion | The repair passes only if the value-side comparator and score-side branch are the same declared structural fixed-support branch for the reviewed approximate lane, or if the reviewed lane is explicitly narrowed to the passing subset without semantic drift. |
| Veto diagnostics | comparator still leaves the declared branch, wrong-target reinterpretation, silent narrowing without explicit reviewed wording, or promotion beyond the approximate-lane claim level. |
| Explanatory diagnostics | focused pytest node outcomes, branch/failure labels, and comparator helper notes. |
| Not concluded | No exact-target gradient claim for model C, no HMC readiness, no top-level API promotion, and no production/default claim. |
| Artifact | reviewed repair result and refreshed downstream handoff artifact. |

## Forbidden Claims/Actions

- Do not reopen exact-target versus surrogate-target policy.
- Do not broaden the repair beyond the minimal model-C structural fixed-support
  value/score seam.
- Do not promote model C to exact-target gradient evidence.
- Do not run runtime commands outside the exact reviewed repair node set.

## Exact Next-Phase Handoff Conditions

Phase 7 may be reopened only if:

- the repair result receives Claude `VERDICT: AGREE`;
- the value-side comparator is explicitly aligned to the reviewed structural
  fixed-support branch, or the lane is explicitly narrowed to the passing
  subset with preserved nonclaims;
- the execution ledger records the repaired branch-alignment status and the
  exact lane scope still admitted.

If the repair does not close the branch mismatch, the next handoff must be a
reviewed blocked closeout rather than a reopened score-admission phase.

## Stop Conditions

- The value-side comparator cannot be aligned without changing the declared lane
  semantics.
- The repaired route still leaves the declared branch on either side.
- Focused repair checks fail and cannot be repaired within the reviewed scope.
- Claude review does not converge after five rounds for the same issue.
- Continuing would require broader runtime authority than the reviewed repair
  scope provides.

## End-Of-Phase Requirements

1. Apply the smallest code/test repair that targets the model-C structural
   fixed-support value/score alignment seam.
2. Run the reviewed focused repair nodes.
3. Write the repair result.
4. Refresh the downstream handoff artifact.
5. Review the repair result and refreshed handoff artifact.
6. Update the execution ledger and Claude review ledger.
