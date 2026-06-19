# P77 Phase 0 Subplan: Boundary Reset

metadata_date: 2026-06-19
status: PHASE0_SUBPLAN_CLAUDE_AGREE_READY_FOR_EXECUTION
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p77-corrected-metric-training-master-program-2026-06-19.md
runbook: docs/plans/bayesfilter-highdim-zhao-cui-p77-visible-gated-execution-runbook-2026-06-19.md
previous_result: docs/plans/bayesfilter-highdim-zhao-cui-p76-phase10-generated-corrected-metric-diagnostic-result-2026-06-19.md
phase: 0
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Phase Objective

Close the P76 prerequisite-repair lane for training purposes and open P77 as a
new training-evidence lane.  Phase 0 must record that P76 proved metric
plumbing and no-training leakage checks, not training improvement.  It must
also bind P77 to the \(20P_\theta\) fresh-sample rule before any future
fixed-branch regression/training evidence claim.

Phase 0 is documentation/planning only.  It must not edit implementation code,
construct an optimizer, call `train_step`, generate new training/evaluation
samples, run a training diagnostic, tune hyperparameters, or change defaults.

## Entry Conditions Inherited From P76

Phase 0 may begin only if:

- P76 Phase 10 result exists;
- P76 Phase 10 status is
  `PHASE10_CLAUDE_AGREE_CLOSED_READY_FOR_PHASE11_SUBPLAN`;
- P76 generated corrected-metric JSON exists and parses;
- P76 runbook/ledger/handoff state is closed through Phase 10;
- the P77 master program, runbook, ledgers, and this Phase 0 subplan have
  been reviewed with Claude to convergence within at most five rounds.
  If five rounds are reached without convergence, Phase 0 must not execute;
  write a blocker result/handoff and stop for human direction.

## Required Artifacts

Phase 0 must produce:

- Phase 0 result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p77-phase0-boundary-reset-result-2026-06-19.md`;
- drafted Phase 1 subplan:
  `docs/plans/bayesfilter-highdim-zhao-cui-p77-phase1-objective-split-contract-subplan-2026-06-19.md`;
- updated P77 master program status;
- updated P77 runbook status;
- updated P77 execution ledger;
- updated P77 Claude review ledger;
- updated P77 stop handoff.

## Required Checks/Tests/Reviews

Pre-execution checks:

```bash
rg -n "PHASE10_CLAUDE_AGREE_CLOSED_READY_FOR_PHASE11_SUBPLAN|generated-sample corrected-metric|train_step_count: 0|optimizer_used: false|fit-quality|Phase 11" docs/plans/bayesfilter-highdim-zhao-cui-p76-phase10-generated-corrected-metric-diagnostic-result-2026-06-19.md docs/plans/bayesfilter-highdim-zhao-cui-p76-visible-gated-execution-runbook-2026-06-18.md docs/plans/bayesfilter-highdim-zhao-cui-p76-visible-stop-handoff-2026-06-18.md
python -m json.tool docs/plans/bayesfilter-highdim-zhao-cui-p76-phase10-generated-corrected-metric-diagnostic-2026-06-19.json
rg -n "20\\s*P|20P|33120|40960|source-prefit|audit leakage|corrected heldout CE|UKF-initialized untrained" docs/plans/bayesfilter-highdim-zhao-cui-p77-corrected-metric-training-master-program-2026-06-19.md docs/plans/bayesfilter-highdim-zhao-cui-p77-visible-gated-execution-runbook-2026-06-19.md
```

Phase 0 documentation checks:

```bash
rg -n "P76 prerequisite|not training evidence|20P|33120|40960|corrected heldout CE|UKF-initialized untrained|Phase 1|no training" docs/plans/bayesfilter-highdim-zhao-cui-p77-phase0-boundary-reset-result-2026-06-19.md docs/plans/bayesfilter-highdim-zhao-cui-p77-phase1-objective-split-contract-subplan-2026-06-19.md
git diff --check -- docs/plans/bayesfilter-highdim-zhao-cui-p77-corrected-metric-training-master-program-2026-06-19.md docs/plans/bayesfilter-highdim-zhao-cui-p77-visible-gated-execution-runbook-2026-06-19.md docs/plans/bayesfilter-highdim-zhao-cui-p77-visible-execution-ledger-2026-06-19.md docs/plans/bayesfilter-highdim-zhao-cui-p77-claude-review-ledger-2026-06-19.md docs/plans/bayesfilter-highdim-zhao-cui-p77-visible-stop-handoff-2026-06-19.md docs/plans/bayesfilter-highdim-zhao-cui-p77-phase0-boundary-reset-subplan-2026-06-19.md docs/plans/bayesfilter-highdim-zhao-cui-p77-phase0-boundary-reset-result-2026-06-19.md docs/plans/bayesfilter-highdim-zhao-cui-p77-phase1-objective-split-contract-subplan-2026-06-19.md
```

Reviews:

- Claude read-only review of the initial P77 planning spine before Phase 0
  execution.
- Claude read-only review of Phase 0 result and Phase 1 subplan after local
  checks.
- Repair loop to convergence or max five rounds for the same material blocker.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Scientific/engineering question | Is P77 correctly scoped as a new training-evidence lane rather than treating P76 metric plumbing as training evidence? |
| Exact baseline/comparator | P76 Phase 10 closeout and the UKF-initialized untrained TT candidate as the future comparator. |
| Primary criterion | Phase 0 result states P76 did not prove training, P77 requires corrected heldout CE as primary fit metric, future evidence runs require \(N_{\rm train}\ge20P_\theta\), and Phase 1 is drafted to specify objective/split/leakage boundaries before any code or training. |
| Veto diagnostics | Any training run, optimizer construction, `train_step`, generated sample creation, hyperparameter tuning, default change, source-prefit revival, audit leakage, under-budget evidence allowance, or fit-quality/lower-gate/validation/HMC/scaling/source-faithfulness claim. |
| Explanatory only | Parameter-count arithmetic, proposed future `1024 x 40` budget, and P76 diagnostic CE values. |
| What will not be concluded | No training improvement, no fit-quality result, no lower-gate repair, no validation/HMC readiness, no scaling, no final hyperparameter/rank/sample policy. |
| Artifact preserving result | Phase 0 result, Phase 1 subplan, runbook/ledger/review-ledger/handoff updates. |

## Forbidden Claims/Actions

- Do not edit implementation code.
- Do not run training or generated-sample diagnostics.
- Do not construct an optimizer or call `train_step`.
- Do not tune hyperparameters.
- Do not change defaults.
- Do not claim P76 proved training improvement.
- Do not claim source-faithful Zhao--Cui implementation.
- Do not claim lower-gate repair, validation readiness, HMC readiness,
  scaling, or final rank/sample policy.
- Do not authorize a future under-budget training-evidence run.

## Exact Next-Phase Handoff Conditions

Phase 1 may begin only if:

- Phase 0 result exists;
- P77 runbook/ledger/handoff status says Phase 0 is Claude-agreed and ready
  for Phase 1;
- Phase 1 subplan exists and has been reviewed by Claude, or is explicitly
  pending review before Phase 1 execution;
- no implementation, training, tuning, GPU/CUDA, package/network, default
  change, or large-run action is required to begin Phase 1.

## Stop Conditions

Stop if:

- P76 Phase 10 closeout is missing or not parseable;
- P77 cannot state the \(20P_\theta\) training-budget rule without ambiguity;
- a future phase would permit training evidence below \(20P_\theta\);
- Claude identifies a material blocker that cannot be repaired within five
  rounds;
- continuing would require implementation edits, training, generated samples,
  GPU/CUDA, package/network work, or a default change.

## Skeptical Plan Audit

Phase 0 is deliberately docs-only because the most likely failure is semantic:
mistaking P76's metric-plumbing success for training success.  The subplan
therefore blocks all training actions and requires the Phase 1 objective/split
contract before any implementation or experiment.
