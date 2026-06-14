# P2 Plan: Range-Bearing Fixture And UKF Reference

Date: 2026-05-28

## Evidence Contract

Question: can the lane define a deterministic TF/TFP range-bearing Gaussian
fixture and UKF approximate reference?

Primary criterion: finite fixture tensors, deterministic checksums, finite UKF
means/covariances/predicted observations, and explicit UKF approximate-reference
caveat.

Veto diagnostics: non-finite UKF values, invalid covariance after
stabilization, missing angle wrapping, missing caveat, or NumPy import in
`tf_tfp`.

What must not be concluded: UKF is not ground truth and cannot validate
posterior correctness, HMC, production use, or monograph claims.

## Inputs

- `experiments/dpf_implementation/fixtures/range_bearing.py` as prototype
  context only.
- P0 result.

## Outputs

- `experiments/dpf_implementation/tf_tfp/fixtures/range_bearing_tf.py`
- `experiments/dpf_implementation/tf_tfp/references/ukf_tf.py`
- `docs/plans/bayesfilter-dpf-ot-tf-tfp-p2-range-bearing-ukf-result-2026-05-28.md`

## Allowed Write Set

- `experiments/dpf_implementation/tf_tfp/fixtures/`
- `experiments/dpf_implementation/tf_tfp/references/`
- `docs/plans/bayesfilter-dpf-ot-tf-tfp-p2-*-2026-05-28.md`

## Forbidden Write Set

Production `bayesfilter/`, tests, monograph chapters, vendored code, highdim
lane, and existing NumPy prototype modules.

## Skeptical Audit Checklist

Check stale context, wrong backend, NumPy drift, proxy overclaim, missing stop
conditions, hidden production drift, monograph drift, vendored contamination,
highdim contamination, and artifact fitness.

## Stop Conditions

Stop if UKF covariance cannot be stabilized, angle residuals cannot be wrapped,
or the artifact would call UKF ground truth.

## Verification Commands

```bash
python -m py_compile experiments/dpf_implementation/tf_tfp/fixtures/range_bearing_tf.py experiments/dpf_implementation/tf_tfp/references/ukf_tf.py
rg -n "import numpy|from numpy" experiments/dpf_implementation/tf_tfp
```

## Claude Review Protocol

Use `claude -p --model claude-opus-4-7 --effort max`; loop to acceptance or max
5 iterations.
