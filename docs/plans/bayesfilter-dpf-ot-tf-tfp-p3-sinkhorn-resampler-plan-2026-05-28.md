# P3 Plan: TensorFlow Sinkhorn Resampler

Date: 2026-05-28

## Evidence Contract

Question: can the lane implement finite-budget entropic OT/Sinkhorn relaxed
resampling in TensorFlow without NumPy implementation imports?

Primary criterion: finite coupling, nonnegative mass, row/column marginal
residuals within tolerance envelope, finite barycentric relaxed particles, and
declared epsilon, iteration budget, stabilization mode, cost function, and target
marginal.

Veto diagnostics: non-finite coupling, negative mass beyond tolerance, residual
failure, missing diagnostics, or NumPy import in `tf_tfp`.

What must not be concluded: no exact categorical resampling, no exact
unregularized OT, no learned/neural OT promotion, no production readiness.

## Inputs

- P0 result.
- Prior NumPy prototype `experiments/dpf_implementation/resampling/sinkhorn.py`
  as context only.

## Outputs

- `experiments/dpf_implementation/tf_tfp/resampling/sinkhorn_tf.py`
- `docs/plans/bayesfilter-dpf-ot-tf-tfp-p3-sinkhorn-resampler-result-2026-05-28.md`

## Allowed Write Set

- `experiments/dpf_implementation/tf_tfp/resampling/`
- `docs/plans/bayesfilter-dpf-ot-tf-tfp-p3-*-2026-05-28.md`

## Forbidden Write Set

Production `bayesfilter/`, tests, monograph chapters, vendored code, highdim
lane, and existing NumPy prototype modules.

## Skeptical Audit Checklist

Check stale context, wrong backend, NumPy drift, proxy overclaim, missing stop
conditions, hidden production drift, monograph drift, vendored contamination,
highdim contamination, and artifact fitness.

## Stop Conditions

Stop if TensorFlow Sinkhorn cannot emit finite diagnostics or if it needs NumPy
arrays for algorithmic computation.

## Verification Commands

```bash
python -m py_compile experiments/dpf_implementation/tf_tfp/resampling/sinkhorn_tf.py
rg -n "import numpy|from numpy" experiments/dpf_implementation/tf_tfp
```

## Claude Review Protocol

Use `claude -p --model claude-opus-4-7 --effort max`; loop to acceptance or max
5 iterations.
