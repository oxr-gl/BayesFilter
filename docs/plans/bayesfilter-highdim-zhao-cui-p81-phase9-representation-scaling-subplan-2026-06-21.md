# P81 Phase 9 Subplan: Representation Scaling Route

status: REVIEWED_READY_TO_EXECUTE
date: 2026-06-21

## Phase Objective

Design the next representation or transition-application change needed to make
the d=18 multistate full-history fixed-branch score route computationally
meaningful.  Phase 9 follows Phase 8's conclusion: streamed all-pairs
logsumexp preserves the tiny target but still leaves quadratic full-grid work.

Phase 9 is not an LEDH/P8p comparator phase and not a GPU benchmark phase.

## Entry Conditions Inherited From Phase 8

- Tiny d=2 dense-vs-streaming value parity passed.
- Tiny d=2 dense-vs-streaming derivative parity passed.
- Tiny two-row multistate score finite-difference regression passed.
- The integrated score route can exercise streaming fallback on a tiny case.
- SIR d=18 horizon-0 smoke still passes as one-row engineering evidence only.
- SIR d=18 two-row all-grid route still fails fast with `COMPLEXITY_GATE`.
- Complete d=18 streamed all-grid propagation exceeds the Phase 8 chunk-product
  cap and remains blocked.

## Required Artifacts

- This Phase 9 subplan.
- Phase 9 result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p81-phase9-representation-scaling-result-2026-06-21.md`.
- Updated P81 master, runbook, execution ledger, Claude review ledger, and stop
  handoff.

The Phase 9 result must include a skeptical-audit note, decision table, run
manifest, route comparison table, explicit non-claims, and a next-phase
recommendation.

## Required Checks, Tests, And Reviews

Phase 9 is read-only audit/design unless the subplan is patched and re-reviewed.
No implementation edits, GPU/CUDA commands, LEDH/P8p diagnostics, package
installs, network fetches, detached agents, destructive actions, or default
policy changes are allowed.

Required local audit checks:

```bash
rg -n "streamed_or_factorized_transition_application|dense all-pairs|factorized_transition|scaling_route|R_eff" docs/plans bayesfilter/highdim tests/highdim -g '*.md' -g '*.py'
rg -n "class .*Transition|factorized|local|neighborhood|LowerRungStreamingRouteConfig|LocalNeighborhoodScalingRouteConfig|transition" bayesfilter/highdim/transition_route.py tests/highdim/test_p52_factorized_transition_route.py tests/highdim/test_p53_m4*.py
rg -n "_multistate_grid_predictive_log_density_from_retained_streaming|_check_pairwise_transition_tensor_budget_conservative|_validate_streaming_transition_inputs" bayesfilter/highdim/filtering.py
```

Review this subplan with Claude read-only before execution.  Review the Phase 9
result and next subplan with Claude read-only after execution.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Which representation or transition-application route is the smallest scientifically honest next step after Phase 8 shows full-grid streaming is still too expensive? |
| Exact baseline/comparator | Current retained all-grid dense/streamed transition route with `COMPLEXITY_GATE`; prior P51/P52/P53 scaling-route artifacts.  LEDH/P8p is not a Phase 9 comparator. |
| Primary criterion | Phase 9 passes if it selects a next implementable route or writes a precise blocker with the evidence needed before implementation. |
| Veto diagnostics | Calling full-grid streaming sufficient for d=18; proposing LEDH comparison from tiny evidence; using dense all-pairs as production route; claiming source-faithfulness without paper/source anchors; selecting a route without derivative semantics, branch contract, and memory/runtime bounds. |
| Explanatory diagnostics | Candidate route width, memory formula, asymptotic transition work, differentiability path, compatibility with fixed-branch hashes, and source-anchor needs. |
| Not concluded | No d=18 full-history correctness, no LEDH/P8p agreement, no HMC readiness, no posterior/scientific validity, no source-faithfulness, no default readiness. |
| Artifact preserving result | Phase 9 result markdown and updated P81 ledgers. |

## Required Analysis

Compare at least these options:

| Option | Required question |
|---|---|
| Keep streamed all-pairs with subsets | Does this answer any scientific question beyond engineering smoke, or should it remain blocked? |
| Factorized Gaussian transition application | Can the Zhao-Cui/SIR transition density structure be applied without enumerating all current-previous grid pairs, and what derivation is required? |
| TT contraction / low-rank transition operator | Can the transition kernel be represented or approximated as a tensor operator compatible with the retained TT density and score derivative? |
| Local/neighborhood route | Can a reviewed local transition neighborhood bound effective previous states while preserving a branch contract and derivative semantics? |
| Source-route sample/ESS propagation | Does the author-style sample propagation route supersede retained all-grid propagation for paper-faithful scaling, and what source anchors are required before using that claim? |

## Forbidden Claims And Actions

- Do not run LEDH/P8p diagnostics.
- Do not run d=18 full-grid transition computation.
- Do not use GPU/CUDA commands in Phase 9.
- Do not implement code unless this subplan is patched and re-reviewed.
- Do not claim source-faithfulness without Zhao-Cui paper and author-source
  anchors.
- Do not claim HMC readiness, posterior validity, production/default readiness,
  or scientific validity.

## Exact Next-Phase Handoff Conditions

Phase 10 may implement only if Phase 9 records:

- the selected route and why it is smaller than the alternatives;
- exact helper/API surfaces to edit;
- value and derivative semantics;
- fixed-branch/replay/hash contract;
- memory and runtime formulas with veto thresholds;
- lower-rung tie-out tests before any d=18 attempt;
- whether source anchors are required and, if so, which files/sections must be
  inspected before implementation.

If no route can be selected without a derivation or source audit, Phase 9 must
close with a blocker and a precise evidence request.

## Stop Conditions

Stop if the only route is full all-pairs enumeration, if the route would change
the scientific target without an explicit branch contract, if source-faithful
language cannot be anchored, if derivative semantics are missing, or if Claude
review does not converge after five rounds.
