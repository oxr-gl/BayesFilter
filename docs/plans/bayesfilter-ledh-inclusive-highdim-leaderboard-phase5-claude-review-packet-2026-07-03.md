# Phase 5 Claude Review Packet: LEDH-Inclusive Merge

Date: 2026-07-03

Role: Claude is read-only reviewer. Codex is supervisor and executor.

## Review Question

Does the Phase 5 merged leaderboard preserve value-only, blocked, and scoped
LEDH statuses without changing frozen non-LEDH baseline meaning?

## Exact Paths

- Merge result:
  `docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-phase5-merge-comparison-result-2026-07-03.md`
- Merged JSON:
  `docs/plans/bayesfilter-two-lane-highdim-ledh-inclusive-leaderboard-results-2026-07-03.json`
- Merged Markdown:
  `docs/plans/bayesfilter-two-lane-highdim-ledh-inclusive-leaderboard-results-2026-07-03.md`
- Merge script:
  `docs/benchmarks/benchmark_two_lane_highdim_ledh_inclusive_results.py`
- Focused tests:
  `tests/test_two_lane_highdim_ledh_leaderboard.py`

## Critical Merge Rules

- Comparator mode is `frozen_non_ledh_baseline_plus_fresh_ledh`.
- Runtime cross-ranking is forbidden.
- Non-LEDH rows are copied from
  `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-03.json`
  with `comparator_provenance: frozen_non_ledh_baseline`.
- Contract E LGSSM route evidence is not merged as the leaderboard LGSSM score.
- LEDH LGSSM is merged as same-target value-only:
  `benchmark_lgssm_exact_oracle_m3_T50`, average log likelihood
  `-2.719201477051`, MCSE `0.0001186681274`, score blocked.
- LEDH fixed spatial SIR is merged as value-only:
  `zhao_cui_spatial_sir_austria_j9_T20`, average log likelihood
  `-45.141507568359`, MCSE `0.010411105587`, score blocked.
- Actual SV, KSC SV, predator-prey, and generalized SV remain blocked for LEDH.
- Parameterized SIR remains scoped component status only for LEDH.

## Local Checks

- `py_compile`: passed.
- `python -m pytest tests/test_two_lane_highdim_ledh_leaderboard.py -q`: `8 passed`.
- JSON assertions: 28 rows, 7 summaries, one LEDH row per model, no LEDH row
  has a populated leaderboard score vector, LGSSM/SIR score statuses blocked,
  parameterized SIR scoped, runtime ranking false: passed.
- `git diff --check`: passed.

## Claims Allowed

- The merged artifact includes LEDH rows for all seven highdim model rows.
- LEDH has two value-only executed rows: same-target LGSSM and fixed spatial
  SIR.
- LEDH has no admitted leaderboard score rows.
- LGSSM and fixed SIR main-row LEDH scores are blocked.
- Parameterized SIR remains scoped component evidence only, not a blocked or
  admitted full observed-data leaderboard score.

## Claims Forbidden

- Do not claim LEDH score works for the leaderboard.
- Do not treat Contract E LGSSM route evidence as `m3_T50` score evidence.
- Do not runtime-rank LEDH against frozen non-LEDH rows.
- Do not claim HMC readiness, posterior correctness, or scientific superiority.

## Verdict Request

Findings first. End with exactly one of:

`VERDICT: AGREE`

or

`VERDICT: REVISE`
