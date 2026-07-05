# P81 Phase 7 Subplan: d=18 Transition Scaling Blocker

status: DRAFT_REVIEW_PENDING
date: 2026-06-21

## Phase Objective

Resolve the Phase 6 blocker before any LEDH/P8p comparison: the current
multistate full-history score route works on a tiny two-row fixture but cannot
run the SIR d=18 two-row candidate because the retained all-grid transition
path forms an all-pairs tensor of size `O(N_current N_previous d)`.

Phase 7 is an audit/design phase.  It must decide whether a bounded
chunked/streamed all-pairs logsumexp derivative can make the d=18 two-row
candidate smoke feasible, or whether the retained transition representation
must change before comparison.

## Entry Conditions Inherited From Phase 6

- Tiny d=2 two-observation multistate score finite-difference regression passed.
- Horizon-0 SIR d=18 score smoke remains valid for one-row observation-term
  wiring only.
- SIR d=18 two-row all-grid transition is blocked by `COMPLEXITY_GATE`.
- No LEDH/P8p candidate comparison has been run.
- The candidate remains fixed-branch/JVP-backed, not closed-form analytical,
  and no source-faithfulness claim is authorized.

## Required Artifacts

- This Phase 7 subplan.
- Phase 7 result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p81-phase7-d18-transition-scaling-blocker-result-2026-06-21.md`.
- Updated P81 master, runbook, execution ledger, Claude review ledger, and stop
  handoff.
- Optional Phase 8 subplan only if Phase 7 identifies a bounded implementation
  route.

The Phase 7 result must include a skeptical-audit note, decision table, run
manifest, explicit non-claims, and a quantitative route table.  For every
candidate route, the quantitative table must state estimated peak bytes, chunk
size, chunk count, asymptotic runtime, and whether a fail-fast preallocation
guard is preserved.

## Required Checks, Tests, And Reviews

No LEDH/P8p diagnostics may run in Phase 7.  No GPU command is needed for this
audit phase.

Local audit checks:

```bash
rg -n "_multistate_grid_predictive_log_density_from_retained|_multistate_grid_predictive_log_density_and_derivative_from_retained|_multistate_pairwise_transition_between_grids_log_density|_multistate_transition_log_density_derivative_between_grids|_check_pairwise_transition_tensor_budget" bayesfilter/highdim/filtering.py
rg -n "logsumexp|reduce_logsumexp|chunk|stream|pairwise|retained" bayesfilter/highdim docs/benchmarks tests/highdim
rg -n "test_multistate_fixed_design_tt_score_path_blocks_sir_d18_two_row_all_grid_transition|COMPLEXITY_GATE" tests/highdim/test_p81_analytical_sir_score.py bayesfilter/highdim/filtering.py
```

If a bounded route is identified, draft Phase 8 before implementation.  Phase 7
itself may not implement a streaming transition kernel unless this subplan is
patched and re-reviewed.

Boundary-safety requirement: any proposed Phase 8 route must preserve a
fail-fast preallocation guard before materializing transition tensors.  The
guard must record the formula
`current_count * previous_count * state_dim * sizeof(float64)` for unchunked
pairwise tensors, an explicit byte threshold, and the analogous per-chunk peak
formula for chunked routes.

Review this subplan with Claude read-only before execution.  Review the Phase 7
result and next subplan with Claude read-only after execution.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | What is the smallest bounded route to get a SIR d=18 two-row candidate full-history score smoke without forming the full all-pairs transition tensor? |
| Exact baseline/comparator | Current all-grid retained transition route with explicit `COMPLEXITY_GATE`; tiny d=2 two-row route as correctness smoke only. LEDH/P8p is not a Phase 7 comparator. |
| Primary criterion | Phase 7 passes if it produces a concrete Phase 8 implementation subplan for a bounded transition route, or a precise blocker showing no bounded route is available under current constraints. |
| Veto diagnostics | Treating tiny d=2 pass as d=18 readiness; running LEDH/P8p; removing the complexity gate; proposing a route without memory/runtime estimates; source-faithfulness overclaim. |
| Explanatory diagnostics | Estimated pairwise tensor bytes, candidate chunk size, number of chunks, possible logsumexp streaming formula, derivative streaming formula, and expected tests. |
| Not concluded | No d=18 full-history correctness, no LEDH agreement, no HMC readiness, no posterior/scientific validity, no performance scaling/default readiness. |
| Artifact preserving result | Phase 7 result markdown and updated P81 ledgers. |

## Required Phase 7 Analysis

Phase 7 must compare at least these options:

| Option | Question |
|---|---|
| Chunk current points | Can we stream over current grid blocks while reusing previous retained grid, keeping per-block tensors under a stated byte budget? |
| Chunk previous points with streaming logsumexp | Can we stream over previous grid blocks and maintain numerically stable logsumexp plus derivative accumulators for each current point? |
| Double chunk | Can we chunk both axes without materializing `current_count x previous_count`, and what does that imply for runtime? |
| Reduced retained grid | Is a smaller retained propagation grid scientifically/engineering-valid for a smoke, or would it change the candidate branch too much? |
| Alternative retained representation | Does the all-grid retained filter have to be replaced by samples/low-rank/TT contraction before d=18 transition score is feasible? |

The result must recommend one of:

- `PHASE8_STREAMED_ALL_PAIRS_IMPLEMENTATION`;
- `PHASE8_REDUCED_RETAINED_SMOKE_IMPLEMENTATION`;
- `BLOCK_REPRESENTATION_CHANGE_REQUIRED`;
- `BLOCK_NEEDS_HUMAN_DIRECTION`.

## Required Phase 8 Readiness Test Plan

If Phase 7 recommends an implementation route, the result and Phase 8 subplan
must include tests for:

- the current unbounded route still failing fast with `COMPLEXITY_GATE` instead
  of attempting allocation;
- the tiny d=2 two-observation multistate score finite-difference regression
  still passing;
- a bounded SIR d=18 two-row smoke defined under a concrete chunking or
  representation budget, without materializing all current-previous pairs;
- finite values/scores and same-branch finite-difference compatibility hashes
  for any candidate smoke that runs;
- explicit non-claims that the bounded smoke is not LEDH agreement, HMC
  readiness, posterior validity, or production/default readiness.

## Forbidden Claims And Actions

- Do not run LEDH/P8p comparator diagnostics.
- Do not run large d=18 diagnostics.
- Do not remove the pairwise transition complexity gate.
- Do not claim d=18 full-history score correctness.
- Do not claim source-faithfulness without Zhao-Cui paper/source anchors.
- Do not install/fetch packages, change defaults, use network, run detached
  agents, or take destructive git/filesystem actions.

## Exact Next-Phase Handoff Conditions

Phase 8 may implement only if Phase 7 identifies:

- exact helper(s) to edit;
- memory/runtime budget;
- chunking or representation contract;
- tiny d=2 regression preservation;
- SIR d=18 two-row smoke conditions;
- branch compatibility/hash contract;
- CPU-hidden and trusted-GPU boundaries;
- clear non-claims.

If Phase 7 cannot identify such a route, write a blocker result and stop.

## Stop Conditions

Stop if the only route requires materializing the full all-pairs tensor, if the
bounded route changes the scientific target without review, if the route would
need a broad refactor/default change, or if Claude review does not converge
after five rounds.
