# Reset Memo: LEDH No-Tape Total Sinkhorn VJP

Date: 2026-07-04

Status: `CURRENT_HANDOFF`

## Short Answer

The manual no-tape total VJP route now works for the checked local targets.
The tiny-prefix LGSSM score computes the total derivative of the same
LEDH-PFPF-OT scalar and matches same-scalar finite differences.  The full T50
GPU leaderboard score is not admitted yet.

## What Changed

- Added a no-tape total finite streaming Sinkhorn VJP primitive route.
- Replaced the P8p SIR full-mode transport local tape with explicit manual
  VJPs.
- Added an opt-in LGSSM `--score-mode manual-reverse` route.
- Added same-scalar finite-difference diagnostics for the LGSSM manual score.
- Fixed the LGSSM initial-particle `phi` chain-rule reduction bug by reducing
  over particles only, preserving one contribution per state coordinate.
- Fixed stale nested LGSSM score metadata so `target_identity.score_status`
  matches the top-level result when manual score mode runs.

## Current Evidence

- Primitive no-tape VJP checks passed.
- P8p SIR scoped regression passed.
- LGSSM tiny-prefix same-scalar FD passed:
  - max absolute score error: `9.465646044759524e-09`;
  - max relative score error: `8.792013654782173e-10`;
  - manual score:
    `[4.6517339713326, -2.2383309550434705, 0.6785225994442738, 8.17939757825367, 10.766186687265593]`.
- Phase 4/5 Claude read-only review returned `REVIEW_STATUS=agreed`,
  `VERDICT=AGREE`.

## Current Boundary

The phrase "score" means the total derivative of the same scalar value route.
Do not call a stopped partial derivative a score unless the stopped scalar is
explicitly declared as the target.

The full T50 LGSSM leaderboard score remains blocked by:
`blocked_material_gate_not_full_gpu_row`.

This memo does not claim HMC readiness, posterior correctness, runtime
superiority, or nonlinear model score correctness.

## Important Artifacts

- Closeout:
  `docs/plans/bayesfilter-ledh-no-tape-total-sinkhorn-vjp-phase5-closeout-result-2026-07-04.md`
- Tiny-prefix JSON:
  `docs/plans/bayesfilter-ledh-no-tape-total-sinkhorn-vjp-phase4-lgssm-score-admission-tiny-prefix-2026-07-04.json`
- LGSSM runner:
  `docs/benchmarks/benchmark_ledh_same_target_lgssm_m3_t50_value.py`
- LGSSM tests:
  `tests/test_ledh_lgssm_manual_score_phase4.py`
- Visible ledger:
  `docs/plans/bayesfilter-ledh-no-tape-total-sinkhorn-vjp-visible-execution-ledger-2026-07-04.md`

## Next Safe Action

To admit the full LGSSM score row, create a separate reviewed full-row GPU/XLA
score gate that runs the same value/score route on `T=50` with trusted GPU
execution.  To extend to nonlinear models, create a separate adapter program
that proves same-scalar value/score consistency for each model before claiming
score correctness.
