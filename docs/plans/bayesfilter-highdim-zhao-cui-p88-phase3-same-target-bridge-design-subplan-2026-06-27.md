# P88 Phase 3 Subplan: Same-Target Reference Bridge Design

Date: 2026-06-27

Status: `REVIEWED_READY_FOR_PHASE3_EXECUTION`

## Phase Objective

Design, or explicitly block, a same-target source-backed reference bridge for
`D18_CORRECTNESS_CANDIDATE`.

## Entry Conditions Inherited From Previous Phase

- Phase 2 reviewed closed and promoted
  `D18_SOURCE_ROUTE_RANK_DEGREE_STABLE` as a degree-stable upstream fact:
  `docs/plans/bayesfilter-highdim-zhao-cui-p88-phase2-degree-convergence-execution-result-2026-06-27.md`.
- P87 Phase 8 missing-bridge blocker remains active unless this phase designs a
  real bridge.

## Required Artifacts

- Phase 3 result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p88-phase3-same-target-bridge-design-result-2026-06-27.md`
- Bridge inventory embedded in the result.
- Refreshed Phase 4 execution subplan or blocker.
- Updated ledgers.

## Required Checks/Tests/Reviews

Local artifact audit and bridge-design work only. Required checks must search
P83/P87/P88 and code/test bridge surfaces. Claude review required.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is there a same-target source-backed bridge with pinned scope, source anchors, and tolerances? |
| Baseline/comparator | P87 Phase 8 missing-bridge result, reviewed Phase 2 degree status after review agrees, author/source route target identity. |
| Primary criterion | Bridge candidate is same-target, source-backed, tolerance-pinned, separable from proxy evidence, and executable under a reviewed Phase 4 protocol; otherwise block. |
| Veto diagnostics | Wrong target, missing source anchors, missing tolerances, proxy bridge, local/UKF/LEDH route treated as source-route correctness, Phase 2 blocker bypass. |
| Explanatory diagnostics | Bridge provenance, target convention, tolerance rationale, expected runtime. |
| Not concluded | Correctness-candidate pass until Phase 4 executes/evaluates. |
| Artifact | Phase 3 bridge design result and refreshed Phase 4 subplan. |

## Forbidden Claims/Actions

- Do not execute a bridge in Phase 3.
- Do not use local fixed-branch, UKF, LEDH, or execution-only evidence as
  correctness.
- Do not start if Phase 2 result review revises or blocks.

## Exact Next-Phase Handoff Conditions

Phase 4 may start only with a reviewed bridge design and exact execution/
evaluation protocol. Otherwise Phase 4 remains blocked.

## Stop Conditions

- No same-target source-backed bridge can be anchored.
- Bridge tolerances cannot be justified before execution.
- Claude review does not converge after five rounds.

## End-Of-Phase Requirements

1. Run required local checks.
2. Write Phase 3 result/close or blocker record.
3. Draft or refresh Phase 4 subplan.
4. Review Phase 4 for consistency, correctness, feasibility, artifact coverage,
   and boundary safety.
