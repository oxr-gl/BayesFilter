# P1 Result: LGSSM Fixture And Kalman Reference

Date: 2026-05-28

## Decision

`P1_LGSSM_TF_KALMAN_ACCEPTED`

## Skeptical Audit

| Check | Status | Evidence |
| --- | --- | --- |
| stale context | pass | Existing NumPy LGSSM was used only as prototype context. |
| wrong backend | pass | New fixture/reference use TF/TFP imports only. |
| NumPy drift | pass | No NumPy imports under `tf_tfp`. |
| proxy overclaim | pass | Kalman is exact only for this LGSSM fixture. |
| stop conditions | pass | Finite Kalman outputs are required. |
| production/monograph/vendored/highdim drift | pass | No such edits or imports. |
| artifact fitness | pass | Fixture and Kalman reference support LGSSM validation. |

## Artifacts

- `experiments/dpf_implementation/tf_tfp/fixtures/lgssm_tf.py`
- `experiments/dpf_implementation/tf_tfp/references/kalman_lgssm_tf.py`

## Evidence

Import probe built a horizon-25 LGSSM fixture and finite TF Kalman result.

## Non-Implications

No nonlinear validation, OT resampling validation, production readiness,
posterior correctness, HMC readiness, or monograph claim follows.
