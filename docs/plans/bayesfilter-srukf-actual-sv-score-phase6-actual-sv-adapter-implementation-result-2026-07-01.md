# Phase 6 Result: Actual-SV Adapter Implementation

Date: 2026-07-01

Status: PASSED_TO_PHASE_7_TEST_LADDER

## Phase Objective

Implement the actual-SV augmented-noise adapter and analytical score wrapper on
top of the generic factor-propagating SR-UKF backend.

## Evidence Contract

| Field | Result |
| --- | --- |
| Question | Does the actual-SV adapter map the audited augmented-noise law to the generic SR-UKF backend and produce an analytical score? |
| Baseline/comparator | Phase 3/4 adapter derivation and the current value-only diagnostic route. |
| Primary criterion | Focused actual-SV adapter tests pass with analytical provenance and no forbidden score route. |
| Veto diagnostics | Wrong sigma-point law, missing observation shock, nonfinite score, failed same-scalar FD, or forbidden dependency. |
| Explanatory diagnostics | Approximation gaps versus SGQF/dense are deferred to Phase 7/8. |
| Not concluded | No full leaderboard readiness, HMC readiness, GPU/XLA readiness, exact actual-SV likelihood, or same-target transformed likelihood. |
| Artifact | `bayesfilter/highdim/actual_sv_srukf_tf.py`, export wiring, `tests/test_actual_sv_srukf_tf.py`, this result. |

## Implementation Summary

- Added `bayesfilter/highdim/actual_sv_srukf_tf.py`, a separate admitted path
  for the actual-SV SR-UKF score.
- Exposed `ActualSVSRUKFPanelScoreResult` and
  `actual_transformed_sv_independent_panel_augmented_noise_srukf_score` through
  `bayesfilter.highdim`.
- Added focused tests in `tests/test_actual_sv_srukf_tf.py`.
- Kept the historical `sv_mixture_cut4.py` SVD/GradientTape UKF diagnostic
  route unchanged and outside the admitted static route-guard target.

## Audited-Label Mapping

| Audited label | Implementation mapping |
| --- | --- |
| `eq:bf-hd-actual-sv-srukf-augmented-law` | `augmented_mean=[m_{t-1},0,0]` and diagonal factor `[S_{t-1}, sigma, 1]` in `_actual_sv_srukf_axis_score`. |
| `eq:bf-hd-actual-sv-srukf-transition-map` | `_actual_sv_transition(points, gamma)` returns `gamma * H_{t-1} + U_t`. |
| `eq:bf-hd-actual-sv-srukf-observation-map` | `_actual_sv_observation(points, gamma, beta)` returns `beta * exp(H_t/2) * E_t`. |
| `eq:bf-hd-actual-sv-srukf-transition-derivatives` | `_actual_sv_step_derivatives(...).transition_jacobian_fn` and `d_transition_fn`. |
| `eq:bf-hd-actual-sv-srukf-observation-state-derivative` | `_actual_sv_step_derivatives(...).observation_jacobian_fn`. |
| `eq:bf-hd-actual-sv-srukf-observation-parameter-derivatives` | `_actual_sv_step_derivatives(...).d_observation_fn`. |
| `eq:bf-hd-actual-sv-srukf-initial-derivatives` | Initial `d_current_mean=zeros([2,1])` and subsequent step handoff from `step.d_filtered_mean`. |
| `eq:bf-hd-actual-sv-srukf-initial-factor-derivatives` | Initial scalar factor derivative `sigma * gamma * dgamma / (1-gamma^2)^(3/2)` and subsequent handoff from `step.d_filtered_factor`. |
| `eq:bf-hd-actual-sv-srukf-surrogate-loglik` | Accumulated `step.log_likelihood` from `tf_srukf_factor_score_step`. |
| `eq:bf-hd-actual-sv-srukf-score-handoff` | Accumulated `step.score`; panel score is flattened as `[theta_gamma_0, theta_beta_0, ...]`. |

## Forbidden Route Set Preserved

The admitted path preserves the exact four forbidden route families:

- `GradientTape`
- `tf_svd_sigma_point_filter`
- historical SVD/eigenderivative derivatives
- strict-SPD principal-root derivative helpers

Static guard scope is the admitted module
`bayesfilter/highdim/actual_sv_srukf_tf.py`. The historical diagnostic module is
not used as a dependency by the admitted route and remains excluded from the
admitted static guard target because it intentionally contains old diagnostic
code.

## Checks Run

- `python -m py_compile bayesfilter/highdim/actual_sv_srukf_tf.py bayesfilter/highdim/__init__.py tests/test_actual_sv_srukf_tf.py`
  - Passed.
- `CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/test_actual_sv_srukf_tf.py -q`
  - Passed: `4 passed`.
  - CPU-only by explicit device hiding; no GPU/XLA evidence is claimed.
- `CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/test_srukf_factor_tf.py tests/test_actual_sv_srukf_tf.py -q`
  - Passed: `13 passed`.
  - CPU-only by explicit device hiding; no GPU/XLA evidence is claimed.
- `git diff --check -- bayesfilter/highdim/actual_sv_srukf_tf.py bayesfilter/highdim/__init__.py tests/test_actual_sv_srukf_tf.py docs/plans/bayesfilter-srukf-actual-sv-score-phase6-actual-sv-adapter-implementation-subplan-2026-07-01.md`
  - Passed.
- `rg -n "GradientTape|tf_svd_sigma_point_filter|eigenderivative|strict_spd_principal_sqrt|strict-SPD principal-root|principal_sqrt_frechet_derivative" bayesfilter/highdim/actual_sv_srukf_tf.py`
  - No matches.

## Test Coverage Added

- Static route guard on the admitted module.
- Short-prefix finite value/score and dimension checks.
- Same-scalar centered finite-difference consistency against the new SR-UKF
  scalar objective.
- Fixed-sigma parameterization check confirming the score dimension is two per
  panel coordinate.

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| Advance to Phase 7 after Claude review if review converges. | Local focused tests passed. | No local veto fired. | Phase 7 must still run broader statistical and interpretation checks. | Run the thorough test ladder subplan. | No leaderboard admission, exact likelihood, HMC readiness, or GPU/XLA readiness. |

## Phase Handoff

Phase 7 may start after bounded Claude review of this result converges. Phase 7
must preserve the exact four forbidden route families, run the broader ladder,
and keep finite-difference checks scoped to same-objective consistency.

## Claude Review

- Review path:
  `docs/plans/bayesfilter-srukf-actual-sv-score-phase6-actual-sv-adapter-implementation-result-2026-07-01.md`
- Prompt shape: bounded one-path read-only review.
- Verdict: `VERDICT: AGREE`.
- Summary: Claude agreed that the result satisfies the Phase 6 subplan as a
  result artifact, including audited-label mapping, CPU-only checks,
  same-scalar FD scope, exact four forbidden-route preservation, separate
  admitted-module rationale, and non-overclaiming.
