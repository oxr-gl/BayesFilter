# Phase 4 Subplan: LEDH Particle Ladders

Date: 2026-07-03

Status: `DRAFT_READY_AFTER_PHASE3_REVIEW`

## Phase Objective

Run LEDH particle-count ladders for admitted model rows using batched seeds on
trusted GPU/XLA/TF32, with value MCSE and score diagnostics kept separate.

## Entry Conditions Inherited From Previous Phase

- Phase 3 passed trusted GPU/XLA/TF32 route checks.
- The Contract E LGSSM route fixture passed value+score at `N=3000`; the
  `N=1000` score gate failed for `ar_coefficient`; the unchunked `N=10000`
  score route is blocked by GPU memory.
- The Contract E fixture is not the leaderboard LGSSM row. It has `D=2`,
  `T=10`, three parameters, and value about `-13.8`; the leaderboard row
  `benchmark_lgssm_exact_oracle_m3_T50` has `D=3`, `T=50`, five parameters,
  dataset seed `81100`, theta `[0.72, 0.55, 0.35, 0.35, 0.45]`, and exact
  value about `-2.7215`.
- Therefore the leaderboard LGSSM score remains blocked, and the leaderboard
  LGSSM value remains blocked until a same-target LEDH value artifact exists.
- Fixed spatial SIR passed only a tiny value smoke; its score remains blocked.
- Runner can emit LEDH rows.
- Phase 1 ledger states which rows are admitted.

## Required Artifacts

- Raw per-row LEDH ladder JSON/MD artifacts.
- Same-target LGSSM value runner artifact for
  `benchmark_lgssm_exact_oracle_m3_T50`, or a direct blocker explaining why it
  cannot be produced.
- Logs under `docs/plans/logs/`.
- Phase 4 result:
  `docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-phase4-ledh-particle-ladders-result-2026-07-03.md`.
- Updated Phase 5 subplan.

## Required Checks, Tests, Reviews

- For each admitted value row: batched seed run with fixed seed list
  `81120,81121,81122,81123,81124`.
- Fixed spatial SIR value-only default rungs: `N=1000` and `N=10000`, using the
  streaming value path and memory-safe chunks.
- Contract E LGSSM score rungs: `N=3000` is admitted only for the Contract E
  fixture. `N=10000` is forbidden for the current unchunked score path unless a
  reviewed memory-safe route is added before execution.
- Leaderboard LGSSM score rungs: blocked. Do not mark
  `benchmark_lgssm_exact_oracle_m3_T50` score as executed from Contract E
  evidence.
- Leaderboard LGSSM value-only rungs may use `N=1000` and `N=10000` only after
  a same-target runner is implemented and records `D=3`, `T=50`, dataset seed
  `81100`, theta `[0.72, 0.55, 0.35, 0.35, 0.45]`, exact Kalman value
  comparator, and blocked score status.
- Optional adjacent high rung: `N=50000` only if pre-run budget and memory
  estimates pass before execution.
- Any deviation from the default ladder must be recorded as a blocker or as a
  reviewed row-specific ladder before seeing results.
- Value stability criterion: for adjacent value rungs `N_a < N_b`, pass only if
  `abs(mean_b - mean_a) <= 5 * sqrt(mcse_a^2 + mcse_b^2)`. If a row has an
  exact value comparator, also report the exact-comparator delta, but do not
  replace the adjacent-rung criterion after seeing results.
- Value MCSE sanity criterion: the larger adjacent rung must have MCSE no larger
  than the smaller adjacent rung, unless the Phase 4 result records a direct
  finite-sample explanation and leaves the row diagnostic-only.
- Runtime gate: a single row/rung command may run for at most 30 minutes
  without creating or updating a structured artifact or log. A full Phase 4 row
  may run for at most 4 hours without a completed row artifact. Exceeding either
  limit is a `blocked_runtime_gate` result, not a silent skip.
- Record mean value, sample SD, MCSE, ESS where available, compile time,
  steady runtime, device,
  transport policy, chunk sizes, Sinkhorn iterations, and score status.
- Score checks only for rows where the same total derivative is computed and
  finite-difference or exact reference is meaningful.
- Claude review of the ladder result and row classifications.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Which admitted rows produce stable same-target LEDH value estimates and which produce admitted total-derivative scores? |
| Baseline/comparator | Existing non-LEDH leaderboard rows and row-specific exact or finite-difference references where available. |
| Primary pass criterion | Each requested LEDH row has either an executed same-target value row with MCSE and diagnostics or a direct blocked/scoped reason; score rows pass their separate total-derivative score criterion at an admitted same-target memory-safe rung. |
| Veto diagnostics | Wrong target; nonfinite outputs; MCSE missing; adjacent value change exceeding `5 * sqrt(mcse_a^2 + mcse_b^2)`; larger-rung MCSE increasing without a direct diagnostic-only explanation; ESS collapse where ESS is available; score mismatch beyond the stated rule; GPU/XLA metadata missing; unchunked Contract E score scheduled at `N=10000`; Contract E evidence used as leaderboard LGSSM score evidence; runtime gate exceeded. |
| Explanatory diagnostics | Runtime, compile time, memory, particle trend, and per-seed dispersion. |
| Not concluded | Runtime ranking does not establish correctness; value-only row does not establish score or HMC readiness. |
| Artifact | Raw ladder JSON/MD and Phase 4 result. |

## Forbidden Claims And Actions

- Do not change pass/fail thresholds after seeing results.
- Do not drop failed seeds silently.
- Do not use "feasible" to skip an adjacent rung after seeing bad results.
- Do not promote value-only rows to value+score.
- Do not compare a scoped component row as a full observed-data filtering row.
- Do not use the Contract E LGSSM `D=2`, `T=10` fixture as evidence that the
  `benchmark_lgssm_exact_oracle_m3_T50` row value or score has run.
- Do not treat the Phase 3 fixed SIR value smoke as exact nonlinear likelihood,
  score, HMC, or Zhao-Cui source-faithfulness evidence.
- Do not run the current unchunked Contract E score route at `N=10000` as a
  Phase 4 ladder cell.

## Exact Next-Phase Handoff Conditions

Advance to Phase 5 only if:

- all admitted rows have raw LEDH artifacts;
- every requested row appears in the Phase 4 status table as executed, scoped,
  or blocked;
- blocked rows have direct reasons;
- each row has value and score statuses;
- every executed value row reports the adjacent-rung value-stability result or
  is explicitly diagnostic-only;
- Contract E score rows are limited to admitted memory-safe rungs or directly
  blocked with the Phase 3 memory reason;
- the leaderboard LGSSM row has either same-target value evidence with score
  blocked, same-target value+score evidence, or a direct blocker;
- fixed spatial SIR remains value-only unless a new reviewed total-derivative
  score gate is added;
- Claude review agrees or fixable issues are patched.

## Stop Conditions

- A row/rung command runs more than 30 minutes without artifact or log progress.
- A full Phase 4 row runs more than 4 hours without a completed row artifact.
- A row repeatedly fails with nonfinite values after one reviewed repair.
- GPU memory or XLA compile behavior makes the planned ladder infeasible.
