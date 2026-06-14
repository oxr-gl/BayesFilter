- The math split is correct: invariant solve/logdet score in ch09 has no eigen-gap denominator, while ch12/ch18 factor derivatives have simple-spectrum denominators.
- Baseline wording needs tightening: use TF QR derivative backend and NumPy solve derivative backend; TF Cholesky is value-only.
- API shape needs alignment with local conventions: existing public linear TF derivative surface is score_hessian; score-only QR helper is private pending API freeze.
- Floor semantics should be pinned: active floor blocked for this phase unless a separate floored-law reference is created.
- Repeated-eigenvalue tests are justified and min_eigen_gap must be telemetry only for solve/logdet score.
- Diagnostics/result containers can support hessian=None and extra telemetry.
- Verification commands need exact test selectors and compile coverage for touched SVD derivative module.
- Stop conditions and nonclaims are good.
VERDICT: REQUEST_CHANGES
