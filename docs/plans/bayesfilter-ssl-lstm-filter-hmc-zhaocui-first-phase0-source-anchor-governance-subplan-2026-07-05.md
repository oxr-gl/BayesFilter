# Phase 0 Subplan: Source-Anchor Governance And Route Classification

Date: 2026-07-05

Status: `DRAFT_READY_FOR_PRECHECK`

## Phase Objective

Determine whether the proposed Zhao-Cui-first SSL-LSTM lane can be honestly
classified as a fixed-variant adaptation, what source anchors are available,
and what claims remain forbidden before any adapter code is written.

## Entry Conditions Inherited From The Previous Phase

- The Zhao-Cui-first master program exists.
- The visible gated execution runbook exists.
- LEDH is explicitly deferred to a separate future program.
- The local Zhao-Cui source snapshot and the existing Phase 4 blocker record are available.

## Required Artifacts

- `docs/plans/bayesfilter-ssl-lstm-filter-hmc-zhaocui-first-phase0-source-anchor-governance-result-2026-07-05.md`
- `docs/reviews/bayesfilter-ssl-lstm-filter-hmc-zhaocui-first-phase0-review-bundle.md`
- A source-anchor and adaptation-classification ledger.
- A concise route-decision note stating whether each proposed choice is
  `source_faithful`, `fixed_hmc_adaptation`, or `extension_or_invention`.
- A refreshed Phase 1 subplan.

## Required Checks, Tests, And Reviews

- Inspect the local Zhao-Cui source-anchor audit ledger and the author source files.
- Inspect the current SSL-LSTM protocol and adapter scaffolding.
- Verify that any proposed SSL-LSTM Zhao-Cui route can remain deterministic in the target path.
- Claude read-only review on the bounded phase-0 bundle if available; otherwise Codex substitute review on the same bounded bundle.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can we classify the Zhao-Cui-first SSL-LSTM route honestly before implementation starts? |
| Baseline/comparator | Local Zhao-Cui source anchors, the SSL-LSTM protocol scaffold, and the current blocked Phase 4 record. |
| Primary pass criterion | The phase writes a usable source-anchor ledger and a route-classification table without overclaiming source-faithful parity. |
| Veto diagnostics | Missing anchors, unclassified route choices, hidden claims of parity, or a review result that still leaves the route boundary ambiguous. |
| Explanatory diagnostics | Source crosswalk notes, route-classification notes, and existing blocker summaries. |
| Not concluded | No implementation success, no HMC success, no method superiority, no LEDH claim. |
| Result artifact | `docs/plans/bayesfilter-ssl-lstm-filter-hmc-zhaocui-first-phase0-source-anchor-governance-result-2026-07-05.md` |

## Forbidden Claims And Actions

- Do not claim source-faithful SSL-LSTM Zhao-Cui parity.
- Do not claim the route is HMC-ready.
- Do not use autodiff as a stand-in for the target score path.
- Do not bring LEDH work into this phase.
- Do not mutate unrelated dirty worktree files.

## Exact Next-Phase Handoff Conditions

Phase 1 may start only when:

- the source-anchor ledger exists and is internally consistent;
- each proposed route choice has a classification;
- the forbidden-claims list is explicit;
- the Phase 1 subplan is drafted and reviewed for consistency, correctness,
  feasibility, artifact coverage, and boundary safety.

## Stop Conditions

- Required source anchors cannot be inspected.
- The route cannot be classified without inventing an unapproved method.
- Claude and Codex do not converge on the phase-0 classification after five review rounds.
- Any boundary crossing would be required before classification is complete.

## End-Of-Phase Protocol

1. Run the required local source and protocol inspections.
2. Write the phase result / close record.
3. Draft or refresh the Phase 1 subplan.
4. Review the Phase 1 subplan for consistency, correctness, feasibility,
   artifact coverage, and boundary safety.
