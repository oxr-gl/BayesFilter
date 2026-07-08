# Phase 1 Subplan: Row Score Inventory

Date: 2026-07-03

Status: `DRAFT_PENDING_PHASE0`

## Phase Objective

Build a row-by-row inventory of LEDH score targets, parameter coordinates,
available exact or finite-difference comparators, current adapter status, and
the smallest admissible next action.

## Entry Conditions Inherited From Previous Phase

Phase 0 must establish:

- score means total derivative of the row likelihood target;
- no current LEDH leaderboard score row is admitted;
- Contract E is route evidence only;
- Claude review and GPU execution boundaries are frozen.

## Required Artifacts

- Inventory result:
  `docs/plans/bayesfilter-ledh-leaderboard-score-repair-phase1-row-score-inventory-result-2026-07-03.md`
- Inventory JSON:
  `docs/plans/bayesfilter-ledh-leaderboard-score-repair-phase1-row-score-inventory-2026-07-03.json`
- Refreshed Phase 2 subplan:
  `docs/plans/bayesfilter-ledh-leaderboard-score-repair-phase2-lgssm-score-repair-subplan-2026-07-03.md`

## Required Checks, Tests, And Reviews

- Read and summarize:
  - current LEDH-inclusive leaderboard JSON/MD;
  - LEDH inclusive closeout/reset memo;
  - July 1 total-VJP repair result;
  - same-target LGSSM value runner.
- Run a local JSON schema/content check for required row ids and LEDH statuses.
- Claude read-only review of the inventory if it changes a row status or next
  action.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Which leaderboard rows have enough target definition and comparator evidence to begin LEDH score repair? |
| Baseline/comparator | Current LEDH-inclusive leaderboard JSON and row-specific prior result artifacts. |
| Primary criterion | Every highdim row has a score target classification: `ready_for_score_repair`, `needs_adapter`, `no_free_theta`, `scoped_diagnostic_only`, or `blocked_wrong_target`. |
| Veto diagnostics | Missing row; ambiguous parameter coordinates; diagnostic row promoted to leaderboard row; value-only evidence promoted to score evidence. |
| Explanatory diagnostics | Existing value MCSE, exact comparator availability, likely runtime/memory risk. |
| Not concluded | No implementation correctness, no new score admission, no HMC readiness. |

## Forbidden Claims And Actions

- Do not run long GPU benchmarks in Phase 1.
- Do not edit algorithm code in Phase 1.
- Do not mark scoped P8p SIR evidence as full observed-data SIR score.
- Do not claim nonlinear row readiness without same-target adapter evidence.

## Exact Next-Phase Handoff Conditions

Advance to Phase 2 only if:

- the inventory identifies LGSSM `benchmark_lgssm_exact_oracle_m3_T50` as the
  first score-repair target;
- its target is recorded as `D=3,T=50`, dataset seed `81100`, theta
  `[0.72, 0.55, 0.35, 0.35, 0.45]`;
- exact Kalman value and score comparator paths or values are recorded;
- Phase 2 subplan has checks for same-target total derivative.

## Stop Conditions

Stop if:

- current leaderboard artifacts are missing or inconsistent;
- the LGSSM target cannot be reconstructed;
- row status changes require human approval;
- Claude blocks the inventory and the blocker is not fixed within five rounds.

## Phase-End Duties

At the end of Phase 1:

1. run the required local checks;
2. write the Phase 1 result and inventory JSON;
3. draft or refresh the Phase 2 subplan;
4. review the Phase 2 subplan for consistency, correctness, feasibility,
   artifact coverage, and boundary safety.
