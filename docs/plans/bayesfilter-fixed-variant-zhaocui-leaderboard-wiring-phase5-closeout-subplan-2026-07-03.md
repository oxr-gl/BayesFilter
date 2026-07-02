# Phase 5 Subplan: Closeout And Handoff

Date: 2026-07-03

Status: `READY_AFTER_PHASE4_SPLIT_MERGE`

## Phase Objective

Close the program with a plain-language result that states what changed, what
passed, what remains blocked, and what is not concluded.

## Entry Conditions Inherited From Previous Phase

- Phase 4 generated and validated the July 3 leaderboard artifacts by a
  split/merge route: unaffected rows are preserved from the frozen July 1 full
  artifact and the validated scoped Zhao-Cui SIR component row is merged in.

## Required Artifacts

- Phase 5 result:
  `docs/plans/bayesfilter-fixed-variant-zhaocui-leaderboard-wiring-phase5-closeout-result-2026-07-03.md`
- Updated review ledger and visible stop handoff.

## Required Checks / Tests / Reviews

- `git diff --check` on all program artifacts.
- Focused `rg` checks for forbidden overclaims.
- Claude read-only final review of Phase 5 result.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is the fixed-variant leaderboard wiring complete within the declared scope? |
| Baseline/comparator | Phase 0 baseline, the frozen July 1 full artifact, and Phase 4 split/merge July 3 artifacts. |
| Primary criterion | Closeout gives direct verdicts for row wiring, retained-grid demotion, analytical score provenance, remaining blockers, and nonclaims. |
| Veto diagnostics | Unsupported production/full-filtering/posterior/GPU claim; missing artifact path; Claude `VERDICT: REVISE` unresolved. |
| Explanatory diagnostics | List of tests, command outputs, and changed files. |
| Not concluded | Anything not explicitly evidenced by phases. |
| Artifact | Phase 5 result and stop handoff. |

## Forbidden Claims / Actions

- Do not claim package/release readiness unless separate release checks run.
- Do not claim full observed-data filtering likelihood if that was not closed.
- Do not claim unrelated expensive rows were freshly rerun in the July 3
  split/merge artifact.
- Do not make a git commit or push unless separately requested.

## Exact Next-Phase Handoff Conditions

No next phase. The program is complete if Phase 5 passes Claude review and
local checks.

## Stop Conditions

- Final review does not converge after five rounds.
- Closeout reveals an unaddressed material contradiction.

## End-Of-Subplan Protocol

1. Run required local checks.
2. Write Phase 5 result / close record.
3. Write final stop handoff.
4. Review the closeout for consistency, correctness, feasibility, artifact
   coverage, and boundary safety.
