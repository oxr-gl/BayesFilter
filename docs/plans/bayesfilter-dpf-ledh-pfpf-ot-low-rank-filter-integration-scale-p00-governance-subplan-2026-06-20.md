# P00 Governance, Source Intake, And Plan Review Subplan

Status: `DRAFT_REVIEW_REQUIRED`

## Phase Objective

Lock the program boundary, source anchors, owned files, evidence contract,
Claude review protocol, and visible runbook before implementation or scale
commands run.

## Entry Conditions Inherited From Previous Phase

This is the first phase.  It inherits the user directive to execute the
low-rank coupling solver-route validation lane independently from the
positive-feature lane and to correct the prior planning error by testing actual
LEDH/PFPF-OT filter-shaped integration, not only component resampling.

## Required Artifacts

- Master program:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-filter-integration-scale-master-program-2026-06-20.md`
- Visible runbook:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-filter-integration-scale-visible-gated-execution-plan-2026-06-20.md`
- Claude review ledger:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-filter-integration-scale-claude-review-ledger-2026-06-20.md`
- Execution ledger:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-filter-integration-scale-visible-execution-ledger-2026-06-20.md`
- Stop handoff:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-filter-integration-scale-visible-stop-handoff-2026-06-20.md`
- Phase result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-filter-integration-scale-p00-governance-result-2026-06-20.md`

## Required Checks, Tests, And Reviews

- Local `rg` checks that each subplan has required sections.
- Local `rg` checks for forbidden unsupported claim language.
- Path-only Claude read-only review of the master program, runbook, and
  subplans.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Are the master program and phase subplans sufficient, bounded, reviewable, and aligned with the actual filter-integration question? |
| Baseline/comparator | User instructions, AGENTS.md policy, visible runbook template, and existing low-rank/LEDH source anchors. |
| Primary pass criterion | Required artifacts exist; required sections are present; no unsupported promotion/default/speedup claims; Claude review converges to `VERDICT: AGREE` or no material finding after bounded repair. |
| Veto diagnostics | Missing required subplan field, missing owned-file boundary, unsupported claim, public export/default/shared contract edit in plan, whole-file Claude prompt requirement, or review nonconvergence after five rounds. |
| Explanatory diagnostics | Claude wording findings and local section-check details. |
| Not concluded | No implementation correctness, filter-scale viability, speedup, ranking, posterior correctness, HMC readiness, public API readiness, production/default readiness, dense Sinkhorn equivalence, broad scalable-OT selection, or TF32-help claim. |
| Artifact | P00 result and Claude review ledger. |

## Forbidden Claims And Actions

- Do not implement code in P00.
- Do not edit shared ledgers, public exports, public defaults, positive-feature
  artifacts, or Agent A artifacts.
- Do not send whole file contents to Claude; send paths and review scope only.
- Do not treat Claude as an execution authority.
- Do not claim component-lane scale success validates actual filter scale.

## Exact Next-Phase Handoff Conditions

P01 may start only if P00 local checks pass and Claude review converges or has
only nonblocking wording findings that are visibly patched or recorded.

## Stop Conditions

- `LOW_RANK_FILTER_INTEGRATION_SCALE_BLOCKED_REVIEW_NONCONVERGENCE`
- `BLOCKED_SHARED_CONTRACT_CHANGE_REQUIRED`
- Missing visible runbook template or unreadable source anchors.

## End-Of-Phase Protocol

1. Run required local checks.
2. Write the P00 result/close record.
3. Draft or refresh P01 subplan.
4. Review P01 for consistency, correctness, feasibility, artifact coverage, and boundary safety.
