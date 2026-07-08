# Phase 8 Subplan: Leaderboard Admission And Release Note

Date: 2026-07-01

Status: DRAFT_SUBPLAN

## Phase Objective

Admit the actual-SV UKF analytical SR-UKF score to the leaderboard only if all
prior gates pass, regenerate artifacts, and write release-note boundaries.

## Entry Conditions Inherited From Previous Phase

- Phase 7 thorough test ladder passed.
- Phase 8 subplan has been refreshed with exact files/commands after Phase 7
  evidence is known.
- Phase 7 result preserves the exact four-route forbidden set:
  `GradientTape`, `tf_svd_sigma_point_filter`, historical SVD/eigenderivative
  derivatives, and strict-SPD principal-root derivative helpers.
- Phase 7 score-at-true consistency passed but exposed the required
  interpretation warning that the cubature SR-UKF actual-SV route can make the
  gamma score nearly zero structurally.

## Required Artifacts

- Leaderboard code diff or explicit no-admission blocker.
- Regenerated leaderboard JSON/Markdown if admitted.
- Release-note/update text describing score provenance and limitations.
- Phase 8 result.
- Final visible stop handoff.
- Provenance entry naming the admitted route:
  `actual_transformed_sv_independent_panel_augmented_noise_srukf_score`.
- Release/admission warning that score-at-true gamma evidence is weak because
  the cubature SR-UKF surrogate can make the gamma score nearly zero
  structurally.

## Required Checks/Tests/Reviews

- Leaderboard analytical score admission tests.
- Static route provenance tests.
- Regeneration command manifest.
- Claude read-only final review of admission/result.
- Checks that the actual-SV row does not call the historical diagnostic
  `actual_transformed_sv_independent_panel_augmented_noise_ukf_score`.
- Checks that admitted score provenance is
  `factor_propagating_srukf_manual_score`.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Should the actual-SV UKF row move from value-only diagnostic to admitted value-score analytical SR-UKF row? |
| Baseline/comparator | Current value-only actual-SV UKF row and Phase 7 evidence. |
| Primary criterion | Admission occurs only if all prior gates passed and leaderboard provenance names the analytical SR-UKF route. |
| Veto diagnostics | Any missing prior result, forbidden score provenance, unsupported release claim, or failed leaderboard test. |
| Explanatory diagnostics | Numeric leaderboard values and runtime. |
| Not concluded | Exact likelihood, HMC convergence, or superiority claims. |
| Artifact | Phase 8 result, regenerated leaderboard artifacts, final handoff. |

## Forbidden Claims/Actions

- Do not admit if any prior gate is missing.
- Do not change leaderboard criteria after seeing values.
- Do not call the route exact actual-SV likelihood.
- Do not import or call `GradientTape`, `tf_svd_sigma_point_filter`,
  historical SVD/eigenderivative derivatives, or strict-SPD principal-root
  derivative helpers from the admitted actual-SV SR-UKF analytical score path.
- Do not hide the gamma-score structural caveat from the release/admission
  note.

## Skeptical Plan Audit Before Execution

- Wrong-route risk: the final leaderboard must use
  `actual_transformed_sv_independent_panel_augmented_noise_srukf_score`, not the
  historical diagnostic UKF score wrapper.
- Proxy-promotion risk: Phase 7 score-at-true consistency permits admission
  consideration only; it does not establish exactness, superiority, HMC
  readiness, or GPU/XLA readiness.
- Boundary risk: release text must explicitly say raw actual-SV
  augmented-noise Gaussian-closure surrogate, not exact transformed
  same-target likelihood.
- Artifact-answer risk: regenerated leaderboard artifacts must expose the
  analytical SR-UKF provenance and the gamma-score caveat.

Audit status before execution:

- READY_FOR_PHASE_8_AFTER_PHASE_7_CLAUDE_REVIEW_CONVERGES.

## Exact Next-Phase Handoff Conditions

This is the final phase. Completion requires final handoff with result paths,
review trail, checks run, unresolved blockers, and nonclaims.

## Stop Conditions

- Any prior phase missing or blocked.
- Claude final review identifies material unsupported claim that cannot be
  repaired in five rounds.

## End-Of-Phase Procedure

1. Run required local checks.
2. Write Phase 8 result/close record.
3. Write final visible stop handoff.
4. Review final handoff for consistency, correctness, feasibility, artifact
   coverage, and boundary safety.
