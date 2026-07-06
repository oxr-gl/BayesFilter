# P04 Repair Classification Closeout Subplan

Status: `DRAFT_FOR_REVIEW`

## Phase Objective

Write the final repair-classification result and the next handoff. The closeout
must separate candidate rejection from research-direction rejection and must
state exactly what can be repaired next.

## Entry Conditions Inherited From Previous Phase

P01 and P02 passed, or P03 passed if it was required. Any classification must be
supported by preserved artifacts and source anchors.

## Required Artifacts

- Final repair-classification result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-repair-classification-result-2026-06-22.md`
- Visible stop/handoff:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-repair-classification-visible-stop-handoff-2026-06-22.md`
- Optional next implementation/tuning subplan draft, only if closeout identifies
  a safe next lane:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-route-performance-repair-subplan-2026-06-22.md`
- Optional next tuning-repair subplan draft, only if closeout identifies
  `TUNING_REPAIR`:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-tuning-repair-subplan-2026-06-22.md`
- Optional combined repair sequencing subplan draft, only if closeout identifies
  `BOTH_REPAIRS` and needs to preserve both lanes explicitly:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-combined-repair-sequencing-subplan-2026-06-22.md`

## Required Checks/Tests/Reviews

- Local check that final result references P00/P01/P02 and optional P03 result.
- Local check that final result includes decision table, inference-status table,
  nonclaims, and next handoff.
- Claude read-only review of final closeout and optional next subplan.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | What is the final repair classification and safest next plan? |
| Baseline/comparator | P01 artifact classifier and P02 code-path classifier, plus P03 if launched. |
| Primary pass criterion | Final result records one classifier, its evidence, its limits, and the next reviewed subplan or stop handoff. |
| Veto diagnostics | Missing phase result, unsupported claim, conflating route-performance and scientific validity, or route-internal edit without reviewed implementation subplan. |
| Explanatory diagnostics | P03 label counts, comparable-but-slow timing ratios, hard vetoes, source timing asymmetry, and residual uncertainty. |
| Not concluded | No speedup, candidate freeze, held-out support, posterior correctness, HMC readiness, dense Sinkhorn equivalence, public API/default readiness, or statistical ranking. |
| Artifact | Final result, stop handoff, review ledger, and optional next subplan draft. |

## Forbidden Claims/Actions

- Do not claim the route repair will succeed.
- Do not claim low-rank is better, faster, or ready by default.
- Do not erase the tuning/comparability/ESS failure evidence.
- Do not launch implementation repair until its dedicated subplan exists and is
  reviewed.

## Exact Next-Phase Handoff Conditions

This is the final phase of the repair-classification program. Handoff depends
on the final classifier:

- `ROUTE_PERFORMANCE_REPAIR`: hand off to the dedicated
  `actual-sir-low-rank-route-performance-repair-subplan`.
- `TUNING_REPAIR`: hand off to the dedicated
  `actual-sir-low-rank-tuning-repair-subplan`.
- `BOTH_REPAIRS`: either hand off to a combined sequencing subplan that
  preserves both lanes, or to a route-performance-first subplan plus an explicit
  tuning-repair preservation note when source-supported timing asymmetry makes
  route repair the smallest discriminating next step.
- `UNCLASSIFIED_NEEDS_MICROPROBE`: hand off to the P03 microprobe or stop if P03
  was vetoed.

## Stop Conditions

- Stop if final classification is unsupported by phase artifacts.
- Stop if Claude review identifies an unfixed material safety or evidence issue.
- Stop after five unresolved Claude review rounds for the same closeout blocker.

## End-Of-Subplan Duties

1. Run required local checks.
2. Write the final closeout result.
3. Draft or refresh the next repair subplan if justified.
4. Review the next repair subplan for consistency, correctness, feasibility,
   artifact coverage, and boundary safety.
