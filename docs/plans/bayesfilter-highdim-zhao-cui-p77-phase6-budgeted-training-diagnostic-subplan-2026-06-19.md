# P77 Phase 6 Subplan: Budgeted Corrected-Metric Training Diagnostic

metadata_date: 2026-06-19
status: PHASE5_CLAUDE_AGREE_AWAITING_EXPLICIT_PHASE6_APPROVAL
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p77-corrected-metric-training-master-program-2026-06-19.md
runbook: docs/plans/bayesfilter-highdim-zhao-cui-p77-visible-gated-execution-runbook-2026-06-19.md
previous_result: docs/plans/bayesfilter-highdim-zhao-cui-p77-phase5-budgeted-training-design-result-2026-06-19.md
phase: 6
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Phase Objective

Run the first proper P77 budgeted corrected-metric training diagnostic, but
only after explicit human approval of this reviewed subplan and the exact
command.

Phase 6 answers whether the existing UKF-warm-started, mini-batch-trained
fixed branch improves corrected validation CE against the untrained UKF
baseline under \(N_{\rm train}=40960\ge33120=20P_\theta\).

## Entry Conditions Inherited From Phase 5

Phase 6 may begin only if:

- Phase 5 result exists;
- Claude agrees Phase 5 execution/result and this Phase 6 subplan;
- the exact Phase 6 command below is frozen;
- the user explicitly approves launching the Phase 6 evidence command;
- no GPU/CUDA, network/package/env operation, default change, destructive
  action, detached agent, or command modification is required.

## Required Artifacts

Phase 6 must produce:

- JSON diagnostic:
  `docs/plans/bayesfilter-highdim-zhao-cui-p77-phase6-budgeted-training-diagnostic-lr1e-3-2026-06-19.json`;
- Phase 6 result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p77-phase6-budgeted-training-diagnostic-result-2026-06-19.md`;
- drafted Phase 7 decision subplan:
  `docs/plans/bayesfilter-highdim-zhao-cui-p77-phase7-decision-boundary-subplan-2026-06-19.md`;
- updated P77 master program, runbook, execution ledger, Claude review ledger,
  and stop handoff.

## Required Checks/Tests/Reviews

Prechecks:

```bash
rg -n "PHASE5|1024 x 40|40960|33120|learning-rate=0.001|validation_improved_for_selection|validation_not_improved_against_untrained_ukf_baseline|approval" docs/plans/bayesfilter-highdim-zhao-cui-p77-phase5-budgeted-training-design-result-2026-06-19.md docs/plans/bayesfilter-highdim-zhao-cui-p77-phase6-budgeted-training-diagnostic-subplan-2026-06-19.md
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q scripts/p77_budgeted_corrected_metric_training.py tests/highdim/test_p77_budgeted_corrected_metric_training.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p77_budgeted_corrected_metric_training.py
```

Evidence command, only after explicit user approval:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python scripts/p77_budgeted_corrected_metric_training.py --output docs/plans/bayesfilter-highdim-zhao-cui-p77-phase6-budgeted-training-diagnostic-lr1e-3-2026-06-19.json --degree 2 --rank 4 --batch-size 1024 --batches 40 --learning-rate 0.001 --max-seconds 7200 --seed 7706 --evidence-run
```

Postchecks:

```bash
python -m json.tool docs/plans/bayesfilter-highdim-zhao-cui-p77-phase6-budgeted-training-diagnostic-lr1e-3-2026-06-19.json
rg -n '"evidence_run": true|"hard_budget_gate_passed": true|"fit_quality_claim_permitted": true|"P_theta": 1656|"minimum_training_samples": 33120|"N_train": 40960|"completed_batches": 40|"validation_improved_for_selection"|"audit_used_for_selection": false|"source_route_prefit_used": false|"default_behavior_changed": false' docs/plans/bayesfilter-highdim-zhao-cui-p77-phase6-budgeted-training-diagnostic-lr1e-3-2026-06-19.json
rg -n "primary criterion|veto diagnostics|explanatory only|not concluded|untrained UKF baseline|validation_not_improved_against_untrained_ukf_baseline|audit final|replay" docs/plans/bayesfilter-highdim-zhao-cui-p77-phase6-budgeted-training-diagnostic-result-2026-06-19.md docs/plans/bayesfilter-highdim-zhao-cui-p77-phase7-decision-boundary-subplan-2026-06-19.md
git diff --check -- scripts/p77_budgeted_corrected_metric_training.py tests/highdim/test_p77_budgeted_corrected_metric_training.py docs/plans/bayesfilter-highdim-zhao-cui-p77-phase6-budgeted-training-diagnostic-lr1e-3-2026-06-19.json docs/plans/bayesfilter-highdim-zhao-cui-p77-phase6-budgeted-training-diagnostic-result-2026-06-19.md docs/plans/bayesfilter-highdim-zhao-cui-p77-phase7-decision-boundary-subplan-2026-06-19.md docs/plans/bayesfilter-highdim-zhao-cui-p77-corrected-metric-training-master-program-2026-06-19.md docs/plans/bayesfilter-highdim-zhao-cui-p77-visible-gated-execution-runbook-2026-06-19.md docs/plans/bayesfilter-highdim-zhao-cui-p77-visible-execution-ledger-2026-06-19.md docs/plans/bayesfilter-highdim-zhao-cui-p77-claude-review-ledger-2026-06-19.md docs/plans/bayesfilter-highdim-zhao-cui-p77-visible-stop-handoff-2026-06-19.md
```

Review:

- Claude read-only review of Phase 6 result and Phase 7 subplan.
- Repair loop to convergence within at most five rounds.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Scientific/engineering question | Does the UKF-warm-started P77 runner improve corrected validation CE against the untrained UKF baseline under \(N_{\rm train}=40960\ge33120\)? |
| Exact baseline/comparator | UKF-initialized untrained TT baseline, same corrected validation and replay CE roles as the trained candidate. |
| Primary criterion | Pass only if the exact approved command completes 40 batches, records `evidence_run=true`, `hard_budget_gate_passed=true`, `fit_quality_claim_permitted=true`, empty blockers, and `validation_improved_for_selection=true`. |
| Veto diagnostics | Incomplete or under-budget run, nonfinite training/metric quantities, bridge/tieout failure, CE reconstruction mismatch, alpha mass failure, seed overlap, audit selection/tuning, failed-route revival, validation non-improvement, default/GPU/network/package/destructive/detached action, or command mismatch. |
| Explanatory only | Training loss, gradient norm, rho range, normalizer, replay CE after validity checks, runtime, TensorFlow warnings, and Phase 4 smoke CE. |
| What will not be concluded | No source-faithful Zhao--Cui claim, no final audit claim, no lower-gate repair, no validation/HMC readiness, no scaling, no default policy, no final rank/sample/learning-rate policy. |
| Artifact preserving result | Phase 6 JSON/result and Phase 7 decision-boundary subplan. |

## Forbidden Claims/Actions

- Do not launch Phase 6 without explicit user approval.
- Do not modify the command after approval without returning to Phase 5.
- Do not use GPU/CUDA, network, package installs, detached agents,
  destructive actions, default changes, or large-run escalation.
- Do not tune from replay or audit.
- Do not revive random, calibrated-constant, or source-prefit routes.
- Do not claim training success unless the primary criterion and veto
  diagnostics pass.
- Do not claim final audit evidence; the current runner does not evaluate a
  separate final audit cloud.
- Treat evidence-run completion as mandatory.  If the command stops before all
  40 requested batches complete, the runner must emit the
  `incomplete_batch_count` blocker and Phase 6 must not pass.

## Exact Next-Phase Handoff Conditions

Phase 7 may begin only if:

- Phase 6 result exists;
- Claude agrees Phase 6 execution/result;
- Phase 7 subplan exists and classifies the result as pass, fail, blocker, or
  tuning-design need;
- no further evidence, GPU, default, or large run is required to begin Phase 7.

## Stop Conditions

Stop if:

- explicit user approval is absent;
- the command would be changed from the reviewed command;
- the run exceeds reviewed bounds or fails before producing a valid JSON;
- the JSON omits required evidence/budget/metric fields;
- validation non-improvement triggers the evidence veto;
- audit or replay leaks into selection;
- Claude identifies a material blocker that cannot be repaired within five
  rounds.

## Skeptical Plan Audit

The main risk is overclaim: a single budgeted run can establish whether the
current path passed this diagnostic, but it cannot establish final rank,
sample, learning-rate, scaling, lower-gate, HMC, or source-faithfulness claims.
Phase 6 must treat validation as the only selector and replay as validity or
explanatory evidence only.
