# P65 Phase 2 Result: Fixed-Branch Zero-TT Repair

metadata_date: 2026-06-15
status: PASSED_ZERO_TT_REPAIR_WITH_RESIDUAL_P60_THRESHOLD_BLOCKERS
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p65-fixed-branch-rank-capacity-master-program-2026-06-14.md
phase: 2
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Decision

Phase 2 repaired the localized target
`BLOCK_P65_HIGH_RANK_FIXED_ALS_ZERO_SQRT_TT`.

The high `(degree=1, rank=2)` fixed branch no longer collapses to a
defensive-only transport under the pinned P64/P60 tuple.  The overall P60
same-route rank comparator still blocks on quantitative threshold deltas, so
this result is a Phase 2 repair handoff only, not a d=18 correctness result.

## Changed Behavior

- `FixedTTFitter.fit` now accepts an explicit `initialization_rule` and records
  it in the fixed-branch manifest and diagnostics.
- The P59/P60 fixed-TTSIRT source-route path uses the documented constant-path
  initialization:
  - first constant channel equals the weighted mean of the positive
    square-root target values;
  - later constant channels equal one;
  - all other TT entries are zero.
- The fixed-variant metadata is emitted as:
  - `fixed_branch_adaptation_class = fixed_hmc_adaptation`;
  - `fit_initialization_rule = fixed_hmc_constant_path_weighted_mean`.
- P60 manifests now include square-root TT core diagnostics for low and high
  candidates.

## Changed Files

- `bayesfilter/highdim/fitting.py`
- `bayesfilter/highdim/source_route.py`
- `bayesfilter/highdim/__init__.py`
- `tests/highdim/test_p60_author_sir_rank_comparator.py`
- `docs/plans/bayesfilter-highdim-zhao-cui-p50-chapter-discipline-rewrite-2026-06-12.tex`
- `docs/plans/bayesfilter-highdim-zhao-cui-p65-visible-execution-ledger-2026-06-14.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p65-claude-review-ledger-2026-06-14.md`

## Evidence

Compile check:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q \
  bayesfilter/highdim/source_route.py \
  bayesfilter/highdim/fitting.py \
  bayesfilter/highdim/__init__.py \
  tests/highdim/test_p60_author_sir_rank_comparator.py
```

Result: passed.

Focused P59/P60 test gate:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q \
  tests/highdim/test_p59_author_sir_36d_target_fit.py \
  tests/highdim/test_p59_author_sir_step_spec_assembly.py \
  tests/highdim/test_p60_author_sir_rank_comparator.py
```

Result: `16 passed, 2 warnings in 765.23s`.

Supplemental shared-fitter regression:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q \
  tests/highdim/test_fixed_branch_fit.py
```

Result: `12 passed, 2 warnings in 3.34s`.

Repaired JSON probe for the pinned tuple reported:

| Quantity | Value |
| --- | --- |
| High square-root normalizers | `[1.2197182121566172, 1.6339670649545497]` |
| High defensive-only steps | `[]` |
| High core norm ranges | `[(0.999999534045549, 1.1044090586950472), (0.9999991709641398, 1.2782685463795218)]` |
| High near-zero core counts | `[0, 0]` |
| Adaptation class | `fixed_hmc_adaptation` |
| Initialization rule | `fixed_hmc_constant_path_weighted_mean` |

Preserved source-route invariants in the probe:

- target dimension `36`;
- realized target `[x_t, x_{t-1}]`;
- previous marginal keep axes `0..17`;
- previous marginal input axes `18..35`;
- defensive `tau = 1e-8`;
- P60 thresholds were not weakened.

## Residual Blockers

The repaired pinned comparator still returns
`BLOCK_P60_D18_SAME_ROUTE_RANK_CONVERGENCE` with:

- `log_marginal_delta_threshold_exceeded`;
- `normalizer_increment_delta_threshold_exceeded`.

These are Phase 3 closeout blockers.  They must not be hidden, renamed as a
pass, or resolved by weakening thresholds.

## Review

Math documentation and source-anchor review converged before implementation:

- Claude P50 documentation review R2: `VERDICT: AGREE`.
- MathDevMCP extracted the relevant labels and returned broad derivation
  diagnostics as `unverified` because the obligation is not fully formalized;
  this is not a formal proof certificate.

Implementation review:

- Claude Phase 2 implementation review R1: `VERDICT: AGREE`.

Claude accepted the bounded implementation as a Phase 2 repair, with the same
qualification recorded here: residual P60 threshold blockers remain real Phase
3 work.

## What Is Not Concluded

- No d=18 correctness claim.
- No d=50 or d=100 scaling claim.
- No adaptive Zhao--Cui parity claim.
- No HMC production readiness claim.
- No proof that constant-path initialization is uniquely necessary.

## Next Handoff

Advance to Phase 3 only as a closeout phase for the distinction between:

- the fixed high-rank zero-TT repair, which passed; and
- the remaining P60 quantitative threshold blockers, which remain open.
