# P12-0 Subplan: Governance, Source Anchors, And Review Gate

Date: 2026-06-19

## Status

`IN_PROGRESS_CLAUDE_REVIEW_REPAIR_LOOP`

## Phase Objective

Lock the P12 lane governance, source-route classifications, owned write set,
forbidden boundaries, and Claude review protocol before any replay or further
execution.

## Entry Conditions Inherited From Previous Phase

This is the first phase.  It inherits only the Wave 1 coordinator record, the
parallel execution structure, and repository policy in `AGENTS.md`.

## Required Artifacts

- P12 master program:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p12-low-rank-solver-route-master-program-2026-06-19.md`
- This subplan.
- P12 Claude review ledger:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p12-low-rank-solver-route-claude-review-ledger-2026-06-19.md`
- Visible gated overnight execution plan:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p12-low-rank-solver-route-visible-gated-overnight-execution-plan-2026-06-19.md`
- Phase result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p12-low-rank-solver-route-p00-governance-source-lock-result-2026-06-19.md`

## Required Checks, Tests, And Reviews

- Confirm all P12 governance artifacts exist.
- Confirm source-route classes appear in master/subplan/runbook.
- Confirm forbidden claims are explicitly barred.
- Claude read-only review is required for convergence, but only after explicit
  user approval.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Are P12 governance, source anchors, write boundaries, stop conditions, and review loops explicit enough to safely govern the lane? |
| Baseline/comparator | Wave 1 coordinator and existing P12 subplan. |
| Primary pass criterion | Master program, phase subplans, runbook, and review ledger exist and encode the frozen Wave 1 contracts without expanding write scope or scientific claims. |
| Veto diagnostics | Missing owned-file boundary, missing stop condition, unsupported source-faithfulness claim, hidden shared contract edit, missing Claude max-5 repair loop, or plan-launch command before approval. |
| Explanatory diagnostics | Number of artifacts, section coverage, local text scans, Claude findings after approval. |
| Not concluded | No implementation correctness, solver validity, speedup, ranking, posterior correctness, HMC readiness, public API readiness, or default readiness. |

## Forbidden Claims And Actions

- Do not claim the P12 implementation is valid in this phase.
- Do not run Claude before user approval.
- Do not launch or continue the execution plan without explicit user approval.
- Do not edit current-agent, shared ledger/handoff, Phase 1, Phase 3, Phase 6,
  Nystrom, public export, or unrelated dirty files.

## Exact Next-Phase Handoff Conditions

Advance to P12-1 only if:

- governance artifacts are present;
- local text checks find required sections and no positive forbidden claims;
- Claude review is approved and returns `VERDICT: AGREE`.

## Stop Conditions

Stop if:

- the user does not approve Claude Code review;
- review finds a material unfixable governance flaw;
- fixing a flaw requires a shared contract change or forbidden file edit.

## End-Of-Phase Protocol

At phase end:

1. run required local checks;
2. write the P12-0 result/close record;
3. draft or refresh the P12-1 subplan;
4. review the P12-1 subplan for consistency, correctness, feasibility,
   artifact coverage, and boundary safety.
