# P8i Phase 3 Subplan: GPU Scaling Profile

Date: 2026-06-16

Status: `REVIEWED_EXECUTED`

## Phase Objective

Profile trusted GPU runtime scaling beyond P8h horizons `4,8` for the exact
P8i route/count before any longer HMC diagnostic.

## Entry Conditions

- Phase 1 selected diagnostic `N=5` at horizons `16,32`.
- Phase 2 produced reviewed passing relaxed-OT AD gradient artifacts at
  horizons `16,32`.
- Exact route: `ot_sinkhorn_barycentric_covariance_carry`;
  route variant: `p8h_sv_scalar_graph_ot_resampled_alg1`;
  coordinate: `canonical_unconstrained`;
  seeds: `81120,81121,81122,81123,81124`.

## Required Artifacts

- Selected-count profile JSON/CSV. This uses the current
  `--p8h-particle-tuning-stage0` runner flag only as the reusable profiling
  codepath for finite value/transport/runtime summaries; Phase 3 is not a new
  particle-tuning or selection phase:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-phase3-gpu-scaling-selected-n5-2026-06-16.json`;
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-phase3-gpu-scaling-selected-n5-2026-06-16.csv`;
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-phase3-gpu-scaling-selected-n5-selected-blocked-2026-06-16.csv`.
- Optional adjacent profile JSON/CSV for `N=10`, only if the selected-count
  profile projects within budget:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-phase3-gpu-scaling-adjacent-n10-2026-06-16.json`;
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-phase3-gpu-scaling-adjacent-n10-2026-06-16.csv`.
- Phase 3 result:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-phase3-gpu-scaling-result-2026-06-16.md`.
- Refreshed Phase 4 subplan.

## Required Checks, Tests, Reviews

- Local checks before GPU execution:

```bash
PYTHONDONTWRITEBYTECODE=1 python -m py_compile scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py
CUDA_VISIBLE_DEVICES=-1 PYTHONDONTWRITEBYTECODE=1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py -k "p8h_phase5 or p8h_ot_gradient"
git diff --check -- scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-*
```

- Trusted GPU selected-count profile:

```bash
PYTHONDONTWRITEBYTECODE=1 MPLCONFIGDIR=/tmp python scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py --p8h-particle-tuning-stage0 --row actual_sv --algorithm ledh_pfpf_alg1_ukf_current --p8h-resampling-route ot_sinkhorn_barycentric_covariance_carry --coordinate canonical_unconstrained --horizons 16,32 --particles 5 --seeds 81120,81121,81122,81123,81124 --device gpu --g0-manifest docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase0-gpu-probe-result-2026-06-15.md --runtime-budget-seconds 1800 --p8h-profile-manifest-phase P8I_PHASE3_GPU_SCALING_SELECTED_N5 --p8h-profile-manifest-plan docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-phase3-gpu-scaling-subplan-2026-06-16.md --output-json docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-phase3-gpu-scaling-selected-n5-2026-06-16.json --output-csv docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-phase3-gpu-scaling-selected-n5-2026-06-16.csv --selected-blocked-csv docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-phase3-gpu-scaling-selected-n5-selected-blocked-2026-06-16.csv
```

- Optional adjacent `N=10` selected horizons, only if the selected `N=5`
  profile is finite, trusted-GPU, transport-valid, and runtime projection keeps
  the adjacent profile within the reviewed budget:

```bash
PYTHONDONTWRITEBYTECODE=1 MPLCONFIGDIR=/tmp python scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py --p8h-particle-tuning-stage0 --row actual_sv --algorithm ledh_pfpf_alg1_ukf_current --p8h-resampling-route ot_sinkhorn_barycentric_covariance_carry --coordinate canonical_unconstrained --horizons 16,32 --particles 10 --seeds 81120,81121,81122,81123,81124 --device gpu --g0-manifest docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase0-gpu-probe-result-2026-06-15.md --runtime-budget-seconds 1800 --p8h-profile-manifest-phase P8I_PHASE3_GPU_SCALING_ADJACENT_N10 --p8h-profile-manifest-plan docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-phase3-gpu-scaling-subplan-2026-06-16.md --output-json docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-phase3-gpu-scaling-adjacent-n10-2026-06-16.json --output-csv docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-phase3-gpu-scaling-adjacent-n10-2026-06-16.csv --selected-blocked-csv docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-phase3-gpu-scaling-adjacent-n10-selected-blocked-2026-06-16.csv
```

- JSON/CSV validation and route/provenance/nonclaim checks.
- Read-only review of Phase 3 result and refreshed Phase 4 subplan before HMC.

## Runtime Projection Rule

Phase 3 defines a concrete HMC-feasibility projection for the next phase. Phase
4 may be refreshed for a bounded HMC Tier-1 diagnostic only if the selected
`N=5` Phase 3 profile satisfies all of the following:

- every selected-count rung is finite, trusted-GPU, transport-valid, and within
  `1800` seconds per rung;
- the worst observed per-seed value runtime at horizon `32`, `N=5`, is at most
  `120` seconds;
- the projected Tier-1 HMC cost
  `5 * worst_h32_seed_value_runtime_seconds` is at most `900` seconds for a
  diagnostic budget consisting of two retained samples, one burn-in step, and
  one initial value/gradient evaluation at one fixed PF seed;
- Phase 4 remains limited to a diagnostic fixed-kernel HMC run unless its own
  reviewed subplan declares a stronger criterion.

If the selected `N=5` profile fails any item above, Phase 3 must write an HMC
runtime blocker and Phase 4 must become a blocker/closeout subplan rather than
an execution subplan. The adjacent `N=10` profile is explanatory only and is
not required to authorize HMC.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Is the selected longer-prefix route/count practically executable on trusted GPU for the next bounded HMC diagnostic? |
| Baseline/comparator | P8h Phase 7 short-prefix GPU profile and P8i Phase 1/2 value/gradient runtimes. |
| Primary criterion | Finite trusted-GPU values and transport diagnostics at horizons `16,32`, `N=5`, with the declared HMC projection rule passing; otherwise explicit blocker. |
| Veto diagnostics | CPU fallback; OOM; nonfinite values/covariances/transport; route/count mismatch; runtime projection beyond budget. |
| Explanatory diagnostics | Runtime scaling, optional adjacent `N=10`, memory notes, ESS, MCSE, transport residuals. |
| Not concluded | Full GPU scaling law, production readiness, HMC readiness, filter ranking, or high-dimensional readiness. |

## Forbidden Claims And Actions

- Do not claim a full GPU scaling law.
- Do not launch HMC before Phase 4.
- Do not run adjacent `N=10` if the selected `N=5` profile already makes HMC
  infeasible.
- Do not treat the Stage-0 tuning vocabulary emitted by the reused runner as a
  new Phase 3 tuning/selection claim.

## Exact Next-Phase Handoff Conditions

Phase 4 may launch only if Phase 3 shows enough runtime headroom for a bounded
HMC Tier-1 diagnostic under the projection rule above, or writes a blocker
explaining why HMC should stop.

## Stop Conditions

- GPU runtime or memory makes the planned HMC tier infeasible.
- Any value/transport/trusted-GPU veto fires in the selected `N=5` profile.
