# BayesFilter SVD solve/logdet score interface plan

Date: 2026-06-08

Owning root: `/home/ubuntu/python/BayesFilter`

Status: `PLAN_REVISED_AFTER_CLAUDE_REVIEW_R1`

## Question

Can BayesFilter add a TensorFlow linear-Gaussian score interface that uses the invariant solve/logdet score algebra from `docs/chapters/ch09_kalman_score.tex` while allowing repeated positive innovation eigenvalues, without weakening the existing simple-spectrum contract for differentiated SVD/eigen factors?

## Skeptical plan audit

Status: passed for revised planning only.

- Wrong baseline risk: the derivative baselines are the NumPy solve-form analytic score in `bayesfilter/linear/kalman_derivatives_numpy.py` and the existing TF QR derivative backend in `bayesfilter/linear/kalman_qr_derivatives_tf.py`. The TF Cholesky path in `bayesfilter/linear/kalman_tf.py` is value-only and may be used only as a value-law comparator.
- Proxy-metric risk: compile success, finite outputs, and telemetry are engineering checks only. Promotion requires parity of the scalar log likelihood and score against the NumPy solve reference, plus QR derivative parity on a shared unfloored law where applicable.
- Hidden assumption: the score contract is for the implemented innovation law. In this phase, any active spectral floor makes the derivative target `blocked`; the implementation must not claim a floored regularized-law derivative unless a separate reference artifact is introduced by a later reviewed plan.
- Repeated-spectrum risk: simple-spectrum assumptions from `ch12`/`ch18` apply to factor derivatives, not automatically to invariant solve/logdet score terms. The implementation must avoid eigenvector derivative formulas and treat `min_eigen_gap` as telemetry only.
- Artifact adequacy: the result must preserve branch labeling, floor behavior, parity evidence, and nonclaims. A passing smoke test alone would not answer the interface question.
- Stop-condition adequacy: implementation must stop if parity only holds on simple-spectrum fixtures, if floor handling is ambiguous, if the proposed interface leaks a false Hessian contract, or if any code path differentiates eigenvectors or spectral bases.

Reason to proceed: the written math already distinguishes solve-form invariant score terms from factor-derivative formulas, the repo has value-only spectral diagnostics, and the repo has both NumPy solve-form and TF QR derivative baselines for unfloored dense LGSSMs.

## Evidence contract

| Field | Contract |
| --- | --- |
| Question | Can a TF SVD/eigh linear-Gaussian score backend implement the invariant solve/logdet score without requiring simple innovation spectrum? |
| Baseline | Primary derivative baseline: `bayesfilter/linear/kalman_derivatives_numpy.py` solve-form analytic score. Secondary derivative comparator where the law matches: `bayesfilter/linear/kalman_qr_derivatives_tf.py`. Value-law comparators: existing SVD/eigh value path in `bayesfilter/linear/kalman_svd_tf.py` and value-only Cholesky/QR paths where applicable. |
| Primary criterion | New TF derivative backend returns `TFFilterDerivativeResult` with finite log likelihood and score, `hessian=None`, `metadata.differentiability_status="analytic_score_only"`, and score/log-likelihood parity against the NumPy solve reference on targeted dense LGSSM fixtures, including repeated and nearly repeated positive innovation spectra. |
| Promotion vetoes | Any need for eigenvector-derivative denominators; any active floor that does not block derivatives with `derivative_target="blocked"`; parity failure versus NumPy solve reference; mismatch between returned log likelihood and implemented TF SVD value law on unfloored cases; exposing Hessian as supported; documentation claiming spectral-factor differentiability is established. |
| Explanatory only | `min_innovation_eigenvalue`, innovation condition estimate, floor count, PSD projection residual, and `min_eigen_gap` telemetry. In this interface, `min_eigen_gap` is never a veto. |
| Not concluded | No Hessian implementation; no proof of factor-derivative correctness for repeated eigenvalues; no nonlinear sigma-point derivative claim; no HMC convergence claim; no GPU-readiness claim; no default-policy promotion beyond this specific linear score-only interface. |
| Artifact | This plan, the implementation diff within the allowed write set, focused tests, and a result/review note written after implementation review. |

## Math distinction: factor derivative vs invariant solve/logdet score

1. `docs/chapters/ch09_kalman_score.tex` equation `bf-solve-score` expresses the first derivative of the Gaussian prediction-error contribution using `S^{-1}`, `dS`, and `w` where `S w = v`. This formula has no explicit eigen-gap denominator.
2. `docs/chapters/ch12_factor_derivatives.tex` and `docs/chapters/ch18_svd_sigma_point.tex` require simple spectrum for SVD/eigen factor derivatives because differentiated eigenvectors or spectral bases introduce denominators like `lambda_a - lambda_b`.
3. Therefore the new scope is the invariant score of the unfloored implemented covariance law, not a differentiated spectral factor contract. The backend may use eigensolve/logdet primitives to evaluate `S^{-1}v`, traces, and log determinants, but it must not expose or rely on eigenvector derivative formulas.
4. If flooring or PSD repair changes the implemented covariance, this phase blocks derivative output rather than claiming either the pre-regularized law or a floored regularized-law derivative.

## Proposed interface name and scope

Public function name for this phase:

- `tf_svd_linear_gaussian_score_hessian`

This name follows the existing public linear TF derivative naming convention even though this phase is score-only. The return contract must state:

- returns `TFFilterDerivativeResult`;
- `hessian=None` always in this phase;
- `metadata.differentiability_status="analytic_score_only"`;
- dense linear Gaussian state-space models only;
- TensorFlow backend using spectral solve/logdet primitives aligned with the SVD value path;
- no masked derivative scope in this phase;
- no claim of differentiated SVD/eigen factors, only invariant score evaluation for the unfloored implemented law;
- if any active floor occurs, return or raise through an explicit blocked derivative branch rather than returning a misleading score.

A private low-level helper may use a clearer internal name such as `_tf_svd_solve_logdet_kalman_score`, but the public exported surface for this plan is `tf_svd_linear_gaussian_score_hessian`.

## Proposed implementation shape

- Add the preferred new module `bayesfilter/linear/kalman_svd_derivatives_tf.py` for the score interface. Touch `bayesfilter/linear/kalman_svd_tf.py` only for small shared helpers if review/implementation shows it is necessary.
- Reuse the same dense innovation covariance construction and spectral solve/logdet primitives as the SVD/eigh value backend.
- Compute the first derivative using the invariant solve-form score algebra from `ch09`, not autodiff through `tf.linalg.eigh` and not eigenvector derivative formulas.
- Reuse `TFFilterDiagnostics` / `TFRegularizationDiagnostics` and return `TFFilterDerivativeResult` from `bayesfilter/results_tf.py`.
- Add a derivative branch label such as `eigensolve_logdet_score_repeated_eigenvalues_allowed`.
- Emit diagnostics for `min_innovation_eigenvalue`, innovation condition estimate, floor count, PSD projection residual, `min_eigen_gap` telemetry, derivative branch label, and derivative target.
- Pin floor semantics for this phase: if `floor_count > 0`, the derivative target is `blocked`, no score is promoted for that path, and tests must verify there is no `implemented_regularized_law` derivative claim under active flooring.
- For unfloored positive spectra, set the derivative target to the unfloored implemented law and record that repeated eigenvalues are allowed for the solve/logdet score.

## Tests

Required focused tests:

1. Repeated-spectrum invariant score:
   - construct a dense fixture with `S = alpha I` at one or more steps;
   - confirm finite TF score/log likelihood and parity with the NumPy solve reference;
   - confirm telemetry reports repeated or zero eigen-gap without treating it as failure.
2. Nearly repeated positive eigenvalues:
   - use a dense fixture with clustered positive eigenvalues;
   - confirm finite outputs and NumPy parity within declared tolerance;
   - record `min_eigen_gap` telemetry as explanatory only.
3. Active floor branch:
   - verify explicit derivative blocking with `derivative_target="blocked"` and no false `implemented_regularized_law` derivative claim when a floor is active.
4. Existing-backend parity where applicable:
   - compare against the TF QR derivative backend on fixtures where both target the same unfloored dense law;
   - compare log likelihood against the SVD value backend, and against Cholesky/QR value-only paths only as value-law comparators.
5. Result-container/diagnostic contract:
   - assert returned object is `TFFilterDerivativeResult`, `hessian is None`, `metadata.differentiability_status == "analytic_score_only"`, branch label is nonempty, and regularization diagnostics preserve the declared derivative target.
6. Public API/export coverage:
   - if exported, add `tf_svd_linear_gaussian_score_hessian` to `bayesfilter/linear/__init__.py`, top-level `bayesfilter/__init__.py`, and `tests/test_v1_public_api.py`.

## Documentation updates

Update only the minimum docs needed to align the contract:

- `docs/chapters/ch09_kalman_score.tex`: clarify that the solve/logdet score is invariant and does not itself require simple innovation spectrum, while the derivative target must still match the implemented covariance law.
- `docs/chapters/ch12_factor_derivatives.tex`: reinforce that simple-spectrum restrictions belong to factor derivatives, not automatically to invariant solve/logdet score evaluation.
- `docs/chapters/ch18_svd_sigma_point.tex` or a validation chapter: add the implementation note that repeated-spectrum allowance here is limited to linear invariant score evaluation and does not establish nonlinear sigma-point spectral derivative safety.

## Nonclaims

- not a Hessian implementation;
- not a proof that spectral factor derivatives are valid at repeated eigenvalues;
- not a nonlinear sigma-point derivative promotion;
- not an HMC readiness or convergence result;
- not a GPU/performance optimization plan;
- not a default-policy change outside this specific linear score-only interface;
- not a floored regularized-law derivative implementation.

## Exact allowed write set

Only these paths may be changed during implementation unless Claude review approves a narrower equivalent set:

- `bayesfilter/linear/kalman_svd_derivatives_tf.py` as the preferred new module;
- `bayesfilter/linear/kalman_svd_tf.py` only for small shared helper reuse if needed;
- `bayesfilter/linear/__init__.py` for additive export;
- `bayesfilter/__init__.py` only if needed for additive top-level export parity;
- `bayesfilter/diagnostics.py` only if a strictly additive diagnostic target/extra contract is required;
- `bayesfilter/results_tf.py` only if a strictly additive result contract adjustment is required;
- `tests/test_svd_linear_gaussian_score_tf.py` as the preferred focused test file;
- `tests/test_v1_public_api.py` only for additive public export coverage;
- the implementation result/review note under `docs/plans/`;
- the minimal doc chapter updates among `ch09`, `ch12`, `ch18`, or a validation chapter.

No other code, docs, commits, or pushes are authorized by this plan.

## Exact verification commands

CPU-only unless Claude review explicitly authorizes a trusted GPU check. Set GPU hidden before TensorFlow import.

```bash
PYTHONPYCACHEPREFIX=/tmp/bayesfilter_svd_score_pycache CUDA_VISIBLE_DEVICES=-1 /home/ubuntu/anaconda3/envs/tfgpu/bin/python -m py_compile \
  bayesfilter/linear/kalman_svd_derivatives_tf.py \
  bayesfilter/linear/kalman_svd_tf.py \
  bayesfilter/linear/__init__.py \
  bayesfilter/__init__.py \
  bayesfilter/diagnostics.py \
  bayesfilter/results_tf.py \
  tests/test_svd_linear_gaussian_score_tf.py \
  tests/test_v1_public_api.py
```

```bash
PYTHONPYCACHEPREFIX=/tmp/bayesfilter_svd_score_pycache CUDA_VISIBLE_DEVICES=-1 /home/ubuntu/anaconda3/envs/tfgpu/bin/python -m pytest -q \
  tests/test_svd_linear_gaussian_score_tf.py \
  tests/test_v1_public_api.py \
  tests/test_linear_kalman_qr_derivatives_tf.py::test_qr_score_hessian_matches_value_and_solve_reference \
  tests/test_linear_kalman_svd_tf.py
```

If the implementation does not touch `bayesfilter/diagnostics.py`, `bayesfilter/results_tf.py`, or top-level exports, they may remain in the compile command as unchanged contract coverage.

## Stop conditions

Stop and return to review before or during implementation if any of the following occurs:

- the intended TF score requires differentiating eigenvectors or spectral bases;
- repeated-eigenvalue fixtures fail except by imposing a simple-spectrum restriction;
- floor-active derivative semantics cannot be implemented as explicit blocking;
- NumPy solve parity fails on the implemented unfloored law;
- the interface needs real Hessian support or broader API changes to appear coherent;
- the write set must expand materially beyond the allowed paths;
- implementation attempts to promote `min_eigen_gap` from telemetry to veto for the solve/logdet score path.

## Review and execution control

- This revised plan must receive Claude `VERDICT: PROCEED` before implementation begins.
- After implementation, run a Claude implementation-review loop with a maximum of 5 review/fix iterations.
- Do not commit or push.
