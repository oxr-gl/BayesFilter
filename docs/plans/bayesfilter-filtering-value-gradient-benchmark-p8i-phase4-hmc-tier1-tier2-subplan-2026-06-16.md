# P8i Phase 4 Subplan: HMC Tier-1 And Tier-2 Diagnostics

Date: 2026-06-16

Status: `REVIEWED_EXECUTED`

## Phase Objective

Advance from P8h Tier-0 fixed-kernel HMC execution smoke to a bounded Phase 4
Tier-1 fixed-kernel diagnostic only if Phase 1-3 value, gradient, and GPU
runtime gates support it. Tier-2 remains out of scope until Tier-1 has a
reviewed result.

## Entry Conditions

- Phase 1 longer-prefix value/count gate reviewed and selected diagnostic
  `N=5` at horizons `16,32`.
- Phase 2 gradient gate reviewed and passed at horizons `16,32`.
- Phase 3 GPU scaling gate produced a reviewed passing selected-count runtime
  profile and HMC projection.

## Required Artifacts

- HMC Tier-1 diagnostic JSON/CSV artifacts:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-phase4-hmc-tier1-fixed-kernel-2026-06-16.json`;
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-phase4-hmc-tier1-fixed-kernel-2026-06-16.csv`.
- Phase 4 result with decision table.
- Refreshed Phase 5 NUTS-readiness subplan.

## Required Checks, Tests, Reviews

- Local checks before GPU execution:

```bash
PYTHONDONTWRITEBYTECODE=1 python -m py_compile scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py
CUDA_VISIBLE_DEVICES=-1 PYTHONDONTWRITEBYTECODE=1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py -k "p8h_hmc"
git diff --check -- scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-*
```

- Trusted GPU Tier-1 fixed-kernel command, only after Phase 3 review:

```bash
PYTHONDONTWRITEBYTECODE=1 MPLCONFIGDIR=/tmp python scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py --p8h-hmc-tier0-smoke --row actual_sv --algorithm ledh_pfpf_alg1_ukf_current --horizon 32 --particles 5 --seeds 81120 --device gpu --g0-manifest docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase0-gpu-probe-result-2026-06-15.md --p8h-resampling-route ot_sinkhorn_barycentric_covariance_carry --coordinate canonical_unconstrained --hmc-num-results 2 --hmc-num-burnin-steps 1 --hmc-step-size 0.005 --hmc-num-leapfrog-steps 1 --runtime-budget-seconds 900 --p8h-hmc-manifest-phase P8I_PHASE4_HMC_TIER1_FIXED_KERNEL_DIAGNOSTIC --p8h-hmc-manifest-plan docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-phase4-hmc-tier1-tier2-subplan-2026-06-16.md --p8h-hmc-policy-label fixed_kernel_no_adaptation_tier1_diagnostic --p8h-hmc-tier-label tier1_fixed_kernel_diagnostic --p8h-hmc-schema-version filter_bench.p8i_hmc_tier1.v1 --p8h-hmc-status-success-label executed_p8i_hmc_tier1_fixed_kernel_diagnostic --p8h-hmc-status-blocked-label blocked_p8i_hmc_tier1_fixed_kernel_diagnostic --p8h-hmc-blocker-reason BLOCK_P8I_HMC_TIER1_FIXED_KERNEL_DIAGNOSTIC --p8h-hmc-evidence-question 'Can a tiny bounded fixed-kernel HMC diagnostic run at horizon 32, N=5, without numerical/runtime validity vetoes?' --p8h-hmc-evidence-baseline 'Reviewed P8i Phase 1 value/count gate, Phase 2 relaxed-OT AD gradient gate, and Phase 3 GPU runtime projection.' --p8h-hmc-evidence-primary-criterion 'Finite trusted-GPU fixed-kernel HMC diagnostic with finite initial value/gradient, finite samples, finite target/log-accept traces, exact P8i route/count/horizon provenance, and runtime within 900 seconds.' --p8h-hmc-predecessor-results-json '{"phase1_result":"docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-phase1-longer-prefix-particle-value-result-2026-06-16.md","phase2_result":"docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-phase2-longer-horizon-gradient-result-2026-06-16.md","phase3_result":"docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-phase3-gpu-scaling-result-2026-06-16.md"}' --output-json docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-phase4-hmc-tier1-fixed-kernel-2026-06-16.json --output-csv docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-phase4-hmc-tier1-fixed-kernel-2026-06-16.csv
```

- JSON/CSV validation and read-only review of result plus Phase 5 subplan.

The `--p8h-hmc-tier0-smoke` flag is reused only as the current fixed-kernel
HMC codepath selector. The emitted Phase 4 artifact must use the P8i
`schema_version`, `phase`, status labels, blocker reason, evidence contract,
plan path, and predecessor result paths specified in the command above.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Can a tiny bounded fixed-kernel HMC diagnostic run at horizon `32`, `N=5`, without numerical/runtime validity vetoes? |
| Baseline/comparator | P8h Phase 8 Tier-0 smoke and P8i Phase 1-3 gates. |
| Primary criterion | One fixed PF seed, two retained samples, one burn-in step, one leapfrog step, fixed step size `0.005`, finite initial value/gradient, finite samples, finite target/log-accept traces, trusted GPU, runtime within `900` seconds, exact P8i provenance; otherwise explicit blocker. |
| Veto diagnostics | Nonfinite samples/log prob/log accept ratio; disconnected or nonfinite initial gradient; CPU fallback; runtime over `900` seconds; HMC execution error; posterior-convergence claim from insufficient chains. |
| Explanatory diagnostics | Acceptance rate, displacement, runtime, ESS/sec if available, trace summaries. |
| Not concluded | Production HMC readiness, posterior convergence, valid tuning, NUTS readiness, stochastic PF marginal-gradient correctness, filter ranking, or default sampler policy. |

## Forbidden Claims And Actions

- Do not call Tier-1 a posterior convergence result.
- Do not run Tier-2 in this phase before a reviewed Tier-1 result.
- Do not run NUTS in Phase 4.

## Exact Next-Phase Handoff Conditions

Phase 5 may launch only if Phase 4 result explicitly decides whether NUTS is
blocked, diagnostic-only, or requires another HMC tier first.

## Stop Conditions

- HMC runtime, nonfinite diagnostics, or integrator failures block the tier.
- Any attempt to interpret Tier-1 as posterior convergence or production HMC
  readiness blocks the result.
