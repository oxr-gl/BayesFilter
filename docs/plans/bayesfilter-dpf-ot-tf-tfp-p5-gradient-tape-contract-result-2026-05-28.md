# P5 Result: GradientTape Same-Scalar Contract

Date: 2026-05-28

## Decision

`P5_GRADIENT_TAPE_SAME_SCALAR_PASSED`

## Skeptical Audit

| Check | Status | Evidence |
| --- | --- | --- |
| stale context | pass | P1/P3/P4 artifacts exist. |
| wrong backend | pass | Gradient path uses TensorFlow `GradientTape`. |
| NumPy drift | pass | No NumPy imports under `tf_tfp`. |
| proxy overclaim | pass | Gradient is for one named proxy scalar only. |
| stop conditions | pass | Same-scalar mismatch or non-finite gradient would block. |
| production/monograph/vendored/highdim drift | pass | No such edits or imports. |
| artifact fitness | pass | Result answers whether autodiff can see the named scalar. |

## Artifact

- `experiments/dpf_implementation/tf_tfp/runners/run_gradient_checks_tf.py`

## Evidence

- Scalar: `lgssm_relaxed_ot_negative_log_normalizer_proxy_tf`
- `tf.GradientTape` gradient: `0.3591554456487759`
- finite-difference reference: `0.35915332758218455`
- absolute error: `2.118066591338952e-06`

## Non-Implications

Finite gradient evidence is not posterior correctness, HMC readiness, production
readiness, or likelihood-score validity beyond this named proxy scalar.
