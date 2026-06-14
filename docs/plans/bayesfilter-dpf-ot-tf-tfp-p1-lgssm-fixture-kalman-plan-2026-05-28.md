# P1 Plan: LGSSM Fixture And Kalman Reference

Date: 2026-05-28

## Evidence Contract

Question: can the lane define a deterministic TF/TFP LGSSM fixture and exact
Kalman reference without NumPy implementation imports?

Primary criterion: finite fixture tensors, deterministic checksums, finite
Kalman filtered means/covariances, and finite log likelihood.

Veto diagnostics: non-finite tensors, invalid covariance, missing checksum, or
NumPy import in `tf_tfp`.

What must not be concluded: no nonlinear validation, OT resampling validation,
production readiness, posterior correctness, HMC readiness, or monograph claim.

## Inputs

- `experiments/dpf_implementation/fixtures/lgssm.py` as prototype context only.
- P0 result.

## Outputs

- `experiments/dpf_implementation/tf_tfp/fixtures/lgssm_tf.py`
- `experiments/dpf_implementation/tf_tfp/references/kalman_lgssm_tf.py`
- `docs/plans/bayesfilter-dpf-ot-tf-tfp-p1-lgssm-fixture-kalman-result-2026-05-28.md`

## Allowed Write Set

- `experiments/dpf_implementation/tf_tfp/fixtures/`
- `experiments/dpf_implementation/tf_tfp/references/`
- `docs/plans/bayesfilter-dpf-ot-tf-tfp-p1-*-2026-05-28.md`

## Forbidden Write Set

Production `bayesfilter/`, tests, monograph chapters, vendored code, highdim
lane, and existing NumPy prototype modules.

## Skeptical Audit Checklist

Check stale context, wrong backend, NumPy drift, proxy overclaim, missing stop
conditions, hidden production drift, monograph drift, vendored contamination,
highdim contamination, and artifact fitness.

## Stop Conditions

Stop if Kalman reference cannot be implemented in TF/TFP, if deterministic
fixture generation is not reproducible, or if covariance updates are non-finite.

## Verification Commands

```bash
python -m py_compile experiments/dpf_implementation/tf_tfp/fixtures/lgssm_tf.py experiments/dpf_implementation/tf_tfp/references/kalman_lgssm_tf.py
rg -n "import numpy|from numpy" experiments/dpf_implementation/tf_tfp
```

## Claude Review Protocol

Use `claude -p --model claude-opus-4-7 --effort max`; loop to acceptance or max
5 iterations.
