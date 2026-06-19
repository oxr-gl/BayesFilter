# P66 Phase 2 Result: Implementation And Focused Tests

metadata_date: 2026-06-15
status: REVIEWED_ACCEPTED_FOR_PHASE3_CLOSEOUT
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p66-fixed-branch-validation-ladder-master-program-2026-06-15.md
phase: 2
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Decision

Phase 2 implemented the reviewed P66 fixed-branch validation-ladder schema and
focused tests.  The old P60 low/high comparator remains callable and unchanged
as historical/sentinel evidence.

The implementation does not execute adjacent rank or degree ladders and does
not claim adjacent-ladder stability.  It implements schema/status rows,
fit-budget resolution, sample-adequacy gates, source-invariant gates,
candidate admissibility gates, and sentinel payload preservation.

## Changed Files

- `bayesfilter/highdim/source_route.py`
  - added P66 statuses;
  - added `P66AuthorSIRFixedBranchValidationLadderResult`;
  - added `p66_fixed_branch_sample_adequacy`;
  - added `p66_fixed_branch_fit_budget_resolution`;
  - added `p66_author_sir_fixed_branch_validation_ladder`;
  - added P66 manifest, invariant, comparison, schema-only ladder, and result
    helpers.
- `bayesfilter/highdim/__init__.py`
  - exported P66 statuses, result type, and functions.
- `tests/highdim/test_p66_author_sir_fixed_branch_validation_ladder.py`
  - added focused P66 contract/unit tests.

## Implemented Contract Points

- Old P60 low/high deltas are preserved as sentinel evidence with
  `interpretation = "explanatory_sentinel_not_primary_gate"`.
- P66 does not weaken old P60 thresholds.
- Candidate `(degree=1, rank=2)` admissibility/noncollapse is represented as a
  precondition/veto gate, not correctness evidence.
- Sample adequacy is represented as permission-to-diagnose, not convergence.
- Fit-budget defaults resolve to:
  - candidate `(degree=1, rank=2)`: `16`;
  - rank ladder `(degree=1, rank=3)`: `36`;
  - degree ladder `(degree=2, rank=2)`: `24`.
- Adjacent rank and degree ladder rows are schema-only unless a later reviewed
  experiment executes them.
- Unauthorized source-route invariant drift blocks with
  `BLOCK_SOURCE_ROUTE_INVARIANT_DRIFT`.
- Authorized ladder differences are explicit:
  - rank ladder authorizes only `fit_rank`;
  - degree ladder authorizes only `fit_degree`.

## Checks

CPU-only intent was set before framework import with
`CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp`.

Commands:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q \
  bayesfilter/highdim/source_route.py \
  bayesfilter/highdim/__init__.py \
  tests/highdim/test_p60_author_sir_rank_comparator.py \
  tests/highdim/test_p66_author_sir_fixed_branch_validation_ladder.py
```

Result: passed.

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q \
  tests/highdim/test_p66_author_sir_fixed_branch_validation_ladder.py
```

Result: `10 passed, 2 warnings in 2.84s`.

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q \
  tests/highdim/test_p60_author_sir_rank_comparator.py
```

Result: `7 passed, 2 warnings in 424.96s`.

The warnings were TensorFlow Probability deprecation warnings about
`distutils.version`.

## Claude Review

The first implementation-review prompt stalled; a tiny probe returned
`PROBE_OK`, so the prompt was redesigned into a bounded line-range review.

Claude implementation review R1b returned `VERDICT: AGREE`.

Accepted findings:

- Status taxonomy and exports match the Phase 1 contract.
- Old P60 is demoted to explanatory sentinel evidence without threshold
  weakening.
- No d18 correctness, HMC production readiness, or adaptive Zhao--Cui parity
  overclaim was visible.
- Sample-adequacy defaults and schema-only ladder behavior align with the
  contract.
- Invariant blocking and authorized differences are wired correctly for the
  Phase 2 scope.
- Synthetic P66 unit tests plus route-backed P60/P65 regression evidence are
  adequate for Phase 2 schema/contract acceptance, but not for future
  adjacent-ladder stability claims.

## Residual Risks

- No adjacent rank or degree ladder was executed in Phase 2.
- `READY_FIXED_BRANCH_VALIDATION_LADDER_SCHEMA` is schema/precondition
  readiness only; it is not adjacent-ladder stability and not correctness.
- The P66 unit tests monkeypatch expensive route builders to keep contract
  checks fast; route-backed evidence remains in the P60/P65 regression tests.
- No d18 correctness, d50/d100 scaling, adaptive parity, or HMC readiness claim
  is established.

## Phase 3 Handoff

Phase 3 may close out P66 if it verifies the final artifacts, records the
remaining nonclaims, and preserves the schema-only boundary for adjacent
ladders.  Phase 3 must not claim adjacent-ladder stability unless a separate
reviewed experiment executes both adjacent ladder diagnostics.

