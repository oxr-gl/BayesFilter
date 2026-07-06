# P04 Subplan: Closeout

Date: 2026-06-23

## Phase Objective

Classify the N8192 paired-drift diagnostic lane without changing defaults or
overstating scientific claims.

## Entry Conditions Inherited From Previous Phase

- P01 result exists.
- P02/P03 results exist if reached.

## Required Artifacts

- P04 closeout:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-n8192-paired-drift-diagnostic-p04-closeout-result-2026-06-23.md`
- Updated ledgers and stop handoff.

## Required Checks, Tests, And Reviews

- Verify reached phase artifacts exist.
- Verify no unsupported claims.
- Claude final read-only review required if P02/P03 are reached or if closeout
  makes material repair-direction claims.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | What is the justified classification of the N8192 paired drift? |
| Baseline/comparator | Reached phase artifacts. |
| Primary pass criterion | Closeout accurately reflects reached phases and preserves nonclaims. |
| Veto diagnostics | Missing artifact, contradictory phase result, unsupported default/HMC/posterior/superiority claim. |
| Explanatory diagnostics | Phase metrics and review comments. |
| Not concluded | No default change, no HMC readiness, no posterior correctness, no statistical superiority. |
| Artifact | P04 closeout and ledgers. |

## Forbidden Claims/Actions

- Do not change defaults.
- Do not rank methods without uncertainty evidence.
- Do not treat one-seed diagnostics as broad claims.

## Exact Next-Phase Handoff Conditions

No next phase in this runbook. Hand off the next safest plan or stop condition.

## Stop Conditions

- Required phase evidence missing or contradictory.
- Final classification would require a human/default-policy decision.

## Skeptical Plan Audit

Closeout must separate stochastic evidence, repair evidence, and default
promotion evidence.
