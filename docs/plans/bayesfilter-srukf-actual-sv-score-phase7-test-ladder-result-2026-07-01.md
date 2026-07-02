# Phase 7 Result: Thorough Test Ladder

Date: 2026-07-01

Status: PASSED_TO_PHASE_8_LEADERBOARD_RELEASE

## Phase Objective

Run a thorough validation ladder for the generic SR-UKF backend and actual-SV
adapter before any leaderboard admission.

## Evidence Contract

| Field | Result |
| --- | --- |
| Question | Does the SR-UKF analytical score route pass necessary engineering and statistical sanity checks for leaderboard admission consideration? |
| Baseline/comparator | Own scalar SR-UKF objective for FD; generic affine parity tests; score-at-true-parameter consistency for actual-SV sanity. |
| Primary criterion | All veto tests pass and the result note preserves uncertainty and nonclaims. |
| Veto diagnostics | Static guard failure, reconstruction failure, affine parity failure, same-scalar FD failure, nonfinite score, or score-at-true interval excluding zero. |
| Explanatory diagnostics | Runtime and approximation caveats. |
| Not concluded | Exact likelihood correctness, HMC readiness, GPU/XLA readiness, or method superiority. |
| Artifact | This result, focused tests, and score-at-true JSON/Markdown artifacts. |

## Checks Run

- `CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/test_srukf_factor_tf.py tests/test_actual_sv_srukf_tf.py -q`
  - Passed: `14 passed`.
  - CPU-only by explicit device hiding; no GPU/XLA evidence is claimed.
- `CUDA_VISIBLE_DEVICES=-1 python docs/benchmarks/benchmark_actual_sv_srukf_phase7_ladder.py`
  - Passed.
  - Wrote:
    `docs/plans/bayesfilter-srukf-actual-sv-score-phase7-score-true-consistency-2026-07-01.json`
    and
    `docs/plans/bayesfilter-srukf-actual-sv-score-phase7-score-true-consistency-2026-07-01.md`.
  - CPU-only by explicit device hiding; TensorFlow printed CUDA initialization
    warnings, but this was not a GPU diagnostic and no GPU claim is made.
- `git diff --check -- bayesfilter/highdim/actual_sv_srukf_tf.py bayesfilter/highdim/__init__.py tests/test_actual_sv_srukf_tf.py docs/benchmarks/benchmark_actual_sv_srukf_phase7_ladder.py docs/plans/bayesfilter-srukf-actual-sv-score-phase6-actual-sv-adapter-implementation-result-2026-07-01.md docs/plans/bayesfilter-srukf-actual-sv-score-phase7-test-ladder-subplan-2026-07-01.md docs/plans/bayesfilter-srukf-actual-sv-score-visible-execution-ledger-2026-07-01.md docs/plans/bayesfilter-srukf-actual-sv-score-claude-review-ledger-2026-07-01.md`
  - Passed.
- Forbidden-token scan on the admitted implementation module:
  `rg -n "GradientTape|tf_svd_sigma_point_filter|eigenderivative|strict_spd_principal_sqrt|strict-SPD principal-root|principal_sqrt_frechet_derivative" bayesfilter/highdim/actual_sv_srukf_tf.py`
  - No matches.

## Score-At-True Consistency

The Phase 7 statistical sanity artifact generated 10 independent datasets for
each declared true-parameter case and computed the analytical SR-UKF score at
the true parameter.

| Case | Param | Mean | SE | z | Pass |
| --- | --- | ---: | ---: | ---: | --- |
| actual_sv_moderate_persistence | theta_gamma | -2.23315e-18 | 2.5587e-18 | -0.872766 | True |
| actual_sv_moderate_persistence | theta_beta | 0.761734 | 1.55086 | 0.491168 | True |
| actual_sv_higher_persistence | theta_gamma | 8.23893e-18 | 8.13905e-18 | 1.01227 | True |
| actual_sv_higher_persistence | theta_beta | 5.09469 | 2.94338 | 1.7309 | True |

Decision: the predeclared two-standard-error gate passed for both parameter
settings.

Important caveat: the cubature SR-UKF actual-SV route can make the gamma score
nearly zero structurally. That is acceptable for this sanity gate but weak
evidence about gamma information in the surrogate. Phase 8 must preserve this
warning in the release/admission note.

## Forbidden Route Set Preserved

The admitted actual-SV analytical score path still excludes the exact four
forbidden route families:

- `GradientTape`
- `tf_svd_sigma_point_filter`
- historical SVD/eigenderivative derivatives
- strict-SPD principal-root derivative helpers

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| Advance to Phase 8 after Claude review if review converges. | Local Phase 7 ladder passed. | No local veto fired. | Leaderboard/release wiring still needs exact provenance and nonclaim boundaries. | Refresh and execute Phase 8 admission subplan. | No exact likelihood, method superiority, HMC readiness, or GPU/XLA readiness. |

## Phase Handoff

Phase 8 may start after bounded Claude review of this result converges. Phase 8
must admit only the new analytical SR-UKF route, preserve the exact four
forbidden-route families, and record the gamma-score caveat.

## Claude Review

- Review path:
  `docs/plans/bayesfilter-srukf-actual-sv-score-phase7-test-ladder-result-2026-07-01.md`
- Prompt shape: bounded one-path read-only review.
- Verdict: `VERDICT: AGREE`.
- Summary: Claude agreed that the result satisfies the Phase 7 test-ladder
  requirements, including local checks, uncertainty handling, gamma-score
  caveat, exact four forbidden-route preservation, Phase 8 handoff, and
  non-overclaiming.
