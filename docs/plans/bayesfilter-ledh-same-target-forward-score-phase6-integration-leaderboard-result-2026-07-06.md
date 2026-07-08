# Phase 6 Result: Integration And Leaderboard Rebuild

metadata_date: 2026-07-06
status: PASSED_WITH_BOUNDED_FALLBACK_CLAUDE_REVIEW
master_program: docs/plans/bayesfilter-ledh-same-target-forward-score-master-program-2026-07-06.md
phase: 6

## Phase Objective

Add all-model LEDH integration checks and rebuild the LEDH-inclusive
leaderboard only with rows that passed same-target value, no-tape score, and
`N=10000` gates.

## Skeptical Plan Audit

| Risk checked | Result |
| --- | --- |
| Wrong baseline | The builder copies frozen non-LEDH rows from the July 3 highdim baseline and marks them not runtime-rankable with fresh LEDH rows. |
| Proxy metrics promoted | Runtime, memory, and compile fields remain explanatory. Score admission is tied to Phase 5 score-memory artifacts. |
| Blocked row promoted | Actual SV, KSC SV, predator-prey, and generalized SV remain LEDH-blocked. |
| Scoped row promoted | The parameterized SIR log-scale diagnostic remains `scoped_component_status_only`, not a full observed-data row. |
| Value/score mismatch | The integration test checks that LGSSM and fixed SIR use Phase 5 no-tape score artifacts for the same row ids and value targets. |
| Hidden runtime ranking | `runtime_cross_ranking_allowed` is `false`; fresh LEDH rows are not runtime-ranked against frozen non-LEDH baselines. |

Audit status: passed locally.

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | Can the LEDH-inclusive leaderboard truthfully report all admitted LEDH values and scores? |
| Baseline/comparator | Phase 5 per-model tests and the July 3/July 5 leaderboard artifacts. |
| Primary criterion | Passed locally: the rebuilt leaderboard includes only LGSSM and fixed SIR as admitted LEDH score rows and preserves blocked/scoped statuses for all other LEDH rows. |
| Veto diagnostics | No value/score algorithm mismatch found; no blocked row promoted; scoped SIR not promoted; runtime cross-ranking remains forbidden. |
| Explanatory diagnostics | Runtime, memory, compile time, MCSE, and frozen non-LEDH context are preserved as explanatory fields only. |
| Not concluded | No HMC readiness, posterior correctness, scientific superiority, exact nonlinear SIR likelihood correctness, or fair runtime ranking. |

## Artifacts

- Builder:
  `docs/benchmarks/benchmark_two_lane_highdim_ledh_inclusive_results.py`
- Integration tests:
  `tests/test_two_lane_highdim_ledh_leaderboard.py`
- Leaderboard JSON:
  `docs/plans/bayesfilter-two-lane-highdim-ledh-inclusive-leaderboard-results-2026-07-06.json`
- Leaderboard Markdown:
  `docs/plans/bayesfilter-two-lane-highdim-ledh-inclusive-leaderboard-results-2026-07-06.md`
- Review bundle:
  `docs/reviews/ledh-same-target-forward-score-phase6-review-bundle-2026-07-06.md`

## Admitted LEDH Rows

| Row | Status | Score route | Score dimension | Evidence artifact |
| --- | --- | --- | ---: | --- |
| `benchmark_lgssm_exact_oracle_m3_T50` | `executed_value_score` | `compact_forward_sensitivity_no_autodiff_same_scalar_lgssm_ledh_pfpf_ot` | 5 | `docs/plans/ledh-phase5-lgssm-score-memory-n10000-2026-07-06.json` |
| `zhao_cui_spatial_sir_austria_j9_T20` | `executed_value_score` | `manual_total_vjp_no_autodiff_same_scalar_fixed_sir_logscale_ledh_pfpf_ot` | 3 | `docs/plans/ledh-phase5-fixed-sir-score-memory-n10000-2026-07-06.json` |

The fixed SIR row uses the amended free-theta target
`theta=(log_kappa_scale, log_nu_scale, log_obs_noise_scale)`.

## Blocked Or Scoped LEDH Rows

| Row | LEDH status | Reason |
| --- | --- | --- |
| `zhao_cui_sv_actual_nongaussian_T1000` | `blocked` | No reviewed same-target current GPU/XLA LEDH row adapter. |
| `zhao_cui_sv_ksc_gaussian_mixture_surrogate_T1000` | `blocked` | No reviewed LEDH adapter for the KSC transformed-mixture target. |
| `zhao_cui_spatial_sir_austria_j9_T20_parameterized_logscale` | `scoped_component_status_only` | Scoped diagnostic/component row, not full observed-data row evidence. |
| `zhao_cui_predator_prey_T20` | `blocked` | No reviewed same-target predator-prey T20 LEDH adapter. |
| `zhao_cui_generalized_sv_synthetic_from_estimated_values` | `blocked` | No reviewed LEDH adapter for the generalized-SV source-row target. |

## Commands And Checks

Regenerated leaderboard artifacts:

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python docs/benchmarks/benchmark_two_lane_highdim_ledh_inclusive_results.py > /tmp/ledh_phase6_builder_stdout_cpuhidden.json
```

Result: exit 0. TensorFlow emitted import-time CUDA plugin/cuInit warnings even
with GPU hidden; this command only regenerated JSON/Markdown artifacts and is
not treated as GPU evidence.

Focused integration checks:

```text
python -m py_compile docs/benchmarks/benchmark_two_lane_highdim_ledh_inclusive_results.py tests/test_two_lane_highdim_ledh_leaderboard.py
python -m pytest tests/test_two_lane_highdim_ledh_leaderboard.py -q
```

Result: `9 passed, 2 warnings`.

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not concluded |
| --- | --- | --- | --- | --- | --- |
| Close Phase 6 | Passed | No veto fired locally or in bounded fallback review | Review used bounded fallback rather than primary material Claude path | Start a new row-adapter runbook for blocked rows if more LEDH scores are required | HMC readiness, posterior correctness, scientific superiority, exact nonlinear SIR likelihood correctness, fair runtime ranking |

## Post-Run Red-Team Note

The strongest alternative explanation is that the leaderboard now truthfully
reports only the two admitted LEDH rows, but the blocked rows still require real
same-target adapter work rather than leaderboard assembly work. A result that
would overturn this closeout would be a test or review finding that a blocked
row was silently promoted, that fixed SIR score evidence comes from the scoped
component diagnostic rather than the full amended row, or that value and score
fields derive from different row targets.

## Read-Only Review

Bounded Claude review gate:

```text
bash /home/chakwong/python/claudecodex/scripts/claude_review_gate.sh --cwd /home/chakwong/BayesFilter --review-name ledh-same-target-forward-score-phase6 --bundle /home/chakwong/BayesFilter/docs/reviews/ledh-same-target-forward-score-phase6-review-bundle-2026-07-06.md --probe-timeout 90 --timeout-seconds 180 --max-retries 1 --allow-bounded-fallback
```

Result:

- `REVIEW_STATUS=bounded_fallback_agree`
- `VERDICT=AGREE`
- Run dir:
  `/home/chakwong/BayesFilter/.claude_reviews/20260707-000438-ledh-same-target-forward-score-phase6`
- Status JSON:
  `/home/chakwong/BayesFilter/.claude_reviews/20260707-000438-ledh-same-target-forward-score-phase6/status.json`

This is weaker than a full primary Claude material review. It is recorded as an
accepted bounded no-obvious-blocker signal under the runbook review protocol,
with the local tests carrying the concrete artifact evidence.

## Phase Status

Phase 6 passed with bounded fallback Claude review. The same-target forward
score runbook is complete.
