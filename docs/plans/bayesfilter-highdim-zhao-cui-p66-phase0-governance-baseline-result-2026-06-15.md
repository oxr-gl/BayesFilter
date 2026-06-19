# P66 Phase 0 Result: Governance, Baseline, And Planning Basis

metadata_date: 2026-06-15
status: PASS_P66_PHASE0_BASELINE_READY_FOR_VALIDATION_CONTRACT
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p66-fixed-branch-validation-ladder-master-program-2026-06-15.md
phase: 0
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Decision

Phase 0 passed.

The fresh local baseline is the CPU-only reproduction of the P65 sentinel state
under the pinned tuple and source-route invariants: the high `(degree=1,
rank=2)` branch is noncollapsed, while the old P60 low/high comparison remains
visible as explanatory sentinel evidence.

This result establishes the planning basis for Phase 1.  It does not prove
scientific correctness and does not implement the replacement validation
ladder.

## Checks

Compile/import check:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q \
  bayesfilter/highdim/source_route.py \
  bayesfilter/highdim/fitting.py \
  bayesfilter/highdim/__init__.py \
  tests/highdim/test_p60_author_sir_rank_comparator.py
```

Result: passed.

Fresh CPU-only pinned-tuple probe:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -c '<exact P66 Phase 0 JSON probe>'
```

CPU-only was intentional and recorded before framework import:
`CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp`.

TensorFlow emitted CUDA-registration/cuInit chatter despite CPU-only settings.
This is not GPU evidence and is not relevant to the Phase 0 logic baseline.

## Probe Result

| Quantity | Value |
| --- | --- |
| P66 Phase 0 status candidate | `WARN_SENTINEL_BRANCH_DIFFERS_FROM_CANDIDATE` |
| P60 status | `BLOCK_P60_D18_SAME_ROUTE_RANK_CONVERGENCE` |
| P60 blockers | `log_marginal_delta_threshold_exceeded`, `normalizer_increment_delta_threshold_exceeded` |
| High square-root normalizers | `[1.2197182121566172, 1.6339670649545497]` |
| High defensive-only steps | `[]` |
| High core norm ranges | `[(0.999999534045549, 1.1044090586950472), (0.9999991709641398, 1.2782685463795218)]` |
| High near-zero core counts | `[0, 0]` |
| Log marginal absolute delta | `12.324659904904365` |
| Normalizer increment absolute deltas | `[1.4032241181382403, 10.921435786766125]` |

Thresholds preserved in the old P60 diagnostic:

- log marginal absolute delta threshold: `5.0`;
- normalizer increment absolute delta threshold: `5.0`;
- probe log-density median absolute delta threshold: `10.0`;
- retained log-density median absolute delta threshold: `10.0`.

Source-route invariants preserved:

- route: `Zhao-Cui full_sol`;
- realized target: `[x_t, x_{t-1}]`;
- target dimension: `36`;
- previous marginal keep axes: `0..17`;
- previous marginal input axes: `18..35`.

## Interpretation

The old low/high P60 comparison remains visible and remains large.  P66 treats
that fact as sentinel/explanatory evidence, not as a primary convergence veto
for this target.  The low `(degree=0, rank=1)` branch is too crude to be a fair
primary convergence baseline for the first nontrivial high branch
`(degree=1, rank=2)`.

The high branch remains admissible under the P65 zero-TT repair evidence.  This
is a precondition for later validation, not convergence evidence.

## What Is Not Concluded

- No code was changed by Phase 0.
- No replacement validation ladder is implemented yet.
- No d=18 correctness claim.
- No d=50/d=100 scaling claim.
- No adaptive Zhao--Cui parity claim.
- No HMC production readiness claim.

## Phase 1 Handoff

Phase 1 may launch after review.  It must produce a reviewed validation
contract and API design before implementation.

Phase 1 must define:

- exact statuses and result schema;
- source-route invariant gate;
- admissibility/noncollapse preconditions;
- old P60 sentinel payload;
- sample-adequacy formula as permission-to-diagnose;
- adjacent-ladder comparison invariants;
- rank ladder `(degree=1, rank=2)` versus `(degree=1, rank=3)`;
- degree ladder `(degree=1, rank=2)` versus `(degree=2, rank=2)`;
- focused test plan for Phase 2.

Phase 1's artifact is a reviewed contract/schema/policy note.  It is not an
experiment result, implementation evidence, convergence evidence, or
correctness evidence.
