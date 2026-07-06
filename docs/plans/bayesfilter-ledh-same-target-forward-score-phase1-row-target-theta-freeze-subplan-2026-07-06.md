# Phase 1 Subplan: Row Target And Theta Freeze

metadata_date: 2026-07-06
status: DRAFT
master_program: docs/plans/bayesfilter-ledh-same-target-forward-score-master-program-2026-07-06.md
phase: 1

## Phase Objective

Freeze every row's observed-data likelihood target, free parameter vector,
allowed observation transform, and score dimensionality before implementation.

## Entry Conditions Inherited From Previous Phase

- Phase 0 launch artifacts passed local checks and read-only review.
- Same-target forward likelihood admission is the hard prerequisite for score
  work.

## Required Artifacts

- Phase 1 result:
  `docs/plans/bayesfilter-ledh-same-target-forward-score-phase1-row-target-theta-freeze-result-2026-07-06.md`
- Row target/theta contract table under `docs/plans`.
- Refreshed Phase 2 subplan.
- Phase 1 review bundle under `docs/reviews`.

## Required Checks/Tests/Reviews

- Search current target contracts, leaderboard ledgers, source-scope contracts,
  and current runner callbacks for each row.
- For Zhao-Cui-family rows, preserve source-anchor discipline where relevant.
- Local `rg` checks for each row id and target scalar.
- Claude read-only review of the row target/theta contract.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | What exact `log p_theta(y_1:T)` target and theta vector must each LEDH row use? |
| Baseline/comparator | Existing row contracts, July 3/July 5 LEDH artifacts, source-scope contracts, and current implementation traces. |
| Primary criterion | Every row has a frozen target scalar, free theta, transform rule, and score dimensionality before code edits. |
| Veto diagnostics | Raw/transformed SV ambiguity; fixed SIR nonempty score invented silently; scoped SIR treated as full row; KSC/actual/generalized SV substitution. |
| Explanatory diagnostics | Historical candidate adapters and diagnostic score routes. |
| Not concluded | No forward scalar is admitted and no score code is implemented in this phase. |

## Forbidden Claims/Actions

- Do not implement code.
- Do not admit existing callbacks as same-target evidence.
- Do not invent a nonempty fixed-SIR score.
- Do not redefine a row after seeing numerical results.

## Allowed Operations

- Edit docs/plans target-contract artifacts.
- Run local text checks.
- Use Claude read-only review.

## Exact Next-Phase Handoff Conditions

Advance to Phase 2 only if the Phase 1 result freezes:

- row target scalar;
- theta vector and shape;
- score dimensionality;
- target density functions required by the forward API;
- human-required decisions, if any.

## Stop Conditions

Stop if a row target cannot be frozen without a human scientific/product
decision, especially fixed SIR nonempty score policy or raw-vs-transformed
actual-SV target policy.
