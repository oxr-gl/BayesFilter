# Phase 5 Subplan: Nonlinear Row Adapter Admission

Date: 2026-07-03

Status: `REFRESHED_AFTER_PHASE4_FIXED_SIR_NO_FREE_THETA`

## Phase Objective

For actual SV, KSC SV, predator-prey, and generalized SV, determine whether a
same-target GPU/XLA/TF32 LEDH adapter exists or can be implemented without
changing the leaderboard target.

## Entry Conditions Inherited From Previous Phase

Phase 4 recorded:

- LGSSM score remains blocked by
  `blocked_total_transport_vjp_needs_no_tape_repair`;
- fixed spatial SIR main row is `no_free_theta_value_only`;
- parameterized SIR log-scale row is scoped component evidence only, not full
  observed-data filtering score evidence.

Phase 5 therefore excludes fixed SIR from score repair and classifies only
actual SV, KSC SV, predator-prey, and generalized SV adapter readiness.

## Required Artifacts

- Phase result:
  `docs/plans/bayesfilter-ledh-leaderboard-score-repair-phase5-nonlinear-adapter-admission-result-2026-07-03.md`
- Adapter admission ledger JSON:
  `docs/plans/bayesfilter-ledh-leaderboard-score-repair-phase5-nonlinear-adapter-admission-2026-07-03.json`
- Refreshed Phase 6 subplan.

## Required Checks, Tests, And Reviews

- Inspect existing benchmark row definitions and LEDH adapter surfaces.
- Confirm fixed SIR is not reintroduced as a score-repair target.
- For Zhao-Cui rows, inspect and cite required paper/source anchors before any
  `source_faithful` claim.
- Local content check for all nonlinear row ids.
- Claude read-only review if any row is moved from blocked to admitted for
  score repair.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Which nonlinear rows have a same-target LEDH adapter ready for score repair? |
| Baseline/comparator | Current leaderboard row definitions and existing non-LEDH row evidence. |
| Primary criterion | Each nonlinear row is classified as `adapter_ready`, `adapter_missing`, `target_mismatch`, or `requires_human_target_decision`. |
| Veto diagnostics | Wrong target; fixed SIR reintroduced as a score target; missing source anchors for Zhao-Cui source claims; diagnostic row promoted to leaderboard row; adapter changes likelihood target. |
| Explanatory diagnostics | Existing value paths, expected parameter coordinates, likely exact/FD comparator. |
| Not concluded | No nonlinear score correctness or value correctness unless implemented and tested later. |

## Forbidden Claims And Actions

- Do not claim adapter readiness from name similarity alone.
- Do not use auxiliary/native-oracle rows as source-row evidence.
- Do not implement row repairs before adapter target classification passes.
- Do not reclassify fixed SIR as a score row.

## Exact Next-Phase Handoff Conditions

Advance to Phase 6 if:

- at least one nonlinear row is `adapter_ready`; or
- all nonlinear rows are blocked and Phase 6 is marked skipped with reason.

## Stop Conditions

Stop if:

- row target definitions conflict;
- source anchors are unavailable for a required source-faithful claim;
- Claude blocks adapter admission and the blocker is not fixed within five
  rounds.

## Phase-End Duties

At the end of Phase 5:

1. run required local checks;
2. write the Phase 5 result and adapter ledger;
3. draft or refresh the Phase 6 subplan;
4. review the Phase 6 subplan for consistency, correctness, feasibility,
   artifact coverage, and boundary safety.
