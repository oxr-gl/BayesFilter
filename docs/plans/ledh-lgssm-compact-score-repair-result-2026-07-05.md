# LEDH LGSSM Compact Score Repair Result

Date: 2026-07-05

## Decision Table

| Item | Status |
| --- | --- |
| Root cause | Implementation bug in compact LGSSM score posterior information term: the compact path used a 2D observation matrix where the implemented LEDH flow uses a per-particle observation Jacobian. |
| Code repair | Done. Compact score uses the per-particle Jacobian path and is wired as the admitted no-autodiff score route. |
| Old route | Historical/manual-reverse route remains diagnostic only and cannot be admitted. |
| Unit tests | Passed: `pytest -q tests/test_ledh_lgssm_manual_score_phase4.py` gave 6 passed. |
| CPU CLI smoke | Passed as a diagnostic. Compact score FD passed with float64 and the artifact correctly blocked admission because it was CPU/prefix. |
| GPU CLI smoke | Passed as a diagnostic. Compact score and value tensors were on GPU; default float32 FD step `1e-3` passed. |
| Full leaderboard row | Not run. Escalation reviewer timed out twice before launch. |

## Evidence

- CPU smoke artifact:
  `docs/plans/ledh-lgssm-compact-score-cli-smoke-2026-07-05.json`
- GPU smoke artifact:
  `docs/plans/ledh-lgssm-compact-score-gpu-smoke-default-fd-2026-07-05.json`
- Full-row run plan:
  `docs/plans/ledh-lgssm-compact-score-full-row-run-plan-2026-07-05.md`

## Important Findings

The score formula now passes the same-scalar finite-difference check in float64
and in GPU float32/TF32 when the finite-difference step is numerically
appropriate. The earlier GPU failure at step `1e-5` was a finite-difference
roundoff problem for float32/TF32, not evidence of a mathematical mismatch.

The runner now requires the full row identity before admitting the score:
seeds `81120,81121,81122,81123,81124`, `N=1000`, `T=50`, active-all transport,
10 Sinkhorn iterations, epsilon `0.5`, GPU value placement, GPU score placement,
finite output, and same-scalar FD pass.

## Nonclaims

This result does not prove exact Kalman score correctness, posterior
correctness, HMC/NUTS readiness, superiority against other algorithms, or
nonlinear-row validity.

## Blocker

The full-row GPU command was not executed because the managed escalation review
timed out twice before command launch. This is an execution-permission blocker,
not a code or math failure.
