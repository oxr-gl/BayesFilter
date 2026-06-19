# P66 Phase 1 Result: Validation Contract And API Design

metadata_date: 2026-06-15
status: REVIEWED_ACCEPTED_FOR_PHASE2_IMPLEMENTATION
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p66-fixed-branch-validation-ladder-master-program-2026-06-15.md
phase: 1
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Decision

Phase 1 proposes a reviewed contract/schema/policy for replacing the old P60
low/high closeness gate.  This artifact is not an experiment result,
implementation evidence, convergence evidence, or correctness evidence.

The current P59/P60 code and manifests are adequate exemplars for a clean P66
taxonomy if treated as exemplars to verify, not authority to copy blindly.

## Current Exemplar Anchors

- `P59AuthorSIRStepSpecAssemblyResult` records P59 source-route assembly status,
  blockers, step specs, sequential result, and manifest.
- P59-9b manifest records target dimension, source target order, fit-data mode,
  previous-marginal axes, fixed-HMC adaptation metadata, defensive `tau`,
  degree/rank, branch hashes, source anchors, and nonclaims.
- `P60AuthorSIRSameRouteRankComparatorResult` currently represents the old
  low/high closeness comparator.  P66 must preserve this as historical/sentinel
  evidence, not as the primary validation gate.
- The current P60 manifest already exposes old low/high deltas, normalizer
  decomposition, square-root TT core diagnostics, ESS, correction ranges,
  thresholds, source invariants, and nonclaims.

## Proposed API Surface

Add a new P66 API without removing P60:

```python
p66_author_sir_fixed_branch_validation_ladder(
    *,
    sample_count: int = 1,
    sentinel_fit_sample_count: int = 2,
    candidate_fit_sample_count: int | None = None,
    candidate_fit_degree: int = 1,
    candidate_fit_rank: int = 2,
    diagnostic_min_multiplier: int = 2,
    preferred_multiplier: int = 4,
    rank_ladder_fit_sample_count: int | None = None,
    degree_ladder_fit_sample_count: int | None = None,
) -> P66AuthorSIRFixedBranchValidationLadderResult
```

The old P60 comparator remains callable and unchanged.  P66 may call P60 to
populate a sentinel payload.

Fit-budget resolution:

- If `candidate_fit_sample_count is None`, resolve it to the candidate branch
  diagnostic minimum.
- If `rank_ladder_fit_sample_count is None`, resolve it to the maximum of the
  candidate and rank-stronger diagnostic minima.
- If `degree_ladder_fit_sample_count is None`, resolve it to the maximum of the
  candidate and degree-stronger diagnostic minima.
- The manifest must record all user-supplied and resolved fit-sample counts
  before interpreting any ladder diagnostic.

## Proposed Statuses

Overall result statuses:

- `READY_FIXED_BRANCH_VALIDATION_LADDER_SCHEMA`
- `PASS_ADJACENT_LADDER_DIAGNOSTICS_STABLE`
- `BLOCK_SOURCE_ROUTE_INVARIANT_DRIFT`
- `BLOCK_FIXED_BRANCH_DEFENSIVE_ONLY`
- `BLOCK_FIT_DESIGN_UNDERDETERMINED_FOR_CONVERGENCE`
- `BLOCK_ADJACENT_RANK_LADDER_NOT_STABLE`
- `BLOCK_ADJACENT_DEGREE_LADDER_NOT_STABLE`
- `BLOCK_VALIDATION_LADDER_IMPLEMENTATION_SCOPE`

Substatus fields:

- `candidate_admissibility_status`
  - `PASS_FIXED_BRANCH_ADMISSIBLE_NONCOLLAPSED`
  - `BLOCK_FIXED_BRANCH_DEFENSIVE_ONLY`
  - `BLOCK_SOURCE_ROUTE_INVARIANT_DRIFT`
- `sentinel_status`
  - `WARN_SENTINEL_BRANCH_DIFFERS_FROM_CANDIDATE`
  - `PASS_SENTINEL_BRANCH_WITHIN_OLD_P60_THRESHOLDS`
- `sample_adequacy_status`
  - `PASS_SAMPLE_ADEQUATE_FOR_DIAGNOSTIC`
  - `BLOCK_FIT_DESIGN_UNDERDETERMINED_FOR_CONVERGENCE`
- `rank_ladder_status`
  - `PASS_ADJACENT_RANK_LADDER_STABLE`
  - `BLOCK_ADJACENT_RANK_LADDER_NOT_STABLE`
  - `SKIP_ADJACENT_RANK_LADDER_UNDERDETERMINED`
  - `SCHEMA_ONLY_ADJACENT_RANK_LADDER_NOT_EXECUTED`
- `degree_ladder_status`
  - `PASS_ADJACENT_DEGREE_LADDER_STABLE`
  - `BLOCK_ADJACENT_DEGREE_LADDER_NOT_STABLE`
  - `SKIP_ADJACENT_DEGREE_LADDER_UNDERDETERMINED`
  - `SCHEMA_ONLY_ADJACENT_DEGREE_LADDER_NOT_EXECUTED`

Status semantics:

- Admissibility statuses are precondition/veto evidence.
- Sentinel statuses are explanatory evidence.
- Sample adequacy statuses are permission-to-diagnose evidence.
- Adjacent-ladder statuses are convergence-style diagnostics.
- None of these statuses is a d=18 correctness claim.
- `READY_FIXED_BRANCH_VALIDATION_LADDER_SCHEMA` means the schema and
  preconditions are implementable or satisfied; it is not a validation pass.
- `PASS_ADJACENT_LADDER_DIAGNOSTICS_STABLE` may be emitted only if adjacent
  rank and degree ladder diagnostics were actually executed and their declared
  stability checks passed.

## Sample-Adequacy Heuristic

For a branch with fixed degree and rank tuple, define:

```text
max_core_columns =
    max_axis ranks[axis] * (degree + 1) * ranks[axis + 1]

diagnostic_min_fit_samples = 2 * max_core_columns
preferred_fit_samples = 4 * max_core_columns
```

This is a scoped engineering heuristic for the P66 fixed-branch comparator.
It is not a proof of adequacy, not a convergence threshold, and not portable
outside this reviewed setup.
The table below is computed from the realized fixed-branch rank tuple pattern
`(1, R, ..., R, 1)` used by the current P59/P60/P65 route.  If realized ranks
or core layout change, values must be recomputed from the realized ranks and
recorded in the manifest.

Concrete values for the planned adjacent ladders:

| Branch | Max core columns | Diagnostic minimum | Preferred |
| --- | ---: | ---: | ---: |
| `(degree=1, rank=2)` | `8` | `16` | `32` |
| `(degree=1, rank=3)` | `18` | `36` | `72` |
| `(degree=2, rank=2)` | `12` | `24` | `48` |

The default P66 adjacent-ladder design should choose diagnostic minima unless
runtime evidence in Phase 2 shows that even those are too slow for visible
execution.  If runtime prevents adjacent-ladder execution, Phase 2 must write a
blocker or refreshed plan rather than silently falling back to the tiny tuple.

## Comparison Invariants

Every P66 candidate, rank-ladder row, and degree-ladder row must record and
check:

- route family and source authority;
- realized target definition;
- target dimension;
- source target order;
- previous marginal keep axes;
- previous marginal input axes;
- source-pushed fit-data mode;
- defensive `tau`;
- initialization rule;
- fixed-HMC adaptation class;
- fit-sample budget policy;
- sample-adequacy rule;
- diagnostic threshold definitions;
- resolved fit-budget counts and their resolution rule;
- admissibility status on both compared branches.

If any invariant differs and the difference is not explicitly authorized by the
ladder definition, the result must block with
`BLOCK_SOURCE_ROUTE_INVARIANT_DRIFT`.

An authorized comparison difference must be explicit in the manifest:

- `authorized_comparison_difference = True`;
- exact differing field;
- reason the difference is part of the reviewed ladder definition.

## Result Manifest Schema

The P66 result manifest must include:

- `target_id`;
- `pipeline_phase = "P66"`;
- `artifact_role = "fixed_branch_validation_ladder"`;
- `status`;
- `blockers`;
- `candidate`;
- `sentinel`;
- `sample_adequacy`;
- `fit_budget_resolution`;
- `rank_ladder`;
- `degree_ladder`;
- `source_invariants`;
- `comparison_invariants`;
- `nonclaims`;
- `p65_baseline_reference`;
- `old_p60_sentinel_payload`.

Candidate payload:

- degree, rank, rank tuple, fit sample count;
- fit branch hashes and density branch hashes;
- square-root normalizers by step;
- defensive-only steps;
- core norm ranges and near-zero counts;
- fit/adaptation metadata;
- admissibility status.

Sentinel payload:

- old P60 status and blockers;
- old P60 low/high deltas and thresholds;
- explicit `interpretation = "explanatory_sentinel_not_primary_gate"`.

Adjacent-ladder payloads:

- candidate branch identity;
- stronger branch identity;
- whether the ladder was actually executed;
- if not executed, `schema_only_reason`;
- sample adequacy for both rows;
- comparison invariants;
- log-marginal delta;
- normalizer increment deltas;
- probe log-density median delta;
- retained log-density median delta;
- ESS and correction ranges;
- status and blockers.

## Focused Phase 2 Tests

Phase 2 must add focused tests for:

- old P60 remains callable and continues to report the sentinel gap;
- P66 candidate `(degree=1, rank=2)` passes
  `PASS_FIXED_BRANCH_ADMISSIBLE_NONCOLLAPSED`;
- P66 sentinel status is
  `WARN_SENTINEL_BRANCH_DIFFERS_FROM_CANDIDATE`;
- tiny fit-sample count blocks convergence-style ladder interpretation with
  `BLOCK_FIT_DESIGN_UNDERDETERMINED_FOR_CONVERGENCE`;
- sample adequacy values for `(1,2)`, `(1,3)`, and `(2,2)` match the table
  above;
- comparison invariants are recorded and checked;
- source-route invariant drift blocks;
- no status or test claims d=18 correctness.

Runtime-sensitive adjacent ladder execution tests may start as schema/status
tests if full `(1,3)` or `(2,2)` execution exceeds visible limits.  If so,
Phase 2 must emit the corresponding `SCHEMA_ONLY_*_NOT_EXECUTED` status, record
that limitation, and not claim adjacent-ladder stability.

## Recommended Implementation Surfaces

- `bayesfilter/highdim/source_route.py`
  - add P66 statuses;
  - add P66 result dataclass;
  - add sample-adequacy helper;
  - add validation-ladder function;
  - reuse P59/P60 assembly and diagnostics where possible.
- `bayesfilter/highdim/__init__.py`
  - export P66 statuses, result type, and function.
- `tests/highdim/test_p66_author_sir_fixed_branch_validation_ladder.py`
  - add focused contract tests.

Do not remove or weaken existing P60 tests.

## What Is Not Concluded

- No code was changed by Phase 1.
- No new ladder implementation exists yet.
- No adjacent-ladder empirical result exists yet.
- No d=18 correctness claim.
- No d=50/d=100 scaling claim.
- No adaptive Zhao--Cui parity claim.
- No HMC production readiness claim.

## Phase 2 Handoff

Phase 2 may implement only this reviewed contract.  If Phase 2 discovers that
the contract is infeasible or too broad, it must stop and write a blocker or a
revised implementation subplan; it must not silently redesign P66 during code
editing.
