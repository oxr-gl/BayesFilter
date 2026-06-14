# P8 Result: LGSSM Validation

Date: 2026-05-29

## Decision

`P8_LGSSM_VALIDATION_PASSED`

## Evidence

Source artifacts:

- `experiments/dpf_implementation/reports/dpf-ledh-pfpf-ot-tf-tfp-lgssm-result-2026-05-29.md`
- `experiments/dpf_implementation/reports/outputs/dpf_ledh_pfpf_ot_tf_tfp_lgssm_2026-05-29.json`

| Metric | Value |
| --- | --- |
| median bootstrap RMSE to Kalman | `0.078913898277458` |
| median bootstrap OT-DPF RMSE to Kalman | `0.06460949367916666` |
| median LEDH-PF-PF-OT RMSE to Kalman | `0.06830431164955209` |
| median LEDH abs loglik delta | `1.1247968987647852` |
| max LEDH Sinkhorn residual | `5.427581322575703e-08` |
| min LEDH Jacobian singular value | `0.8048770788598271` |

## Skeptical Audit

| Check | Status | Notes |
| --- | --- | --- |
| wrong baseline | pass | Kalman is exact for this LGSSM; PF/OT-DPF are comparators. |
| proxy overclaim | pass | Smoke caps are run-validity gates, not scientific validation. |
| missing stop conditions | pass | Non-finite, Sinkhorn, log-det, and CPU manifest failures veto. |
| drift/contamination | pass | No production, monograph, vendored, or high-dimensional lane edits. |

## Verification

- LGSSM runner: pass.
- LGSSM validate-only: pass.
- LGSSM reproducibility: pass.
- JSON parse: pass.

## What Is Not Concluded

No production/API readiness, HMC readiness, posterior correctness,
NAWM-scale readiness, banking/model-risk claim, or monograph claim.
