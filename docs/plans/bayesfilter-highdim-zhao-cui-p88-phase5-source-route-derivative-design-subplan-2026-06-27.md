# P88 Phase 5 Subplan: Source-Route Analytical Derivative Design

Date: 2026-06-27

Status: `REVIEWED_READY_FOR_PHASE5_LOCAL_DERIVATIVE_DESIGN_AUDIT`

## Phase Objective

Design source-route full-history analytical derivative wiring with paper/source
anchors and explicit JVP/autodiff exclusion for the promoted path.

## Entry Conditions Inherited From Previous Phase

- Phase 4 no-runtime blocker result must be reviewed:
  `docs/plans/bayesfilter-highdim-zhao-cui-p88-phase4-correctness-bridge-execution-result-2026-06-27.md`.
- `D18_CORRECTNESS_CANDIDATE` remains blocked by missing same-target
  source-backed reference bridge.
- P87 Phase 4/5 fixed-branch evidence remains secondary unless this phase
  designs source-route derivative wiring.

## Required Artifacts

- Phase 5 result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p88-phase5-source-route-derivative-design-result-2026-06-27.md`
- Source/paper anchor inventory embedded in the result.
- Refreshed Phase 6 subplan or blocker handoff.
- Updated ledgers.

## Required Checks/Tests/Reviews

Local code/doc audit only unless refreshed. Required checks must inspect
`ForwardAccumulator`, `target_derivative_backend`, source-route derivative
helpers, cited author anchors, and the inherited correctness blocker. Claude
review required.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is there a source-route full-history analytical derivative design that can be implemented without JVP/autodiff promotion? |
| Baseline/comparator | P87 JVP-free fixed-branch repair, P83/P87/P88 source-route boundaries, Phase 4 correctness blocker, author paper/source anchors. |
| Primary criterion | Every derivative component is classified with source anchors, implementation surface, JVP exclusion, and exact future tests; otherwise block. |
| Veto diagnostics | Missing source anchors, JVP/ForwardAccumulator in promoted path, local fixed-branch evidence promoted to source-route derivative, wrong branch, correctness/HMC/production overclaim. |
| Explanatory diagnostics | FD/JVP rows may explain only; they are not proof. |
| Not concluded | Implemented derivative correctness, correctness-candidate status, HMC readiness, production readiness, GPU readiness, LEDH agreement, or default-policy readiness. |
| Artifact | Phase 5 design result and refreshed Phase 6 subplan. |

## Forbidden Claims/Actions

- Do not implement derivative code unless this subplan is visibly refreshed.
- Do not call JVP/autodiff analytical source-route derivative evidence.
- Do not use derivative design to bypass the Phase 4 correctness blocker.
- Do not claim HMC readiness.

## Exact Next-Phase Handoff Conditions

Phase 6 may start only if Phase 5 either blocks or provides a reviewed
derivative-readiness boundary needed for HMC/production readiness.

## Stop Conditions

- Source anchors cannot be inspected.
- Derivative path requires JVP/autodiff in promoted route.
- Claude review does not converge after five rounds.

## End-Of-Phase Requirements

1. Run required local checks.
2. Write Phase 5 result/close or blocker record.
3. Draft or refresh Phase 6 subplan.
4. Review Phase 6 for consistency, correctness, feasibility, artifact coverage,
   and boundary safety.
