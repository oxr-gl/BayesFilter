# P81 Phase 11 Subplan: Memory, Rank, And Compression Policy

status: REVIEWED_READY_TO_EXECUTE
date: 2026-06-21

## Phase Objective

Decide the next scientifically honest route for turning the parameterized local
transition tie-out into a computationally meaningful d=18 candidate, or write a
precise blocker if no route can be selected without a new derivation.

Phase 11 is a read-only design/audit phase unless this subplan is patched and
re-reviewed.  It is not a d=18 run, not an LEDH-PFPF-OT comparator phase, and
not a source-faithfulness phase.

## Entry Conditions Inherited From Phase 10

- Phase 8 streamed all-pairs transition propagation still leaves quadratic
  full-grid work.
- Phase 9 selected the P53 local-neighborhood route as the smallest
  deterministic fixed-gradient diagnostic route, not as a source-faithful route.
- Phase 10 fixed parameterized local-route theta semantics and tied out tiny
  local-vs-dense values and theta gradients.
- P53-M5 still blocks exact d=18 local-route rank selection under the active
  8 GiB step-memory cap:

```text
R_eff = 2916
rank-1 forecast = 29,386,561,536 bytes
r_max = 0
```

## Required Artifacts

- This Phase 11 subplan.
- Phase 11 result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p81-phase11-memory-rank-compression-result-2026-06-21.md`.
- Updated P81 master, runbook, execution ledger, Claude review ledger, and stop
  handoff.

The Phase 11 result must include a skeptical-audit note, decision table, run
manifest, route-policy comparison, nonclaims, and exact next-phase handoff.

## Required Checks, Tests, And Reviews

Review the Phase 10 result and this Phase 11 subplan with Claude read-only
before Phase 11 execution.

Allowed Phase 11 commands are read-only audits only:

```bash
rg -n "R_eff|rank-1 forecast|rank selection|memory_forecast|step_memory|TT-MPO|operator|compression|local-neighborhood|source-faithful|extension_or_invention" docs/plans bayesfilter/highdim tests/highdim -g '*.md' -g '*.py'
rg -n "rank_ceiling|step_memory_bytes|P53_RANK_SELECTION|LocalNeighborhoodScalingRouteConfig|P53_LOCAL_SCALING_ROUTE_ID|tt_mpo|operator" bayesfilter/highdim tests/highdim -g '*.py'
rg -n "source-route|retained object|TTSIRT|marginal|proposal correction|local/operator|R_eff" docs/plans/bayesfilter-highdim-zhao-cui-p56-source-anchor-audit-2026-06-10.md docs/plans/bayesfilter-highdim-zhao-cui-p57-m7-source-faithful-rank-ukf-calibration-result-2026-06-11.md
```

No implementation edits, GPU/CUDA commands, LEDH diagnostics, package installs,
network fetches, detached agents, destructive actions, default changes, or d=18
full-grid computations are allowed in Phase 11 unless the subplan is patched and
reviewed again.

Review the Phase 11 result and next subplan with Claude read-only after
execution.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | What is the next valid route after exact parameterized local-route tie-out still fails the d=18 rank/memory contract? |
| Exact baseline/comparator | P53-M5 exact local-route rank-selection blocker; Phase 10 parameterized local-route tie-out; P56/P57 source-route boundary. |
| Primary pass criterion | Phase 11 passes if it selects exactly one next implementable route with memory/rank formulas, derivative semantics, branch contract, and required lower-rung tests, or writes a precise blocker. |
| Veto diagnostics | Relaxing memory caps without a new claim class; pretending tiny tie-out solves d=18; jumping to LEDH comparison; calling local/operator route source-faithful; selecting a compressed route without approximation status and derivative semantics. |
| Explanatory diagnostics | Forecast memory, rank bounds, approximation/error status, branch replay identity, differentiability path, source-anchor requirements, and smallest lower-rung tie-out. |
| Not concluded | No d=18 full-history correctness, no LEDH-PFPF-OT agreement, no HMC readiness, no posterior validity, no source-faithfulness, no default readiness. |
| Artifact preserving result | Phase 11 result markdown and updated P81 ledgers. |

## Required Analysis

Compare at least these options:

| Option | Required question |
|---|---|
| Exact local route with larger cap | Is this just cap relaxation, and what claim class would change? |
| Smaller local approximation | What neighborhood truncation or factor approximation is introduced, and how would error be tested? |
| TT-MPO/operator compression | What tensor-operator object is represented, what rank controls it, and how are theta derivatives propagated? |
| Hybrid local plus retained-TT contraction | Can the Phase 10 local factors contract against retained TT cores without enumerating all current/previous rows? |
| Source-route retained object | Is this the right route for source-faithful claims, and what paper/source anchors must govern it? |
| Stop/block | What derivation or code substrate is missing before implementation can be scientifically honest? |

## Forbidden Claims And Actions

- Do not run LEDH-PFPF-OT diagnostics.
- Do not run d=18 full-grid transition propagation.
- Do not run GPU/CUDA commands in Phase 11.
- Do not edit implementation code unless the subplan is patched and reviewed.
- Do not claim source-faithfulness for local/operator routes.
- Do not claim HMC readiness, posterior validity, production/default readiness,
  or scientific validity.

## Exact Next-Phase Handoff Conditions

Phase 12 may implement only if Phase 11 records:

- exactly one selected route or a blocker;
- memory and runtime formulas with veto thresholds;
- value and theta-derivative semantics;
- branch replay/hash contract;
- exact lower-rung tie-out tests before any d=18 attempt;
- approximation status and nonclaims;
- source-anchor requirements if the selected route crosses into
  source-faithfulness territory.

If no route can be selected without a new derivation, Phase 11 must close with
a blocker and request the missing derivation or human direction.

## Stop Conditions

Stop if the only proposed action is cap relaxation, if tiny tie-out is promoted
to d=18 readiness, if source-faithfulness is claimed without anchors, if the
selected route lacks derivative semantics, if the route would require
unreviewed GPU/large-run/code-edit boundaries, or if Claude review does not
converge after five rounds.
