# Phase 4 Subplan: LEDH Particle Ladders

Date: 2026-07-03

Status: `DRAFT_PENDING_PHASE3`

## Phase Objective

Run LEDH particle-count ladders for admitted model rows using batched seeds on
trusted GPU/XLA/TF32, with value MCSE and score diagnostics kept separate.

## Entry Conditions Inherited From Previous Phase

- Phase 3 passed tiny GPU/XLA gates or produced an approved value-only scope.
- Runner can emit LEDH rows.
- Phase 1 ledger states which rows are admitted.

## Required Artifacts

- Raw per-row LEDH ladder JSON/MD artifacts.
- Logs under `docs/plans/logs/`.
- Phase 4 result:
  `docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-phase4-ledh-particle-ladders-result-2026-07-03.md`.
- Updated Phase 5 subplan.

## Required Checks, Tests, Reviews

- For each admitted row: batched seed run with fixed seed list.
- At least two adjacent particle counts where feasible.
- Record mean value, sample SD, MCSE, ESS, compile time, steady runtime, device,
  transport policy, chunk sizes, Sinkhorn iterations, and score status.
- Score checks only for rows where the same total derivative is computed and
  finite-difference or exact reference is meaningful.
- Claude review of the ladder result and row classifications.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Which admitted rows produce stable LEDH value estimates and which produce admitted total-derivative scores? |
| Baseline/comparator | Existing non-LEDH leaderboard rows and row-specific exact or finite-difference references where available. |
| Primary pass criterion | Each admitted LEDH row has either an executed value row with MCSE and diagnostics or a direct blocked reason; score rows pass their separate score criterion. |
| Veto diagnostics | Nonfinite outputs; MCSE missing; adjacent particle count moves beyond stated tolerance; ESS collapse; score mismatch beyond the stated rule; GPU/XLA metadata missing. |
| Explanatory diagnostics | Runtime, compile time, memory, particle trend, and per-seed dispersion. |
| Not concluded | Runtime ranking does not establish correctness; value-only row does not establish score or HMC readiness. |
| Artifact | Raw ladder JSON/MD and Phase 4 result. |

## Forbidden Claims And Actions

- Do not change pass/fail thresholds after seeing results.
- Do not drop failed seeds silently.
- Do not promote value-only rows to value+score.
- Do not compare a scoped component row as a full observed-data filtering row.

## Exact Next-Phase Handoff Conditions

Advance to Phase 5 only if:

- all admitted rows have raw LEDH artifacts;
- blocked rows have direct reasons;
- each row has value and score statuses;
- Claude review agrees or fixable issues are patched.

## Stop Conditions

- A run exceeds the visible runtime gate without artifact progress.
- A row repeatedly fails with nonfinite values after one reviewed repair.
- GPU memory or XLA compile behavior makes the planned ladder infeasible.
