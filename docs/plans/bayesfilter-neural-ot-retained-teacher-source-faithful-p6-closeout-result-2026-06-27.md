# P6 Result: Closeout And Extension Boundary

Date: 2026-06-27

## Status

`FIXED_ADAPTATION_ROUTE_CLOSED_BUT_NOT_FULLY_SOURCE_FAITHFUL`

## Decision

`FIXED_ADAPTATION_ROUTE_CLOSED_BUT_NOT_FULLY_SOURCE_FAITHFUL`

The 2026-06-27 source-faithful closure program reaches the following route verdict:

- BayesFilter now has a **governed and audited classification** of the retained-teacher neural-OT lane.
- The current fixed-target retained-Sinkhorn route is the correct base adaptation substrate.
- That route is **not yet fully source-faithful Meta OT**, but it is now classified as a **fixed adaptation route with major extension components**.
- The current annealed four-potential branch remains **extension_or_invention**, not first-route source-faithful closure evidence.

This means the program does **not** end in full source-faithful closure yet. It ends in a much sharper and safer execution boundary.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | After donor audit, port/decomposition, adapter design, and faithfulness audit, what exactly has BayesFilter closed, and what extension work is now allowed or still blocked? |
| Baseline/comparator | P5 faithfulness audit result and all prior program artifacts. |
| Primary pass criterion | A closeout result states one route verdict, one extension boundary, and one list of still-blocked claims/actions. |
| Veto diagnostics | Ambiguous verdict; reopening annealed extension or custom invention without a faithfulness classification; usefulness claims that outrun the audit verdict. |
| Explanatory diagnostics | Local metrics, engineering convenience, and follow-on experiment ideas. |
| Not concluded | P6 does not by itself prove the paper's effectiveness on all BayesFilter routes. |

## Final Route Verdict

### 1. Fixed-target retained-Sinkhorn route
**Verdict:** `FIXED_ADAPTATION_ROUTE_CLOSED_BUT_NOT_FULLY_SOURCE_FAITHFUL`

Meaning:
- this route is the correct BayesFilter substrate for future donor-faithful retained-teacher work,
- it already preserves the donor's broad retained-teacher deployment semantics,
- but it still diverges materially from donor-core Meta OT on the learned-object and training-objective side.

### 2. Annealed four-potential route
**Verdict:** `CUSTOM_EXTENSION_REQUIRED_SOURCE_FAITHFUL_CLOSURE_FAILED`

Meaning:
- this route is outside the first Meta OT-faithful closure path,
- it remains a separate BayesFilter extension/invention branch,
- and it must not be treated as source-faithful donor evidence.

## What Work Is Allowed Next

### Allowed immediately
1. **Meta OT-aligned refit of the fixed-target retained-Sinkhorn route**
   - redesign the student to predict one donor-style dual half,
   - recover the complementary half teacher-consistently,
   - add a donor-faithful objective-based training path,
   - preserve corrected retained Sinkhorn deployment and replay/residual audits.

2. **BayesFilter internal donor porting / modification work**
   - internal academic port/decomposition/modification is allowed under the user-stated internal-use boundary,
   - public redistribution remains out of scope.

3. **Explicitly labeled fixed adaptations**
   - weighted particle-cloud representation,
   - TensorFlow/TFP implementation,
   - BayesFilter manifests / replay diagnostics,
   - all allowed so long as they remain explicitly labeled as fixed adaptations rather than silently called source-faithful.

### Deferred but not forbidden
1. **UNOT reconsideration**
   - allowed only if a later blocker or adapter analysis shows it is the better primary donor.

2. **Annealed retained-teacher route**
   - allowed only as a later extension branch after the fixed-target Meta OT-aligned route is refit more faithfully, or with an explicit decision to pursue a separate extension program.

## What Remains Blocked

### Blocked claims
- claiming that BayesFilter already has a source-faithful Meta OT implementation,
- claiming that the annealed four-potential route is first-route donor-faithful,
- claiming donor-paper failure from the current adaptation gap,
- using current local low-budget or heldout results as a substitute for source-faithfulness.

### Blocked actions
- silently continuing with the current full dual-pair student path while calling it donor-faithful Meta OT,
- treating the current annealed branch as the default faithful route,
- reopening broad custom neural-OT invention without classifying it explicitly as `extension_or_invention`.

## Recommended Immediate Follow-On Program

The next practical implementation program should now be narrower than the work done so far:

### Target
Refit the current fixed-target retained-Sinkhorn route toward the Meta OT donor-core contract.

### Required implementation delta
1. Replace or augment the current dual-pair student with a **single-dual-half predictor**.
2. Add **teacher-side complementary recovery** rather than direct free prediction of both halves.
3. Add a **donor-faithful objective-based training path** alongside or ahead of pure pair-regression.
4. Preserve the current strong replay/residual heldout evaluation contract.

### Suggested file focus
- `experiments/dpf_implementation/tf_tfp/resampling/sinkhorn_warmstart_student_tf.py`
- `experiments/dpf_implementation/tf_tfp/runners/run_retained_teacher_sinkhorn_teacher_data_tf.py`
- `experiments/dpf_implementation/tf_tfp/runners/run_retained_teacher_sinkhorn_heldout_eval_tf.py`

## Final Boundary Statement

The most important closeout outcome is this:

> BayesFilter should continue from the fixed-target retained-Sinkhorn lane, not from the annealed lane, if the goal is source-faithful Meta OT closure.

The annealed branch is not deleted and not invalidated as research history, but it is not the correct first faithfulness route.

## What P6 Does Not Conclude

P6 does **not** conclude:
- that the current fixed-target route is already good enough scientifically,
- that Meta OT is guaranteed to work well after refit,
- that UNOT should never be revisited,
- or that the annealed route has no future value.

P6 concludes only that the route boundary is now explicit and safer:
- fixed-target retained-Sinkhorn is the correct Meta OT adaptation substrate,
- annealed four-potential work is a later extension,
- and BayesFilter must stop blurring those categories.
