# P00 Governance, Plan Review, And GPU Selection Preflight Subplan

Status: `DRAFT_REVIEW_REQUIRED_ROUND_2`

## Phase Objective

Lock the efficiency evidence contract, owned files, fixed criteria, GPU
selection rule, Claude review protocol, and visible runbook before any
implementation or benchmark commands run.

## Entry Conditions Inherited From Previous Phase

This is the first phase.  It inherits the completed low-rank integration result
`LOW_RANK_FILTER_INTEGRATION_SCALE_PASSED_DIAGNOSTIC_ONLY`, but does not treat
that result as efficiency evidence.  The user asks whether the route makes the
LEDH/PFPF-OT TF32 algorithm efficient at very large particle counts.

## Required Artifacts

- Master program:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-efficiency-validation-master-program-2026-06-21.md`
- Visible runbook:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-efficiency-validation-visible-gated-execution-plan-2026-06-21.md`
- Claude review ledger:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-efficiency-validation-claude-review-ledger-2026-06-21.md`
- Execution ledger:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-efficiency-validation-visible-execution-ledger-2026-06-21.md`
- Stop handoff:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-efficiency-validation-visible-stop-handoff-2026-06-21.md`
- Phase result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-efficiency-validation-p00-governance-result-2026-06-21.md`

## Required Checks, Tests, And Reviews

- Local `rg` checks that each subplan has required sections.
- Local `rg` checks for fixed efficiency criteria, numeric timeouts, TF32 hard
  gates, same-GPU hard gates, output-comparability gates, and forbidden
  non-claims.
- Trusted GPU selection preflight with GPU1 preference and GPU0 fallback rule.
- Path-only Claude read-only review of the master program and linked subplans.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is the efficiency-validation plan sufficient to test whether low-rank helps LEDH/PFPF-OT TF32 handle very large particle counts? |
| Baseline/comparator | User request, AGENTS.md policy, visible runbook template, prior integration closeout as diagnostic context, existing streaming route as feasible-N comparator. |
| Primary pass criterion | Required artifacts exist; required sections are present; fixed criteria are predeclared; GPU selection rule is recorded; numeric timeouts are fixed; paired ladder includes upward streaming attempts as far as runnable; TF32/same-GPU/output-comparability hard gates are recorded; Claude returns `VERDICT: AGREE`. |
| Veto diagnostics | Missing required section, unsupported efficiency/posterior/default claim, missing GPU1 preference, absent fixed thresholds/timeouts, treating runtime as promotion without paired screen and output-comparability gates, allowing mixed-GPU paired claims, TF32 mismatch for TF32 claims, or Claude review nonconvergence after five rounds. |
| Explanatory diagnostics | Claude wording findings, local section checks, GPU preflight details. |
| Not concluded | No actual efficiency result, no posterior correctness, no HMC readiness, no public API readiness, no production/default readiness, no dense Sinkhorn equivalence, and no broad scalable-OT selection. |
| Artifact | P00 result and Claude review ledger. |

## Forbidden Claims And Actions

- Do not implement or benchmark in P00 beyond GPU preflight.
- Do not claim efficiency from prior diagnostic artifacts or from low-rank-only
  large-N rows.
- Do not use broad repo prompts for Claude.
- Do not edit shared/public/default artifacts.

## Exact Next-Phase Handoff Conditions

P01 may start only if P00 local checks pass, GPU selection/preflight is recorded
or a GPU blocker is written, and Claude review converges with `VERDICT: AGREE`.

## Stop Conditions

- `LOW_RANK_LEDH_EFFICIENCY_BLOCKED_REVIEW_NONCONVERGENCE`
- `LOW_RANK_LEDH_EFFICIENCY_BLOCKED_GPU_UNAVAILABLE`
- `LOW_RANK_LEDH_EFFICIENCY_BLOCKED_SHARED_CONTRACT_CHANGE_REQUIRED`

## End-Of-Phase Protocol

1. Run required local checks.
2. Write the P00 result/close record.
3. Draft or refresh P01 subplan.
4. Review P01 for consistency, correctness, feasibility, artifact coverage, and boundary safety.
