# P88 Phase 4 Subplan: Correctness-Candidate Bridge Execution

Date: 2026-06-27

Status: `REVIEWED_READY_FOR_PHASE4_NO_RUNTIME_BLOCKER_CLOSEOUT`

## Phase Objective

Close the correctness-candidate bridge execution gate as a no-runtime blocker
unless Phase 3 review unexpectedly identifies an executable same-target bridge
protocol. Preserve `D18_CORRECTNESS_CANDIDATE` as blocked.

## Entry Conditions Inherited From Previous Phase

- Phase 2 reviewed closed and promoted `D18_SOURCE_ROUTE_RANK_DEGREE_STABLE`
  only as an upstream degree-stable fact.
- Phase 3 local result found no same-target source-backed bridge with pinned
  scope, source anchors, and tolerances:
  `docs/plans/bayesfilter-highdim-zhao-cui-p88-phase3-same-target-bridge-design-result-2026-06-27.md`.
- Phase 2 degree status must not be bypassed into correctness.

## Required Artifacts

- Phase 4 result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p88-phase4-correctness-bridge-execution-result-2026-06-27.md`
- No bridge output manifest is required unless Phase 3 review revises the
  missing-bridge decision.
- Refreshed Phase 5 subplan or blocker handoff.
- Updated ledgers.

## Required Checks/Tests/Reviews

No runtime command may run from this refreshed blocker handoff. Required checks:

- confirm Phase 3 missing-bridge status;
- confirm P59/P83/P86/P87 blocker anchors are still present;
- confirm no bridge manifest is named for execution;
- run P88 diff hygiene.

Claude review is required before Phase 4 closes. Claude cannot authorize a
correctness-candidate promotion from this blocker subplan.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can Phase 4 execute a reviewed bridge, or must it close as blocked because Phase 3 found no bridge protocol? |
| Baseline/comparator | Phase 3 missing-bridge result and Phase 2 degree status. |
| Primary criterion | If Phase 3 review agrees no bridge exists, write a no-runtime blocker result preserving `D18_CORRECTNESS_CANDIDATE` as blocked. |
| Veto diagnostics | Runtime bridge execution without protocol, wrong target, missing source anchors, missing tolerances, proxy metric masquerading as correctness, command drift, Phase 2 degree overclaim. |
| Explanatory diagnostics | Prior missing-bridge artifacts, P59 fail-closed guards, and bridge inventory. |
| Not concluded | Posterior correctness, HMC readiness, production readiness, full-history analytical-gradient correctness. |
| Artifact | Phase 4 blocker result and refreshed Phase 5 subplan. |

## Forbidden Claims/Actions

- Do not change bridge tolerances after seeing results.
- Do not invent bridge tolerances in Phase 4.
- Do not execute a bridge command from this blocker handoff.
- Do not execute GPU/CUDA, HMC/sampler, production-route, LEDH, package,
  network, or default-policy evaluation commands in Phase 4.
- Do not promote HMC/production readiness.
- Do not claim GPU readiness, production readiness, default-policy readiness,
  correctness-candidate promotion, LEDH agreement, d50/d100 scaling, or
  source-route analytical-gradient readiness.
- Do not treat a diagnostic-only bridge as exact correctness.

## Exact Next-Phase Handoff Conditions

Phase 5 may start only after Phase 4 records a reviewed blocker preserving
`D18_CORRECTNESS_CANDIDATE` as blocked and refreshes Phase 5 with that inherited
condition.

## Stop Conditions

- Phase 3 review revises the missing-bridge decision; in that case Phase 4 must
  stop as nonconverged and a separate reviewed replacement subplan is required.
- A requested Phase 4 action is broader than writing, checking, and reviewing
  no-runtime blocker artifacts.
- Claude review does not converge after five rounds.

## End-Of-Phase Requirements

1. Run required local checks.
2. Write Phase 4 result/close or blocker record.
3. Draft or refresh Phase 5 subplan.
4. Review Phase 5 for consistency, correctness, feasibility, artifact coverage,
   and boundary safety.
