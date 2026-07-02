# P0 Result: Governance Reset And Retained-Teacher Neural-OT Evidence Boundary

Date: 2026-06-27

## Status

`PASS_P0_GOVERNANCE_RESET_READY_FOR_P1`

## Decision

`PASS_P0_GOVERNANCE_RESET_READY_FOR_P1`

BayesFilter's existing retained-teacher neural-OT artifacts are now explicitly classified under the new source-faithful closure program.

They are **not deleted** and they are **not repudiated**.

They remain useful as:
- implementation history,
- BayesFilter-native retained-teacher exploration,
- local training / heldout evidence,
- annealed-route transfer and repair lineage,
- and sources of known failure modes.

They must **not** be cited as evidence that BayesFilter has already completed a source-faithful Meta OT or UNOT implementation.

The controlling governance artifacts for future faithfulness claims in this lane are now:
- `docs/plans/bayesfilter-neural-ot-retained-teacher-source-faithfulness-gap-note-2026-06-27.md`
- `docs/plans/bayesfilter-neural-ot-retained-teacher-source-faithful-closure-master-program-2026-06-27.md`

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can BayesFilter reset the retained-teacher neural-OT claim boundary so older neural-OT artifacts cannot be accidentally cited as source-faithful Meta OT or UNOT evidence before donor audit, donor choice, and port-first closure occur? |
| Baseline/comparator | Existing retained-teacher neural-OT plans/results from 2026-06-18, batched annealed transfer artifacts from 2026-06-18, retained-teacher LEDH master/repair artifacts from 2026-06-25 and 2026-06-26, plus the new 2026-06-27 gap note and source-faithful closure master program. |
| Primary pass criterion | A governance result artifact lists the main historical neural-OT artifacts, classifies them as implementation history / BayesFilter-native evidence / repair lineage rather than source-faithful closure evidence, and states the supersession rule for future faithfulness claims. |
| Veto diagnostics | No deletion; no overwriting old results; older retained-teacher or annealed notes left implicitly promotable as source-faithful evidence; major 2026-06-18 and 2026-06-26 artifact families omitted. |
| Explanatory diagnostics | Artifact counts, family grouping, and route labels only. |
| Not concluded | P0 does not choose the donor, does not port code, and does not prove paper faithfulness. |

## Supersession Rule

Effective for the retained-teacher neural-OT lane:

1. Older neural-OT artifacts are **not** deleted.
2. Older neural-OT artifacts remain usable as:
   - implementation history,
   - BayesFilter-native retained-teacher prototype evidence,
   - local training or heldout diagnostics,
   - annealed-route transfer/plumbing lineage,
   - repair lineage.
3. Older neural-OT artifacts must **not** be cited as evidence that BayesFilter has already reached:
   - `source_faithful Meta OT closure`, or
   - `source_faithful UNOT closure`.
4. Future documents in this lane must classify major routes using the vocabulary:
   - `implementation_history_only`,
   - `BayesFilter-native retained-teacher prototype`,
   - `fixed_adaptation`,
   - `extension_or_invention`,
   - `source_faithful`.
5. `source_faithful` is reserved for post-program artifacts that have passed donor audit, donor choice, donor decomposition/port, and faithfulness audit.

## Artifact Family Classification

### A. Donor / Survey / Fit / Governance Inputs

| Artifact family | Classification | Allowed future use |
| --- | --- | --- |
| `docs/plans/bayesfilter-neural-ot-source-code-availability-ledger-2026-06-18.md` | `IMPLEMENTATION_GOVERNANCE_INPUT_ONLY` | Source availability evidence; not a faithfulness closeout artifact |
| `docs/plans/bayesfilter-neural-ot-implementation-fit-note-2026-06-18.md` | `IMPLEMENTATION_GOVERNANCE_INPUT_ONLY` | Donor-fit / adaptation evidence; not a faithfulness closeout artifact |
| `docs/plans/bayesfilter-neural-ot-implementation-handoff-memo-2026-06-18.md` | `IMPLEMENTATION_HISTORY_ONLY` | Evidence of the earlier BayesFilter-native sequencing choice |
| `docs/plans/bayesfilter-neural-ot-survey-closeout-reset-memo-2026-06-18.md` and related survey notes | `IMPLEMENTATION_GOVERNANCE_INPUT_ONLY` | Survey and ranking context only |

### B. BayesFilter-Native Fixed-Target Retained-Sinkhorn First-Pass Family

| Artifact family | Classification | Allowed future use |
| --- | --- | --- |
| `docs/plans/bayesfilter-neural-ot-retained-teacher-first-pass-implementation-plan-2026-06-18.md` | `BAYESFILTER_NATIVE_RETAINED_TEACHER_PROTOTYPE` | Historical BayesFilter-native first-pass design; not source-faithful donor closure |
| `docs/plans/bayesfilter-neural-ot-retained-teacher-teacher-data-*.md` | `BAYESFILTER_NATIVE_RETAINED_TEACHER_PROTOTYPE` | Local teacher-data lineage and diagnostics only |
| `docs/plans/bayesfilter-neural-ot-retained-teacher-heldout-eval-*.md` | `BAYESFILTER_NATIVE_RETAINED_TEACHER_PROTOTYPE` | Local heldout evidence only |
| `docs/plans/bayesfilter-neural-ot-retained-teacher-low-budget-*.md` | `BAYESFILTER_NATIVE_RETAINED_TEACHER_PROTOTYPE` | Local low-budget evidence only |
| `docs/plans/bayesfilter-neural-ot-retained-teacher-sv-*.md` and `range-bearing-*.md` | `BAYESFILTER_NATIVE_RETAINED_TEACHER_PROTOTYPE` | Cross-envelope diagnostics only |

These artifacts may be cited as evidence that BayesFilter built and tested a local retained-teacher prototype. They may not be cited as proof of source-faithful Meta OT or UNOT closure.

### C. Batched Annealed LEDH Transfer / Plumbing Family

| Artifact family | Classification | Allowed future use |
| --- | --- | --- |
| `docs/plans/batched-ledh-pfpf-ot-retained-teacher-gpu-transfer-plan-2026-06-18.md` | `EXTENSION_OR_INVENTION_HISTORY_ONLY` | Historical transfer/plumbing evidence only |
| Early batched warm-start benchmark artifacts tied to the transfer pass | `EXTENSION_OR_INVENTION_HISTORY_ONLY` | Historical route-transfer context only |

This family is explicitly not source-faithful closure evidence because the transfer pass itself marked training as `N/A` and treated the route as an annealed transfer/plumbing branch.

### D. Annealed Learned-Warmstart Repair Family

| Artifact family | Classification | Allowed future use |
| --- | --- | --- |
| `docs/plans/bayesfilter-ledh-pfpf-ot-retained-teacher-neural-ot-master-program-2026-06-25.md` and phase artifacts | `REPAIR_LINEAGE_ONLY` | Historical retained-teacher annealed-route program lineage |
| `docs/plans/bayesfilter-ledh-pfpf-ot-retained-teacher-learned-warmstart-reset-memo-2026-06-26.md` | `REPAIR_LINEAGE_ONLY` | Evidence that learned mode required repair before interpretation |
| `docs/plans/bayesfilter-ledh-pfpf-ot-retained-teacher-learned-warmstart-repair-master-program-2026-06-26.md` | `REPAIR_LINEAGE_ONLY` | Evidence of the annealed repair sequence; not source-faithful donor closure |
| Phase A/B/C subplans from 2026-06-26 | `REPAIR_LINEAGE_ONLY` | Target-object / dataset / checkpoint governance for the annealed branch |

These artifacts may be cited as evidence that the annealed branch was incomplete and needed repair. They may not be cited as proof that donor-faithful retained-teacher implementation has already been achieved.

### E. Active 2026-06-27 Source-Faithful Governance Family

| Artifact family | Classification | Allowed future use |
| --- | --- | --- |
| `docs/plans/bayesfilter-neural-ot-retained-teacher-source-faithfulness-gap-note-2026-06-27.md` | `ACTIVE_GOVERNANCE_ARTIFACT` | Governing gap/policy note |
| `docs/plans/bayesfilter-neural-ot-retained-teacher-source-faithful-closure-master-program-2026-06-27.md` | `ACTIVE_GOVERNANCE_ARTIFACT` | Governing master program |
| `docs/plans/bayesfilter-neural-ot-retained-teacher-source-faithful-p0-*.md` and later P1-P6 artifacts | `ACTIVE_PROGRAM_ARTIFACT` | Active closure program artifacts |

## Inventory Snapshot

Visible inventory command used:

```bash
rg --files docs/plans | rg 'neural-ot|retained-teacher|learned-warmstart|batched-ledh-pfpf-ot-retained-teacher|source-faithful-closure|source-faithfulness-gap-note'
```

The main inventoried families visible in the current dialogue were:
- donor/source survey and implementation-fit notes,
- fixed-target retained-teacher first-pass notes,
- cross-envelope and low-budget notes,
- batched annealed transfer plan,
- retained-teacher annealed repair and phase notes,
- the new 2026-06-27 gap and master-program artifacts.

## Required Claim Boundary Going Forward

From this point on, if a future note in this lane wants to claim source faithfulness, it must point to:
1. donor paper anchors,
2. donor repo anchors,
3. a chosen primary donor decision,
4. donor decomposition / minimal port artifacts,
5. a BayesFilter adapter note,
6. and a faithfulness audit table.

Without those, the correct labels remain:
- `implementation_history_only`,
- `BayesFilter-native retained-teacher prototype`,
- `fixed_adaptation`,
- or `extension_or_invention`.

## What P0 Does Not Conclude

P0 does **not** conclude:
- that Meta OT or UNOT are correct for BayesFilter,
- that they are incorrect,
- that the earlier BayesFilter-native work was worthless,
- that the annealed branch can never work,
- or that any donor has yet been chosen.

P0 changes **evidence categories**, not paper truth.

## Next Step

Advance to P1 donor source-anchor audit under:
- `docs/plans/bayesfilter-neural-ot-retained-teacher-source-faithful-p1-donor-anchor-audit-subplan-2026-06-27.md`

P1 will inspect Meta OT and UNOT at the paper+repo level before any further custom retained-teacher implementation proceeds.
