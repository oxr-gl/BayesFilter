# P65 Phase 3 Subplan: Bug-Test Closeout And Handoff

metadata_date: 2026-06-15
status: REFRESHED_READY_FOR_PHASE3_PRECHECK
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p65-fixed-branch-rank-capacity-master-program-2026-06-14.md
phase: 3
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Phase Objective

Close out the P65 bug test by separating the repaired zero-TT failure from the
remaining P60 quantitative threshold blockers.  Phase 3 must not turn the
remaining threshold blockers into a pass or claim d=18 correctness.

## Entry Conditions Inherited From Previous Phase

- Phase 2 implementation repair passed focused checks:
  `16 passed` for the focused P59/P60 gate and `12 passed` for the
  supplemental shared-fitter regression.
- Phase 2 result identifies exact changed behavior and preserved invariants.
- The pinned comparator now has positive high square-root mass and no high
  defensive-only steps.
- The pinned comparator still returns
  `BLOCK_P60_D18_SAME_ROUTE_RANK_CONVERGENCE` due
  `log_marginal_delta_threshold_exceeded` and
  `normalizer_increment_delta_threshold_exceeded`.

## Required Artifacts

- Phase 3 result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p65-phase3-bug-test-closeout-result-2026-06-14.md`.
- Updated visible execution ledger.
- Final stop handoff:
  `docs/plans/bayesfilter-highdim-zhao-cui-p65-visible-stop-handoff-2026-06-14.md`.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the Phase 2 implementation close the high-rank defensive-only zero-TT bug while honestly preserving the residual P60 threshold blockers? |
| Baseline/comparator | P64 failing result with high defensive-only steps `[1,2]`; Phase 2 repaired comparator with high defensive-only steps `[]` and positive high square-root normalizers. |
| Primary pass criterion | Closeout result states `P65_FIXED_BRANCH_ZERO_TT_REPAIR_PASSED_WITH_RESIDUAL_THRESHOLD_BLOCKERS`, focused checks remain green, zero-TT repair evidence is preserved, and residual threshold blockers are explicitly carried forward. |
| Veto diagnostics | Defensive-only high branch returns; thresholds weakened; target/order/axes changed; artificial fit data; nonfinite values; source claims unsupported; focused tests fail; residual threshold blockers hidden or called a full pass. |
| Explanatory diagnostics | Normalizer decomposition, log marginal deltas, normalizer increment deltas, ESS, clipping diagnostics, rank/degree/count settings. |
| Not concluded | No paper-scale correctness, no d=50/d=100 success, no adaptive parity, no HMC readiness. |

## Required Checks/Tests/Reviews

- Repaired comparator JSON probe preserving:
  - high square-root normalizers;
  - high defensive-only steps;
  - high core norm ranges and near-zero counts;
  - source invariants;
  - residual P60 blockers.
- Focused P60 test file:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q \
  tests/highdim/test_p60_author_sir_rank_comparator.py
```

- Focused P59/P60 test set:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q \
  tests/highdim/test_p59_author_sir_36d_target_fit.py \
  tests/highdim/test_p59_author_sir_step_spec_assembly.py \
  tests/highdim/test_p60_author_sir_rank_comparator.py
```

- Bounded Claude review of the closeout result.

## Forbidden Claims/Actions

- Do not promote beyond the phase evidence.
- Do not hide residual blockers.
- Do not call a blocker a pass because one metric improved.
- Do not weaken or reinterpret the P60 log-marginal or normalizer-increment
  thresholds.
- Do not claim that fixed-HMC constant-path initialization is an unqualified
  source-faithful Zhao--Cui operation.

## Exact Next-Phase Handoff Conditions

This is a closeout phase.  End with one of:

- `P65_FIXED_BRANCH_RANK_CAPACITY_REPAIR_PASSED_FOCUSED_BUG_TEST`;
- `P65_FIXED_BRANCH_ZERO_TT_REPAIR_PASSED_WITH_RESIDUAL_THRESHOLD_BLOCKERS`;
- `P65_FIXED_BRANCH_RANK_CAPACITY_REPAIR_BLOCKED_LOCALIZED`;
- `P65_FIXED_BRANCH_RANK_CAPACITY_REPAIR_INCONCLUSIVE`.

## Stop Conditions

- Required focused tests fail and fix would require new scope.
- Claude identifies an unresolved material closeout overclaim after five rounds.
- Runtime exceeds visible execution budget without a discriminating artifact.

## End-Of-Subplan Protocol

1. Run required local checks.
2. Write Phase 3 result.
3. Write final visible stop handoff.
4. Record what is not concluded and the safest next action.
