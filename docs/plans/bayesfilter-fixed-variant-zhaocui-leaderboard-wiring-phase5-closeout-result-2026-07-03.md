# Phase 5 Result: Closeout And Handoff

Date: 2026-07-03

Status: `PASS_PROGRAM_CLOSED_SPLIT_MERGE_ARTIFACT`

## Decision Table

| Field | Status |
| --- | --- |
| Decision | The fixed-variant Zhao-Cui leaderboard wiring program is closed within the declared scoped-component boundary. |
| Primary criterion status | Passed: the July 3 leaderboard JSON/MD include the parameterized Zhao-Cui SIR scoped component row with manual/analytical score provenance and retained-grid production exclusion. |
| Veto diagnostic status | No veto remains open for the scoped row. Full observed-data/filtering SIR remains explicitly unclaimed. |
| Main uncertainty | The July 3 artifact is a split/merge artifact; unrelated expensive rows were preserved from the frozen July 1 full artifact rather than freshly rerun. |
| Next justified action | Use the July 3 JSON/MD as the current scoped leaderboard artifact, and separately plan any fresh all-row rerun or full-filtering SIR derivative work if needed. |
| What is not being concluded | No fresh all-row rerun, no full observed-data/filtering SIR likelihood or score identity, no exact likelihood proof, no posterior correctness, no new GPU result, and no retained-grid production admission. |

## Closed Artifacts

- Master program:
  `docs/plans/bayesfilter-fixed-variant-zhaocui-leaderboard-wiring-master-program-2026-07-03.md`
- Phase 4 result:
  `docs/plans/bayesfilter-fixed-variant-zhaocui-leaderboard-wiring-phase4-regeneration-validation-result-2026-07-03.md`
- July 3 full split/merge leaderboard JSON:
  `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-03.json`
- July 3 full split/merge leaderboard Markdown:
  `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-03.md`
- Scoped row validation JSON/MD:
  `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-03-scoped-zhaocui-sir-row.json`
  and
  `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-03-scoped-zhaocui-sir-row.md`
- Claude review ledger:
  `docs/plans/bayesfilter-fixed-variant-zhaocui-leaderboard-wiring-claude-review-ledger-2026-07-03.md`
- Visible execution ledger:
  `docs/plans/bayesfilter-fixed-variant-zhaocui-leaderboard-wiring-visible-execution-ledger-2026-07-03.md`

## Scoped Zhao-Cui SIR Result

| Field | Value |
| --- | --- |
| Row id | `zhao_cui_spatial_sir_austria_j9_T20_parameterized_logscale` |
| Algorithm id | `zhao_cui_scalar_or_multistate` |
| Scope | `local_complete_data_zhao_cui_sir_d18_component` |
| Admission | `scoped_component_row_admitted` |
| Average log likelihood | `-60.44641064507831` |
| Log likelihood | `-1208.9282129015662` |
| Score | `[1163.1499331099205, -508.7932467308049, 21.10862132639743]` |
| Score L2 norm | `1269.7377322529198` |
| Score provenance | `zhao_cui_sir_d18_local_complete_data_manual_parameter_score_methods` |
| Route role | `fixed_variant_zhao_cui_source_route` |
| Retained-grid role | `diagnostic_historical_retained_grid` |
| Retained-grid admission | `not_admitted_for_production_leaderboard_use_fixed_variant_zhao_cui` |

## Local Checks

Commands:

```bash
python -m py_compile docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py tests/test_two_lane_highdim_leaderboard_phase5.py tests/test_two_lane_highdim_leaderboard_phase7.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py --cached-baseline docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-01.json --scoped-patch docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-03-scoped-zhaocui-sir-row.json --output docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-03.json --markdown-output docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-03.md
python -m json.tool docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-03.json
rg -n "split_merge_cached_july1|scoped_component_row_admitted|local_complete_data_zhao_cui_sir_d18_component|zhao_cui_sir_d18_local_complete_data_manual_parameter_score_methods|not a full observed-data/filtering row|not evidence that unrelated expensive rows were rerun|not_admitted_for_production_leaderboard_use_fixed_variant_zhao_cui|1163\\.149933|-508\\.793247|21\\.108621|-60\\.446411" docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-03.json docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-03.md
git diff --check -- docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py tests/test_two_lane_highdim_leaderboard_phase5.py tests/test_two_lane_highdim_leaderboard_phase7.py docs/plans/bayesfilter-fixed-variant-zhaocui-leaderboard-wiring-*.md docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-03.json docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-03.md docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-03-scoped-zhaocui-sir-row.json docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-03-scoped-zhaocui-sir-row.md
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m pytest tests/test_two_lane_highdim_leaderboard_phase5.py tests/test_two_lane_highdim_leaderboard_phase7.py -q
```

Outcome:

- Compile checks passed.
- Split/merge artifact generation passed.
- JSON syntax validation passed.
- Required scope/provenance/nonclaim markers were found.
- `git diff --check` passed.
- Focused pytest passed: `9 passed, 2 warnings in 7.19s`.

## Claude Review

Claude Opus max-effort read-only review of the Phase 4 result returned:

```text
VERDICT: AGREE
```

Claude found no material overclaim. It noted only that the Phase 4 status
string is strong in isolation, but acceptable because the document repeatedly
narrows "full artifact" to the split/merge sense.

## Final Handoff

Use the July 3 JSON/MD for the current fixed-variant Zhao-Cui scoped component
leaderboard state. Do not use it as evidence that the old retained-grid route
is production-admitted or that full observed-data/filtering SIR likelihood and
score identity have been solved.
