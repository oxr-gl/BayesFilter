# High-Dimensional Nonlinear Filtering Smoke Diagnostic

JSON artifact: `docs/benchmarks/bayesfilter-highdim-nonlinear-filtering-smoke-2026-05-27.json`

Diagnostic only.  No high-dimensional filtering, HMC, GPU, XLA, NAWM, posterior-accuracy, or production-default claim is made.

## Environment

- Python: `3.11.14`
- TensorFlow: `2.19.1`
- CUDA_VISIBLE_DEVICES: `-1`
- Command: `docs/benchmarks/benchmark_highdim_nonlinear_filtering_smoke.py --output docs/benchmarks/bayesfilter-highdim-nonlinear-filtering-smoke-2026-05-27.json --markdown-output docs/benchmarks/bayesfilter-highdim-nonlinear-filtering-smoke-2026-05-27.md --point-cap 256`

## Rows

| Case | Blocks | Backend | Mode | Aug Dim | Points | Status | Runtime s | Label |
| --- | ---: | --- | --- | ---: | ---: | --- | ---: | --- |
| model_b | 1 | tf_svd_cubature | eager | 3 | 6 | ok | 0.012027 | diagnostic_only |
| model_b | 1 | tf_svd_cubature | xla | 3 | 6 | ok | 0.000571 | diagnostic_only |
| model_b | 1 | tf_svd_ukf | eager | 3 | 7 | ok | 0.012818 | diagnostic_only |
| model_b | 1 | tf_svd_ukf | xla | 3 | 7 | ok | 0.000535 | diagnostic_only |
| model_b | 1 | tf_svd_cut4 | eager | 3 | 14 | ok | 0.013881 | diagnostic_only |
| model_b | 1 | tf_svd_cut4 | xla | 3 | 14 | ok | 0.000693 | diagnostic_only |
| block_model_b | 2 | tf_svd_cubature | eager | 6 | 12 | ok | 0.013583 | diagnostic_only |
| block_model_b | 2 | tf_svd_cubature | xla | 6 | 12 | ok | 0.000572 | diagnostic_only |
| block_model_b | 2 | tf_svd_ukf | eager | 6 | 13 | ok | 0.014302 | diagnostic_only |
| block_model_b | 2 | tf_svd_ukf | xla | 6 | 13 | ok | 0.000563 | diagnostic_only |
| block_model_b | 2 | tf_svd_cut4 | eager | 6 | 76 | ok | 0.014651 | diagnostic_only |
| block_model_b | 2 | tf_svd_cut4 | xla | 6 | 76 | ok | 0.000585 | diagnostic_only |
| block_model_b | 4 | tf_svd_cubature | eager | 12 | 24 | ok | 0.017698 | diagnostic_only |
| block_model_b | 4 | tf_svd_cubature | xla | 12 | 24 | ok | 0.000643 | diagnostic_only |
| block_model_b | 4 | tf_svd_ukf | eager | 12 | 25 | ok | 0.016811 | diagnostic_only |
| block_model_b | 4 | tf_svd_ukf | xla | 12 | 25 | ok | 0.000791 | diagnostic_only |
| block_model_b | 4 | tf_svd_cut4 | eager | 12 | 4120 | skipped |  | skip_point_cap_for_scaling_diagnostic |
| block_model_b | 4 | tf_svd_cut4 | xla | 12 | 4120 | skipped |  | skip_point_cap_for_scaling_diagnostic |

## Non-Implication

P8 smoke rows are BayesFilter execution diagnostics only. They do not certify high-dimensional filtering validity, HMC readiness, NAWM readiness, GPU speedup, XLA readiness, posterior accuracy, or production default policy.
