# P8i Phase 3 Result: GPU Scaling Profile

Date: 2026-06-16

Status: `PASS_GPU_SCALING_FOR_TIER1_REVIEWED`

## Phase Objective

Profile trusted GPU runtime scaling beyond P8h horizons `4,8` for the exact
P8i route/count before any longer HMC diagnostic.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Is the selected longer-prefix route/count practically executable on trusted GPU for the next bounded HMC diagnostic? |
| Baseline/comparator | P8h Phase 7 short-prefix GPU profile and P8i Phase 1/2 value/gradient runtimes. |
| Primary criterion | Finite trusted-GPU values and transport diagnostics at horizons `16,32`, `N=5`, with the declared HMC projection rule passing; otherwise explicit blocker. |
| Veto diagnostics | CPU fallback; OOM; nonfinite values/covariances/transport; route/count mismatch; runtime projection beyond budget. |
| Explanatory diagnostics | Runtime scaling, optional adjacent `N=10`, memory notes, ESS, MCSE, transport residuals. |
| Not concluded | Full GPU scaling law, production readiness, HMC readiness, filter ranking, or high-dimensional readiness. |

## Skeptical Audit

- Wrong-baseline check: P8h Phase 7 short-prefix timing is context only; Phase
  3 measures horizons `16,32`.
- Proxy-metric check: runtime feasibility does not validate HMC behavior or
  posterior convergence.
- Stop-condition check: Phase 4 may proceed only if the selected `N=5` profile
  passes finite/trusted-GPU/transport/runtime gates and the concrete HMC
  projection rule.
- Artifact-fit check: the JSON/CSV artifacts preserve route, count, horizons,
  seeds, trusted GPU evidence, runtime, transport diagnostics, P8i plan path,
  and nonclaims.

## Codepath Boundary

The current runner uses `--p8h-particle-tuning-stage0` to produce finite
value/transport/runtime summaries. In Phase 3 this is only a profiling
codepath. The emitted selected/blocked CSVs still use Stage-0 tuning
vocabulary and report `BLOCK_P8H_PARTICLE_TUNING_MISSING_NEXT_RUNG` when a
single particle count is profiled. That is not interpreted as a Phase 3 tuning
failure because Phase 3 does not select a particle count. The operative Phase
3 evidence is the evaluated rung table and the HMC projection rule.

## Commands And Checks

Pre/post-run checks:

```bash
PYTHONDONTWRITEBYTECODE=1 python -m py_compile scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py
CUDA_VISIBLE_DEVICES=-1 PYTHONDONTWRITEBYTECODE=1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py -k "p8h_phase5 or p8h_ot_gradient"
python -m json.tool docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-phase3-gpu-scaling-selected-n5-2026-06-16.json
python -m json.tool docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-phase3-gpu-scaling-adjacent-n10-2026-06-16.json
git diff --check -- docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-* scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py
```

Results:

- `py_compile`: passed.
- Focused pytest before Phase 3: `9 passed, 21 deselected, 2 warnings`.
- JSON validation: passed for selected `N=5` and adjacent `N=10`.
- `git diff --check`: passed.

Selected `N=5` profile command:

```bash
PYTHONDONTWRITEBYTECODE=1 MPLCONFIGDIR=/tmp python scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py --p8h-particle-tuning-stage0 --row actual_sv --algorithm ledh_pfpf_alg1_ukf_current --p8h-resampling-route ot_sinkhorn_barycentric_covariance_carry --coordinate canonical_unconstrained --horizons 16,32 --particles 5 --seeds 81120,81121,81122,81123,81124 --device gpu --g0-manifest docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase0-gpu-probe-result-2026-06-15.md --runtime-budget-seconds 1800 --p8h-profile-manifest-phase P8I_PHASE3_GPU_SCALING_SELECTED_N5 --p8h-profile-manifest-plan docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-phase3-gpu-scaling-subplan-2026-06-16.md --output-json docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-phase3-gpu-scaling-selected-n5-2026-06-16.json --output-csv docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-phase3-gpu-scaling-selected-n5-2026-06-16.csv --selected-blocked-csv docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-phase3-gpu-scaling-selected-n5-selected-blocked-2026-06-16.csv
```

Adjacent `N=10` explanatory profile command:

```bash
PYTHONDONTWRITEBYTECODE=1 MPLCONFIGDIR=/tmp python scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py --p8h-particle-tuning-stage0 --row actual_sv --algorithm ledh_pfpf_alg1_ukf_current --p8h-resampling-route ot_sinkhorn_barycentric_covariance_carry --coordinate canonical_unconstrained --horizons 16,32 --particles 10 --seeds 81120,81121,81122,81123,81124 --device gpu --g0-manifest docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase0-gpu-probe-result-2026-06-15.md --runtime-budget-seconds 1800 --p8h-profile-manifest-phase P8I_PHASE3_GPU_SCALING_ADJACENT_N10 --p8h-profile-manifest-plan docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-phase3-gpu-scaling-subplan-2026-06-16.md --output-json docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-phase3-gpu-scaling-adjacent-n10-2026-06-16.json --output-csv docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-phase3-gpu-scaling-adjacent-n10-2026-06-16.csv --selected-blocked-csv docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8i-phase3-gpu-scaling-adjacent-n10-selected-blocked-2026-06-16.csv
```

## Results

| Horizon | N | Runtime seconds | Finite | Transport pass | Trusted GPU | Runtime budget | Mean log likelihood | MCSE | Min relative ESS |
|---:|---:|---:|---|---|---|---|---:|---:|---:|
| 16 | 5 | `50.011299` | true | true | true | within | `-8.206925764133295` | `0.4239197536475199` | `0.3171734228962384` |
| 32 | 5 | `69.100267` | true | true | true | within | `-16.271024752723953` | `0.638939306310582` | `0.3171734228962384` |
| 16 | 10 | `66.498299` | true | true | true | within | `-8.12720112559305` | `0.264306830814899` | `0.28129792005599485` |
| 32 | 10 | `101.689673` | true | true | true | within | `-15.725237466322332` | `0.2245172697039196` | `0.26070678480212783` |

Run wall times:

- selected `N=5`: `131.251189` seconds;
- adjacent `N=10`: `180.621767` seconds.

## HMC Projection

Phase 3 projection rule:

- worst selected-count H32 seed value runtime threshold: `120` seconds;
- observed selected-count H32 rung runtime per five seeds: `69.100267`
  seconds;
- conservative worst-seed proxy used here: the H32 selected-count rung runtime
  `69.100267` seconds, which is below `120`;
- projected Tier-1 HMC cost: `5 * 69.100267 = 345.501335` seconds;
- Tier-1 budget: `900` seconds.

The projection passes. Phase 4 may be refreshed for a bounded fixed-kernel
Tier-1 diagnostic, pending read-only review. This projection does not claim
HMC readiness, valid tuning, or posterior convergence.

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not being concluded |
|---|---|---|---|---|---|
| Pass Phase 3 GPU runtime profile for a bounded Tier-1 HMC diagnostic, pending review. | Selected `N=5` H16/H32 rungs are finite, trusted-GPU, transport-valid, within runtime budget, and pass the HMC projection rule. | No Phase 3 selected-count veto fired. | The projection is a coarse runtime gate; HMC can still fail numerically or geometrically. | Refresh Phase 4 as a tiny fixed-kernel Tier-1 diagnostic with explicit vetoes and no NUTS/adaptation. | No full GPU scaling law, no HMC readiness, no production readiness, no posterior convergence, no ranking, no default policy. |

## Post-Run Red-Team Note

Strongest alternative explanation: value-profile runtimes understate HMC cost
because HMC repeatedly evaluates gradients and may incur overhead not captured
by the profile.

What would overturn this result: a reviewed HMC diagnostic showing nonfinite
samples/trace quantities, CPU fallback, runtime budget failure, or target
evaluation instability.

Weakest part of the evidence: the HMC projection uses observed profiling
runtime as a conservative planning gate, not a measured HMC runtime.

## Handoff

Proceed to Phase 4 only after read-only review accepts this result and the
refreshed Phase 4 subplan. Phase 4 must remain a bounded fixed-kernel HMC
diagnostic first, with no NUTS, no adaptation, no posterior-convergence claim,
and no production-readiness claim.
