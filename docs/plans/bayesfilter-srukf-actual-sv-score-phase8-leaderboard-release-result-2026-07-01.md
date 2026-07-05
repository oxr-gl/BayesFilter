# Phase 8 Result: Leaderboard Admission And Release Note

Date: 2026-07-01

Status: COMPLETE

## Phase Objective

Admit the actual-SV UKF analytical SR-UKF score to the highdim leaderboard after
the derivation, implementation, and test-ladder gates passed.

## Evidence Contract

| Field | Result |
| --- | --- |
| Question | Should the actual-SV UKF row move from value-only diagnostic to admitted value-score analytical SR-UKF row? |
| Baseline/comparator | Current value-only actual-SV UKF row and Phase 7 evidence. |
| Primary criterion | Admission occurs only if prior gates passed and leaderboard provenance names the analytical SR-UKF route. |
| Veto diagnostics | Missing prior result, forbidden score provenance, unsupported release claim, or failed leaderboard test. |
| Explanatory diagnostics | Numeric leaderboard values and runtime. |
| Not concluded | Exact likelihood, HMC convergence/readiness, GPU/XLA readiness, or superiority claims. |
| Artifact | July 1 highdim leaderboard JSON/Markdown, this result, final handoff. |

## Implementation Summary

- Prior gate artifacts checked before admission:
  `docs/plans/bayesfilter-srukf-actual-sv-score-phase6-actual-sv-adapter-implementation-result-2026-07-01.md`
  and
  `docs/plans/bayesfilter-srukf-actual-sv-score-phase7-test-ladder-result-2026-07-01.md`.
- Updated `docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py` to emit
  a new actual-SV UKF cell through
  `actual_transformed_sv_independent_panel_augmented_noise_srukf_score`.
- Preserved the historical SVD/autodiff demotion logic for other UKF rows.
- Updated the UKF analytical-score contract so reviewed
  `factor_propagating_srukf_manual_score` provenance is admitted alongside the
  existing reviewed KSC principal-root route.
- Regenerated:
  `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-01.json`
  and
  `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-01.md`.

## Actual-SV UKF Leaderboard Row

| Field | Value |
| --- | --- |
| Row | `zhao_cui_sv_actual_nongaussian_T1000` |
| Algorithm | `ukf` |
| Comparison status | `executed_value_score` |
| Numeric execution status | `executed_actual_sv_augmented_noise_srukf_value_score` |
| Score status | `analytical_score_emitted` |
| Average log likelihood | `-1.4607021961950382` |
| Score L2 norm | `1916.1087897290417` |
| Score provenance | `actual_sv_augmented_noise_factor_propagating_srukf_manual_score` |
| Timing rank status | `not_ranked_by_phase7_timing` |

Release/admission warning preserved in the row nonclaims:

- Score-at-true gamma consistency is weak evidence because the cubature SR-UKF
  surrogate can make gamma score nearly zero structurally.

## Checks Run

- `python -m py_compile docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py tests/test_two_lane_highdim_leaderboard_analytical_scores.py tests/test_two_lane_highdim_leaderboard_phase7.py`
  - Passed.
- `CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/test_two_lane_highdim_leaderboard_analytical_scores.py::test_actual_sv_ukf_cell_uses_reviewed_srukf_score_without_full_payload_rebuild tests/test_actual_sv_srukf_tf.py tests/test_srukf_factor_tf.py -q`
  - Passed: `15 passed`.
  - CPU-only by explicit device hiding; no GPU/XLA evidence is claimed.
- `CUDA_VISIBLE_DEVICES=-1 python docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py --output docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-01.json --markdown-output docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-01.md`
  - Passed and regenerated July 1 leaderboard artifacts.
  - CPU-only by explicit device hiding; TensorFlow printed CUDA initialization
    warnings, but this was not a GPU diagnostic and no GPU claim is made.
- `python -m json.tool docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-01.json`
  - Passed.
- `git diff --check -- docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py tests/test_two_lane_highdim_leaderboard_analytical_scores.py tests/test_two_lane_highdim_leaderboard_phase7.py docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-01.json docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-01.md`
  - Passed.

## Forbidden Route Set Preserved

The admitted actual-SV UKF score route still excludes the exact four forbidden
route families:

- `GradientTape`
- `tf_svd_sigma_point_filter`
- historical SVD/eigenderivative derivatives
- strict-SPD principal-root derivative helpers

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| Admit the actual-SV UKF SR-UKF analytical value/score row after Claude review if review converges. | Local checks and leaderboard regeneration passed. | No local veto fired. | This is still a surrogate Gaussian-closure row, and gamma-score evidence is weak. | Final handoff and optional commit/push if requested. | No exact likelihood, method superiority, HMC readiness, or GPU/XLA readiness. |

## Phase Handoff

This is the final planned phase. After bounded Claude review converges, the
program should close with a final visible stop handoff listing artifacts,
checks, residual nonclaims, and remaining unrelated leaderboard blockers.

## Claude Review

- Review path:
  `docs/plans/bayesfilter-srukf-actual-sv-score-phase8-leaderboard-release-result-2026-07-01.md`
- Prompt shape: bounded one-path read-only review.
- Verdict: `VERDICT: AGREE`.
- Summary: Claude agreed that the Phase 8 result satisfies the
  leaderboard-admission/release subplan as a result artifact, including prior
  gate dependency, admitted actual-SV SR-UKF provenance, regenerated leaderboard
  artifacts, exact four forbidden-route preservation, gamma-score caveat, and
  non-overclaiming. Claude suggested explicit prior-result path traceability;
  the result was patched to name the Phase 6 and Phase 7 result paths.
