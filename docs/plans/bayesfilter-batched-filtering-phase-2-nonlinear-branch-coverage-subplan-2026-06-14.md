# Phase 2 Subplan: Nonlinear Branch Coverage

Date: 2026-06-14

## Status

`READY_FOR_LOCAL_CHECK_AND_REVIEW`

## Phase Objective

Extend correctness coverage from affine SVD sigma-point fixtures to a small
non-affine batched nonlinear fixture, and add fail-closed branch diagnostics for
the experimental batched SVD sigma-point value+score path.  Phase 2 remains
CPU-only and correctness-focused; it does not run GPU benchmarks or change any
production default.

## Entry Conditions Inherited From Previous Phase

- Phase 0 passed with validated baseline artifacts and reviewed boundaries.
- Phase 1 passed with `19 passed` CPU-only tests covering experimental batched
  Kalman plus affine batched SVD-UKF/cubature value+score parity, singleton,
  row permutation, graph/XLA parity, shape mismatch, and CPU-only visibility.
- Phase 1 added `tests/test_experimental_batched_svd_sigma_point_tf.py`.
- Existing scalar nonlinear score tests in
  `tests/test_nonlinear_sigma_point_scores_tf.py` provide Model B/C scalar
  authority and finite-difference checks.
- Existing nonlinear fixtures live in
  `bayesfilter/testing/nonlinear_models_tf.py`.
- Existing unrelated dirty worktree changes must be preserved.
- No production default change is authorized.
- CUT4 remains outside default-promotion scope.

## Required Artifacts

- New nonlinear batched test file:
  `tests/test_experimental_batched_svd_sigma_point_nonlinear_tf.py`
- Phase 2 result:
  `docs/plans/bayesfilter-batched-filtering-phase-2-nonlinear-branch-coverage-result-2026-06-14.md`
- Phase 3 subplan draft:
  `docs/plans/bayesfilter-batched-filtering-phase-3-interface-candidate-subplan-2026-06-14.md`
- Claude review artifact for this subplan:
  `docs/plans/bayesfilter-batched-filtering-phase-2-claude-review-round-01-2026-06-14.md`
- Additional review rounds only if material revisions are required.

## Required Checks, Tests, And Reviews

Pre-execution local checks:

1. Verify this subplan contains all required headings.
2. Verify the scalar nonlinear authority paths import:
   `CUDA_VISIBLE_DEVICES=-1 /home/ubuntu/anaconda3/envs/tfgpu/bin/python -c "from bayesfilter.testing import make_nonlinear_accumulation_model_tf, make_nonlinear_accumulation_first_derivatives_tf, model_b_observations_tf; from bayesfilter.nonlinear.svd_sigma_point_derivatives_tf import tf_svd_ukf_score, tf_svd_cubature_score; print('ok')"`.
3. Verify Phase 1 tests still pass before adding nonlinear coverage:
   `PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES=-1 /home/ubuntu/anaconda3/envs/tfgpu/bin/python -m pytest -q tests/test_experimental_batched_svd_sigma_point_tf.py`.

Implementation:

1. Add `tests/test_experimental_batched_svd_sigma_point_nonlinear_tf.py`.
2. Keep the file CPU-only with `os.environ.setdefault("CUDA_VISIBLE_DEVICES",
   "-1")` before TensorFlow import.
3. Implement a tiny batch-native Model B wrapper in the test file, mirroring
   `make_nonlinear_accumulation_model_tf` and
   `make_nonlinear_accumulation_first_derivatives_tf` for theta
   `(rho, sigma, beta)` with fixed `alpha=0.55` and fixed
   `observation_sigma=0.30`.
   - The scalar authority calls must use the same `alpha=0.55` and
     `observation_sigma=0.30`.
   - The Phase 2 result must record these constants and state that scalar and
     batched laws use identical fixture semantics.
4. Compare batched nonlinear SVD-UKF and SVD-cubature value+score against
   scalar production `tf_svd_ukf_score` and `tf_svd_cubature_score` row by row
   for a small `B=2` parameter grid.
5. Add row permutation preservation for the nonlinear fixture.
6. Add graph and CPU-XLA parity as explanatory diagnostics if they compile
   within the tiny shape, but do not make graph or CPU-XLA success a Phase 2
   pass criterion.  If graph or CPU-XLA fails while eager scalar parity and
   branch diagnostics pass, record it as a Phase 3/4 integration risk rather
   than weakening the Phase 2 nonlinear parity/branch result.
7. Add fail-closed branch diagnostics:
   - active placement floor must be triggered by calling the experimental
     batched value+score path with `placement_floor=10.0`, and the assertion
     target must be the raised TensorFlow error message containing
     `blocked_active_floor`;
   - weak spectral gap must be triggered by calling the experimental batched
     value+score path with `spectral_gap_tolerance=10.0`, and the assertion
     target must be the raised TensorFlow error message containing
     `blocked_weak_spectral_gap`;
   - both branch assertions must target the experimental batched value+score
     path, not a local placeholder wrapper or source-text label check;
   - nonfinite or invalid outputs are not swallowed.

Required test commands:

1. `PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES=-1 /home/ubuntu/anaconda3/envs/tfgpu/bin/python -m pytest -q tests/test_experimental_batched_svd_sigma_point_tf.py tests/test_experimental_batched_svd_sigma_point_nonlinear_tf.py`
2. `PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES=-1 /home/ubuntu/anaconda3/envs/tfgpu/bin/python -m pytest -q tests/test_nonlinear_sigma_point_scores_tf.py -k "model_b_analytic_score_matches_finite_difference or model_c_default_structural_fixed_support_score_matches_finite_difference"`

Audit-only command:

1. `rg -n "make_nonlinear_accumulation|tf_svd_cut4|blocked_active_floor|blocked_weak_spectral_gap|jit_compile|row_permutation|CUDA_VISIBLE_DEVICES" tests/test_experimental_batched_svd_sigma_point_nonlinear_tf.py`

The `rg` audit is not a correctness gate.  It summarizes expected labels and
confirms CUT4 is not added to default-promotion coverage.

Review:

- Claude Opus max effort must review this subplan read-only before execution.
- If Claude requests revision and the issue is fixable, patch this subplan
  visibly and rerun focused subplan checks.
- Stop after five review rounds for the same material blocker.
- Claude is not an execution authority.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the experimental batched SVD sigma-point value+score path preserve scalar authority parity and fail-closed branch behavior on a small non-affine nonlinear fixture? |
| Baseline/comparator | Existing scalar production Model B SVD-UKF/cubature score APIs row by row; existing scalar nonlinear score finite-difference tests; Phase 1 affine batched SVD tests. |
| Primary pass criterion | Required pytest commands pass, new nonlinear batched tests cover UKF/cubature eager scalar parity, row permutation, and fail-closed branch diagnostics. |
| Veto diagnostics | Scalar nonlinear parity mismatch; nonfinite outputs; fail-closed branch errors not raised on the experimental batched path; GPU visible during CPU-only tests; needing production edits to express the nonlinear wrapper; fixture-constant mismatch between scalar and batched laws; CUT4 included in default-promotion scope. |
| Explanatory diagnostics | Exact parity residuals, TensorFlow warnings, optional graph parity, optional CPU-XLA outcome, and branch diagnostic message text. |
| Not concluded | No production API readiness, no broad nonlinear accuracy claim beyond Model B tiny fixture, no GPU performance claim, no CUT4 readiness, no HMC/NeuTra integration claim. |
| Artifact preserving result | Phase 2 result file plus the new nonlinear test file and pytest output summary. |

## Forbidden Claims And Actions

- Do not modify production APIs or defaults.
- Do not benchmark GPU or use eager GPU timing.
- Do not add CUT4 to default-promotion coverage.
- Do not claim broad nonlinear correctness from a tiny Model B fixture.
- Do not change pass/fail criteria after seeing results.
- Do not overwrite unrelated dirty files.
- Do not use Claude to edit or approve execution.

## Exact Next-Phase Handoff Conditions

Advance to Phase 3 only if:

- Claude review of this subplan converges with `VERDICT: AGREE`;
- the required Phase 2 tests pass;
- the Phase 2 result file records exact commands, outcomes, repairs, and
  remaining nonlinear limitations;
- Phase 3 subplan exists and includes objective, inherited entry conditions,
  artifacts, checks/reviews, evidence contract, forbidden claims/actions,
  handoff conditions, and stop conditions;
- Phase 3 subplan has been reviewed for consistency, correctness, feasibility,
  artifact coverage, and boundary safety.

## Stop Conditions

Stop and write a blocker result if:

- scalar nonlinear authority paths cannot be imported or used safely;
- a batch-native Model B test wrapper cannot be expressed without production
  edits;
- scalar parity fails for UKF or cubature and the failure is not clearly a test
  construction bug;
- fail-closed active-floor or weak-gap diagnostics do not fire as expected;
- scalar and batched fixture constants or semantics cannot be shown identical;
- CPU-only tests see a visible GPU;
- Claude review does not converge after five rounds for the same material
  blocker;
- continuing would require package installation, network access, GPU trusted
  execution, destructive git/filesystem action, production default changes, or
  modifying unrelated dirty worktree changes.

## End-Of-Phase Procedure

1. Run the required local checks.
2. Write the Phase 2 result / close record.
3. Draft or refresh the Phase 3 subplan.
4. Review the Phase 3 subplan for consistency, correctness, feasibility,
   artifact coverage, and boundary safety.
5. Send material Phase 3 subplan questions to Claude as read-only review before
   execution.
