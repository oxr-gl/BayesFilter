# P00 Repair Classification Governance Subplan

Status: `DRAFT_FOR_REVIEW`

## Phase Objective

Verify that the repair-classification program is anchored to the actual P03
stop artifacts, has a valid evidence contract, preserves BayesFilter governance,
and is safe to launch without modifying solver or streaming code.

## Entry Conditions Inherited From Previous Phase

P03 tuning ended with `NO_FREEZE_CANDIDATE_REPAIR_REQUIRED`. Stage B, P04, P05,
and P06 from the earlier tuning master are not allowed because no candidate was
freeze-nominated.

## Required Artifacts

- P00 result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-repair-classification-p00-governance-result-2026-06-22.md`
- Refreshed execution ledger:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-repair-classification-visible-execution-ledger-2026-06-22.md`
- Refreshed Claude review ledger:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-repair-classification-claude-review-ledger-2026-06-22.md`

## Required Checks/Tests/Reviews

- Local structural check that all repair-classification plan files include the
  required phase sections.
- Local existence check for P03 result, P03 stop handoff, P03 aggregate JSON,
  P03 aggregate Markdown, and focused tuning-grid test file.
- Read-only source/artifact anchor check using `rg` only.
- Claude read-only review of the master program, visible runbook, and P00-P04
  subplans before launching P01.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is the repair-classification program safe and sufficiently grounded to launch? |
| Baseline/comparator | P03 result, stop handoff, and aggregate artifact from the prior tuning run. |
| Primary pass criterion | Required artifacts exist, local structural checks pass, no forbidden action is present, and Claude review converges or no material issue remains. |
| Veto diagnostics | Missing P03 artifact, missing required subplan section, stale baseline, path that would execute P04/P05/P06, route-internal edit, or Claude `VERDICT: REVISE` on an unfixed material issue. |
| Explanatory diagnostics | Dirty worktree status and source anchor availability. |
| Not concluded | No repair classification, speedup, candidate freeze, or code correctness claim. |
| Artifact | P00 result and ledgers. |

## Forbidden Claims/Actions

- Do not classify the P03 failure yet.
- Do not run GPU tuning or held-out support.
- Do not edit solver, streaming route, public API, package metadata, or
  unrelated dirty files.
- Do not treat Claude agreement as authority to cross implementation or
  scientific-claim boundaries.

## Exact Next-Phase Handoff Conditions

Advance to P01 only if P00 result records `PASS`, P03 artifacts are present,
structural checks pass, and review has no unresolved material issue.

## Stop Conditions

- Stop if any P03 anchor artifact is missing or corrupted.
- Stop if the plan would require route-internal edits before a reviewed
  implementation subplan.
- Stop after five unresolved Claude review rounds for the same P00 blocker.

## End-Of-Subplan Duties

1. Run the required local checks.
2. Write the P00 result.
3. Draft or refresh P01.
4. Review P01 for consistency, correctness, feasibility, artifact coverage, and
   boundary safety.
