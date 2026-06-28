# P00 Governance, Audit, And Review Subplan

Status: `DRAFT_FOR_REVIEW`

## Phase Objective

Establish the restart evidence contract, phase boundaries, repair loop, artifact
schema, skeptical audit, and Claude review protocol before implementation or
benchmark execution.

## Entry Conditions Inherited From Previous Phase

This is the first phase. It inherits the user request, repository policy, and
the reset memo showing the previous lane stopped at `TUNING_REQUIRED`.

## Required Artifacts

- Master program:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-tuning-master-program-2026-06-22.md`
- Visible runbook:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-tuning-visible-gated-execution-runbook-2026-06-22.md`
- Execution ledger:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-tuning-visible-execution-ledger-2026-06-22.md`
- Claude review ledger:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-tuning-claude-review-ledger-2026-06-22.md`
- Phase result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-tuning-p00-governance-result-2026-06-22.md`

## Required Checks/Tests/Reviews

- Confirm reset memo, harness, comparator, and solver source anchors exist.
- Confirm master/runbook/subplans include tuning-versus-holdout separation.
- Confirm every phase has required artifacts, checks, evidence contract,
  forbidden claims/actions, handoff conditions, stop conditions, and end duties.
- Claude Opus max effort read-only review to convergence or five rounds for the
  same blocker.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is the governed restart plan capable of answering the actual-SIR low-rank tuning question without proxy promotion or boundary drift? |
| Baseline/comparator | Existing compiled streaming actual-SIR TF32/GPU route through the owned validation harness. |
| Primary pass criterion | Source anchors exist, phase artifacts exist, skeptical audit passes, and Claude review returns `VERDICT: AGREE` or a blocker result is written. |
| Veto diagnostics | Wrong baseline, proxy/tuning evidence promoted to held-out support, missing stop condition, unfair comparison, stale reset state, environment mismatch, unsupported claim, or artifact mismatch. |
| Explanatory diagnostics | Prior stopped row, prior synthetic low-rank evidence, and harness readiness context. |
| Not concluded | No implementation correctness, runtime result, speedup, posterior correctness, HMC readiness, default readiness, or statistical ranking. |
| Artifact | P00 result and Claude review ledger. |

## Forbidden Claims/Actions

- Do not run GPU benchmarks in P00.
- Do not claim tuning success, speedup, or support.
- Do not send whole files to Claude.
- Do not modify existing validation artifacts or public code.

## Exact Next-Phase Handoff Conditions

Advance to P01 only if P00 result is `PASS`, Claude review converges, and P01 is
present with local checks, artifact paths, and bounded implementation/write
scope.

## Stop Conditions

- Stop if source anchors are missing or contradict the planned comparator.
- Stop if Claude and Codex do not converge after five review rounds for the same
  material blocker.
- Stop if P01 would require public API/default-policy or shared contract changes.

## End-Of-Subplan Duties

1. Run required local checks.
2. Write the P00 phase result.
3. Draft or refresh P01.
4. Review P01 for consistency, correctness, feasibility, artifact coverage, and
   boundary safety.
