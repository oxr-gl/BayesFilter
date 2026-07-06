# P05 Subplan: Closeout And Leaderboard Readiness Decision

Date: 2026-06-21

Status: `DRAFT_DEPENDS_ON_P04`

## Phase Objective

Synthesize P00-P04 into a bounded decision about whether Nystrom is
leaderboard-ready for later scalable-OT screening.

## Entry Conditions Inherited From Previous Phase

- P00-P04 each wrote result artifacts or an explicit blocker.
- Any GPU blocker is documented with exact reason.
- No unsupported default, posterior, HMC, API, or ranking claim has been made.

## Required Artifacts

- Final result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-nystrom-algorithm-complete-result-2026-06-21.md`
- Updated execution ledger.
- Updated stop handoff.
- Claude final closeout review record in the review ledger.

## Required Checks, Tests, Reviews

- Local artifact existence and JSON parse checks for completed benchmark phases.
- `rg` claim-boundary check over final result for forbidden unsupported claims.
- Compact read-only Claude final closeout review.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is Nystrom ready to enter a future screening leaderboard as a real diagnostic candidate? |
| Baseline/comparator | P02 dense small-reference, P03 downstream smoke, P04 GPU scale envelope. |
| Primary criterion | Final result accurately records phase statuses, hard vetoes, uncertainty, and next justified action without overclaiming. |
| Veto diagnostics | Missing phase result, unsupported ranking/default/posterior/HMC/API claim, failed required artifact parse, or unresolved Claude material finding. |
| Explanatory diagnostics | Runtime, memory, dense-reference errors, selected ranks, GPU metadata. |
| Not concluded | No final algorithm ranking, production/default readiness, posterior correctness, HMC readiness, public API readiness, or statistical superiority. |
| Artifact | Final result, ledger, stop handoff. |

## Forbidden Claims And Actions

- Do not change default algorithm.
- Do not commit or push unless explicitly requested later.
- Do not start a screening leaderboard automatically.

## Exact Next-Phase Handoff Conditions

There is no automatic next execution phase. If final status is
`leaderboard_ready_diagnostic_candidate`, the next separate program may build a
leaderboard using Nystrom plus other completed candidates. If not, the final
result must state the repair or blocker before screening.

## Stop Conditions

- Final evidence is internally inconsistent.
- Required closeout review does not converge after five rounds.
- A result would require a human decision about default/product/scientific
  claims.
