# Phase 7 Subplan: Source-Faithful Zhao-Cui Anchor Track

Date: 2026-07-06

Status: `PLACEHOLDER_AWAITING_ANCHOR_APPROVAL`

## Phase Objective

Create a separate source-faithful Zhao-Cui track only with paper and author
source anchors, classifying every route choice before implementation.

## Entry Conditions Inherited From Previous Phase

- Human explicitly wants source-faithful parity work.
- Paper/source artifacts are available for inspection.

## Required Artifacts

- Paper/source anchor ledger.
- Route classification table.
- Phase result or blocker.

## Required Checks, Tests, Reviews

- Inspect cited paper sections/equations and local author source lines.
- Review verifies anchors, not only internal consistency.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Which Zhao-Cui operations are source-faithful, fixed-HMC adaptations, or extensions/inventions for this setting? |
| Baseline/comparator | Zhao-Cui paper/math and author source code, not the clean-room `zhaocui_fixed` artifact alone. |
| Primary pass criterion | Every material route choice has paper/source anchors or is explicitly classified otherwise. |
| Veto diagnostics | Ungrounded faithful language, missing source line anchors, or route changes mislabeled as faithful. |
| Explanatory diagnostics | Anchor tables, operation classifications, and gaps. |
| Not concluded | Source-faithful implementation unless all required anchors and checks pass. |

## Forbidden Claims And Actions

Do not use "faithful", "source-faithful", or equivalent without paper and
author-source anchors.

## Exact Next-Phase Handoff Conditions

Proceed only after anchor review returns `VERDICT: AGREE`.

## Stop Conditions

Stop on `BLOCK_SOURCE_UNGROUNDED`, missing author source, or review
nonconvergence.
