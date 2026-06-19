# P77 Phase 2 Subplan: Parameter Count, Budget, And Tuning Protocol

metadata_date: 2026-06-19
status: DRAFT_PENDING_PHASE1_EXECUTION_REVIEW
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p77-corrected-metric-training-master-program-2026-06-19.md
runbook: docs/plans/bayesfilter-highdim-zhao-cui-p77-visible-gated-execution-runbook-2026-06-19.md
previous_result: docs/plans/bayesfilter-highdim-zhao-cui-p77-phase1-objective-split-contract-result-2026-06-19.md
phase: 2
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Phase Objective

Make the P77 fixed-branch regression/training budget and hyperparameter
tuning protocol operational before any implementation or training phase.

Phase 2 must eliminate arbitrary choices by freezing:

- the source of truth for \(P_\theta\);
- the \(N_{\rm train}\ge20P_\theta\) evidence gate;
- the distinction between mechanics smokes and training evidence;
- the validation-only tuning, stopping, and selection protocol;
- the replay role;
- audit exclusion;
- comparator/reporting fields for the untrained UKF baseline.

Phase 2 is design-only.  It must not edit implementation code, construct an
optimizer, call `train_step`, generate samples, run training, run a mechanics
smoke, use GPU/CUDA, install packages, use network, or change defaults.

## Entry Conditions Inherited From Phase 1

Phase 2 may begin only if:

- Phase 1 result exists;
- Claude agrees Phase 1 execution/result and this Phase 2 subplan is adequate
  for execution;
- the Phase 1 contract preserves corrected target-only validation CE as the
  primary fit metric;
- the only live comparator is the UKF-initialized untrained TT candidate;
- random initialization, calibrated-constant initialization, and source-route
  prefit remain failed historical routes only;
- audit remains final-only;
- no implementation or training action is needed to execute Phase 2.

## Required Artifacts

Phase 2 must produce:

- Phase 2 result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p77-phase2-budget-tuning-protocol-result-2026-06-19.md`;
- drafted Phase 3 subplan:
  `docs/plans/bayesfilter-highdim-zhao-cui-p77-phase3-implementation-surface-subplan-2026-06-19.md`;
- updated P77 master program, runbook, execution ledger, Claude review ledger,
  and stop handoff.

## Required Checks/Tests/Reviews

Prechecks:

```bash
rg -n "PHASE1|training objective|corrected target-only|UKF-initialized untrained|20P|33120|40960|random|calibrated-constant|source-prefit|audit final" docs/plans/bayesfilter-highdim-zhao-cui-p77-phase1-objective-split-contract-result-2026-06-19.md docs/plans/bayesfilter-highdim-zhao-cui-p77-phase2-budget-tuning-protocol-subplan-2026-06-19.md
rg -n "P76CorrectedHeldoutMetricBatch|corrected_heldout_density_metric|P75ObjectiveBatch|train_step|make_adam_optimizer" bayesfilter/highdim/stochastic_density_training.py
```

Documentation checks:

```bash
rg -n "P_theta|parameter count|rank|degree|basis|trainable mask|recompute|1656|33120|40960|20P|budget arithmetic|evidence gate|non-evidence|mechanics smoke" docs/plans/bayesfilter-highdim-zhao-cui-p77-phase2-budget-tuning-protocol-result-2026-06-19.md docs/plans/bayesfilter-highdim-zhao-cui-p77-phase3-implementation-surface-subplan-2026-06-19.md
rg -n "learning rate|batch count|validation stopping|selection protocol|audit exclusion|replay veto|untrained UKF baseline|comparator|corrected validation CE|random|calibrated-constant|source-prefit" docs/plans/bayesfilter-highdim-zhao-cui-p77-phase2-budget-tuning-protocol-result-2026-06-19.md docs/plans/bayesfilter-highdim-zhao-cui-p77-phase3-implementation-surface-subplan-2026-06-19.md
rg -n "wrong baselines|proxy metrics|missing stop conditions|unfair comparisons|hidden assumptions|stale context|environment mismatch|artifact adequacy|under-budget mechanics smokes" docs/plans/bayesfilter-highdim-zhao-cui-p77-phase2-budget-tuning-protocol-result-2026-06-19.md
git diff --check -- docs/plans/bayesfilter-highdim-zhao-cui-p77-phase2-budget-tuning-protocol-subplan-2026-06-19.md docs/plans/bayesfilter-highdim-zhao-cui-p77-phase2-budget-tuning-protocol-result-2026-06-19.md docs/plans/bayesfilter-highdim-zhao-cui-p77-phase3-implementation-surface-subplan-2026-06-19.md docs/plans/bayesfilter-highdim-zhao-cui-p77-corrected-metric-training-master-program-2026-06-19.md docs/plans/bayesfilter-highdim-zhao-cui-p77-visible-gated-execution-runbook-2026-06-19.md docs/plans/bayesfilter-highdim-zhao-cui-p77-visible-execution-ledger-2026-06-19.md docs/plans/bayesfilter-highdim-zhao-cui-p77-claude-review-ledger-2026-06-19.md docs/plans/bayesfilter-highdim-zhao-cui-p77-visible-stop-handoff-2026-06-19.md
```

Review:

- Claude read-only review of Phase 2 result and Phase 3 subplan.
- Repair loop to convergence within at most five rounds; if not converged,
  write blocker/handoff and stop.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Scientific/engineering question | Can P77 freeze a non-arbitrary budget and tuning protocol that makes a later training run scientifically interpretable? |
| Exact baseline/comparator | UKF-initialized untrained TT candidate evaluated by corrected validation/replay/audit CE under the same role definitions as trained candidates. |
| Primary criterion | Phase 2 result defines \(P_\theta\), recomputation rule, \(20P_\theta\) evidence gate, first proper budget, validation-only tuning/stopping/selection, replay role, audit exclusion, failed-route fences, and required Phase 3 implementation-surface fields. |
| Veto diagnostics | Arbitrary or post-hoc hyperparameter choices, under-budget evidence allowance, audit tuning, replay hidden-selection leakage, random/constant/source-prefit revival, implementation/training action during Phase 2, or failure to specify comparator/reporting fields. |
| Explanatory only | Candidate learning-rate families, possible batch-size/runtime tradeoffs, mechanics-smoke needs, and P76 CE values. |
| What will not be concluded | No training improvement, no final hyperparameter selection from data, no implementation result, no training-run approval, no lower-gate repair, no validation/HMC readiness, no scaling. |
| Artifact preserving result | Phase 2 result and Phase 3 implementation-surface subplan. |

## Required Mathematical And Operational Content

Phase 2 must define all of the following.

### Parameter Count Source Of Truth

For a dense trainable TT with basis counts \(b_k\) and rank tuple
\((r_0,\ldots,r_d)\),
\[
  P_\theta=\sum_{k=1}^d r_{k-1}b_kr_k.
\]

For the current \(d=36\), degree-2 product basis with \(b_k=3\), and rank
tuple \((1,4,\ldots,4,1)\),
\[
  P_\theta
  =
  1\cdot3\cdot4
  +
  34\cdot4\cdot3\cdot4
  +
  4\cdot3\cdot1
  =
  1656.
\]

If dimension, basis count, degree, rank tuple, trainable/frozen core mask, or
parameterization changes, Phase 2 must require recomputing \(P_\theta\) from
the actual trainable scalar variables before any evidence run.

### Budget Arithmetic

The hard evidence gate is
\[
  N_{\rm train}\ge20P_\theta.
\]

For \(P_\theta=1656\),
\[
  20P_\theta=33120.
\]

With `batch_size = 1024`, the minimum evidence batch count is
\[
  \left\lceil33120/1024\right\rceil=33.
\]

The preferred first proper diagnostic budget is `1024 x 40 = 40960` fresh
training samples.  This is the minimum budget that may support a P77 training
evidence claim for the current candidate unless Phase 2 justifies a larger
budget.  It is not approval to run the command.

### Tuning And Stopping Protocol

Phase 2 must freeze a validation-only protocol for:

- learning-rate candidates;
- batch count or epoch count;
- gradient clipping;
- regularization weights;
- stopping rule;
- candidate-selection rule;
- replay veto or explanatory role.

This must be written as a validation stopping and selection protocol.  The
protocol must state which values are fixed a priori, which values may be
selected by corrected validation CE, and which values remain non-evidence
mechanics settings.

The protocol must explain how each candidate set was chosen before seeing new
training results.  Audit cannot tune or select any of these values.

### Required Comparator Fields

Every later proper training diagnostic must report:

- untrained UKF baseline corrected validation CE;
- trained candidate corrected validation CE;
- validation improvement by the predeclared rule;
- replay corrected CE for both candidates;
- audit corrected CE for both candidates only after all choices are frozen;
- \(P_\theta\), \(N_{\rm train}\), batch size, batch count, fresh-sample
  generation rule, seeds, optimizer settings, gradient clipping, and
  regularization weights.

## Forbidden Claims/Actions

- Do not edit implementation code.
- Do not run training, generated-sample diagnostics, or mechanics smokes.
- Do not construct an optimizer or call `train_step`.
- Do not tune hyperparameters from new results.
- Do not choose final hyperparameters based on audit or replay leakage.
- Do not weaken the \(20P_\theta\) evidence gate.
- Do not treat training loss, residuals, replay values, P76 CE values, or
  mechanics-smoke values as primary fit quality.
- Do not revive random initialization, calibrated-constant initialization, or
  source-route prefit as live routes, baselines, comparators, fallback
  candidates, tuning anchors, or promotion references.
- Do not claim training improvement, lower-gate repair, validation/HMC
  readiness, scaling, source-faithfulness, or final policy.

## Exact Next-Phase Handoff Conditions

Phase 3 may begin only if:

- Phase 2 result exists;
- Claude agrees Phase 2 execution/result;
- Phase 3 subplan exists and scopes implementation-surface work without
  allowing training evidence;
- Phase 3 code edits are limited to the scoped P77 runner/test surface named in
  the reviewed Phase 3 subplan;
- no training, generated samples, GPU/CUDA, network/package operation, default
  change, or large run is needed to begin Phase 3.

## Stop Conditions

Stop if:

- \(P_\theta\) cannot be counted unambiguously;
- the \(20P_\theta\) gate cannot be enforced;
- validation-only tuning/stopping/selection cannot be specified without
  arbitrariness;
- audit cannot remain final-only;
- failed historical routes are revived as live baselines;
- Phase 3 would require implementation edits outside the reviewed scoped P77
  runner/test surface;
- Claude identifies a material blocker that cannot be repaired within five
  rounds;
- continuing would require training, generated samples, GPU/CUDA,
  network/package operations, default changes, or a large run.

## Skeptical Plan Audit

Before executing Phase 2, Codex must record a skeptical audit covering wrong
baselines, proxy metrics, missing stop conditions, unfair comparisons, hidden
assumptions, stale context, environment mismatch, artifact adequacy, and
under-budget mechanics smokes.

The central risk is that "hyperparameter tuning" becomes arbitrary after
seeing results.  Phase 2 must make the tuning ladder small, justified,
validation-only, and auditable before implementation or training.
