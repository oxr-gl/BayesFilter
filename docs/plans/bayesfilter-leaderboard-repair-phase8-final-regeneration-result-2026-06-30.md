# Phase 8 result: final regeneration and release note

Date: 2026-06-30

Status: `PASSED_FINAL_REVIEW_PENDING_CLAUDE_RESULT_REVIEW`

## Phase Objective

Regenerate the final leaderboard and write the release/reset note summarizing
fixed cells, remaining blockers, evidence, and nonclaims.

## Evidence Contract

| Field | Result |
| --- | --- |
| Question | Is the final leaderboard internally consistent and honest about value, analytical score, target, batch, and GPU/XLA status? |
| Baseline/comparator | Initial June 30 leaderboard, phase results, and immutable Phase 7 preservation baseline. |
| Primary criterion | Met locally. Final artifacts contain no stale actual-SV `not_same_target` blocker, no fixed-SGQF analytical-score row with tape/autodiff provenance, no hidden blockers, and no Phase 7 timing fields that can rank or admit blocked cells. |
| Veto diagnostics | Not fired locally. P91 sidecar timing remains under `p91_scoped_evidence.phase7_sidecar_performance`; blocked/value-only rows are not timing-rankable; local checks passed. |
| Explanatory diagnostics | Existing source runtimes and P91 sidecar CPU/GPU/XLA timings remain explanatory only. |
| Not concluded | No scientific superiority, exact nonlinear likelihood, posterior convergence, HMC production readiness, or production-GPU timing packet. |
| Artifact | Final leaderboard JSON/Markdown, reset/release memo, this Phase 8 result, visible stop handoff, and Claude review ledger. |

## Final Artifacts

- `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-06-30.json`
- `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-06-30.md`
- `docs/plans/bayesfilter-two-lane-highdim-leaderboard-phase7-preservation-baseline-2026-06-30.json`
- `docs/plans/bayesfilter-leaderboard-repair-reset-memo-2026-06-30.md`
- `docs/plans/bayesfilter-leaderboard-repair-visible-stop-handoff-2026-06-30.md`
- `docs/plans/bayesfilter-leaderboard-repair-claude-review-ledger-2026-06-30.md`

## Final Row Summary

| Row | Executed algorithms | Full three-way ready | Blocked/missing algorithms |
| --- | --- | --- | --- |
| `benchmark_lgssm_exact_oracle_m3_T50` | fixed-SGQF, UKF, Zhao-Cui | true | none |
| `zhao_cui_sv_actual_nongaussian_T1000` | fixed-SGQF, UKF, Zhao-Cui | true | none |
| `zhao_cui_sv_ksc_gaussian_mixture_surrogate_T1000` | fixed-SGQF, UKF, Zhao-Cui | true | none |
| `zhao_cui_spatial_sir_austria_j9_T20` | UKF | false | fixed-SGQF, Zhao-Cui |
| `zhao_cui_predator_prey_T20` | UKF | false | fixed-SGQF, Zhao-Cui |
| `zhao_cui_generalized_sv_synthetic_from_estimated_values` | UKF | false | fixed-SGQF, Zhao-Cui |

## Local Checks

CPU-only TensorFlow commands intentionally used `CUDA_VISIBLE_DEVICES=-1`
before framework import. The regeneration emitted CUDA factory/cuInit warning
noise in CPU-only mode; per repo policy, this is not GPU-stack evidence.

- Baseline hash check:
  `docs/plans/bayesfilter-two-lane-highdim-leaderboard-phase7-preservation-baseline-2026-06-30.json`
  matched SHA-256
  `cb71a48830d6daf62062a3dec55ad93f238c1d41aad6a75e5f1bfc6b803c6f2f`.
- `CUDA_VISIBLE_DEVICES=-1 python -m py_compile docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py tests/test_two_lane_highdim_leaderboard_phase3.py tests/test_two_lane_highdim_leaderboard_phase4.py tests/test_two_lane_highdim_leaderboard_phase5.py tests/test_two_lane_highdim_leaderboard_phase6.py tests/test_two_lane_highdim_leaderboard_phase7.py`: passed.
- `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py --output docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-06-30.json --markdown-output docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-06-30.md`: passed.
- `CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/test_two_lane_highdim_leaderboard_phase3.py tests/test_two_lane_highdim_leaderboard_phase4.py tests/test_two_lane_highdim_leaderboard_phase5.py tests/test_two_lane_highdim_leaderboard_phase6.py tests/test_two_lane_highdim_leaderboard_phase7.py -q`: passed, 9 tests, 2 warnings, 382.52 seconds.
- Final schema and Phase 7 preservation validation against the immutable
  baseline: passed.

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not concluded |
| --- | --- | --- | --- | --- | --- |
| Close the leaderboard repair program after final Claude result review | Passed locally | No local veto fired | Remaining blockers require new evaluator/adaptor work, not administrative approval | Start a separate governed implementation program for remaining blocked rows | No exact nonlinear likelihood, scientific superiority, production GPU timing, or HMC readiness |

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `ef119f8bdb17b206339de92d722344a448eea745`; working tree dirty. |
| Commands | Listed in Local Checks. |
| Environment | `tf-gpu` Python environment; CPU-only checks hid GPU with `CUDA_VISIBLE_DEVICES=-1`. |
| CPU/GPU status | No new GPU run in Phase 8. Reused P91 GPU/XLA evidence only as sidecar. |
| Data version | P8D numeric artifact plus Phase 7 preservation baseline. |
| Random seeds | N/A for Phase 8 regeneration/validation. |
| Wall time | Focused pytest: 382.52 seconds. |
| Output artifacts | Listed in Final Artifacts. |
| Plan file | `docs/plans/bayesfilter-leaderboard-repair-phase8-final-regeneration-subplan-2026-06-30.md`. |
| Result file | `docs/plans/bayesfilter-leaderboard-repair-phase8-final-regeneration-result-2026-06-30.md`. |

## Post-Run Red-Team Note

Strongest alternative explanation: users could still over-read the table as a
complete production benchmark because several high-dimensional rows are
executed and P91 has sidecar GPU/XLA timings.

Mitigation: final artifacts state that rows with blocked algorithms are not
full three-way rows, main rows are not a production-GPU timing packet, and P91
timings are local complete-data sidecar evidence only. The preservation
validator also prevents P91 sidecar timing from leaking into main timing/ranking
fields.

## Handoff

No next phase remains in this runbook. The visible stop handoff and reset memo
summarize remaining implementation work for a new governed program.
