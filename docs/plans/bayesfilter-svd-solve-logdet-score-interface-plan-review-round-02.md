Findings first:

- The round-1 blockers are mostly resolved in the revised plan. It now correctly separates invariant solve/logdet score algebra from spectral-factor derivatives, cites the right baselines, pins the public API to `tf_svd_linear_gaussian_score_hessian`, sets `hessian=None` with `metadata.differentiability_status="analytic_score_only"`, blocks active floors for this phase, demotes `min_eigen_gap` to telemetry only, gives concrete verification commands, and bounds the write set.
- The mathematical safety story is substantially sound. `ch09`'s solve-form score uses only `S^{-1}`, `\dot S`, `v`, and `w`, while `ch12` and `ch18` place the simple-spectrum hazard specifically on factor/eigenvector derivatives through gap denominators. The revised plan's repeated-eigenvalue allowance is limited to invariant score evaluation.
- The code-surface alignment is mostly correct. The existing SVD TF path is value-only and reports blocked derivative semantics. The QR TF derivative backend is the live derivative comparator and has score/Hessian plus private score-only precedent. `TFFilterDerivativeResult` accepts `hessian=None`, and `TFRegularizationDiagnostics` supports `derivative_target="blocked"`.
- One caution, not a blocker: `tests/test_svd_linear_gaussian_score_tf.py` does not exist yet and is expected to be newly added by implementation.
- No false Cholesky-derivative baseline claim remains.
- No false public-API mismatch remains; additive exports are properly scoped.
- Small caution, not a blocker: `analytic_score_only` is new but allowed because `FilterRunMetadata.differentiability_status` is an unconstrained string field.

VERDICT: PROCEED
