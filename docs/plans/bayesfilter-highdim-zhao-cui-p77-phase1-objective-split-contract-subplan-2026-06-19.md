# P77 Phase 1 Subplan: Objective, Split, And Leakage Contract

metadata_date: 2026-06-19
status: DRAFT_REPAIRED_AFTER_CLAUDE_R1_PENDING_REVIEW
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p77-corrected-metric-training-master-program-2026-06-19.md
runbook: docs/plans/bayesfilter-highdim-zhao-cui-p77-visible-gated-execution-runbook-2026-06-19.md
previous_result: docs/plans/bayesfilter-highdim-zhao-cui-p77-phase0-boundary-reset-result-2026-06-19.md
phase: 1
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Phase Objective

Define the mathematical objective, comparator, and data-role split for P77
before any implementation or training.  Phase 1 must freeze what counts as
training loss, validation metric, replay diagnostic, audit final check, and
forbidden leakage.

Phase 1 is design-only.  It must not edit implementation code, construct an
optimizer, call `train_step`, generate new samples, run a training diagnostic,
tune hyperparameters, or change defaults.

## Entry Conditions Inherited From Phase 0

Phase 1 may begin only if:

- Phase 0 result exists;
- Phase 0 status is Claude-agreed and ready for Phase 1 execution, or this
  subplan is being reviewed before Phase 1 execution;
- P77 master/runbook/ledger/handoff record the \(20P_\theta\) training-budget
  rule;
- P76 Phase 10 closeout remains the predecessor for metric plumbing;
- no implementation or training action is needed to execute Phase 1.

## Required Artifacts

Phase 1 must produce:

- Phase 1 result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p77-phase1-objective-split-contract-result-2026-06-19.md`;
- drafted Phase 2 subplan:
  `docs/plans/bayesfilter-highdim-zhao-cui-p77-phase2-budget-tuning-protocol-subplan-2026-06-19.md`;
- updated P77 master program, runbook, execution ledger, Claude review ledger,
  and stop handoff.

## Required Checks/Tests/Reviews

Prechecks:

```bash
rg -n "PHASE0|20P|33120|40960|corrected heldout CE|UKF-initialized untrained|not training evidence|audit final" docs/plans/bayesfilter-highdim-zhao-cui-p77-phase0-boundary-reset-result-2026-06-19.md docs/plans/bayesfilter-highdim-zhao-cui-p77-corrected-metric-training-master-program-2026-06-19.md docs/plans/bayesfilter-highdim-zhao-cui-p77-visible-gated-execution-runbook-2026-06-19.md
rg -n "P76CorrectedHeldoutMetricBatch|corrected_heldout_density_metric|P75ObjectiveBatch|weighted_empirical_cross_entropy_weights|train_step|make_adam_optimizer" bayesfilter/highdim/stochastic_density_training.py
```

Documentation checks:

```bash
rg -n "training loss|validation metric|replay|audit final|corrected target-only|UKF-initialized untrained|20P|no under-budget|forbidden leakage|Phase 2|random|calibrated-constant|source-prefit|failed historical routes|not live routes" docs/plans/bayesfilter-highdim-zhao-cui-p77-phase1-objective-split-contract-result-2026-06-19.md docs/plans/bayesfilter-highdim-zhao-cui-p77-phase2-budget-tuning-protocol-subplan-2026-06-19.md
rg -n "P_theta|parameter count|rank|degree|budget arithmetic|evidence gate|non-evidence|validation stopping|selection protocol|audit exclusion|untrained UKF baseline|comparator" docs/plans/bayesfilter-highdim-zhao-cui-p77-phase2-budget-tuning-protocol-subplan-2026-06-19.md
rg -n "wrong baselines|proxy metrics|missing stop conditions|unfair comparisons|hidden assumptions|stale context|environment mismatch|artifact adequacy|under-budget mechanics smokes" docs/plans/bayesfilter-highdim-zhao-cui-p77-phase1-objective-split-contract-result-2026-06-19.md
git diff --check -- docs/plans/bayesfilter-highdim-zhao-cui-p77-phase1-objective-split-contract-subplan-2026-06-19.md docs/plans/bayesfilter-highdim-zhao-cui-p77-phase1-objective-split-contract-result-2026-06-19.md docs/plans/bayesfilter-highdim-zhao-cui-p77-phase2-budget-tuning-protocol-subplan-2026-06-19.md docs/plans/bayesfilter-highdim-zhao-cui-p77-corrected-metric-training-master-program-2026-06-19.md docs/plans/bayesfilter-highdim-zhao-cui-p77-visible-gated-execution-runbook-2026-06-19.md docs/plans/bayesfilter-highdim-zhao-cui-p77-visible-execution-ledger-2026-06-19.md docs/plans/bayesfilter-highdim-zhao-cui-p77-claude-review-ledger-2026-06-19.md docs/plans/bayesfilter-highdim-zhao-cui-p77-visible-stop-handoff-2026-06-19.md
```

Review:

- Claude read-only review of Phase 1 result and Phase 2 subplan.
- Repair loop to convergence within at most five rounds; if not converged,
  write blocker/handoff and stop.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Scientific/engineering question | What objective and data split must govern P77 training so later evidence cannot be contaminated by proxy metrics or leakage? |
| Exact baseline/comparator | UKF-initialized untrained TT evaluated with corrected target-only CE on the same validation/replay/audit metric roles. |
| Primary criterion | Phase 1 result freezes the training loss, corrected validation CE, replay diagnostic, audit final check, seed/data roles, non-leakage rules, comparator, and nonclaim boundaries before any training. |
| Veto diagnostics | Missing role split, audit used for tuning/selection/stopping, training loss treated as primary fit quality, raw residuals promoted to pass criterion, source-prefit revival, under-budget evidence allowance, implementation/training action during Phase 1. |
| Explanatory only | Discussion of possible optimizer/hyperparameter families, P76 CE values, and mechanics-smoke roles. |
| What will not be concluded | No training improvement, no hyperparameter choice, no budget approval, no implementation surface, no lower-gate repair, no validation/HMC readiness, no scaling. |
| Artifact preserving result | Phase 1 result and Phase 2 budget/tuning subplan. |

## Required Mathematical Content

Phase 1 must define:

- the training objective actually optimized, with its relation to
  \(\rho_\theta\), \(Z_\theta\), and generated training batches;
- the corrected validation CE:
  \[
    \widehat{\mathcal L}_{\rm val}(\theta)
    =
    -\sum_i \alpha_i^{\rm val}\log \rho_\theta(z_i)+\log Z_\theta,
    \qquad
    \alpha_i^{\rm val}
    =
    \frac{w_i s_i^2}{\sum_j w_j s_j^2};
  \]
- the UKF-initialized untrained comparator \(\theta_0\);
- a validation role for tuning/stopping, a replay role for robustness, and an
  audit role for final-only checks;
- the rule that audit cannot select hyperparameters, stopping time, rank,
  degree, sample count, learning rate, or optimizer settings;
- the rule that \(N_{\rm train}\ge20P_\theta\) is required before any training
  evidence claim.
- the rule that random initialization, calibrated-constant initialization, and
  source-route prefit are failed historical routes only.  They must not be
  revived as live candidates, comparators, tuning anchors, baselines, fallback
  options, or promotion references in Phase 2.

## Required Phase 2 Draft Content

The Phase 2 subplan drafted at Phase 1 close must include at least:

- a parameter-count source of truth for \(P_\theta\), including the formula
  \[
    P_\theta=\sum_{k=1}^d r_{k-1} b_k r_k,
  \]
  the current \(d=36\), degree-2/rank-4 calculation
  \(P_\theta=1656\), and a recomputation rule if dimension, degree, basis
  count, rank tuple, or frozen/trainable mask changes;
- budget arithmetic for the hard evidence gate
  \(N_{\rm train}\ge 20P_\theta\), including why `1024 x 40 = 40960`
  fresh training samples exceeds the current `33120` minimum, and a separate
  label for any under-budget mechanics smoke as non-evidence;
- a predeclared tuning protocol for learning rate, number of batches,
  optimizer settings, stopping, and selection that uses validation data only
  and records whether replay diagnostics can veto or only explain;
- explicit audit exclusion: audit samples may be used only after all
  hyperparameters, stopping time, rank, degree, sample budget, learning rate,
  optimizer settings, and candidate-selection rules are frozen;
- comparator/reporting fields for the untrained UKF baseline on the same
  corrected validation/replay/audit roles;
- explicit preservation that random, calibrated-constant, and source-prefit
  routes remain failed historical routes, not live baselines.

## Forbidden Claims/Actions

- Do not edit implementation code.
- Do not run training, generated-sample diagnostics, or smokes.
- Do not construct an optimizer or call `train_step`.
- Do not tune hyperparameters.
- Do not choose final hyperparameters.
- Do not weaken the \(20P_\theta\) budget rule.
- Do not treat training loss or residuals as primary fit quality.
- Do not revive random initialization, calibrated-constant initialization, or
  source-route prefit as live routes, baselines, comparators, fallback
  candidates, tuning anchors, or promotion references.
- Do not claim training improvement, lower-gate repair, validation/HMC
  readiness, scaling, source-faithfulness, or final policy.

## Exact Next-Phase Handoff Conditions

Phase 2 may begin only if:

- Phase 1 result exists;
- Claude agrees Phase 1 execution/result;
- Phase 2 subplan exists and freezes parameter-count, budget, and tuning
  protocol work;
- no implementation/training/GPU/network/default action is needed to begin
  Phase 2.

## Stop Conditions

Stop if:

- Phase 1 cannot define a clean data-role split;
- corrected heldout CE cannot remain primary;
- audit cannot be made final-only;
- the \(20P_\theta\) rule becomes ambiguous or weakened;
- Claude identifies a material blocker that cannot be repaired within five
  rounds;
- continuing would require implementation edits, training, generated samples,
  GPU/CUDA, network/package operations, or default changes.

## Skeptical Plan Audit

Before executing Phase 1, Codex must record the full skeptical audit required
by the runbook in the Phase 1 result.  The audit must explicitly answer:

- wrong baselines: the only live comparator is the UKF-initialized untrained
  candidate; random, calibrated-constant, and source-prefit routes remain
  failed historical routes;
- proxy metrics: training loss, residuals, replay values, mechanics smokes,
  and P76 CE values cannot become promotion criteria;
- missing stop conditions: audit leakage, under-budget evidence, implementation
  action, or unconverged Claude review stop the phase;
- unfair comparisons: trained and untrained candidates must use the same
  corrected CE formula and data-role definitions;
- hidden assumptions: \(P_\theta\), batch count, role split, and audit
  exclusion must be written before training;
- stale context: P76 is metric plumbing and prerequisite context, not a
  training-evidence result;
- environment mismatch: Phase 1 is docs-only and must not depend on CPU/GPU,
  generated samples, optimizer state, or package/network state;
- artifact adequacy: the Phase 1 result and Phase 2 subplan must contain enough
  detail to prevent arbitrary tuning or under-budget promotion;
- under-budget mechanics smokes: any later smoke below \(20P_\theta\) is
  mechanics-only and cannot tune, select, promote, or support a training
  evidence claim.

The main risk is designing a training protocol that still lets validation,
replay, audit, failed historical routes, or residual proxies blur together.
Phase 1 must make the roles boringly explicit before any code or experiment
moves.
