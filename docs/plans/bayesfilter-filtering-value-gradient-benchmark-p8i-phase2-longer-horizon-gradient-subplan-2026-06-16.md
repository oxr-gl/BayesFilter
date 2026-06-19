# P8i Phase 2 Subplan: Longer-Horizon OT Gradient Ladder

Date: 2026-06-16

Status: `REVIEWED_EXECUTED`

## Phase Objective

Check longer-prefix AD gradient stability for the exact P8h/P8i route at the
Phase 1 selected diagnostic particle count, while preserving that this is a
fixed-seed relaxed-OT computational graph diagnostic.

## Entry Conditions

- Phase 1 result exists and selected diagnostic count `N=5` for horizons
  `16,32`.
- Phase 1 artifacts preserve P8i provenance even though the current runner
  reuses `--p8h-particle-tuning-stage0` as a codepath selector.
- Runner gradient mode has a P8i manifest override:
  `--p8h-gradient-manifest-phase` and `--p8h-gradient-manifest-plan`.

## Required Artifacts

- Pilot gradient JSON/CSV:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-phase2-gradient-h16-pilot-2026-06-16.json`;
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-phase2-gradient-h16-pilot-2026-06-16.csv`.
- Full Phase 2 gradient JSON/CSV for horizon `32` if the pilot passes:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-phase2-gradient-h32-2026-06-16.json`;
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-phase2-gradient-h32-2026-06-16.csv`.
- Phase 2 result preserving the gradient-scope classification:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-phase2-longer-horizon-gradient-result-2026-06-16.md`.

## Required Checks, Tests, Reviews

- Local checks before GPU execution:

```bash
PYTHONDONTWRITEBYTECODE=1 python -m py_compile scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py
CUDA_VISIBLE_DEVICES=-1 PYTHONDONTWRITEBYTECODE=1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py -k "p8h_ot_gradient"
git diff --check -- scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-*
```

- Trusted-GPU pilot gradient command, only after Phase 1 result and this
  subplan are reviewed:

```bash
PYTHONDONTWRITEBYTECODE=1 MPLCONFIGDIR=/tmp python scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py --p8h-ot-gradient-check --row actual_sv --algorithm ledh_pfpf_alg1_ukf_current --horizon 16 --particles 5 --seeds 81120,81121,81122,81123,81124 --device gpu --g0-manifest docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase0-gpu-probe-result-2026-06-15.md --p8h-resampling-route ot_sinkhorn_barycentric_covariance_carry --coordinate canonical_unconstrained --runtime-budget-seconds 1800 --p8h-gradient-fd-threshold 1e-5 --p8h-gradient-manifest-phase P8I_PHASE2_LONGER_HORIZON_GRADIENT_H16_PILOT --p8h-gradient-manifest-plan docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-phase2-longer-horizon-gradient-subplan-2026-06-16.md --output-json docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-phase2-gradient-h16-pilot-2026-06-16.json --output-csv docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-phase2-gradient-h16-pilot-2026-06-16.csv
```

- Proceed to the horizon `32` gradient gate only if horizon `16` passes:

```bash
PYTHONDONTWRITEBYTECODE=1 MPLCONFIGDIR=/tmp python scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py --p8h-ot-gradient-check --row actual_sv --algorithm ledh_pfpf_alg1_ukf_current --horizon 32 --particles 5 --seeds 81120,81121,81122,81123,81124 --device gpu --g0-manifest docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase0-gpu-probe-result-2026-06-15.md --p8h-resampling-route ot_sinkhorn_barycentric_covariance_carry --coordinate canonical_unconstrained --runtime-budget-seconds 1800 --p8h-gradient-fd-threshold 1e-5 --p8h-gradient-manifest-phase P8I_PHASE2_LONGER_HORIZON_GRADIENT_H32 --p8h-gradient-manifest-plan docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-phase2-longer-horizon-gradient-subplan-2026-06-16.md --output-json docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-phase2-gradient-h32-2026-06-16.json --output-csv docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-phase2-gradient-h32-2026-06-16.csv
```

- Programmatic JSON/CSV validation after each GPU command.
- Focused route/provenance/nonclaim searches.
- Read-only review of the Phase 2 result and refreshed Phase 3 subplan.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Are AD gradients finite, connected, repeatable, and finite-difference-consistent enough at horizons `16,32` and `N=5` to justify the next GPU/HMC diagnostic? |
| Baseline/comparator | P8h Phase 6 short-prefix horizon `4` gradient result and P8i Phase 1 selected longer-prefix count. |
| Primary criterion | Horizon `16` and `32` artifacts pass finite connected gradients over five fixed seeds, repeat-value/gradient stability, max finite-difference residual at most `1e-5`, trusted-GPU placement, exact route/count provenance, and P8i phase/plan manifest fields; otherwise explicit blocker. |
| Veto diagnostics | Disconnected gradient; nonfinite value/gradient; max finite-difference residual above `1e-5`; CPU fallback; route/count mismatch; stale P8h-only phase/plan provenance; relaxed-OT AD gradient overclaimed as exact stochastic PF marginal score. |
| Explanatory diagnostics | Gradient norms, finite-difference residuals, repeat deltas, ESS, runtime. |
| Not concluded | Stochastic PF marginal-gradient correctness, HMC readiness, NUTS readiness, posterior convergence, filter ranking, or default sampler policy. |

## Forbidden Claims And Actions

- Do not claim exact stochastic PF marginal-gradient correctness.
- Do not launch HMC or NUTS in Phase 2.
- Do not change the selected count after seeing gradient results.
- Do not treat finite-difference agreement as a proof of stochastic gradient
  correctness.

## Exact Next-Phase Handoff Conditions

Phase 3 may launch only if Phase 2 passes both horizons or writes a blocker
that preserves the next smallest GPU-scaling diagnostic.

## Stop Conditions

- Gradient diagnostics fail or require changed thresholds.
- Runtime exceeds the reviewed budget.
- The horizon `16` pilot fails; do not run horizon `32` after a pilot veto.
