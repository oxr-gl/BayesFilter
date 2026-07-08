# Phase 4 Result: UKF Analytical-Score Cleanup

Date: 2026-07-02

Status: `BLOCK_PHASE4_UKF_TARGET_ROWS_MANUAL_SRUKF_ROUTES_MISSING`

## Decision Table

| Field | Result |
| --- | --- |
| Decision | Keep the predator-prey and generalized-SV UKF target rows as value-only blockers. |
| Primary criterion status | Not met for either target row: no reviewed exact-row principal-square-root or factor-propagating SR-UKF manual derivative binding exists. |
| Veto diagnostic status | Veto preserved: the only current target-row score provenance is autodiff diagnostic evidence, so no score is admitted. |
| Main uncertainty | Whether the project wants a dedicated derivation/implementation phase for manual SR-UKF derivatives on these exact nonlinear rows. |
| Next justified action | Advance to Phase 5 readiness/calibration for rows already admitted in Phases 1-2 and previously admitted SV/KSC rows; do not include these two UKF rows in score readiness. |
| What is not being concluded | No claim that UKF is impossible for these rows, no HMC/GPU/production readiness claim, no all-row leaderboard regeneration, and no scientific ranking claim. |

## Evidence Contract Outcome

| Field | Outcome |
| --- | --- |
| Question | Can predator-prey and generalized-SV UKF value-only rows be upgraded to analytical-score rows without SVD/tape/FD provenance? |
| Baseline/comparator | July 1 UKF value-only rows and reviewed SR-UKF standards from actual-SV/KSC work. |
| Primary criterion | Finite analytical score plus structured principal-square-root/factor route binding, or precise row-local blocker. |
| Outcome | Precise row-local blockers for both target rows. |
| Veto diagnostics | Autodiff/tape evidence remains diagnostic only; no SVD/FD score admitted. |
| Artifact | Derivative inventory, route-binding ledger, and row-local UKF JSON artifacts listed below. |

## Artifacts

- Derivative inventory:
  `docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-phase4-ukf-derivative-inventory-2026-07-02.json`
- Structured route-binding ledger:
  `docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-phase4-ukf-route-bindings-2026-07-02.json`
- Predator-prey UKF row-local artifact:
  `docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-phase4-predator-prey-ukf-row-2026-07-02.json`
- Generalized-SV UKF row-local artifact:
  `docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-phase4-generalized-sv-ukf-row-2026-07-02.json`

## Findings

The July 1 baseline already had finite UKF values for both target rows:

| Row | Status | Average log likelihood | Log likelihood | Runtime |
| --- | --- | ---: | ---: | ---: |
| `zhao_cui_predator_prey_T20` | `executed_value_only` | `-8.56827587430274` | `-171.3655174860548` | `5.479427` |
| `zhao_cui_generalized_sv_synthetic_from_estimated_values` | `executed_value_only` | `-1.428934153339374` | `-1440.365626566089` | `15.095921` |

Both rows were value-only because the available score provenance was TensorFlow
autodiff diagnostic evidence:

- `ukf_predator_prey_structural_sigma_point_tf_autodiff_score`
- `ukf_generalized_sv_augmented_noise_sigma_point_tf_autodiff_score`

Phase 4 did not find a reviewed exact-row manual principal-square-root or
factor-propagating SR-UKF binding for either target row. Existing admitted UKF
score standards are actual-SV factor SR-UKF and KSC principal-square-root UKF
routes; they are guardrails only and are not reused as predator-prey or
generalized-SV evidence.

## Checks

Broad preflight command:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/test_two_lane_highdim_leaderboard_analytical_scores.py tests/test_actual_sv_srukf_tf.py tests/test_srukf_factor_tf.py
```

Outcome: interrupted with code `130` after no useful output; narrowed under the
smallest-focused-diagnostic rule.

Narrowed route-guard bundle:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/test_srukf_factor_tf.py::test_srukf_backend_source_passes_static_route_guard tests/test_srukf_factor_tf.py::test_srukf_route_guard_rejects_forbidden_route_families tests/test_srukf_factor_tf.py::test_srukf_route_guard_assertion_rejects_forbidden_file
```

Outcome: `7 passed in 2.24s`.

Route/provenance inventory scans found reviewed admitted SR-UKF score functions
for actual-SV and KSC, and no exact predator-prey/generalized-SV manual SR-UKF
score implementation binding.

## Boundary Safety

This phase intentionally does not:

- admit `GradientTape`, `ForwardAccumulator`, finite-difference, or historical
  SVD eigenderivative UKF score evidence;
- relabel an autodiff diagnostic as analytical score;
- reuse actual-SV or KSC SR-UKF evidence for generalized-SV or predator-prey;
- repair SIR UKF without a reviewed no-free-theta replacement contract;
- regenerate the all-row leaderboard.

## Phase 5 Handoff

Phase 5 may proceed with:

- admitted Zhao-Cui predator-prey row-local value/manual-score evidence from
  Phase 1;
- admitted Zhao-Cui generalized-SV row-local value/manual-score evidence from
  Phase 2;
- precise SIR full-row blocker from Phase 3;
- precise UKF value-only blockers from Phase 4.

Readiness/calibration must not promote the two Phase 4 UKF rows to score rows.
