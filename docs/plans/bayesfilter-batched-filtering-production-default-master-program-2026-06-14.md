# Batched Filtering Production Default Master Program

Date: 2026-06-14

## Status

`COMPLETED_FILTERING_LANE_CORRECTED`

## Purpose

Move the batched filtering value+score work from isolated experimental
evidence toward a filtering production-candidate decision for workloads that
evaluate many parameter proposals against one observation sequence, including
MLE and other likelihood/score consumers.

This program does **not** authorize changing a production default.  It builds
the evidence, interfaces, tests, and benchmark artifacts needed for a final
human default-readiness decision.

## Current Evidence Baseline

- Experimental batched Kalman value+score exists in
  `bayesfilter/linear/experimental_batched_kalman_tf.py`.
- Experimental batched SVD sigma-point value+score exists in
  `bayesfilter/nonlinear/experimental_batched_svd_sigma_point_tf.py`.
- Kalman parity artifacts exist for `B=200` and `B=4096` on selected rows.
- SVD-UKF parity exists for `B=20`, `T=200`, `state_dim=10`,
  `obs_dim=10`, `parameter_dim=2`, with max absolute value error
  `1.7053e-13` and max absolute score error `4.5475e-13`.
- SVD-UKF compiled GPU timing exists after replacing the experimental Python
  time loop with `tf.while_loop`.
- CUT4 is out of default scope because its `2q + 2^q` point count is
  unsuitable for realistic batched GPU use at the target dimensions.

Phase 0 must revalidate this baseline by checking the cited artifact files and
recorded quantitative fields before later phases may rely on it.  If a cited
artifact is missing, malformed, or inconsistent with the baseline claims, Phase
0 must either patch this baseline downward or stop with a blocker result.

## Program Evidence Contract

| Field | Contract |
| --- | --- |
| Engineering question | Can batched-over-parameters filtering value+score become a filtering production candidate for supported Kalman and SVD sigma-point workloads? |
| Baseline/comparator | Existing scalar production value+score APIs row-by-row; current experimental batched artifacts; scalar-loop CPU baselines for performance. |
| Primary pass criterion | Every phase produces required artifacts, passes declared local checks, preserves scalar parity, and reaches a reviewed handoff without unsupported default or scientific claims. |
| Promotion veto diagnostics | Scalar parity failure; nonfinite outputs; JIT/XLA incompatibility in supported target paths; wrong device placement for GPU benchmarks; missing result artifacts; unresolved Claude/Codex review disagreement after five rounds; production default change requiring human approval. |
| Explanatory diagnostics | Warm-call timing, compile time, memory/capacity observations, per-filter seconds, and branch summaries. |
| Not concluded | No unconditional production default, no CUT4 readiness, no broad nonlinear accuracy claim beyond tested fixtures, no HMC/NeuTra readiness, and no posterior scientific claim from filtering microbenchmarks alone. |
| Required artifacts | Phase subplans, phase results, Claude read-only reviews, visible execution ledger, benchmark JSON/MD artifacts, final handoff. |

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| Keep time sequential but batch parameter proposals | User question and existing experimental design | Filtering recursion is sequential in time, but parameter proposals/chains are independent | Hidden coupling or row-order error | Row permutation and scalar-row parity tests | hypothesis |
| Combine value and score | MLE, optimization, HMC, NeuTra, and surrogate consumers may need both at each proposal | Reuses sigma points, factorizations, residuals, and derivative intermediates | API becomes too narrow for value-only users | Provide value-only wrapper or documented adapter | hypothesis |
| JIT-only GPU benchmark rule | User direction | Eager GPU timing is misleading for these kernels | Accidentally promotes eager placement smoke as speed evidence | Benchmark harness must fail closed unless compiled or explicitly smoke-only | reviewed |
| Exclude CUT4 from default scope | CUT4 point count grows as `2q + 2^q` | Target `q=20` implies `1,048,616` points per step | Missing a niche small-dimensional CUT4 win | Keep optional tiny CUT4 diagnostics outside default promotion | reviewed |
| Promote conditionally, not unconditionally | Existing project policy and current evidence | Different models/derivative providers have different JIT and branch behavior | Overbroad default breaks unsupported models | Phase 6 default-readiness gate requires human approval | reviewed |

## Phase Index

| Phase | Name | Objective | Subplan | Result |
| ---: | --- | --- | --- | --- |
| 0 | Inventory And Boundary Audit | Confirm artifacts, boundaries, current gaps, and next subplan readiness. | `docs/plans/bayesfilter-batched-filtering-phase-0-inventory-boundary-subplan-2026-06-14.md` | `docs/plans/bayesfilter-batched-filtering-phase-0-inventory-boundary-result-2026-06-14.md` |
| 1 | Test Stabilization | Add pytest-sized batched Kalman/SVD sigma-point correctness coverage without production default changes. | `docs/plans/bayesfilter-batched-filtering-phase-1-test-stabilization-subplan-2026-06-14.md` | `docs/plans/bayesfilter-batched-filtering-phase-1-test-stabilization-result-2026-06-14.md` |
| 2 | Nonlinear Branch Coverage | Add nonlinear and branch/fail-closed coverage for batched SVD sigma-point score. | `docs/plans/bayesfilter-batched-filtering-phase-2-nonlinear-branch-coverage-subplan-2026-06-14.md` | `docs/plans/bayesfilter-batched-filtering-phase-2-nonlinear-branch-coverage-result-2026-06-14.md` |
| 3 | Production Interface Candidate | Design and implement a non-default production-facing adapter/API candidate. | `docs/plans/bayesfilter-batched-filtering-phase-3-interface-candidate-subplan-2026-06-14.md` | `docs/plans/bayesfilter-batched-filtering-phase-3-interface-candidate-result-2026-06-14.md` |
| 4 | Compiled Benchmark Ladder | Run JIT-only CPU/GPU benchmark ladder with scalar-loop comparators. | `docs/plans/bayesfilter-batched-filtering-phase-4-compiled-benchmark-ladder-subplan-2026-06-14.md` | `docs/plans/bayesfilter-batched-filtering-phase-4-compiled-benchmark-ladder-result-2026-06-14.md` |
| 5 | Consumer Boundary Audit | Historical HMC/static-unroll consumer-boundary check; superseded as a filtering promotion gate by Phase 6 correction. | `docs/plans/bayesfilter-batched-filtering-phase-5-downstream-harness-subplan-2026-06-14.md` | `docs/plans/bayesfilter-batched-filtering-phase-5-downstream-harness-result-2026-06-14.md` |
| 6 | Filtering-Lane Readiness Decision | Produce the corrected filtering production-candidate recommendation and explicit nonclaims. | `docs/plans/bayesfilter-batched-filtering-phase-6-default-readiness-subplan-2026-06-14.md` | `docs/plans/bayesfilter-batched-filtering-phase-6-default-readiness-result-2026-06-14.md` |

## Phase Gate Summary

### Phase 0: Inventory And Boundary Audit

Pass only if the current experimental files and artifacts are identified, the
dirty worktree boundary is recorded, no production files are modified, and Phase
1 has a reviewed subplan.

### Phase 1: Test Stabilization

Pass only if pytest-sized Kalman and SVD-UKF/cubature batched tests cover
scalar-row parity, singleton batch, row permutation, graph parity, and CPU XLA
parity.  GPU benchmarking is forbidden in this phase.

### Phase 2: Nonlinear Branch Coverage

Pass only if non-affine fixture coverage and fail-closed branch diagnostics are
tested against scalar authority paths.  This phase may reject default-readiness
while still preserving the research direction.

### Phase 3: Production Interface Candidate

Pass only if a non-default production-facing API or adapter candidate exists,
uses the repo's established interfaces where feasible, and preserves scalar
fallback behavior.  It must not become the package default.

### Phase 4: Compiled Benchmark Ladder

Pass only if all GPU comparisons are JIT/XLA compiled, device placement is
trusted, scalar-loop and batched CPU/GPU comparators are recorded, like-for-like
scalar GPU comparators are included where feasible, and compile time is
separated from warm-call timing.  If a scalar GPU comparator is infeasible, the
result must explain why and must not present batched GPU timing as a broad GPU
speedup claim against a weaker CPU-only scalar baseline.

### Phase 5: Consumer Boundary Audit

Historical note: Phase 5 exercised an HMC/static-unroll value+score consumer
boundary.  This was later identified as the wrong gate for filtering production
readiness.  It is preserved as audit trail only and must not promote or block
filtering.  HMC/NeuTra validation belongs in separate consumer-lane plans.

### Phase 6: Filtering-Lane Readiness Decision

Pass only if a final decision table separates filtering correctness,
performance evidence, filtering API/default policy, and nonclaims.  Changing a
default requires explicit human approval after this phase.

## Cross-Agent Review Contract

Codex is the supervisor and executor.

Claude Opus with max effort is a read-only reviewer only.  Claude must not edit
files, run experiments, launch agents, authorize boundary crossing, change
claims, or approve production defaults.

Claude review prompts must reference plan/result paths and bounded excerpts or
questions; they must not paste whole files.  If Claude does not respond, Codex
must run a small probe.  If the probe responds, Codex must treat the failed
review as a prompt-design problem and revise the prompt.

For each material subplan or blocker, Codex loops Claude review until
`VERDICT: AGREE`, a nonfixable blocker appears, or five rounds are reached for
the same blocker.

## Anticipated Human/Trusted Approvals

- Claude Code worker invocations for read-only review require trusted
  execution.
- GPU detection, initialization, and compiled GPU benchmark commands require
  trusted execution.
- Package installation, network fetch, credentials, destructive filesystem
  operations, git commits, or production default changes are not authorized by
  this program and require separate human approval.

## Forbidden Claims And Actions

- Do not claim production readiness before Phase 6.
- Do not change a production default without explicit human approval.
- Do not use eager GPU timing as CPU/GPU benchmark evidence.
- Do not include CUT4 in default promotion.
- Do not overwrite existing production files for convenience.
- Do not revert unrelated dirty worktree changes.
- Do not let Claude execute or authorize implementation.

## Final Handoff Requirements

The final handoff must list:

- final phase reached;
- status and blockers;
- result artifacts;
- Claude review trail;
- local tests and benchmarks actually run;
- unresolved numerical, performance, API, and default-policy gaps;
- what was not concluded;
- exact next human decision required.
