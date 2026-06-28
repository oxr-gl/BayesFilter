# P04 Subplan: Closeout And Default-Review Classification

Date: 2026-06-23

## Phase Objective

Synthesize P01-P03 evidence and classify the fixed-policy promotion-stress lane
without changing defaults or overstating scientific claims.

## Entry Conditions Inherited From Previous Phase

- P01 replicated high-N gate passed or wrote a valid failure result.
- P02 full-history/memory gate passed if reached.
- P03 Nystrom-specific gradient mechanics gate passed if reached.
- Claude review converged for material HMC/default-boundary interpretations.

## Required Artifacts

- P04 closeout result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-fixed-policy-promotion-stress-p04-closeout-result-2026-06-23.md`
- Updated execution ledger:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-fixed-policy-promotion-stress-visible-execution-ledger-2026-06-23.md`
- Updated stop handoff if a stop condition fired:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-fixed-policy-promotion-stress-visible-stop-handoff-2026-06-23.md`
- Updated Claude review ledger:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-fixed-policy-promotion-stress-claude-review-ledger-2026-06-23.md`

## Required Checks, Tests, And Reviews

- Verify required phase result files exist for all reached phases.
- Verify every referenced benchmark JSON/Markdown/log exists.
- Verify no result file claims default change, HMC readiness, posterior
  correctness, statistical superiority, or broad robustness.
- Write closeout decision table and inference-status table.
- Include run manifest summary across reached phases.
- Include negative/blocked result classification if any phase failed.
- Claude Opus max-effort read-only review is required for final closeout.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | What classification is justified by the fixed-policy promotion-stress evidence? |
| Baseline/comparator | Reached phase artifacts and their paired streaming TF32 comparators. |
| Primary pass criterion | Closeout accurately reflects reached phase gates, preserves nonclaims, and receives Claude read-only agreement for boundary safety. |
| Veto diagnostics | Missing result artifact, unsupported default/HMC/posterior/superiority claim, phase result contradiction, Claude/Codex non-convergence after five rounds. |
| Explanatory diagnostics | Phase runtimes, descriptive benchmark metrics, review comments. |
| Not concluded | No default change unless a separate human/default-policy decision is made; no HMC readiness; no posterior correctness; no statistical superiority. |
| Artifact | P04 closeout result and ledgers. |

## Forbidden Claims/Actions

- Do not change defaults.
- Do not claim the fixed policy is globally robust.
- Do not rank viable methods by descriptive-only metrics.
- Do not claim HMC readiness from gradient mechanics evidence.
- Do not bury failed or blocked phase evidence.

## Exact Next-Phase Handoff Conditions

There is no next phase in this visible runbook. If all phases pass, hand off as
`PROMOTION_STRESS_PASSED_FOR_HUMAN_DEFAULT_REVIEW`. If a phase fails with valid
artifacts, hand off as `FIXED_POLICY_PROMOTION_STRESS_FAILED_OR_REPAIR_NEEDED`.
If a phase is invalid or blocked, hand off as `BLOCKED_REQUIRES_HUMAN_DIRECTION`.

## Stop Conditions

- Final classification would require a default-policy decision.
- Required phase evidence is missing or contradictory.
- Claude review does not converge after five rounds for material boundary
  issues.

## Skeptical Plan Audit

Closeout must distinguish candidate failure from research-direction rejection,
and must distinguish promotion-stress pass from default-policy change.

Audit status: `READY_AFTER_P03_OR_FAILURE_CLASSIFICATION`.
