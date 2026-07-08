# P84 Phase 6 Subplan: Analytical Derivative Repair

Date: 2026-06-23

Status: `DRAFT_BLOCKED_PENDING_PHASE5`

## Phase Objective

Repair or precisely block
`BLOCK_P83_PHASE4_ANALYTICAL_DERIVATIVE_READINESS`.

## Entry Conditions Inherited From Previous Phase

- Phase 5 KR status is known.
- Same-branch source-route scalar derivative target is frozen.

## Required Artifacts

- Result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p84-phase6-analytical-derivative-repair-result-2026-06-23.md`
- Derivative contract and tests if implemented.
- Updated execution ledger and Phase 7 subplan.

## Required Checks / Tests / Reviews

```bash
rg -n "ForwardAccumulator|JVP|finite difference|analytical derivative|same-branch|BLOCK_P83_PHASE4_ANALYTICAL_DERIVATIVE_READINESS" \
  docs/plans \
  bayesfilter/highdim \
  tests/highdim -S
```

Claude review is required before claiming derivative readiness.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Is there source-route same-branch analytical derivative wiring suitable for downstream HMC/gradient use? |
| Baseline/comparator | P83 Phase 4 blocker, source-route implementation, and source anchors. |
| Primary criterion | Analytical derivative route is implemented/identified, tested, and not merely FD/JVP/ForwardAccumulator. |
| Veto diagnostics | FD/JVP promoted as analytical readiness, branch mismatch, nonfinite gradients. |
| Explanatory diagnostics | FD/JVP comparisons, shape checks, local smokes. |
| Not concluded | No HMC readiness until Phase 7 sampler checks. |
| Artifact | Derivative result and tests. |

## Forbidden Claims / Actions

- Do not call FD/JVP/ForwardAccumulator the analytical comparator.
- Do not launch HMC before derivative readiness passes.

## Exact Next-Phase Handoff Conditions

Phase 7 may begin only if derivative readiness passes or HMC is explicitly
blocked/out of scope.

## Stop Conditions

Stop if only diagnostic derivative routes exist.
