# P9 Result: Integration Closeout

metadata_date: 2026-06-11
phase: FILTER_BENCH_P9
status: BLOCK_FILTER_BENCH_P9_NUMERIC_BENCHMARK_PENDING
supervisor: Codex
reviewer: Claude Code read-only

## Evidence Contract

| Field | Result |
| --- | --- |
| Question | Have the pre-benchmark gaps and the revised P8 synthetic-truth benchmark contract been closed enough to trust filtering for Bayesian-estimation handoff? |
| Baseline/comparator | P0-P8 phase results, P8 synthetic-truth contract, and the reviewed methodology proposal. |
| Primary criterion | Block handoff: P0-P7 and the revised P8 contract gate have durable artifacts, but the actual synthetic-truth numeric benchmark has not yet generated accepted truth draws, synthetic datasets, horizon/seed calibration, or likelihood/score/curvature measurements. |
| Veto diagnostics | Bayesian-estimation handoff veto fired: `BLOCK_FILTER_BENCH_P8_SYNTHETIC_TRUTH_NUMERIC_RUN_PENDING`. |
| Nonclaims | No filter ranking, no full numeric value/score/curvature result, no DPF gradient certification, no HMC readiness, and no Bayesian-estimation readiness. |

## Phase Status Summary

| Phase | Status |
| --- | --- |
| P0 | `PASS_FILTER_BENCH_P0_CONTRACT` |
| P1 | `PASS_FILTER_BENCH_P1_TARGET_REGISTRY` |
| P2 | `PASS_FILTER_BENCH_P2_ADAPTER_PROTOCOL` |
| P3 | `PASS_FILTER_BENCH_P3_REFERENCE_ORACLES` |
| P4 | `PASS_FILTER_BENCH_P4_DETERMINISTIC_FILTERS` |
| P5 | `PASS_FILTER_BENCH_P5_DPF_FILTERS` |
| P6 | `PASS_FILTER_BENCH_P6_GRADIENT_SEMANTICS` |
| P7 | `PASS_FILTER_BENCH_P7_PREFLIGHT_MATRIX` |
| P8 old matrix gate | `BLOCK_FILTER_BENCH_P8_RUNNER_MATRICES` |
| P8 revised synthetic-truth contract | `PASS_FILTER_BENCH_P8_SYNTHETIC_TRUTH_CONTRACT` |
| P8 full numeric performance run | `BLOCK_FILTER_BENCH_P8_SYNTHETIC_TRUTH_NUMERIC_RUN_PENDING` |
| P9 closeout | `BLOCK_FILTER_BENCH_P9_NUMERIC_BENCHMARK_PENDING` |

## Engineering Ledger

Passed:

- Frozen 7 x 12 current roster exists.
- Historical `LEDH-PFPF-OT` is excluded from current evidence.
- P7 preflight and P8 synthetic-truth contract have no silent current-roster
  holes.
- P8 now freezes canonical `phi` derivative semantics, componentwise score
  schema, Hessian transform gap policy, DPF MC uncertainty requirements, truth
  prior lanes, horizon calibration ladder, stochastic seed ladder, and tuple
  manifest schema.

Still pending:

- Accepted truth-parameter draws.
- Synthetic datasets generated from accepted truth parameters.
- Horizon calibration with long-run variance diagnostics.
- DPF seed calibration with particle Monte Carlo uncertainty.
- Reviewed numeric evaluators that write likelihood, score, curvature, failure,
  and stochastic uncertainty tables.

## Numerical Validity Ledger

Current evidence supports only the benchmark contract and schema.  It does not
yet support numerical comparisons of filter likelihood values, expected score
geometry, curvature, failure rates, or stochastic filter uncertainty.

The strongest blocker is that P8 numeric performance fields are intentionally
pending.  This is correct behavior: filling them from smoke fixtures or P7
preflight statuses would violate the reviewed evidence contract.

## Scientific Interpretation Ledger

The project now has a defensible methodology for nonlinear models:
synthetic-truth likelihood geometry replaces the impossible requirement for
exact nonlinear oracles everywhere.  However, the scientific claim that the
filtering ladder behaves acceptably across models has not yet been tested.

No filter should be ranked or promoted to Bayesian-estimation use from the P8
contract alone.

## Decision Table

| Decision | Primary criterion | Veto diagnostic status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| Block Bayesian-estimation handoff | Full numeric synthetic-truth benchmark is not yet run | P8 numeric-run-pending veto active | Whether the filters show plausible likelihood/score/curvature behavior after truth/data/horizon/seed calibration | Create and execute the next synthetic-truth numeric benchmark plan | Filter ranking, filtering closeout, Bayesian-estimation readiness |
| Preserve P8 contract as passed | Revised P8 contract has durable artifacts and Claude execution review agreed | No contract-emission veto fired | None for schema-level contract; numeric evidence remains separate | Use this contract as the basis for the next run | Numeric performance or scientific adequacy |

## Required Next Program

The next program should implement the numeric synthetic-truth benchmark:

1. Freeze benchmark truth priors in canonical `phi` coordinates for each model.
2. Generate accepted truth draws and rejection logs.
3. Generate synthetic datasets per accepted truth.
4. Calibrate horizons with HAC or batch-means uncertainty estimates.
5. Calibrate stochastic filter seeds and particle uncertainty.
6. Run reviewed evaluators for value, componentwise score, score summaries,
   curvature, failure rates, and stochastic diagnostics.
7. Ask Claude read-only reviewer to audit the numeric execution before any
   filter ranking or Bayesian-estimation handoff.

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | dirty worktree; P9 closeout artifact uncommitted |
| Dirty-state summary | dirty worktree preserved; unrelated changes not reverted |
| Command | Markdown closeout from reviewed P0-P8 artifacts; no numeric run |
| Environment | local Python environment |
| Conda env | N/A |
| CPU/GPU status | No GPU command; no GPU conclusion |
| Seeds | N/A; no random draws generated |
| Plan | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-gap-p9-closeout-subplan-2026-06-10.md` |
| Result | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-gap-p9-closeout-result-2026-06-11.md` |
| P8 revised contract | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8-synthetic-truth-contract-2026-06-11.json` |

## Post-Run Red-Team Note

- Strongest alternative explanation: the repaired contract may create a false
  sense that the filtering benchmark itself is complete.
- What would overturn the block: a reviewed numeric synthetic-truth run with
  accepted truth draws, calibrated horizons/seeds, and likelihood/score/
  curvature/stochastic uncertainty tables.
- Weakest part of evidence: P9 has no new numerical measurements; it is a
  governance closeout on readiness.

Required token:

```text
BLOCK_FILTER_BENCH_P9_NUMERIC_BENCHMARK_PENDING
```
