# P77 Phase 5 Subplan: Proper Budgeted Training Diagnostic Design

metadata_date: 2026-06-19
status: DRAFT_PENDING_PHASE4_EXECUTION_REVIEW
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p77-corrected-metric-training-master-program-2026-06-19.md
runbook: docs/plans/bayesfilter-highdim-zhao-cui-p77-visible-gated-execution-runbook-2026-06-19.md
previous_result: docs/plans/bayesfilter-highdim-zhao-cui-p77-phase4-mechanics-smoke-result-2026-06-19.md
phase: 5
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Phase Objective

Design the first proper P77 budgeted corrected-metric training diagnostic
without running it.

Phase 5 must turn the Phase 2 protocol and Phase 4 mechanics-smoke result into
an exact Phase 6 evidence-run plan.  It must freeze the command(s), learning
rate handling, pass/fail rule, veto diagnostics, replay/audit boundaries,
runtime bounds, and approval needs before any evidence run.

Phase 5 is design-only.  It must not run `1024 x 40`, pass `--evidence-run`,
run a training-evidence command, use GPU/CUDA, use network, install packages,
change defaults, or launch detached agents.

## Entry Conditions Inherited From Phase 4

Phase 5 may begin only if:

- Phase 4 result exists;
- Claude agrees Phase 4 execution/result and this Phase 5 subplan is adequate;
- Phase 4 JSON exists and parses;
- Phase 4 JSON records `evidence_run=false`,
  `non_evidence_mechanics_smoke=true`, `hard_budget_gate_passed=false`,
  `fit_quality_claim_permitted=false`, and
  `validation_improved_for_selection=null`;
- \(P_\theta=1656\), minimum evidence samples `33120`, and preferred first
  proper budget `1024 x 40 = 40960` remain unchanged;
- the P77 runner/test focused checks pass;
- no proper evidence run is required to execute Phase 5.

## Required Artifacts

Phase 5 must produce:

- Phase 5 result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p77-phase5-budgeted-training-design-result-2026-06-19.md`;
- drafted Phase 6 subplan:
  `docs/plans/bayesfilter-highdim-zhao-cui-p77-phase6-budgeted-training-diagnostic-subplan-2026-06-19.md`;
- updated P77 master program, runbook, execution ledger, Claude review ledger,
  and stop handoff.

## Required Checks/Tests/Reviews

Prechecks:

```bash
python -m json.tool docs/plans/bayesfilter-highdim-zhao-cui-p77-phase4-mechanics-smoke-2026-06-19.json
rg -n '"non_evidence_mechanics_smoke": true|"evidence_run": false|"hard_budget_gate_passed": false|"fit_quality_claim_permitted": false|"validation_improved_for_selection": null|"P_theta": 1656|"minimum_training_samples": 33120|"N_train": 4' docs/plans/bayesfilter-highdim-zhao-cui-p77-phase4-mechanics-smoke-2026-06-19.json
rg -n "P_theta|1656|33120|40960|learning rate|validation-only|audit exclusion|replay|untrained UKF baseline|failed historical routes" docs/plans/bayesfilter-highdim-zhao-cui-p77-phase2-budget-tuning-protocol-result-2026-06-19.md docs/plans/bayesfilter-highdim-zhao-cui-p77-phase4-mechanics-smoke-result-2026-06-19.md
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q scripts/p77_budgeted_corrected_metric_training.py tests/highdim/test_p77_budgeted_corrected_metric_training.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p77_budgeted_corrected_metric_training.py
```

Documentation checks:

```bash
rg -n "1024 x 40|40960|33120|20P|evidence-run|--evidence-run|learning-rate|0.0001|0.0003|0.001|validation-only|audit final|replay|approval" docs/plans/bayesfilter-highdim-zhao-cui-p77-phase5-budgeted-training-design-result-2026-06-19.md docs/plans/bayesfilter-highdim-zhao-cui-p77-phase6-budgeted-training-diagnostic-subplan-2026-06-19.md
rg -n "primary criterion|veto diagnostics|explanatory only|not concluded|non-evidence|fit_quality_claim_permitted|validation_improved_for_selection|untrained UKF baseline" docs/plans/bayesfilter-highdim-zhao-cui-p77-phase5-budgeted-training-design-result-2026-06-19.md docs/plans/bayesfilter-highdim-zhao-cui-p77-phase6-budgeted-training-diagnostic-subplan-2026-06-19.md
git diff --check -- scripts/p77_budgeted_corrected_metric_training.py tests/highdim/test_p77_budgeted_corrected_metric_training.py docs/plans/bayesfilter-highdim-zhao-cui-p77-phase4-mechanics-smoke-result-2026-06-19.md docs/plans/bayesfilter-highdim-zhao-cui-p77-phase5-budgeted-training-design-subplan-2026-06-19.md docs/plans/bayesfilter-highdim-zhao-cui-p77-phase5-budgeted-training-design-result-2026-06-19.md docs/plans/bayesfilter-highdim-zhao-cui-p77-phase6-budgeted-training-diagnostic-subplan-2026-06-19.md docs/plans/bayesfilter-highdim-zhao-cui-p77-corrected-metric-training-master-program-2026-06-19.md docs/plans/bayesfilter-highdim-zhao-cui-p77-visible-gated-execution-runbook-2026-06-19.md docs/plans/bayesfilter-highdim-zhao-cui-p77-visible-execution-ledger-2026-06-19.md docs/plans/bayesfilter-highdim-zhao-cui-p77-claude-review-ledger-2026-06-19.md docs/plans/bayesfilter-highdim-zhao-cui-p77-visible-stop-handoff-2026-06-19.md
```

Review:

- Claude read-only review of the Phase 5 result and Phase 6 subplan.
- Repair loop to convergence within at most five rounds.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Scientific/engineering question | Can P77 freeze an exact, non-arbitrary first proper corrected-metric training diagnostic before any evidence run? |
| Exact baseline/comparator | UKF-initialized untrained TT baseline evaluated by corrected validation, replay, and final-only audit CE under the same role definitions as the trained candidate. |
| Primary criterion | Phase 5 result and Phase 6 subplan specify exact CPU-only command(s), \(N_{\rm train}=40960\ge33120\), predeclared learning-rate handling, validation-only selection rule, replay role, final-only audit rule, veto diagnostics, runtime bounds, and explicit approval requirement before Phase 6 execution. |
| Veto diagnostics | Any evidence command is run in Phase 5; arbitrary/post-hoc tuning; audit or replay used for selection; under-budget evidence allowance; proxy metrics promoted; random/constant/source-prefit revived; default/GPU/network/package/destructive/detached action. |
| Explanatory only | Phase 4 smoke CE values, training loss, replay CE, runtime warnings, and expected runtime estimates. |
| What will not be concluded | No training improvement, no hyperparameter selection from new results, no proper evidence result, no lower-gate repair, no validation/HMC readiness, no scaling. |
| Artifact preserving result | Phase 5 result and Phase 6 budgeted-training diagnostic subplan. |

## Required Diagnostic Design

Phase 5 must freeze the following Phase 6 design.

### First Proper Budget

The first proper evidence budget for the current candidate is:

```text
batch_size = 1024
batches = 40
N_train = 40960
P_theta = 1656
minimum_training_samples = 33120
```

This satisfies the hard rule \(N_{\rm train}\ge20P_\theta\).

### Learning-Rate Handling

Learning-rate candidates remain the predeclared Phase 2 set:

\[
  \eta\in\{10^{-4}, 3\cdot10^{-4}, 10^{-3}\}.
\]

Phase 5 must choose one of two designs and justify it before Phase 6:

- single-candidate diagnostic at \(\eta=10^{-3}\), the current default,
  interpreted as the first proper evidence run for the existing runner; or
- three-candidate validation-only diagnostic, where each candidate starts from
  the same UKF initializer, uses the same `1024 x 40` budget, and the winner
  is selected only by corrected validation CE after vetoes.

If the three-candidate design is chosen, the sample budget applies per
learning-rate candidate.  Audit remains final-only after validation selection.

### Required Phase 6 Command Shape

The Phase 6 evidence command must be CPU-only unless the user separately
approves GPU:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python scripts/p77_budgeted_corrected_metric_training.py --output <phase6-json> --degree 2 --rank 4 --batch-size 1024 --batches 40 --learning-rate <predeclared-lr> --max-seconds <reviewed-bound> --seed <reviewed-seed> --evidence-run
```

The exact output path, learning rate(s), max-seconds value, and seed(s) must be
written in the Phase 5 result and Phase 6 subplan.

### Primary Pass Rule

A Phase 6 candidate may pass the training diagnostic only if all of the
following hold:

- `evidence_run=true`;
- `hard_budget_gate_passed=true`;
- `N_train >= 33120`;
- `fit_quality_claim_permitted=true`;
- validation and replay metric quantities are finite;
- bridge/tieout checks pass;
- audit is not used for training, stopping, tuning, or selection;
- failed historical routes remain fenced;
- corrected validation CE for the trained candidate is lower than corrected
  validation CE for the untrained UKF baseline under the predeclared
  validation-only rule;
- `validation_improved_for_selection=true` appears only for a budget-passing
  evidence run.

### Veto Diagnostics

Phase 6 must veto on:

- nonfinite training loss, gradient, rho, normalizer, log density, CE, alpha,
  or target mass;
- bridge failure or target tieout failure;
- CE reconstruction mismatch;
- corrected alpha mass tolerance failure;
- seed overlap between training, validation, replay, and audit roles;
- audit used for selection, tuning, stopping, or rescue;
- `hard_budget_gate_passed=false`;
- failed historical route revival;
- unapproved GPU/CUDA, network/package/env operation, default change,
  destructive action, detached agent, or large-run escalation.

Replay may veto only for nonfinite/invalid metric construction, reconstruction
or alpha-mass failure, wrong role/provenance, or a numeric severe-degradation
threshold frozen in the Phase 5 result.  Otherwise replay is explanatory.

### Audit Boundary

Audit is final-only.  Phase 6 may evaluate audit only after validation
selection has frozen the selected candidate and no further tuning is allowed.

If the current runner cannot yet evaluate audit for evidence runs, Phase 5
must either:

- specify a Phase 6 design that does not claim final audit evidence and stops
  after validation/replay, or
- require a scoped runner patch in a later reviewed phase before Phase 6.

## Forbidden Claims/Actions

- Do not run the Phase 6 evidence command in Phase 5.
- Do not pass `--evidence-run` in Phase 5.
- Do not use GPU/CUDA, network, package installs, detached agents, destructive
  actions, default changes, or large diagnostics.
- Do not tune from Phase 4 smoke values.
- Do not use replay or audit for selection.
- Do not revive random, calibrated-constant, or source-prefit routes.
- Do not claim training improvement, hyperparameter choice from new evidence,
  lower-gate repair, validation/HMC readiness, scaling, or source-faithful
  Zhao--Cui parity.

## Exact Next-Phase Handoff Conditions

Phase 6 may begin only if:

- Phase 5 result exists;
- Claude agrees Phase 5 execution/result and the Phase 6 subplan;
- the exact Phase 6 command(s), outputs, seed(s), learning rate(s), runtime
  bound, primary criterion, veto diagnostics, replay/audit roles, and nonclaims
  are frozen;
- the user explicitly approves the Phase 6 evidence run after seeing the
  reviewed Phase 6 subplan.

## Stop Conditions

Stop if:

- Phase 5 cannot choose a non-arbitrary single-candidate or three-candidate
  learning-rate design;
- Phase 6 would require audit behavior the runner cannot represent;
- evidence-run runtime bounds cannot be stated;
- the \(20P_\theta\) gate or validation-only selection rule is weakened;
- replay or audit would leak into selection;
- failed historical routes are revived;
- Claude identifies a material blocker that cannot be repaired within five
  rounds;
- continuing would require running the evidence command or crossing any
  human-required boundary.

## Skeptical Plan Audit

The main Phase 5 risk is accidentally designing a run that is still arbitrary:
choosing learning rate, stopping, replay threshold, or audit behavior after
seeing Phase 6 results.  Phase 5 must freeze those choices before Phase 6.
The second risk is treating Phase 4's one-step CE movement as evidence; Phase
5 must explicitly ignore Phase 4 CE for tuning or promotion.
