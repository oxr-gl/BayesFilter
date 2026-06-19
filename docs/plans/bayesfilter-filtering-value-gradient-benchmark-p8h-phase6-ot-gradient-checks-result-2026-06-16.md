# P8h Phase 6 Result: OT Gradient Checks

Date: 2026-06-16

Status: `PASS_OT_GRADIENT_REVIEWED`

## Phase Objective

Run AD gradient checks through LEDH, PF-PF correction, and relaxed Sinkhorn OT
transport for the exact Phase 5 selected Stage 0 route/count.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Are AD gradients finite, connected, and reproducible for the selected P8h OT-resampled scalar on trusted GPU? |
| Baseline/comparator | Phase 5 selected Stage 0 route/count and Phase 4 route diagnostics. Historical P8g no-resampling gradient smoke is context only. |
| Primary criterion | AD gradients through the declared relaxed Sinkhorn OT computational graph are finite, non-`None`, repeatable under fixed randomness, use the exact P8h route/count, and carry seed uncertainty diagnostics. |
| Veto diagnostics | Disconnected gradients; nonfinite gradients; zero/missing gradient norm; no-resampling detour; missing route/manifest fields; missing trusted GPU evidence; finite difference promoted to proof; stochastic categorical-resampling gradient claim. |
| Explanatory diagnostics | Finite-difference deltas, gradient norms, seed variability. |
| Not concluded | Stochastic PF marginal-gradient correctness, HMC readiness, GPU scaling, full-horizon value adequacy, or filter ranking. |

## Skeptical Audit

- Wrong-baseline check: P8g no-resampling G3 remains historical context only
  and is not used as P8h gradient evidence.
- Proxy-metric check: finite-difference agreement is diagnostic only; the
  primary criterion is AD connectivity/finiteness/repeatability through the
  declared relaxed OT route.
- Stop-condition check: wrong route/count, no-resampling detour, missing GPU
  proof, missing manifest fields, or zero/missing/nonfinite gradient norm would
  block.
- Artifact-fit check: the JSON/CSV artifacts preserve route, count, seed,
  gradient, repeatability, FD diagnostic, and GPU tensor evidence.

## Implementation And Checks

Implemented Phase 6-specific OT gradient support in:

- `scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py`;
- `tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py`;
- `tests/test_ledh_pfpf_alg1_ukf_tf.py`.

Local checks:

```bash
PYTHONDONTWRITEBYTECODE=1 python -m py_compile scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py tests/test_ledh_pfpf_alg1_ukf_tf.py
CUDA_VISIBLE_DEVICES=-1 PYTHONDONTWRITEBYTECODE=1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py tests/test_ledh_pfpf_alg1_ukf_tf.py -k "p8h or gradient or sinkhorn or ot"
git diff --check -- scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py tests/highdim/test_filtering_value_gradient_benchmark_p8d_numeric.py tests/test_ledh_pfpf_alg1_ukf_tf.py docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-*
```

Results:

- `py_compile`: passed.
- Focused pytest: `31 passed, 14 deselected, 2 warnings`.
- `git diff --check`: passed.

## Trusted GPU Run

```bash
PYTHONDONTWRITEBYTECODE=1 MPLCONFIGDIR=/tmp python scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py --p8h-ot-gradient-check --row actual_sv --algorithm ledh_pfpf_alg1_ukf_current --horizon 4 --particles 5 --seeds 81120,81121,81122,81123,81124 --device gpu --g0-manifest docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8g-phase0-gpu-probe-result-2026-06-15.md --p8h-resampling-route ot_sinkhorn_barycentric_covariance_carry --coordinate canonical_unconstrained --output-json docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase6-ot-gradient-checks-gpu-2026-06-16.json --output-csv docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase6-ot-gradient-checks-gpu-2026-06-16.csv
```

Artifacts:

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase6-ot-gradient-checks-gpu-2026-06-16.json`;
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase6-ot-gradient-checks-gpu-2026-06-16.csv`.

Programmatic JSON/CSV validation passed.

## Diagnostic Results

Run scope:

- row: `zhao_cui_sv_actual_nongaussian_T1000`;
- algorithm: `ledh_pfpf_alg1_ukf_current`;
- route: `ot_sinkhorn_barycentric_covariance_carry`;
- route variant: `p8h_sv_scalar_graph_ot_resampled_alg1`;
- horizon: `4`;
- particles: `5`;
- seeds: `81120,81121,81122,81123,81124`;
- coordinate: `theta=(Phi^{-1}(gamma), log(beta))`, sigma fixed at `1.0`;
- device: trusted GPU.

Summary:

| Metric | Value |
|---|---:|
| Mean log likelihood | `-2.5683584481630004` |
| Mean gradient | `[-0.39614437892242593, -0.10503046709727153]` |
| Max repeat gradient absolute delta | `0.0` |
| Max finite-difference residual | `4.565204103634812e-09` |
| Values finite | true |
| Gradients finite | true |
| Gradients connected | true |

Per-seed gradient diagnostics:

| Seed | Log likelihood | Gradient | Gradient norm | Repeat delta | FD residual | Resampling count |
|---:|---:|---|---:|---:|---:|---:|
| 81120 | `-2.735546047598974` | `[-0.7196653064013585, -0.6863372245627708]` | `0.9944731967520736` | `0.0` | `2.7443309846830743e-09` | 4 |
| 81121 | `-2.697056795767752` | `[-0.3268992759293101, -0.3640070100518703]` | `0.4892486484089758` | `0.0` | `4.565204103634812e-09` | 4 |
| 81122 | `-2.604389461209828` | `[-0.22812249997472422, 0.702910661733284]` | `0.7390015381398345` | `0.0` | `7.862586137719063e-10` | 4 |
| 81123 | `-2.088980824362422` | `[-0.14678338100947455, 0.12620118118094936]` | `0.19357711401929564` | `0.0` | `1.3011280941555015e-09` | 4 |
| 81124 | `-2.7158191118760246` | `[-0.5592514312972622, -0.30391994378595005]` | `0.6364978363190965` | `0.0` | `9.980609116944095e-10` | 4 |

Device diagnostics:

- value tensors: `/job:localhost/replica:0/task:0/device:GPU:0`;
- gradient tensors: `/job:localhost/replica:0/task:0/device:GPU:0`;
- no silent CPU fallback claim: true.

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not being concluded |
|---|---|---|---|---|---|
| Pass Phase 6 OT-gradient diagnostic, pending review | Passed for selected Stage 0 route/count. | No Phase 6 veto fired. | This is a fixed-seed AD graph diagnostic, not proof of stochastic PF marginal-gradient correctness or long-horizon HMC behavior. | Review this result and refresh Phase 7 for trusted GPU performance/scaling of the exact route/count. | No stochastic PF marginal-gradient correctness, no HMC readiness, no GPU scaling conclusion, no full-horizon adequacy, no filter ranking. |

## Post-Run Red-Team Note

Strongest alternative explanation: the checked scalar is a short-horizon,
fixed-seed computational graph. It shows the declared relaxed Sinkhorn route is
connected and finite for this diagnostic, but it may not represent the
stochastic PF marginal score or longer-horizon behavior.

What would overturn this result: a reviewed rerun showing disconnected or
nonfinite gradients, wrong/no-resampling route, missing GPU proof, or
unacceptable sensitivity under the declared route.

Weakest part of the evidence: finite differences are close for this short
diagnostic, but FD is only explanatory and does not prove gradient correctness
for the stochastic algorithm.

## Handoff

Proceed to Phase 7 only after read-only review accepts this result and the
Phase 7 subplan is refreshed for the exact route/count. Phase 7 must treat this
as gradient-connectivity evidence only, not GPU-scaling or HMC readiness.
