# Actual-Transformed SV Augmented-Noise SGQF Next-Step Result Note

metadata_date: 2026-06-26
program_id: actual-transformed-sv-augmented-noise-sgqf-next-step
status: PASS_VALUE_ONLY_PRECURSOR_ROUTE_SHORT_PREFIX_ONLY
plan_file: docs/plans/bayesfilter-actual-transformed-sv-augmented-noise-sgqf-next-step-plan-2026-06-26.md

## Plan reference
- `docs/plans/bayesfilter-actual-transformed-sv-augmented-noise-sgqf-next-step-plan-2026-06-26.md`
- `docs/plans/bayesfilter-actual-transformed-sv-source-scope-sgqf-unlock-plan-2026-06-24.md`
- `docs/plans/bayesfilter-source-scope-sgqf-family-unlocks-master-program-2026-06-24.md`
- `docs/plans/bayesfilter-exact-transformed-sv-fixed-sgqf-precursor-result-2026-06-26.md`
- `docs/plans/bayesfilter-exact-transformed-sv-fixed-sgqf-broader-precursor-ladder-result-2026-06-26.md`

## Question
Can the repo add a minimal **augmented-noise-first, value-only SGQF precursor**
for the actual-transformed SV family, with short-prefix deterministic evidence,
without silently upgrading that precursor into same-target source-row admission?

## Skeptical audit outcome
Pass, with explicit scope limits.

Why the audit passed:
- the first-pass scope stayed at the short-prefix, value-only, deterministic
  diagnostic level;
- the route is labeled as an augmented-noise precursor rather than same-target
  admission;
- numerical comparison remained tied to the exact-transformed dense reference as
  a plausibility check, not as a claim that the precursor closes the source-row
  identity gap;
- source-scope contract tests were rerun so wording drift would have been caught.

## Evidence contract
Baseline / truth anchor:
- `highdim.exact_transformed_sv_independent_panel_dense_reference(...)`
  on the same tiny deterministic fixture

Primary promotion criterion:
- a short-prefix augmented-noise SGQF precursor route exists,
- returns finite value outputs,
- preserves explicit precursor-only / value-only diagnostics and non-claims,
- and shows bounded disagreement versus the exact-transformed dense reference
  good enough to keep the engineering path alive.

Veto diagnostics:
- target-identity drift,
- non-finite outputs,
- source-scope contract drift,
- any accidental analytical-score or same-target admission narration.

Explanatory-only diagnostics:
- exact gap size versus the exact-transformed dense reference,
- how much looser the precursor is than the existing internal exact-transformed
  SGQF wrapper.

What is not concluded:
- no same-target source-row admission,
- no analytical-score support,
- no generic non-Gaussian SGQF core support,
- no HMC or production-readiness claim.

## Implementation summary
Added a new precursor route in:
- `bayesfilter/highdim/sv_mixture_cut4.py`
  - `ActualTransformedSVPanelFilterResult`
  - `actual_transformed_sv_independent_panel_augmented_noise_fixed_sgqf_filter(...)`
  - `_actual_transformed_sv_augmented_noise_fixed_sgqf_model(...)`

Exported through:
- `bayesfilter/highdim/__init__.py`

Added focused short-prefix tests in:
- `tests/highdim/test_p41_exact_transformed_sv_zhaocui_ladder.py`

The route shape is deliberately narrow:
- independent-panel outer loop,
- two-dimensional SGQF cloud per coordinate (`latent state`, `observation-noise`),
- Gaussian-closure recursion with a small `observation_variance_floor`,
- value-only diagnostics and explicit non-claims.

## Command actually run
Compile check:
```bash
CUDA_VISIBLE_DEVICES=-1 python -m compileall -q \
  bayesfilter/highdim/sv_mixture_cut4.py \
  bayesfilter/highdim/__init__.py \
  tests/highdim/test_p41_exact_transformed_sv_zhaocui_ladder.py \
  tests/highdim/test_p43_sv_value_gradient_cut4_zhaocui.py \
  tests/highdim/test_filtering_value_gradient_benchmark_source_paper_scope.py
```

Focused verification:
```bash
CUDA_VISIBLE_DEVICES=-1 pytest -q \
  tests/highdim/test_p41_exact_transformed_sv_zhaocui_ladder.py \
  tests/highdim/test_p43_sv_value_gradient_cut4_zhaocui.py \
  tests/highdim/test_filtering_value_gradient_benchmark_source_paper_scope.py
```

Gap measurement probe:
```bash
CUDA_VISIBLE_DEVICES=-1 python - <<'PY'
import tensorflow as tf
import bayesfilter.highdim as highdim

obs = tf.constant([[0.12, -0.08, 0.05]], dtype=tf.float64)
gamma = tf.constant([0.60, 0.52, 0.47], dtype=tf.float64)
beta = tf.constant([0.40, 0.35, 0.45], dtype=tf.float64)
sigma = tf.constant([1.00, 0.85, 0.75], dtype=tf.float64)
for dim in [1,2,3]:
    cur_obs = obs[:, :dim]
    dense = highdim.exact_transformed_sv_independent_panel_dense_reference(cur_obs, gamma=gamma[:dim], beta=beta[:dim], sigma=sigma[:dim], order=401, radius=8.0)
    sgqf = highdim.actual_transformed_sv_independent_panel_augmented_noise_fixed_sgqf_filter(cur_obs, gamma=gamma[:dim], beta=beta[:dim], sigma=sigma[:dim], sparse_level=2)
    dense_mean = tf.stack([r.mean_path for r in dense.coordinate_results], axis=1)
    dense_var = tf.stack([r.variance_path for r in dense.coordinate_results], axis=1)
    per_time_jac = tf.reduce_sum(tf.math.log(tf.abs(cur_obs)), axis=1)
    sgqf_var = tf.linalg.diag_part(sgqf.covariance_path)
    offdiag = sgqf.covariance_path - tf.linalg.diag(sgqf_var)
    print('dim', dim)
    print('log_gap', float(tf.abs(sgqf.log_likelihood + tf.reduce_sum(per_time_jac) - dense.log_likelihood).numpy()))
    print('step_gap', float(tf.reduce_max(tf.abs(sgqf.log_normalizers + per_time_jac - dense.log_normalizers)).numpy()))
    print('mean_gap', float(tf.reduce_max(tf.abs(sgqf.mean_path - dense_mean)).numpy()))
    print('var_gap', float(tf.reduce_max(tf.abs(sgqf_var - dense_var)).numpy()))
    print('offdiag_gap', float(tf.reduce_max(tf.abs(offdiag)).numpy()))
PY
```

## Run manifest
| Field | Value |
|---|---|
| git commit | `97ad05d40676f3fd15a2a2b4d45034ebb657ed97` |
| git branch | `zhaocui-fixed-branch-derivative-validation` |
| environment | `tf-gpu` conda env |
| CPU/GPU status | `CPU-only; CUDA_VISIBLE_DEVICES=-1` |
| plan path | `docs/plans/bayesfilter-actual-transformed-sv-augmented-noise-sgqf-next-step-plan-2026-06-26.md` |
| result path | `docs/plans/bayesfilter-actual-transformed-sv-augmented-noise-sgqf-next-step-result-2026-06-26.md` |
| code surfaces | `bayesfilter/highdim/sv_mixture_cut4.py`, `bayesfilter/highdim/__init__.py`, `tests/highdim/test_p41_exact_transformed_sv_zhaocui_ladder.py` |
| seeds | deterministic tiny fixture only |
| wall time | focused pytest 350.93s |

## Result summary
The first augmented-noise-first next step passed at the intended evidence level.

What is now true:
- the repo has a concrete **actual-transformed SV augmented-noise SGQF
  precursor** entry point;
- the route is regression-covered on a short-prefix deterministic fixture;
- the route stayed governance-clean under the existing p41/p43/source-scope
  tests;
- the route remains explicitly value-only and precursor-only.

## Diagnostics
| Metric | Value | Interpretation |
|---|---:|---|
| focused pytest status | `63 passed` | p41, p43, and source-scope contract checks all passed after adding the precursor route. |
| warnings | `2 deprecation warnings` | TFP packaging/version warnings only. |
| worst short-prefix `log_likelihood` gap | `0.23655605513577171` | Short-prefix plausibility gap versus exact-transformed dense reference; bounded but clearly looser than the exact internal SGQF wrapper. |
| worst short-prefix `log_normalizers` gap | `0.23655605513577171` | Same as the one-step total on the tested short prefix. |
| worst short-prefix `mean_path` gap | `0.5564179786156743` | Large enough to prevent any same-target narration; still finite and stable as a precursor. |
| worst short-prefix `variance_path` gap | `0.2618274684216835` | Bounded but materially looser than the exact internal SGQF wrapper. |
| worst off-diagonal leakage | `0.0` | Independent-panel diagonal covariance structure remained exact on the tested fixture. |
| cloud dimension guard | `pass` | The new precursor rejects non-2D clouds as intended. |
| source-scope contract drift | `not observed` | Existing source-scope tests continued to pass. |

## Engineering observations
- The precursor is implemented as a two-dimensional per-coordinate SGQF route
  with explicit observation-noise augmentation.
- It uses a small positive `observation_variance_floor` to keep the Gaussian-
  closure recursion numerically well-defined under the current SGQF core.
- This makes the route usable as a precursor, but it is also the main reason it
  must not be described as same-target admission or generic non-Gaussian core
  evidence.
- The route is materially looser than the internal exact-transformed SGQF
  wrapper, which is acceptable for this specific engineering gate but not for a
  source-row admission claim.

## Empirical evidence
- The precursor returns finite short-prefix values across dims 1/2/3 on the
  deterministic fixture.
- The exact-transformed dense reference remains the stronger same-target oracle;
  the augmented-noise precursor is only a bounded approximation route at this
  stage.
- Existing p43 and source-scope tests passing means the new route did not
  contaminate score claims or row-identity contracts.

## Mathematical claims
- No new mathematical claim is promoted.
- This note records only that a bounded augmented-noise SGQF precursor can be
  executed and checked on a short deterministic fixture.
- It does not establish that the precursor is mathematically equivalent to the
  exact-transformed target.

## Decision table
| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not concluded |
|---|---|---|---|---|---|
| admit the augmented-noise SGQF route as a value-only, short-prefix engineering precursor for the actual-transformed SV family | satisfied: route exists, focused tests pass, metadata/non-claims preserved, and short-prefix comparison stays finite and bounded | no target-identity drift, no score-claim drift, no source-scope contract drift observed | whether the precursor can be improved enough to support any later runner/value-status integration beyond the current short-prefix ceiling | keep the route precursor-only, record its loose gap profile explicitly, and only widen scope under a new reviewed plan | no same-target admission, no analytical score, no generic non-Gaussian core, no HMC, no production claim |

## Post-run red-team note
Strongest alternative explanation:
- the route may only be “working” because the small observation-variance floor
  stabilizes a Gaussian-closure surrogate that is still too far from the exact
  transformed target for anything beyond precursor use.

What would overturn the present conclusion:
- failure on a slightly broader short-prefix ladder,
- source-scope artifact drift treating this precursor as row admission,
- or evidence that the observation-variance-floor adaptation dominates the route
  behavior rather than merely stabilizing it.

Weakest part of the evidence:
- the precursor is much looser than the exact internal SGQF wrapper on the same
  tiny fixture, especially in filtered means.

## Next steps
1. Treat this route as a **value-only, short-prefix augmented-noise precursor**
   and nothing more.
2. Do not yet touch runner/leaderboard row status from `blocked_not_same_target`
   based on this result alone.
3. If the family is revisited next, the honest follow-up is a reviewed short-
   prefix improvement pass (or an explicit blocked/limit note), not score-path or
   source-row promotion work.
4. Keep the internal exact-transformed SGQF wrapper and this augmented-noise
   precursor as separate evidence lanes with separate claim ceilings.
