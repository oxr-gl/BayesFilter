# P0 Subplan: Governance Reset And Evidence Boundary

Date: 2026-06-27

## Status

`DRAFT_FOR_VISIBLE_EXECUTION`

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can BayesFilter reset the retained-teacher neural-OT claim boundary so older neural-OT artifacts cannot be accidentally cited as source-faithful Meta OT or UNOT evidence before donor audit, donor choice, and port-first closure occur? |
| Baseline/comparator | Existing retained-teacher neural-OT plans/results from 2026-06-18, batched annealed transfer artifacts from 2026-06-18, retained-teacher LEDH master/repair artifacts from 2026-06-25 and 2026-06-26, plus the new 2026-06-27 gap note and source-faithful closure master program. |
| Primary pass criterion | A governance result artifact lists the main historical neural-OT artifacts, classifies them as implementation history / BayesFilter-native evidence / repair lineage rather than source-faithful closure evidence, and states the supersession rule for future faithfulness claims. |
| Veto diagnostics | Deleting historical files; overwriting old results; leaving older retained-teacher or annealed notes implicitly promotable as source-faithful evidence; failing to classify the major 2026-06-18 and 2026-06-26 artifact families. |
| Explanatory diagnostics | Artifact counts, family grouping, and route labels only. |
| Not concluded | P0 does not choose the primary donor, does not port code, and does not prove paper faithfulness. |
| Required artifact | `docs/plans/bayesfilter-neural-ot-retained-teacher-source-faithful-p0-governance-reset-result-2026-06-27.md` |

## Required Actions

1. Inventory the main retained-teacher neural-OT artifact families under `docs/plans/`.
2. Group them into at least:
   - donor/source-survey artifacts,
   - BayesFilter-native fixed-target retained-Sinkhorn first-pass artifacts,
   - annealed LEDH transfer/plumbing artifacts,
   - annealed learned-warmstart repair artifacts,
   - new 2026-06-27 source-faithful governance artifacts.
3. Write a supersession rule that states:
   - older artifacts are not deleted,
   - they remain implementation history / local evidence / repair lineage,
   - they must not be cited as source-faithful Meta OT or UNOT closure evidence.
4. Define the new allowed vocabulary for this lane:
   - `implementation_history_only`,
   - `BayesFilter-native retained-teacher prototype`,
   - `fixed_adaptation`,
   - `extension_or_invention`,
   - `source_faithful` reserved for post-program closure.
5. Point future phases to the 2026-06-27 gap note and source-faithful closure master program as the controlling governance artifacts.

## Skeptical Audit

| Risk | Control |
| --- | --- |
| Reset note reads like deletion or repudiation of all prior work | State explicitly that prior artifacts remain auditably useful as implementation history, local training evidence, and repair lineage. |
| Reset is too weak and still lets old notes be cited as faithful evidence | Write an explicit supersession rule and classification table. |
| Reset overstates what is known about paper failure | State clearly that P0 changes evidence categories only; it does not blame the papers. |
| Important artifact family omitted | Use visible inventory from `rg --files docs/plans | rg 'neural-ot|retained-teacher|learned-warmstart|batched-ledh-pfpf-ot-retained-teacher'`. |

## Gate

P0 passes only when the result artifact includes:
- the classification table,
- the supersession rule,
- the artifact-family inventory,
- and the explicit statement that 2026-06-27 governance artifacts now control future source-faithfulness claims for this lane.
