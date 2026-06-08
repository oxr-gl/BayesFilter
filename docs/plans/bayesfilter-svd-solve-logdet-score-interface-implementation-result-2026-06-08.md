# BayesFilter SVD solve/logdet score interface implementation result

Date: 2026-06-08

Status: focused local verification passed after Claude-requested blocked-branch and public-wrapper boundary fixes; Claude implementation review round 4 passed.

## Summary

- Added `bayesfilter/linear/kalman_svd_derivatives_tf.py` with dense-only `tf_svd_linear_gaussian_score_hessian`.
- The implementation evaluates the invariant Kalman solve/logdet score and does not differentiate eigenvectors or spectral factors.
- Repeated positive innovation eigenvalues are allowed; `min_eigen_gap` is diagnostics telemetry only.
- Active spectral flooring raises `blocked_active_floor` and does not claim an implemented regularized-law derivative.
- After Claude implementation review round 2, the active-floor exception now carries
  a blocked `TFFilterDerivativeResult` with
  `diagnostics.regularization.derivative_target == "blocked"` and a NaN score.
- After Claude implementation review round 3, the public Python wrapper now
  rejects non-eager graph-wrapped use with a `blocked_non_eager` message rather
  than returning through a TensorFlow assertion path. The compiled numerical
  tensor kernel remains internal; the public result-container API is
  Python/eager orchestration.
- Added additive public exports and focused regression tests.

## Nonclaims

- No Hessian implementation.
- No nonlinear sigma-point derivative promotion.
- No spectral-factor derivative support at repeated eigenvalues.
- No HMC or GPU readiness claim.

## Verification

Execution context: BayesFilter repo root, CPU-only with
`CUDA_VISIBLE_DEVICES=-1`, Python bytecode redirected to
`/tmp/bayesfilter_svd_score_pycache`.

Compile command:

```bash
env PYTHONPYCACHEPREFIX=/tmp/bayesfilter_svd_score_pycache CUDA_VISIBLE_DEVICES=-1 /home/ubuntu/anaconda3/envs/tfgpu/bin/python -m py_compile \
  bayesfilter/linear/kalman_svd_derivatives_tf.py \
  bayesfilter/linear/__init__.py \
  bayesfilter/__init__.py \
  tests/test_svd_linear_gaussian_score_tf.py \
  tests/test_v1_public_api.py
```

Result: passed with no output.

Focused pytest command:

```bash
env PYTHONPYCACHEPREFIX=/tmp/bayesfilter_svd_score_pycache CUDA_VISIBLE_DEVICES=-1 /home/ubuntu/anaconda3/envs/tfgpu/bin/python -m pytest -q \
  tests/test_svd_linear_gaussian_score_tf.py \
  tests/test_v1_public_api.py \
  tests/test_linear_kalman_qr_derivatives_tf.py::test_qr_score_hessian_matches_value_and_solve_reference \
  tests/test_linear_kalman_svd_tf.py
```

Initial result: `19 passed` in `55.03s`. Warnings were TensorFlow Probability
and TensorFlow/gast deprecation warnings only.

After the eager blocked-branch fix, the same compile command passed again with
no output. The same focused pytest command passed again with `19 passed` in
`44.86s`; warnings remained TensorFlow Probability and TensorFlow/gast
deprecation warnings only.

After the non-eager public-wrapper boundary fix, the same compile command
passed again with no output. The same focused pytest command passed with
`20 passed` in `46.07s`; warnings remained TensorFlow Probability and
TensorFlow/gast deprecation warnings only.

## Review status

Claude implementation review round 2 requested one blocker fix: expose
`derivative_target="blocked"` on the active-floor blocked artifact rather than
only raising a bare exception. Claude implementation review round 3 requested
clarifying the non-eager public-wrapper behavior. The public wrapper now blocks
graph-wrapped use explicitly. Claude implementation review round 4 reported no
remaining blocking findings and returned `VERDICT: PASS`.
