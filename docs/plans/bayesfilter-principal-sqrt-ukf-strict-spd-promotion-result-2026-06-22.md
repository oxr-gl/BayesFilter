# Experiment result: principal-square-root UKF strict-SPD promotion refresh

## Plan reference
- `/.claude/plans/shimmying-churning-sky.md`

## Command actually run
```bash
CUDA_VISIBLE_DEVICES=-1 pytest -q tests/test_experimental_batched_svd_sigma_point_tf.py -k "principal_sqrt or repeated_positive"
```

```bash
CUDA_VISIBLE_DEVICES=-1 pytest -q tests/test_nonlinear_sigma_point_values_tf.py tests/test_nonlinear_sigma_point_scores_tf.py tests/test_v1_public_api.py tests/highdim/test_public_api_highdim.py -k "principal_sqrt or public_api or svd_sigma_point_analytic_score_matches_finite_difference"
```

## Result summary
- Added strict-SPD principal-square-root mathematical contract for both placement and innovation covariance derivatives in `docs/chapters/ch18_svd_sigma_point.tex`.
- Added shared strict-SPD principal-square-root helper logic in `bayesfilter/linear/svd_factor_tf.py` and exported it via `bayesfilter/linear/__init__.py`.
- Completed the experimental batched principal-square-root backend so `tf_principal_sqrt_ukf` uses principal-square-root derivative handling for both placement and innovation covariance branches.
- Added public scalar principal-square-root routes:
  - value/filter path through `backend="tf_principal_sqrt_ukf"` in `bayesfilter/nonlinear/sigma_points_tf.py`
  - analytic score path `tf_principal_sqrt_ukf_score` in `bayesfilter/nonlinear/svd_sigma_point_derivatives_tf.py`
- Exported the scalar score path through `bayesfilter/nonlinear/__init__.py` and top-level `bayesfilter/__init__.py`.
- Refreshed targeted evidence tests and public API checks.

## Diagnostics
| Metric | Value | Interpretation |
|---|---:|---|
| Experimental principal-sqrt kernel subset | `4 passed, 13 deselected` | Repeated-positive placement and repeated-positive innovation-spectrum fixtures now pass on `tf_principal_sqrt_ukf`; the historical SVD branch still blocks on weak spectral-gap fixtures. |
| Scalar/public principal-sqrt subset | `15 passed, 21 deselected` | Public scalar value/score path, API exposure, and finite-difference/public-surface checks passed for the new strict-SPD principal-square-root backend. |
| CPU/GPU mode for refreshed runs | CPU-only (`CUDA_VISIBLE_DEVICES=-1`) | Correct for smoke/correctness evidence refresh; no GPU claim is made from these runs. |
| Python executable | `/home/chakwong/anaconda3/envs/tf-gpu/bin/python` | Environment used for refreshed evidence. |
| TensorFlow version | `2.19.1` | Version used for refreshed evidence. |
| Git commit | `5ea363e594516be236ca7c78ab2067b28a5b6eb5` | Working tree is still dirty; result is scoped to this commit plus current working-tree changes. |

## Engineering observations
- The promoted scalar route is now present, but only as an explicit backend/function choice; no repo-wide default switch was made.
- The strict-SPD helper is shared in the linear layer, reducing duplication between scalar and batched principal-square-root routes.
- The experimental batched wrapper/interface collection still has a separate collection issue in this environment because Python resolves a site-packages `tests` package before the repo `tests/` directory; this did not block the directly relevant kernel and scalar/public checks.
- The promoted branch remains fail-closed on strict-SPD assumptions; structural-null and floor-active branches remain out of scope.

## Empirical evidence
- The new repeated-positive innovation-spectrum experimental test shows the principal-square-root route succeeds on a case where the historical eigenderivative UKF path blocks on a weak spectral gap.
- The public scalar principal-square-root value path is finite on benign fixtures and remains close to the historical UKF route on benign nonlinear fixtures.
- The public scalar principal-square-root score path passes the targeted finite-difference/public-surface refresh subset.
- Public symbol lists now include `tf_principal_sqrt_ukf_score` and the corresponding tests pass.

## Mathematical claims
- The strict-SPD principal-square-root derivative contract for both placement and innovation covariance branches is now documented in `docs/chapters/ch18_svd_sigma_point.tex` using Sylvester/Frechet equations.
- On the promoted strict-SPD branch, the innovation covariance derivative contract is solve/Sylvester based and is not expressed through eigendecomposition-derivative formulas.
- No claim is made here about semidefinite/structural-null branches, posterior correctness beyond tested contracts, or HMC convergence.

## Decision
- Promote the **strict-SPD principal-square-root UKF** to the public scalar BayesFilter value/filter backend `backend="tf_principal_sqrt_ukf"` and the public scalar score entry point `tf_principal_sqrt_ukf_score`.
- Demote the historical eigenderivative `tf_svd_ukf` / `tf_svd_ukf_score` path to a **historical, diagnostic-only, and regression-comparison** role.
- Do **not** use the historical eigenderivative route as the HMC-facing production recommendation on the promoted strict-SPD scope.
- Do **not** extend the promotion claim to structural-null / floor-active / semidefinite branches.
- Treat the refreshed evidence as sufficient for a public strict-SPD promotion step and a demotion of the old path, but still insufficient for a broader unconditional default-policy claim outside the strict-SPD scope.

## Next step
- If a repo-wide backend policy note is desired, write a short follow-up that treats `tf_principal_sqrt_ukf` as the promoted strict-SPD route and `tf_svd_ukf` as the historical diagnostic comparator.
- Keep future HMC work scoped to the promoted strict-SPD branch unless and until non-SPD/floor-active behavior is separately derived, implemented, and evidenced.
- Use the historical eigenderivative path only for regression comparison, spectral-gap telemetry, and failure-mode diagnosis on bounded fixtures.
