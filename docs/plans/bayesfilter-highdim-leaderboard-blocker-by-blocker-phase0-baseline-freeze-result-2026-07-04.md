# Phase 0 Result: Baseline Freeze And Launch Gate

Date: 2026-07-04

Status: `PASS_PHASE0_BASELINE_FREEZE`

## Decision Table

| Field | Decision |
| --- | --- |
| Decision | Launch the blocker-by-blocker program from the July 3 combined leaderboard baseline. |
| Primary criterion status | Passed: the baseline artifacts exist, the candidate phase list covers the current remaining blocker families, and the repair-priority order is now stated honestly as a planning order rather than a literal artifact row order. |
| Veto diagnostic status | Passed: no row repair, GPU/XLA, HMC, package/network, or long benchmark was run in Phase 0. |
| Main uncertainty | Phase 0 does not repair any row and does not prove the later same-target scores. |
| Next justified action | Review and execute Phase 1 full-row LGSSM GPU/XLA score gate. |
| Not concluded | No row repair, no score correctness claim, no GPU readiness claim, no HMC readiness claim, and no scientific validity claim. |

## Baseline Integrity

The July 3 leaderboard artifacts were treated as read-only Phase 0 inputs.

| Artifact | SHA256 |
| --- | --- |
| `docs/plans/bayesfilter-two-lane-highdim-ledh-inclusive-leaderboard-results-2026-07-03.json` | `a53a5f646fbda35062e294e40225bd3f9d8ffc1a41a17ef37ca2b03b53c9e6df` |
| `docs/plans/bayesfilter-two-lane-highdim-ledh-inclusive-leaderboard-results-2026-07-03.md` | `68123024b7e172bc52cd50fd4b8c9da266066539208db9d20dae417a95b7ff1a` |

The JSON artifact contains seven row-summary entries, including the scoped
parameterized SIR row as diagnostic-only context. The repair-priority plan
covers the six current blocker families plus UKF cleanup and final
regeneration.

## Coverage Check

| Planned phase | Covered blocker family or role |
| --- | --- |
| Phase 1 | `benchmark_lgssm_exact_oracle_m3_T50` full-row LGSSM admission gate |
| Phase 2 | `zhao_cui_sv_actual_nongaussian_T1000` |
| Phase 3 | `zhao_cui_sv_ksc_gaussian_mixture_surrogate_T1000` |
| Phase 4 | `zhao_cui_generalized_sv_synthetic_from_estimated_values` |
| Phase 5 | `zhao_cui_spatial_sir_austria_j9_T20` |
| Phase 6 | `zhao_cui_predator_prey_T20` |
| Phase 7 | UKF analytical-score cleanup |
| Phase 8 | Final regeneration and closeout |

The scoped parameterized SIR row is not promoted to a main repair phase.

## Checks Run

| Check | Result |
| --- | --- |
| Baseline artifact hash check | Passed |
| JSON row-summary inventory | Passed |
| Remaining-blockers ledger cross-check | Passed |
| `git diff --check` on the planning files touched by the launch gate | Passed |

## Nonclaims

- This does not certify LEDH total-derivative score correctness.
- This does not certify HMC readiness.
- This does not certify posterior correctness or scientific superiority.
- This does not rank runtime across algorithms.

## Handoff

Phase 0 is complete. Phase 1 may begin after the refreshed Phase 1 subplan is
reviewed. Phase 1 must treat the tiny-prefix LGSSM route as diagnostic only
and may admit the full `T=50` row only through trusted same-route GPU/XLA
evidence.
