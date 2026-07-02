# Reset memo: principal-square-root UKF promotion and historical SVD-UKF demotion

## Date
2026-06-22

## Context
This pass started from a mismatch between the intended UKF derivative policy and
what the repo still implemented/documented in places.  The repository already
contained an experimental principal-square-root UKF lane in the batched
sigma-point code, but the promoted/public scalar UKF path still followed the
historical eigenderivative SVD/eigen branch.  The key blocker for later HMC
work was that the innovation covariance derivative path still ran through
close-eigenvalue-sensitive eigendecomposition derivatives.  The goal of this
pass was therefore to:
- document the strict-SPD principal-square-root derivative contract clearly,
- complete the innovation-covariance derivative branch so it no longer uses
  eigenderivative formulas on the promoted strict-SPD route,
- promote the strict-SPD principal-square-root UKF route publicly,
- demote the old eigenderivative `tf_svd_ukf` lane to historical and
  diagnostic-only status.

## Decision / policy
Future sessions should assume the following unless new evidence and a reviewed
artifact explicitly change it:

1. **The promoted strict-SPD UKF route is the principal-square-root backend.**
   The HMC-facing strict-SPD public routes are:
   - value/filter: `backend="tf_principal_sqrt_ukf"`
   - score: `tf_principal_sqrt_ukf_score(...)`

2. **The historical eigenderivative `tf_svd_ukf` / `tf_svd_ukf_score` path is
   no longer the promoted route.**
   It remains available only for:
   - diagnostic comparison,
   - regression baselines,
   - spectral-gap telemetry,
   - bounded failure-mode debugging.

3. **On the promoted strict-SPD principal-square-root branch, the innovation
   covariance derivative must not be expressed through eigendecomposition
   derivatives.**
   The intended derivative contract is solve/Sylvester based for both:
   - placement covariance square root,
   - innovation covariance square root.

4. **This promotion is strict-SPD only.**
   Do not silently extend the principal-square-root promotion claim to:
   - structural-null branches,
   - floor-active branches,
   - semidefinite innovation covariances,
   - non-SPD fallback behavior.
   Those remain separate work.

5. **Do not reopen the question of whether the historical eigenderivative UKF
   path should remain promoted.**
   That question is settled by this pass: it is historical/diagnostic-only for
   the current scope.

## What changed
- File: `docs/chapters/ch18_svd_sigma_point.tex`
  - Expanded the principal-square-root section so it now documents both:
    - strict-SPD placement-factor derivatives,
    - strict-SPD innovation covariance square-root derivatives.
  - Added explicit solve/Sylvester math and stated that the promoted branch must
    not reintroduce eigendecomposition-derivative formulas on innovation
    covariance derivatives.
  - Marked the old `tf_svd_ukf` branch as historical and the
    `tf_principal_sqrt_ukf` branch as the promoted strict-SPD route.

- File: `docs/chapters/ch20_filter_choice.tex`
  - Reframed the old SVD/eigenderivative sigma-point lane as historical and
    diagnostic-only once the strict-SPD principal-square-root route exists.

- File: `docs/chapters/ch28_nonlinear_ssm_validation.tex`
  - Updated validation language so the affine and nonlinear fixture discussion
    explicitly distinguishes:
    - historical diagnostic SVD-UKF,
    - promoted strict-SPD principal-square-root UKF.

- File: `bayesfilter/linear/svd_factor_tf.py`
  - Added shared strict-SPD principal-square-root helper logic:
    - `PrincipalSqrtFirstDerivativeDiagnostics`
    - `principal_sqrt_frechet_derivative_from_eigh(...)`
    - `strict_spd_principal_sqrt_first_derivatives(...)`

- File: `bayesfilter/linear/__init__.py`
  - Exported the shared principal-square-root helper symbols.

- File: `bayesfilter/nonlinear/experimental_batched_svd_sigma_point_tf.py`
  - Completed the experimental batched `tf_principal_sqrt_ukf` route so both:
    - placement,
    - innovation covariance derivatives
    use principal-square-root derivative handling.
  - Added innovation-side diagnostics including Sylvester residual tracking.

- File: `bayesfilter/nonlinear/sigma_points_tf.py`
  - Added public scalar value/filter support for
    `backend="tf_principal_sqrt_ukf"`.
  - Added backend role labels that classify:
    - `tf_principal_sqrt_ukf` as promoted strict-SPD,
    - `tf_svd_ukf` as historical diagnostic-only.
  - Updated diagnostic metadata so the historical lane is described accordingly.

- File: `bayesfilter/nonlinear/svd_sigma_point_derivatives_tf.py`
  - Added public scalar score route `tf_principal_sqrt_ukf_score(...)`.
  - Added scalar strict-SPD principal-square-root placement and innovation
    derivative handling.
  - Marked `tf_svd_ukf_score(...)` as the historical eigenderivative path kept
    for diagnostics and regression comparison.

- File: `bayesfilter/nonlinear/__init__.py`
- File: `bayesfilter/__init__.py`
  - Exported the new public scalar score symbol
    `tf_principal_sqrt_ukf_score`.

- File: `tests/test_experimental_batched_svd_sigma_point_tf.py`
  - Added/updated repeated-positive placement and innovation-spectrum evidence
    for the experimental principal-square-root route.

- File: `tests/test_nonlinear_sigma_point_scores_tf.py`
  - Added targeted scalar principal-square-root score checks and public surface
    checks.

- File: `tests/test_nonlinear_sigma_point_values_tf.py`
  - Added targeted scalar principal-square-root value checks and benign-fixture
    parity checks.

- File: `tests/test_v1_public_api.py`
- File: `tests/highdim/test_public_api_highdim.py`
  - Updated public symbol expectations to include
    `tf_principal_sqrt_ukf_score`.

- File: `docs/plans/bayesfilter-principal-sqrt-ukf-strict-spd-promotion-result-2026-06-22.md`
  - Recorded the promotion result and the historical/demoted role of
    `tf_svd_ukf`.

- File: `docs/plans/bayesfilter-batched-filtering-phase-6-default-readiness-result-2026-06-14.md`
  - Reframed the older batched SVD-UKF production-candidate note as a historical
    artifact for that specific 2026-06 program, not the current promoted UKF
    route.

## Bugs / blockers resolved
- Symptom:
  - The intended principal-square-root UKF route existed only partially: the
    innovation covariance derivative path still went through eigendecomposition
    derivatives in both concept and implementation.
- Root cause:
  - The earlier square-root lane fixed placement-factor derivatives but did not
    fully switch the innovation derivative branch to a solve/Sylvester contract.
- Resolution:
  - Implemented strict-SPD principal-square-root innovation derivative handling
    in the experimental and scalar promoted paths.

- Symptom:
  - Repo language still allowed the impression that `tf_svd_ukf` remained the
    current promoted/default UKF route.
- Root cause:
  - Historical result artifacts and some narrative docs had not been updated
    after the principal-square-root promotion work.
- Resolution:
  - Updated code/doc status signals so `tf_svd_ukf` is now explicitly historical
    and diagnostic-only, while `tf_principal_sqrt_ukf` is the promoted strict-SPD
    route.

## Verification already run
```bash
CUDA_VISIBLE_DEVICES=-1 pytest -q tests/test_experimental_batched_svd_sigma_point_tf.py -k "principal_sqrt or repeated_positive"
```

```bash
CUDA_VISIBLE_DEVICES=-1 pytest -q tests/test_nonlinear_sigma_point_values_tf.py tests/test_nonlinear_sigma_point_scores_tf.py tests/test_v1_public_api.py tests/highdim/test_public_api_highdim.py -k "principal_sqrt or public_api or svd_sigma_point_analytic_score_matches_finite_difference"
```

Observed:
- Experimental principal-square-root subset: `4 passed, 13 deselected`
- Scalar/public principal-square-root subset: `15 passed, 21 deselected`
- The repeated-positive innovation-spectrum fixture now passes on the promoted
  principal-square-root route while the historical eigenderivative SVD-UKF path
  still blocks on weak spectral-gap fixtures.
- Public API symbol checks passed after adding `tf_principal_sqrt_ukf_score`.

## Current policy
- Use `tf_principal_sqrt_ukf` / `tf_principal_sqrt_ukf_score` for strict-SPD
  principal-square-root UKF work.
- Treat `tf_svd_ukf` / `tf_svd_ukf_score` as historical diagnostic-only
  comparators.
- Keep future HMC-facing work scoped to the promoted strict-SPD branch unless a
  new reviewed artifact extends the supported branch structure.
- Do not interpret the current work as proving anything about structural-null,
  floor-active, or semidefinite principal-square-root behavior.

## Known limitations / cautions
- The promoted branch is strict-SPD only.
- The batched experimental interface still has a separate collection/import issue
  in this environment because Python may resolve a site-packages `tests` package
  before the repo `tests/` directory; this did not block the directly relevant
  kernel checks.
- The repo-wide default-policy question outside the strict-SPD scope is still a
  product/policy question, not something resolved by the current targeted
  evidence alone.
- The working tree is dirty; future sessions should re-check current file state
  before assuming no other parallel work has modified these files further.

## Suggested next steps
1. Start the fixed-SGQF testing lane as a separate task/agent.
2. Before any SGQF reruns that will guide research direction, create a fresh
   experiment plan under `docs/plans/` for the SGQF testing question.
3. Treat this reset memo and the 2026-06-22 principal-square-root promotion
   result note as the context handoff for any future UKF/HMC-related work.
