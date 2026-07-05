# Phase 4 Result: LEDH Particle Ladders

Date: 2026-07-03

Status: `PASSED_VALUE_ONLY_FOR_ADMITTED_ROWS_SCORE_BLOCKED`

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Which admitted rows produce stable same-target LEDH value estimates and which produce admitted total-derivative scores? |
| Baseline/comparator | Existing non-LEDH leaderboard rows and row-specific exact references where available. |
| Primary pass criterion | Each requested LEDH row has either an executed same-target value row with MCSE and diagnostics or a direct blocked/scoped reason; score rows pass their separate total-derivative score criterion at an admitted same-target memory-safe rung. |
| Veto diagnostics | Wrong target; nonfinite outputs; MCSE missing; adjacent value change exceeding `5 * sqrt(mcse_a^2 + mcse_b^2)`; larger-rung MCSE increasing without explanation; score mismatch; GPU/XLA metadata missing; Contract E evidence used as leaderboard LGSSM score evidence; runtime gate exceeded. |
| Explanatory diagnostics | Runtime, compile time, memory, particle trend, per-seed dispersion, ESS. |
| Not concluded | Runtime ranking does not establish correctness; value-only rows do not establish score or HMC readiness. |
| Artifacts | Raw ladder JSON/MD artifacts and this Phase 4 result. |

## Skeptical Audit

- Wrong-target risk was real and was repaired before Phase 4 execution:
  Contract E LGSSM is route evidence only, not evidence for
  `benchmark_lgssm_exact_oracle_m3_T50`.
- The same-target LGSSM value runner records `D=3`, `T=50`, dataset seed
  `81100`, theta `[0.72, 0.55, 0.35, 0.35, 0.45]`, exact total Kalman log
  likelihood `-136.0759748579247`, and exact per-time average
  `-2.721519497158494`.
- Score evidence was not promoted from value evidence. Both executed Phase 4
  rows remain score-blocked.
- Runtime comparisons to frozen non-LEDH rows remain forbidden.

Audit result: `PHASE4_VALUE_EVIDENCE_INTERPRETABLE_SCORE_NOT_CLAIMED`.

## Commands And Artifacts

### Same-Target LGSSM Value Smoke, `N=64`

Artifacts:

- `docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-phase4-lgssm-m3-t50-same-target-value-smoke-N64-2026-07-03.json`
- `docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-phase4-lgssm-m3-t50-same-target-value-smoke-N64-2026-07-03.md`
- `docs/plans/logs/bayesfilter-ledh-inclusive-highdim-leaderboard-phase4-lgssm-m3-t50-same-target-value-smoke-N64-2026-07-03.log`

Outcome: `passed_same_target_value_smoke_score_blocked`.

### Same-Target LGSSM Value Ladder

Artifacts:

- `docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-phase4-lgssm-m3-t50-same-target-value-ladder-N1000-2026-07-03.json`
- `docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-phase4-lgssm-m3-t50-same-target-value-ladder-N1000-2026-07-03.md`
- `docs/plans/logs/bayesfilter-ledh-inclusive-highdim-leaderboard-phase4-lgssm-m3-t50-same-target-value-ladder-N1000-2026-07-03.log`
- `docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-phase4-lgssm-m3-t50-same-target-value-ladder-N10000-2026-07-03.json`
- `docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-phase4-lgssm-m3-t50-same-target-value-ladder-N10000-2026-07-03.md`
- `docs/plans/logs/bayesfilter-ledh-inclusive-highdim-leaderboard-phase4-lgssm-m3-t50-same-target-value-ladder-N10000-2026-07-03.log`

| N | Mean average log likelihood | SD | MCSE | Exact average | Delta | Rel. error | Min ESS range | Status |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| 1000 | -2.720394775391 | 0.003493758736 | 0.001562456406 | -2.721519497158 | 0.001124721768 | 0.0413% | 285.55 to 316.40 | passed value-only |
| 10000 | -2.719201477051 | 0.0002653499996 | 0.0001186681274 | -2.721519497158 | 0.002318020108 | 0.0852% | 2872.84 to 3003.67 | passed value-only |

Adjacent-rung rule:

- `abs(mean_10000 - mean_1000) = 0.001193298340`.
- `5 * sqrt(mcse_1000^2 + mcse_10000^2) = 0.007834781660`.
- Result: `passed`.
- MCSE decreased from `0.001562456406` to `0.0001186681274`.

Score status: `blocked_score_same_target_total_derivative_not_implemented`.

### Fixed Spatial SIR Value Ladder

Artifacts:

- `docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-phase4-fixed-sir-value-ladder-N1000-2026-07-03.json`
- `docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-phase4-fixed-sir-value-ladder-N1000-2026-07-03.md`
- `docs/plans/logs/bayesfilter-ledh-inclusive-highdim-leaderboard-phase4-fixed-sir-value-ladder-N1000-2026-07-03.log`
- `docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-phase4-fixed-sir-value-ladder-N10000-2026-07-03.json`
- `docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-phase4-fixed-sir-value-ladder-N10000-2026-07-03.md`
- `docs/plans/logs/bayesfilter-ledh-inclusive-highdim-leaderboard-phase4-fixed-sir-value-ladder-N10000-2026-07-03.log`

| N | Mean log likelihood | SD | MCSE | Min ESS range | Status |
| ---: | ---: | ---: | ---: | --- | --- |
| 1000 | -901.605566406250 | 1.206453540503 | 0.539542425652 | 606.38 to 672.22 | passed value-only |
| 10000 | -902.830151367187 | 0.465598796261 | 0.208222111736 | 6432.78 to 6511.61 | passed value-only |

Adjacent-rung rule:

- `abs(mean_10000 - mean_1000) = 1.224584960937`.
- `5 * sqrt(mcse_1000^2 + mcse_10000^2) = 2.891636547417`.
- Result: `passed`.
- MCSE decreased from `0.539542425652` to `0.208222111736`.

Score status: blocked. This value ladder is not score, HMC, exact nonlinear
likelihood, or Zhao-Cui TT/SIRT source-faithfulness evidence.

## Local Checks

Commands:

```bash
python -m py_compile docs/benchmarks/benchmark_ledh_same_target_lgssm_m3_t50_value.py docs/benchmarks/benchmark_two_lane_highdim_ledh_leaderboard.py
python -m pytest tests/test_two_lane_highdim_ledh_leaderboard.py -q
git diff --check
```

Results:

- `py_compile`: passed.
- focused pytest: `6 passed`.
- `git diff --check`: passed.

## Decision Table

| Decision | Status |
| --- | --- |
| Leaderboard LGSSM value | passed same-target value-only at `N=1000` and `N=10000` |
| Leaderboard LGSSM score | blocked; same-target total derivative is not implemented in the value runner |
| Fixed spatial SIR value | passed value-only at `N=1000` and `N=10000` |
| Fixed spatial SIR score | blocked; not tested and not claimed |
| Parameterized SIR | scoped component row only |
| Actual SV, KSC SV, predator-prey, generalized SV | blocked until reviewed same-target LEDH adapters exist |
| Runtime ranking against frozen non-LEDH rows | forbidden |

## Phase 5 Handoff

Phase 5 may merge fresh LEDH rows into the leaderboard with these statuses:

- `benchmark_lgssm_exact_oracle_m3_T50`: `executed_value_only_score_blocked`,
  value from the same-target `N=10000` artifact, MCSE reported, exact Kalman
  value comparator reported, score blocked.
- `zhao_cui_spatial_sir_austria_j9_T20`: `executed_value_only_score_blocked`,
  value from the fixed SIR `N=10000` artifact, MCSE reported, score blocked.
- `zhao_cui_spatial_sir_austria_j9_T20_parameterized_logscale`: scoped
  component row only.
- Actual SV, KSC SV, predator-prey, and generalized SV: blocked until
  same-target adapters exist.

Do not merge the Contract E LGSSM score diagnostic as the leaderboard LGSSM
score. That would be wrong target evidence.

## Post-Run Red Team

The strongest alternative explanation for both value ladders is ordinary Monte
Carlo variation across only five seeds. That is why the artifact keeps MCSE and
adjacent-rung stability separate from score and HMC claims.

For LGSSM, the value evidence is strong enough for a value-only row because the
target is exact and the per-time average relative error is below `0.1%` at
`N=10000`. It is not score evidence.

For fixed SIR, there is no exact value comparator in this phase. The result
shows finite, stable adjacent-rung LEDH value behavior for the fixed row, not
exact likelihood correctness.

## Nonclaims

- Phase 4 does not certify any LEDH total-derivative score for the leaderboard.
- Phase 4 does not certify HMC readiness.
- Phase 4 does not rank LEDH runtime against frozen non-LEDH rows.
- Phase 4 does not claim Zhao-Cui TT/SIRT source-faithfulness.
