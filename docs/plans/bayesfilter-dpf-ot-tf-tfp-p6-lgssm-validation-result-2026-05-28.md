# P6 Result: LGSSM Validation

Date: 2026-05-28

## Decision

`P6_LGSSM_TF_VALIDATION_PASSED`

## Skeptical Audit

| Check | Status | Evidence |
| --- | --- | --- |
| stale context | pass | P1-P5 results exist. |
| wrong backend | pass | Validation uses TF/TFP runner. |
| NumPy drift | pass | No NumPy imports under `tf_tfp`. |
| proxy overclaim | pass | RMSE/log-likelihood deltas are smoke diagnostics only. |
| stop conditions | pass | Exact smoke caps are enforced in result decision. |
| production/monograph/vendored/highdim drift | pass | No such edits or imports. |
| artifact fitness | pass | Result answers LGSSM/Kalman smoke question. |

## Evidence

- Decision: `DPF_OT_TF_TFP_LGSSM_PASSED`
- median bootstrap filtered-mean RMSE to Kalman: `0.0404376903097443`
- median OT-DPF filtered-mean RMSE to Kalman: `0.04777780918669452`
- median bootstrap abs log-likelihood delta: `0.10923174509147415`
- median OT-DPF abs log-likelihood delta: `0.8277592299940579`
- max OT Sinkhorn residual: `4.3050919044940184e-08`
- CPU-only manifest: `pre_import_cuda_visible_devices=-1`, visible GPUs `[]`

## Artifacts

- `experiments/dpf_implementation/reports/dpf-ot-tf-tfp-lgssm-result-2026-05-28.md`
- `experiments/dpf_implementation/reports/outputs/dpf_ot_tf_tfp_lgssm_2026-05-28.json`

## Non-Implications

LGSSM smoke success is not nonlinear validation, exact likelihood validity,
posterior correctness, HMC readiness, production readiness, or monograph
validation.
