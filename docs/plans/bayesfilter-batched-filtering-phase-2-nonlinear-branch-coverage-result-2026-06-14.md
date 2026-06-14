# Phase 2 Result: Nonlinear Branch Coverage

Date: 2026-06-14

## Status

`PASSED_WITH_REVIEWED_HANDOFF_TO_PHASE_3_PLANNING`

## Phase Objective

Extend correctness coverage from affine SVD sigma-point fixtures to a small
non-affine batched nonlinear fixture, and add fail-closed branch diagnostics for
the experimental batched SVD sigma-point value+score path.

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | The experimental batched SVD sigma-point value+score path preserves scalar authority parity and fail-closed branch behavior on a small non-affine Model B fixture. |
| Baseline/comparator | Existing scalar production Model B SVD-UKF/cubature score APIs row by row; existing scalar nonlinear finite-difference tests; Phase 1 affine batched SVD tests. |
| Primary criterion | Passed: required pytest commands passed; new nonlinear batched tests cover UKF/cubature eager scalar parity, row permutation, and fail-closed branch diagnostics. |
| Veto diagnostics | No veto fired. |
| Explanatory diagnostics | Optional graph/XLA diagnostic is present in the test file and skips if unavailable; TensorFlow/gast warnings remain noisy but non-blocking. |
| Not concluded | No production API readiness, no broad nonlinear accuracy claim beyond tiny Model B fixture, no GPU performance claim, no CUT4 readiness, no HMC/NeuTra integration claim. |

## Implementation

Added:

- `tests/test_experimental_batched_svd_sigma_point_nonlinear_tf.py`

The new test file defines a local batch-native Model B nonlinear accumulation
wrapper and compares it row by row against scalar production APIs:

- `tf_svd_ukf_score`
- `tf_svd_cubature_score`

Fixture constants are identical between scalar and batched laws:

- `alpha = 0.55`
- `observation_sigma = 0.30`
- parameter vector `theta = (rho, sigma, beta)`

No production API or default files were modified.

## Required Checks Actually Run

| Check | Command summary | Result |
| --- | --- | --- |
| Phase 2 subplan headings | `rg -n "^## ..."` over Phase 2 subplan | Passed |
| Scalar nonlinear authority import | `CUDA_VISIBLE_DEVICES=-1 /home/ubuntu/anaconda3/envs/tfgpu/bin/python -c "..."; print('ok')` | Passed: `ok` |
| Phase 1 SVD test precheck | `PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES=-1 /home/ubuntu/anaconda3/envs/tfgpu/bin/python -m pytest -q tests/test_experimental_batched_svd_sigma_point_tf.py` | Passed: `10 passed` |
| Phase 2 nonlinear + affine SVD tests | `PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES=-1 /home/ubuntu/anaconda3/envs/tfgpu/bin/python -m pytest -q tests/test_experimental_batched_svd_sigma_point_tf.py tests/test_experimental_batched_svd_sigma_point_nonlinear_tf.py` | Passed: `19 passed` |
| Scalar nonlinear authority subset | `PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES=-1 /home/ubuntu/anaconda3/envs/tfgpu/bin/python -m pytest -q tests/test_nonlinear_sigma_point_scores_tf.py -k "model_b_analytic_score_matches_finite_difference or model_c_default_structural_fixed_support_score_matches_finite_difference"` | Passed: `6 passed, 12 deselected` |
| Audit-only source scan | `rg -n "make_nonlinear_accumulation|tf_svd_cut4|blocked_active_floor|blocked_weak_spectral_gap|jit_compile|row_permutation|CUDA_VISIBLE_DEVICES" tests/test_experimental_batched_svd_sigma_point_nonlinear_tf.py` | Completed; expected labels found; no `tf_svd_cut4` reference. |

## Branch Diagnostics

The nonlinear batched test asserts fail-closed diagnostics on the experimental
batched value+score path:

- `placement_floor=10.0` raises an error containing `blocked_active_floor`;
- `spectral_gap_tolerance=10.0` raises an error containing
  `blocked_weak_spectral_gap`.

These are branch/fail-closed correctness checks, not performance or production
readiness evidence.

## Claude Review Trail

| Round | Artifact | Verdict | Action |
| ---: | --- | --- | --- |
| 1 | `docs/plans/bayesfilter-batched-filtering-phase-2-claude-review-round-01-2026-06-14.md` | `REVISE` | Patched CPU-hidden precheck, branch triggers, fixture-constant recording, and graph/XLA status. |
| 2 | `docs/plans/bayesfilter-batched-filtering-phase-2-claude-review-round-02-2026-06-14.md` | `REVISE` | Demoted graph parity as well as CPU-XLA to explanatory diagnostics. |
| 3 | `docs/plans/bayesfilter-batched-filtering-phase-2-claude-review-round-03-2026-06-14.md` | `AGREE` | Accepted as Phase 2 subplan convergence. |

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| Accept Phase 2 nonlinear coverage | Passed: required commands passed | No veto fired | Coverage is one tiny Model B fixture | Proceed to Phase 3 non-default interface candidate | No production readiness |
| Carry UKF/cubature as supported candidates | Passed for tiny nonlinear parity | No scalar parity veto | Larger nonlinear and branch grids not tested | Keep conditional scope in interface design | No broad nonlinear claim |
| Keep graph/XLA as diagnostic for nonlinear fixture | Diagnostic present, not a gate | N/A | Graph/XLA behavior may matter in later integration | Revisit in Phase 3/4 as integration/performance evidence | No compiled default claim |
| Keep CUT4 excluded | Passed: no CUT4 default-scope tests added | No scope creep | Tiny CUT4 remains outside this program | Continue excluding CUT4 from default-promotion gates | No CUT4 readiness |

## Next-Phase Handoff Conditions

Phase 3 may begin only after its subplan exists and is reviewed for:

- consistency with Phase 0-2 results;
- non-default API/interface boundary safety;
- no public export/default change without explicit approval;
- scalar fallback behavior;
- artifact coverage and tests;
- dirty-worktree preservation.

Phase 3 should design and implement a non-default interface candidate or adapter
that lets callers use batched value+score deliberately, without changing package
defaults.
