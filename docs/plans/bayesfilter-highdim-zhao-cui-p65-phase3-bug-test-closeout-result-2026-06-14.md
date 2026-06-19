# P65 Phase 3 Result: Bug-Test Closeout And Handoff

metadata_date: 2026-06-15
status: P65_FIXED_BRANCH_ZERO_TT_REPAIR_PASSED_WITH_RESIDUAL_THRESHOLD_BLOCKERS
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p65-fixed-branch-rank-capacity-master-program-2026-06-14.md
phase: 3
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Decision

The Phase 2 constant-path fixed-branch adaptation closes the localized
high-rank defensive-only zero-TT bug under the pinned P64/P60 tuple.

The P60 same-route rank-convergence comparator is not a full pass.  It still
returns `BLOCK_P60_D18_SAME_ROUTE_RANK_CONVERGENCE` because the quantitative
log-marginal and normalizer-increment threshold blockers remain.

## Evidence

Focused P60 closeout test:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q \
  tests/highdim/test_p60_author_sir_rank_comparator.py
```

Result: `7 passed, 2 warnings in 420.17s`.

Focused P59/P60 closeout test set:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q \
  tests/highdim/test_p59_author_sir_36d_target_fit.py \
  tests/highdim/test_p59_author_sir_step_spec_assembly.py \
  tests/highdim/test_p60_author_sir_rank_comparator.py
```

Result: `16 passed, 2 warnings in 742.55s`.

JSON closeout probe:

| Quantity | Value |
| --- | --- |
| Closeout status | `P65_FIXED_BRANCH_ZERO_TT_REPAIR_PASSED_WITH_RESIDUAL_THRESHOLD_BLOCKERS` |
| P60 status | `BLOCK_P60_D18_SAME_ROUTE_RANK_CONVERGENCE` |
| P60 blockers | `log_marginal_delta_threshold_exceeded`, `normalizer_increment_delta_threshold_exceeded` |
| High square-root normalizers | `[1.2197182121566172, 1.6339670649545497]` |
| High defensive-only steps | `[]` |
| High core norm ranges | `[(0.999999534045549, 1.1044090586950472), (0.9999991709641398, 1.2782685463795218)]` |
| High near-zero core counts | `[0, 0]` |
| Adaptation class | `fixed_hmc_adaptation` |
| Initialization rule | `fixed_hmc_constant_path_weighted_mean` |

Residual quantitative deltas:

| Quantity | Value | Threshold |
| --- | ---: | ---: |
| Log marginal absolute delta | `12.324659904904365` | `5.0` |
| Normalizer increment absolute delta, step 1 | `1.4032241181382403` | `5.0` |
| Normalizer increment absolute delta, step 2 | `10.921435786766125` | `5.0` |

Preserved source-route invariants:

- target dimension `36`;
- realized target `[x_t, x_{t-1}]`;
- previous marginal keep axes `0..17`;
- previous marginal input axes `18..35`;
- source-route label in the probe: `Zhao-Cui full_sol`.

## Interpretation

The original high-rank branch failure was that the fitted square-root TT had
zero or near-zero resolved mass, so the transport became defensive-only.  That
specific failure is now gone: both high-branch steps have positive square-root
mass, no defensive-only steps, and no near-zero core counts under the declared
diagnostic tolerance.

The remaining P60 blockers are different.  They say the low and high fixed
branches still disagree too much in the rank-comparator metrics.  They are not
evidence that the zero-TT repair failed, and they are also not evidence that
d=18 correctness has been achieved.

## What Is Not Concluded

- No d=18 correctness claim.
- No paper-scale Zhao--Cui reproduction claim.
- No d=50 or d=100 scaling claim.
- No adaptive Zhao--Cui parity claim.
- No HMC production readiness claim.
- No permission to weaken P60 thresholds.

## Recommended Next Action

Start a new scoped phase or plan for the residual P60 threshold blockers.  The
first question should be whether the remaining deltas are caused by the
expected difference between low `(degree=0, rank=1)` and high `(degree=1,
rank=2)` fixed branches, by the tiny fixed sample design, or by another
implementation defect.
