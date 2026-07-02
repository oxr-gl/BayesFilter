# Phase 0 Result: Baseline Freeze And Launch Gate

Date: 2026-07-02

Status: `PASS_PHASE0_BASELINE_FREEZE`

## Decision Table

| Field | Decision |
| --- | --- |
| Decision | Launch the July 2 remaining-blockers program and advance to Phase 1 predator-prey T20. |
| Primary criterion status | Passed: launch artifacts exist, July 1 JSON/Markdown baseline hashes were recorded, remaining blockers were parsed, and runbook/master controls were verified. |
| Veto diagnostic status | Passed: no silent N/A blocker found; no Phase 0 row repair, GPU/XLA, HMC, package/network, or long benchmark was run. |
| Main uncertainty | Phase 0 did not inspect model internals or repair any row. |
| Next justified action | Review and execute Phase 1 predator-prey T20 target/evaluator subplan. |
| Not concluded | No row repair, score correctness, GPU readiness, HMC readiness, production readiness, or scientific validity. |

## Baseline Integrity

The July 1 leaderboard artifacts were treated as read-only Phase 0 inputs.

| Artifact | SHA256 |
| --- | --- |
| `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-01.json` | `3b4cf180b961b4ba4819887caa47da794b958e627ad03d1ec70c23ec48833e51` |
| `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-01.md` | `f07431bdfca397ad9d5a3960278316611e4ba0ec8d66f008a7d12113eb6406a3` |

The Markdown artifact contains all three targeted remaining-blocker row ids.
The JSON artifact contains nine targeted cells: three rows times three
algorithms.

## Remaining Blocker Inventory

| Row | Algorithm | Status | Score status | Numeric status | Reason |
| --- | --- | --- | --- | --- | --- |
| `zhao_cui_spatial_sir_austria_j9_T20` | `fixed_sgqf` | `blocked` | `blocked_no_free_theta` | `blocked_by_two_lane_contract_or_missing_source_scope_evaluator` | no reviewed SGQF source-scope spatial SIR route is wired |
| `zhao_cui_spatial_sir_austria_j9_T20` | `ukf` | `executed_value_only` | `None` | `executed_numeric_value_only_no_free_theta` | `None` |
| `zhao_cui_spatial_sir_austria_j9_T20` | `zhao_cui_scalar_or_multistate` | `blocked_or_status_only` | `None` | `blocked_full_filtering_evaluator_pending_p91_local_component_ready` | P91 local component ready; full observed-data/filtering row still blocked |
| `zhao_cui_predator_prey_T20` | `fixed_sgqf` | `blocked` | `blocked_target_alignment` | `blocked_predator_prey_sgqf_value` | no reviewed fixed-SGQF evaluator is wired for source-scope T20; P47 two-observation lower rung is diagnostic only |
| `zhao_cui_predator_prey_T20` | `ukf` | `executed_value_only` | `blocked_autodiff_not_admitted` | `executed_numeric_value_only_autodiff_score_not_admitted` | autodiff score provenance is diagnostic only |
| `zhao_cui_predator_prey_T20` | `zhao_cui_scalar_or_multistate` | `blocked_or_status_only` | `None` | `blocked_model_specific_evaluator_adapter_required` | `P8D_MODEL_SPECIFIC_NUMERIC_EVALUATOR_ADAPTER_REQUIRED` |
| `zhao_cui_generalized_sv_synthetic_from_estimated_values` | `fixed_sgqf` | `blocked` | `blocked_exact_source_row_evaluator_missing` | `blocked_generalized_sv_fixed_sgqf_source_row_evaluator_missing` | exact fixed-SGQF source-row evaluator missing |
| `zhao_cui_generalized_sv_synthetic_from_estimated_values` | `ukf` | `executed_value_only` | `blocked_autodiff_not_admitted` | `executed_numeric_value_only_autodiff_score_not_admitted` | autodiff score provenance is diagnostic only |
| `zhao_cui_generalized_sv_synthetic_from_estimated_values` | `zhao_cui_scalar_or_multistate` | `blocked_or_status_only` | `None` | `blocked_generalized_sv_zhao_cui_source_row_evaluator_adapter_required` | exact Zhao-Cui source-row evaluator missing |

No targeted cell is a silent N/A: each has explicit status, score status, or
reason.

## Checks Run

| Check | Result |
| --- | --- |
| Required-section structural check for master/runbook/subplans | Passed |
| JSON baseline parse and nine-row remaining-blocker inventory | Passed |
| JSON/Markdown target-row presence check | Passed |
| Control scan for Claude read-only, no detached run, GPU/XLA, autodiff, P47, P91, score-at-true, stop conditions | Passed |
| `git diff --check -- docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-*.md` | Passed |

## Claude Review

| Artifact | Rounds | Verdict |
| --- | ---: | --- |
| Master program | 1 narrowed review after one stalled broad prompt | `VERDICT: AGREE` |
| Visible runbook | 3 | `VERDICT: AGREE` |
| Phase 0 subplan | 2 | `VERDICT: AGREE` |

The runbook was revised to remove an explicit Claude health-probe command
because Claude judged that a fresh `claude -p` probe conflicts with the
runbook's no nested-agent rule. The final runbook now narrows and retries once,
then stops/handoffs for human direction if Claude review does not return.

## Run Manifest

| Field | Value |
| --- | --- |
| Repository | `/home/chakwong/BayesFilter` |
| Device context | No TensorFlow/GPU command was run in Phase 0. |
| Network/package access | None |
| Baseline artifacts | July 1 JSON/Markdown listed above |
| Plan artifacts | July 2 remaining-blockers master, runbook, ledgers, stop handoff, Phase 0-6 subplans |
| Result artifact | This file |

## Handoff

Phase 0 is complete. Phase 1 may begin after the refreshed Phase 1 subplan is
reviewed. Phase 1 must freeze the real predator-prey T20 target and must not
report P47 lower-rung diagnostic evidence as the T20 leaderboard row.
