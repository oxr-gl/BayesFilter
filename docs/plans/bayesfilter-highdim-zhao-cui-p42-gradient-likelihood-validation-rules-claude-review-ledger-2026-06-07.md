# P42 Claude Review Ledger: Gradient and Likelihood Validation Rules

metadata_date: 2026-06-07
phase: P42-governance

## Review Iteration 1

status: `BLOCKED_P42_RULES_GOVERNANCE`

Reviewer summary:
- Split across-dataset data-law variability from within-dataset evaluator
  variability.
- Make score-covariance/whitening operational in high dimension, including
  shrinkage, diagonal/block options, and ridge rules.
- Tighten finite-difference governance: finite differences are corroborative,
  require minimum ladder sizes, shifted-ladder repeatability, stable-window
  criteria, regression acceptance criteria, and derivative uncertainty.
- Demote autodiff unless branch/floor/rank/solver/quadrature invariance is
  proven over the whole perturbation neighborhood and refinement checks pass.
- Separate exact-target correctness, statistical relevance, and approximate
  surrogate-HMC usefulness as distinct claim classes.
- Add horizon-scaling rules and error-versus-horizon checks.
- Strengthen near-stationary-point handling so relative norm error is not the
  sole pass metric.

Response:
- Patched the rules document to address these blockers before iteration 2.

## Review Iteration 2

status: `BLOCKED_P42_RULES_GOVERNANCE`

Reviewer summary:
- Evaluator variability was separated for likelihood values but not for
  gradients.
- High-dimensional score-scale rules still used vague triggers such as
  "comfortably larger" and "acceptable threshold".
- Near-stationary handling used the scale-dependent threshold `||g_ref|| < 1`
  without tying it to the parameterization or score scale.

Response:
- Patched repeated same-dataset score-evaluator variability rules.
- Replaced vague score-covariance triggers with executable replication and
  condition-number thresholds.
- Replaced the near-stationary rule with a score-scale-relative trigger.

## Review Iteration 3

status: `PASS_P42_RULES_GOVERNANCE`

Reviewer summary:
- The repeated same-dataset value/score evaluator-variability rules now address
  data-law versus evaluator-noise separation.
- Full-covariance score scaling now has explicit admissibility conditions and
  mandatory fallbacks.
- The near-stationary rule is now score-scale-aware rather than a raw Euclidean
  cutoff.

Residual cautions:
- Near-stationary fixtures still require predeclared absolute and directional
  tolerances before seeing results.
- Tier 3 HMC dynamics rules remain threshold-light; actual promotion plans
  must predeclare unacceptable Hamiltonian error, reversibility error, and
  acceptance degradation thresholds before making go/no-go claims.

Response:
- Converged after review iteration 3, below the maximum of five iterations.
