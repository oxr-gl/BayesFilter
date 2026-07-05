# P5 Result: Closeout And Next Boundary

Date: 2026-06-28

## Status

`DONOR_ALIGNED_REFIT_IMPLEMENTED_BUT_NOT_PROMOTED_ON_CURRENT_HELDOUT_RULE`

## Decision

`DONOR_ALIGNED_REFIT_IMPLEMENTED_BUT_NOT_PROMOTED_ON_CURRENT_HELDOUT_RULE`

The Meta OT-aligned fixed-target retained-Sinkhorn refit program reaches the following closeout boundary:

1. The donor-aligned one-half route is now **implemented**.
2. The donor-style objective-based training path is now **implemented**.
3. The corrected retained-Sinkhorn deployment path is **preserved**.
4. The route is therefore materially closer to the Meta OT donor-core contract than the earlier local dual-pair route.
5. But under the current tiny heldout dataset and current binding primary-budget rule, the new route is **not promoted** because it still loses to zero-init at the primary corrective budget.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | After implementing the Meta OT-aligned one-half refit, what exactly has been achieved, and what should happen next given the heldout primary-budget failure? |
| Baseline/comparator | The pre-refit local retained-teacher route, zero-init retained Sinkhorn baseline, and the new donor-aligned one-half route. |
| Primary pass criterion | A closeout result states whether the refit landed the intended donor-aligned mechanics and whether it is promoted or blocked under the current heldout rule. |
| Veto diagnostics | Claiming success despite primary-budget heldout failure; confusing semantic donor alignment with local empirical promotion; reopening annealed route as fallback without a separate decision. |
| Explanatory diagnostics | Low-budget gains, train objective improvement, residual finiteness, and small-data limitations. |
| Not concluded | No donor-paper failure claim, no annealed-route promotion, no broad usefulness claim. |

## What Was Achieved

### Achieved technically
- one-half prediction route (`canonical_log_u`) added,
- teacher-side complementary recovery path added,
- donor-style objective-based loss path added,
- teacher-data manifest annotated for the donor-aligned route,
- updated heldout evaluation executed successfully enough to produce a decision artifact.

### Achieved scientifically / methodologically
- the fixed-target retained-Sinkhorn route is now closer to the Meta OT donor-core contract,
- the donor-faithful implementation question has been made sharper and more testable,
- BayesFilter now has a concrete donor-aligned path instead of only conceptual alignment.

## What Was Not Achieved

- no empirical promotion under the current heldout primary-budget rule,
- no evidence that the donor-aligned route should replace zero-init at the binding `K_corr=20` rung,
- no evidence that the annealed branch is rescued by this refit,
- no full source-faithful closure claim for the overall BayesFilter route family.

## Route Verdict After The Refit Program

### Fixed-target retained-Sinkhorn lane
**Verdict:** `DONOR_ALIGNED_BUT_LOCALLY_NON_PROMOTED`

Meaning:
- this lane is still the correct substrate for donor-faithful work,
- it is more faithful now than before,
- but it is not yet justified as a promoted local performer under the current heldout rule.

### Annealed four-potential lane
**Verdict:** unchanged from the earlier closure program:
- `extension_or_invention`
- not part of the first donor-faithful success case

## Most Supported Explanation Of The Outcome

The strongest interpretation remains:
- the donor-aligned route is now implemented coherently,
- but the current local heldout contract is dominated by a tiny dataset and a primary budget where zero-init is already essentially exact,
- so the route may still be meaningful as a donor-faithful implementation step even though it is not promoted as the better local heldout performer.

## Justified Next Action

The next justified action is **not** to jump back to the annealed route.

The next justified action is to strengthen the fixed-target donor-aligned evidence base before any new route expansion. Concretely, the next smallest discriminating artifact should be one of:
1. expand the donor-aligned teacher-data envelope while keeping the one-half route fixed,
2. run a revised heldout ladder where the primary criterion is not trivially saturated by zero-init at high corrective budget,
3. add a focused donor-aligned comparison artifact that separates:
   - semantic donor faithfulness,
   - local low-budget usefulness,
   - primary-budget non-promotion.

## What Remains Blocked

- claiming that the donor-aligned refit is already the winning local route,
- using this result to justify the annealed branch,
- using this result to claim Meta OT failure,
- reopening broad neural-OT invention without explicitly classifying it.

## Final Boundary Statement

The key closeout boundary is:

> BayesFilter should continue refining and evaluating the fixed-target donor-aligned retained-Sinkhorn lane if it wants stronger Meta OT-faithful evidence. The annealed four-potential branch remains out of scope for that claim.

## What P5 Does Not Conclude

P5 does **not** conclude:
- that the donor-aligned route is a dead end,
- that the paper is wrong,
- that the old dual-pair route was better in a source-faithful sense,
- or that the next step should be donor switching or annealed-route promotion.

It concludes only that the donor-aligned route is now implemented but not yet promoted under the current local heldout rule.
