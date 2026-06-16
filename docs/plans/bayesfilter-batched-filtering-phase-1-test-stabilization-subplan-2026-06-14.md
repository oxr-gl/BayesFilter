# Phase 1 Subplan: Test Stabilization

Date: 2026-06-14

## Status

`READY_FOR_LOCAL_CHECK_AND_REVIEW`

## Phase Objective

Add pytest-sized correctness coverage for the experimental batched filtering
value+score paths without changing production defaults.  Kalman correctness
coverage already exists and must be rerun as part of the phase.  SVD
sigma-point coverage must be added in a new test file for the batched
SVD-UKF and SVD-cubature paths, using scalar production value+score APIs as the
authority row by row.  Cubature receives its first batched pytest coverage in
this phase; Phase 0 did not provide a separate cubature quantitative artifact.

## Entry Conditions Inherited From Previous Phase

- Phase 0 passed with Claude round-2 `VERDICT: AGREE`.
- Phase 0 validated the current quantitative baseline artifacts:
  SVD-UKF `B=20,T=200,n=m=10` scalar parity, Kalman `B=200`/`B=4096`
  selected-row parity, and SVD-UKF compiled GPU artifacts with
  `jit_compile=true`.
- Phase 0 live CPU smokes passed for Kalman pytest coverage and a tiny SVD-UKF
  parity run.
- The worktree remains dirty with unrelated modified/untracked files.  This
  phase must preserve them.
- No production default change is authorized.
- GPU benchmarking is not authorized in Phase 1.

## Required Artifacts

- New SVD sigma-point test file:
  `tests/test_experimental_batched_svd_sigma_point_tf.py`
- Phase 1 result:
  `docs/plans/bayesfilter-batched-filtering-phase-1-test-stabilization-result-2026-06-14.md`
- Phase 2 subplan draft:
  `docs/plans/bayesfilter-batched-filtering-phase-2-nonlinear-branch-coverage-subplan-2026-06-14.md`
- Claude review artifact for this subplan:
  `docs/plans/bayesfilter-batched-filtering-phase-1-claude-review-round-01-2026-06-14.md`
- Additional review rounds only if material revisions are required.

## Required Checks, Tests, And Reviews

Pre-execution local checks:

1. Verify this subplan contains all required headings.
2. Verify no production files are planned for editing in this phase.
3. Verify the SVD benchmark fixture helpers can be imported without running a
   CLI action:
   `/home/ubuntu/anaconda3/envs/tfgpu/bin/python -c "import docs.benchmarks.benchmark_experimental_batched_svd_sigma_point_cpu_gpu as m; print(m._stable_fixture.__name__)"`.
4. Verify scalar SVD-cubature authority is importable before implementation:
   `/home/ubuntu/anaconda3/envs/tfgpu/bin/python -c "from bayesfilter.nonlinear.svd_sigma_point_derivatives_tf import tf_svd_cubature_score; print(tf_svd_cubature_score.__name__)"`.

Implementation:

1. Add `tests/test_experimental_batched_svd_sigma_point_tf.py`.
2. Keep the file CPU-only with `os.environ.setdefault("CUDA_VISIBLE_DEVICES",
   "-1")` before TensorFlow import.
3. Reuse the benchmark harness's affine fixture helpers instead of duplicating
   the fixture.
4. Add tests for:
   - SVD-UKF and SVD-cubature value+score scalar-row parity for `B=3`,
     `T=5`, `state_dim=2`, `obs_dim=2`, `parameter_dim=2`;
   - singleton batch parity for SVD-UKF and SVD-cubature;
   - row permutation order preservation for SVD-UKF and SVD-cubature;
   - eager, `tf.function`, and CPU XLA parity for SVD-UKF and SVD-cubature;
   - shape mismatch fail-closed behavior for model/derivative batch mismatch;
   - CPU-only device visibility.

Required test commands:

1. `PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES=-1 /home/ubuntu/anaconda3/envs/tfgpu/bin/python -m pytest -q tests/test_experimental_batched_linear_kalman_tf.py tests/test_experimental_batched_svd_sigma_point_tf.py`

Audit-only command:

1. `rg -n "tf_svd_cut4|cut4|CUDA_VISIBLE_DEVICES|jit_compile|row_permutation|singleton|shape_mismatch|tf_svd_cubature" tests/test_experimental_batched_svd_sigma_point_tf.py`

The `rg` audit is not a correctness gate.  It is used only to summarize whether
expected test labels and forbidden CUT4/default-scope terms are visible in the
new test file.

Review:

- Claude Opus max effort must review this subplan read-only before execution.
- If Claude requests revision and the issue is fixable, patch this subplan
  visibly and rerun focused subplan checks.
- Stop after five review rounds for the same material blocker.
- Claude is not an execution authority.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the experimental batched Kalman and SVD sigma-point value+score paths be covered by small deterministic pytest correctness tests before any production integration work? |
| Baseline/comparator | Existing scalar production Kalman QR score and scalar SVD sigma-point score APIs row by row; existing Kalman tests; Phase 0 artifact baseline. |
| Primary pass criterion | Required pytest command passes, new SVD tests cover UKF/cubature scalar parity, singleton, row permutation, graph/XLA parity, shape mismatch, and CPU-only visibility. |
| Veto diagnostics | Test failure not explained as unrelated; nonfinite outputs; scalar parity mismatch; XLA compile failure for the tiny SVD-UKF or cubature tests; missing/unsafe scalar cubature authority; GPU visible during CPU-only tests; editing production/default files; CUT4 included in default-promotion test scope. |
| Explanatory diagnostics | Test runtime, TensorFlow warnings, exact max parity residuals, and import warnings. |
| Not concluded | No production API readiness, no nonlinear branch coverage beyond affine fixture, no GPU performance claim, no CUT4 readiness, no HMC/NeuTra integration claim. |
| Artifact preserving result | Phase 1 result file plus the new test file and pytest output summary. |

## Forbidden Claims And Actions

- Do not modify production APIs or defaults.
- Do not benchmark GPU or use eager GPU timing.
- Do not add CUT4 to default-promotion coverage.
- Do not claim nonlinear model correctness from the affine fixture tests.
- Do not overwrite unrelated dirty files.
- Do not use Claude to edit or approve execution.

## Exact Next-Phase Handoff Conditions

Advance to Phase 2 only if:

- Claude review of this subplan converges with `VERDICT: AGREE`;
- the required Phase 1 tests pass;
- the Phase 1 result file records the exact commands and outcomes;
- Phase 2 subplan exists and includes objective, inherited entry conditions,
  artifacts, checks/reviews, evidence contract, forbidden claims/actions,
  handoff conditions, and stop conditions;
- Phase 2 subplan has been reviewed for consistency, correctness, feasibility,
  artifact coverage, and boundary safety.

## Stop Conditions

Stop and write a blocker result if:

- the SVD fixture helpers cannot be imported safely;
- scalar SVD-cubature authority cannot be imported or used safely;
- the new SVD tests require editing production files before correctness
  coverage can be expressed;
- required tests fail for a reason that invalidates the experimental baseline;
- cubature cannot satisfy the planned scalar parity or graph/XLA contract
  without production edits;
- CPU-only tests see a visible GPU;
- Claude review does not converge after five rounds for the same material
  blocker;
- continuing would require package installation, network access, GPU trusted
  execution, destructive git/filesystem action, production default changes, or
  modifying unrelated dirty worktree changes.

## End-Of-Phase Procedure

1. Run the required local checks.
2. Write the Phase 1 result / close record.
3. Draft or refresh the Phase 2 subplan.
4. Review the Phase 2 subplan for consistency, correctness, feasibility,
   artifact coverage, and boundary safety.
5. Send material Phase 2 subplan questions to Claude as read-only review before
   execution.
