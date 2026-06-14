# P9 Result: Range-Bearing Validation

Date: 2026-05-29

## Decision

`P9_RANGE_BEARING_VALIDATION_PASSED`

## Evidence

Source artifacts:

- `experiments/dpf_implementation/reports/dpf-ledh-pfpf-ot-tf-tfp-range-bearing-result-2026-05-29.md`
- `experiments/dpf_implementation/reports/outputs/dpf_ledh_pfpf_ot_tf_tfp_range_bearing_2026-05-29.json`

| Metric | Value |
| --- | --- |
| median bootstrap state RMSE to UKF | `0.07818713843359673` |
| median bootstrap OT-DPF state RMSE to UKF | `0.07942867384530457` |
| median LEDH-PF-PF-OT state RMSE to UKF | `0.07742171157461389` |
| median LEDH latent position RMSE | `0.08208559692155928` |
| median LEDH observation proxy RMSE | `0.1141841886622492` |
| max LEDH Sinkhorn residual | `6.661338147750939e-16` |
| min LEDH Jacobian singular value | `0.643116090267122` |

## Skeptical Audit

| Check | Status | Notes |
| --- | --- | --- |
| wrong baseline | pass | UKF is approximate and explicitly labelled. |
| proxy overclaim | pass | RMSE metrics are proxy diagnostics only. |
| missing stop conditions | pass | Non-finite, UKF caveat, corrected-weight, Jacobian, and Sinkhorn failures veto. |
| drift/contamination | pass | No production, monograph, vendored, or high-dimensional lane edits. |

## Verification

- Range-bearing runner: pass.
- Range-bearing validate-only: pass.
- Range-bearing reproducibility: pass.
- JSON parse: pass.

## What Is Not Concluded

No UKF ground truth, production/API readiness, HMC readiness, posterior
correctness, NAWM-scale readiness, banking/model-risk claim, or monograph claim.
