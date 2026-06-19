# P8g-G6 Subplan: HMC Diagnostic Tiers

Date: 2026-06-15

Status: `DRAFT_DEPENDS_ON_G5`

## Phase Objective

Run diagnostic HMC integrator tiers for the fixed-randomness/no-resampling LEDH
conditional surrogate objective.

## Entry Conditions

- G3 fixed-randomness gradient objective passed.
- Canonical coordinate and frozen seed/salt schedule are artifacted.
- G4/G5 value/callback outcomes are explicit.

## Required Artifacts

- HMC readiness tier manifest.
- Tier diagnostics JSON/CSV/Markdown.
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase6-hmc-diagnostic-tiers-result-2026-06-15.md`

## Required Checks/Tests/Reviews

- Tier 1 finite value/score.
- Tier 2 directional finite-difference checks.
- Tier 3 leapfrog reversibility and energy error.
- Tier 4 tiny short-chain diagnostic, if Tier 3 passes.
- Focused tests for promotion boundaries.
- Claude read-only review.

## Planned Command And Artifact Contract

Repository root: `/home/chakwong/BayesFilter`.

Environment assumptions:

- G3 fixed-randomness gradient result and seed/coordinate contract are cited;
- auxiliary randomness is fixed across each trajectory;
- tiers are diagnostic only and cannot certify production HMC.

Exact planned commands:

- compile check, non-GPU:
  `python -m py_compile scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py scripts/run_model_suite_hmc_qualification.py tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py`
- HMC boundary tests, deliberate CPU:
  `CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m pytest tests/highdim/test_p50_hmc_readiness_tiers.py tests/highdim/test_p51_hmc_tier2_leapfrog.py tests/highdim/test_p51_hmc_tier3_short_chain.py -q -k "p8g or fixed or hmc or ledh"`
- trusted GPU Tier 1-3 diagnostic entry point, to be implemented or confirmed in
  G6:
  `python scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py --p8g-hmc-diagnostic-tiers --tiers 1,2,3 --rows actual_sv,generalized_sv --particles <selected_count> --seeds 81120,81121,81122,81123,81124 --fixed-randomness-contract docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase3-fixed-randomness-gradient-contract-2026-06-15.md --g0-manifest docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase0-gpu-probe-result-2026-06-15.md --output-json docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase6-hmc-diagnostic-tiers-2026-06-15.json --output-csv docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase6-hmc-diagnostic-tiers-2026-06-15.csv`
- optional trusted GPU Tier 4 tiny short chain, only after Tier 3 passes:
  `python scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py --p8g-hmc-diagnostic-tiers --tiers 4 --rows <passed_rows> --particles <selected_count> --seeds 81120,81121,81122,81123,81124 --fixed-randomness-contract docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase3-fixed-randomness-gradient-contract-2026-06-15.md --g0-manifest docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase0-gpu-probe-result-2026-06-15.md --append-json docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase6-hmc-diagnostic-tier4-2026-06-15.jsonl`
- formatting check, non-GPU:
  `git diff --check`

If HMC diagnostic entry points or boundary tests do not exist, G6 must add them
before any HMC compatibility claim, then rerun compile, focused tests, trusted
Tier 1-3, and `git diff --check`.

Phase-local output paths:

- required phase result:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase6-hmc-diagnostic-tiers-result-2026-06-15.md`;
- Tier 1-3 JSON/CSV:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase6-hmc-diagnostic-tiers-2026-06-15.json`,
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase6-hmc-diagnostic-tiers-2026-06-15.csv`;
- optional Tier 4 JSONL:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase6-hmc-diagnostic-tier4-2026-06-15.jsonl`.

Approval boundary:

- every trusted GPU HMC diagnostic command requires explicit approval;
- Tier 4 is long-run adjacent and requires a separate launch checkpoint after
  Tier 3 evidence is written.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Is the fixed-randomness/no-resampling LEDH surrogate objective compatible with diagnostic HMC integrator checks? |
| Baseline/comparator | G3 gradient objective and declared canonical coordinate. |
| Primary criterion | Tiers pass without overclaiming stochastic PF target HMC readiness. |
| Veto diagnostics | Random draws/schedule/coordinate changes during trajectory; stochastic PF marginal target claim; non-finite energy/gradient; reversibility failure. |
| Explanatory diagnostics | Energy error, reversibility residual, tiny chain summaries. |
| Not concluded | Production HMC readiness or stochastic PF target HMC readiness. |

## Forbidden Claims/Actions

- Do not call Tier 3/4 production HMC.
- Do not use changing random streams inside a trajectory.
- Do not include resampling without a future reviewed subplan.

## Next-Phase Handoff Conditions

Advance to G7 with a tier status for each in-scope LEDH row and explicit
nonclaims.

## Stop Conditions

- Any tier violates frozen auxiliary data.
- Energy/reversibility diagnostics fail.
- HMC language becomes ambiguous.
