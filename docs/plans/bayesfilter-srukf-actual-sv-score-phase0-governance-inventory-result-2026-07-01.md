# Phase 0 Result: Governance And Drift Inventory

Date: 2026-07-01

Status: PASS_PHASE0_GOVERNANCE_INVENTORY

## Objective

Freeze the SR-UKF actual-SV program boundary, inventory current drift evidence,
confirm launch artifacts exist, and launch only documentation/audit-first
execution.

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | Are the governance artifacts sufficient to launch derivation-first SR-UKF repair without repeating UKF drift? |
| Baseline/comparator | User request, visible runbook template, `AGENTS.md` Claude prompt shape, and current code/doc anchors. |
| Primary criterion | Passed. Launch artifacts exist, the Phase 0 result preserves the drift inventory, the two products are named, old drift routes are forbidden, and the Phase 1 handoff is specified. |
| Veto diagnostics | No missing launch artifact, no detached/nested launch, no unbounded Claude review, no unsupported derivation/implementation/scientific claim. |
| Not concluded | No SR-UKF derivation correctness, implementation correctness, numerical accuracy, leaderboard readiness, or HMC readiness is concluded. |

## Drift Inventory

Current code/doc anchors that motivated the repair:

- Current actual-SV UKF value-only diagnostic route:
  `bayesfilter/highdim/sv_mixture_cut4.py`, function
  `actual_transformed_sv_independent_panel_augmented_noise_ukf_filter`.
  The route labels itself as a value-only diagnostic and records
  `score_admission_status` as
  `value_only_until_reviewed_analytical_augmented_noise_score_exists`.
- Current actual-SV UKF score wrapper:
  `bayesfilter/highdim/sv_mixture_cut4.py`, function
  `actual_transformed_sv_independent_panel_augmented_noise_ukf_score`.
  The wrapper uses `GradientTape` and records
  `score_admission_status` as
  `not_admitted_requires_reviewed_analytical_augmented_noise_score`.
- Current KSC strict-SPD principal-root derivative score comparator:
  `bayesfilter/highdim/sv_mixture_cut4.py`, helper
  `_ukf_component_score_update`, calls `tf_principal_sqrt_ukf_score`.
  This remains a KSC/source-scope comparator, not the generic
  factor-propagating SR-UKF backend requested here.
- Current leaderboard admission guard:
  `docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py` rejects admitted
  score rows with autodiff/GradientTape provenance and rejects UKF leaderboard
  score provenance that uses historical SVD/eigenderivative wording.
- Current LaTeX drift source:
  `docs/chapters/ch18_svd_sigma_point.tex` documents a strict-SPD
  principal-square-root/Sylvester route and explicitly treats structural nulls
  or rank-deficient laws as a different branch.
- Current square-root contract:
  `docs/chapters/ch17_square_root_sigma_point.tex` states that a square-root
  backend must describe the actual factor recursion, whether covariances are
  reconstructed, and which operations define the differentiable target path.

## Two Products Frozen

1. Generic factor-propagating SR-UKF backend:
   - derives and implements factor propagation and analytical first derivatives;
   - does not rely on strict-SPD principal-root derivative substitution;
   - remains independent of actual-SV modeling choices.
2. Actual-SV augmented-noise adapter:
   - derives and implements the actual-SV pre-transition augmented-noise law;
   - maps that law into the generic backend;
   - preserves the UKF Gaussian-closure diagnostic boundary without claiming
     exact actual-SV likelihood.

## Forbidden Old Routes

For admitted leaderboard score rows, this program forbids:

- `GradientTape` or autodiff score provenance;
- historical SVD/eigenderivative score provenance;
- strict-SPD principal-root derivative substitution as the claimed generic
  factor-propagating SR-UKF analytical score;
- post-transition artificial perturbation that changes the actual-SV
  augmented-noise law.

## Checks Run

Local checks:

```text
rg -n "Phase Objective|Entry Conditions Inherited|Required Artifacts|Required Checks/Tests/Reviews|Evidence Contract|Forbidden Claims/Actions|Exact Next-Phase Handoff Conditions|Stop Conditions" docs/plans/bayesfilter-srukf-actual-sv-score-phase*-subplan-2026-07-01.md
rg -n "GradientTape|historical SVD|strict-SPD|principal-root|principal-square-root|autodiff|detached|VERDICT|MathDevMCP|score-at-true" docs/plans/bayesfilter-srukf-actual-sv-score-*.md
git diff --check -- docs/plans/bayesfilter-srukf-actual-sv-score-*.md
```

Outcome:

- Required subplan fields found.
- Forbidden-route guard language found.
- `git diff --check` passed for the SR-UKF plan artifacts.

Claude reviews:

- Master program: `VERDICT: AGREE`.
- Visible runbook: `VERDICT: AGREE`.
- Phase 0 subplan iteration 1: `VERDICT: REVISE`.
- Phase 0 subplan iteration 2 after patch: `VERDICT: AGREE`.

Review ledger:

- `docs/plans/bayesfilter-srukf-actual-sv-score-claude-review-ledger-2026-07-01.md`

## Phase 1 Handoff

Phase 1 may begin.

Required Phase 1 subplan:

- `docs/plans/bayesfilter-srukf-actual-sv-score-phase1-generic-derivation-subplan-2026-07-01.md`

Phase 1 must patch the LaTeX derivation for the generic factor-propagating
SR-UKF backend only. It must not implement code, run leaderboard regeneration,
or claim actual-SV adapter readiness.

## Stop/Handoff Status

No human-required blocker is present at the end of Phase 0.
