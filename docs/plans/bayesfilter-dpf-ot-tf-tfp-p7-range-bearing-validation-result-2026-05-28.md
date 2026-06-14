# P7 Result: Range-Bearing Validation

Date: 2026-05-28

## Decision

`P7_RANGE_BEARING_TF_VALIDATION_PASSED`

## Skeptical Audit

| Check | Status | Evidence |
| --- | --- | --- |
| stale context | pass | P1-P5 results exist. |
| wrong backend | pass | Validation uses TF/TFP runner. |
| NumPy drift | pass | No NumPy imports under `tf_tfp`. |
| proxy overclaim | pass | UKF and RMSE metrics are proxy diagnostics only. |
| stop conditions | pass | UKF finite status and Sinkhorn residuals passed. |
| production/monograph/vendored/highdim drift | pass | No such edits or imports. |
| artifact fitness | pass | Result answers range-bearing/UKF smoke question. |

## Evidence

- Decision: `DPF_OT_TF_TFP_RANGE_BEARING_PASSED`
- median bootstrap state RMSE to UKF: `0.04928816435621779`
- median OT-DPF state RMSE to UKF: `0.06459801669123823`
- median bootstrap latent position RMSE: `0.07149138539801286`
- median OT-DPF latent position RMSE: `0.07566496675661072`
- median bootstrap observation proxy RMSE: `0.09654120366403485`
- median OT-DPF observation proxy RMSE: `0.11491050363308848`
- max OT Sinkhorn residual: `4.440892098500626e-16`
- CPU-only manifest: `pre_import_cuda_visible_devices=-1`, visible GPUs `[]`

## Artifacts

- `experiments/dpf_implementation/reports/dpf-ot-tf-tfp-range-bearing-result-2026-05-28.md`
- `experiments/dpf_implementation/reports/outputs/dpf_ot_tf_tfp_range_bearing_2026-05-28.json`

## Non-Implications

UKF is approximate and not ground truth.  Proxy RMSE is not posterior
correctness, HMC readiness, production readiness, or monograph validation.
