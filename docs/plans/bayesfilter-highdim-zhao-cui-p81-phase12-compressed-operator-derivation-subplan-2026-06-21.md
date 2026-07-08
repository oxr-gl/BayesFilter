# P81 Phase 12 Subplan: Compressed Operator Derivation

status: REVIEWED_READY_TO_EXECUTE
date: 2026-06-21

## Phase Objective

Derive and choose, or block, a compressed deterministic transition route that
could make the parameterized local-route diagnostics meaningful beyond tiny
tie-out.  The target is a mathematical/design artifact, not implementation.

Phase 12 is read-only unless patched and re-reviewed.  It is not a d=18 run,
not an LEDH-PFPF-OT comparator phase, and not a source-faithfulness phase.

## Entry Conditions Inherited From Phase 11

- Phase 10 fixed parameterized local-route theta semantics and tied out tiny
  values and theta gradients.
- Phase 11 blocked direct implementation because exact local-route rank
  selection remains infeasible under P53-M5.
- P53 local/operator `R_eff` remains `extension_or_invention` for
  source-faithfulness.
- No implemented TT-MPO/operator-compression route with theta-derivative
  semantics exists in the audited code.

## Required Artifacts

- This Phase 12 subplan.
- Phase 12 result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p81-phase12-compressed-operator-derivation-result-2026-06-21.md`.
- Updated P81 master, runbook, execution ledger, Claude review ledger, and stop
  handoff.

The Phase 12 result must include the derivation or blocker, route classification,
exact/approximation status, approximation/error contract when the route is not
exact, memory formula, derivative semantics, lower-rung test contract, and
nonclaims.

## Required Checks, Tests, And Reviews

Review the Phase 11 result and this Phase 12 subplan with Claude read-only
before execution.

Allowed Phase 12 commands are read-only audits only:

```bash
rg -n "TT-MPO|MPO|operator compression|transition operator|Kronecker|tensor operator|local contraction|retained TT|theta derivative|JVP" docs/plans docs/chapters bayesfilter/highdim tests/highdim -g '*.md' -g '*.tex' -g '*.py'
rg -n "spatial_sir_local|LocalNeighborhood|FunctionalTT|TTCore|tt_evaluation|retained_filter|transition_log_density|ForwardAccumulator" bayesfilter/highdim tests/highdim -g '*.py'
```

No implementation edits, GPU/CUDA commands, LEDH diagnostics, package installs,
network fetches, detached agents, destructive actions, default changes, or d=18
full-grid computations are allowed unless the subplan is patched and reviewed.

Review the Phase 12 result and next subplan with Claude read-only after
execution.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Is there a derivable compressed deterministic transition route with explicit memory/rank and theta-gradient semantics, or should the deterministic local/operator lane block? |
| Exact baseline/comparator | Phase 10 tiny parameterized local tie-out; Phase 11 P53-M5 memory blocker; current absence of TT-MPO/operator implementation. |
| Primary pass criterion | Phase 12 passes only if it selects one route with enough derivation detail to draft an implementation subplan, or records a blocker with missing evidence. |
| Veto diagnostics | Undefined transition object; missing approximation status; missing approximation/error contract for non-exact routes; missing theta derivative semantics; missing branch/replay contract; relying on cap relaxation; claiming d=18 readiness or source-faithfulness. |
| Explanatory diagnostics | Candidate operator rank, local dependency width, retained-TT contraction shape, expected memory/runtime, and lower-rung tests. |
| Not concluded | No implementation, no d=18 correctness, no LEDH agreement, no HMC/posterior/default readiness, no source-faithfulness. |
| Artifact preserving result | Phase 12 result markdown and updated P81 ledgers. |

## Required Analysis

For each candidate route, answer:

1. What transition object is being represented?
2. Is the route exact for diagonal Gaussian transition covariance, or an
   approximation?
3. If approximate, what error is introduced, what quantity is bounded or
   monitored, what evidence would veto implementation, and what claim limits
   remain binding?
4. How are theta derivatives propagated?
5. What is the replay identity?
6. What is the memory/runtime formula?
7. What lower-rung tests would veto implementation?
8. Does the route remain `extension_or_invention`, or does it require source
   anchors?

Candidates to compare:

- TT-MPO compressed transition operator;
- hybrid local-factor contraction against retained TT cores;
- neighborhood-truncated approximation;
- source-route retained object as separate source-faithful lane;
- no deterministic compressed route without new math.

## Forbidden Claims And Actions

- Do not run LEDH-PFPF-OT diagnostics.
- Do not run d=18 full-grid transition propagation.
- Do not run GPU/CUDA commands.
- Do not edit implementation code unless the subplan is patched and reviewed.
- Do not claim source-faithfulness for local/operator routes.
- Do not claim HMC readiness, posterior validity, production/default readiness,
  or scientific validity.

## Exact Next-Phase Handoff Conditions

Phase 13 may implement only if Phase 12 records:

- selected route id and claim class;
- exact or approximate status;
- approximation/error contract and claim limits if the route is not exact;
- equations for value and theta derivative path;
- replay identity;
- memory/rank formulas and veto thresholds;
- lower-rung value/theta-gradient tests;
- stop conditions for d=18 attempts.

If no route is sufficiently defined, Phase 12 must close with a blocker and
request a derivation or human direction.

## Stop Conditions

Stop if the route object cannot be defined, if a non-exact route lacks an
approximation/error contract, if theta derivatives are not specified, if the
memory formula is missing, if the route depends only on raising caps, if
source-faithfulness is claimed without anchors, or if Claude review does not
converge after five rounds.
