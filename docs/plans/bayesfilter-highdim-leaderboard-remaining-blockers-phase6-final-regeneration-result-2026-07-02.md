# Phase 6 Result: Final Regeneration And Closeout

Date: 2026-07-02

Status: `PASS_PHASE6_FINAL_REGENERATION_WITH_REMAINING_GAPS_PRESERVED`

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| Accept regenerated highdim leaderboard artifacts as the closeout artifact for this runbook | Passed: regenerated JSON/Markdown preserve Phase 1/2 Zhao-Cui admissions, Phase 3/4 blockers, and Phase 5 readiness sidecar/no-claim statuses | Passed: preservation check `PASS`; no GPU/XLA command run; no autodiff/FD score admitted for repaired Zhao-Cui rows | Full payload tests are expensive and one stale assertion had to be corrected after actual-SV/KSC became full-ready | Use the regenerated artifacts for reporting; future work should target remaining SGQF and UKF/SIR blockers under separate subplans | Exact nonlinear likelihood correctness, posterior correctness, HMC convergence, GPU/XLA readiness, production release readiness |

## Final Artifacts

- JSON leaderboard:
  `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-02.json`
- Markdown leaderboard:
  `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-02.md`
- Preservation check:
  `docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-phase6-preservation-check-2026-07-02.json`

## Final Row Summary

| Row | Full three-way ready | Score-admitted algorithms |
| --- | --- | --- |
| `benchmark_lgssm_exact_oracle_m3_T50` | `true` | `fixed_sgqf`, `ukf`, `zhao_cui_scalar_or_multistate` |
| `zhao_cui_sv_actual_nongaussian_T1000` | `true` | `fixed_sgqf`, `ukf`, `zhao_cui_scalar_or_multistate` |
| `zhao_cui_sv_ksc_gaussian_mixture_surrogate_T1000` | `true` | `fixed_sgqf`, `ukf`, `zhao_cui_scalar_or_multistate` |
| `zhao_cui_spatial_sir_austria_j9_T20` | `false` | none |
| `zhao_cui_predator_prey_T20` | `false` | `zhao_cui_scalar_or_multistate` |
| `zhao_cui_generalized_sv_synthetic_from_estimated_values` | `false` | `zhao_cui_scalar_or_multistate` |

## Checks Run

- CPU-only final regeneration:
  `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py --output docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-02.json --markdown-output docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-02.md`
  passed after approximately 47 minutes. TensorFlow emitted CUDA registration
  warnings even though GPU was intentionally hidden; no GPU/XLA evidence is
  claimed.
- `python -m json.tool docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-02.json`: passed.
- Preservation check command from the Phase 6 subplan: passed with status
  `PASS`.
- Focused pytest bundle:
  `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/test_two_lane_highdim_leaderboard_analytical_scores.py tests/highdim/test_phase1_predator_prey_t20_zhaocui_admission.py tests/highdim/test_phase2_generalized_sv_exact_source_row_admission.py`
  initially returned `13 passed, 1 failed, 2 warnings` after approximately
  48 minutes. The failure was a stale expectation that actual-SV remained
  not full-ready; the regenerated payload now correctly marks actual-SV and
  KSC as full-ready because all three algorithms have admitted scores.
- Narrow recheck after the stale expectation repair:
  `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/test_two_lane_highdim_leaderboard_analytical_scores.py::test_row_summary_full_ready_requires_all_algorithms_with_admitted_scores`
  passed with `1 passed, 2 warnings` after approximately 46 minutes.
- `git diff --check` over Phase 6 artifacts, regenerated artifacts, the
  updated test, and ledgers: passed.

## Remaining Gaps

- `zhao_cui_spatial_sir_austria_j9_T20` remains blocked for full observed-data
  filtering score admission because no reviewed full-row free-theta binding is
  available. P91 local complete-data evidence remains sidecar only.
- Predator-prey UKF and generalized-SV UKF remain value-only because no
  reviewed exact-row principal-square-root or factor-propagating SR-UKF manual
  derivative binding exists for those rows.
- Predator-prey fixed-SGQF remains blocked by target alignment/evaluator
  wiring.
- Generalized-SV fixed-SGQF remains blocked by exact source-row evaluator
  wiring.
- Batch parity, trusted GPU/XLA, and multi-seed score-at-true readiness remain
  deferred/no-claim for the two newly admitted Zhao-Cui rows.

## Nonclaims

- The regenerated leaderboard does not prove exact nonlinear likelihood
  correctness.
- The regenerated leaderboard does not certify posterior correctness, HMC
  convergence, GPU/XLA readiness, or production release readiness.
- Phase 5 readiness artifacts are sidecar/no-claim diagnostics and do not
  promote row admission.
- Historical SVD UKF, autodiff, finite-difference, and tape-gradient scores are
  not admitted as analytical leaderboard scores for the repaired rows.

## Handoff

The runbook can close after final Claude review of this result and stop
handoff. Future work should use a new subplan for remaining UKF/SIR/SGQF
blockers rather than reopening this completed remaining-blockers runbook.
