# P4 Subplan: BayesFilter Adapter Design

Date: 2026-06-27

## Status

`DRAFT_SCAFFOLD_AWAITING_P3`

## Dependency

This subplan must not be finalized until P3 records the donor-core decomposition.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | After donor-core decomposition, what is the narrowest TensorFlow/TFP BayesFilter adapter that preserves source semantics while clearly marking fixed adaptations versus extensions? |
| Baseline/comparator | P3 donor-component map and the retained-teacher chapter definition. |
| Primary pass criterion | A result artifact maps donor objects and functions into BayesFilter interfaces while classifying every change as `fixed_adaptation` or `extension_or_invention`. |
| Veto diagnostics | Silent object substitution; silent route change; mixing fixed-target retained Sinkhorn and annealed transport semantics without classification. |
| Explanatory diagnostics | Data representation convenience, helper abstractions, and code-organization trade-offs. |
| Not concluded | P4 does not yet prove source faithfulness; it defines the adapter boundary. |
| Required artifact | `docs/plans/bayesfilter-neural-ot-retained-teacher-source-faithful-p4-adapter-design-result-2026-06-27.md` |

## Required Actions

1. Define the BayesFilter counterpart for each donor-core object.
2. Distinguish route boundaries explicitly.
3. Classify each adaptation as `fixed_adaptation` or `extension_or_invention`.
4. Freeze the adapter boundary for P5 faithfulness audit.

## Gate

P4 details finalize only after P3 donor decomposition; no faithfulness claim before P5.
