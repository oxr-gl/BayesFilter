# Phase R12 Closeout: GPU XLA TF32 Contract E Manual Score Route

Date: 2026-06-30

Status: `EXECUTED_FAILED_KALMAN_MCSE_GATE`

## Decision Table

| Field | Result |
| --- | --- |
| Decision | R12 unblocked the score-route wiring: GPU/XLA/TF32 manual reverse-scan scores are finite. Do not treat the estimator as passing, because the Kalman 2*MCSE gate failed. |
| Primary criterion status | Failed. `D=2` failed value, `ar_coefficient`, and `log_observation_variance`; `D=1` failed `ar_coefficient` and `log_observation_variance`. |
| Veto diagnostic status | Route/device vetoes passed: visible GPU, XLA, TF32, manual score route, finite values/scores, no ridge failure, covariance residual below limit. |
| Main uncertainty | The dominant remaining suspect is finite Sinkhorn/transport budget, because row residuals are very large at `eps0.55_steps2` while column residuals and Contract E covariance restoration are clean. |
| Next justified action | R13 should be a GPU/XLA/TF32 manual-score Sinkhorn budget ladder at fixed `N=1000,T=10,R=10`, with row residual as a veto/diagnostic and Kalman value/score as the primary gate. |
| Not concluded | No SIR/SV correctness, no HMC readiness, no production readiness, no FD certificate, and no claim that the remaining bias is solely finite `N`. |

## Run Manifest

- Command: `bash scripts/run_contract_e_r12_gpu_manual_score.sh`
- Plan: `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase3-r12-gpu-xla-manual-score-route-plan-2026-06-30.md`
- JSON: `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase3-r12-gpu-xla-tf32-manual-score-2026-06-30.json`
- Markdown result: `docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase3-r12-gpu-xla-tf32-manual-score-result-2026-06-30.md`
- TensorFlow: `2.19.1`
- Device: `["LogicalDevice(name='/device:GPU:0', device_type='GPU')"]`
- XLA: `True`
- TF32: `True`
- Elapsed seconds: `38.676`
- Route: `gpu_xla_tf32_batched_contract_e_manual_reverse_scan_score_diagnostic`
- Score route: `manual-reverse-scan`
- Settings: `[{'epsilon': 0.55, 'label': 'eps0.55_steps2', 'steps': 2}]`

## Result Summary

| Dim | Value z | Failed score components | Max row residual | Max column residual | Max covariance residual |
| ---: | ---: | --- | ---: | ---: | ---: |
| 2 | -2.053 | `ar_coefficient, log_observation_variance` | 0.956566 | 1.073e-06 | 3.047e-07 |
| 1 | -1.466 | `ar_coefficient, log_observation_variance` | 0.995968 | 8.345e-07 | 2.124e-07 |

## Interpretation

The R11 all-NaN score failure was a route-wiring problem. R12 replaces the outer-tape score wrapper with a manual reverse scan and produces finite per-seed scores on the trusted GPU/XLA/TF32 path.

The remaining failure is now a real numerical/statistical gate failure under the current `eps0.55_steps2` transport budget. The largest diagnostic clue is the row residual: approximately `0.96` for `D=2` and `1.00` for `D=1`. Those values are too large to ignore and make the two-step Sinkhorn budget the next most likely target.

## Checks

Passed before the GPU run:

```bash
python -m py_compile docs/benchmarks/diagnose_ledh_pfpf_ot_contract_e_lgssm_gradient.py docs/benchmarks/diagnose_ledh_pfpf_ot_contract_e_lgssm_gpu_score.py docs/benchmarks/contract_e_reset_tf.py
python -m pytest tests/test_contract_e_phase3_gradient_route_audit.py -q
python -m pytest tests/test_contract_e_cholesky_ridge_reset.py -q
```
