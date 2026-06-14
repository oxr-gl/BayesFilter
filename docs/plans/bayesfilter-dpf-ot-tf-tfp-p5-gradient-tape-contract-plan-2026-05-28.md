# P5 Plan: GradientTape Same-Scalar Contract

Date: 2026-05-28

## Evidence Contract

Question: can the TF/TFP OT-DPF path expose a same-scalar autodiff gradient with
`tf.GradientTape` and compare it to a finite-difference reference?

Primary criterion: named scalar, fixed observations, common random numbers,
finite `tf.GradientTape` gradient, finite-difference reference for the same
scalar, and agreement within a smoke tolerance.

Veto diagnostics: value and gradient target different scalars, random numbers
change across finite differences, non-finite gradient, or NumPy import in
`tf_tfp`.

What must not be concluded: finite gradient is not posterior correctness, HMC
readiness, production readiness, or likelihood-score validity.

## Inputs

- P1 LGSSM fixture.
- P3 TensorFlow Sinkhorn resampler.
- P4 OT-DPF value path.

## Outputs

- `experiments/dpf_implementation/tf_tfp/runners/run_gradient_checks_tf.py`
- `docs/plans/bayesfilter-dpf-ot-tf-tfp-p5-gradient-tape-contract-result-2026-05-28.md`

## Allowed Write Set

- `experiments/dpf_implementation/tf_tfp/runners/`
- `experiments/dpf_implementation/tf_tfp/filters/`
- `docs/plans/bayesfilter-dpf-ot-tf-tfp-p5-*-2026-05-28.md`

## Forbidden Write Set

Production `bayesfilter/`, tests, monograph chapters, vendored code, highdim
lane, and existing NumPy prototype modules.

## Skeptical Audit Checklist

Check stale context, wrong backend, NumPy drift, proxy overclaim, missing stop
conditions, hidden production drift, monograph drift, vendored contamination,
highdim contamination, and artifact fitness.

## Stop Conditions

Stop if `tf.GradientTape` cannot see the scalar, finite differences use a
different scalar, or common random numbers cannot be enforced.

## Verification Commands

```bash
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_gradient_checks_tf
rg -n "import numpy|from numpy" experiments/dpf_implementation/tf_tfp
```

## Claude Review Protocol

Use `claude -p --model claude-opus-4-7 --effort max`; loop to acceptance or max
5 iterations.
