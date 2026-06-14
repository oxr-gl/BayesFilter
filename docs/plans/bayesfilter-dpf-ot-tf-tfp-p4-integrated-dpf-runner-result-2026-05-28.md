# P4 Result: Integrated TF Bootstrap PF And OT-DPF Runners

Date: 2026-05-28

## Decision

`P4_INTEGRATED_TF_RUNNERS_ACCEPTED`

## Skeptical Audit

| Check | Status | Evidence |
| --- | --- | --- |
| stale context | pass | P1-P3 artifacts exist. |
| wrong backend | pass | Filters/runners use TF/TFP imports only. |
| NumPy drift | pass | No NumPy imports under `tf_tfp`. |
| proxy overclaim | pass | Runners produce smoke/proxy diagnostics only. |
| stop conditions | pass | Non-finite rows or mismatched model checksums block validation. |
| production/monograph/vendored/highdim drift | pass | No such edits or imports. |
| artifact fitness | pass | Runners produce LGSSM/range-bearing JSON and markdown outputs. |

## Artifacts

- `experiments/dpf_implementation/tf_tfp/filters/bootstrap_pf_tf.py`
- `experiments/dpf_implementation/tf_tfp/filters/dpf_ot_tf.py`
- `experiments/dpf_implementation/tf_tfp/runners/run_lgssm_ot_dpf_tf.py`
- `experiments/dpf_implementation/tf_tfp/runners/run_range_bearing_ot_dpf_tf.py`

## Evidence

Targeted LGSSM and range-bearing runner executions both passed and wrote JSON
outputs with CPU-only manifests, model checksums, observation checksums, and
reproducibility digests.

## Non-Implications

No production readiness, public API readiness, HMC readiness, posterior
correctness, categorical PF equivalence, or monograph claim follows.
