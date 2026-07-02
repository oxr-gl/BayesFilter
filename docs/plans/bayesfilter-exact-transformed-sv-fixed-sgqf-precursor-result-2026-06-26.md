# Exact-Transformed SV Fixed-SGQF Precursor Verification Result Note

metadata_date: 2026-06-26
program_id: source-scope-sgqf-exact-transformed-sv-precursor
status: PASS_TINY_FIXTURE_VALUE_ONLY_PRECURSOR
plan_file: docs/plans/bayesfilter-source-scope-sgqf-family-unlocks-master-program-2026-06-24.md

## Plan reference
- Primary governing artifact: `docs/plans/bayesfilter-source-scope-sgqf-family-unlocks-master-program-2026-06-24.md`
- Reset memo / immediate context: `docs/plans/bayesfilter-source-scope-sgqf-unlocks-reset-memo-2026-06-24.md`
- This execution was a focused tiny-fixture verification pass for the already-implemented precursor path in `bayesfilter/highdim/sv_mixture_cut4.py`; it was not a long benchmark, default-policy change, or source-row admission run.

## Question
Can the repo now support the current
`exact_transformed_sv_independent_panel_fixed_sgqf_filter(...)` path as a
**tiny-fixture, independent-panel, exact-target, value-only precursor route**
for exact transformed SV, without promoting it to a broader source-scope,
analytical-score, or source-faithful claim?

## Skeptical audit outcome
Pass, with explicit scope limits.

Why this audit passed before execution:
- the comparator is the same-target dense exact transformed SV reference,
  not a proxy target such as KSC or a Gaussian closure;
- the run is a small CPU-only fixture verification, not a long research-grade
  benchmark or leaderboard promotion;
- the tests intentionally keep the route internal and do not export it from
  `bayesfilter/highdim/__init__.py`;
- the result is framed as value-only and tiny-fixture-only, which prevents the
  generic non-Gaussian SGQF partial core from being over-claimed.

## Evidence contract
Baseline / truth anchor:
- `highdim.exact_transformed_sv_independent_panel_dense_reference(...)`

Primary promotion criterion:
- the exact transformed SV SGQF wrapper returns finite values on dims 1/2/3
  tiny fixtures and stays within declared dense-reference tolerances for:
  - total log-likelihood,
  - per-time log normalizers,
  - filtered mean path,
  - filtered covariance path.

Veto diagnostics:
- non-finite value outputs,
- mismatch against same-target dense reference beyond declared tolerances,
- covariance leakage inconsistent with the independent-panel diagonal
  construction,
- acceptance of a non-scalar SGQF cloud in a route that is supposed to run a
  one-dimensional cloud per coordinate,
- any attempt to treat this as an analytical-score, source-faithful, or
  leaderboard-admitted source row.

Explanatory-only diagnostics:
- exact numerical gap sizes used to set the regression thresholds,
- fixture layout checks for the dim-1 panel wrapper.

What is not concluded even if this pass succeeds:
- no coupled multivariate Zhao-Cui TT claim,
- no analytical-score claim,
- no source-faithful source-row admission,
- no generalized-SV unlock,
- no HMC or production-readiness claim.

## Implementation summary
Updated test coverage in:
- `tests/highdim/test_p41_exact_transformed_sv_zhaocui_ladder.py`

Added focused checks for:
- same-target SGQF-vs-dense tieout on dims 1/2/3,
- rejection of non-scalar SGQF clouds,
- dim-1 wrapper layout consistency,
- preservation of narrow diagnostics / non-claims.

The verified implementation target remains the existing internal route in:
- `bayesfilter/highdim/sv_mixture_cut4.py`
  - `ExactTransformedSVPanelFilterResult`
  - `exact_transformed_sv_independent_panel_fixed_sgqf_filter(...)`

No export was added to `bayesfilter/highdim/__init__.py`, and no generic
non-Gaussian Fixed-SGQF core claim was introduced.

## Command actually run
Diagnostic tolerance-calibration probe:
```bash
CUDA_VISIBLE_DEVICES=-1 python - <<'PY'
import tensorflow as tf
import bayesfilter.highdim as highdim
import bayesfilter.highdim.sv_mixture_cut4 as mod

def observations(dim):
    values = tf.constant([[0.12, -0.08, 0.05],[-0.07,0.11,-0.04]], dtype=tf.float64)
    return values[:, :dim]

def params(dim):
    gamma = tf.constant([0.60, 0.52, 0.47], dtype=tf.float64)[:dim]
    beta = tf.constant([0.40, 0.35, 0.45], dtype=tf.float64)[:dim]
    sigma = tf.constant([1.00, 0.85, 0.75], dtype=tf.float64)[:dim]
    return gamma, beta, sigma

for dim in [1,2,3]:
    obs = observations(dim)
    gamma,beta,sigma = params(dim)
    dense = highdim.exact_transformed_sv_independent_panel_dense_reference(obs, gamma=gamma, beta=beta, sigma=sigma, order=401, radius=8.0)
    sgqf = mod.exact_transformed_sv_independent_panel_fixed_sgqf_filter(obs, gamma=gamma, beta=beta, sigma=sigma, sparse_level=2)
    dense_mean = tf.stack([r.mean_path for r in dense.coordinate_results], axis=1)
    dense_var = tf.stack([r.variance_path for r in dense.coordinate_results], axis=1)
    sgqf_var = tf.linalg.diag_part(sgqf.covariance_path)
    offdiag = sgqf.covariance_path - tf.linalg.diag(tf.linalg.diag_part(sgqf.covariance_path))
    print('dim', dim)
    print('log_gap', float(tf.abs(sgqf.log_likelihood-dense.log_likelihood).numpy()))
    print('step_gap', float(tf.reduce_max(tf.abs(sgqf.log_normalizers-dense.log_normalizers)).numpy()))
    print('mean_gap', float(tf.reduce_max(tf.abs(sgqf.mean_path-dense_mean)).numpy()))
    print('var_gap', float(tf.reduce_max(tf.abs(sgqf_var-dense_var)).numpy()))
    print('offdiag_gap', float(tf.reduce_max(tf.abs(offdiag)).numpy()))
PY
```

Compile check:
```bash
CUDA_VISIBLE_DEVICES=-1 python -m compileall -q \
  tests/highdim/test_p41_exact_transformed_sv_zhaocui_ladder.py
```

Focused verification:
```bash
CUDA_VISIBLE_DEVICES=-1 pytest -q \
  tests/highdim/test_p41_exact_transformed_sv_zhaocui_ladder.py
```

## Run manifest
- git commit: `97ad05d40676f3fd15a2a2b4d45034ebb657ed97`
- git branch: `zhaocui-fixed-branch-derivative-validation`
- environment: `tf-gpu` conda env
- CPU/GPU status: CPU-only by explicit `CUDA_VISIBLE_DEVICES=-1`
- plan file: `docs/plans/bayesfilter-source-scope-sgqf-family-unlocks-master-program-2026-06-24.md`
- result file: `docs/plans/bayesfilter-exact-transformed-sv-fixed-sgqf-precursor-result-2026-06-26.md`
- data version: fixed tiny in-repo fixture observations from `tests/highdim/test_p41_exact_transformed_sv_zhaocui_ladder.py`
- random seeds: deterministic fixture / no stochastic benchmark run
- wall time: `pytest` 13.32s; compile check negligible
- modified code path: `tests/highdim/test_p41_exact_transformed_sv_zhaocui_ladder.py`

## Result summary
- Focused precursor verification passed.
- The updated `p41` exact-transformed ladder test file passed fully on CPU-only
  execution.
- The SGQF exact-transformed path is now regression-covered as a tiny-fixture,
  independent-panel, exact-target, value-only precursor route.

## Diagnostics
| Metric | Value | Interpretation |
|---|---:|---|
| `pytest` status | `16 passed` | Focused p41 ladder suite passed after adding the SGQF precursor tests. |
| `pytest` warnings | `2 deprecation warnings` | From TensorFlow Probability packaging/version code; not a route failure. |
| max `log_likelihood` gap | `0.018228303954654024` | Below the chosen `2e-2` regression threshold. |
| max `log_normalizers` gap | `0.015451825669833497` | Below the chosen `2e-2` regression threshold. |
| max `mean_path` gap | `0.05712523089766541` | Below the chosen `6e-2` regression threshold. |
| max `variance_path` gap | `0.13489970925351957` | Below the chosen `1.5e-1` regression threshold. |
| max covariance off-diagonal leakage | `0.0` | Confirms the independent-panel diagonal covariance construction on the tested fixture. |
| non-scalar cloud rejection | `pass` | The route still enforces a one-dimensional cloud per coordinate. |
| dim-1 wrapper layout check | `pass` | Panel wrapper remains consistent with scalar dense-reference bookkeeping. |

## Engineering observations
- The exact-transformed SGQF path is verified through an internal-module import
  rather than a public `highdim` export.
- The current regression coverage is intentionally attached to the `p41`
  exact-transformed ladder, which is the right same-target evidence lane.
- The observed maximum gaps were stable across dims 1/2/3 because the tested
  route is an independent-product panel wrapper around the same scalar update
  structure.

## Empirical evidence
- On the declared dim 1/2/3 tiny fixtures, the route stays finite and within the
  selected same-target dense-reference tolerances for value-path diagnostics.
- The route preserves diagonal covariance structure exactly on the tested
  independent-panel fixture.
- The route rejects a non-scalar cloud, matching the intended one-dimensional
  per-coordinate SGQF construction.

## Mathematical claims
- No new mathematical claim is promoted here.
- This result note records numerical agreement against the same-target dense
  reference on a tiny fixture only.
- Any broader claim about source-faithfulness, generalized non-Gaussian SGQF
  core correctness, or analytical score support still requires separate artifacts.

## Decision table
| decision | primary criterion | veto diagnostics | main uncertainty | next justified action | not concluded |
|---|---|---|---|---|---|
| Admit the current exact-transformed SV SGQF path as a tiny-fixture, independent-panel, exact-target, value-only precursor route | Passed focused dims 1/2/3 SGQF-vs-dense checks within declared tolerances; focused p41 suite passed on CPU-only execution | No non-finite outputs, no covariance leakage, and non-scalar cloud rejection behaved as intended | Whether this precursor should remain internal only or be used to justify the next augmented-noise-first unlock step | Keep the route internal and value-only, and use this note as the evidence anchor for any next-step unlock planning | No analytical-score, source-faithful, generalized-SV, HMC, production, or leaderboard-row-admission claim |

## Interpretation
The repo now has test-backed evidence that the existing
`exact_transformed_sv_independent_panel_fixed_sgqf_filter(...)` function is a
real same-target value-path precursor on the declared tiny exact-transformed SV
fixture.

This means:
- it is no longer just an unverified partial idea;
- it remains an internal independent-panel precursor rather than a public or
  source-faithful route;
- and it should be used as a narrow evidence anchor, not as a shortcut to claim
  generic non-Gaussian Fixed-SGQF support.

## Post-run red-team note
Strongest alternative explanation:
- the route may look stronger than it is because the tested fixture is tiny and
  factorized, so the stable gaps may reflect that narrow setting rather than a
  broader non-Gaussian SGQF capability.

What result would overturn the present conclusion:
- failure on a slightly broader exact-transformed tiny fixture family,
- instability when the same independent-panel target is checked at nearby
  parameter values or slightly longer horizons,
- or evidence that downstream artifacts start describing this as analytical-score
  or source-faithful support without the required separate gates.

Weakest part of the current evidence:
- the result is value-only and fixture-local; it does not exercise a generic
  non-Gaussian SGQF core because no such verified generic core exists yet.

## Next steps
1. Treat this note as the verification anchor for the current exact-transformed
   SGQF precursor route.
2. Keep the route internal and value-only unless a reviewed plan explicitly
   expands scope.
3. Use this precursor result, together with the master SGQF unlock program, to
   decide whether the next engineering step should be:
   - a broader exact-transformed precursor ladder, or
   - the augmented-noise-first path that the 2026-06-24 reset memo recommends
     for source-scope unlock progression.
4. Do not use this note to justify generic non-Gaussian `tf_fixed_sgqf_filter(...)`
   support; that remains a separate incomplete implementation problem.
