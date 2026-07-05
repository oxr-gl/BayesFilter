# P2 Result: Teacher-Data And Manifest Refit

Date: 2026-06-27

## Status

`PASS_P2_TEACHER_DATA_CONTRACT_READY_FOR_P3`

## Decision

`PASS_P2_TEACHER_DATA_CONTRACT_READY_FOR_P3`

The retained-Sinkhorn teacher-data contract is now refit for the Meta OT-aligned route.

### New primary learned target
The controlling learned target for the refit program is now:
- `teacher.canonical_log_u`

### Supporting but non-primary latent fields
The teacher-data artifact may still preserve:
- `teacher.canonical_log_v`
- raw `final_log_u`, `final_log_v`

but these are now:
- audit/debugging support fields,
- not the primary donor-aligned learned target.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | How should the current retained-Sinkhorn teacher-data path be refit so it supports Meta OT-aligned one-half training while preserving BayesFilter manifests, heldout splits, and replay diagnostics? |
| Baseline/comparator | Current teacher-data runner and the P1 one-half target/recovery contract. |
| Primary pass criterion | A result artifact freezes the updated teacher-data fields, manifest fields, split policy, and replay/recovery checks required before student refit. |
| Veto diagnostics | Losing teacher replay artifacts; losing manifests or reproducibility digests; keeping only pair-regression-oriented targets; ambiguous relation between stored half-target and recovered complementary half. |
| Explanatory diagnostics | Dataset size, file layout, and compactness only. |
| Not concluded | P2 does not yet refit the student module. |

## Updated Teacher-Data Contract

### Primary learned target fields
The refit route must treat these as primary target fields:
- `particles`
- `weights`
- `epsilon`
- `teacher.canonical_log_u`
- `teacher.canonical_gauge_policy`

### Required replay / corrected-output support fields
The artifact must also continue to preserve:
- `teacher.barycentric_particles`
- `teacher.diagnostics`
- source/target weights or enough information to reconstruct the retained teacher route consistently

These remain necessary because donor faithfulness does **not** replace BayesFilter's requirement to judge corrected replay/residual behavior after deployment.

### Supporting latent audit fields
The artifact may continue to store:
- `teacher.canonical_log_v`
- `teacher.final_log_u`
- `teacher.final_log_v`
- `teacher.final_gauge_policy`

But these fields are now classified as:
- secondary latent audit support,
- not the controlling learned target for the donor-aligned refit.

## Updated Manifest Contract

The teacher-data manifest for the refit route must record at minimum:
- route identifier for the fixed-target retained-Sinkhorn donor-aligned lane,
- target-object identifier making clear that the learned target is `canonical_log_u`,
- gauge policy (`mean_log_u_zero`),
- split counts and split policy,
- teacher epsilon / tolerance / iteration budget,
- reproducibility digest,
- artifact paths,
- existing BayesFilter replay / residual support fields.

### Required route note
The manifest/result must say clearly that:
- the route is **Meta OT-aligned one-half retained-Sinkhorn refit**,
- not the older BayesFilter-native dual-pair route,
- and not the annealed four-potential route.

## Recovery / Replay Contract

The artifact must support the following deployment and evaluation story:
1. read `particles`, `weights`, `epsilon`, and `teacher.canonical_log_u`,
2. predict the same one-half object during training/eval,
3. recover the complementary half teacher-consistently,
4. run corrective retained Sinkhorn,
5. compare corrected replay against `teacher.barycentric_particles` and teacher diagnostics.

This is the minimum route BayesFilter must support before P3 student/objective refit can be judged coherently.

## Split Policy

The current deterministic train / heldout split structure remains acceptable and should be preserved.

However, future teacher-data artifacts for the refit route must explicitly distinguish:
- **old dual-pair BayesFilter-native artifacts**
- versus **new Meta OT-aligned one-half artifacts**

so later training runs cannot accidentally mix the two target contracts.

## Compatibility Rule

Older teacher-data artifacts may remain readable for historical comparison, but they must not silently define the new donor-aligned route.

A Meta OT-aligned refit artifact should therefore carry an explicit route/target identifier distinguishing it from the older pair-regression contract.

## What P2 Does Not Conclude

P2 does **not** conclude:
- that the current teacher-data code already implements the one-half route,
- that `canonical_log_v` is useless,
- that the old pair-based artifacts should be deleted,
- or that the student refit is complete.

P2 only freezes the new teacher-data and manifest contract so the student/objective refit can proceed without ambiguity.

## Next Step

Advance to:
- `docs/plans/bayesfilter-neural-ot-metaot-refit-p3-student-objective-subplan-2026-06-27.md`

P3 will now refit the current student path and training story toward one-half prediction plus donor-faithful objective-based training.
