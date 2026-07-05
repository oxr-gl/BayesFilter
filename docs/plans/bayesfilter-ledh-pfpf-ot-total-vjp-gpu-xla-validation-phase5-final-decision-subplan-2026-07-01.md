# Phase 5 Subplan: Final Decision And Next Implementation

Date: 2026-07-01

Status: `READY_FOR_CLAUDE_REVIEW`

## Phase Objective

Write the final decision for the corrected full total-derivative route and the
next implementation action.

## Entry Conditions Inherited From Previous Phase

- Phase 4 passed the predeclared raw-direction rule with a runtime caveat.
- All earlier phase results exist.

## Required Artifacts

- Final decision result:
  `docs/plans/bayesfilter-ledh-pfpf-ot-total-vjp-gpu-xla-validation-phase5-final-decision-result-2026-07-01.md`.
- Final visible stop handoff.
- Claude final review entry.

## Required Checks, Tests, Reviews

- Check all phase result files exist.
- Check final decision cites exact artifacts.
- Claude read-only review of final decision and handoff.

Proposed final label:

`GPU_XLA_VIABLE_TOTAL_DERIVATIVE_EXPERIMENTAL_ROUTE_WITH_RAW_DIRECTION_GATE_PASS`

This label is allowed to say:

- the corrected finite-Sinkhorn total-derivative route runs under trusted
  GPU/XLA/TF32 through the checked `N=1000,T=3` SIR diagnostic;
- the raw-direction same-scalar FD gate passed under the predeclared relaxed
  rule;
- the route remains experimental because the FD diagnostic is expensive and
  this is not full HMC production readiness.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | What does the evidence justify doing next with the corrected route? |
| Baseline/comparator | Phase 0--4 artifacts. |
| Primary criterion | Final label is directly supported and nonclaims are explicit. |
| Veto diagnostics | Unsupported promotion, hidden failed gate, missing artifact, evasive language. |
| Explanatory diagnostics | Runtime/memory summaries and strongest alternative explanation. |
| Not concluded | Any claim not supported by phase artifacts. |
| Artifact preserving result | Final decision result and stop handoff. |

## Forbidden Claims And Actions

- Do not promote to production default unless evidence explicitly supports it
  and the user approves that policy change.
- Do not hide blockers behind soft language.
- Do not call a partial derivative a score.

## Exact Next-Phase Handoff Conditions

This is the last phase.  Write the final visible handoff and stop.

## Stop Conditions

- Missing phase artifacts.
- Claude final review fails to converge after five rounds.
