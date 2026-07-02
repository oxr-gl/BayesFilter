# P5 Result: Faithfulness Audit

Date: 2026-06-27

## Status

`PASS_P5_ROUTE_CLASSIFICATION_READY_FOR_P6`

## Decision

`PASS_P5_ROUTE_CLASSIFICATION_READY_FOR_P6`

The current BayesFilter retained-teacher routes are now classified relative to the chosen Meta OT donor-core contract.

### Route verdicts
- **Current fixed-target retained-Sinkhorn route:** `FIXED_ADAPTATION_WITH_MAJOR_EXTENSION_COMPONENTS`
- **Current annealed four-potential route:** `EXTENSION_OR_INVENTION`
- **Current 2026-06-27 program status:** source-faithful closure **not yet achieved**

This is not a paper-failure verdict. It is a route-classification verdict.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the resulting BayesFilter retained-teacher route count as source-faithful, fixed adaptation, or extension/invention relative to the chosen donor? |
| Baseline/comparator | Meta OT paper anchors, Meta OT donor-core decomposition from P3, and the P4 adapter design. |
| Primary pass criterion | A paper→repo→BayesFilter obligation table classifies every implementation-relevant deviation and supports a single route verdict. |
| Veto diagnostics | Missing donor anchors; missing deviation table; calling the route faithful while major semantic deviations remain unlabeled. |
| Explanatory diagnostics | Local training results, runtime, and convenience differences. |
| Not concluded | P5 does not claim broad usefulness or production readiness. |

## Meta OT Donor-Core Contract Used For Audit

The chosen donor-core contract from P3 is:
1. repeated discrete entropic OT problems,
2. fixed teacher-side geometry,
3. predict **one dual half** `f_pred`,
4. recover the complementary dual half `g_pred` from the teacher-side update rule,
5. train by the teacher's own dual objective,
6. deploy through corrective Sinkhorn warm-starting.

Any BayesFilter route is classified against that contract.

## Paper → Repo → BayesFilter Obligation Table

| Obligation | Meta OT donor-core anchor | Current BayesFilter fixed-target retained-Sinkhorn route | Current annealed four-potential route | Classification |
| --- | --- | --- | --- | --- |
| Keep a retained entropic OT teacher | Meta OT discrete entropic teacher with corrective Sinkhorn | Yes; fixed-target retained Sinkhorn teacher is preserved | No exact donor match; annealed streaming transport is a different route family | Fixed-target: `source-faithful at teacher-preservation level`; Annealed: `extension_or_invention` |
| Learn a solver-native latent state, not the final plan | predict one dual half `f_pred` | Yes in spirit; predicts a teacher-native latent dual state | Yes in spirit; predicts solver-native warm-start potentials | Fixed-target: `fixed_adaptation`; Annealed: `extension_or_invention` |
| Predict only one dual half and recover the other teacher-consistently | `f_pred` then `g_from_f(...)` | No; current student predicts canonicalized `(log_u, log_v)` directly | No; predicts four annealed latent tensors directly | Fixed-target: `major extension_or_invention component`; Annealed: `extension_or_invention` |
| Use an objective-based teacher-side training objective | donor dual objective | No; current local route primarily supports explicit teacher-state regression plus replay evaluation | No donor-faithful donor-side training route exists yet | Fixed-target: `major extension_or_invention component`; Annealed: `extension_or_invention` |
| Preserve corrective teacher deployment | `eval_discrete.py` warm-starts and still runs corrective Sinkhorn | Yes; corrected retained Sinkhorn deployment exists and is the deployment semantics | Partially analogous but via a different route family and different latent object | Fixed-target: `source-faithful at deployment-semantic level`; Annealed: `extension_or_invention` |
| Deployment object is corrected teacher output | corrected teacher plan/output | Yes; corrected teacher barycentric cloud / residual contract | Yes in local branch terms, but with a different route family | Fixed-target: `fixed_adaptation`; Annealed: `extension_or_invention` |
| Stay in donor route family for the first faithful closure | discrete retained Sinkhorn family | Yes; fixed-target retained Sinkhorn stays in family | No; annealed LEDH branch changes route family | Fixed-target: `fixed_adaptation`; Annealed: `extension_or_invention` |
| Avoid premature donor-semantic branching | donor-core is narrow | Current route already branched by choosing dual-pair regression instead of one-half donor prediction | Current route branched much further into annealed four-potential design | Fixed-target: `fixed_adaptation with major extension`; Annealed: `extension_or_invention` |

## Route Classification Details

### A. Current fixed-target retained-Sinkhorn route
**Verdict:** `FIXED_ADAPTATION_WITH_MAJOR_EXTENSION_COMPONENTS`

#### Why it is not yet fully source-faithful
The route is still not donor-faithful because two major donor-core semantics are missing:
1. **one-half prediction with teacher-side recovery** is not preserved,
2. **objective-based donor training** is not preserved as the central local learning story.

The current route instead:
- predicts a canonicalized full dual pair `(log_u, log_v)`,
- uses teacher-state regression helpers,
- then evaluates corrected replay through retained Sinkhorn.

That means it is closer than the annealed route, but still not a direct Meta OT-faithful closure.

#### Why it is closer than the annealed route
It still preserves:
- retained discrete entropic OT teacher semantics,
- corrected Sinkhorn deployment,
- teacher-native latent-state learning rather than final-plan prediction.

So it is not free invention; it is a constrained BayesFilter adaptation with major extensions relative to the donor core.

### B. Current annealed four-potential route
**Verdict:** `EXTENSION_OR_INVENTION`

#### Why
The current annealed route differs from Meta OT donor-core at too many essential levels:
- different route family (annealed streaming transport rather than donor discrete retained Sinkhorn),
- different learned object `(a_y, b_x, a_x, b_y)` rather than donor one-half dual prediction,
- different training and evaluation closure program,
- different deployment internals.

Even if it remains conceptually retained-teacher in a broad sense, it is not the first source-faithful Meta OT target. It is a later extension branch.

## Most Important Consequence

The current source-faithful closure gap is now sharply localized:
- BayesFilter does **not** need to abandon the fixed-target retained-Sinkhorn lane,
- but it **does** need to refit that lane toward the Meta OT donor-core contract,
- especially on the learned-object and training-objective side.

## What Must Not Be Concluded

1. Do **not** say the current fixed-target route is source-faithful Meta OT.
2. Do **not** say the current annealed route is the first faithful Meta OT adaptation.
3. Do **not** say the current classification means Meta OT is unusable for BayesFilter.
4. Do **not** say the current routes are worthless; the fixed-target route remains useful implementation history and adaptation substrate.
5. Do **not** use low-budget or heldout local wins as a faithfulness substitute.

## Minimum Required Follow-On To Reach Source Faithfulness

For the fixed-target route to move toward source-faithful closure, BayesFilter must at minimum:
1. revise the learned object from donor-incompatible full-pair prediction toward donor-faithful one-half prediction with teacher-side complementary recovery,
2. add or restore a donor-faithful objective-based training path rather than only dual-pair regression,
3. keep corrective retained Sinkhorn deployment and replay/residual audits,
4. rerun the local route under the new donor-aligned contract before claiming faithfulness.

## Next Step

Advance to P6 under:
- `docs/plans/bayesfilter-neural-ot-retained-teacher-source-faithful-p6-closeout-subplan-2026-06-27.md`

P6 must now issue the closeout verdict and state exactly what work is allowed next under the source-faithful closure program.
