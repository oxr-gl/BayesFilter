# LEDH-PFPF-OT LGSSM Worst-Time Budget Diagnostic Result

Date: 2026-06-26T13:00:36.117116+00:00

## Manifest

| Field | Value |
|---|---|
| num_particles | `128` |
| dense_parity_particles | `64` |
| seed_count | `10` |
| baseline_steps | `100` |
| candidate_steps | `[100, 200, 400]` |
| device_scope | `cpu` |
| cuda_visible_devices | `-1` |
| tf32_execution_enabled | `True` |
| runtime_seconds | `94.25710308999987` |

## Decision Table

| Field | Status |
|---|---|
| decision | Focused worst-time row residuals pass, but covariance contraction remains live. |
| primary_criterion_status | state_dim=1 passes at steps=400 with row=2.831e-04; state_dim=2 passes at steps=400 with row=1.192e-06; state_dim=1 best cov ratio=0.618472; state_dim=2 best cov ratio=0.379565 |
| veto_diagnostic_status | PASS |
| main_uncertainty | The target clouds are produced by baseline steps before the target; a full-propagation higher-budget run is still needed if this passes. |
| next_justified_action | Move to reset covariance semantics before changing the statistical harness. |
| not_concluded | No gradient correctness, SIR correctness, GPU/XLA performance, HMC readiness, posterior correctness, production readiness, or broad scientific validity. |

## Candidate Residuals

| State dim | Target t | Steps | Row residual | Streaming row residual | Column residual | Dense/streaming max diff | Subset row residual | Cov trace ratio | Mean shift |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 8 | 100 | 1.509e-02 | 1.509e-02 | 5.960e-07 | 0.000e+00 | 7.586e-03 | 0.618390 | 9.686e-09 |
| 1 | 8 | 200 | 4.357e-03 | 4.357e-03 | 7.153e-07 | 0.000e+00 | 1.113e-03 | 0.618450 | 4.470e-09 |
| 1 | 8 | 400 | 2.831e-04 | 2.831e-04 | 7.153e-07 | 0.000e+00 | 2.199e-05 | 0.618472 | 5.960e-09 |
| 2 | 7 | 100 | 3.241e-03 | 3.241e-03 | 5.960e-07 | 0.000e+00 | 1.106e-03 | 0.379591 | 2.792e-08 |
| 2 | 7 | 200 | 2.536e-04 | 2.536e-04 | 5.364e-07 | 0.000e+00 | 3.123e-05 | 0.379567 | 2.610e-08 |
| 2 | 7 | 400 | 1.192e-06 | 1.192e-06 | 5.960e-07 | 0.000e+00 | 3.576e-07 | 0.379565 | 2.814e-08 |

## Target Value Context

| State dim | Target t | Prefix mean | Kalman prefix | Prefix delta | Target increment delta | ESS mean | ESS min |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 8 | -5.984098 | -6.242581 | 0.258483 | 0.025829 | 127.516 | 127.016 |
| 2 | 7 | -10.447180 | -11.122513 | 0.675333 | 0.085663 | 127.200 | 126.866 |
