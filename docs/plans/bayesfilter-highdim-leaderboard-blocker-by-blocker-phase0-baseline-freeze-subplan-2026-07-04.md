# Phase 0 Subplan: Baseline Freeze And Launch Gate

Date: 2026-07-04

Status: `DRAFT_PENDING_PLAN_REVIEW`

## Phase Objective

Freeze the July 3 combined highdim leaderboard baseline and confirm the
candidate row-family order and blocker vocabulary before any row-family repair
starts.

## Entry Conditions Inherited From The Previous Phase

- The master program and visible runbook exist in draft form.
- The combined July 3 leaderboard JSON/Markdown baseline is the authority.
- The current remaining-blockers ledger is authoritative:
  `docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-visible-execution-ledger-2026-07-02.md`.
- No row-family repair has started yet.

## Required Artifacts

- Phase 0 result:
  `docs/plans/bayesfilter-highdim-leaderboard-blocker-by-blocker-phase0-baseline-freeze-result-2026-07-04.md`
- Visible execution ledger update.
- If needed, a phase-0 review bundle for Claude.
- A baseline reconciliation note that explicitly says whether the phase-family
  list covers the current remaining-blocker families and how its repair order
  relates to the July 3 combined leaderboard and July 2 remaining-blockers
  ledger.

## Required Checks, Tests, And Reviews

- Confirm the baseline artifact paths and row-family order from the combined
  leaderboard JSON.
- Confirm that the planned phase list covers the current blocked row families,
  while remembering that the candidate list is provisional until this phase
  certifies it.
- Run `git diff --check` on the new planning files.
- Claude read-only review of the plan bundle if the plan or runbook changes in a
  material way.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is the blocker-by-blocker program frozen against the correct baseline and row family order? |
| Baseline/comparator | July 3 combined highdim leaderboard JSON/Markdown and `docs/plans/bayesfilter-highdim-leaderboard-remaining-blockers-visible-execution-ledger-2026-07-02.md`. |
| Primary criterion | The program records the correct row-family order and plain-language gate rules before repair begins. |
| Veto diagnostics | Wrong row family order, stale blocker vocabulary, or any attempt to promote diagnostic evidence into admission evidence. |
| Explanatory diagnostics | Baseline hash or file-path checks, row inventory summary, and review verdict. |
| Not concluded | Any repair, admission, or GPU readiness claim. |

## Forbidden Claims/Actions

- Do not claim any row is repaired in Phase 0.
- Do not start any row-family code change before the baseline is frozen.
- Do not promote sidecar, lower-rung, or autodiff evidence.

## Exact Next-Phase Handoff Conditions

Advance to Phase 1 only if:

- the baseline and row-family coverage/order are confirmed in a result artifact;
- the plain-language gate is preserved;
- the runbook and master program agree on the same phase index.
- the result artifact explicitly cites the current remaining-blockers ledger
  path.

## Stop Conditions

Stop and write a blocker result if:

- the row-family coverage is wrong or the repair order cannot be justified;
- the baseline artifact is stale or missing;
- the program tries to admit a score without same-target evidence.

## Phase-End Duties

At the end of Phase 0:

1. run the required local checks;
2. write the Phase 0 result / close record;
3. draft or refresh the Phase 1 subplan;
4. review the Phase 1 subplan for consistency, correctness, feasibility,
   artifact coverage, and boundary safety.
