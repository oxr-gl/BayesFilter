# LEDH Leaderboard Score Repair Master Program

Date: 2026-07-03

Status: `DRAFT_PENDING_REVIEW`

## Resume Amendment: Same-Route Manual-VJP Gate

This program resumes after Phase 2 retracted the tape-gradient LGSSM score
attempt.  Phase 3 is now the active phase.

From this point forward:

- LEDH score computation must use manual VJP or a documented analytical
  equivalent.  `GradientTape` and `ForwardAccumulator` are forbidden for
  production LEDH score computation.
- A row may be promoted to `executed_value_score` only if the reported value
  and score come from the same scalar algorithmic route.  The merged
  leaderboard admission guard must require `value_route_id == score_route_id`
  and `value_score_route_status == same_route_value_score`.
- Finite-difference checks must perturb the same scalar objective whose value
  is reported.  An FD check of a different scalar is wrong-target evidence.
- CPU-hidden diagnostics may be local debugging evidence only.  Material LEDH
  score evidence for the default route still requires trusted GPU/XLA/TF32
  execution after local no-autodiff checks pass.

## Objective

Repair LEDH leaderboard score admission row by row.  Here `score` means the
total derivative of the stated leaderboard log likelihood target with respect
to the stated parameter coordinates.

Plainly: a derivative that treats parameter-dependent LEDH flow, transport,
proposal, reset, or likelihood quantities as constants is a partial derivative.
It is wrong for MLE or HMC score claims unless the row explicitly declares that
partial derivative as a different diagnostic quantity.

## Current Baseline

The current LEDH-inclusive highdim leaderboard is:

- `docs/plans/bayesfilter-two-lane-highdim-ledh-inclusive-leaderboard-results-2026-07-03.json`
- `docs/plans/bayesfilter-two-lane-highdim-ledh-inclusive-leaderboard-results-2026-07-03.md`

No LEDH leaderboard score row is admitted there.

Already supported:

- LGSSM row `benchmark_lgssm_exact_oracle_m3_T50` has same-target LEDH
  value-only evidence at `N=10000`.
- Fixed spatial SIR row `zhao_cui_spatial_sir_austria_j9_T20` has fixed-row
  LEDH value-only evidence at `N=10000`.
- The corrected LEDH total-VJP route passed scoped P8p SIR diagnostics and a
  trusted GPU/XLA/TF32 raw-direction gate through `N=1000,T=3`.

Not supported:

- Contract E LGSSM is not the leaderboard LGSSM row and must not be used as
  same-target leaderboard score evidence.
- P8p SIR diagnostics are not full observed-data leaderboard SIR scores.
- Actual SV, KSC SV, predator-prey, and generalized SV have no admitted
  same-target LEDH adapter for score repair.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | For each highdim leaderboard row, can LEDH compute the total derivative of the exact stated leaderboard likelihood target in the stated parameter coordinates? |
| Baseline/comparator | Row-specific exact derivative when available; otherwise same-scalar finite differences with fixed randomness and a declared Monte Carlo uncertainty rule. |
| Primary pass criterion | A row can move to `executed_value_score` for LEDH only after same-target value admission, total-derivative implementation, and row-specific score validation pass. |
| Veto diagnostics | Wrong row target; value/score route mismatch; tape/autodiff score route; partial derivative called score; missing parameter dependency; nonfinite value or score; FD/exact mismatch beyond predeclared rule; missing GPU/XLA/TF32 evidence for production LEDH route; missing artifact. |
| Explanatory diagnostics | Runtime, compile time, memory, ESS, particle trend, per-seed dispersion, score covariance conditioning. |
| Not concluded | Passing a score row does not by itself prove HMC readiness, posterior correctness, scientific superiority, or runtime ranking against frozen non-LEDH rows. |
| Artifacts | Phase subplans/results, row inventories, raw JSON/Markdown outputs, logs, Claude review records, final merged leaderboard if any row is admitted. |

## Score Admission Rule

For a row with exact score:

- use the exact score as the primary comparator;
- report and validate the value from the same scalar LEDH route that produces
  the score;
- admit only if every reported LEDH score coordinate passes the predeclared
  tolerance or the result artifact records a row-specific blocker.

For a stochastic same-scalar FD score:

- use fixed dataset and fixed randomness where the row route permits it;
- perturb the same scalar objective whose value is reported;
- report seed-mean, sample SD, and MCSE;
- apply the same HMC-direction rule only when justified for that row:
  within `2 MCSE`, or within `4 MCSE` with MCSE decreasing as `N` increases,
  or relative error below `1%`.

These rules are row-admission rules only.  They are not posterior correctness
or HMC production-readiness rules.

## Phase Index

| Phase | Name | Main subplan | Required result |
| --- | --- | --- | --- |
| 0 | Launch Boundary And Score Meaning Freeze | `docs/plans/bayesfilter-ledh-leaderboard-score-repair-phase0-launch-boundary-score-meaning-subplan-2026-07-03.md` | `docs/plans/bayesfilter-ledh-leaderboard-score-repair-phase0-launch-boundary-score-meaning-result-2026-07-03.md` |
| 1 | Row Score Inventory | `docs/plans/bayesfilter-ledh-leaderboard-score-repair-phase1-row-score-inventory-subplan-2026-07-03.md` | `docs/plans/bayesfilter-ledh-leaderboard-score-repair-phase1-row-score-inventory-result-2026-07-03.md` |
| 2 | Same-Target LGSSM Score Repair | `docs/plans/bayesfilter-ledh-leaderboard-score-repair-phase2-lgssm-score-repair-subplan-2026-07-03.md` | `docs/plans/bayesfilter-ledh-leaderboard-score-repair-phase2-lgssm-score-repair-result-2026-07-03.md` |
| 3 | Memory-Safe GPU/XLA Score Scaling | `docs/plans/bayesfilter-ledh-leaderboard-score-repair-phase3-memory-safe-gpu-xla-score-subplan-2026-07-03.md` | `docs/plans/bayesfilter-ledh-leaderboard-score-repair-phase3-memory-safe-gpu-xla-score-result-2026-07-03.md` |
| 4 | Fixed SIR Score Target Decision | `docs/plans/bayesfilter-ledh-leaderboard-score-repair-phase4-fixed-sir-score-target-subplan-2026-07-03.md` | `docs/plans/bayesfilter-ledh-leaderboard-score-repair-phase4-fixed-sir-score-target-result-2026-07-03.md` |
| 5 | Nonlinear Row Adapter Admission | `docs/plans/bayesfilter-ledh-leaderboard-score-repair-phase5-nonlinear-adapter-admission-subplan-2026-07-03.md` | `docs/plans/bayesfilter-ledh-leaderboard-score-repair-phase5-nonlinear-adapter-admission-result-2026-07-03.md` |
| 6 | Admitted Nonlinear Score Repair | `docs/plans/bayesfilter-ledh-leaderboard-score-repair-phase6-nonlinear-score-repair-subplan-2026-07-03.md` | `docs/plans/bayesfilter-ledh-leaderboard-score-repair-phase6-nonlinear-score-repair-result-2026-07-03.md` |
| 7 | Leaderboard Merge | `docs/plans/bayesfilter-ledh-leaderboard-score-repair-phase7-leaderboard-merge-subplan-2026-07-03.md` | `docs/plans/bayesfilter-ledh-leaderboard-score-repair-phase7-leaderboard-merge-result-2026-07-03.md` |
| 8 | Closeout And Reset Memo | `docs/plans/bayesfilter-ledh-leaderboard-score-repair-phase8-closeout-reset-subplan-2026-07-03.md` | `docs/plans/bayesfilter-ledh-leaderboard-score-repair-phase8-closeout-reset-result-2026-07-03.md` |

## Skeptical Plan Audit

This plan is allowed to start only if the following checks pass:

- Baseline is the July 3 LEDH-inclusive leaderboard, not Contract E.
- Score admission is based on total derivatives of the row target, not partial
  derivatives or diagnostics from another row.
- Value-only evidence cannot be promoted to score evidence.
- P8p SIR total-VJP evidence cannot be promoted to full SIR leaderboard score
  without a same-target observed-data row.
- GPU/XLA/TF32 production claims require trusted GPU execution.
- Runtime comparisons against frozen non-LEDH rows remain forbidden.

Current audit result: `PASS_TO_PLAN_REVIEW`.  The plan may be sent to Claude as
read-only reviewer.  Execution starts only after the review gate agrees or a
human explicitly accepts a documented review blocker.

## Repair Loop

For every material phase:

1. run the local checks named in that phase subplan;
2. write the phase result or blocker record;
3. draft or refresh the next subplan;
4. run a bounded Claude read-only review for material subplans/results;
5. patch fixable findings visibly and rerun focused checks;
6. stop after five Claude review rounds for the same blocker.

Claude is a reviewer only.  Claude cannot authorize scientific claims, runtime
boundary crossings, product claims, funding decisions, model-file changes, or
human approvals.

## Human Approval Surface

The following actions require trusted or explicit approval before execution:

- Claude Code review gate calls;
- GPU/CUDA/TensorFlow/XLA runs;
- overnight or long-running commands;
- package installation, network fetches, destructive filesystem actions, or
  changes to default repository policy.

The current user instruction asks to launch after the plan is written.  The
launch remains visible and recoverable; detached execution is not used.
