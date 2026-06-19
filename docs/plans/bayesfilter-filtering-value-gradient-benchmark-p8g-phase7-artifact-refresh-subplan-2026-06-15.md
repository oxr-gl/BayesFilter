# P8g-G7 Subplan: P8d/P8g Artifact Refresh

Date: 2026-06-15

Status: `DRAFT_DEPENDS_ON_G6`

## Phase Objective

Refresh stale P8d/P8g JSON/CSV/Markdown artifacts using the tuned GPU value
results, gradient readiness results, callback outcomes, and HMC diagnostic
tiers.

## Entry Conditions

- G0-G6 have result artifacts or blocker results.
- G4 selected/blocked particle counts are available.
- G5 callback outcomes are explicit.
- G6 HMC diagnostic tier outcomes are explicit.

## Required Artifacts

- Refreshed P8d/P8g JSON.
- Value, status, uncertainty/tuning, gradient, and HMC-readiness CSV tables.
- Markdown summary.
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase7-artifact-refresh-result-2026-06-15.md`
- Final visible stop handoff if any blocker remains.

## Required Checks/Tests/Reviews

- Schema roundtrip tests for all output tables.
- Checks that blocked KSC/Spatial SIR rows remain in every table.
- Checks that value and gradient/HMC readiness are not conflated.
- `python -m py_compile ...`
- Focused pytest.
- `git diff --check`
- Claude read-only final review.

## Planned Command And Artifact Contract

Repository root: `/home/chakwong/BayesFilter`.

Environment assumptions:

- G0-G6 phase results or blocker results are cited;
- artifact refresh is reporting/serialization and may use NumPy only for
  allowed reporting/data inspection;
- value, gradient, callback, GPU, and HMC statuses remain separate columns or
  tables.

Exact planned commands:

- compile check, non-GPU:
  `python -m py_compile scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py`
- artifact/schema tests, deliberate CPU:
  `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m pytest tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py tests/highdim/test_filtering_value_gradient_benchmark_adapter_schema.py -q -k "p8g or artifact or schema or blocked or hmc or gradient"`
- refresh entry point, to be implemented or confirmed in G7:
  `python scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py --p8g-refresh-artifacts --phase-results docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase0-gpu-probe-result-2026-06-15.md,docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase1-profile-result-2026-06-15.md,docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase2-vectorized-alg1-result-2026-06-15.md,docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase3-fixed-randomness-gradient-result-2026-06-15.md,docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase4-particle-tuning-result-2026-06-15.md,docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase5-callback-closure-result-2026-06-15.md,docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase6-hmc-diagnostic-tiers-result-2026-06-15.md --output-json docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-numeric-results-2026-06-15.json --value-csv docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-value-table-2026-06-15.csv --status-csv docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-status-table-2026-06-15.csv --uncertainty-csv docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-stochastic-uncertainty-table-2026-06-15.csv --gradient-csv docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-gradient-readiness-table-2026-06-15.csv --hmc-csv docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-hmc-readiness-table-2026-06-15.csv --markdown docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-numeric-summary-2026-06-15.md`
- formatting check, non-GPU:
  `git diff --check`

If the refresh CLI or schema tests do not exist, G7 must create them before any
artifact-closure claim, then rerun compile, focused tests, refresh, and
`git diff --check`.

Phase-local output paths:

- required phase result:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase7-artifact-refresh-result-2026-06-15.md`;
- refreshed JSON/CSV/Markdown paths listed in the refresh command;
- final stop handoff if any blocker remains:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-visible-stop-handoff-2026-06-15.md`.

Approval boundary:

- G7 is non-GPU unless a missing artifact requires recomputation; any such
  recomputation must return to the owning earlier phase and request approval
  there;
- do not push, commit, or overwrite unrelated artifacts without separate user
  instruction.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Do refreshed artifacts honestly represent P8g value, gradient, callback, GPU, and HMC diagnostic statuses? |
| Baseline/comparator | Stale P8d artifact and P8g phase results. |
| Primary criterion | Every row/cell is executed or blocked with visible status and nonclaims in every output schema. |
| Veto diagnostics | Stale P8d failures reused; blocked rows omitted; gradient readiness mixed into value table; GPU artifacts lack G0 citation; HMC overclaim. |
| Explanatory diagnostics | Artifact counts, table coverage, residual blockers, review findings. |
| Not concluded | Production HMC readiness, stochastic PF target HMC readiness, or final scientific ranking. |

## Forbidden Claims/Actions

- Do not silently drop blocked rows.
- Do not overwrite artifacts without recording provenance.
- Do not claim closure if any required table is missing.

## Next-Phase Handoff Conditions

If all gates pass, write final P8g closeout. If blockers remain, write visible
stop handoff with safest next decision.

## Stop Conditions

- Output schema cannot preserve required statuses.
- Tests fail.
- Claude final review does not converge after five rounds.
