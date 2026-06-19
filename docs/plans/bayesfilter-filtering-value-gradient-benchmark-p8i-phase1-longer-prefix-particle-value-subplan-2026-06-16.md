# P8i Phase 1 Subplan: Longer-Prefix Particle And Value Ladder

Date: 2026-06-16

Status: `REVIEWED_EXECUTED`

## Phase Objective

Test whether the P8h OT-resampled Algorithm 1 route can move beyond horizons
`4,8` to longer-prefix particle/value adequacy under trusted GPU execution,
without treating the result as full production tuning unless the declared gate
passes.

## Entry Conditions

- P8i Phase 0 gap ledger is reviewed.
- P8h Phase 5 selected `N=5` only as short-prefix Stage 0 evidence.
- P8h Phase 6/7/8 route, gradient, GPU, and Tier-0 HMC artifacts remain
  inherited context only.

## Required Artifacts

- Fresh trusted GPU precheck note embedded in the Phase 1 result. The note must
  record that an escalated/trusted GPU probe was run immediately before the
  Phase 1 ladder and must cite the command output or blocker.
- Pilot rung JSON/CSV for the smallest discriminating cell:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-phase1-pilot-rung-2026-06-16.json`;
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-phase1-pilot-rung-2026-06-16.csv`;
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-phase1-pilot-rung-selected-blocked-2026-06-16.csv`.
- Longer-prefix ladder JSON:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-phase1-longer-prefix-particle-value-2026-06-16.json`.
- Longer-prefix ladder CSV:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-phase1-longer-prefix-particle-value-2026-06-16.csv`.
- Selected/blocked CSV:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-phase1-longer-prefix-particle-value-selected-blocked-2026-06-16.csv`.
- Phase 1 result:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-phase1-longer-prefix-particle-value-result-2026-06-16.md`.
- Run-manifest checklist embedded in the Phase 1 result. The result must
  verify that the JSON artifact records, or the result separately records:
  git commit, dirty-state summary, exact command actually run, environment or
  conda environment when known, CPU/GPU status, fresh trusted GPU precheck
  status, G0 manifest path, random seeds, horizons, particle counts, wall
  time, output artifact paths, plan file, and result file. Use `N/A` only when
  the field genuinely does not apply.

## Required Checks, Tests, Reviews

- Pre-run local checks:
  `git diff --check -- scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-*`
- Fresh trusted GPU precheck, run escalated/trusted immediately before any
  Phase 1 GPU ladder:

```bash
nvidia-smi
```

- Pilot rung first, run escalated/trusted only after review:

```bash
PYTHONDONTWRITEBYTECODE=1 MPLCONFIGDIR=/tmp python scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py --p8h-particle-tuning-stage0 --row actual_sv --algorithm ledh_pfpf_alg1_ukf_current --p8h-resampling-route ot_sinkhorn_barycentric_covariance_carry --coordinate canonical_unconstrained --horizons 16 --particles 5,10 --seeds 81120,81121,81122,81123,81124 --device gpu --g0-manifest docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase0-gpu-probe-result-2026-06-15.md --runtime-budget-seconds 1800 --p8h-profile-manifest-phase P8I_PHASE1_LONGER_PREFIX_PARTICLE_VALUE_PILOT --p8h-profile-manifest-plan docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-phase1-longer-prefix-particle-value-subplan-2026-06-16.md --output-json docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-phase1-pilot-rung-2026-06-16.json --output-csv docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-phase1-pilot-rung-2026-06-16.csv --selected-blocked-csv docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-phase1-pilot-rung-selected-blocked-2026-06-16.csv
```

- Proceed to the full planned Phase 1 ladder only if the pilot rung is finite,
  transport-valid, trusted-GPU, within runtime budget, and does not project the
  full ladder beyond budget. Full ladder candidate command:

```bash
PYTHONDONTWRITEBYTECODE=1 MPLCONFIGDIR=/tmp python scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py --p8h-particle-tuning-stage0 --row actual_sv --algorithm ledh_pfpf_alg1_ukf_current --p8h-resampling-route ot_sinkhorn_barycentric_covariance_carry --coordinate canonical_unconstrained --horizons 16,32 --particles 5,10,20 --seeds 81120,81121,81122,81123,81124 --device gpu --g0-manifest docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase0-gpu-probe-result-2026-06-15.md --runtime-budget-seconds 1800 --p8h-profile-manifest-phase P8I_PHASE1_LONGER_PREFIX_PARTICLE_VALUE --p8h-profile-manifest-plan docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-phase1-longer-prefix-particle-value-subplan-2026-06-16.md --output-json docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-phase1-longer-prefix-particle-value-2026-06-16.json --output-csv docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-phase1-longer-prefix-particle-value-2026-06-16.csv --selected-blocked-csv docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-phase1-longer-prefix-particle-value-selected-blocked-2026-06-16.csv
```

- Programmatic JSON/CSV validation and focused route/nonclaim checks.
- Programmatic run-manifest validation that the JSON artifact and Phase 1
  result preserve the required manifest fields listed above.
- Read-only Claude review of the result and Phase 2 subplan.

The `--p8h-particle-tuning-stage0` flag is reused only as the current runner's
codepath selector for the OT-resampled Algorithm 1 tuning harness. P8i
provenance must be carried by `--p8h-profile-manifest-phase`, the P8i plan
path, P8i output artifact paths, and the Phase 1 result. The result must not
call the run a P8h Phase 5 result.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Does the exact P8h route remain finite, transport-valid, trusted-GPU, and adjacent-rung stable at longer prefixes `16,32` for five fixed seeds? |
| Baseline/comparator | P8h Phase 5 short-prefix `4,8` ladder and within-P8i adjacent particle rungs. |
| Primary criterion | Either select a diagnostic longer-prefix count by the restated finite/trusted-GPU/transport/runtime/five-seed-MCSE/adjacent-rung rule below, or write an explicit blocker. |
| Veto diagnostics | Nonfinite value; missing trusted GPU evidence; transport residual/covariance carry failure; runtime over budget; five-seed MC uncertainty failure; adjacent-rung instability; schema/provenance still labeled as P8h Phase 5 without P8i manifest fields. |
| Explanatory diagnostics | Runtime, ESS, MCSE, adjacent deltas, per-seed values, transport residuals. |
| Not concluded | Full-horizon adequacy unless full horizon is explicitly included and passes; gradient correctness; HMC readiness; NUTS readiness; ranking; default sampler policy. |

## Forbidden Claims And Actions

- Do not treat `N=5` inherited from P8h as longer-prefix adequacy unless this
  phase reselects it under the Phase 1 gate.
- Do not run full horizon `1000` in Phase 1 without first reviewing a runtime
  projection from the `16,32` result.
- Do not claim HMC or gradient readiness from value-ladder pass alone.

## Restated Selection Rule

A candidate particle count passes Phase 1 only if all selected longer-prefix
horizons pass the following predeclared checks:

- every per-seed value is finite;
- every recorded transport diagnostic passes canonical
  `target_by_source_row_stochastic` validation, transport/covariance shape
  validation, finite particles/covariances/corrected weights, and row residual
  not exceeding the recorded tolerance;
- trusted GPU evidence is present in the artifact and no CPU fallback is
  treated as success;
- exactly five fixed seeds are used;
- each rung runtime is within `1800` seconds;
- MC standard error is at most
  `max(2.0, 0.0025 * abs(mean_log_likelihood))`;
- the adjacent-rung absolute mean difference is at most
  `2 * adjacent_combined_mc_se + 1.0`.

The selected count is the smallest particle count satisfying all checks with
the next adjacent particle rung present. If no count satisfies these checks,
the result must record the first applicable blocker reason rather than
changing thresholds.

## Exact Next-Phase Handoff Conditions

Phase 2 may launch only if Phase 1 produces either a selected longer-prefix
count or a blocker that justifies the next smallest gradient diagnostic.

## Stop Conditions

- Runtime projection from the pilot rung implies the full planned ladder would
  exceed budget.
- Any transport/covariance carry or trusted-GPU veto fires.
- The selection rule needs to be changed after seeing outcomes.
