# Phase 4 Subplan: Generalized-SV Exact Source-Row Evaluator

Date: 2026-07-04

Status: `DRAFT_PENDING_PLAN_REVIEW`

## Phase Objective

Repair the generalized-SV exact source-row evaluator so the row is either
admitted with same-target analytical/manual score evidence or preserved as a
precise source-row blocker.

## Entry Conditions Inherited From The Previous Phase

- Phase 0 froze the leaderboard baseline and row-family order.
- Phase 3 has either passed or recorded a precise KSC blocker that does not
  invalidate generalized-SV work.
- The July 3 artifact still marks generalized-SV as blocked by exact-row
  evaluator missing.

## Required Artifacts

- Phase 4 result:
  `docs/plans/bayesfilter-highdim-leaderboard-blocker-by-blocker-phase4-generalized-sv-result-2026-07-04.md`
- Any code or benchmark edits needed for the generalized-SV exact row.
- Row-local JSON/Markdown result artifact.
- Visible execution ledger update.

## Required Checks, Tests, And Reviews

- Source/target freeze check: exact source-row target must be named plainly.
- If any claim uses "faithful", include paper/source anchors; otherwise do not
  use faithfulness wording.
- Same-target value/score consistency check for the generalized-SV row.
- `git diff --check` on touched files.
- Claude review of the phase result if the row is admitted or the blocker
  wording changes materially.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the generalized-SV exact source-row evaluator be repaired for same-target value and score? |
| Baseline/comparator | The July 3 combined leaderboard generalized-SV blocked row and any explicitly cited source-row artifacts. |
| Primary criterion | Same-target generalized-SV value and score are both finite and share the same route; otherwise the phase records a precise blocker. |
| Veto diagnostics | Actual-SV, KSC, precursor, auxiliary, or native-oracle evidence used as source-row admission evidence; autodiff score provenance; target drift. |
| Explanatory diagnostics | FD consistency, runtime, score norm, and source-anchor audit. |
| Not concluded | Actual-SV, KSC, SIR, predator-prey, UKF cleanup, or full leaderboard regeneration. |

## Forbidden Claims/Actions

- Do not use actual-SV or KSC evidence as source-row admission evidence.
- Do not say "faithful" without anchors.
- Do not call autodiff score provenance analytical/manual.

## Exact Next-Phase Handoff Conditions

Advance to Phase 5 only if Phase 4 writes either:

- admitted generalized-SV same-target value/score; or
- a precise generalized-SV blocker that does not require reordering later phases.

## Stop Conditions

Stop and write a blocker result if:

- the source-row target is not exact;
- the score route lacks theta coordinates or manual provenance;
- the phase attempts to borrow another family’s evidence.

## Phase-End Duties

At the end of Phase 4:

1. run the required local checks;
2. write the Phase 4 result / close record;
3. draft or refresh the Phase 5 subplan;
4. review the Phase 5 subplan for consistency, correctness, feasibility,
   artifact coverage, and boundary safety.
