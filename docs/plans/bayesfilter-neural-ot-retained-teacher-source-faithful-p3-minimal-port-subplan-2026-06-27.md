# P3 Subplan: Minimal Source-Faithful Port Or Decomposition

Date: 2026-06-27

## Status

`DRAFT_SCAFFOLD_AWAITING_P2`

## Dependency

This subplan must not be finalized until P2 chooses a single primary donor route.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can BayesFilter port or faithfully decompose the narrowest runnable retained-teacher route from the chosen donor repo before creating further custom neural-OT machinery? |
| Baseline/comparator | The chosen donor from P2 and its source-anchor audit from P1. |
| Primary pass criterion | A result artifact identifies the minimum donor-core path, separates donor-core logic from donor benchmark scaffolding, and records the first runnable/reconstructible retained-teacher route. |
| Veto diagnostics | Starting with a BayesFilter-specific redesign before donor decomposition; no donor-component map; no distinction between source core and benchmark shell. |
| Explanatory diagnostics | Dependency friction, helper modules, data loaders, and optional performance code. |
| Not concluded | P3 does not yet declare BayesFilter adaptation complete. |
| Required artifact | `docs/plans/bayesfilter-neural-ot-retained-teacher-source-faithful-p3-minimal-port-result-2026-06-27.md` |

## Required Actions

1. Lock the exact donor repo target from P2.
2. Identify the narrowest donor-core path implementing the retained-teacher mechanism.
3. Separate:
   - source core algorithm,
   - source teacher/data machinery,
   - source benchmark/reproduction scaffolding.
4. Record a donor-component map for P4.

## Gate

P3 details finalize only after P2; no custom BayesFilter redesign before this gate passes.
