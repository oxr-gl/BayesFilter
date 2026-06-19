# P66 Phase 2 Subplan: Implementation And Focused Tests

metadata_date: 2026-06-15
status: REVIEWED_READY_FOR_IMPLEMENTATION
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p66-fixed-branch-validation-ladder-master-program-2026-06-15.md
phase: 2
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Phase Objective

Implement the reviewed P66 validation ladder contract and focused tests.

Phase 2 may add new validation APIs and tests, but it must not weaken the old
P60 comparator.  The old P60 low/high closeness result should remain available
as historical/sentinel evidence.

## Entry Conditions Inherited From Previous Phase

- Phase 1 result contains a reviewed validation contract and API design.
- Phase 2 implementation surfaces and tests are enumerated.
- Phase 1 did not authorize d=18 correctness or adaptive parity claims.
- Phase 1 proposed implementation surfaces:
  `bayesfilter/highdim/source_route.py`, `bayesfilter/highdim/__init__.py`, and
  `tests/highdim/test_p66_author_sir_fixed_branch_validation_ladder.py`.

## Required Artifacts

- Phase 2 implementation result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p66-phase2-implementation-result-2026-06-15.md`.
- Updated tests and code.
- Updated P66 visible execution ledger.
- Claude implementation review entry.
- Refreshed Phase 3 closeout subplan.

## Required Checks/Tests/Reviews

- Compile touched files.
- Focused tests for:
  - old P60 remains callable and reports sentinel gap;
  - source-route invariant gate;
  - admissibility/noncollapse gate;
  - sentinel low/high diagnostic status;
  - candidate fit-budget resolution;
  - rank-ladder default fit-budget resolution;
  - degree-ladder default fit-budget resolution;
  - manifest persistence of `fit_budget_resolution` for candidate, rank ladder,
    and degree ladder rows;
  - sample-adequacy blocker for convergence when rows are insufficient;
  - sample-adequacy values for `(degree=1, rank=2)`,
    `(degree=1, rank=3)`, and `(degree=2, rank=2)`;
  - adjacent rank ladder manifest/status;
  - adjacent degree ladder manifest/status.
  - authorized comparison differences record
    `authorized_comparison_difference=True`, exact field, and reason;
  - unauthorized comparison drift blocks with
    `BLOCK_SOURCE_ROUTE_INVARIANT_DRIFT`;
  - schema-only adjacent ladder rows emit
    `SCHEMA_ONLY_ADJACENT_RANK_LADDER_NOT_EXECUTED` or
    `SCHEMA_ONLY_ADJACENT_DEGREE_LADDER_NOT_EXECUTED`;
  - schema-only rows carry `schema_only_reason`.
- Repaired P65 tests must remain green.
- Bounded Claude review of implementation diff and evidence.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the code implement the reviewed validation ladder without weakening old P60 thresholds or changing the source route? |
| Baseline/comparator | P66 Phase 1 contract and P65 fixed-branch repair behavior. |
| Primary pass criterion | New P66 tests pass; old P60 remains historical/sentinel; source invariants and branch admissibility preconditions are enforced; sample adequacy is recorded as permission-to-diagnose; adjacent-ladder diagnostics are recorded without being promoted to d=18 correctness. |
| Veto diagnostics | Old thresholds weakened; old sentinel gap hidden; high branch becomes defensive-only; target/order/axes drift; defensive tau changes; tests promote admissibility to d=18 correctness. |
| Explanatory diagnostics | Status payloads, ladder deltas, sample adequacy ratios, old P60 deltas, fit residuals, ESS, correction ranges. |
| Not concluded | No d=18 correctness, no d=50/d=100 scaling, no adaptive parity, no HMC readiness. |

## Forbidden Claims/Actions

- Do not rewrite unrelated code.
- Do not remove P65/P60 historical diagnostics.
- Do not run long ladders without a reviewed experiment plan.
- Do not change default product policy or scientific claims.
- Do not let admissibility or sample adequacy statuses imply convergence.
- Do not alter adjacent-ladder comparison invariants except as explicitly
  authorized by the Phase 1 contract.
- Do not emit `PASS_ADJACENT_LADDER_DIAGNOSTICS_STABLE` unless adjacent rank
  and degree ladders were actually executed.

## Exact Next-Phase Handoff Conditions

Advance to Phase 3 only if:

- focused implementation checks pass;
- Claude implementation review converges;
- Phase 2 result records exact changed files and residual risks;
- Phase 3 subplan is refreshed around closeout, not new development.

## Stop Conditions

- Implementation requires a broader design than Phase 1 authorized.
- Focused tests expose new source-route drift.
- Runtime cost exceeds visible execution limits before a discriminating
  artifact is produced.
- Claude and Codex do not converge after five rounds for the same blocker.

## End-Of-Subplan Protocol

1. Run required local checks.
2. Write Phase 2 result or blocker.
3. Draft or refresh Phase 3 subplan.
4. Review Phase 3 subplan for consistency, correctness, feasibility, artifact
   coverage, and boundary safety.
