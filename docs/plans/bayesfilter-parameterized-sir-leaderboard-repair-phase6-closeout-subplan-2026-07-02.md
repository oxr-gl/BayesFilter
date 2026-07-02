# Phase 6 Subplan: Closeout And Release Note

Date: 2026-07-02

Status: `DRAFT_PENDING_PHASE5`

## Phase Objective

Write the final closeout, release-note language, and handoff for the
parameterized SIR repair.

## Entry Conditions Inherited From Previous Phase

- Phase 5 produced checked leaderboard artifacts or a precise blocker.
- No unresolved material review finding remains unrecorded.

## Required Artifacts

- Phase 6 result:
  `docs/plans/bayesfilter-parameterized-sir-leaderboard-repair-phase6-closeout-result-2026-07-02.md`
- Updated visible stop handoff.
- Optional release-note excerpt.

## Required Checks/Tests/Reviews

- `git diff --check` on touched files.
- Static search for forbidden claims in new artifacts.
- Claude read-only review of closeout if Phase 5 changed leaderboard status.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is the repair result recorded with accurate claims, checks, and residual risks? |
| Baseline/comparator | Master program and all phase results. |
| Primary pass criterion | Closeout says exactly what changed, what passed, what remains blocked, and what is not concluded. |
| Veto diagnostics | Unsupported exactness/source/HMC/GPU claims; missing test list; missing unresolved blocker list. |
| Explanatory diagnostics | Review trail and command manifest. |
| Not concluded | Anything not directly tested in prior phases. |
| Artifact | Phase 6 closeout and stop handoff. |

## Forbidden Claims/Actions

- Do not claim production readiness unless all planned production gates passed.
- Do not omit failed or skipped checks.
- Do not perform git commit/push unless the user asks separately.

## Exact Next-Phase Handoff Conditions

No next phase. The program is complete if the closeout passes. Otherwise write
a blocker handoff.

## Stop Conditions

Stop if closeout cannot reconcile the claims with artifacts, or if unrelated
dirty work makes a clean handoff impossible.

## End-Of-Phase Requirements

1. Run required local checks.
2. Write Phase 6 result or blocker.
3. Refresh stop handoff.
4. Review final claims for consistency, correctness, feasibility, artifact
   coverage, and boundary safety.
