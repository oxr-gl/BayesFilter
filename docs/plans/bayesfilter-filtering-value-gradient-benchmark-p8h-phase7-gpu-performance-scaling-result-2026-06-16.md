# P8h Phase 7 Result: GPU Performance And Scaling

Date: 2026-06-16

Status: `PASS_SMALL_HMC_FEASIBILITY_REVIEWED`

## Phase Objective

Profile trusted GPU performance for the exact selected P8h route/count and one
adjacent comparison rung, using short-prefix diagnostics only.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Is the selected OT-resampled route/count practically executable on trusted GPU for a small HMC diagnostic? |
| Baseline/comparator | Phase 5/6 selected route/count and adjacent `N=10` P8h comparison rung. P8g no-resampling timing is historical context only. |
| Primary criterion | Profile artifacts show finite trusted-GPU execution for `N=5` at horizons `4,8`, no CPU fallback, and no runtime/OOM blocker for a small HMC smoke. |
| Veto diagnostics | Missing reviewed Phase 5/6 pass; untrusted GPU evidence; missing route/manifest fields; OOM without blocker; CPU fallback treated as success; route/count/configuration mismatch; nonfinite value, covariance, or transport diagnostics. |
| Explanatory diagnostics | Runtime, particle-count comparison, ESS, MCSE. |
| Not concluded | Production readiness, full GPU scaling law, full-horizon performance, HMC readiness, or high-dimensional readiness beyond tested scope. |

## Skeptical Audit

- Wrong-baseline check: P8g timing is historical context only and is not used
  as an operative comparator.
- Proxy-metric check: runtime feasibility does not validate values, gradients,
  HMC behavior, or production readiness.
- Stop-condition check: wrong route/count/configuration, missing trusted GPU
  proof, nonfinite values/covariances/transport, OOM, or CPU fallback would
  block.
- Artifact-fit check: the profile JSON/CSV preserve route, count, device,
  runtime, transport, and selected/adjacent rung diagnostics.

## Commands And Checks

Pre-execution checks:

```bash
git diff --check -- scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py tests/test_ledh_pfpf_alg1_ukf_tf.py docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-*
PYTHONDONTWRITEBYTECODE=1 python -m py_compile scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py tests/test_ledh_pfpf_alg1_ukf_tf.py
rg -n "PASS|N=5|ot_sinkhorn_barycentric_covariance_carry" docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase5-value-filtering-tuning-result-2026-06-15.md docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase6-ot-gradient-checks-result-2026-06-16.md
```

Additional provenance repair checks after manifest option patch:

```bash
PYTHONDONTWRITEBYTECODE=1 python -m py_compile scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py
CUDA_VISIBLE_DEVICES=-1 PYTHONDONTWRITEBYTECODE=1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py -k "p8h or particle"
git diff --check -- scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase7-gpu-performance-scaling-subplan-2026-06-15.md
```

Results:

- `py_compile`: passed.
- Focused provenance pytest: `10 passed, 13 deselected, 2 warnings`.
- `git diff --check`: passed.
- Reviewed Phase 5/6 result status grep: passed.

Trusted GPU profile command:

```bash
PYTHONDONTWRITEBYTECODE=1 MPLCONFIGDIR=/tmp python scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py --p8h-particle-tuning-stage0 --row actual_sv --algorithm ledh_pfpf_alg1_ukf_current --p8h-resampling-route ot_sinkhorn_barycentric_covariance_carry --coordinate canonical_unconstrained --horizons 4,8 --particles 5,10 --seeds 81120,81121,81122,81123,81124 --device gpu --g0-manifest docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase0-gpu-probe-result-2026-06-15.md --p8h-profile-manifest-phase P8H_PHASE7_GPU_PERFORMANCE_SCALING --p8h-profile-manifest-plan docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase7-gpu-performance-scaling-subplan-2026-06-15.md --output-json docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase7-gpu-performance-scaling-profile-2026-06-16.json --output-csv docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase7-gpu-performance-scaling-profile-2026-06-16.csv --selected-blocked-csv docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase7-gpu-performance-scaling-selected-blocked-2026-06-16.csv
```

Artifacts:

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase7-gpu-performance-scaling-profile-2026-06-16.json`;
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase7-gpu-performance-scaling-profile-2026-06-16.csv`;
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase7-gpu-performance-scaling-selected-blocked-2026-06-16.csv`.

Programmatic validation passed.

## Profile Results

Manifest highlights:

| Field | Value |
|---|---|
| Phase | `P8H_PHASE7_GPU_PERFORMANCE_SCALING` |
| Plan | `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase7-gpu-performance-scaling-subplan-2026-06-15.md` |
| Device | Trusted GPU; TensorFlow recorded `/device:GPU:0` |
| Route | `ot_sinkhorn_barycentric_covariance_carry` |
| Route variant | `p8h_sv_scalar_graph_ot_resampled_alg1` |
| Particles | `5,10` |
| Horizons | `4,8` |
| Seeds | `81120,81121,81122,81123,81124` |
| Wall time | `185.755875` seconds |

Rung summary:

| Horizon | N | Runtime seconds | Finite | Transport pass | Trusted GPU | MCSE | Min relative ESS |
|---:|---:|---:|---|---|---|---:|---:|
| 4 | 5 | `35.546933` | true | true | true | `0.12193456145119645` | `0.8038143813839937` |
| 4 | 10 | `39.144796` | true | true | true | `0.08867057298002864` | `0.7544068195810831` |
| 8 | 5 | `39.274453` | true | true | true | `0.5092899481855204` | `0.40324545666386885` |
| 8 | 10 | `48.130157` | true | true | true | `0.34975722827069927` | `0.44278208320912543` |

Selected/blocked table preserved `N=5` as the selected Stage 0 count with
`N=10` checked as adjacent rung.

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not being concluded |
|---|---|---|---|---|---|
| Pass Phase 7 small-HMC-feasibility profile | Passed for short-prefix `N=5` and adjacent `N=10`. | No Phase 7 veto fired; read-only review returned `VERDICT: AGREE`. | The profile is short-prefix only and does not show full-horizon scaling or HMC behavior. | Review the refreshed Phase 8 subplan for the smallest HMC diagnostic tier only, then execute if accepted. | No HMC readiness, no production readiness, no full GPU scaling law, no full-horizon performance, no filter ranking. |

## Post-Run Red-Team Note

Strongest alternative explanation: the short-prefix GPU runtime is feasible
because horizons `4,8` are tiny; longer horizons or HMC evaluation loops may
still be too slow.

What would overturn this result: a reviewed HMC smoke or longer-prefix profile
showing OOM, CPU fallback, nonfinite diagnostics, or runtime too high for even
a minimal diagnostic.

Weakest part of the evidence: Phase 7 did not profile an HMC kernel itself; it
only established that the selected value/gradient route is practically
executable enough to justify a small HMC diagnostic attempt.

## Handoff

Read-only review accepted this result with `VERDICT: AGREE`. Proceed to Phase
8 only after the refreshed Phase 8 subplan is reviewed as a smallest-tier HMC
diagnostic. Phase 8 must not claim HMC readiness unless its own declared HMC
diagnostics pass.
