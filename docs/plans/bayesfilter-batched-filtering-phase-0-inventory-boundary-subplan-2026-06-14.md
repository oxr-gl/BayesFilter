# Phase 0 Subplan: Inventory And Boundary Audit

Date: 2026-06-14

## Status

`READY_FOR_LOCAL_CHECK_AND_REVIEW`

## Phase Objective

Confirm the current state of the batched filtering experimental work, record the
boundary between existing dirty/unrelated work and this program, verify that the
master program/runbook artifacts are internally consistent, and draft the Phase
1 subplan for correctness-focused pytest stabilization.

## Entry Conditions Inherited From Previous Phase

- User requested a master program with phase subplans, read-only Claude review,
  visible execution, and a repair loop.
- Existing experimental batched Kalman and SVD sigma-point files may be
  untracked and must not be overwritten casually.
- Existing unrelated dirty worktree changes must be preserved.
- No production default change is authorized.
- Claude may review only; Codex remains supervisor and executor.

## Required Artifacts

- Master program:
  `docs/plans/bayesfilter-batched-filtering-production-default-master-program-2026-06-14.md`
- Visible runbook:
  `docs/plans/bayesfilter-batched-filtering-visible-gated-execution-runbook-2026-06-14.md`
- Execution ledger:
  `docs/plans/bayesfilter-batched-filtering-visible-execution-ledger-2026-06-14.md`
- Phase 0 result:
  `docs/plans/bayesfilter-batched-filtering-phase-0-inventory-boundary-result-2026-06-14.md`
- Phase 1 subplan draft:
  `docs/plans/bayesfilter-batched-filtering-phase-1-test-stabilization-subplan-2026-06-14.md`
- Claude review artifact:
  `docs/plans/bayesfilter-batched-filtering-claude-review-round-01-2026-06-14.md`

## Required Checks, Tests, And Reviews

Local checks:

1. Verify required headings exist in the master program, runbook, and Phase 0
   subplan with `rg`.
2. Verify the declared Python/TensorFlow environment is usable:
   `/home/ubuntu/anaconda3/envs/tfgpu/bin/python -c "import sys, tensorflow as tf; print(sys.executable); print(tf.__version__)"`.
   A missing interpreter, TensorFlow import failure, or unexpected executable is
   a Phase 0 blocker unless a reviewed fallback is written before execution.
3. Verify the current evidence baseline quantitatively:
   - cited artifact files exist;
   - SVD-UKF `B=20,T=200,n=m=10` parity artifact reports `passed=true`,
     max absolute value error no larger than `2e-13`, and max absolute score
     error no larger than `5e-13`;
   - compiled GPU timing artifacts for `B=20`, `B=256`, and `B=4096` exist and
     record `jit_compile=true`;
   - Kalman parity artifacts for `B=200` and `B=4096` exist and report
     `passed=true`.
4. Verify the experimental SVD sigma-point module has no obvious Python
   time-loop patterns in the JIT-critical recursion with:
   `rg -n "for t in range\\(|range\\(n_timesteps\\)" bayesfilter/nonlinear/experimental_batched_svd_sigma_point_tf.py`
   and treat any match as a Phase 0 blocker unless it is clearly in a comment
   explaining the prior repair.
   This grep is only a cheap proxy; it must be paired with the live SVD smoke
   check below and may not be treated as complete proof of graph-native control
   flow.
5. Record `git status --short` to preserve dirty-worktree boundaries.
6. Inventory relevant batched artifacts with `rg --files docs/benchmarks | rg "experimental-batched-(kalman|svd)"`.
7. Run a CPU-only smoke test for existing experimental Kalman tests:
   `PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES=-1 /home/ubuntu/anaconda3/envs/tfgpu/bin/python -m pytest -q tests/test_experimental_batched_linear_kalman_tf.py`.
8. Run a tiny CPU-only live SVD-UKF parity smoke, not a benchmark:
   `PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES=-1 /home/ubuntu/anaconda3/envs/tfgpu/bin/python docs/benchmarks/benchmark_experimental_batched_svd_sigma_point_cpu_gpu.py --mode parity --backend tf_svd_ukf --batch-size 3 --time-steps 5 --state-dim 2 --obs-dim 2 --parameter-dim 2 --rows all --device-scope cpu --device /CPU:0 --expect-device-kind cpu --output docs/benchmarks/experimental-batched-svd-ukf-phase0-smoke-b3-t5-n2-m2-2026-06-14.json`.

Review:

- Ask Claude Opus max effort for read-only review of the master program,
  runbook, and Phase 0 subplan by path only.
- If Claude requests revision and the issue is fixable, patch the same subplan
  or master/runbook visibly and rerun focused checks.
- Stop after five review rounds for the same blocker.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Are the visible gated program, runbook, and Phase 0 execution boundary coherent enough to start correctness stabilization? |
| Baseline/comparator | User instructions, current experimental artifacts, existing scalar production APIs, and repo scientific coding policy. |
| Primary pass criterion | Local checks pass, Claude review returns `VERDICT: AGREE`, Phase 0 result records inventory/boundaries, and Phase 1 subplan is drafted and consistency-reviewed. |
| Veto diagnostics | Missing required headings; missing/mismatched Python/TensorFlow environment; missing or stale cited baseline artifact; unresolved Python time loop in experimental SVD recursion; failed Kalman or SVD smoke test not classed as unrelated; Claude/Codex nonconvergence after five rounds; any attempted default change. |
| Explanatory diagnostics | Dirty worktree inventory, artifact inventory, older eager GPU timing artifacts, and known benchmark gaps. |
| Not concluded | No production readiness, no nonlinear correctness expansion, no GPU performance conclusion, no HMC/NeuTra integration claim. |
| Artifact preserving result | Phase 0 result file and visible execution ledger. |

## Forbidden Claims And Actions

- Do not change production defaults.
- Do not run GPU benchmarks in Phase 0.
- Do not claim SVD-UKF nonlinear correctness beyond existing affine parity.
- Do not claim the no-loop grep proves graph-native/JIT safety by itself.
- Do not include CUT4 in default scope.
- Do not send whole files to Claude; use path-based review prompts.
- Do not let Claude edit files or authorize execution.
- Do not revert or overwrite unrelated dirty worktree changes.

## Exact Next-Phase Handoff Conditions

Advance to Phase 1 only if:

- Phase 0 local checks pass or any failures are documented as non-blocking with
  a reviewed rationale;
- the quantitative baseline claims in the master program are either validated
  or explicitly downgraded;
- Claude review converges with `VERDICT: AGREE`;
- Phase 0 result is written;
- Phase 1 subplan exists and includes objective, inherited entry conditions,
  artifacts, checks/reviews, evidence contract, forbidden claims/actions,
  handoff conditions, and stop conditions;
- Phase 1 subplan is reviewed for consistency, correctness, feasibility,
  artifact coverage, and boundary safety.

## Stop Conditions

Stop and write a blocker result if:

- local checks reveal the current experimental SVD path still contains a Python
  time loop in the JIT-critical filtering recursion;
- the declared Python/TensorFlow environment is missing or cannot import the
  required modules;
- cited evidence artifacts are missing or disagree with the master program and
  cannot be corrected before execution;
- the existing Kalman smoke test fails for reasons that invalidate the current
  experimental baseline;
- the tiny SVD-UKF live smoke fails for reasons that invalidate the current
  experimental baseline;
- Claude review does not converge after five rounds for the same material
  blocker;
- continuing would require package installation, network fetch, credentials,
  destructive git/filesystem actions, GPU trusted execution, or a production
  default change before the reviewed plan reaches the relevant phase;
- current dirty worktree changes make it impossible to isolate this program's
  edits safely.

## End-Of-Phase Procedure

1. Run the required local checks.
2. Write the Phase 0 result / close record.
3. Draft or refresh the Phase 1 subplan.
4. Review the Phase 1 subplan for consistency, correctness, feasibility,
   artifact coverage, and boundary safety.
5. If the Phase 1 subplan is material, send it to Claude as read-only review
   before execution.
