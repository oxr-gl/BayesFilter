# P4 Result: BayesFilter Adapter Design

Date: 2026-06-27

## Status

`PASS_P4_ADAPTER_BOUNDARY_READY_FOR_P5`

## Decision

`PASS_P4_ADAPTER_BOUNDARY_READY_FOR_P5`

BayesFilter now has a narrow adapter boundary for the chosen Meta OT donor-core route.

The first source-faithful BayesFilter adaptation target is:
- a **fixed-target retained Sinkhorn route**,
- with a **single donor-style predicted dual half** as the primary learned object,
- with **teacher-side complementary dual recovery**,
- and with **corrective retained Sinkhorn** preserved at deployment.

The current BayesFilter fixed-target retained-Sinkhorn implementation can support this route, but its present student interface and teacher-data representation will require explicit adapter changes before the route can be called source-faithful to Meta OT.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | After donor-core decomposition, what is the narrowest TensorFlow/TFP BayesFilter adapter that preserves source semantics while clearly marking fixed adaptations versus extensions? |
| Baseline/comparator | P3 donor-component map and the retained-teacher chapter definition. |
| Primary pass criterion | A result artifact maps donor objects and functions into BayesFilter interfaces while classifying every change as `fixed_adaptation` or `extension_or_invention`. |
| Veto diagnostics | Silent object substitution; silent route change; mixing fixed-target retained Sinkhorn and annealed transport semantics without classification. |
| Explanatory diagnostics | Data representation convenience, helper abstractions, and code-organization trade-offs. |
| Not concluded | P4 does not yet prove source faithfulness; it defines the adapter boundary. |

## Adapter Target Chosen

### First faithful adaptation target
The donor-faithful first adaptation target is:
- **fixed-target retained Sinkhorn only**,
- **not** the annealed LEDH route,
- **not** the four-potential annealed warm-start route,
- **not** a direct plan predictor,
- **not** a two-half arbitrary dual regressor.

This preserves the donor-core Meta OT logic as closely as possible in BayesFilter.

## Paper → Donor → BayesFilter Mapping

| Role | Meta OT donor-core | Current BayesFilter retained-Sinkhorn route | P4 classification |
| --- | --- | --- | --- |
| Problem family | repeated discrete entropic OT problems `(a,b)` under fixed geometry | repeated retained Sinkhorn teacher problems over weighted particle clouds and equal-weight target | `fixed_adaptation` |
| Learned object | single dual half `f_pred` | current student predicts canonicalized pair `(log_u, log_v)` | `extension_or_invention` relative to Meta OT |
| Complementary-state recovery | `g_from_f(...)` via teacher-side update | currently no donor-faithful one-half recovery path; student predicts both halves directly | `extension_or_invention` |
| Teacher-side training objective | objective-based donor dual objective | current branch mainly uses teacher-state regression plus heldout replay checks | `extension_or_invention` unless objective-based donor loss is restored |
| Corrective teacher deployment | predicted dual state warm-starts corrective Sinkhorn | current BayesFilter route already preserves corrective Sinkhorn deployment | `source_faithful` at the deployment-semantic level |
| Deployment object | corrected teacher output | corrected teacher barycentric cloud / residual contract | `source_faithful` at the object level |

## Current BayesFilter Components Relevant To The Adapter

### Current student path
Current BayesFilter fixed-target retained-Sinkhorn student helper:
- `experiments/dpf_implementation/tf_tfp/resampling/sinkhorn_warmstart_student_tf.py`

Current behavior:
- `SinkhornWarmStartStudentTF` predicts **two outputs** and returns a canonicalized `SinkhornLogStateTF(log_u, log_v)`.
- `teacher_state_loss_tf(...)` compares the full canonicalized dual pair.

This is BayesFilter-native and valid as a local retained-teacher prototype, but it is **not yet donor-faithful** to Meta OT's single-half route.

### Current teacher-data path
Current teacher-data runner:
- `experiments/dpf_implementation/tf_tfp/runners/run_retained_teacher_sinkhorn_teacher_data_tf.py`

Current behavior:
- captures weighted particle clouds,
- stores canonicalized teacher dual pair `(canonical_log_u, canonical_log_v)`,
- stores teacher barycentric particles and residual diagnostics.

This is close enough to support a donor-faithful adaptation, but it currently over-specifies the latent target relative to Meta OT's single-half prediction route.

### Current heldout-eval path
Current heldout evaluation runner:
- `experiments/dpf_implementation/tf_tfp/runners/run_retained_teacher_sinkhorn_heldout_eval_tf.py`

Current behavior:
- predicts full dual state,
- runs corrective retained Sinkhorn,
- evaluates corrected replay against zero-init.

This means the **deployment-semantic** side is already aligned with retained-teacher Meta OT logic. The mismatch is mainly in the learned-object and training-objective side.

## Fixed Adaptations Required For A Meta OT-Faithful BayesFilter Route

These changes are classified as **fixed adaptations**, not free invention, because they are needed to translate donor semantics into BayesFilter's project conventions.

### 1. Replace the donor input representation with BayesFilter's weighted particle-cloud representation
Meta OT's donor-core discrete route consumes repeated OT problems over discrete measures `(a,b)` under a fixed geometry.

BayesFilter adaptation:
- input becomes weighted particle-cloud retained-teacher OT problems,
- source marginal comes from normalized particle weights,
- target marginal remains equal-weight,
- geometry/cost comes from the BayesFilter retained Sinkhorn teacher.

This is a `fixed_adaptation` because it changes the representation of the OT problem, but not the donor-core semantics: repeated entropic OT problems, learned warm start, corrective teacher solve.

### 2. Preserve TensorFlow/TFP implementation rather than JAX/OTT runtime
BayesFilter's implementation stack remains TensorFlow / TensorFlow Probability.

This is a `fixed_adaptation` because it changes framework/runtime but not the retained-teacher algorithmic contract.

### 3. Keep BayesFilter teacher-data manifests and heldout replay checks
BayesFilter's manifest, reproducibility, and heldout replay diagnostics are local governance requirements.

These are `fixed_adaptation` because they strengthen auditability without changing the donor-core semantics.

## Extension / Invention Boundaries

The following are **not** source-faithful Meta OT by default and must be treated as explicit extension/invention unless a later audit proves otherwise.

### 1. Predicting both `log_u` and `log_v` directly
Current BayesFilter student predicts both halves directly.

Relative to the donor-core Meta OT route, this is an `extension_or_invention` because the donor route predicts one half and recovers the other teacher-consistently.

### 2. Canonicalized dual-pair regression as the primary learning story
Current BayesFilter teacher-data and student loss support full dual-pair regression.

Relative to donor-core Meta OT objective-based amortization, this is an `extension_or_invention` unless BayesFilter adds the donor-style objective-based route or proves a faithful one-half reduction.

### 3. Reopening the annealed four-potential route now
The annealed learned-warmstart route predicts `(a_y, b_x, a_x, b_y)` and belongs to a later route family.

Relative to Meta OT donor-core retained Sinkhorn, that is an `extension_or_invention`, not the first faithful target.

## Recommended First Adapter Contract

The first BayesFilter adapter that stays closest to Meta OT should:
1. take BayesFilter retained-Sinkhorn teacher problems as repeated discrete OT instances,
2. predict **one canonicalized dual half** only,
3. recover the complementary half through the teacher-side update rule,
4. keep corrective retained Sinkhorn at deployment,
5. judge success by corrected teacher replay/residuals, not latent loss alone.

## Minimal Code/Artifact Direction Implied By P4

To move BayesFilter toward Meta OT faithfulness, the first local adaptation should prefer:
- revising the fixed-target retained-Sinkhorn student route,
- not the annealed route,
- and replacing or augmenting the current dual-pair student path with a donor-faithful one-half prediction path.

That suggests the natural first adaptation targets are:
- `experiments/dpf_implementation/tf_tfp/resampling/sinkhorn_warmstart_student_tf.py`
- `experiments/dpf_implementation/tf_tfp/runners/run_retained_teacher_sinkhorn_teacher_data_tf.py`
- `experiments/dpf_implementation/tf_tfp/runners/run_retained_teacher_sinkhorn_heldout_eval_tf.py`

## Updated Blocker Boundary

The earlier license blocker is now reduced by explicit user direction:
- internal academic modification and porting are allowed,
- public distribution is not the current use case.

So P4 no longer treats donor porting as blocked for internal academic work.

The remaining technical blocker is not license. It is **semantic discipline**:
- BayesFilter must not keep calling the current dual-pair / annealed routes Meta OT-faithful unless the learned-object and training-objective boundary are corrected.

## What P4 Does Not Conclude

P4 does **not** conclude:
- that the current BayesFilter student is already Meta OT-faithful,
- that the current annealed route is the right first donor-faithful target,
- or that one-half donor prediction is already implemented locally.

P4 only fixes the adaptation boundary and deviation classes.

## Next Step

Advance to P5 under:
- `docs/plans/bayesfilter-neural-ot-retained-teacher-source-faithful-p5-faithfulness-audit-subplan-2026-06-27.md`

P5 must now classify the current BayesFilter retained-Sinkhorn route and the current annealed route precisely as `source_faithful`, `fixed_adaptation`, or `extension_or_invention` relative to the Meta OT donor-core contract.
