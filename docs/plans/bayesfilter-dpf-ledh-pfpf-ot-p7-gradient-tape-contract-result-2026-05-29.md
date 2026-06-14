# P7 Result: GradientTape Contract

Date: 2026-05-29

## Decision

`P7_GRADIENT_TAPE_CONTRACT_PASSED`

## Result

The named scalar is
`lgssm_ledh_pfpf_ot_corrected_negative_log_normalizer_proxy_tf`.  GradientTape
and finite differences both evaluate this same scalar with fixed observations
and common random numbers.

| Metric | Value |
| --- | --- |
| GradientTape | `1.0815014757961667` |
| finite difference | `1.08150132739393` |
| absolute error | `1.484022367215232e-07` |
| tolerance | `0.01` |

## Skeptical Audit

| Check | Status | Notes |
| --- | --- | --- |
| same-scalar contract | pass | GradientTape and finite difference use the same function and fixed random arrays. |
| proxy overclaim | pass | This is one proxy scalar, not HMC/posterior validation. |
| missing stop conditions | pass | Non-finite/None gradient or tolerance failure veto. |
| backend/contamination | pass | TF/TFP only, no NumPy/student/vendored/highdim imports. |

## Verification

- `CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_ledh_pfpf_gradient_checks_tf`: pass.
- `CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_ledh_pfpf_gradient_checks_tf --validate-only`: pass.
- `CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_ledh_pfpf_gradient_checks_tf --check-reproducibility`: pass.

## What Is Not Concluded

No HMC readiness, posterior correctness, likelihood-score validity beyond this
named proxy scalar, production readiness, NAWM-scale readiness, or monograph
claim.
