# P77 Phase 7 Subplan: Decision Boundary After First Budgeted Diagnostic

metadata_date: 2026-06-20
status: PHASE6_CLAUDE_AGREE_READY_FOR_PHASE7_DECISION
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p77-corrected-metric-training-master-program-2026-06-19.md
runbook: docs/plans/bayesfilter-highdim-zhao-cui-p77-visible-gated-execution-runbook-2026-06-19.md
previous_result: docs/plans/bayesfilter-highdim-zhao-cui-p77-phase6-budgeted-training-diagnostic-result-2026-06-19.md
phase: 7
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Phase Objective

Classify the Phase 6 result and choose the next evidence boundary without
overclaiming from a single budgeted corrected-validation diagnostic.

Phase 7 is a decision and planning phase.  It does not launch new training,
does not tune hyperparameters, does not run a final audit cloud, and does not
change defaults unless a separately reviewed later phase explicitly authorizes
that work.

## Entry Conditions Inherited From Phase 6

Phase 7 may begin only if:

- the Phase 6 JSON exists and parses;
- the Phase 6 result exists;
- Claude agrees Phase 6 execution/result or all Claude blockers have been
  repaired within the five-round loop;
- the Phase 7 decision does not retroactively alter the Phase 6 evidence
  contract;
- no GPU/CUDA, network/package/environment operation, default change,
  destructive action, detached agent, or large run is required.

## Required Artifacts

Phase 7 must produce:

- Phase 7 result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p77-phase7-decision-boundary-result-2026-06-19.md`;
- either a stop handoff or a reviewed next subplan, depending on the decision;
- updated P77 master program, runbook, execution ledger, Claude review ledger,
  and stop handoff.

## Required Checks/Tests/Reviews

Local checks:

```bash
python -m json.tool docs/plans/bayesfilter-highdim-zhao-cui-p77-phase6-budgeted-training-diagnostic-lr1e-3-2026-06-19.json
rg -n '"evidence_run": true|"hard_budget_gate_passed": true|"fit_quality_claim_permitted": true|"completed_batches": 40|"requested_batches": 40|"validation_improved_for_selection": true|"blockers": \\[\\]' docs/plans/bayesfilter-highdim-zhao-cui-p77-phase6-budgeted-training-diagnostic-lr1e-3-2026-06-19.json
rg -n "not source-faithful|not final audit|not lower-gate|not HMC readiness|not scaling|not default|single" docs/plans/bayesfilter-highdim-zhao-cui-p77-phase6-budgeted-training-diagnostic-result-2026-06-19.md
```

Review:

- Claude read-only review of the Phase 7 result and any next subplan.
- Repair loop to convergence within at most five rounds for material issues.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Scientific/engineering question | Given the Phase 6 pass, what is the next smallest honest evidence boundary for P77? |
| Exact baseline/comparator | Phase 6 trained candidate versus the untrained UKF baseline, as already recorded; no new comparator is introduced in Phase 7. |
| Primary criterion | Phase 7 passes if it classifies Phase 6 as one of: pass, fail, blocker, or tuning-design need, and chooses a next action consistent with the Phase 6 nonclaims. |
| Veto diagnostics | Any attempt to claim final audit validity, source-faithfulness, HMC readiness, default policy, scaling, lower-gate repair, or final hyperparameter policy from Phase 6 alone. |
| Explanatory only | Phase 6 training loss, gradient norm, replay values, runtime, and TensorFlow startup warnings. |
| What will not be concluded | No new scientific correctness claim; Phase 7 only decides the next governed evidence step. |
| Artifact preserving result | Phase 7 result and the next subplan or stop handoff. |

## Candidate Phase 7 Classifications

Phase 7 must classify Phase 6 as exactly one of:

- `pass_first_budgeted_diagnostic`: Phase 6 passed its frozen primary
  criterion and veto checks, so the next work should test robustness or add a
  missing evidence layer.
- `fail_validation_gate`: Phase 6 completed but did not improve corrected
  validation CE, so the next work should diagnose training or tuning.
- `blocker`: Phase 6 lacked required fields, failed a veto diagnostic, or had
  command/provenance mismatch.
- `tuning_design_need`: Phase 6 was inconclusive or positive but too brittle
  to proceed without a reviewed tuning design.

The current Phase 6 result appears to support
`pass_first_budgeted_diagnostic`, pending Claude review.

## Candidate Next Actions

If Phase 7 classifies Phase 6 as `pass_first_budgeted_diagnostic`, the likely
next governed phase should be one of:

- replicated validation evidence across new seeds with the same frozen
  corrected metric;
- a separately generated final audit cloud that remains unused for training,
  stopping, tuning, or model selection;
- downstream lower-gate/HMC-readiness diagnostics, with Phase 6 treated only
  as prerequisite fit evidence;
- a small learning-rate or sample-budget robustness check, but only if the
  decision artifact explains why replication or final-audit evidence is not
  the next smallest discriminating step.

Phase 7 must not silently launch any of these.  It only chooses and drafts the
next governed subplan.

## Forbidden Claims/Actions

- Do not claim source-faithful Zhao--Cui behavior.
- Do not claim final audit evidence from Phase 6.
- Do not claim lower-gate repair, validation/HMC readiness, scaling, default
  policy, or final rank/sample/learning-rate policy.
- Do not use replay or audit to retroactively select Phase 6.
- Do not launch new training, final-audit, GPU, large, network, package,
  destructive, detached, or default-changing commands.
- Do not alter the Phase 6 primary criterion after seeing the result.

## Exact Next-Phase Handoff Conditions

A later phase may begin only if:

- Phase 7 result exists;
- Claude agrees Phase 7 execution/result;
- the chosen next step has a dedicated reviewed subplan;
- any required human approval for evidence runs, GPU/CUDA, large runs,
  network/package/environment operations, default changes, destructive
  actions, or detached execution has been obtained separately.

## Stop Conditions

Stop if:

- Claude identifies a material Phase 6 result blocker that cannot be repaired
  within five rounds;
- Phase 7 cannot choose a next evidence boundary without a user scientific
  direction decision;
- the next action would require evidence, GPU, default, package, network,
  destructive, detached, or large-run approval not already granted;
- a proposed result would overclaim beyond Phase 6.

## Skeptical Plan Audit

The central risk is promotion creep: Phase 6 passed a meaningful but narrow
budgeted corrected-validation gate.  Phase 7 must preserve that result without
turning it into a final audit, source-faithfulness, HMC-readiness, default, or
scaling claim.  The next phase should be chosen because it answers the next
smallest missing evidence question, not because it makes the current result
sound stronger.
