# P08 Subplan: Final Scoped Promotion Decision

Date: 2026-06-25

Status: `DRAFT_AFTER_P07`

## Phase Objective

Synthesize P01-P07 evidence into a scoped final verdict: ready for owner default
switch, optional route only, repair required, or blocked. P08 does not run new
benchmarks and does not change code defaults.

## Entry Conditions Inherited From Previous Phase

- P01-P07 results exist.
- Candidate policy remained locked unless a reviewed repair phase downgraded
  promotion claims.
- HMC readiness remained out of scope.

## Required Artifacts

- Final result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-result-2026-06-25.md`
- Updated master program, visible runbook, execution ledger, Claude review
  ledger, and stop handoff.

## Required Checks, Tests, And Reviews

- Parse all P01-P07 result artifacts.
- Verify final verdict follows phase outcomes and does not overclaim.
- Inference-status table covering hard vetoes, viable candidate status,
  statistically supported ranking, default-candidate readiness, and next
  evidence needed.
- Claude read-only review of final decision; convergence required.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | What scoped final verdict is justified by P01-P07 evidence? |
| Baseline/comparator | Aggregated phase evidence; no new comparator in P08. |
| Primary criterion | Final verdict is logically entailed by phase results and review converges. |
| Veto diagnostics | Missing phase result, unsupported claim, HMC readiness claim, statistical ranking without uncertainty, default-code switch, or review nonconvergence. |
| Explanatory diagnostics | Phase-level summaries, residual risk table, open gaps. |
| Not concluded | HMC readiness, public API/package release, scientific superiority, dense equivalence, funding/product claims. |
| Artifact | Final result and updated handoff. |

## Forbidden Claims And Actions

- Do not run new experiments.
- Do not change code defaults.
- Do not claim HMC readiness.
- Do not claim statistical superiority unless a phase explicitly supports it
  with uncertainty.
- Do not hide failed or scoped-out phases.

## Exact Next-Phase Handoff Conditions

- `SVD_NYSTROM_PROMOTION_READY_FOR_OWNER_DEFAULT_SWITCH`: all required gates
  pass and final review agrees.
- `SVD_NYSTROM_OPTIONAL_ROUTE_ONLY`: evidence supports optional bounded use but
  not default switch.
- `SVD_NYSTROM_REPAIR_REQUIRED`: fixable blocker or failed gate requires repair.
- `BLOCKED_HUMAN_DIRECTION_REQUIRED`: final decision requires owner direction.

## Stop Conditions

- Any required P01-P07 result missing.
- Final review does not converge after five rounds.
- Final verdict would require code default change, package release, or
  scientific/product claim without explicit owner approval.

## Local Self-Review Of Next Subplan

P08 is terminal. Any follow-up implementation/default switch must use a new
owner-approved implementation plan.
