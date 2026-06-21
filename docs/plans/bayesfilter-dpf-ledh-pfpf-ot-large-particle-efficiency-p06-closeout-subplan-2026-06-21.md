# P06 Closeout And Decision Subplan

Date: 2026-06-21

Status: DRAFT_FOR_REVIEW

## Phase Objective

Synthesize P03/P04/P05 evidence into an explicit answer to whether the current
streaming GPU TF32 LEDH-PFPF-OT route improves LGSSM-shaped benchmark
operational feasibility at very large particle counts, while preserving
statistical and scientific claim boundaries.

## Entry Conditions Inherited From Previous Phase

- P03 large-`N` reach result exists or a blocker result exists.
- P04 matched TF32-vs-FP32 result exists or a blocker result exists.
- P05 dense context result or justified skip exists.

## Required Artifacts

- Final result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-large-particle-efficiency-result-2026-06-21.md`
- Updated execution ledger:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-large-particle-efficiency-visible-execution-ledger-2026-06-21.md`
- Updated stop handoff:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-large-particle-efficiency-visible-stop-handoff-2026-06-21.md`
- Updated Claude review ledger if final review is requested.

## Required Checks, Tests, And Reviews

- JSON artifact audit across P03/P04/P05:
  - required files exist;
  - P03 hard gates are represented correctly;
  - P04 matched comparison is represented correctly;
  - P05 contextual/non-promotional status is represented correctly.
- Final result note must include:
  - decision table;
  - inference-status table;
  - run manifest;
  - post-run red-team note;
  - what is supported;
  - what is not supported;
  - next smallest discriminating test.
- Claude read-only review of final interpretation if P06 claims operational
  help or recommends extending to larger `N`.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Based on the completed artifacts, what can we say about large-particle operational efficiency for the current streaming GPU TF32 LEDH-PFPF-OT route? |
| Baseline/comparator | P03 streaming reach and P04 same-route FP32-no-TF32 comparator; P05 dense small-`N` context only. |
| Primary criterion | Final result correctly maps evidence to claims and nonclaims without unsupported promotion. |
| Veto diagnostics | Missing required artifacts, unsupported speedup/statistical claim, posterior-correctness claim, or artifact/hard-gate mismatch. |
| Explanatory diagnostics | Runtime/memory summaries and dense context. |
| Not concluded | No posterior correctness, no HMC readiness, no statistical ranking, no public API readiness, no universal scalability limit. |
| Artifact | Final result and stop handoff. |

## Forbidden Claims Or Actions

- Do not claim "statistically faster" without replication/uncertainty.
- Do not claim posterior correctness from synthetic LGSSM feasibility.
- Do not treat a passed engineering reach ladder as proof of scientific
  validity.
- Do not launch a new larger ladder from P06 without a new subplan.

## Exact Next-Phase Handoff Conditions

This is the final phase. Handoff must state:

- whether the current route helped LGSSM-shaped operational large-`N`
  feasibility;
- largest passed shape;
- whether TF32 had descriptive runtime advantage at matched shape;
- whether the dense context was executed or skipped;
- next recommended discriminating run.

## Stop Conditions

- Artifact audit fails and cannot be repaired in the current run.
- Claude/Codex final interpretation review does not converge after five rounds.
- A new user/human decision is required before making the final claim.

## End-Of-Phase Actions

1. Run required artifact audit.
2. Write the final result/close record.
3. Refresh the visible stop handoff.
4. Review final interpretation for boundary safety.
