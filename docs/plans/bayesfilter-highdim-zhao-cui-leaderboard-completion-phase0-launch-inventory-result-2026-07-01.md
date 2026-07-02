# Phase 0 Result: Launch Inventory And Fail-Closed Zhao-Cui Contract

Date: 2026-07-01

Status: `PASS_PHASE0_LAUNCH_INVENTORY`

Subplan:

- `docs/plans/bayesfilter-highdim-zhao-cui-leaderboard-completion-phase0-launch-inventory-subplan-2026-07-01.md`

## Decision Table

| Field | Result |
| --- | --- |
| Decision | Launch the Zhao-Cui-only leaderboard completion program under the visible runbook. |
| Primary criterion status | Passed: required artifacts exist, required subplan sections are present, current Zhao-Cui rows are inventoried, and admitted/value-only/blocked outcomes are representable without SGQF or autodiff analytical-score shortcuts. |
| Veto diagnostic status | Passed: SGQF is excluded; autodiff remains blocked for analytical-score admission; source-faithfulness is fail-closed on missing/partial/conflicting anchors; trusted GPU/XLA rules are encoded in master/runbook. |
| Main uncertainty | Later phases may still close rows as precise blockers if target/evaluator/derivative ownership cannot be stated safely. |
| Next justified action | Review and execute Phase 1 for actual-SV and KSC Zhao-Cui analytical-score repair. |
| Not concluded | No code correctness, score correctness, full leaderboard completion, GPU readiness, HMC readiness, production readiness, source-faithful adaptive Zhao-Cui reproduction, or exact nonlinear likelihood correctness. |

## Launch Review Status

| Artifact | Review status |
| --- | --- |
| Master program | Claude iteration 2: `VERDICT: AGREE` |
| Visible runbook | Claude iteration 2: `VERDICT: AGREE` |
| Phase 0 subplan | Claude iteration 3: `VERDICT: AGREE` |

Review ledger:

- `docs/plans/bayesfilter-highdim-zhao-cui-leaderboard-completion-claude-review-ledger-2026-07-01.md`

## Current Zhao-Cui Row Inventory

Source artifact:

- `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-01.json`

| Row | Comparison status | Score status | Numeric execution status |
| --- | --- | --- | --- |
| `benchmark_lgssm_exact_oracle_m3_T50` | `executed_value_score` | `None` | `executed_lgssm_exact_oracle_adapter_value_score` |
| `zhao_cui_sv_actual_nongaussian_T1000` | `executed_value_only` | `blocked_autodiff_not_admitted` | `executed_numeric_value_only_autodiff_score_not_admitted` |
| `zhao_cui_sv_ksc_gaussian_mixture_surrogate_T1000` | `executed_value_only` | `blocked_autodiff_not_admitted` | `executed_numeric_value_only_autodiff_score_not_admitted` |
| `zhao_cui_spatial_sir_austria_j9_T20` | `blocked_or_status_only` | `None` | `blocked_full_filtering_evaluator_pending_p91_local_component_ready` |
| `zhao_cui_predator_prey_T20` | `blocked_or_status_only` | `None` | `blocked_model_specific_evaluator_adapter_required` |
| `zhao_cui_generalized_sv_synthetic_from_estimated_values` | `blocked_or_status_only` | `None` | `blocked_generalized_sv_zhao_cui_source_row_evaluator_adapter_required` |

## Representability Check

The current leaderboard schema can represent the three outcome classes needed
by this program:

- admitted value plus score: `executed_value_score`;
- value-only with score blocker: `executed_value_only` plus
  `blocked_autodiff_not_admitted`;
- precise blocked/status-only row: `blocked_or_status_only` plus explicit
  `reason` and `numeric_execution_status`.

The Phase 0 check verified:

- admitted Zhao-Cui rows have a score vector;
- value-only rows preserve the autodiff-not-admitted score blocker;
- blocked rows preserve a reason string;
- no SGQF row is needed to satisfy the Zhao-Cui representability contract.

## Local Checks

No TensorFlow, GPU, HMC, package, network, or long benchmark command was run in
Phase 0.

| Check | Result |
| --- | --- |
| Required artifact existence check | Passed |
| Required subplan-section check | Passed |
| Current Zhao-Cui row inventory check | Passed |
| Admitted/value-only/blocked representability check | Passed |
| Master/runbook source-anchor, autodiff, and trusted GPU/XLA keyword check | Passed |
| `git diff --check` on new Zhao-Cui completion plan artifacts | Passed |

## Evidence Contract Close

Phase 0 asked whether the Zhao-Cui-only completion program could launch without
mixing SGQF work, admitting autodiff as analytical score, or hiding real
evaluator gaps.

Result: yes. The launch artifacts are in place, the repair loop has hard
bounds, Claude review converged, and the next phase is narrow: actual-SV/KSC
Zhao-Cui score repair or precise blocker.

## Phase 1 Handoff

Phase 1 may start after its subplan review converges:

- `docs/plans/bayesfilter-highdim-zhao-cui-leaderboard-completion-phase1-sv-ksc-score-subplan-2026-07-01.md`

Phase 1 must not relabel existing autodiff scores as analytical. It must either
emit a manual same-scalar analytical score for actual-SV/KSC Zhao-Cui rows, or
preserve exact blockers.
