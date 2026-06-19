# P8i Phase 4 Result: HMC Tier-1 Fixed-Kernel Diagnostic

Date: 2026-06-16

Status: `PASS_TIER1_FIXED_KERNEL_EXECUTION_REVIEWED`

## Phase Objective

Advance from P8h Tier-0 fixed-kernel HMC execution smoke to a bounded P8i
Tier-1 fixed-kernel diagnostic only if Phase 1-3 value, gradient, and GPU
runtime gates support it.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Can a tiny bounded fixed-kernel HMC diagnostic run at horizon `32`, `N=5`, without numerical/runtime validity vetoes? |
| Baseline/comparator | Reviewed P8i Phase 1 value/count gate, Phase 2 relaxed-OT AD gradient gate, and Phase 3 GPU runtime projection. |
| Primary criterion | One fixed PF seed, two retained samples, one burn-in step, one leapfrog step, fixed step size `0.005`, finite initial value/gradient, finite samples, finite target/log-accept traces, trusted GPU, runtime within `900` seconds, exact P8i artifact provenance; runtime failures emit an explicit blocker artifact, while invalid preflight arguments stop before artifact creation. |
| Veto diagnostics | Nonfinite samples/log prob/log accept ratio; disconnected or nonfinite initial gradient; CPU fallback; runtime over `900` seconds; HMC execution error; posterior-convergence claim from insufficient chains. |
| Explanatory diagnostics | Acceptance rate, displacement, runtime, trace summaries. |
| Not concluded | Production HMC readiness, posterior convergence, valid tuning, NUTS readiness, stochastic PF marginal-gradient correctness, filter ranking, or default sampler policy. |

## Skeptical Audit

- Wrong-baseline check: Phase 4 is based on reviewed P8i Phase 1-3 gates, not
  P8h Tier-0 alone.
- Proxy-metric check: acceptance rate and displacement are explanatory only;
  this tiny chain cannot establish posterior convergence or tuning validity.
- Stop-condition check: any nonfinite diagnostic, CPU fallback, runtime
  failure, or HMC execution error would block.
- Artifact-fit check: the JSON carries P8i schema, phase, status labels,
  predecessor result paths, plan path, runtime budget, GPU tensor devices, and
  nonclaims.

## Implementation And Checks

The fixed-kernel HMC codepath is reused through the legacy
`--p8h-hmc-tier0-smoke` flag, but the Phase 4 artifact uses P8i Tier-1
metadata:

- schema: `filter_bench.p8i_hmc_tier1.v1`;
- phase: `P8I_PHASE4_HMC_TIER1_FIXED_KERNEL_DIAGNOSTIC`;
- status: `executed_p8i_hmc_tier1_fixed_kernel_diagnostic`;
- blocker reason: `BLOCK_P8I_HMC_TIER1_FIXED_KERNEL_DIAGNOSTIC`;
- predecessor result paths for P8i Phase 1/2/3.

The route identifier remains `p8h_sv_scalar_graph_ot_resampled_alg1` because
it is the inherited route variant established in P8h and carried by P8i. It is
not a P8h execution-phase claim. The JSON `nonclaims` list also inherits the
legacy phrase `Tier-0 fixed-kernel HMC execution smoke only`; for P8i this is
interpreted as a conservative nonclaim that the run is an execution diagnostic
only, not as a Tier-0 artifact identity. The controlling artifact identity is
the P8i schema, phase, status, plan, predecessor paths, and evidence contract
listed above.

Local checks:

```bash
PYTHONDONTWRITEBYTECODE=1 python -m py_compile scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py
CUDA_VISIBLE_DEVICES=-1 PYTHONDONTWRITEBYTECODE=1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py -k "p8h_hmc"
python -m json.tool docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-phase4-hmc-tier1-fixed-kernel-2026-06-16.json
git diff --check -- docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-* scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py
```

Results:

- `py_compile`: passed.
- Focused pytest before HMC run: `5 passed, 27 deselected, 2 warnings`.
- JSON validation: passed.
- `git diff --check`: passed.

Trusted GPU command:

```bash
PYTHONDONTWRITEBYTECODE=1 MPLCONFIGDIR=/tmp python scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py --p8h-hmc-tier0-smoke --row actual_sv --algorithm ledh_pfpf_alg1_ukf_current --horizon 32 --particles 5 --seeds 81120 --device gpu --g0-manifest docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase0-gpu-probe-result-2026-06-15.md --p8h-resampling-route ot_sinkhorn_barycentric_covariance_carry --coordinate canonical_unconstrained --hmc-num-results 2 --hmc-num-burnin-steps 1 --hmc-step-size 0.005 --hmc-num-leapfrog-steps 1 --runtime-budget-seconds 900 --p8h-hmc-manifest-phase P8I_PHASE4_HMC_TIER1_FIXED_KERNEL_DIAGNOSTIC --p8h-hmc-manifest-plan docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-phase4-hmc-tier1-tier2-subplan-2026-06-16.md --p8h-hmc-policy-label fixed_kernel_no_adaptation_tier1_diagnostic --p8h-hmc-tier-label tier1_fixed_kernel_diagnostic --p8h-hmc-schema-version filter_bench.p8i_hmc_tier1.v1 --p8h-hmc-status-success-label executed_p8i_hmc_tier1_fixed_kernel_diagnostic --p8h-hmc-status-blocked-label blocked_p8i_hmc_tier1_fixed_kernel_diagnostic --p8h-hmc-blocker-reason BLOCK_P8I_HMC_TIER1_FIXED_KERNEL_DIAGNOSTIC --p8h-hmc-evidence-question 'Can a tiny bounded fixed-kernel HMC diagnostic run at horizon 32, N=5, without numerical/runtime validity vetoes?' --p8h-hmc-evidence-baseline 'Reviewed P8i Phase 1 value/count gate, Phase 2 relaxed-OT AD gradient gate, and Phase 3 GPU runtime projection.' --p8h-hmc-evidence-primary-criterion 'Finite trusted-GPU fixed-kernel HMC diagnostic with finite initial value/gradient, finite samples, finite target/log-accept traces, exact P8i route/count/horizon provenance, and runtime within 900 seconds.' --p8h-hmc-predecessor-results-json '{"phase1_result":"docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-phase1-longer-prefix-particle-value-result-2026-06-16.md","phase2_result":"docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-phase2-longer-horizon-gradient-result-2026-06-16.md","phase3_result":"docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-phase3-gpu-scaling-result-2026-06-16.md"}' --output-json docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-phase4-hmc-tier1-fixed-kernel-2026-06-16.json --output-csv docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-phase4-hmc-tier1-fixed-kernel-2026-06-16.csv
```

## Results

| Diagnostic | Value |
|---|---:|
| Status | `executed_p8i_hmc_tier1_fixed_kernel_diagnostic` |
| Wall time | `139.355637` seconds |
| Runtime budget | `900` seconds |
| Horizon | `32` |
| Particle count | `5` |
| PF seed | `81120` |
| HMC seed | `[81120, 82120]` |
| Retained samples | `2` |
| Burn-in steps | `1` |
| Leapfrog steps | `1` |
| Step size | `0.005` |
| Acceptance rate | `1.0` |
| Sample displacement L2 | `0.00255696713787321` |
| Initial log likelihood | `-16.677140748029405` |
| Initial gradient L2 | `4.3868728708727245` |

Gate diagnostics:

| Gate | Status |
|---|---|
| Trusted GPU | true |
| Initial value finite | true |
| Initial gradient finite | true |
| Initial gradient connected | true |
| Samples finite | true |
| Log accept ratio finite | true |
| Target log probability finite | true |
| Runtime within budget | true |
| Blocker | `null` |

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not being concluded |
|---|---|---|---|---|---|
| Pass Phase 4 tiny fixed-kernel HMC Tier-1 execution diagnostic, pending review. | Passed the declared finite/trusted-GPU/runtime gates. | No Phase 4 veto fired. | The chain is far too small and untuned to say anything about posterior convergence, valid tuning, or NUTS readiness. | Refresh Phase 5 as a NUTS-readiness decision; current evidence supports blocking NUTS rather than running adaptive NUTS. | No production HMC readiness, posterior convergence, valid tuning, NUTS readiness, stochastic PF marginal-gradient correctness, ranking, or default policy. |

## Post-Run Red-Team Note

Strongest alternative explanation: the tiny chain executes because the step
size and sample count are extremely conservative; longer or adaptive samplers
may still fail or be too slow.

What would overturn this result: a rerun showing nonfinite trace quantities,
CPU fallback, runtime failure, or HMC execution errors under the same gate.
Invalid row/algorithm/route/count/coordinate/device/HMC arguments are preflight
validation errors and stop before artifact creation; they are not runtime
blocker artifacts.

Weakest part of the evidence: two retained samples with one burn-in step cannot
diagnose mixing, calibration, posterior geometry, tuning, or convergence.

## Handoff

Proceed to Phase 5 only after read-only review accepts this result and the
refreshed Phase 5 subplan. Phase 5 should be a NUTS-readiness decision. Based
on the current evidence, NUTS should remain blocked unless a reviewed subplan
adds a NUTS implementation, adaptation budget, and diagnostics that are not
present in Phase 4.
