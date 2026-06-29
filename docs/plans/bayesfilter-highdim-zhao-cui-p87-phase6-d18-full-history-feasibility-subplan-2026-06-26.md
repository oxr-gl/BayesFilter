# P87 Phase 6 Subplan: d18 Full-History Feasibility Gate

Date: 2026-06-26

Status: `REVIEWED_READY_FOR_PHASE6_EXECUTION`

## Phase Objective

Select or block a feasible SIR d18 full-history route that is not dense
all-pairs, streamed all-pairs, or a memory-budget-only variant of either
all-pairs route.

## Entry Conditions Inherited From Previous Phase

- Phase 5 tiny full-history regression passed under CPU-hidden local checks.
- Phase 5 did not run or claim SIR d18 full-history feasibility.
- `BLOCK_D18_ALL_PAIRS_DRIFT`, `BLOCK_PROXY_PROMOTION`, and
  `BLOCK_SOURCE_CLAIM_UNGROUNDED` remain active.
- The Phase 2 JVP-free repair sentinel remains active for any analytical
  gradient promotion.

## Required Artifacts

- Phase 6 result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p87-phase6-d18-full-history-feasibility-result-2026-06-26.md`
- Route feasibility table.
  Required columns: route name, claim class, source/provenance anchor,
  derivative semantics, replay identity, memory bound, rank/sample contract,
  blocker reason, and selected/not-selected decision.
- Explicit route classification for each candidate:
  `fixed_hmc_adaptation`, `extension_or_invention`, or `blocked_all_pairs`.
- Memory/rank/derivative-semantics contract for any selected route.
- Phase 6 decision table with decision, primary criterion status, veto
  diagnostic status, main uncertainty, next justified action, and what is not
  concluded.
- Phase 6 run/check manifest preserving commands actually run, CPU-hidden or
  GPU-not-used status, plan file, result file, reviewed artifacts consulted,
  wall time or `N/A`, and whether any TensorFlow command was intentionally
  avoided.
- Updated Phase 7 subplan.

## Required Checks/Tests/Reviews

Allowed edit scope:

- `docs/plans/bayesfilter-highdim-zhao-cui-p87-phase6-d18-full-history-feasibility-result-2026-06-26.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p87-phase7-source-route-rank-degree-gate-subplan-2026-06-26.md`
- P87 execution/review ledgers

Allowed read/check scope:

- `bayesfilter/highdim`
- `tests/highdim`
- `docs/plans/bayesfilter-highdim-zhao-cui-p81*.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p83*.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p86*.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p87*.md`

Execution environment:

- Repository root: `/home/chakwong/BayesFilter`.
- Execution target: local route audit only.
- No TensorFlow numerical command is required in Phase 6. If a Python command
  importing TensorFlow becomes necessary during a repair loop, it must use
  `CUDA_VISIBLE_DEVICES=-1` before import and the subplan must be patched
  visibly first.
- GPU/CUDA, long training, HMC, LEDH, and d18 all-history numerical runs are
  forbidden in Phase 6.
- Network/model access: none during local checks; Claude is read-only review
  only.

```bash
set -euo pipefail
rg -n "all-pairs|pairwise|streaming|LocalNeighborhoodScalingRouteConfig|factorized|source-route|retained" bayesfilter/highdim docs/plans tests/highdim -g '*.py' -g '*.md'
rg -n "COMPLEXITY_GATE|_check_pairwise_transition_tensor_budget_conservative|_multistate_grid_predictive_log_density_from_retained_streaming" bayesfilter/highdim/filtering.py tests/highdim/test_p81_analytical_sir_score.py
git diff --check -- docs/plans/bayesfilter-highdim-zhao-cui-p87*.md
```

Claude review required for route selection.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is there a feasible non-all-pairs SIR d18 full-history route with derivative semantics and memory/rank contract? |
| Baseline/comparator | P81 Phase 9 all-pairs blocker; P53/P83/P86 source/local-route artifacts. |
| Primary criterion | Select a route with explicit derivative semantics, replay identity, memory bound, rank/sample contract, and claim class; otherwise block. |
| Veto diagnostics | Dense all-pairs, streamed all-pairs, "increase memory" route, missing derivative semantics, source-faithful overclaim, proxy metrics promoted to correctness. |
| Explanatory diagnostics | Memory/rank estimates, route provenance, known tests. |
| Not concluded | SIR d18 correctness, source-route correctness, HMC readiness, production readiness, GPU readiness, or training/default-policy readiness. |
| Artifact | Phase 6 result. |

## Forbidden Claims/Actions

- Do not run all-pairs d18.
- Do not run streamed all-pairs d18.
- Do not treat increasing the dense/streaming memory budget as a new route.
- Do not call local/operator route source-faithful.
- Do not run long training or GPU benchmarks.
- Do not run HMC, LEDH comparisons, or default-policy changes.
- Do not use finite execution, ESS, fit loss, replay stability, or tiny-fixture
  parity as correctness proof.

## Exact Next-Phase Handoff Conditions

Phase 7 may start only if Phase 6 selects the source-route rank/degree gate or
another reviewed non-all-pairs route with explicit derivative semantics,
replay identity, memory bound, rank/sample contract, and claim class. If no
route is feasible, Phase 6 must write a blocker result and stop.

## Stop Conditions

- Only available route is all-pairs.
- Only available route is streamed all-pairs.
- No derivative semantics for selected route.
- Only proposed fix is increasing memory or chunk size for an all-pairs route.
- Route selection depends on source-faithful language without paper/source
  anchors.
- Claude review does not converge after five rounds.

## End-Of-Phase Requirements

1. Run required local checks.
2. Write Phase 6 result/close or blocker record with the route feasibility
   table, decision table, and run/check manifest required above.
3. Draft or refresh Phase 7 subplan.
4. Review Phase 7 for consistency, correctness, feasibility, artifact coverage,
   and boundary safety.
