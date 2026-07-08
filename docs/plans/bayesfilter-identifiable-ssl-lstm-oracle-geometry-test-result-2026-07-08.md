# BayesFilter Identifiable SSL-LSTM Oracle Geometry Test Result - 2026-07-08

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not being concluded |
| --- | --- | --- | --- | --- | --- |
| Proper complete-data oracle geometry diagnostic passes after utility repair | Passed: MAP candidate accepted, dense Hessian SPD, finite sample count 260 >= required 45, low-rank geometry accepted, relative Frobenius error 0.1656 <= 0.45 | No vetoes in final artifact | Complete-data oracle target is easier than filtering likelihood; max absolute dense residual remains explanatory-only at 7.0176 | Try the same initializer on a scalar filtering-likelihood geometry diagnostic before HMC | No filtering-likelihood validity, no HMC convergence, no posterior correctness, no sampler superiority, no Zhao-Cui source-faithfulness, no default readiness |

## Inference Status

| Evidence class | Status |
| --- | --- |
| Hard veto screen | Passed in `docs/benchmarks/identifiable_ssl_lstm_oracle_geometry_cpu_hidden_2026-07-08.json` |
| Statistically supported ranking | None; this was a single diagnostic target |
| Descriptive-only differences | Runtime, condition numbers, train/holdout RMSE, and max absolute dense-precision residual |
| Default-readiness | Not assessed |
| Next evidence needed | Filtering-likelihood geometry diagnostic, then bounded HMC diagnostics only if the filtering geometry remains viable |

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `b1c97c9424907e177f8a95ab98657f07b064a081` |
| Command | `CUDA_VISIBLE_DEVICES=-1 python docs/benchmarks/benchmark_identifiable_ssl_lstm_oracle_geometry_2026_07_08.py` |
| Environment | `tfgpu` |
| CPU/GPU status | CPU-hidden debug/reference exception, `CUDA_VISIBLE_DEVICES=-1` |
| Data version | `stateless_simulated_scalar_ssl_lstm_complete_data_oracle_v1` |
| Random seed | `(20260708, 1701)` |
| Wall time | 23.7 seconds in final artifact |
| Plan file | `docs/plans/bayesfilter-identifiable-ssl-lstm-oracle-geometry-test-plan-2026-07-08.md` |
| Result artifacts | `docs/benchmarks/identifiable_ssl_lstm_oracle_geometry_cpu_hidden_2026-07-08.json`, `docs/benchmarks/identifiable_ssl_lstm_oracle_geometry_cpu_hidden_2026-07-08.md` |

## What Changed

- Added `docs/benchmarks/benchmark_identifiable_ssl_lstm_oracle_geometry_2026_07_08.py`.
- Added `tests/test_identifiable_ssl_lstm_oracle_geometry.py`.
- Repaired `bayesfilter/inference/quadratic_geometry.py` so low-rank SPD quadratic geometry uses score-difference curvature fitting in whitened coordinates and caps the effective directional rank at `dim - 1`.
- Updated the plan contract so max absolute dense residual is explanatory only; the promotion gate uses relative Frobenius agreement plus hard validity gates.

## Diagnostic History

- Truth-centered diagnostic was preserved as `docs/benchmarks/identifiable_ssl_lstm_oracle_geometry_truth_center_rejected_cpu_hidden_2026-07-08.json`; it failed because the finite simulated path had a nonzero score at the generating truth.
- MAP-centered value-only/default low-rank fits failed or nearly failed because the old value-only regression did not reliably recover known quadratic curvature.
- Final score-difference curvature fit passed the proper oracle geometry gate.

## Checks

- `python -m py_compile bayesfilter/inference/quadratic_geometry.py docs/benchmarks/benchmark_identifiable_ssl_lstm_oracle_geometry_2026_07_08.py` passed.
- `pytest tests/test_quadratic_geometry.py tests/test_identifiable_ssl_lstm_oracle_geometry.py -q` passed: 13 passed, 27 warnings.
- `CUDA_VISIBLE_DEVICES=-1 python docs/benchmarks/benchmark_identifiable_ssl_lstm_oracle_geometry_2026_07_08.py` passed.
- `git diff --check` passed.

## Post-Run Red Team

Strongest alternative explanation: the complete-data oracle target is too favorable, so passing this gate may not transfer to a filtering likelihood where latent states are integrated out or approximated.

What would overturn the result: a synthetic quadratic or oracle target showing score-difference curvature fitting produces non-SPD, non-finite, or relative-error-failing geometry under the same contract.

Weakest evidence part: the max absolute dense-precision residual still exceeds the descriptive threshold; it is not a hard veto because the low-rank initializer intentionally compresses curvature and passed the relative SPD geometry screen.
