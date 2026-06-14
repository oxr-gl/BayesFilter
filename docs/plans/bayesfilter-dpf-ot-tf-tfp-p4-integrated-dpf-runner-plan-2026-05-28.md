# P4 Plan: Integrated TF Bootstrap PF And OT-DPF Runners

Date: 2026-05-28

## Evidence Contract

Question: can the lane implement TF/TFP bootstrap PF and finite-Sinkhorn relaxed
OT-DPF value paths for the P1/P2 fixtures?

Primary criterion: finite log-normalizer proxies, finite filtered means and
variances, finite ESS, bounded resampling diagnostics, and no NumPy imports.

Required manifest/checksum fields: model checksum, observation checksum,
method id, seed, particle count, CPU-only manifest with
`pre_import_cuda_visible_devices=-1`, TensorFlow/TFP versions, command, runtime,
and output path.

Veto diagnostics: non-finite weights, malformed model callables, missing
resampling caveat, value path outside TF/TFP, or NumPy import in `tf_tfp`.

What must not be concluded: no posterior correctness, production readiness,
HMC readiness, monograph claim, or categorical PF equivalence.

## Inputs

- P1 LGSSM/Kalman fixture.
- P2 range-bearing/UKF fixture.
- P3 Sinkhorn resampler.

## Outputs

- `experiments/dpf_implementation/tf_tfp/filters/bootstrap_pf_tf.py`
- `experiments/dpf_implementation/tf_tfp/filters/dpf_ot_tf.py`
- `experiments/dpf_implementation/tf_tfp/runners/run_lgssm_ot_dpf_tf.py`
- `experiments/dpf_implementation/tf_tfp/runners/run_range_bearing_ot_dpf_tf.py`
- `docs/plans/bayesfilter-dpf-ot-tf-tfp-p4-integrated-dpf-runner-result-2026-05-28.md`
- draft JSON smoke outputs under
  `experiments/dpf_implementation/reports/outputs/dpf_ot_tf_tfp_lgssm_2026-05-28.json`
  and
  `experiments/dpf_implementation/reports/outputs/dpf_ot_tf_tfp_range_bearing_2026-05-28.json`

## Allowed Write Set

- `experiments/dpf_implementation/tf_tfp/filters/`
- `experiments/dpf_implementation/tf_tfp/runners/`
- `docs/plans/bayesfilter-dpf-ot-tf-tfp-p4-*-2026-05-28.md`

## Forbidden Write Set

Production `bayesfilter/`, tests, monograph chapters, vendored code, highdim
lane, and existing NumPy prototype modules.

## Skeptical Audit Checklist

Check stale context, wrong backend, NumPy drift, proxy overclaim, missing stop
conditions, hidden production drift, monograph drift, vendored contamination,
highdim contamination, and artifact fitness.

## Stop Conditions

Stop if TF runners cannot set CPU-only environment before TensorFlow import, if
weights become non-finite, or if model comparisons use mismatched observations.

If a stop condition fires, write
`docs/plans/bayesfilter-dpf-ot-tf-tfp-p4-integrated-dpf-runner-result-2026-05-28.md`
with decision `P4_STRUCTURED_BLOCKER`.

## Verification Commands

```bash
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_lgssm_ot_dpf_tf
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_range_bearing_ot_dpf_tf
python -m json.tool experiments/dpf_implementation/reports/outputs/dpf_ot_tf_tfp_lgssm_2026-05-28.json >/dev/null
python -m json.tool experiments/dpf_implementation/reports/outputs/dpf_ot_tf_tfp_range_bearing_2026-05-28.json >/dev/null
rg -n '"pre_import_cuda_visible_devices": "-1"|"model_checksum"|"observation_checksum"|"command"' experiments/dpf_implementation/reports/outputs/dpf_ot_tf_tfp_lgssm_2026-05-28.json experiments/dpf_implementation/reports/outputs/dpf_ot_tf_tfp_range_bearing_2026-05-28.json
rg -n "import numpy|from numpy" experiments/dpf_implementation/tf_tfp
```

## Claude Review Protocol

Use `claude -p --model claude-opus-4-7 --effort max`; loop to acceptance or max
5 iterations.
