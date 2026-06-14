# Phase 1 Result: Test Stabilization

Date: 2026-06-14

## Status

`PASSED_WITH_REVIEWED_HANDOFF_TO_PHASE_2_PLANNING`

## Phase Objective

Add pytest-sized correctness coverage for experimental batched Kalman and SVD
sigma-point value+score paths without changing production defaults.

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | The experimental batched Kalman and SVD sigma-point value+score paths now have small deterministic pytest correctness coverage before production integration work. |
| Baseline/comparator | Existing scalar production Kalman QR score and scalar SVD sigma-point score APIs row by row. |
| Primary criterion | Passed: required pytest command passed and new SVD tests cover UKF/cubature scalar parity, singleton, row permutation, graph/XLA parity, shape mismatch, and CPU-only visibility. |
| Veto diagnostics | No veto fired. One shape-mismatch test bug was repaired by asserting the actual earlier fail-closed construction boundary. |
| Explanatory diagnostics | TensorFlow/gast deprecation warnings are noisy but non-blocking. |
| Not concluded | No production API readiness, no nonlinear branch coverage beyond affine fixture, no GPU performance claim, no CUT4 readiness, no HMC/NeuTra integration claim. |

## Implementation

Added:

- `tests/test_experimental_batched_svd_sigma_point_tf.py`

The new file is CPU-only and covers:

- scalar-row value+score parity for `tf_svd_ukf` and `tf_svd_cubature`;
- singleton batch parity for both backends;
- row permutation order preservation for both backends;
- eager, `tf.function`, and CPU XLA parity for both backends;
- fail-closed shape mismatch behavior;
- CPU-only GPU hiding.

No production API or default files were modified.

## Required Checks Actually Run

| Check | Command summary | Result |
| --- | --- | --- |
| Phase 1 subplan headings | `rg -n "^## ..."` over Phase 1 subplan | Passed |
| Fixture helper import | `/home/ubuntu/anaconda3/envs/tfgpu/bin/python -c "import docs.benchmarks.benchmark_experimental_batched_svd_sigma_point_cpu_gpu as m; print(m._stable_fixture.__name__)"` | Passed: `_stable_fixture` |
| Scalar cubature authority import | `/home/ubuntu/anaconda3/envs/tfgpu/bin/python -c "from bayesfilter.nonlinear.svd_sigma_point_derivatives_tf import tf_svd_cubature_score; print(tf_svd_cubature_score.__name__)"` | Passed: `tf_svd_cubature_score` |
| First full Phase 1 pytest | `PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES=-1 /home/ubuntu/anaconda3/envs/tfgpu/bin/python -m pytest -q tests/test_experimental_batched_linear_kalman_tf.py tests/test_experimental_batched_svd_sigma_point_tf.py` | Failed: 18 passed, 1 failed due to test expecting failure later than construction |
| Focused repair check | same interpreter, `tests/test_experimental_batched_svd_sigma_point_tf.py` | Passed: `10 passed` |
| Final Phase 1 pytest | same full command over Kalman and SVD test files | Passed: `19 passed` |
| Audit-only source scan | `rg -n "tf_svd_cut4|cut4|CUDA_VISIBLE_DEVICES|jit_compile|row_permutation|singleton|shape_mismatch|tf_svd_cubature" tests/test_experimental_batched_svd_sigma_point_tf.py` | Completed; confirms CPU-only marker, XLA test, row permutation, singleton, shape mismatch, and cubature references. No CUT4 references. |

## Repair Note

Initial shape-mismatch test attempted to build invalid derivative tensors and
then call `tf_batched_svd_sigma_point_value_and_score`.  The experimental
dataclass correctly failed closed during derivative construction with:

`ValueError: d_initial_covariance has shape (3, 2, 2, 2), expected (2, 2, 2, 2)`

The test was repaired to assert this earlier construction-time fail-closed
boundary.  This did not require production edits.

## Claude Review Trail

| Round | Artifact | Verdict | Action |
| ---: | --- | --- | --- |
| 1 | `docs/plans/bayesfilter-batched-filtering-phase-1-claude-review-round-01-2026-06-14.md` | `REVISE` | Patched Phase 1 subplan to make cubature first-class, add cubature authority precheck/stop conditions, and demote `rg` to audit-only. |
| 2 | `docs/plans/bayesfilter-batched-filtering-phase-1-claude-review-round-02-2026-06-14.md` | `AGREE` | Accepted as Phase 1 subplan convergence. |

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| Accept Phase 1 correctness stabilization | Passed: `19 passed` | No veto fired | Tests are affine-fixture only for SVD | Proceed to Phase 2 nonlinear and branch/fail-closed coverage | No production readiness |
| Keep cubature in supported test scope | Passed: cubature scalar parity, singleton, permutation, graph/XLA tests pass | No cubature import/XLA veto | Cubature lacks larger benchmark ladder | Carry cubature into Phase 2 only where nonlinear scalar authority exists | No performance claim |
| Keep CUT4 excluded from default-promotion scope | Passed: no CUT4 test coverage added | No scope creep | Tiny CUT4 remains possible outside default path | Continue excluding CUT4 from promotion gates | No CUT4 readiness |

## Next-Phase Handoff Conditions

Phase 2 may begin only after its subplan exists and is reviewed for:

- consistency with Phase 0 and Phase 1 results;
- nonlinear fixture feasibility;
- branch/fail-closed artifact coverage;
- boundary safety around existing dirty worktree changes;
- no production default change and no CUT4 default-promotion scope.

Phase 2 should focus on non-affine SVD sigma-point value+score parity and
branch/fail-closed diagnostics, not performance.
