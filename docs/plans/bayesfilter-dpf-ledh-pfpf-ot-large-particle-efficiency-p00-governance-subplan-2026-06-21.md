# P00 Governance And Claim Lock Subplan

Date: 2026-06-21

Status: DRAFT_FOR_REVIEW

## Phase Objective

Lock the research question, evidence contract, GPU-selection policy, nonclaims,
and phase gate structure before any implementation or GPU execution.

## Entry Conditions Inherited From Previous Phase

None. This is the entry phase for the large-particle efficiency lane.

## Required Artifacts

- Master program:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-large-particle-efficiency-master-program-2026-06-21.md`
- Visible runbook:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-large-particle-efficiency-visible-gated-execution-runbook-2026-06-21.md`
- Execution ledger:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-large-particle-efficiency-visible-execution-ledger-2026-06-21.md`
- Review ledger:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-large-particle-efficiency-claude-review-ledger-2026-06-21.md`
- P00 result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-large-particle-efficiency-p00-governance-result-2026-06-21.md`

## Required Checks, Tests, And Reviews

- Local content checks verify that the master program and all phase subplans
  contain:
  - phase objective;
  - inherited entry conditions;
  - required artifacts;
  - required checks/tests/reviews;
  - evidence contract;
  - forbidden claims/actions;
  - exact next-phase handoff conditions;
  - stop conditions.
- Claude read-only review of the master program, runbook, and phase index.
- Codex skeptical plan audit recorded in the master program and execution
  ledger.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is the proposed large-particle efficiency program scoped to answer LGSSM-shaped operational large-`N` LEDH-PFPF-OT benchmark scalability without overclaiming quality or posterior correctness? |
| Baseline/comparator | Current streaming GPU TF32 default is the primary route; FP32-no-TF32 is the same-route runtime comparator; dense is only small-`N` context. |
| Primary criterion | All governance artifacts exist, contain required fields, and Claude/Codex review does not find an unresolved material boundary or baseline flaw. |
| Veto diagnostics | Missing required fields, wrong baseline, dense large-`N` comparator treated as required promotion criterion, runtime treated as statistical ranking, unrecorded GPU policy, or unsupported production/scientific claim. |
| Explanatory diagnostics | Prior artifacts and historical timings may motivate the ladder but cannot substitute for current-run evidence. |
| Not concluded | No implementation correctness, no large-`N` pass, no runtime benefit, no posterior correctness, and no HMC readiness. |
| Artifact | P00 result and review ledger. |

## Forbidden Claims Or Actions

- Do not run GPU experiments in P00.
- Do not claim the algorithm helps LEDH until P03/P04/P06 evidence exists.
- Do not treat dense small-`N` results as large-`N` superiority evidence.
- Do not ask Claude to edit files or execute experiments.

## Exact Next-Phase Handoff Conditions

Advance to P01 only if:

- required governance artifacts exist;
- local content checks pass;
- Claude review converges to `VERDICT: AGREE`, or any requested revisions have
  been patched and rechecked;
- P00 result records the evidence contract and nonclaims.

## Stop Conditions

- Missing or contradictory evidence contract.
- Claude/Codex review non-convergence after five rounds for the same blocker.
- Need for a human decision about changing the research question or default
  policy.

## End-Of-Phase Actions

1. Run required local content checks.
2. Write the P00 result/close record.
3. Draft or refresh the P01 subplan.
4. Review the P01 subplan for consistency, correctness, feasibility, artifact
   coverage, and boundary safety.
