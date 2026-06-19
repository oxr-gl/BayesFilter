# P76 Phase 7 Subplan: Fit-Diagnostic Triage

status: SUPERSEDED_BY_PHASE6B_CORRECTED_EVIDENCE_CONTRACT_DO_NOT_EXECUTE
superseded_by: docs/plans/bayesfilter-highdim-zhao-cui-p76-phase7-fit-diagnostic-subplan-v2-2026-06-18.md

## Supersession Notice

This original Phase 7 draft is retained for provenance only.  Do not execute
it.  Phase 6b corrected the post-Phase-6 evidence contract and requires the
successor subplan:

- `docs/plans/bayesfilter-highdim-zhao-cui-p76-phase7-fit-diagnostic-subplan-v2-2026-06-18.md`

The corrected gate requires target-only heldout density cross-entropy, explicit
sample-to-parameter minima, train/validation/audit separation, predeclared
tuning rules, and visible blocking of raw or sign/scale-adjusted square-root
residual promotion.

metadata_date: 2026-06-18
old_status_before_supersession: DRAFT_CLAUDE_REVIEW_PENDING
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p76-ukf-warm-start-minibatch-master-program-2026-06-18.md
runbook: docs/plans/bayesfilter-highdim-zhao-cui-p76-visible-gated-execution-runbook-2026-06-18.md
previous_result: docs/plans/bayesfilter-highdim-zhao-cui-p76-phase6-bounded-minibatch-pilot-result-2026-06-18.md
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Phase Objective

Diagnose the meaning of the Phase 6 fit-quality failure without running a
large pilot.  The immediate task is to distinguish:

1. density-space failure;
2. square-root-amplitude diagnostic mismatch;
3. insufficient capacity/sample/step budget;
4. optimizer or scaling instability;
5. target-generation or weighting pathologies.

Phase 7 is diagnostic and planning-oriented.  It must not claim the algorithm
is repaired or rejected.

## Entry Conditions Inherited From Phase 6

Phase 7 may begin only if:

- the Phase 6 result exists;
- the Phase 6 pilot JSON parses;
- `ukf_frame_bridge.status == "pass"`;
- finite loss, gradient, rho, normalizer, and log-density flags are true;
- Phase 6 result preserves that audit residual magnitudes are explanatory
  under the Phase 6 evidence contract;
- Claude agrees the Phase 6 interpretation and this Phase 7 subplan are
  bounded.

## Required Artifacts

Phase 7 must produce:

- diagnostic result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p76-phase7-fit-diagnostic-result-2026-06-18.md`;
- if a script is needed, a dedicated opt-in diagnostic script:
  `scripts/p76_fit_diagnostic_triage.py`;
- if a script is added, focused tests for script-level invariants;
- refreshed execution, review, runbook, and stop-handoff records;
- either a Phase 8 subplan or a stop handoff.

## Required Checks/Tests/Reviews

Prechecks:

```bash
python -m json.tool docs/plans/bayesfilter-highdim-zhao-cui-p76-phase6-bounded-minibatch-pilot-2026-06-18.json
rg -n "ukf_frame_bridge|overall_status|audit_status_not_phase6_veto|rms_relative|max_relative|rho_max|normalizer|completed_batches|source_route_prefit_used|cpu_only" docs/plans/bayesfilter-highdim-zhao-cui-p76-phase6-bounded-minibatch-pilot-2026-06-18.json docs/plans/bayesfilter-highdim-zhao-cui-p76-phase6-bounded-minibatch-pilot-result-2026-06-18.md
```

If Phase 7 adds a script:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q scripts/p76_fit_diagnostic_triage.py tests/highdim/test_p76_bounded_ukf_minibatch_pilot.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p76_bounded_ukf_minibatch_pilot.py tests/highdim/test_p76_ukf_initializer.py tests/highdim/test_p75_stochastic_density_training.py
```

Review:

- Claude read-only review of the Phase 6 interpretation and Phase 7 result;
- loop to convergence or max 5 rounds for the same material blocker.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Scientific/engineering question | Why did the Phase 6 degree-2/rank-4/20-batch UKF-frame pilot have enormous audit square-root residuals despite a passing UKF-frame bridge and finite training? |
| Exact baseline/comparator | Phase 6 JSON/result only. Historical P75 failures are context, not live comparators. |
| Primary criterion | Produce a bounded diagnostic classification and the smallest justified next action. |
| Diagnostics that can veto | Treating square-root residuals as lower-gate repair/rejection; using audit data for training/tuning; changing defaults; launching a large pilot; GPU/CUDA use; source-route prefit revival; nonfinite diagnostic quantities. |
| Explanatory only | Density-space heldout loss estimates, square-root residuals with optimal scale/sign, target dynamic range, alpha/weight concentration, parameter/sample counts, optimizer trace, rho/normalizer ranges. |
| What will not be concluded | No lower-gate repair, no validation/HMC readiness, no scaling, no final architecture/sample policy, no evidence against UKF as an idea. |
| Artifact preserving result | Phase 7 diagnostic result and any opt-in diagnostic JSON if a script is needed. |

## Required Diagnostic Questions

Phase 7 must answer, at least qualitatively:

- Are the Phase 6 audit residuals measuring \(h_\theta\) against a target while
  the training objective optimizes normalized \(p_\theta=\rho_\theta/Z_\theta\)?
- Do density-space diagnostics tell the same story as the square-root
  residuals?
- Does allowing an optimal scalar and sign for \(h_\theta\) materially reduce
  the square-root residuals?
- How many raw trainable TT parameters were used, and how does that compare
  with the number of fresh samples and optimizer steps?
- Are target values, cross-entropy weights, or alpha weights highly
  concentrated?
- Are rho values or the normalizer in a range that suggests scale instability?

## Forbidden Claims/Actions

- Do not use GPU/CUDA.
- Do not run a large mini-batch pilot.
- Do not change defaults.
- Do not install or fetch packages.
- Do not use network.
- Do not launch detached agents.
- Do not use audit samples for training, stopping, or hyperparameter
  selection.
- Do not revive random, calibrated constant, or source-route prefit as live
  repair ladders.
- Do not claim lower-gate repair, validation readiness, HMC readiness,
  source-faithfulness, scaling, or final rank/sample policy.

## Exact Next-Phase Handoff Conditions

Phase 8 may begin only if:

- Phase 7 result exists;
- Claude agrees the diagnostic interpretation is bounded;
- the next action is a specific reviewed subplan;
- any larger pilot, GPU use, default change, or new objective/regularizer has
  separate user approval.

## Stop Conditions

Stop if:

- Phase 6 JSON cannot be parsed or contradicts the Phase 6 result;
- the diagnostic cannot distinguish density-space failure from square-root
  diagnostic mismatch without a larger run;
- the only next action would be a large pilot or GPU run without separate
  approval;
- Claude identifies a material blocker that cannot be repaired within five
  rounds.

## Skeptical Plan Audit

The main risk is interpreting a proxy diagnostic as an algorithmic conclusion.
Phase 7 therefore must first audit whether the residual diagnostic is aligned
with the density objective before attributing the failure to capacity,
samples, optimizer settings, or the UKF idea.
