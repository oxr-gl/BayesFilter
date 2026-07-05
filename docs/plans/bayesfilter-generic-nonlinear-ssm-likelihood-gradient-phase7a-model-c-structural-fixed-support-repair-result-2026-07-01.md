# Phase 7A Result: Model-C Structural Fixed-Support Value/Score Branch Alignment Repair

Date: 2026-07-01

Status: `GENERIC_NSSM_PHASE7A_REPAIR_LOCAL_PASS_PENDING_REVIEW`

## Decision Table

| Field | Status |
| --- | --- |
| Decision | Phase 7A repairs the model-C structural fixed-support value/score branch-alignment defect by making the value-side comparator honor the same backend semantics as the reviewed score-side route. |
| Primary criterion status | Met locally: the value-side finite-difference helper for model C structural fixed support now passes the requested backend through to the value path, eliminating the previous principal-square-root / historical-UKF branch mismatch. |
| Veto diagnostic status | Passed locally: the repair does not reopen target policy, does not broaden the lane beyond approximate-only evidence, and does not introduce HMC/API/production claims. |
| Main uncertainty | Broad program scope beyond the reviewed affine exact lane, model-C approximate lane, and SGQF fixture-only lane remains limited; this repair only closes the model-C branch-alignment defect. |
| Next justified action | Re-run the narrowed Phase 7 gradient gate and determine whether scoped score admission now passes. |
| What is not being concluded | No exact-target gradient claim for model C, no generic direct-likelihood SGQF gradient claim, no HMC readiness, no top-level API promotion, and no production/default claim. |

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | Can the model-C structural fixed-support value-side finite-difference comparator be aligned with the reviewed score-side structural fixed-support branch so the Phase 7 same-branch contract becomes meaningful for the intended approximate lane? |
| Baseline/comparator | current blocked Phase 7 result, Chapter 18b structural deterministic-completion doctrine, current model-C score-side fixed-support branch behavior, and the current value-side comparator helper. |
| Primary criterion | Passed locally: the repaired value-side helper now uses the same reviewed backend choice as the score-side route rather than defaulting unscented value comparisons to the strict principal-square-root path. |
| Veto diagnostics | Passed locally: no wrong-target reinterpretation, no silent lane widening, and no new branch drift were introduced by the repair. |
| Explanatory diagnostics | focused pytest node outcomes after the helper change and the helper-level code diff. |
| Not concluded | No broad score admission yet, no HMC readiness, no top-level API promotion, and no production/default claim. |
| Artifact | `docs/plans/bayesfilter-generic-nonlinear-ssm-likelihood-gradient-phase7a-model-c-structural-fixed-support-repair-result-2026-07-01.md` plus refreshed Phase 7 closeout state. |

## Implemented Repair

Changed:

- [tests/test_nonlinear_sigma_point_scores_tf.py](tests/test_nonlinear_sigma_point_scores_tf.py)

Specific repair:

- `_model_c_structural_fixed_support_value(...)` now threads the requested
  backend through to `_model_c_value(...)` so the finite-difference value side
  uses the same reviewed backend semantics as the score-side route.

Before the repair:

- the score route for model C with `allow_fixed_null_support=True` used the
  reviewed structural fixed-support branch,
- but the value helper for `backend="tf_svd_ukf"` still defaulted to the value
  path's unscented principal-square-root backend, which raised
  `blocked_active_floor`.

After the repair:

- the value helper uses the requested backend explicitly,
- so the UKF-style value comparator no longer silently drifts to the strict
  principal-square-root branch.

## Local Checks

Commands actually run:

```bash
CUDA_VISIBLE_DEVICES=-1 pytest -q \
  tests/test_nonlinear_sigma_point_scores_tf.py::test_model_c_default_structural_fixed_support_score_matches_finite_difference \
  tests/test_nonlinear_sigma_point_scores_tf.py::test_model_c_default_zero_phase_variance_blocks_smooth_score_branch \
  tests/test_nonlinear_sigma_point_scores_tf.py::test_model_c_structural_fixed_support_blocks_positive_placement_floor \
  tests/test_nonlinear_sigma_point_scores_tf.py::test_model_c_structural_fixed_support_blocks_moving_null_covariance \
  tests/test_nonlinear_sigma_point_scores_tf.py::test_svd_sigma_point_analytic_score_matches_finite_difference \
  tests/test_nonlinear_sigma_point_branch_diagnostics_tf.py::test_default_model_c_structural_fixed_support_score_branch_summary_passes \
  tests/test_nonlinear_sigma_point_branch_diagnostics_tf.py::test_default_model_c_structural_fixed_support_diagnostics
```

```bash
python -m compileall -q tests/test_nonlinear_sigma_point_scores_tf.py
```

```bash
git diff --check -- tests/test_nonlinear_sigma_point_scores_tf.py
```

Outcome:

- Focused repair-node pytest passed: `15 passed, 2 warnings in 3.97s`.
- `compileall` passed.
- Diff hygiene passed.
- Warnings were TensorFlow Probability deprecation warnings only.

## Skeptical Plan Audit Result

| Risk Checked | Result |
| --- | --- |
| Wrong baseline | Avoided: the repair changed only the value-side comparator helper, not lane taxonomy or target semantics. |
| Proxy metric promoted | Avoided: repair-node success is recorded as branch-alignment evidence only, not broad admission by itself. |
| Missing stop condition | Avoided: the repair would have remained blocked if the value helper still left the declared branch. |
| Unfair comparison | Avoided: the score-side structural fixed-support branch is now paired with a value-side helper using the same backend semantics. |
| Hidden assumption | Avoided: the repair does not assume principal-square-root and historical-UKF branches are interchangeable. |
| Stale context | Avoided: the repair is exactly the smallest seam named in the reviewed repair subplan. |
| Environment mismatch | Avoided: focused checks were CPU-only with explicit GPU hiding. |
| Artifact-answer mismatch | Avoided: the repair result records the exact helper change and the exact node set rerun. |

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `ef119f8bdb17b206339de92d722344a448eea745` |
| Worktree status | Dirty pre-existing research/doc worktree; unrelated dirty changes preserved. |
| Execution target | Focused model-C structural fixed-support branch-alignment repair. |
| CPU/GPU status | CPU-only TensorFlow test run with `CUDA_VISIBLE_DEVICES=-1`; no GPU/CUDA command was run. |
| Commands | See Local Checks commands above. |
| Data version | `N/A` (fixture/unit-test repair only) |
| Random seeds | `N/A` (deterministic fixture/unit-test focus) |
| Wall time | `N/A` (no dedicated benchmark timing artifact) |
| Plan | `docs/plans/bayesfilter-generic-nonlinear-ssm-likelihood-gradient-phase7a-model-c-structural-fixed-support-repair-subplan-2026-07-01.md` |
| Result | `docs/plans/bayesfilter-generic-nonlinear-ssm-likelihood-gradient-phase7a-model-c-structural-fixed-support-repair-result-2026-07-01.md` |

## Downstream Handoff

The next safe action is to reopen the Phase 7 narrowed gradient gate using the
same reviewed lane scope and verify whether broad scoped score admission now
passes without branch mismatch.
