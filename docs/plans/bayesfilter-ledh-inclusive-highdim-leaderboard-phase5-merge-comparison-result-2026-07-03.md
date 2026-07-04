# Phase 5 Result: Merge And Cross-Algorithm Comparison

Date: 2026-07-03

Status: `PASSED_MERGED_VALUE_ONLY_LEDGER_SCORE_BLOCKED`

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the merged leaderboard compare LEDH with the other algorithms on every row while preserving target and score status? |
| Baseline/comparator | July 3 non-LEDH highdim leaderboard plus Phase 4 LEDH value artifacts. |
| Primary pass criterion | Merged artifact exists and has no hidden missing LEDH rows, no unsupported score rows, no baseline mutation, explicit frozen-vs-fresh provenance, and value-only rows labeled directly. |
| Veto diagnostics | Missing row; hidden blocked row; Contract E LGSSM fixture used as leaderboard score evidence; value-only row ranked as score-ready; scoped row ranked as full row; baseline row changed without recorded reason; runtime cross-ranking in frozen-baseline mode. |
| Explanatory diagnostics | Runtime and MCSE comparisons. |
| Not concluded | No posterior correctness, no HMC readiness, no broad superiority claim. |
| Artifact | Merged JSON/MD and this Phase 5 result. |

## Skeptical Audit

- Wrong-target risk is controlled by merging only the same-target LGSSM
  `m3_T50` value artifact, not the Contract E route diagnostic.
- Score-proxy risk is controlled by leaving every LEDH score as blocked.
- Runtime fairness risk is controlled by `runtime_cross_ranking_allowed: false`
  and per-row `runtime_rankable` flags set to `false`.
- Hidden-row risk is controlled by requiring all seven model rows and all four
  comparison algorithms per row.
- Frozen-baseline mutation risk is controlled by labeling non-LEDH rows with
  `comparator_provenance: frozen_non_ledh_baseline`.

Audit result: `PHASE5_MERGE_EVIDENCE_INTERPRETABLE`.

## Generated Artifacts

- JSON:
  `docs/plans/bayesfilter-two-lane-highdim-ledh-inclusive-leaderboard-results-2026-07-03.json`
- Markdown:
  `docs/plans/bayesfilter-two-lane-highdim-ledh-inclusive-leaderboard-results-2026-07-03.md`
- Merge script:
  `docs/benchmarks/benchmark_two_lane_highdim_ledh_inclusive_results.py`

## Merged LEDH Row Statuses

| Row | LEDH status | Avg loglik | MCSE | Score status | Runtime rankable |
| --- | --- | ---: | ---: | --- | --- |
| `benchmark_lgssm_exact_oracle_m3_T50` | `executed_value_only_score_blocked` | -2.719201477051 | 0.0001186681274 | `blocked_score_same_target_total_derivative_not_implemented` | false |
| `zhao_cui_sv_actual_nongaussian_T1000` | `blocked` |  |  | `blocked_score` | false |
| `zhao_cui_sv_ksc_gaussian_mixture_surrogate_T1000` | `blocked` |  |  | `blocked_score` | false |
| `zhao_cui_spatial_sir_austria_j9_T20` | `executed_value_only_score_blocked` | -45.141507568359 | 0.010411105587 | `blocked_score_for_full_leaderboard_row` | false |
| `zhao_cui_spatial_sir_austria_j9_T20_parameterized_logscale` | `scoped_component_status_only` |  |  | `scoped_score_diagnostic_not_full_observed_data_score` | false |
| `zhao_cui_predator_prey_T20` | `blocked` |  |  | `blocked_score` | false |
| `zhao_cui_generalized_sv_synthetic_from_estimated_values` | `blocked` |  |  | `blocked_score` | false |

## Local Checks

Commands:

```bash
python -m py_compile docs/benchmarks/benchmark_two_lane_highdim_ledh_inclusive_results.py docs/benchmarks/benchmark_ledh_same_target_lgssm_m3_t50_value.py docs/benchmarks/benchmark_two_lane_highdim_ledh_leaderboard.py
python -m pytest tests/test_two_lane_highdim_ledh_leaderboard.py -q
python docs/benchmarks/benchmark_two_lane_highdim_ledh_inclusive_results.py --output docs/plans/bayesfilter-two-lane-highdim-ledh-inclusive-leaderboard-results-2026-07-03.json --markdown-output docs/plans/bayesfilter-two-lane-highdim-ledh-inclusive-leaderboard-results-2026-07-03.md
```

Results:

- `py_compile`: passed.
- focused pytest: `8 passed`.
- merged artifact generation: passed.

## Decision Table

| Decision | Status |
| --- | --- |
| Merged LEDH-inclusive artifact | passed |
| LGSSM LEDH value row | merged as same-target value-only |
| LGSSM LEDH score row | blocked; Contract E not merged |
| Fixed spatial SIR LEDH value row | merged as value-only |
| Fixed spatial SIR LEDH score row | blocked |
| Other LEDH rows | explicit blocked/scoped statuses preserved |
| Runtime ranking | disabled |

## Phase 6 Handoff

Phase 6 may close the program with this plain-language state:

- LEDH has one same-target LGSSM value-only row and one fixed spatial SIR
  value-only row in the merged leaderboard.
- LEDH has no admitted leaderboard score rows.
- Runtime comparisons against frozen non-LEDH rows are not allowed.
- Actual SV, KSC SV, predator-prey, and generalized SV remain blocked until
  reviewed same-target LEDH adapters exist.
- Parameterized SIR remains scoped component evidence only.

## Nonclaims

- Phase 5 does not certify any LEDH total-derivative score.
- Phase 5 does not certify HMC readiness.
- Phase 5 does not certify posterior correctness or scientific superiority.
- Phase 5 does not compare fresh LEDH runtimes against frozen non-LEDH rows.
