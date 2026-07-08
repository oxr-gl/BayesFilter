# Phase 1 Result: Scalar Filtering-Likelihood Geometry Target

Date: 2026-07-08
Status: `PASSED_AFTER_COMPILED_SCORE_REPAIR`
Master program: `docs/plans/bayesfilter-scalar-filtering-geometry-to-hmc-readiness-master-program-2026-07-08.md`
Subplan: `docs/plans/bayesfilter-scalar-filtering-geometry-to-hmc-readiness-phase1-filtering-geometry-subplan-2026-07-08.md`

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not being concluded |
| --- | --- | --- | --- | --- | --- |
| Scalar filtering-likelihood geometry gate passes after runtime repair | Passed: parent horizon-30 artifact reports `geometry_sanity_passed: true`, finite initial value/score, 72 finite samples >= 45 required, accepted SPD precision, condition number 35.99 <= 1e5, compiled/eager parity passed | No hard vetoes in parent artifact | CPU-hidden non-XLA compiled wrapper was required for runtime; center refinement was rejected outside trust radius, so no MAP-center claim is supported | Draft and review Phase 2 geometry-to-mass handoff using the accepted precision at the declared center | No HMC readiness, HMC convergence, posterior correctness, sampler superiority, statistical ranking, default readiness, GPU/XLA readiness, or Zhao-Cui source-faithfulness |

## Inference Status

| Evidence class | Status |
| --- | --- |
| Hard veto screen | Passed for the parent horizon-30 CPU-hidden filtering-geometry artifact |
| Statistically supported ranking | None; single diagnostic target |
| Descriptive-only differences | Score norm, runtime, residuals, finite-difference curvature, center-refinement diagnostics, and condition number magnitude |
| Default-readiness | Not assessed |
| HMC-readiness | Not assessed; Phase 1 did not run HMC |
| Next evidence needed | Geometry-to-mass handoff with explicit coordinate convention and SPD regularization audit |

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `b1c97c9424907e177f8a95ab98657f07b064a081` |
| Command | `timeout 300 env CUDA_VISIBLE_DEVICES=-1 python docs/benchmarks/benchmark_scalar_ssl_lstm_filtering_geometry_2026_07_08.py --json-path docs/benchmarks/scalar_ssl_lstm_filtering_geometry_cpu_hidden_2026-07-08.json --markdown-path docs/benchmarks/scalar_ssl_lstm_filtering_geometry_cpu_hidden_2026-07-08.md > docs/benchmarks/scalar_ssl_lstm_filtering_geometry_cpu_hidden_2026-07-08.log 2>&1` |
| Environment | `tfgpu` |
| CPU/GPU status | CPU-hidden debug/reference exception, `CUDA_VISIBLE_DEVICES=-1`; log includes expected CUDA no-device noise |
| Data version | `stateless_simulated_scalar_ssl_lstm_filtering_path_v1` |
| Random seed | `(20260708, 2301)` |
| Wall time | 55.58 seconds in parent artifact |
| Plan file | `docs/plans/bayesfilter-scalar-filtering-geometry-to-hmc-readiness-master-program-2026-07-08.md` |
| Subplan file | `docs/plans/bayesfilter-scalar-filtering-geometry-to-hmc-readiness-phase1-filtering-geometry-subplan-2026-07-08.md` |
| Result artifacts | `docs/benchmarks/scalar_ssl_lstm_filtering_geometry_cpu_hidden_2026-07-08.json`, `docs/benchmarks/scalar_ssl_lstm_filtering_geometry_cpu_hidden_2026-07-08.md`, `docs/benchmarks/scalar_ssl_lstm_filtering_geometry_cpu_hidden_2026-07-08.log` |

## Key Diagnostics

| Diagnostic | Value | Role |
| --- | --- | --- |
| Initial center role | `truth_free_initial_center` | Boundary guard; not MAP |
| Initial center score norm | 1.0012 in whitened coordinates | Explanatory only |
| Compiled/eager parity | Passed, value absolute error `7.11e-15`, score max absolute error `0.0` | Implementation veto passed |
| Finite samples | 72 / 72, required 45 | Hard gate passed |
| Low-rank geometry status | `usable` | Hard gate passed |
| Precision eigenvalues | `[0.1841, 0.1841, 4.0780, 6.6260]` | SPD/condition gate passed |
| Precision condition number | 35.99 | Hard gate passed against cap 1e5; magnitude otherwise descriptive |
| Holdout RMSE | 0.0163 <= 0.1892 threshold | Geometry fit gate only |
| Center refinement | Rejected, reason `outside_trust_radius`, `z_norm=0.3139` > trust radius 0.30 | Boundary guard; do not use as MAP |

## Repair History

- Initial horizon-100/260 diagnostic was interrupted after exceeding the visible-execution boundary without writing JSON/Markdown artifacts.
- Repaired horizon-30/72 eager diagnostic hit `timeout 300` and wrote no JSON/Markdown artifact.
- Micro horizon-4/45 preflight completed in 29.7 seconds and wrote a valid artifact. This was harness/runtime evidence only and did not authorize Phase 2.
- Compiled-score repair used `tf.function(jit_compile=False)` for the value/score wrapper, verified compiled/eager parity in tests, and allowed the parent horizon-30/72 diagnostic to complete in 55.58 seconds.

## Checks

- `python -m py_compile docs/benchmarks/benchmark_scalar_ssl_lstm_filtering_geometry_2026_07_08.py` passed.
- `pytest tests/test_scalar_ssl_lstm_filtering_geometry.py tests/test_quadratic_geometry.py -q` passed: 13 passed, with TensorFlow AutoGraph/gast deprecation warnings.
- `git diff --check` passed.
- Local Codex substitute reviews returned `VERDICT: AGREE` for the Phase 1 subplan, runtime micro repair, and compiled-score repair. These reviews are weaker than full Claude review because external Claude review was policy-blocked for private repository context transfer risk.

## Post-Run Red Team

Strongest alternative explanation: the horizon-30 scalar SVD-UKF target is still too small and too favorable, and the accepted low-rank precision may not transfer to longer horizons, full parameter dimension, fixed-SGQF, Zhao-Cui variants, GPU/XLA, or HMC dynamics.

What would overturn the result: a repeated parent-scale run or independent score check showing nonfinite filtering values/scores, mismatched compiled/eager scores, non-SPD precision, or artifact coordinate mismatch under the same contract.

Weakest evidence part: the center is not stationary and refinement was rejected outside the trust radius. Phase 2 must treat the accepted precision as a local geometry initializer at the declared center, not as a certified MAP covariance.

## Next Handoff

Draft and review Phase 2 mass handoff. Phase 2 must:

- use the accepted precision/covariance in the whitened coordinate convention from the artifact;
- regularize and validate SPD/condition properties before any HMC mechanics;
- preserve the `truth_free_initial_center` boundary and avoid MAP claims;
- not run HMC unless Phase 3 is separately planned and reviewed.
