# P76 Phase 7 v2 Subplan: Corrected Fit-Diagnostic Protocol

metadata_date: 2026-06-18
status: READY_AFTER_PHASE6B_CLAUDE_AGREE
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p76-ukf-warm-start-minibatch-master-program-2026-06-18.md
runbook: docs/plans/bayesfilter-highdim-zhao-cui-p76-visible-gated-execution-runbook-2026-06-18.md
previous_result: docs/plans/bayesfilter-highdim-zhao-cui-p76-phase6b-corrected-evidence-contract-result-2026-06-18.md
supersedes: docs/plans/bayesfilter-highdim-zhao-cui-p76-phase7-fit-diagnostic-subplan-2026-06-18.md
phase: 7
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Phase Objective

Convert the Phase 6b corrected evidence contract into a concrete diagnostic
protocol for the next P76 step without launching that diagnostic yet.

Phase 7 v2 is docs/protocol planning only.  It must decide what minimal future
artifact would be needed to compute density-aligned heldout metrics, training
loss checks, validation rules, and sample-budget gates.  It must not run a new
diagnostic, generate new samples, edit implementation code, tune
hyperparameters, or reinterpret the existing Phase 6 run as fit-quality
evidence.

## Entry Conditions Inherited From Phase 6b

Phase 7 v2 may begin only if:

- Phase 6b result exists;
- the legacy Phase 7 draft contains
  `SUPERSEDED_BY_PHASE6B_CORRECTED_EVIDENCE_CONTRACT_DO_NOT_EXECUTE`;
- the legacy Phase 7 draft points to this v2 subplan;
- Phase 6 is reclassified as mechanics-only;
- the corrected density-aligned heldout metric is primary for future
  fit-quality interpretation;
- raw square-root residuals, including sign/scale-adjusted versions, are
  secondary and explanatory only;
- the minimum sample-to-parameter rule is recorded as necessary but not
  sufficient;
- Claude agrees the Phase 6b execution artifacts.

## Required Artifacts

Phase 7 v2 must produce:

- Phase 7 v2 result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p76-phase7-fit-diagnostic-result-v2-2026-06-18.md`;
- either a Phase 8 subplan or a stop handoff;
- updates to the P76 runbook, execution ledger, Claude review ledger, and stop
  handoff.

Phase 7 v2 may propose a later implementation or diagnostic artifact, but it
must not create or execute it.  Any proposed later artifact must have its own
reviewed subplan and approval boundary.

## Required Checks/Tests/Reviews

Prechecks:

```bash
python -m json.tool docs/plans/bayesfilter-highdim-zhao-cui-p76-phase6-bounded-minibatch-pilot-2026-06-18.json
rg -n "SUPERSEDED_BY_PHASE6B_CORRECTED_EVIDENCE_CONTRACT_DO_NOT_EXECUTE" docs/plans/bayesfilter-highdim-zhao-cui-p76-phase7-fit-diagnostic-subplan-2026-06-18.md
rg -n "mechanics-only|density-aligned heldout|16560|minimum necessary|target-only weights|not the approved primary heldout metric" docs/plans/bayesfilter-highdim-zhao-cui-p76-phase6b-corrected-evidence-contract-result-2026-06-18.md
rg -n "weighted_empirical_cross_entropy_weights|tau \\* q0|raw = batch.weights" bayesfilter/highdim/stochastic_density_training.py
```

Execution checks after drafting the Phase 7 v2 result:

```bash
rg -n "docs-only|density-aligned heldout|alpha_i|target-only|not approved primary heldout metric|train/validation/audit|minimum necessary|no implementation edits|no new diagnostic" docs/plans/bayesfilter-highdim-zhao-cui-p76-phase7-fit-diagnostic-result-v2-2026-06-18.md
git diff --check -- docs/plans/bayesfilter-highdim-zhao-cui-p76-phase7-fit-diagnostic-subplan-v2-2026-06-18.md docs/plans/bayesfilter-highdim-zhao-cui-p76-phase7-fit-diagnostic-result-v2-2026-06-18.md docs/plans/bayesfilter-highdim-zhao-cui-p76-visible-gated-execution-runbook-2026-06-18.md docs/plans/bayesfilter-highdim-zhao-cui-p76-visible-execution-ledger-2026-06-18.md docs/plans/bayesfilter-highdim-zhao-cui-p76-claude-review-ledger-2026-06-18.md docs/plans/bayesfilter-highdim-zhao-cui-p76-visible-stop-handoff-2026-06-18.md
```

Review:

- Claude read-only review of the Phase 7 v2 result and any proposed Phase 8
  subplan.
- Loop repair to convergence or max five rounds for the same material blocker.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Scientific/engineering question | What exact future diagnostic surface is needed to determine whether P76 fitting is failing because of density mismatch, sample/capacity limits, optimizer/tuning limits, or target-generation pathologies, under the corrected Phase 6b metric contract? |
| Exact baseline/comparator | Existing Phase 6 mechanics JSON/result and Phase 6b corrected contract only. Historical P75 failures remain boundary context, not live candidate methods. |
| Primary criterion | Produce a reviewed diagnostic protocol for a later phase that uses target-only heldout density cross-entropy as primary, keeps train/validation/audit roles disjoint, predeclares tuning, and refuses fit-quality claims below the sample-budget minimum. |
| Veto diagnostics | Any plan to execute a diagnostic in Phase 7 v2; implementation-code edits; new generated samples; use of the current `weighted_empirical_cross_entropy_weights` helper as the primary heldout metric without a reviewed target bridge; audit leakage; post-hoc target weights; post-hoc hyperparameters; raw or sign/scale-adjusted square-root residual promotion; GPU/CUDA; network; package installation; default changes; source-prefit revival. |
| Explanatory only | Phase 6 loss trace, gradient norm, alpha range, rho range, normalizer, square-root residuals, line residuals, runtime, and parameter/sample count. |
| What will not be concluded | No UKF success/rejection, no fit-quality pass/fail, no lower-gate repair, no validation/HMC readiness, no scaling, no final rank/sample policy. |
| Artifact preserving result | Phase 7 v2 result and either a Phase 8 subplan or stop handoff. |

## Corrected Diagnostic Requirements

The future diagnostic proposed by Phase 7 v2 must be able to compute, for a
heldout batch \(B=\{(z_i,w_i,s_i)\}_{i=1}^n\),
\[
  u_i=s_i^2,\qquad
  \alpha_i^B=\frac{w_i u_i}{\sum_j w_j u_j},
\]
and
\[
  \mathcal L_B(\theta)
  =
  -\sum_i\alpha_i^B\log\rho_\theta(z_i)+\log Z_\theta .
\]

It must explicitly state:

- how \(z_i,w_i,s_i\) are generated;
- why the batch is train, validation, or audit/test;
- how sample-stream disjointness is enforced;
- how \(\alpha_i^B\) is computed without \(h_\theta\), \(\rho_\theta\),
  \(Z_\theta\), training loss, validation loss, audit/test outcomes, or
  post-hoc model terms;
- how nonfinite or zero target mass vetoes the batch;
- how the current helper alpha rule with \(s_i^2+\tau q_0(z_i)\) is avoided or
  explicitly bridged by a reviewed target change.

## Capacity And Tuning Requirements

Any future substantive fit-quality pilot proposed after Phase 7 v2 must
satisfy:

- \(N_{\rm train}\ge 10N_\theta\), with \(N_\theta\) computed from the actual
  degree, dimension, and ranks;
- a separately justified validation size;
- a separately justified one-touch audit/test size;
- finite candidate sets or inherited values for learning rate,
  regularization, gradient clipping, batch size, batch count, degree, rank,
  validation cadence, and stopping rule;
- a validation-selection rule that cannot inspect audit/test metrics;
- instability vetoes for nonfinite loss, gradient, rho, normalizer, log
  density, invalid target mass, or audit leakage.

The \(10N_\theta\) rule is necessary, not sufficient.  Higher sample budgets or
larger capacity may still be needed for complex geometry.

## Forbidden Claims/Actions

- Do not edit implementation code in Phase 7 v2.
- Do not run a new training, diagnostic, or pilot command in Phase 7 v2 beyond
  local documentation checks and JSON parsing.
- Do not generate new train, validation, audit, or line samples in Phase 7 v2.
- Do not use GPU/CUDA.
- Do not install or fetch packages.
- Do not use network.
- Do not launch detached agents.
- Do not change defaults.
- Do not revive random, calibrated constant, or source-route prefit as live
  repair candidates.
- Do not use audit/test samples for training, stopping, hyperparameter
  selection, or metric selection.
- Do not use the current helper alpha rule as the primary heldout metric
  without a reviewed target bridge.
- Do not claim lower-gate repair, validation readiness, HMC readiness, scaling,
  source-faithfulness, final rank/sample policy, UKF success, or UKF rejection.

## Exact Next-Phase Handoff Conditions

Phase 8 may begin only if:

- Phase 7 v2 result exists;
- Phase 7 v2 result states a concrete next diagnostic or stop decision;
- any next diagnostic has a dedicated reviewed subplan;
- any implementation edit, generated-sample diagnostic, tuning run, large run,
  GPU/CUDA use, default change, or target change has separate approval;
- Claude agrees the Phase 7 v2 result and next subplan.

## Stop Conditions

Stop if:

- the Phase 6 JSON cannot be parsed;
- the legacy Phase 7 supersession marker is missing;
- the corrected density metric cannot be operationalized without an
  implementation edit not approved for this phase;
- a future diagnostic would require new generated samples before a reviewed
  subplan and approval;
- Claude identifies a material blocker that cannot be repaired within five
  rounds;
- the next phase would still permit post-hoc target weights, post-hoc
  hyperparameters, audit leakage, or square-root residual promotion.

## Skeptical Plan Audit

The main risk is again proxy promotion: a convenient residual, helper loss, or
too-small finite run could be mistaken for fit evidence.  Phase 7 v2 prevents
that by keeping itself docs-only and requiring any future diagnostic to use the
Phase 6b density-aligned metric, sample-budget rule, and split/tuning protocol
before execution.
